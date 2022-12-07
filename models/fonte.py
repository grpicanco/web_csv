from datetime import date
from extensao import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    dt_criacao = db.Column(db.Date, nullable=False, default=date.today())
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Fonte(BaseModel):
    site = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)
