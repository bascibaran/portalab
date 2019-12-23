from app import db


class Dataset(db.Model):
    __tablename__ = 'data_catalog'

    id = db.
    name = db.Column(db.String(20))

    type = db.Column(db.String(20)) 

    def __repr__(self):
        return 'Id: {}, name: {}'.format(self.id, self.name)
