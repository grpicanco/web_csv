import enum
from extensao import db
from models.fonte import BaseModel


class TipoCampo(enum.Enum):
    INTEGER = 1
    FLOAT = 2
    STRING = 3
    DATE = 4
    BOOLEAN = 5


class Campo(BaseModel):
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.Enum(TipoCampo), default=TipoCampo.STRING)
    arquivo = db.relationship('Arquivo', backref='campo', lazy=True, cascade='all, delete')
