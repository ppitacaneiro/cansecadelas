import os
import click
from app import create_app
from app.scrappers.cambados import CambadosScrapper
from app.petsadopt.models import Pet

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

@app.cli.command("scrapper")
def scrapper():
    print("Scrapper command")
    Pet.delete_all()
    # config
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    }
    # extract from config file in json format
    url = 'https://refugiocambados.es/adopta/animales-en-adopcion/'
    
    scrapper = CambadosScrapper(url, headers)
    pets = scrapper.scrap()
    for pet in pets:
        print(pet)
        new_pet = Pet(
            name=pet['pet_name'],
            image_src=pet['url_image'],
            url_adopt=pet['url_website'],
        )
        new_pet.save()
    print("Scrapper command finished")
