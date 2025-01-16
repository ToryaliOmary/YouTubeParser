##Dieser Code öffnet Youtube, sucht nach einem Begriff und notiert dessen Titel 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Chrome-Optionen einstellen
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # GPU-Beschleunigung deaktivieren
options.add_argument("--no-sandbox")  # Sandbox-Modus deaktivieren (optional)
options.add_argument("--disable-dev-shm-usage")  # Speicherproblemen vorbeugen (optional)

# WebDriver mit Optionen initialisieren
driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com")

# Warten, bis die Seite vollständig geladen ist
time.sleep(2)

# Suchfeld finden und "Kindervideos" eingeben
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Kindervideos")
search_box.send_keys(Keys.RETURN)

# Warten, bis die Suchergebnisse geladen sind
time.sleep(2)

# Titel des ersten Videos extrahieren
try:
    first_video = driver.find_element(By.XPATH, '//*[@id="video-title"]')
    print("Titel des ersten Videos:", first_video.get_attribute("title"))
except Exception as e:
    print("Fehler beim Abrufen des Videotitels:", e)

# Browser schließen
driver.quit()
