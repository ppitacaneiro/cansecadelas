import json
import os
import click
import requests
from app import create_app
from app.petsadopt.models import Pet
from app.scrappers.scrapper_factory import ScrapperFactory

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

def load_websites_from_json(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found")
        return []

@app.cli.command("scrapper")
@click.argument("filename")
def scrapper(filename):
    print("Scrapper command")
    Pet.delete_all()
    websites = load_websites_from_json(filename)
    for website in websites:
        name = website.get('name')
        url = website.get('url')
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
