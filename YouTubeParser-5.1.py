
# Dieser Code öffnet Youtube, sucht einen Begriff, öffnet das erste Video, speichert die ersten 5 Empfehlungen, 
# anschließend öffnet er die erste Videoempfehlung und speichert wieder die ersten 5 Empfhelungen 
# dieser Prozess wird einer vorgebenen Anzahl nach wiederholt 
# Lösung: Shorts und Reels werden nicht berücksichtigt, da innerhalb der SuchQuery "&sp=EgIQAQ%3D%3D" eingegeben ist, das Shorts und Reels ausschließt 


# Benutzung: 
# search_query="Elsa verboten" -> Suche 
# depth=4 -> Anzahl der Iterationen 
# output_file="youtube_recommendations.csv" -> Speicherort der Daten 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Funktion zum Extrahieren der Titel und Links der ersten 5 empfohlenen Videos
def extract_recommended_titles(driver):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(3)  # Zusätzliche Wartezeit für das Laden der Empfehlungen

    recommended_videos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-compact-video-renderer span#video-title'))
    )

    titles_and_links = []
    for video in recommended_videos[:5]:
        try:
            link = video.find_element(By.XPATH, "ancestor::a").get_attribute("href")
            title = video.text
            titles_and_links.append((title, link))
        except Exception as e:
            print(f"Fehler beim Verarbeiten eines Videos: {e}")
            continue
    return titles_and_links

# CSV-Datei erstellen
def save_to_csv(data, filename, search_query):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Schreibe das Suchwort als Titel in die erste Zeile
        writer.writerow([f"Suchwort: {search_query}"])
        writer.writerow(["Typ", "Nummer", "Titel", "URL"])  # Kopfzeile für die Daten
        writer.writerows(data)

# Hauptfunktion
def explore_youtube_recommendations(search_query, depth, output_file):
    driver = webdriver.Chrome(options=options)
    try:
        video_counter = 1  # Zähler für Hauptvideos
        all_data = []  # Speichert alle Daten für CSV

        # YouTube öffnen mit Filter für normale Videos
        search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%3D%3D"
        driver.get(search_url)
        time.sleep(3)

        # Erstes Video finden und starten
        first_video = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
        )
        current_video_title = first_video.get_attribute("title")
        current_video_url = first_video.get_attribute("href")
        print(f"{video_counter}. Hauptvideo: {current_video_title} ({current_video_url})")
        all_data.append(["Hauptvideo", video_counter, current_video_title, current_video_url])

        driver.execute_script("arguments[0].scrollIntoView(true);", first_video)
        driver.execute_script("arguments[0].click();", first_video)
        time.sleep(5)

        # Schleife durch die gewünschten Ebenen
        for level in range(1, depth + 1):
            # Empfehlungen extrahieren
            recommendations = extract_recommended_titles(driver)
            for idx, (title, link) in enumerate(recommendations, start=1):
                print(f"  {video_counter}.{idx} Empfehlung: {title} ({link})")
                all_data.append(["Empfehlung", f"{video_counter}.{idx}", title, link])

            # Nächstes Hauptvideo auswählen
            if recommendations:
                next_video_title, next_video_url = recommendations[0]
                video_counter += 1
                print(f"{video_counter}. Hauptvideo: {next_video_title} ({next_video_url})")
                all_data.append(["Hauptvideo", video_counter, next_video_title, next_video_url])

                # Zum nächsten Video navigieren
                driver.get(next_video_url)
                time.sleep(5)
            else:
                print(f"Keine Empfehlungen in Ebene {level}.")
                break

        # Daten in CSV speichern
        save_to_csv(all_data, output_file, search_query)

    finally:
        driver.quit()

# Funktion aufrufen
if __name__ == "__main__":
    # Beispielaufruf mit Suche nach "Elsa verboten" und einer Tiefe von 4
    explore_youtube_recommendations(search_query="Elsa verboten", depth=4, output_file="youtube_recommendations.csv")
