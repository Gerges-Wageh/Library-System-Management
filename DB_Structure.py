from peewee import *
import datetime
############# Here i create class for every table in my database i wanna deal with #############

###### this part is for choices before every thing need choices
##tuple of tuples(choices) the first arg of an inner tuple is saved in DB and the other is shown to user##
#### after that go to anyline with choices and them let choices = this variable
### for example ///// status = CharField(choices = book_status) \\\\\
class Publisher(Model):
    name = CharField(unique=True)
    location = CharField(null=True)

    class Meta:
        database = db

class Author(Model):
    name = CharField(unique=True)
    location = CharField(null=True)

    class Meta:
        database = db



class Category(Model):
    category_name = CharField(unique=True)
    parent_category = IntegerField(null=True)
    ##Recursive RelationShip (like tree of categories )

    class Meta:
        database = db

class Branch(Model):
    name = CharField()
    code = CharField(null=True,unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


Book_Status = (
    (1,'New'),
    (2,'Used'),
    (3,'Damage'),
)

class Books(Model):
    title = CharField(unique=True)  # data type of character takes one line at most
    #null y3ny ynf3 a5zn el 7aga de fe mkan empty wla lazm tt5zn b value (defalut:null=false)
    description = TextField(null=True) #data type of text takes bunch of words
    category = ForeignKeyField(Category,backref='category',null=True )
    #data type of relations between tables----backreference
    code = CharField(null=True)
    # parts *
    part_order = IntegerField(null=True)  #el Goz2 el kam ?
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher,backref='publisher',null=True)
    author = ForeignKeyField(Author,backref='author',null=True)
    image = CharField(null=True)
    status = CharField(choices=Book_Status)
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class Clients(Model):
    name = CharField()
    mail = CharField(null=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True , unique=True)

    class Meta:
        database = db


class Employee(Model):
    name = CharField()
    mail = CharField(null=True , unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True,unique=True)
    periority = IntegerField(null=True)

    class Meta:
        database = db



Process_Type = (
    (1,'Rent'),
    (2,'Retrieve')
)
class Daily_Movments(Model):
    book = ForeignKeyField(Books,backref='daily_book')
    client = ForeignKeyField(Clients,backref='book_client')
    type = CharField(choices=Process_Type)  # Choices \\\rent or retrieve
    date = DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch,backref='daily_branch',null=True)
    book_from = DateField(null=True)
    book_to = DateField(null=True)
    employee = ForeignKeyField(Employee,backref='daily_employee',null=True) #the employee that handles this operation

    class Meta:
        database = db


Actions_Type = (
    (1,'Login'),
    (2,'Update'),
    (3,'Create'),
    (4,'Delete')
)
Table_Choices = (
    (1,'Books'),
    (2,'Clients'),
    (3,'Employee'),
    (4,'Category'),
    (5,'Branch'),
    (6,'Daily Movements'),
    (7,'Publisher'),
    (8,'Author')
)
class History(Model):
    employee = ForeignKeyField(Employee,backref='history_employee')
    action = CharField(choices=Actions_Type) # Choices
    table = CharField(choices=Table_Choices) #Choices
    date = DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch,backref='history_branch')

    class Meta:
        database = db



############## the next two line to create tables for our classes in MySQL ##############
db.connect()
db.create_tables([Books,Clients,Employee,Category,Branch,Daily_Movments ,History,Publisher,Author])

###########################################################################






