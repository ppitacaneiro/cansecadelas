from app.db import db, BaseModelMixin

class Pet(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_src = db.Column(db.String)
    url_adopt = db.Column(db.String)

    def __init__(self, name, image_src, url_adopt):
        self.name = name
        self.image_src = image_src
        self.url_adopt = url_adopt

    def __repr__(self):
        return f'Pet({self.name})'

    def __str__(self):
        return f'{self.name}'