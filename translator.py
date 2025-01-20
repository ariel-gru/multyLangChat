import urllib.parse
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Translator:
    def __init__(self):
        # הגדרת אפשרויות לדפדפן כרום במצב ראשוני (Headless)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def split_text_to_chunks(self, text):
        """
        Split text into chunks of a given size, trying to keep full sentences.
        """
        chunks = []
        for i in range(0, len(text), 1600):
            chunks.append(text[i:i+1600])
        return chunks

    def translate(self, text_to_translate, target_language):
        """
        Translate the given text into the target language using Google Translate.
        """
        translated_text = ""
        
        if len(text_to_translate) > 1600:
            chunks = self.split_text_to_chunks(text_to_translate)
            for chunk in chunks:
                translated_text += self.translate(chunk, target_language)
            return translated_text
        
        # הצפנה של הטקסט כך שיתאים ל-URL
        text_to_translate = urllib.parse.quote(text_to_translate)
        
        # בניית URL של Google Translate
        template = f"https://translate.google.com/?sl=auto&tl={target_language}&text={text_to_translate}"
        
        self.driver.get(template)
        
        try:
            translated_text_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lRu31"))
            )
            return translated_text_element.text
        except TimeoutException:
            print("Timed out waiting for translation")
            return ""

    def quit(self):
        """
        Close the browser.
        """
        self.driver.quit()


# שימוש בקלאס:
if __name__ == "__main__":
    translator = Translator()
    
    while True:
        sipur = input("Enter text to translate: ")
        if sipur == "XXX":break
        translated_text = translator.translate(sipur, "en")
        print(f"Translated text: {translated_text}")
    
    translator.quit()
