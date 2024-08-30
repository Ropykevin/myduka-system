import psycopg2

# connect to the database
conn=psycopg2.connect(
    dbname="myduka_db",
    password="Kevin254!",
    user="postgres",
    host='localhost',
    port=5432
)
# define the coursor perfoms database operations
curr=conn.cursor()

# fetch data
def get_data(table_name):
    query=f"select * from {table_name}"
    curr.execute(query)
    data=curr.fetchall()
    return data
# insert data

def insert_products(values):
    query = "insert into products(name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
    curr.execute(query, values)
    conn.commit()

def insert_sales(values):
    query = "insert into sales(pid,quantity,created_at)values(%s,%s,now())"
    curr.execute(query, values)
    conn.commit()

# profit per product 
def product_profit():
    query = "select name,sum((selling_price-buying_price)*quantity)as profit from products join sales on products.id=sales.pid group by name"
    curr.execute(query)
    data=curr.fetchall()
    return data

# sales per product 

def s_product():
    query = "select name,sum(selling_price*quantity)as sales from products join sales on products.id=sales.pid group by name;"
    curr.execute(query)
    data=curr.fetchall()
    return data
    
# profit per day

# profit per product

# register user

def register_user(values):
    query="insert into users (full_name,email,password)values(%s,%s,%s)"
    curr.execute(query,values)
    conn.commit()


# query to check email existance on db (exist)
# select * from users where email = 'ropy@gmail.com'
# fuction to check email
def check_email(email):
    query = "select * from users where email = %s"
    curr.execute(query,(email,))
    data=curr.fetchone()
    if data:
        return data
    

# login.html create a form to login user


def check_email_pass(email,password):
    query = "select * from users where email = %s and password = %s"
    curr.execute(query,(email,password))
    data=curr.fetchall()
    return data