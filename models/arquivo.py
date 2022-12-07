from models.fonte import BaseModel
from extensao import db


class Arquivo(BaseModel):
    titulo = db.Column(db.String(120), nullable=False)
    separador = db.Column(db.String(120), nullable=False)
    fonte = db.relationship('Fonte', backref='arquivo', lazy=True, cascade="all, delete")
