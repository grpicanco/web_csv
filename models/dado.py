from extensao import db
from models.fonte import BaseModel


class Dado(BaseModel):
    index = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.String(120), nullable=False)
    campo = db.Column(db.Integer, db.ForeignKey('campo.id', ondelete='CASCADE'), nullable=False)
