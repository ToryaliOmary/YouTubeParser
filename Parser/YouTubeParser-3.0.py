
# Dieser Code öffnet Youtube, sucht einen Begriff, öffnet das erste Video, speichert die ersten 5 Empfehlungen, 
# öffnet das erste emphohlene Video, speichert dessen ersten 5 Empfehlungen 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Funktion zum Extrahieren der Titel der ersten 5 empfohlenen Videos
def extract_recommended_titles():
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(3)  # Zusätzliche Wartezeit für das Laden der Empfehlungen

    recommended_videos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-compact-video-renderer span#video-title'))
    )

    titles = []
    for video in recommended_videos[:5]:
        titles.append(video.text)
    return titles

# WebDriver initialisieren
driver = webdriver.Chrome(options=options)

try:
    # YouTube öffnen
    driver.get("https://www.youtube.com")
    time.sleep(2)  # Kurz warten, bis die Seite geladen ist

    # Nach einem Begriff suchen
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Kindervideos")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Warten, bis die Ergebnisse geladen sind

    # Erstes Video anklicken und Titel ausgeben
    first_video = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]'))
    )
    first_video_title = first_video.get_attribute("title")
    print(f"Erstes Video: {first_video_title}")
    driver.execute_script("arguments[0].scrollIntoView(true);", first_video)
    driver.execute_script("arguments[0].click();", first_video)  # Klick mit JavaScript
    time.sleep(5)  # Warten, bis das Video geladen ist

    # Titel der ersten 5 Empfehlungen extrahieren
    first_recommendations = extract_recommended_titles()
    print("Empfohlene Videos nach dem ersten Video:")
    for idx, title in enumerate(first_recommendations, start=1):
        print(f"  {idx}. {title}")

    # Erstes empfohlenes Video anklicken
    recommended_video = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-compact-video-renderer span#video-title'))
    )
    recommended_video_link = recommended_video.find_element(By.XPATH, "ancestor::a")
    driver.execute_script("arguments[0].scrollIntoView(true);", recommended_video_link)
    driver.execute_script("arguments[0].click();", recommended_video_link)  # Klick mit JavaScript
    time.sleep(5)  # Warten, bis das empfohlene Video geladen ist

    # Titel der ersten 5 Empfehlungen nach dem zweiten Video extrahieren
    second_recommendations = extract_recommended_titles()
    print("Empfohlene Videos nach dem zweiten Video:")
    for idx, title in enumerate(second_recommendations, start=1):
        print(f"  {idx}. {title}")

finally:
    driver.quit()  # Browser schließen
