from api import db

class Recipient(db.Model):
    __tablename__ = 'recipient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(120))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Recipient {}>'.format(self.name)


def init_db():
    db.create_all()

    # Create a test user
    #new_user = User('a@a.com', 'aaaaaaaa')
    #new_user.name = 'xxxx'
    #db.session.add(new_user)
    #db.session.commit()

if __name__ == '__main__':
    init_db()

