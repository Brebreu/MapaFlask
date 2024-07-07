# Mapa de Propriedades

Este projeto é uma aplicação web que permite visualizar propriedades em um mapa interativo, adicionar marcadores personalizados e exportar polígonos desenhados no mapa. A aplicação utiliza Flask como backend, Leaflet.js para renderizar o mapa e Bootstrap para o estilo.

## Requisitos

Certifique-se de ter instalado os seguintes softwares:

- Python 3.x
- Pip (Python package installer)

## Instalação

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.
https://github.com/Brebreu/MapaFlask.githttps://github.com/Brebreu/MapaFlask.git
### Clone o Repositório

Clone o repositório do projeto para sua máquina local:

```bash
git clone https://github.com/Brebreu/MapaFlask.git
cd MapaFlask
```
### Crie um Ambiente Virtual

Crie e ative um ambiente virtual para o projeto:

```bash
python -m venv venv
source venv/bin/activate # Para sistemas Unix
venv\Scripts\activate # Para Windows
```
### Instale as Dependências

Instale as dependências necessárias utilizando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```
### Configuração do Projeto

Certifique-se de que os arquivos de shapefile e os dados em JSON estejam nos locais corretos conforme configurado no código. Você pode alterar os caminhos no arquivo app.py se necessário.

### Executando a Aplicação

Para rodar a aplicação, execute o seguinte comando:

```bash
flask run
```
A aplicação estará disponível em http://127.0.0.1:5000.

### Estrutura do Projeto

    app.py: Arquivo principal da aplicação Flask.
    templates/: Diretório contendo os templates HTML.
        index.html: Template principal para o mapa e a sidebar.
    static/: Diretório contendo arquivos estáticos como CSS, JavaScript e imagens.
        css/styles.css: Arquivo CSS principal.
        js/script.js: Arquivo JavaScript principal.
        libs/: Diretório contendo bibliotecas como Leaflet e Leaflet Draw.
        images/: Diretório contendo imagens usadas na aplicação.

### Uso da Aplicação
### Interface de Usuário

    Mapa: O mapa é renderizado usando Leaflet.js e permite visualizar diferentes camadas de dados.
    Sidebar: A sidebar contém um formulário para buscar propriedades, adicionar marcadores e exportar polígonos desenhados.
    Botão de Menu: Use o botão de menu para abrir e fechar a sidebar.

### Funcionalidades

    Buscar Propriedade: Insira a latitude e longitude e clique em "Buscar Proprietário" para encontrar informações sobre a propriedade.
    Adicionar Marcador: Insira a latitude e longitude e clique em "Adicionar Marcador" para adicionar um marcador personalizado no mapa.
    Exportar Polígonos: Desenhe polígonos no mapa e clique em "Exportar Polígonos" para baixar o arquivo GeoJSON contendo os polígonos desenhados.

### Desenhando e Exportando Polígonos

    Use as ferramentas de desenho na barra lateral esquerda do mapa para desenhar polígonos, linhas, retângulos, círculos e marcadores.
    Após desenhar, clique em "Exportar Polígonos" para baixar o arquivo GeoJSON contendo os polígonos desenhados.

### Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

