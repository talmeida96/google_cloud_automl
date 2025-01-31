import cv2                          # biblioteca OpenCV para manipulação de imagens e vídeo
import os                           # biblioteca padrão do Python para operações de sistema operacional
import threading                    # gerencia threads e permite a captura periódica de imagens sem bloquear a interface
import time                         # biblioteca para manipulações de tempo
import tkinter as tk                # cria a interface gráfica do usuário
from tkinter import filedialog      # cria a caixa de diálogo para escolha do diretório de armazenamento
from PIL import Image, ImageTk      # biblioteca Pillow para manipulação de imagens

# Variáveis globais para controle
capturing = False                   # booleano que indica se a captura periódica de imagens está ativa ou não
capture_thread = None               # thread que executa a função captura_periodica
save_directory = ""                 # diretório de armazenamento das imagens

# Inicializar a captura de vídeo
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

        # Mostrar a ROI em uma nova janela
        cv2.imshow("ROI", roi)

        # Salvar a imagem
        file_path = os.path.join(save_directory, f"roi_4_{int(time.time())}.jpg")
        cv2.imwrite(file_path, roi)
        print(f"Imagem salva em: {file_path}")

# Função para iniciar a captura periódica de imagens
def iniciar_captura():
    global capturing, capture_thread
    capturing = True                # indicar que a captura periódica está ativa
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
    while capturing:
        capturar_imagem()
        time.sleep(4)           # intervalo de captura

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

        if roi_x + roi_width > img_width:
            roi_width = img_width - roi_x
        if roi_y + roi_height > img_height:
            roi_height = img_height - roi_y

        if roi_width > 0 and roi_height > 0:
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
root.title("Gerador de Datasets com ROI (2)")

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

# Adicionar botões
btn_select_directory = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio)
btn_select_directory.grid(row=2, column=0, pady=10)

btn_start = tk.Button(root, text="Start", command=iniciar_captura)
btn_start.grid(row=2, column=1, pady=10)

btn_stop = tk.Button(root, text="Stop", command=parar_captura)
btn_stop.grid(row=2, column=2, pady=10)

# Iniciar a atualização da webcam
atualizar_webcam()

# Iniciar o loop da interface gráfica
root.mainloop()

# Quando tudo estiver feito, liberar a captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
