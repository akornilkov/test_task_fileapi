from datetime import datetime
from fileapi.app.db import db


class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False, default=0)
    files = db.relationship('FileModel', backref='tasks', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.name
