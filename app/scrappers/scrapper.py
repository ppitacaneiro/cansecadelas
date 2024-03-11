import requests
from bs4 import BeautifulSoup

class WebScrapper:
    
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        
    def get_page_content(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.content
    
    def parse_content(self, content):
        return BeautifulSoup(content, 'html.parser')
    
    def extract_pet_info():
        raise NotImplementedError("This method must be implemented in a subclass")
    
    def scrap(self):
        content = self.get_page_content()
        soup = self.parse_content(content)
        return self.extract_pet_info(soup)
            