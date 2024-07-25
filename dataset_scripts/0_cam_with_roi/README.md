![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

# Região de Interesse para Dataset (ML) - Introdução

### Descrição
Este projeto utiliza a biblioteca OpenCV para o capturar vídeo de uma webcam e exibir uma Região de Interesse (ROI) de forma destacada. A posição da ROI é alterada aleatoriamente em intervalos de tempo pré-definidos, e a janela de visualização pode ser fechada pressionando a `tecla 'q'`.

## Funcionalidades
- Exibição em tempo real do vídeo da webcam.
- Destaque de uma Região de Interesse (ROI) com borda colorida.
- Atualização periódica da posição da ROI com variação aleatória dentro de intervalo definido.
- Exibição do tempo decorrido desde o início da execução na tela.
- Fechamento da janela de exibição ao pressionar 'q'.

## Requisitos
- Python 3.x
- OpenCV

## Instalação
1. Clone este repositório:
    ```bash
    git clone https://github.com/seu_usuario/seu_repositorio.git
    cd seu_repositorio
    ```
2. Instale as dependências:
    ```bash
    pip install opencv-python
    ```

## Uso
1. Execute o script principal:
    ```bash
    python 0_cam_with_roi.py
    ```
2. A janela de exibição da webcam será aberta, mostrando a ROI destacada.
3. A ROI será movida aleatoriamente conforme intervalo definido, dentro dos limites da tela.
4. Pressione 'q' para fechar a janela de exibição.

## Estrutura do Código
- **Importações:** Importa as bibliotecas necessárias para manipulação de imagens, vídeo e tempo.
- **Definição da ROI:** Define a posição inicial e dimensões da ROI.
- **Variação da ROI:** Define a variação máxima permitida para o reposicionamento da ROI.
- **Inicialização da Webcam:** Configura a captura de vídeo da webcam.
- **Loop Principal:** Captura frames da webcam, atualiza a posição da ROI, desenha a borda da ROI e exibe o tempo decorrido.
- **Finalização:** Libera a captura da webcam e fecha todas as janelas abertas.