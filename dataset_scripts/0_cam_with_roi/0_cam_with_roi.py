import cv2          # biblioteca OpenCV para manipulação de imagens e vídeo
import time         # biblioteca para manipulações de tempo
import random       # biblioteca para gerar númeras aleatórios

# Variáveis para definição da região de interesse inicial (ROI)
x = 295             # Coordenada X do canto superior esquerdo
y = 220             # Coordenada Y do canto superior esquerdo
w = 200             # Largura da ROI
h = 100             # Altura da ROI

# Variáveis para variação do posicionamento da ROI
new_x = x
new_y = y

# Intervalo máximo para a variação aleatória da posição da ROI
max_var_x = 10
max_var_y = 10

border_colour = (0, 255, 0)     # Cor da borda de destaque em BGR (azul = 0, verde = 255, vermelho = 0)
line_width = 1                  # Espessura da borda de destaque 

# Tempo inicial do timer (em segundos)
init_time = time.time()
end_time = 0

# Inicializa a captura da webcam
captura = cv2.VideoCapture(0)

while True:
    # Captura o frame da webcam
    ret, frame = captura.read()

    # Verifica se a captura foi bem sucedida
    if not ret:
        break

    # Atualiza a posição da ROI a cada x segundos (opcional) - sem thread
    if end_time > 3:
        # Gera valores aleatórios para a nova posição da ROI dentro do intervalo definido
        new_x = x + random.randint(-max_var_x, max_var_x)
        new_y = y + random.randint(-max_var_y, max_var_y)

        # Limita a nova posição da ROI para que não saia da tela
        new_x = max(0, min(new_x, frame.shape[1] - w))
        new_y = max(0, min(new_y, frame.shape[0] - h))

        init_time = time.time()

    # Calcula o tempo decorrido desde o início
    end_time = time.time() - init_time

    # Converte o tempo decorrido para formato de string (minutos:segundos)
    minutos, segundos = divmod(int(end_time), 60)
    tempo_str = f"{minutos:02}:{segundos:02}"

    # Recorta a região de interesse (ROI)
    roi = frame[new_y:new_y+h, new_x:new_x+w]

    # Desenha a borda na ROI
    cv2.rectangle(roi, (0, 0), (w-1, h-1), border_colour, line_width)

    # Exibe o tempo na tela (posicionado no canto superior esquerdo)
    cv2.putText(frame, tempo_str, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Exibe o frame com a borda e o tempo na tela
    cv2.imshow('Regiao de Interesse (ROI)', frame)

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura da webcam
captura.release()

# Fecha todas as janelas abertas
cv2.destroyAllWindows()