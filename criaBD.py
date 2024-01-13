from fakePinterest import database,app
from fakePinterest.models import Usuario, Fotos

with app.app_context():
    database.create_all()