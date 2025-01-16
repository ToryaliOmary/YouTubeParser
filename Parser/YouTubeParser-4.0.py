
# Dieser Code öffnet Youtube, sucht einen Begriff, öffnet das erste Video, speichert die ersten 5 Empfehlungen, 
# öffnet das erste emphohlene Video, speichert dessen ersten 5 Empfehlungen, 
# öffnet wieder das erste emphohlene Video, speichert dessen 5 Empfehlungen, 
# öffnet wieder das erste emphohlene Video, speichert dessen 5 Empfehlungen
# insgesamt 4 mal aktuell
# to be continued


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
def extract_recommended_titles():
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(3)  # Zusätzliche Wartezeit für das Laden der Empfehlungen

    recommended_videos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-compact-video-renderer span#video-title'))
    )

    titles_and_links = []
    for video in recommended_videos[:5]:
        title = video.text
        link = video.find_element(By.XPATH, "ancestor::a").get_attribute("href")
        titles_and_links.append((title, link))
    return titles_and_links

# CSV-Datei erstellen
def save_to_csv(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Typ", "Nummer", "Titel", "URL"])
        writer.writerows(data)

# WebDriver initialisieren
driver = webdriver.Chrome(options=options)

try:
    video_counter = 1  # Zähler für Hauptvideos
    all_data = []  # Speichert alle Daten für CSV

    # YouTube öffnen
    driver.get("https://www.youtube.com")
    time.sleep(2)  # Kurz warten, bis die Seite geladen ist

    # Nach einem Begriff suchen
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Kindervideos")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Warten, bis die Ergebnisse geladen sind

    # Erstes Video finden, klicken und Empfehlungen speichern
    first_video = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
    )
    first_video_title = first_video.get_attribute("title")
    first_video_url = first_video.get_attribute("href")
    print(f"{video_counter}. Hauptvideo: {first_video_title} ({first_video_url})")
    all_data.append(["Hauptvideo", video_counter, first_video_title, first_video_url])

    driver.execute_script("arguments[0].scrollIntoView(true);", first_video)
    driver.execute_script("arguments[0].click();", first_video)
    time.sleep(5)  # Warten, bis das Video geladen ist

    # Empfehlungen für erstes Hauptvideo extrahieren
    first_recommendations = extract_recommended_titles()
    for idx, (title, link) in enumerate(first_recommendations, start=1):
        print(f"  {video_counter}.{idx} Empfehlung: {title} ({link})")
        all_data.append(["Empfehlung", f"{video_counter}.{idx}", title, link])

    # Erstes empfohlenes Video des ersten Hauptvideos öffnen
    if first_recommendations:
        next_video_title, next_video_url = first_recommendations[0]
        video_counter += 1
        print(f"{video_counter}. Hauptvideo: {next_video_title} ({next_video_url})")
        all_data.append(["Hauptvideo", video_counter, next_video_title, next_video_url])

        driver.get(next_video_url)
        time.sleep(5)  # Warten, bis das nächste Video geladen ist

        # Empfehlungen für das zweite Hauptvideo extrahieren
        second_recommendations = extract_recommended_titles()
        for idx, (title, link) in enumerate(second_recommendations, start=1):
            print(f"  {video_counter}.{idx} Empfehlung: {title} ({link})")
            all_data.append(["Empfehlung", f"{video_counter}.{idx}", title, link])

        # Erstes empfohlenes Video des zweiten Hauptvideos öffnen
        if second_recommendations:
            next_video_title, next_video_url = second_recommendations[0]
            video_counter += 1
            print(f"{video_counter}. Hauptvideo: {next_video_title} ({next_video_url})")
            all_data.append(["Hauptvideo", video_counter, next_video_title, next_video_url])

            driver.get(next_video_url)
            time.sleep(5)  # Warten, bis das nächste Video geladen ist

            # Empfehlungen für das dritte Hauptvideo extrahieren
            third_recommendations = extract_recommended_titles()
            for idx, (title, link) in enumerate(third_recommendations, start=1):
                print(f"  {video_counter}.{idx} Empfehlung: {title} ({link})")
                all_data.append(["Empfehlung", f"{video_counter}.{idx}", title, link])

            # Erstes empfohlenes Video des dritten Hauptvideos öffnen
            if third_recommendations:
                next_video_title, next_video_url = third_recommendations[0]
                video_counter += 1
                print(f"{video_counter}. Hauptvideo: {next_video_title} ({next_video_url})")
                all_data.append(["Hauptvideo", video_counter, next_video_title, next_video_url])

                driver.get(next_video_url)
                time.sleep(5)  # Warten, bis das nächste Video geladen ist

                # Empfehlungen für das dritte Hauptvideo extrahieren
                fourth_recommendations = extract_recommended_titles()
                for idx, (title, link) in enumerate(fourth_recommendations, start=1):
                    print(f"  {video_counter}.{idx} Empfehlung: {title} ({link})")
                    all_data.append(["Empfehlung", f"{video_counter}.{idx}", title, link])

    # Daten in CSV speichern
    save_to_csv(all_data, "youtube_video_data_4.0.csv")

finally:
    driver.quit()  # Browser schließen