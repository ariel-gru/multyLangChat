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
        '''
        Initialize a headless Chrome browser
        '''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    
    def translate(self, text, target_language):
        """
        Translates the given text (any length) to the target language using Google Translate and Selenium.
        Automatically splits into 1600-character chunks.
        """
        translated_chunks = []

        for i in range(0, len(text), 1600):
            chunk = text[i:i+1600]
            encoded_chunk = urllib.parse.quote(chunk)
            url = f"https://translate.google.com/?sl=auto&tl={target_language}&text={encoded_chunk}"

            self.driver.get(url)

            try:
                translated_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "lRu31"))
                )
                translated_chunks.append(translated_element.text)
            except TimeoutException:
                print(f"Timeout on chunk: {chunk[:30]}...")
                translated_chunks.append("")

        return ''.join(translated_chunks)

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
