from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    role = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % (self.user_id)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    executor_id = db.Column(db.Integer, default=None)
    customer_id = db.Column(db.Integer)
    ts = db.Column(db.String(256))
    status = db.Column(db.Integer)
    time_start = db.Column(db.Integer, default=None)
    time_end = db.Column(db.Integer, default=None)

    def __repr__(self):
        return '<Order %r>' % (self.ts_id)