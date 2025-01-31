import zipfile
import gradio as gr
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont

def generate_labels_colors(labels):
    np.random.seed(42)
    color_map = dict(
        zip(
            labels,
            list(
                map(
                    lambda i: "# " + "%06x" % np.random.randint(0, 16777215),
                    range(len(labels)),
                )
            ),
        )
    )
    return color_map

def preprocess_image(interpreter, image):
    """Pré-processar a imagem de entrada para alimentar o modelo TFLite"""

    input_details = interpreter.get_input_details()[0]
    model_height, model_width = input_details["shape"][1:3]

    # Redimensionar a imagem
    image_resized = tf.image.resize(image, (model_height, model_width))

    # Normalizar a imagem
    img_array = tf.cast(image_resized, tf.float32) / 255.0

    # Verificar se é necessário escalar e quantizar
    if input_details["dtype"] == tf.uint8:
        input_scale, input_zero_point = input_details["quantization"]
        img_array = img_array / input_scale + input_zero_point
        img_array = tf.cast(img_array, input_details["dtype"])

    # Adicionar dimensão de lote, se necessário
    img_array = tf.expand_dims(img_array, axis=0)

    return img_array


def detect_objects(interpreter, image_array, threshold):
    """Retorna uma lista de resultados de detecção, cada um um dicionário com informações do objeto."""

    interpreter.set_tensor(interpreter.get_input_details()[0]["index"], image_array)
    interpreter.invoke()

    boxes = np.squeeze(
        interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
    )
    classes = np.squeeze(
        interpreter.get_tensor(interpreter.get_output_details()[1]["index"])
    )
    scores = np.squeeze(
        interpreter.get_tensor(interpreter.get_output_details()[2]["index"])
    )
    count = int(
        np.squeeze(interpreter.get_tensor(interpreter.get_output_details()[3]["index"]))
    )
    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                "bounding_box": boxes[i],
                "class_id": classes[i],
                "score": scores[i],
            }
            results.append(result)
    return results

def read_labels_tflite(tflite_model_path):
    with zipfile.ZipFile(tflite_model_path, "r") as archive:
        for file in archive.namelist():
            labels = archive.read(file).decode(encoding="utf-8").split()
    return labels

def load_tflite_model(tflite_model_path):
    # Carrega o modelo TFLite
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()
    return interpreter

def predict(interpreter, labels, image, threshold):
    """Execute a detecção de objetos na imagem de entrada e desenhe os resultados da detecção."""
    colors = generate_labels_colors(labels)
    new_image = image.copy()

    # Load the input image and preprocess it
    preprocessed_image = preprocess_image(interpreter, new_image)

    # Run object detection on the input image
    results = detect_objects(interpreter, preprocessed_image, threshold=threshold)

    # Create a Pillow ImageDraw object
    draw = ImageDraw.Draw(new_image)

    for obj in results:
        # Convert the object bounding box from relative coordinates to absolute
        # coordinates based on the original image resolution
        ymin, xmin, ymax, xmax = obj["bounding_box"]

        xmin = int(xmin * new_image.width)
        xmax = int(xmax * new_image.width)
        ymin = int(ymin * new_image.height)
        ymax = int(ymax * new_image.height)

        # Find the class index of the current object
        class_id = int(obj["class_id"])

        # Draw the bounding box and label on the image
        color = colors[labels[class_id]]
        print(color)
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=str(color), width=2)

        font = ImageFont.truetype("arial.ttf", 12)
        label = f"{labels[class_id]} {round(obj['score'] * 100, 2)}%"

        text_position = (xmin, ymin)

        text_left, text_top, text_right, text_bottom = draw.textbbox(
            text_position, label, font=font
        )
        draw.rectangle(
            (text_left - 5, text_top - 5, text_right + 5, text_bottom + 5),
            fill=tuple(color),
        )

        draw.text(text_position, label, fill="black", font=font)

    return new_image


def inference(tflite_model_path, image, threshold):
    interpreter = load_tflite_model(tflite_model_path)
    labels = read_labels_tflite(tflite_model_path)
    new_image = predict(interpreter, labels, image, threshold)

    return new_image

with gr.Blocks() as gui:
    gr.Markdown("# Interface para Detecção de Objetos 🎉")
    with gr.Row():
        with gr.Column():
            input_model = gr.File(label="Upload TFLite Model")
            webcam_input = gr.Image(sources="webcam", streaming=True, type="pil")
            slider = gr.Slider(
                0.1,
                1.0,
                step=0.05,
                value=0.5,
                label="Threshold",
                info="Escolha um intervalo de confiança",
            )
            button = gr.Button("Detectar Objetos!")
        with gr.Column():
            webcam_output = gr.Image("Objetos detectados")
    button.click(
        inference, inputs=[input_model, webcam_input, slider], outputs=webcam_output
    )

gui.launch()
