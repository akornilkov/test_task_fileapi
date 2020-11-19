from fileapi.app.db import db


class StatusModel(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Status name={self.name} name_en={self.name_en}>'
