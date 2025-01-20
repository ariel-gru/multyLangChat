import urllib.parse
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def split_text_to_chunks(text):
    """
    Split text into chunks of a given size, trying to keep full sentences.
    """
    chunks = []
    for i in range(0, len(text), 1600):
        chunks.append(text[i:i+1600])
    return chunks
#i=0
def translate(text_to_translate,targer_language):
    #global i
    translated_text=""
    if len(text_to_translate) > 1600:
        #print(1)
        chunks=split_text_to_chunks(text_to_translate)
        for chunk in chunks:
            translated_text += translate(chunk,targer_language)
        return translated_text
    
    text_to_translate = urllib.parse.quote(text_to_translate)
    
    template = f"https://translate.google.com/?sl=auto&tl={targer_language}&text={text_to_translate}"
    
    driver.get(template)
    #i=i-1
    #print(i)
    try:
        translated_text_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lRu31"))
        )
        return translated_text_element.text
    except TimeoutException:
        print("Timed out waiting for translation")
        return ""
sipur=input("enter text")
print(translate(sipur,"en"))

driver.quit()
