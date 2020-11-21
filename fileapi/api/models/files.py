from fileapi.app.db import db


class FileModel(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(100))
    size = db.Column(db.Integer)
    description = db.Column(db.String(200))
    loaded_from = db.Column(db.String(250))
    loaded_to = db.Column(db.String(250))
    started_at = db.Column(db.DateTime, nullable=True, default=None)
    finished_at = db.Column(db.DateTime, nullable=True, default=None)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.name
