from .scrapper import WebScrapper

class CambadosScrapper(WebScrapper):
    def __init__(self, url, headers):
        super().__init__(url, headers)
        
    def extract_pet_info(self, soup):
        pet_info = []
        items = soup.find_all('ul', class_='products elementor-grid columns-3')
        for item in items:
            pets_names = item.find_all('h2', class_='woocommerce-loop-product__title')
            url_images = item.find_all('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            url_website = item.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
            for pet_name, url_image, url in zip(pets_names, url_images, url_website):
                pet_data = {
                    'pet_name': pet_name.text.strip(),
                    'url_image': url_image['src'],
                    'url_website': url['href']
                }
                pet_info.append(pet_data)
        return pet_info
        

