import os
import zipfile
import gradio as gr
import numpy as np
import tensorflow as tf

DATA_PATH = os.path.join(os.pardir, "data", "models", "multi")
MODEL_FILE = "raspberry_cropped.tflite"
MODEL_PATH = os.path.join(DATA_PATH, MODEL_FILE)
LABEL_FILE = "dict.txt"

# Extrair o arquivo de labels se não estiver presente
if not os.path.isfile(os.path.join(DATA_PATH, LABEL_FILE)):
    with zipfile.ZipFile(MODEL_PATH, "r") as zip_ref:
        zip_ref.extractall(DATA_PATH)

# Carregar as labels a partir do arquivo de texto
with open(os.path.join(DATA_PATH, LABEL_FILE)) as my_file:
    LABELS = my_file.read().split()

# Criar um interpretador para o modelo e alocar na memória
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Função para fazer predições usando o modelo
def predict(image):
    global LABELS
    global interpreter

    # Recuperar os detalhes da entrada e saída do modelo
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    # Redimensionar a imagem para o tamanho esperado pelo modelo
    image = image.resize((224, 224))

    # Normalizar a imagem para a escala entre 0 e 1
    image_arr = np.array(image, dtype=np.float32) / 255.0

    # Converter a imagem para o tipo de dados esperado pelo modelo, se necessário
    if input_details["dtype"] == np.uint8:
        input_scale, input_zero_point = input_details["quantization"]
        image_arr = image_arr / input_scale + input_zero_point

    # Adicionar uma dimensão extra para a imagem
    image_arr = np.expand_dims(image_arr, axis=0).astype(input_details["dtype"])

    # Enviar a imagem para o modelo
    interpreter.set_tensor(input_details["index"], image_arr)

    # Realizar a inferência com o modelo
    interpreter.invoke()

    # Obter os resultados da saída do modelo
    output = interpreter.get_tensor(output_details["index"])[0]

    # Converter os resultados de volta para o tipo de dados original, se necessário
    if output_details["dtype"] == np.uint8:
        output_scale, output_zero_point = output_details["quantization"]
        output = output_scale * (output.astype(np.float32) - output_zero_point)

    # Criar um dicionário de confianças para cada classe
    confidences = {LABELS[i]: float(confidence) for i, confidence in enumerate(output)}

    # Imprimir as confianças e a classe com maior confiança
    print(confidences, output.argmax())

    return confidences

# Criar uma interface Gradio para a função de predição
gr.Interface(
    fn=predict,
    inputs=[gr.Image(type="pil")],
    outputs=[gr.Label()],
).launch()
