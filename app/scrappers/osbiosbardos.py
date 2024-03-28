from .scrapper import WebScrapper

class BiosbardosScrapper(WebScrapper):
    BASE_URL = "https://protectoraosbiosbardos.org/"
    
    def __init__(self, url, headers):
        super().__init__(url, headers)
        
    def extract_pet_info(self, soup):
        pet_info = []
        enlaces_paginas = []
        try:
            enlace_ultima_pagina = soup.find("a", title="Última página", href=True)
            
            if enlace_ultima_pagina:
                ultimo_numero_pagina = int(enlace_ultima_pagina["href"].split("=")[-1])
            else:
                raise ValueError("No se ha encontrado el enlace de la última página")
            
            for num_pagina in range(1, ultimo_numero_pagina + 1):
                enlace_pagina = f"{self.url}?p={num_pagina}"
                enlaces_paginas.append(enlace_pagina)
                
            for enlace in enlaces_paginas:
                print('enlace',enlace)
                content = self.get_page_content(enlace)
                soup = self.parse_content(content)
                tarjetas_adopcion = soup.find_all("div", class_="card-body")
                for tarjeta in tarjetas_adopcion:
                    try:
                        nombre_mascota_element = tarjeta.find("h3", class_="card-title")
                        url_imagen_element = tarjeta.find("img", class_="card-img-top")
                        enlace_ampliar_info_element = tarjeta.find("a", href=True)
                        if nombre_mascota_element and url_imagen_element and enlace_ampliar_info_element:
                            nombre_mascota = nombre_mascota_element.text.strip()
                            url_imagen = url_imagen_element["src"]
                            enlace_ampliar_info = enlace_ampliar_info_element["href"]    
                            pet_data = {
                            'pet_name': nombre_mascota,
                            'url_image': self.BASE_URL + url_imagen,
                            'url_website': enlace_ampliar_info
                            }
                            pet_info.append(pet_data)
                            print('pet_data',pet_data)
                    except Exception as e:
                        print(f"An error ocurred: {e}")
                        
        except Exception as e:
            print(f"An error ocurred: {e}")
        
        return pet_info
            
        