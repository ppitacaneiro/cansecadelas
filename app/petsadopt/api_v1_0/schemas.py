from marshmallow import fields
from app.ext import ma

class PetSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    image_src = fields.String()
    url_adopt = fields.String()
    sheltter_id = fields.Integer()
    sheltter = fields.Nested('SheltterSchema')
    
class SheltterSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    address = fields.String()
    phone = fields.String()
    email = fields.String()
    url = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()