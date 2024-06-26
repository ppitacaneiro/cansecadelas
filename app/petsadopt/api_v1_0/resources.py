from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from app.common.error_handling import ObjectNotFound

from .schemas import PetSchema, SheltterSchema
from ..models import Pet, Sheltter

pets_adopt_v1_0_bp = Blueprint('pets_adopt_v1_0_bp', __name__)

pet_schema = PetSchema()
sheltter_schema = SheltterSchema()

api = Api(pets_adopt_v1_0_bp)

class PetListResource(Resource):
    # ?page=2&per_page=10
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            pagination = Pet.get_all_paginated(page, per_page)
            result = pet_schema.dump(pagination.items, many=True)
            return {
                'items': result,
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'message': 'Internal Server Error'}), 500
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
    
class ShellterListResource(Resource):
    def get(self):
        sheltters = Sheltter.get_all()
        result = sheltter_schema.dump(sheltters, many=True)
        return result, 200
    
class ShellterResource(Resource):
    def get(self, sheltter_id):
        sheltter = Sheltter.get_by_id(sheltter_id)
        if sheltter is None:
            raise ObjectNotFound('El refugio no existe')
        resp = sheltter_schema.dump(sheltter)
        return resp

api.add_resource(PetListResource, '/api/v1.0/pets/', endpoint='pet_list_resource')
api.add_resource(PetResource, '/api/v1.0/pets/<int:pet_id>', endpoint='pet_resource')
api.add_resource(ShellterListResource, '/api/v1.0/sheltters/', endpoint='sheltter_list_resource')
api.add_resource(ShellterResource, '/api/v1.0/sheltters/<int:sheltter_id>', endpoint='sheltter_resource')