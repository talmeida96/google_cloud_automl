# Gerador de Datasets (Múltiplas ROIs)
Este projeto é uma aplicação em Python que utiliza OpenCV e Tkinter para capturar imagens da webcam, selecionar múltiplas regiões de interesse (ROIs) e salvar essas imagens junto com as informações das ROIs em um arquivo CSV. O objetivo é facilitar a criação de datasets anotados para uso em tarefas de visão computacional.

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)

## Funcionalidades
- `Captura de Imagens`: Captura imagens da câmera periodicamente, de acordo com intervalo definido.
- `Regiões de Interesse (ROIs)`: Permite a definição de múltiplas ROIs na imagem capturada.
- `Salvamento de Dados`: Salva as imagens capturadas em um diretório especificado e armazena informações das ROIs em um arquivo CSV.
- `Interface Gráfica`: Interface amigável para o usuário manipular a criação do dataset.

## Bibliotecas Utilizadas
- **CV2**: Biblioteca OpenCV para manipulação de imagem e vídeo.
- **OS**: Biblioteca padrão do Python para operações de sistema operacional.
- **THREADING**: Gerencia threads e permite a captura periódica de imagens sem bloquear a interface.
- **TIME**: Biblioteca para manipulações de tempo.
- **TKINTER**: Biblioteca para interface gráfica de usuário (GUIs).
- **PIL**: Biblioteca Pillow para manipulação de imagem.
- **RANDOM**: Biblioteca para gerar números aleatórios.
- **CSV**: Biblioteca para ler e escrever arquivos no formato CSV.

## COMO UTILIZAR
1. `Selecionar Diretório`: Clique no botão "**Selecionar Diretório**" para escolher o local de armazenamento das imagens.
2. `Adicionar ROI`: Clique no botão "**Adicionar ROI**" para adicionar uma nova região de interesse.
    - **X**: é o ponto inicial no eixo x
    - **Y**: é o ponto inicial no eixo y
    - **Largura**: é a largura total considerando o eixo x
    - **Altura**: é altura total considerando o eixo y
    - **Categoria**: é o nome do rótulo que será cadastrado para esta ROI
    - **Excluir ROI**: excluir campos de cadastro de ROI não utilizados
3. `Iniciar Captura`: Clique no botão "**Start**" para iniciar a captura periódica de imagens.
4. `Parar Captura`: Clique no botão "**Stop**" para parar a captura de imagens.

### Ajustar Sliders:
- `Variação Máxima`: Define a variação de posição máxima das ROIs entre capturas de forma aleatória.
- `Intervalo(s)`: Define o intervalo de tempo em segundos entre cada captura de imagem.

## Estrutura do Código
### Variáveis Globais
- **capturing**: Indica se a captura periódica de imagens está ativa.
- **capture_thread**: Thread que executa a função de captura periódica.
- **save_directory**: Diretório de armazenamento das imagens.
- **file_name**: Nome do arquivo CSV onde as informações das ROIs serão salvas.
- **gcs_path**: Caminho de armazenamento no Cloud Storage.
- **img_width, img_height**: Largura e altura da imagem capturada.
- **init_time**: Tempo de referência para a captura periódica.
- **init_positions**: Posições iniciais das ROIs.
- **img_counter**: Contador de imagens capturadas.

### Funções Principais
- `capturar_imagem()`: Captura e salva a imagem atual, e escreve as informações das ROIs em um arquivo CSV.
- `iniciar_captura()`: Inicia a captura de imagens em uma thread separada.
- `parar_captura()`: Para a captura de imagens e aguarda a thread de captura finalizar.
- `captura_periodica()`: Captura imagens periodicamente e atualiza as posições das ROIs.
- `selecionar_diretorio()`: Abre um diálogo para selecionar o diretório de salvamento das imagens.
- `atualizar_webcam()`: Atualiza a visualização da webcam com as ROIs desenhadas.
- `adicionar_roi()`: Adiciona uma nova ROI ao painel de controle.
- `remover_roi(index)`: Remove uma ROI do painel de controle.
- `update_image_count_label()`: Atualiza o contador de imagens capturadas no rótulo.

### Interface Gráfica
A interface gráfica é composta por vários frames e widgets:

- `Frame de Controles Principais`: Contém botões para selecionar diretório, iniciar e parar captura, e adicionar ROIs.
- `Frame Principal`: Exibe a visualização da webcam e as ROIs desenhadas.
- `Frame de Controles Inferiores`: Contém rótulos e sliders para ajustar as configurações de variação e intervalo de captura.
- `Frame de Controles à Direita`: Painel de controle para adicionar e ajustar ROIs.

## Requisitos
- Python 3.x
- OpenCV (cv2)
- Pillow (PIL)

## Como Executar
Certifique-se de que todas as bibliotecas necessárias estão instaladas:
```bash
pip install opencv-python pillow
```
Ou instale através do arquivo de _requirements.txt_:
```bash
pip install -r requirements.txt
```

### Execute o script Python:
```bash
python loadfile_gen.py
```
