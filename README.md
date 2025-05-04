# RedGifs Scraper

Um script para scraping e download de vídeos do RedGifs usando Selenium e Node.js.

## Funcionalidades

- Captura links de vídeos do RedGifs.
- Baixa os vídeos automaticamente usando um script Node.js (`downloader.js`).
- Ignora anúncios e seções irrelevantes.
- Evita duplicação de downloads.

## Requisitos

- Python 3.x
- Node.js
- Google Chrome
- ChromeDriver
- Bibliotecas Python:
  - `selenium`
  - `pyperclip`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/roge-rdv/redgifs-scraper.git
   cd redgifs-scraper
   ```

2. Instale as dependências Python:
   ```bash
   pip install selenium pyperclip
   ```

3. Certifique-se de que o `ChromeDriver` está instalado e configurado no PATH.

4. Instale as dependências Node.js (se necessário para o `downloader.js`):
   ```bash
   npm install
   ```

## Uso

1. Execute o script:
   ```bash
   python scraper.py
   ```

2. Insira a URL do RedGifs para iniciar o scraping.

3. Os links capturados serão salvos em `video_links.txt`, e os vídeos baixados serão registrados em `downloaded_links.txt`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
