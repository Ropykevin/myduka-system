from flask import Flask, render_template, request, redirect, url_for, flash,session
from dbservice import get_data, insert_products, insert_sales, s_product, product_profit, register_user, check_email, update_product,conn,curr
from flask_bcrypt import Bcrypt
from functools import wraps

# create Flask instance
# configure your application
# define routes
# run the application
app = Flask(__name__)
# url => uniform resource locator
# Routes =>
bcrypt = Bcrypt(app)
app.secret_key="sssss"


def login_required(f):
    @wraps(f)
    def protected():
        if 'email' not in session:
            return redirect(url_for('login'))
    return protected

@app.route("/")
def index():
    return render_template("index.html")

# home


@app.route("/home")
def home():
    return render_template("index.html")

# products route


@app.route("/products")
def products():
    if "email" not in session:
        return redirect(url_for('login'))
    prods = get_data("products")
    return render_template('products.html', prods=prods)


@app.route('/add_products', methods=['POST', 'GET'])
def add_products():
    # check method
    if request.method == "POST":
        # request data
        pname = request.form['product_name']
        bprice = request.form['buying_price']
        sprice = request.form['selling_price']
        squantity = request.form['stock_quantity']
        # insert products
        new_prod = (pname, bprice, sprice, squantity)
        insert_products(new_prod)
        return redirect(url_for('products'))
# sales
# display sales inside a table

# https methods
# techniques  used to send,fetch,update,delete from the browser
# post =>send
# get => fetch
# put=>update
# delete=>

# edit product
@app.route('/edit_product',methods=['POST','GET'])
def edit_prod():
    if "email" not in session:
        return redirect(url_for('login'))
    if request.method=="POST":
        pid = request.form['product_id']
        pname = request.form['product_name']
        bprice = request.form['buying_price']
        sprice = request.form['selling_price']
        squantity = request.form['stock_quantity']
        # update
        query = '''UPDATE products
           SET name = %s,
               buying_price = %s,
               selling_price = %s,
               stock_quantity = %s
           WHERE id = %s'''
        # Assuming you are using a cursor from a database connection
        curr.execute(query, (pname, bprice, sprice, squantity, pid))
        # commit the changes
        conn.commit
        return redirect(url_for('products'))
    return render_template('edit_product.html')



@app.route("/sales")
def sales():
    if "email" not in session:
        return redirect(url_for('login'))
    sale = get_data("sales")
    products = get_data("products")
    return render_template("sales.html", sales=sale, products=products)


@app.route("/make_sale", methods=["POST", "GET"])
def make_sale():
    # check the method
    if request.method == "POST":
        # request data
        pid = request.form['pid']
        quantity = request.form['quantity']
        # insert sale
        new_sale = (pid, quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))


# create html files for each route
# products.html
# home.html
# sales.html
# dashboard.html

@app.route('/dashboard')
@login_required
def dashboard():
    s_prods = s_product()
    print(s_prods)
    names = []
    sales = []
    for i in s_prods:
        names.append(i[0])
        sales.append(float(i[1]))
    return render_template('dashboard.html', names=names, sales=sales)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        # get form data
        fname = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        x = check_email(email)
        if x==None:
            # insert user
            new_user = (fname, email, hashed_password)
            register_user(new_user)
            return redirect(url_for('login'))
        else:
            flash("Email already exists login ")
            return redirect(url_for('login'))
    return render_template('register.html')


# flash messages
# login.html
# route to login user
# write a query thats going to fetch the user  with an email and password
# select * from users where email=%s and password=%s;
#
# create a function on dbservice thats going fetch the user with an email and password

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # get form data
        email = request.form['email']
        password = request.form['password']
        user = check_email(email)
        print(user)
        
        if user==None:
            flash("Email does not exist")
            return redirect(url_for('register'))
        else:
            # check password
            if bcrypt.check_password_hash(user[-1],password):
                flash('login successful')
                # store email in session
                session['email']=email
                return redirect(url_for('dashboard'))
            else:
                flash("password is incorrect")
    return render_template('login.html')



# logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

app.run(debug=True) 
