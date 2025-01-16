from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd  # Import für Excel-Export

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-software-rasterizer")

# Funktion zum Extrahieren der Videobeschreibung
def extract_video_short_description(driver):
    try:
        # Sicherstellen, dass die Seite vollständig geladen ist
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#description-inline-expander"))
        )
        time.sleep(2)
        try:
            expand_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inline-expander"))
            )
            expand_button.click()
            #print("'Mehr anzeigen'-Button wurde gefunden und geklickt.")
            time.sleep(2)
        except Exception:
            print("'Mehr anzeigen'-Button nicht gefunden. Fährt mit der vorhandenen Beschreibung fort.")

        # Kurzbeschreibung extrahieren
        description_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#description-inline-expander > yt-attributed-string"))
        )
        description_text = description_element.text.strip()
        #print(f"Kurzbeschreibung extrahiert: {description_text}")
        return description_text
    except Exception as e:
        print(f"Fehler beim Extrahieren der Kurzbeschreibung: {e}")
        return ""

# Funktion zum Extrahieren der empfohlenen Videos
def extract_recommended_titles(driver):
    try:
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        recommended_videos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ytd-compact-video-renderer span#video-title"))
        )

        titles_and_links = []
        for video in recommended_videos[:5]:
            try:
                link = video.find_element(By.XPATH, "ancestor::a").get_attribute("href")
                title = video.text
                # Überspringen, wenn es sich um Shorts handelt
                if "shorts" not in link:
                    titles_and_links.append((title, link))
                else:
                    print(f"Shorts-Video übersprungen: {title}")
            except Exception as e:
                print(f"Fehler beim Verarbeiten eines Videos: {e}")
                continue
        return titles_and_links
    except Exception as e:
        print(f"Fehler beim Extrahieren der empfohlenen Videos: {e}")
        return []

# Funktion zum Speichern in Excel
def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["Typ", "Nummer", "Titel", "URL", "Beschreibung"])
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"Daten erfolgreich in {filename} gespeichert.")

# Hauptfunktion
def explore_youtube_videos(search_query, depth, output_file):
    driver = webdriver.Chrome(options=options)
    try:
        video_counter = 1
        all_data = []
        visited_titles = []  #Liste für alle bereits besuchten Titel

        # YouTube öffnen und Suche durchführen, Shorts ausschließen
        search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%3D%3D"
        driver.get(search_url)
        time.sleep(3)

        # Erstes Video finden und starten
        first_video = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a#video-title"))
        )
        current_video_title = first_video.get_attribute("title")
        current_video_url = first_video.get_attribute("href")

        driver.execute_script("arguments[0].click();", first_video)
        time.sleep(5)

        # Beschreibung des ersten Videos extrahieren
        current_video_description = extract_video_short_description(driver)
        all_data.append(["Hauptvideo", f"{video_counter}", current_video_title, current_video_url, current_video_description])

        visited_titles.append(current_video_title)  #Ersten Titel zur Liste hinzufügen

        for level in range(depth):
            #print(f"Ebene {level + 1}: Empfehlungen werden extrahiert.")

            # Empfehlungen extrahieren
            recommendations = extract_recommended_titles(driver)
            recommendation_counter = 1  #Zähler für Empfehlungen des aktuellen Hauptvideos

            for idx, (title, link) in enumerate(recommendations, start=1):
                recommendation_number = f"{video_counter}.{recommendation_counter}"  #Nummerierung der Empfehlungen
                print(f"{recommendation_number} Empfehlung: {title} ({link})")
                all_data.append(["Empfehlung", recommendation_number, title, link, ""])
                recommendation_counter += 1

            # Nächstes unbesuchtes Video finden
            next_video_title = None
            next_video_url = None
            for title, link in recommendations:
                if title not in visited_titles:  #Prüfung, ob Titel bereits besucht wurde
                    next_video_title = title
                    next_video_url = link
                    break

            if next_video_title and next_video_url:
                video_counter += 1
                print(f"{video_counter}. Hauptvideo: {next_video_title} ({next_video_url})")

                visited_titles.append(next_video_title)  #Hinzufügen des neuen Titels zur Liste
                driver.get(next_video_url)
                time.sleep(5)

                next_video_description = extract_video_short_description(driver)
                all_data.append(["Hauptvideo", f"{video_counter}", next_video_title, next_video_url, next_video_description])
            else:
                print("Keine neuen Videos mehr gefunden.")
                break

        # Daten speichern
        save_to_excel(all_data, output_file)
        print(f"Daten gespeichert in {output_file}")
    finally:
        driver.quit()

# Funktion aufrufen
if __name__ == "__main__":
    explore_youtube_videos(search_query="Micky Maus gruselig", depth=20, output_file="YouTube_Figuren_Micky maus gruselig.xlsx")
