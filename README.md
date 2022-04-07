# Detection Face and Age Service

Este projeto é parte integrada do Age-Classification que pode ser encontrado aqui: 
- https://github.com/vitorglemos/age-classification

# Utilização Online (API)

Para testar a API, basta enviar o link da url com a imagem utilizando esse endereço:
- Acesse: https://thawing-reaches-91892.herokuapp.com/v1/home
- No campo em branco insira uma url e clique em **Enviar**, Imagem de exemplo: https://melhorcomsaude.com.br/wp-content/uploads/2017/03/genetica_rostos_filhos-500x282.jpg
- Se tudo ocorrer bem, o resultado:
<img src="https://github.com/vitorglemos/age-classification/blob/main/result.png?raw=true">

# Deploy

A aplicação está configurada para subir em Docker. Os arquivos necessários podem ser encontrados na raiz do Diretório:
- DockerFile
- docker-compose.yml

Aqui utilizamos a plataforma Heroku, para fazer deploy basta baixar o projeto e executar o comando:
```
cd detection_service
heroku container:push web --app <app_name>
```

# Documentação da API
A documentação da API pode ser conferida no endereço /docs, exemplo da aplicação online:
- https://thawing-reaches-91892.herokuapp.com/docs

# Tecnologias Utilizadas
- Python 3.7
- FastAPI
- Keras
- Tensorflow
- OpenCV
- Docker
