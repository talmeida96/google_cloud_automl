# Vertex - FTA Couse

## Primeiro módulo

1. Acessar a plataforma Google Vertex
2. Criar um conjunto de dados
3. Treinar usando os conjunto de dados criados
4. Avaliar os modelos
5. Realizar inferências com os modelos usando Python 🐍

## Segundo módulo

1. Configurar camera
2. Consumir modelo
3. Rodar modelo em notebook
4. Rodar modelo local usando um executavel/serviço

## Em breve:
- [ ] Criar notebook sobre utilização da camera [Basler](https://github.com/basler/pypylon)
- [ ] Criar conteúdo sobre o runtime [ONNX](https://onnx.ai/onnx/intro/concepts.html)
- [ ] Criar template utilizando o [ML.NET](https://www.youtube.com/playlist?list=PL1rZQsJPBU2TwElfOzqOsUW1yuxKNA091)

### Criar ambiente no mini conda

Criar ambiente virutal:
```sh
conda env create -n vertex_course -f environment.yml
```

Ativar ambiente:
```sh
conda activate vertex_course
```

### Como rodar os modelo em container

A plataforma Google Vertex oferece a possibilidade de utilizar containers pré-prontos para implementar rapidamente aplicações prontas. Com o arquivo .yml abaixo, é possível criar modelos facilmente. Necessário fazer o download do .pb da imagem do modelo.

```yml
version: "3"
services:
  modelo1:
    image: gcr.io/cloud-devrel-public-resources/gcloud-container-1.14.0:latest
    ports:
      - "8501:8501"
    volumes:
      - ./models/Exemplo1:/tmp/mounted_model/0001
    networks:
      - model_network
    container_name: Exemplo1

  modelo2:
    image: gcr.io/cloud-devrel-public-resources/gcloud-container-1.14.0:latest
    ports:
      - "8502:8501"
    volumes:
      - ./models/Exemplo1:/tmp/mounted_model/0001
    networks:
      - model_network
    container_name: Exemplo2

networks:
  model_network:
    driver: bridge
```