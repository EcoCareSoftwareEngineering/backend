from . import db


class IotDevices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
