from app.db import db, BaseModelMixin

class Pet(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_src = db.Column(db.String)
    url_adopt = db.Column(db.String)
    sheltter_id = db.Column(db.Integer, db.ForeignKey('sheltter.id'), nullable=False)

    def __init__(self, sheltter_id, name, image_src, url_adopt):
        self.sheltter_id = sheltter_id
        self.name = name
        self.image_src = image_src
        self.url_adopt = url_adopt

    def __repr__(self):
        return f'Pet({self.name})'

    def __str__(self):
        return f'{self.name}'

class Sheltter(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    url = db.Column(db.String)
    pets = db.relationship('Pet', backref='sheltter', lazy=False, cascade='all, delete-orphan')

    def __init__(self, name, address, phone, url, latitude, longitude):
        self.name = name
        self.address = address
        self.phone = phone
        self.url = url
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'Sheltter({self.name})'

    def __str__(self):
        return f'{self.name}'