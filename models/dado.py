from extensao import db
from models.fonte import BaseModel


class Dado(BaseModel):
    index = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.String(120), nullable=False)
    campo = db.relationship('Campo', backref='dado', lazy=True, cascade="all, delete")
