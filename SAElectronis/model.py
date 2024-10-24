# class Order(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.Boolean, default=False)
#     first_name = db.Column(db.String(64))
#     surname = db.Column(db.String(64))
#     email = db.Column(db.String(128))
#     phone = db.Column(db.String(32))
#     total_cost = db.Column(db.Float)
#     date = db.Column(db.DateTime)
#     # tours = db.relationship("Tour", secondary=orderdetails, backref="orders")
#     tours = db.relationship("Tour", secondary=orderdetails, back_populates='orders')
    
#     def __repr__(self):
#         return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.first_name}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nDate: {self.date}\nTours: {self.tours}\nTotal Cost: ${self.total_cost}"