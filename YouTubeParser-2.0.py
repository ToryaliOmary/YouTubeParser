
#Dieser Code öffnet Youtube, sucht nach einem Begirff, öffnet das erste Video und notiert Titel des Videos und ersten 10 Empfehlungen in eine .csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # GPU-Beschleunigung deaktivieren
options.add_argument("--disable-webgl")  # WebGL deaktivieren
options.add_argument("--no-sandbox")  # Sandbox-Modus deaktivieren
options.add_argument("--disable-dev-shm-usage")  # Speicherproblemen vorbeugen

# WebDriver initialisieren
driver = webdriver.Chrome(options=options)

try:
    # YouTube öffnen
    driver.get("https://www.youtube.com")
    time.sleep(2)  # Warten, bis die Seite geladen ist

    # Nach Begriff suchen
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Kindervideos")  # Suchbegriff
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Warten, bis Ergebnisse geladen sind

    # Erstes Video öffnen und Titel sowie URL speichern
    first_video_title = None
    first_video_url = None
    try:
        first_video = driver.find_element(By.XPATH, '//a[@id="video-title"]')
        first_video_title = first_video.get_attribute("title")
        first_video_url = first_video.get_attribute("href")
        first_video.click()
        print(f"Das erste Video wurde geöffnet: {first_video_title}")
    except Exception as e:
        print("Fehler beim Öffnen des ersten Videos:", e)
        driver.quit()
        exit()

    time.sleep(5)  # Warten, bis das Video geladen ist

    # Titel der empfohlenen Videos extrahieren (ohne URLs)
    recommended_titles = []
    try:
        recommendations = driver.find_elements(By.XPATH, '//a[@id="video-title"]')[:11]  # 10 Empfehlungen + 1 Hauptvideo
        for idx, video in enumerate(recommendations, start=1):
            title = video.get_attribute("title")
            if title and title != first_video_title:  # Hauptvideo-Titel ignorieren
                recommended_titles.append({"Nummer": idx, "Titel": title})
    except Exception as e:
        print("Fehler beim Abrufen der empfohlenen Videos:", e)

    # Speichern in einer CSV-Datei
    csv_filename = "youtube_video_data_2.0.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Kopfzeilen schreiben
            writer.writerow(["Video-Typ", "Nummer", "Titel", "URL"])

            # Hauptvideo schreiben
            writer.writerow(["Hauptvideo", "", first_video_title, first_video_url])

            # Empfohlene Videos schreiben
            for video in recommended_titles:
                writer.writerow(["Empfehlung", video["Nummer"], video["Titel"], ""])
        print(f"Die Videos wurden in {csv_filename} gespeichert.")
    except Exception as e:
        print("Fehler beim Speichern der CSV-Datei:", e)

finally:
    driver.quit()  # Browser schließen
