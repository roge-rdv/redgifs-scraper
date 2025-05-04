from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip  # Biblioteca para acessar a área de transferência
import time
import subprocess  # Para executar o downloader.js

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-logging')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

# Solicita ao usuário a URL do site
url = input("Por favor, insira a URL para fazer o scraping: ").strip()
driver.get(url)

# Espera carregar a página inicial
time.sleep(5)

# Abre o arquivo em modo de escrita (append) para salvar os links dinamicamente
with open("video_links.txt", "a") as f, open("downloaded_links.txt", "a+") as downloaded_f:
    downloaded_f.seek(0)
    downloaded_links = set(downloaded_f.read().splitlines())  # Carrega links já baixados
    processed_ids = set()  # Initialize set to track processed video IDs

    try:
        while True:  # Loop infinito até o usuário interromper manualmente
            # Localiza todos os vídeos na lista
            try:
                gif_list = driver.find_element(By.CLASS_NAME, "gifList")
            except:
                gif_list = driver.find_element(By.CLASS_NAME, "previewFeed")
            videos = gif_list.find_elements(By.XPATH, './/div[starts-with(@id, "gif_")]')

            for video in videos:
                # Verifica se o elemento é um anúncio
                if "bannerWrapper" in video.get_attribute("class"):
                    print("Anúncio detectado. Ignorando...")
                    continue  # Pule o elemento se for um anúncio

                # Verifica se o elemento é uma seção de trending tags
                if "trendingTags" in video.get_attribute("class"):
                    print("Seção de trending tags detectada. Ignorando...")
                    continue  # Pule o elemento se for a seção de trending tags
                
                # Verifica se o elemento e uma secao de trending Creators
                if "trendingCreators" in video.get_attribute("class"):
                    print("Seção de trending creators detectada. Ignorando...")
                    continue
                
                # Verifica se o elemento é uma seção de trending Niches 
                if "trendingNiches" in video.get_attribute("class"):
                    print("Seção de trending niches detectada. Ignorando...")
                    continue

                video_id = video.get_attribute("id")
                if video_id in processed_ids:
                    continue  # Pula vídeos já processados

                processed_ids.add(video_id)  # Marca o vídeo como processado

                try:
                    # Aguarda o botão "MoreRoundButton" estar visível
                    more_button = WebDriverWait(video, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "MoreRoundButton"))
                    )
                    more_button.click()
                    time.sleep(1)

                    # Aguarda o botão "Share" estar visível e clica
                    share_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Share"]'))
                    )
                    share_button.click()
                    time.sleep(1)

                    # Aguarda o botão "Copy Link" estar visível e clica
                    copy_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Copy Link"]'))
                    )
                    copy_button.click()
                    time.sleep(1)

                    # Captura o link da área de transferência
                    link = pyperclip.paste()
                    if link and link not in downloaded_links:
                        f.write(link + "\n")  # Salva o link no arquivo imediatamente
                        f.flush()  # Garante que o link seja gravado no disco
                        print(f"Link capturado e salvo: {link}")

                        # Executa o downloader.js para baixar o vídeo
                        try:
                            subprocess.run(["node", "downloader.js", link], check=True)
                            downloaded_f.write(link + "\n")  # Registra o link como baixado
                            downloaded_f.flush()
                            downloaded_links.add(link)
                            print(f"Vídeo baixado com sucesso: {link}")
                        except subprocess.CalledProcessError as e:
                            print(f"Erro ao baixar o vídeo {link}: {e}")
                    elif link in downloaded_links:
                        print(f"Link já baixado: {link}")
                    else:
                        print(f"Nenhum link capturado para o vídeo {video_id}.")

                except Exception as e:
                    print(f"Erro ao processar vídeo {video_id}: {e}")

                # Rola para o próximo vídeo
                driver.execute_script("arguments[0].scrollIntoView();", video)
                time.sleep(1)

            # Rola para carregar mais vídeos (infinite scroll)
            infinite_scroll = driver.find_element(By.CLASS_NAME, "infiniteScroll")
            driver.execute_script("arguments[0].scrollIntoView();", infinite_scroll)
            time.sleep(3)  # Aguarda o carregamento de novos vídeos

    except KeyboardInterrupt:
        print("Captura interrompida pelo usuário.")

print("Processo concluído.")
driver.quit()
