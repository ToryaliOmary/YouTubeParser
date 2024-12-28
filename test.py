from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-software-rasterizer")

def extract_youtube_video_details(video_url):
    driver = webdriver.Chrome(options=options)
    try:
        # YouTube-Video öffnen
        driver.get(video_url)
        time.sleep(5)

        # Titel extrahieren
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#title > h1 > yt-formatted-string"))
            )
            video_title = title_element.text.strip()
            print(f"Titel extrahiert: {video_title}")
        except Exception as e:
            print(f"Fehler beim Extrahieren des Titels: {e}")
            video_title = ""

        # URL extrahieren
        video_url = driver.current_url
        print(f"URL extrahiert: {video_url}")

        # Kurzbeschreibung extrahieren
        try:
            try:
                expand_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inline-expander"))
                )
                expand_button.click()
                print("'Mehr anzeigen'-Button wurde gefunden und geklickt.")
                time.sleep(2)  # Warten, bis die Beschreibung vollständig geladen ist
            except Exception:
                print("'Mehr anzeigen'-Button nicht gefunden. Fährt mit der vorhandenen Beschreibung fort.")

            description_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#description-inline-expander > yt-attributed-string"))
            )
            video_description = description_element.text.strip()
            print(f"Kurzbeschreibung extrahiert: {video_description}")
        except Exception as e:
            print(f"Fehler beim Extrahieren der Kurzbeschreibung: {e}")
            video_description = ""
            
        # Rückgabe der extrahierten Daten
        return {
            "title": video_title,
            "url": video_url,
            "short_description": video_description
        }
    finally:
        driver.quit()

# Funktion aufrufen
if __name__ == "__main__":
    # Beispiel-YouTube-Video-URL
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Never Gonna Give You Up
    details = extract_youtube_video_details(video_url)
    print("Video-Details:", details)
