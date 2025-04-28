import os
import zipfile
import gradio as gr
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

# Diretório onde o modelo está armazenado
DATA_PATH = os.path.join(os.pardir, "data", "models", "detec")
# Nome do modelo .tflite a ser utilizado
MODEL_FILE = "detec_badges.tflite"
# Caminho completo do diretório até o arquivo do modelo
MODEL_PATH = os.path.join(DATA_PATH, MODEL_FILE)

with zipfile.ZipFile(MODEL_PATH, "r") as archive:
    for file in archive.namelist():
        LABELS = archive.read(file).decode(encoding="utf-8").split()
        display(LABELS)

        LABELS = LABELS[0:]
        display(f"N° de Classes: {len(LABELS)}", LABELS)


with zipfile.ZipFile(MODEL_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_PATH)

# Criação do interpretador do modelo
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)

# Alocação na memória
interpreter.allocate_tensors()

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype=np.uint8)
dict(zip(LABELS, COLORS))

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

def preprocess_image(interpreter, image):
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


def predict(image, threshold):
    global LABELS
    global interpreter

    new_image = image.copy()

    # Load the input image and preprocess it
    preprocessed_image = preprocess_image(interpreter, new_image)

    # Run object detection on the input image
    results = detect_objects(interpreter, preprocessed_image, threshold=threshold)
    display(results)

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
        color = [int(c) for c in COLORS[class_id]]
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=tuple(color), width=2)

        # Make adjustments to make the label visible for all objects
        # font = ImageFont.load_default()
        font = ImageFont.truetype("arial.ttf", 40)
        label = f"{LABELS[class_id]} {round(obj['score'] * 100, 2)}%"

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


gr.Interface(
    fn=predict,
    inputs=[
        gr.Image(type="pil"),
        gr.Slider(
            0.1,
            1.0,
            step=0.05,
            value=0.5,
            label="Threshold",
            info="Choose a confident percentage value",
        ),
    ],
    outputs=[gr.Image()],
).launch()
