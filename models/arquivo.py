from models.fonte import BaseModel
from extensao import db


class Arquivo(BaseModel):
    titulo = db.Column(db.String(120), nullable=False)
    separador = db.Column(db.String(120), nullable=False)
    fonte = db.Column(db.Integer, db.ForeignKey('fonte.id', ondelete="CASCADE"), nullable=False)

    def json(self):
        return {
            'id': f'{self.id}',
            'titulo': f'{self.titulo}',
            'separador': f'{self.separador}',
            'fonte': f'{self.fonte}',
            'ativo': f'{self.ativo}',
            'dt_criacao': f'{self.dt_criacao}'
        }
