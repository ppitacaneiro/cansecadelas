import os
import click
import requests
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
    
    try:
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
    except requests.exceptions.RequestException as e:
        print(f"Unable to connect to the website: {e}")
    except Exception as e:
        print(f"An error ocurred: {e}")
    else:   
        print("Scrapper command finished successfully")
    finally:
        print("Scrapper command finished")
