from marshmallow import fields
from app.ext import ma

class PetSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    image_src = fields.String()
    url_adopt = fields.String()
    