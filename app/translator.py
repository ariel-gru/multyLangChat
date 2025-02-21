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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    #Spliting the text to make the translation faster in case of a long sentence.
    def split_translate(self, text, target_language):
        """
        Spliting the text.
        """
        chunks = []
        translated_text = ""
        for i in range(0, len(text), 1600):
            chunks.append(text[i:i+1600])
        for chunk in chunks:
                translated_text += self.translate(chunk, target_language)
        return translated_text

    def translate(self, text_to_translate, target_language):
        """
        Translate the given text to the target language using Google Translate.
        """
        if len(text_to_translate) > 1600:
            self.split_translate(text_to_translate,target_language)
        #URL matching
        text_to_translate = urllib.parse.quote(text_to_translate)
        
        # google translate url pattern
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


if __name__ == "__main__":
    translator = Translator()
    #hebrew translation test
    while True:
        sipur = input("Enter text to translate: ")
        if sipur == "XXX":break
        translated_text = translator.translate(sipur, "iw")#iw --> abbreviation for Hebrew.
        print(f"Translated text: {translated_text}")
    
    translator.quit()
