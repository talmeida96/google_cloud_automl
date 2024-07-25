![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

# Região de Interesse para Dataset (ML)
### 🚧 **OPÇÃO 1** 🚧 | _não possui threads_

### Descrição
Este projeto utiliza a biblioteca OpenCV para capturar o vídeo de uma webcam, exibir uma Região de Interesse (ROI) de forma destacada e salvar as imagens da ROI em intervalos de tempo pré-definidos. A posição da ROI é alterada aleatoriamente dentro de um intervalo máximo pré-definido de acordo com o tempo configurado.

## Funcionalidades
- Exibição em tempo real do vídeo da webcam.
- Destaque de uma Região de Interesse (ROI) com borda colorida.
- Atualização periódica da posição da ROI com variação aleatória dentro de intervalo definido.
- Captura e armazenamento de imagens da ROI em intervalos de tempo pré-definidos.
- Configuração do diretório de armazenamento e nome dos arquivos de imagem.
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
1. Configure o diretório de armazenamento e o intervalo de tempo para a captura de imagens no código:
    ```python
    output_dir = "testes/"
    time.sleep(5)                   # intervalo entre capturas em segundos
    ```
2. Execute o script principal:
    ```bash
    python 1_cam_with_roi.py
    ```
3. A janela de exibição da webcam será aberta, mostrando a ROI destacada.
4. A ROI será movida aleatoriamente a cada 3 segundos, dentro dos limites da tela, e uma imagem será salva no diretório configurado a cada 5 segundos.
5. Pressione 'q' para fechar a janela de exibição.

## Estrutura do Código
- **Importações:** Importa as bibliotecas necessárias para manipulação de imagens, vídeo e tempo.
- **Definição da ROI:** Define a posição inicial e dimensões da ROI.
- **Variação da ROI:** Define a variação máxima permitida para o reposicionamento da ROI.
- **Inicialização da Webcam:** Configura a captura de vídeo da webcam.
- **Loop Principal:** Captura frames da webcam, atualiza a posição da ROI, desenha a borda da ROI, salva a imagem da ROI e exibe o vídeo em tempo real.
- **Finalização:** Libera a captura da webcam e fecha todas as janelas abertas.