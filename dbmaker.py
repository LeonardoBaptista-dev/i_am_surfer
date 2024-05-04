from iamsurfer import database, app
from iamsurfer.models import Usuario, Foto
from datetime import datetime, timezone

with app.app_context():
    database.create_all()       