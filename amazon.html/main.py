from flask import Flask, redirect, url_for, render_template, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(_name_)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class Products(Base):
    _tablename_ = 'Product_name'
    id = Column(Integer, primary_key=True)
    Product_name = Column(String(30), nullable=False)
    Product_owner = Column(String(40), nullable=False)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f'Product name: {self.Product_name}; Product_owner: {self.Product_owner}; Price: {self.price}'
    
engine = create_engine('sqlite:///Products.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in flask_session:
        subjects = ['Westinghouse Outdoor Power Equipment 12500 Peak Watt Tri-Fuel Home Backup Portable Generator, Remote Electric Start, Transfer Switch Ready, Gas, Propane, and Natural Gas Powered', 'SAMSUNG Galaxy S24 Ultra Cell Phone, 256GB AI Smartphone, Unlocked Android, 50MP Zoom Camera, Long Battery Life, S Pen, US Version, 2024, Titanium Gray', 'Amazon Fire TV 55" Omni QLED Series 4K UHD smart TV, Dolby Vision IQ, Fire TV Ambient Experience, local dimming, hands-free with Alexa']
        return render_template('user.html', subjects=subjects)
    return redirect(url_for('login'))

@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    flask_session.pop('user', None)
    return 'You are logged out'

@app.route('/amazonproducts', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        Product_name = request.form['Product_name']
        Product_owner = request.form['Product_owner']
        price = request.form['price']
        if Product_name and Product_owner and price:
            try:
                price = float(price)
                new_book = Products(Product_name=Product_name, Product_owner=Product_owner, price=price)
                db_session.add(new_book)
                db_session.commit()
                return 'Data added successfully'
            except ValueError:
                return 'Invalid input for price'
    return render_template('amazonproducts.html')

if _name_ == "_main_":
    app.run(debug=True)

book1 = Products(Product_name='Westinghouse Outdoor Power Equipment 12500 Peak Watt Tri-Fuel Home Backup Portable Generator, Remote Electric Start, Transfer Switch Ready, Gas, Propane, and Natural Gas Powered', 
 Product_owner='Mark Smith', price=1499.99)
db_session.add(book1)
db_session.commit()

book2 = Products(Product_name='SAMSUNG Galaxy S24 Ultra Cell Phone, 256GB AI Smartphone, Unlocked Android, 50MP Zoom Camera, Long Battery Life, S Pen, US Version, 2024, Titanium Gray',
 Product_owner='Samsung', price=1299.99)
db_session.add(book2)
db_session.commit()

result = db_session.query(Products).all()
for row in result:
    print(row)