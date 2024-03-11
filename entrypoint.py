import os
import click
from app import create_app
from app.petsadopt.models import Pet
from app.scrappers.scrapper_factory import ScrapperFactory

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

@app.cli.command("scrapper")
def scrapper():
    print("Scrapper command")
    Pet.delete_all()
    
    url = 'https://refugiocambados.es/adopta/animales-en-adopcion/'
    name = 'cambados'
    
    scrapper = ScrapperFactory.get_scrapper(name, url)
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
