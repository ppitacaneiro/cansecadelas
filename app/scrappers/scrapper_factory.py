from app.scrappers.cambados import CambadosScrapper
from app.scrappers.osbiosbardos import BiosbardosScrapper

class ScrapperFactory:
    
    deafult_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    }
    
    @staticmethod
    def get_scrapper(scrapper_name, url, headers = deafult_headers):
        if scrapper_name == 'cambados':
            return CambadosScrapper(url, headers)
        elif scrapper_name == 'osbiosbardos':
            return BiosbardosScrapper(url, headers)
        else:
            raise ValueError("Invalid scrapper name")