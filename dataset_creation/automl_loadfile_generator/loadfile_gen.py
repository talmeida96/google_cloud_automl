import cv2                                          # biblioteca OpenCV para manipulação de imagens e vídeo
import os                                           # biblioteca padrão do Python para operações de sistema operacional
import threading                                    # gerencia threads e permite a captura periódica de imagens sem bloquear a interface
import time                                         # biblioteca para manipulações de tempo
import tkinter as tk                                # biblioteca para interface gráfica de usuário (GUIs)
from tkinter import filedialog, ttk                 # módulos do Tkinter
from PIL import Image, ImageTk                      # biblioteca Pillow para manipulação de imagens
import random                                       # biblioteca para gerar númeras aleatórios
import csv                                          # biblioteca para ler e escrever arquivos no formato CSV

capturing = False                                   # booleano que indica se a captura periódica de imagens está ativa ou não
capture_thread = None                               # thread que executa a função captura_periodica
save_directory = ""                                 # diretório de armazenamento das imagens
file_name = "load_file.csv"                         # nome do arquivo de carga a ser gerado

gcs_path = "gs://t0_thayna_main/single_badges/"     # caminho de armazenamento no Cloud Storage ***ALTERAR***

img_width = 640                                     # largura da imagem capturada
img_height = 480                                    # altura da imagem capturada
init_time = 0                                       # tempo de referência para a captura periódica
init_positions = []                                 # posições das regiões de interesse
img_counter = 0                                     # contador de imagens

cap = cv2.VideoCapture(1)                           # inicialização da câmera | 0 = webcam integrada
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

def capturar_imagem():
    """Captura e salva a imagem atual, e escreve as informações das ROIs em um arquivo CSV."""
    global img_counter, frame
    
    if save_directory:
        img_name = f"img_{int(time.time())}.jpg"
        file_path = os.path.join(save_directory, img_name)
        cv2.imwrite(file_path, frame)
        img_counter += 1
        update_image_count_label()

    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        for i, (roi_x, roi_y, roi_width, roi_height, label_entry) in enumerate(init_positions):
            roi_width = min(roi_width, img_width - roi_x)
            roi_height = min(roi_height, img_height - roi_y)

            if roi_width > 0 and roi_height > 0:
                x_min = roi_x
                y_min = roi_y
                x_max = roi_x + roi_width
                y_max = roi_y + roi_height

                # Normaliza as coordenadas
                x_min_norm = x_min / img_width
                y_min_norm = y_min / img_height
                x_max_norm = x_max / img_width
                y_max_norm = y_max / img_height

                label = label_entry.get()
                info = (
                    f"{gcs_path}{img_name},"
                    f"{label},"
                    f"{x_min_norm:.8f},{y_min_norm:.8f},"
                    f"{x_max_norm:.8f},{y_min_norm:.8f},"
                    f"{x_max_norm:.8f},{y_max_norm:.8f},"
                    f"{x_min_norm:.8f},{y_max_norm:.8f}"
                )
                # print(info)
                writer.writerow([
                    f"{gcs_path}{img_name}", label, 
                    f"{x_min_norm:.8f}", f"{y_min_norm:.8f}",
                    f"{x_max_norm:.8f}", f"{y_min_norm:.8f}",
                    f"{x_max_norm:.8f}", f"{y_max_norm:.8f}",
                    f"{x_min_norm:.8f}", f"{y_max_norm:.8f}"
                ])

def iniciar_captura():
    """Inicia a captura de imagens em uma thread separada."""
    global capturing, capture_thread, init_time, init_positions
    capturing = True
    init_time = time.time()
    init_positions = [(x.get(), y.get(), width.get(), height.get(), label) for _, label, x, y, width, height, _, _ in rois]
    capture_thread = threading.Thread(target=captura_periodica)
    capture_thread.start()

def parar_captura():
    """Para a captura de imagens e aguarda a thread de captura finalizar."""
    global capturing, capture_thread
    capturing = False
    if capture_thread is not None:
        capture_thread.join()

def captura_periodica():
    """Captura imagens periodicamente e atualiza as posições das ROIs."""
    global init_time
    while capturing:
        if time.time() - init_time > intervalo_slider.get():
            max_variacao = variacao_slider.get()
            for i, (initial_x, initial_y, roi_width, roi_height, _) in enumerate(init_positions):
                new_x = initial_x + random.randint(-max_variacao, max_variacao)
                new_y = initial_y + random.randint(-max_variacao, max_variacao)
                new_x = max(0, min(new_x, img_width - roi_width))
                new_y = max(0, min(new_y, img_height - roi_height))
                rois[i][2].set(new_x)
                rois[i][3].set(new_y)
            init_time = time.time()
        capturar_imagem()
        time.sleep(intervalo_slider.get())

def selecionar_diretorio():
    """Abre um diálogo para selecionar o diretório de salvamento das imagens."""
    global save_directory
    save_directory = filedialog.askdirectory()
    if save_directory:
        print(f"Diretório de armazenamento: {save_directory}")

def atualizar_webcam():
    """Atualiza a visualização da webcam com as ROIs desenhadas."""
    global frame, img_width, img_height

    ret, frame = cap.read()
    if ret:
        img_height, img_width, _ = frame.shape

        frame_with_rois = frame.copy()
        for _, _, x, y, width, height, _, _ in rois:
            roi_x = x.get()
            roi_y = y.get()
            roi_width = width.get()
            roi_height = height.get()
            cv2.rectangle(frame_with_rois, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

        cv2image = cv2.cvtColor(frame_with_rois, cv2.COLOR_BGR2RGBA)
        img = cv2.resize(cv2image, (640, 480))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)

    root.after(10, atualizar_webcam)

def adicionar_roi():
    """Adiciona uma nova ROI ao painel de controle."""
    row = len(rois) * 6  # Ajusta o espaçamento entre as ROIs

    # Cria e posiciona os widgets da nova ROI
    categoria_label = tk.Label(frame_direita_interior, text=f"Categoria {len(rois) + 1}", anchor="center")
    categoria_label.grid(row=row, column=0, columnspan=5, pady=5)

    label_entry = tk.Entry(frame_direita_interior)
    label_entry.grid(row=row + 1, column=1, columnspan=2, sticky="ew")

    x = tk.Scale(frame_direita_interior, from_=0, to=640, orient="horizontal", resolution=1, label=f"X{len(rois) + 1}")
    x.set(100)
    x.grid(row=row + 2, column=0, padx=5, sticky="ew")
    
    y = tk.Scale(frame_direita_interior, from_=0, to=480, orient="horizontal", resolution=1, label=f"Y{len(rois) + 1}")
    y.set(100)
    y.grid(row=row + 2, column=1, padx=5, sticky="ew")
    
    width = tk.Scale(frame_direita_interior, from_=1, to=640, orient="horizontal", resolution=1, label=f"Largura{len(rois) + 1}")
    width.set(224)
    width.grid(row=row + 2, column=2, padx=5, sticky="ew")
    
    height = tk.Scale(frame_direita_interior, from_=1, to=480, orient="horizontal", resolution=1, label=f"Altura{len(rois) + 1}")
    height.set(224)
    height.grid(row=row + 2, column=3, padx=5, sticky="ew")

    btn_remove_roi = tk.Button(frame_direita_interior, text="Excluir ROI", command=lambda idx=len(rois): remover_roi(idx))
    btn_remove_roi.grid(row=row, column=4, rowspan=3, columnspan=3, padx=5, pady=5, sticky="ns")

    separator = ttk.Separator(frame_direita_interior, orient="horizontal")
    separator.grid(row=row + 3, column=0, columnspan=5, pady=5, sticky="ew")
    
    rois.append((categoria_label, label_entry, x, y, width, height, btn_remove_roi, separator))

    # Atualiza a barra de rolagem
    frame_direita_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def remover_roi(index):
    """Remove uma ROI do painel de controle."""
    for widget in rois[index]:
        widget.grid_forget()
        widget.destroy()  # Destroi o widget após remover do grid
    del rois[index]

    # Reposiciona os widgets restantes
    for i in range(index, len(rois)):
        categoria_label, label_entry, x, y, width, height, btn_remove_roi, separator = rois[i]

        row = i * 6

        categoria_label.config(text=f"Categoria {i + 1}")
        x.config(label=f"X{i + 1}")
        y.config(label=f"Y{i + 1}")
        width.config(label=f"Largura{i + 1}")
        height.config(label=f"Altura{i + 1}")
        btn_remove_roi.config(command=lambda idx=i: remover_roi(idx))

        categoria_label.grid(row=row, column=0, columnspan=5, pady=5)
        label_entry.grid(row=row + 1, column=1, columnspan=2, sticky="ew")
        x.grid(row=row + 2, column=0, padx=5, sticky="ew")
        y.grid(row=row + 2, column=1, padx=5, sticky="ew")
        width.grid(row=row + 2, column=2, padx=5, sticky="ew")
        height.grid(row=row + 2, column=3, padx=5, sticky="ew")
        btn_remove_roi.grid(row=row, column=4, rowspan=3, columnspan=3, padx=5, pady=5, sticky="ns")
        separator.grid(row=row + 3, column=0, columnspan=5, pady=5, sticky="ew")

    # Atualiza a barra de rolagem
    frame_direita_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def update_image_count_label():
    """Atualiza o contador de imagens capturadas no rótulo."""
    image_count_label.config(text=f"Imagens capturadas: {img_counter}")

# Configura a interface gráfica
root = tk.Tk()
root.geometry("1500x600")
root.title("Gerador de Datasets (Múltiplas ROIs)")

rois = []

# Frame para controles principais
frame_controles = tk.Frame(root)
frame_controles.pack(fill="x", padx=10, pady=10)
frame_controles.columnconfigure([0, 1, 2, 3], weight=1)

tk.Button(frame_controles, text="Selecionar Diretório", command=selecionar_diretorio).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_controles, text="Start", command=iniciar_captura).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_controles, text="Stop", command=parar_captura).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_controles, text="Adicionar ROI", command=adicionar_roi).grid(row=0, column=3, padx=5, pady=5)

# Frame principal para a webcam e ROIs
frame_principal = tk.Frame(root)
frame_principal.pack(fill="both", expand=True)

webcam_label = tk.Label(frame_principal)
webcam_label.pack(side="left", fill="both", expand=True)

# Frame para controles inferiores
frame_inf = tk.Frame(frame_principal)
frame_inf.pack(fill="x")
frame_inf.columnconfigure([0, 1, 2], weight=1)

image_count_label = tk.Label(frame_inf, text="Imagens capturadas: 0")
image_count_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# Frame para centralizar os sliders
frame_sliders = tk.Frame(frame_inf)
frame_sliders.grid(row=1, column=0, columnspan=3)

# Define os sliders
variacao_slider = tk.Scale(frame_sliders, from_=0, to=100, orient="horizontal", resolution=1, label="Variação Máxima")
variacao_slider.set(5)  # Valor inicial
variacao_slider.grid(row=0, column=0, padx=5, pady=5)

intervalo_slider = tk.Scale(frame_sliders, from_=1, to=10, orient="horizontal", resolution=1, label="Intervalo(s)")
intervalo_slider.set(3)  # Valor inicial
intervalo_slider.grid(row=0, column=1, padx=5, pady=5)

# Separador horizontal
separator = ttk.Separator(frame_inf, orient="horizontal")
separator.grid(row=2, column=0, columnspan=3, pady=5)

# Frame para os controles à direita
frame_direita = tk.Frame(frame_principal)
frame_direita.pack(fill="both", expand=True, side="left")

canvas = tk.Canvas(frame_direita)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_direita, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.config(yscrollcommand=scrollbar.set)

frame_direita_interior = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_direita_interior, anchor="nw")
frame_direita_interior.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

# Inicia a interface gráfica
adicionar_roi()
atualizar_webcam()
root.mainloop()

# Libera recursos
cap.release()
cv2.destroyAllWindows()
