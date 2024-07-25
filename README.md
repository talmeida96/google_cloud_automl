![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

# Google Cloud AutoML

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)

 ### Descrição
 Os códigos presentes neste repositório serão utilizados no decorrer do curso AutoML, uma ferramenta de ML automatizado disposibilizada pelo Google Cloud Vertex AI.

## 📚 Códigos Disponíveis

📁 `dataset_scripts`: Os códigos desta subpasta são destinados à demonstração passo-a-passo de possibilidades de interfaces gráficas facilmente geradas por usuários sem experiência prévia através de ferramentas de IA para com finalidade de facilitar a captação de imagens para construção de datasets para modelos de imagem como classificação ou detecção de objetos.

📁 `automl_loadfile_generator`: Os códigos desta subpasta são referentes à criação de datasets destinados à modelos de detecção de objetos que serão carregados no AutoML através de um arquivo de carga de formato .csv cujos parâmetros de configuração (**ML_USE, GCS_PATH, LABELS e bounding boxes**) já serão carregados para _auto labeling_ da plataforma.

 ## 📌 Bibliotecas Utilizadas
- **CV2**: Biblioteca OpenCV para manipulação de imagem e vídeo.
- **OS**: Biblioteca padrão do Python para operações de sistema operacional.
- **THREADING**: Gerencia threads e permite a captura periódica de imagens sem bloquear a interface.
- **TIME**: Biblioteca para manipulações de tempo.
- **TKINTER**: Biblioteca para interface gráfica de usuário (GUIs).
- **PIL**: Biblioteca Pillow para manipulação de imagem.
- **RANDOM**: Biblioteca para gerar números aleatórios.
- **CSV**: Biblioteca para ler e escrever arquivos no formato CSV.
