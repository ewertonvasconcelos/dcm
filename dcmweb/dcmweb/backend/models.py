from flask_sqlalchemy import SQLAlchemy
from dcmweb import app

db = SQLAlchemy(app)


class Server(db.Model):
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String())
    datacenter = db.Column(db.String())
    rack = db.Column(db.String())
    position = db.Column(db.String())
    video_port = db.Column(db.String())
    mgnt_port = db.Column(db.String())
    status = db.Column(db.String())
    uptime = db.Column(db.String())

    def __init__(self, hostname, datacenter, rack, position, video_port, mgnt_port, uptime="0", status="DISCOVERING"):
        self.hostname = hostname
        self.datacenter = datacenter
        self.rack = rack
        self.position = position
        self.video_port = video_port
        self.mgnt_port = mgnt_port
        self.uptime = uptime
        self.status = status 
        

    def __repr__(self):
        return '<id {}>'.format(self.id)