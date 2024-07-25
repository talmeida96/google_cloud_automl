![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

# Gerador de Dataset com ROI cortado (2)
### 🚧 **OPÇÃO 3** 🚧

## Descrição
Este projeto utiliza a biblioteca OpenCV para capturar imagens de uma webcam e permite ao usuário selecionar uma Região de Interesse (ROI) para captura.
As imagens são salvas periodicamente em um diretório escolhido pelo usuário. A interface gráfica é construída com a biblioteca Tkinter.

## Funcionalidades
- Captura de vídeo em tempo real da webcam.
- Seleção de uma Região de Interesse (ROI) através de sliders.
- Salvamento periódico das imagens da ROI em um diretório especificado pelo usuário.
- Ajuste da variação máxima da posição da ROI e do intervalo entre capturas.
- Interface gráfica intuitiva para controle da captura e visualização da webcam.

## Requisitos
- Python 3.x
- OpenCV
- PIL (Pillow)
- Tkinter (geralmente incluído na instalação padrão do Python)

## Instalação
1. Clone este repositório:
    ```bash
    git clone https://github.com/seu_usuario/seu_repositorio.git
    cd seu_repositorio
    ```
2. Instale as dependências:
    ```bash
    pip install opencv-python pillow
    ```

## Uso
1. Execute o script principal:
    ```bash
    python 3_cam_with_roi.py
    ```
2. A interface gráfica será aberta, exibindo o vídeo da webcam.
3. Ajuste os sliders para definir a posição (X, Y) e as dimensões (Largura, Altura) da ROI.
4. Use o botão "Selecionar Diretório" para escolher onde as imagens capturadas serão salvas.
5. Ajuste os sliders "Variação Máxima" e "Intervalo (s)" para controlar a variação e a frequência das capturas.
6. Clique em "Start" para iniciar a captura periódica de imagens.
7. Clique em "Stop" para parar a captura.

## Estrutura do Código
- **Importações:** Importa as bibliotecas necessárias.
- **Variáveis Globais:** Mantém o estado e os parâmetros do programa.
- **Inicialização da Webcam:** Configura a webcam para captura de vídeo.
- **Funções de Captura e Salvamento:** Capturam e salvam imagens da ROI definida pelo usuário.
- **Funções de Controle:** Iniciam e param a captura periódica de imagens.
- **Função de Atualização da Webcam:** Atualiza a exibição da webcam na GUI.
- **Interface Gráfica:** Cria e configura a GUI com sliders e botões.
- **Finalização:** Libera recursos ao finalizar o programa.