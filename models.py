from flask_login import UserMixin
from __init__ import db,login_manager

class User(UserMixin, db.Model):
    userId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255),unique=True)

    def get_id(self):
           return (self.userId)

@login_manager.user_loader
def load_user(userId): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(userId))


class Client(UserMixin,db.Model):
    
    rowId = db.Column(db.Integer,primary_key=True)
    client_Id = db.Column(db.String(255),unique=True,nullable=False)
    agent_Id = db.Column(db.String(255),default=None)
    client_Share = db.Column(db.Integer,nullable=False)
    agent_Share = db.Column(db.Integer,default=None)
    fund_Tree_Share = db.Column(db.Integer,nullable=False)
    is_Eligible = db.Column(db.Boolean,default=False)
    pan_card = db.Column(db.Boolean,default=False)
    aadhar_card = db.Column(db.Boolean,default=False)
    bank_passbook = db.Column(db.Boolean,default=False)

    def get_id(self):
           return (self.client_Id)
