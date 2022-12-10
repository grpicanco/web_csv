from models.fonte import BaseModel
from extensao import db


class Arquivo(BaseModel):
    titulo = db.Column(db.String(120), nullable=False)
    separador = db.Column(db.String(120), nullable=False)
    fonte = db.Column(db.Integer, db.ForeignKey('fonte.id', ondelete="CASCADE"), nullable=False)
