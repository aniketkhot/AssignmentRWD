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

class Product:
    def __init__(self, productId, productName, description, prize, CPU, GPU, camera, battery, productReleaseDate,image):
        self.productId = productId
        self.productName = productName
        self.description = description
        self.prize = prize
        self.CPU = CPU
        self.GPU = GPU
        self.camera = camera
        self.battery = battery
        self.productReleaseDate=productReleaseDate
        self.image = image



    def get_category_details(self):
        return str(self)

    def __repr__(self):
        str = "ProductId {}, ProductName {}, Description {}, Prize {}, CPU {}, GPU {}, Camera {}, Battery {}, ProductReleaseDate {},image {}\n"
        str = str.format(self.productId,self.productName,self.description, self.prize, self.CPU, self.GPU, self.camera, self.battery,self.productReleaseDate, self.image)
        return str

class User:
    def __init__(self, userId, firstName, lastName, email, login, logOut):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.login = login
        self.logOut = logOut

    def get_User_details(self):
        return str(self)
    
    def __repr__(self):
        str = "UserId: {}, FirstName: {}, LastName: {}, Email: {}, Login: {}, LogOut: {}\n"
        str = str.format(self.userId,self.firstName,self.lastName,self.email,self.login,self.logOut)
        return str
    
class ProductDetails:
    def __init__(self, detailsId, description, productId, categoryId, metaData, versioning, changeDetails, addNewVersion):
        self.detailsId = detailsId
        self.description = description
        self.productId = productId
        self.categoryId = categoryId
        self.metaData = metaData
        self.versioning = versioning
        self.changeDetails = changeDetails
        self.addNewVersion = addNewVersion

    def get_book_details(self):
        return str(self)
    
    def __repr__(self):
        str = "DetailsId: {}, Description: {}, ProductId: {}, CategoryId: {}, MetaData: {}, Versioning: {}, ChangeDetails: {}, AddNewVersion: {}\n"
        str = str.format(self.detailsId,self.description,self.productId,self.categoryId,self.metaData,self.versioning,self.changeDetails,self.addNewVersion)
        return str
    
class Basket:
    def __init__(self, basketId, basketLimit, products, basketName):
        self.basketId = basketId
        self.basketLimit = basketLimit
        self.products = products
        self.basketName = basketName


    def get_User_details(self):
        return str(self)
    
    def __repr__(self):
        str = "BasketId: {}, BasketLimit: {},Products: {}, BasketName\n"
        str = str.format(self.basketId,self.basketLimit,self.products, self.basketName)
        return str
    
class Category:
    def __init__(self, categoryId, categoryName, categoryDetails, removeCategory, filterByCategory):
        self.categoryId = categoryId
        self.categoryName = categoryName
        self.categoryDetails = categoryDetails
        self.removeCategory = removeCategory
        self.filterCategory = filterByCategory


    def get_User_details(self):
        return str(self)
    
    def __repr__(self):
        str = "CategoryId: {}, CategoryName: {}, CategoryDetails: {}, RemoveCategory: {}, FilterCategory: {}\n"
        str = str.format(self.categoryId,self.categoryName,self.categoryDetails,self.removeCategory,self.filterCategory)
        return str



    
    
