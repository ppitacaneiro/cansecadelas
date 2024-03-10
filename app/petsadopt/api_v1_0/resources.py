from flask import request, Blueprint
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound

from .schemas import PetSchema
from ..models import Pet

pets_adopt_v1_0_bp = Blueprint('pets_adopt_v1_0_bp', __name__)

pet_schema = PetSchema()

api = Api(pets_adopt_v1_0_bp)

class PetListResource(Resource):
    def get(self):
        pets = Pet.get_all()
        result = pet_schema.dump(pets, many=True)
        return result, 200
    def post(self):
        print("Se ha llamado al método POST de PetListResource")  
        data = request.get_json()
        pet_dict = pet_schema.load(data)
        pet = Pet(
            name=pet_dict['name'],
            image_src=pet_dict['image_src'],
            url_adopt=pet_dict['url_adopt'],
        )
        pet.save()
        resp = pet_schema.dump(pet)
        return resp, 201

class PetResource(Resource):
    def get(self, pet_id):
        pet = Pet.get_by_id(pet_id)
        if pet is None:
            raise ObjectNotFound('La mascota no existe')
        resp = pet_schema.dump(pet)
        return resp

api.add_resource(PetListResource, '/api/v1.0/pets/', endpoint='pet_list_resource')
api.add_resource(PetResource, '/api/v1.0/pets/<int:pet_id>', endpoint='pet_resource')