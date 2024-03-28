from .scrapper import WebScrapper

class ApadanScrapper(WebScrapper):
    def __init__(self, url, headers):
        super().__init__(url, headers)
        
    def extract_pet_info(self, soup):
        pet_info = []
        pages_urls = self.get_all_pages(soup)
        for page_url in pages_urls:
            try:
                content = self.get_page_content(page_url)
                soup = self.parse_content(content)
                pets = self.extract_pet_info_from_page(soup)
                pet_info.extend(pets)
            except Exception as e:
                print(f"Error ocurred while trying to get the content of the page {page_url} - {e}")
                
        return pet_info
    
    def extract_pet_info_from_page(self, soup):
        pets_data = []
        pets_in_page = soup.find_all('article', class_='fusion-portfolio-post')
        for pet in pets_in_page:
            try:
                pet_name = pet.find('h4', class_='fusion-rollover-title').text
                url_more_info = pet.find('h4', class_='fusion-rollover-title').find('a')['href']
                url_image = pet.find('img')['src']
                pet_data = {
                    'pet_name': pet_name.strip(),
                    'url_image': url_image,
                    'url_website': url_more_info
                }
                pets_data.append(pet_data)
            except Exception as e:
                print(f"Error ocurred while trying to extract the pet info - {e}")
            
        return pets_data
            
    
    def get_all_pages(self, soup):
        pagination_container = soup.find("div", class_="pagination clearfix")
        page_links = pagination_container.find_all('a', class_='inactive')
        return self.get_url_of_all_pages(page_links)
        
    def get_url_of_all_pages(self, page_links):
        urls = []
        for link in page_links:
            url = link['href']
            urls.append(url)
            
        first_page = urls[0].replace('page/2','page/1')
        urls.insert(0, first_page)
        return urls