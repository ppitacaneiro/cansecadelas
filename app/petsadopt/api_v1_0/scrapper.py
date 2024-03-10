from flask import Blueprint
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup
from ..models import Pet
from .schemas import PetSchema

pets_scrapper_v1_0_bp = Blueprint('pets_scrapper_v1_0_bp', __name__)

pet_schema = PetSchema()

api = Api(pets_scrapper_v1_0_bp)

class ScrapperResource(Resource):
    def get(self):
        pets = get_pets()
        result = pet_schema.dump(pets, many=True)
        return result, 200
    
api.add_resource(ScrapperResource, '/api/v1.0/scrapper/', endpoint='pet_scrapper')

def get_pets():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    # Realizar la solicitud HTTP
    page = requests.get('https://refugiocambados.es/adopta/animales-en-adopcion/', headers=headers)

    data_pets = []
    pets = []

    # Parsear el contenido HTML
    soup = BeautifulSoup(page.text, 'html.parser')

    # Encontrar todos los elementos h2 con la clase "woocommerce-loop-product__title"
    items = soup.find_all('ul', class_='products elementor-grid columns-3')

    # Iterar sobre los elementos encontrados
    for item in items:
        # Obtener el texto del elemento h2 (nombre de la mascota)
        pets_names = item.find_all('h2', class_='woocommerce-loop-product__title')
        
        # Obtener las URLs de las imágenes
        url_images = item.find_all('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
        
        # Obtener las URLs de los sitios web de las mascotas
        url_website = item.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
        
        # Iterar sobre cada conjunto de datos y crear un diccionario para cada mascota
        for pet_name, url_image, url in zip(pets_names, url_images, url_website):
            pet_data = {
                'pet_name': pet_name.text.strip(),
                'url_image': url_image['src'],
                'url_website': url['href']
            }
            data_pets.append(pet_data)

        # Imprimir los datos de las mascotas (solo para verificar)
        try:
            for pet in data_pets:
                print(pet)
                new_pet = Pet(
                    name=pet['pet_name'],
                    image_src=pet['url_image'],
                    url_adopt=pet['url_website'],
                )
                new_pet.save()
                pets.append(new_pet)
                
            print(pets)
            return pets
        except Exception as e:
            raise Exception('Error al guardar la mascota', e)
    