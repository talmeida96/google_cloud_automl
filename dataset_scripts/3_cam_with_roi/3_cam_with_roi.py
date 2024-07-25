'''
Este código abre 1 janelas com:
- a visualização de webcam 
- um controle de ROI (Região de Interesse) através de sliders (X, Y, largura e altura)
- um botão para definição da variação máxima do posicionamento*
- um botão para definição do intervalo de captura das imagens
- um botão de definição do diretório para armazenamento das imagens capturadas
- um botão para início das capturas com um intervalo pré-definido
- um botão de finalização das capturas
- rodar em ambiente virtual (vertex_course)
'''

import cv2                          # biblioteca OpenCV para manipulação de imagens e vídeo
import os                           # biblioteca padrão do Python para operações de sistema operacional
import threading                    # gerencia threads e permite a captura periódica de imagens sem bloquear a interface
import time                         # biblioteca para manipulações de tempo
import tkinter as tk                # biblioteca para interface gráfica de usuário (GUIs)
from tkinter import filedialog      # módulo do Tkinter para criar caixas de diálogo de seleção de arquivos
from PIL import Image, ImageTk      # biblioteca Pillow para manipulação de imagens
import random                       # biblioteca para gerar númeras aleatórios

# Variáveis globais de controle
capturing = False                   # booleano que indica se a captura periódica de imagens está ativa ou não
capture_thread = None               # thread que executa a função captura_periodica
save_directory = ""                 # diretório de armazenamento das imagens
frame = None                        # armazena o frame da imagem capturada da webcam
img_width = 640                     # largura da imagem capturada
img_height = 480                    # altura da imagem capturada
init_time = 0                       # tempo de referência para a captura periódica
initial_x = 0                       # valor inicial do slider para x
initial_y = 0                       # valor inicial do slider para y

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

# Função para capturar e salvar a imagem
def capturar_imagem():
    global frame, img_width, img_height

    # Capturar a ROI atual
    roi_x = x_slider.get()
    roi_y = y_slider.get()
    roi_width = width_slider.get()
    roi_height = height_slider.get()

    # Assegurar que a ROI não ultrapasse os limites da imagem
    if roi_x + roi_width > img_width:
        roi_width = img_width - roi_x
    if roi_y + roi_height > img_height:
        roi_height = img_height - roi_y

    # Verificar se a ROI tem dimensões válidas
    if roi_width > 0 and roi_height > 0:
        roi = frame[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]

        # Salvar a imagem
        file_path = os.path.join(save_directory, f"roi_5_{int(time.time())}.jpg")
        cv2.imwrite(file_path, roi)

# Função para iniciar a captura periódica de imagens
def iniciar_captura():
    global capturing, capture_thread, init_time, initial_x, initial_y
    capturing = True            # indicar que a captura periódica está ativa
    init_time = time.time()

    # Armazenar os valores iniciais dos sliders
    initial_x = x_slider.get()
    initial_y = y_slider.get()

    # Criar e iniciar uma nova thread "capture_thread" para executar a função "captura_periodica"
    capture_thread = threading.Thread(target=captura_periodica)
    capture_thread.start()

# Função para parar a captura periódica de imagens
def parar_captura():
    global capturing, capture_thread
    capturing = False

    # Se a thread "capture_thread" estiver ativa, espera que ela termine de executar
    if capture_thread is not None:
        capture_thread.join()

# Função que realiza a captura periódica de imagens
def captura_periodica():
    global init_time
    while capturing:
        if time.time() - init_time > intervalo_slider.get():
            max_variacao = variacao_slider.get()
            roi_width = width_slider.get()
            roi_height = height_slider.get()

            # Gera valores aleatórios para a nova posição da ROI dentro do intervalo definido
            new_x = initial_x + random.randint(-max_variacao, max_variacao)
            new_y = initial_y + random.randint(-max_variacao, max_variacao)

            # Limitar a nova posição do ROI para que não saia da tela
            new_x = max(0, min(new_x, img_width - roi_width))
            new_y = max(0, min(new_y, img_height - roi_height))

            x_slider.set(new_x)
            y_slider.set(new_y)

            init_time = time.time()

        capturar_imagem()
        time.sleep(intervalo_slider.get())      # aguarda o intervalo do slider antes de realizar a próxima captura

# Função para selecionar o diretório de salvamento
def selecionar_diretorio():
    global save_directory
    save_directory = filedialog.askdirectory()
    if save_directory:
        print(f"Diretório de salvamento: {save_directory}")

# Função para atualizar a exibição da webcam
def atualizar_webcam():
    global frame, img_width, img_height

    ret, frame = cap.read()     # lê um novo frame da webcam
    if ret:
        img_height, img_width, _ = frame.shape

        roi_x = x_slider.get()
        roi_y = y_slider.get()
        roi_width = width_slider.get()
        roi_height = height_slider.get()

        frame_with_roi = frame.copy()
        cv2.rectangle(frame_with_roi, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

        cv2image = cv2.cvtColor(frame_with_roi, cv2.COLOR_BGR2RGBA)
        img = cv2.resize(cv2image, (640, 480))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)

    root.after(10, atualizar_webcam)

# Criar a interface gráfica
root = tk.Tk()
root.title("Gerador de Datasets com ROI (3)")

# Adicionar o Canvas para exibir a webcam
webcam_label = tk.Label(root)
webcam_label.grid(row=0, column=0, columnspan=4)

# Adicionar sliders para ajustar as coordenadas e o tamanho da ROI
x_slider = tk.Scale(root, from_=0, to=640, orient="horizontal", label="X")
x_slider.set(100)
x_slider.grid(row=1, column=0)

y_slider = tk.Scale(root, from_=0, to=480, orient="horizontal", label="Y")
y_slider.set(100)
y_slider.grid(row=1, column=1)

width_slider = tk.Scale(root, from_=1, to=640, orient="horizontal", label="Largura")
width_slider.set(224)
width_slider.grid(row=1, column=2)

height_slider = tk.Scale(root, from_=1, to=480, orient="horizontal", label="Altura")
height_slider.set(224)
height_slider.grid(row=1, column=3)

# Adicionar slider para definir a variação máxima e o intervalo
variacao_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Variação Máxima")
variacao_slider.set(10)
variacao_slider.grid(row=2, column=0, columnspan=2)

intervalo_slider = tk.Scale(root, from_=1, to=10, orient="horizontal", label="Intervalo (s)")
intervalo_slider.set(3)
intervalo_slider.grid(row=2, column=2, columnspan=2)

# Adicionar botões
btn_select_directory = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio)
btn_select_directory.grid(row=3, column=0, pady=10)

btn_start = tk.Button(root, text="Start", command=iniciar_captura)
btn_start.grid(row=3, column=1, pady=10)

btn_stop = tk.Button(root, text="Stop", command=parar_captura)
btn_stop.grid(row=3, column=2, pady=10)

# Iniciar a atualização da webcam
atualizar_webcam()

# Iniciar o loop da interface gráfica
root.mainloop()

# Quando tudo estiver feito, liberar a captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
