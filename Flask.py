#!/hkedwardu/205CDE/bin/python
from flask import Flask, render_template, request, redirect, session
from tabulate import tabulate
from email_validator import validate_email, EmailNotValidError
import threading
import pymysql

app = Flask(__name__)
app.secret_key = 'ABCDE'#!/hkedwardu/205CDE/bin/python
from flask import Flask, render_template, request, redirect, session
from tabulate import tabulate
from email_validator import validate_email, EmailNotValidError
import threading
import pymysql

app = Flask(__name__)
app.secret_key = 'ABCDE'

db = pymysql.connect(host="localhost", user="newuser", password="password", database="website_db")

newuser = "New Comer"
lock = threading.Lock()

@app.route('/')
def index():
    if 'username' in session: # if user is logged in
        return render_template('Index_Logined.html', name = session['username'])
    else:   #if user is not logged in
        return render_template('Index.html', name = newuser)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Get product ID to search the product price
    P_ID = request.form['product_id']
    mycursor = db.cursor()
    sql = "SELECT P_Price FROM product WHERE P_ID = %s"
    val = (P_ID)
    mycursor.execute(sql, val)
    for row in mycursor:
        P_price = row[0]

    # Add row to the 'cart' table
    sql = "INSERT INTO cart (C_ID, P_ID, P_Quantity, Price) VALUES (%s, %s, %s, %s)"
    val = (session['user_CID'], P_ID, 1, P_price)
    mycursor.execute(sql, val)
    db.commit()
    POPUP = "The product added into your cart!"
    
    #send message to confirm
    return render_template('Index_Logined.html', POPMessage = POPUP)

@app.route('/Sign_Up', methods=['GET', 'POST'])
def SignUp():
    #Get user's name,Email, password, gender, phone number and address
    if request.method == 'POST':
        username = request.form['name']
        userEmail = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        UserPhNum = request.form['phone']
        UserAddr = request.form['address']
        SignUpmessage = ''

        try:
            valid = validate_email(userEmail)
        except ValueError as e:
            SignUpmessage = 'Unvalid Email address, please enter again.'
            return render_template('Sign_Up.html', name = newuser, SignUpmessage = SignUpmessage)

        # Add them into the 'customers' table
        mycursor = db.cursor()
        sql = "INSERT INTO customers (C_ID, C_NAME, C_Email, C_Password, gender, Phone_Num, Address) VALUES ( NULL, %s, %s, %s, %s, %s, %s)"
        val = (username, userEmail, password, gender, UserPhNum, UserAddr)
        mycursor.execute(sql, val)

        try:
            db.commit()
            sql = "INSERT INTO login (C_ID, C_NAME, C_Password) VALUES ( %s, %s, %s)"
            val = (mycursor.lastrowid, username, password)
            mycursor.execute(sql, val)
            db.commit()
            SignUpmessage = 'Sign Up success, wellcome to our store! Please login again!'
            return render_template('Sign_Up.html', name = username, SignUpmessage = SignUpmessage)
        except:
            db.rollback()
            SignUpmessage = 'Sign Up unsuccess, please enter the infomation again!'
            return render_template('Sign_Up.html', name = newuser, SignUpmessage = SignUpmessage)

    return render_template('Sign_Up.html', name = newuser)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user_CID = ''
        
        # find the user in the login table
        mycursor = db.cursor()
        sql = "SELECT C_ID FROM login WHERE C_Name = %s AND C_Password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        
        # If user is found
        if myresult:
            session['username'] = username
            session['user_CID'] = myresult
            message = "Sign in success! Please use home button to return to home page!"
            return render_template('Login.html', name = session['username'], SignInM = message)
        
        # If user is not found
        else:
            message = "Wrong User's name or password, please enter again."
            return render_template('Login.html', SignInM = message)

    if 'username' in session:
        return render_template('Index_Logined.html', name = session['username'])
    else:
        return render_template('Login.html', name = newuser)

@app.route('/Change_PW', methods=['GET', 'POST'])
def Change_PW():
    if request.method == 'POST':
        Old_Password = request.form['Old_password']
        New_Password = request.form['New_password']
        Confirm_Password = request.form['confirm_password']
        
        if New_Password != Confirm_Password:
            ChangePWM = 'You enter different new password, enter again'
            return render_template('Change_PW.html', name = session['username'], ChangePWM = ChangePWM)

        mycursor = db.cursor()
        sql = "SELECT C_Password FROM login WHERE C_ID = %s"
        val = (session['user_CID'])
        mycursor.execute(sql, val)
        for row in mycursor:
            OldPW = row[0]
        if Old_Password != OldPW:
            ChangePWM = 'You enter worng old password, enter again'
            return render_template('Change_PW.html', name = session['username'], ChangePWM = ChangePWM)
        else:
            sql = "UPDATE login SET C_Password = %s WHERE C_ID = %s"
            val = (New_Password, session['user_CID'])
            mycursor.execute(sql, val)
            db.commit()
            ChangePWM = 'Change password success! Please login again!'
            session.pop('username',None)
            return render_template('Change_PW.html', name = newuser, ChangePWM = ChangePWM)

    return render_template('Change_PW.html', name = session['username'])

@app.route('/Cart')
def Cart():
    mycursor = db.cursor()
    val = session['user_CID']
    sql = "SELECT SUM(Price) FROM cart WHERE C_ID = %s"
    mycursor.execute(sql, val)
    for row in mycursor:
        Cost = row[0]

    sql = "SELECT P_ID FROM cart WHERE C_ID = %s"
    mycursor.execute(sql, val)
    ProductID = []
    for row in mycursor:
        ProductID.append(row)
    
    sql = "SELECT P_Quantity,Price FROM cart WHERE C_ID = %s"
    mycursor.execute(sql, val)
    cartArray = []
    for row in mycursor:
        cartArray.append(row)

    ProductName = ['']
    for i in range(len(ProductID)):
        sql = "SELECT P_Name FROM product WHERE P_ID = %s"
        val = ProductID[i]
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        ProductName.append(myresult)
        
    
    EmptyMessage = ''
    CartTable = None
    ProductN_Table = None
    if Cost == None:
        EmptyMessage = "You have nothing in the shopping cart!"
    else:
        CartTable = tabulate(cartArray, headers = ['Quantity', 'Price(HK$)'], tablefmt='html')
        ProductN_Table = tabulate(ProductName, headers = ['Product Name'], tablefmt='html')

    return render_template('Cart.html', name = session['username'], Cost = Cost, CartTable = CartTable, ProductN_Table = ProductN_Table, Empty = EmptyMessage)

@app.route('/Clear_Cart', methods=['POST'])
def Clear_Cart():
    mycursor = db.cursor()
    sql = "DELETE FROM cart WHERE C_ID = %s"
    val = session['user_CID']
    mycursor.execute(sql, val)
    db.commit()

    return redirect('/Cart')


@app.route('/Payment', methods=['GET', 'POST'])
def Payment():
    mycursor = db.cursor()
    sql = "SELECT SUM(Price) FROM cart WHERE C_ID = %s"
    val = session['user_CID']
    lock.acquire()
    mycursor.execute(sql, val)
    lock.release()
    Total_Fee = None
    session['PM_ID'] = None
    PM_Ture = str('')
    for row in mycursor:
        Total_Fee = row[0]

    if request.method == 'POST':
        PaymentBTN = request.form['PaymentBTN']
        if Total_Fee == None and PaymentBTN == "1":
            return render_template('Total_None.html', name = session['username'])
        PM_Code_Py = request.form['PM_Code']
        if PM_Code_Py != '' and PaymentBTN == "0":
            sql = "SELECT PM_Discount_Value FROM promotion_list WHERE PM_CODE = %s"
            val = PM_Code_Py
            lock.acquire()
            mycursor.execute(sql, val)
            lock.release()
            myresult = mycursor.fetchone()
            # If promote code is found
            if myresult:
                PM_Value = myresult[0]
                Total_Fee -= PM_Value
                PM_Ture = str('Success! You get discount!')
                sql = "SELECT PM_ID FROM promotion_list WHERE PM_CODE = %s"
                val = PM_Code_Py
                lock.acquire()
                mycursor.execute(sql, val)
                lock.release()
                myresult = mycursor.fetchone()
                if myresult:
                    session['PM_ID'] = myresult
        elif PM_Code_Py == '' and PaymentBTN == "0":
            PM_Ture = str('Please enter the promotion code!')
        else:
            PM_Ture = str('')
            session['PM_ID'] = None
        if Total_Fee != 0 and PaymentBTN == "1":
            return redirect('/Complete')


    return render_template('Sell.html', name = session['username'], Payment = Total_Fee, PM_Ture = PM_Ture)

@app.route('/Complete')
def Complete():
    mycursor = db.cursor()
    Product_Num = None
    val = session['user_CID']
    sql = "SELECT COUNT(C_ID) FROM cart WHERE C_ID = %s"
    lock.acquire()
    mycursor.execute(sql, val)
    lock.release()
    myresult = mycursor.fetchone()
    Product_Num = myresult[0]
    for x in range(Product_Num):
        sql = "SELECT C_ID,P_ID,P_Quantity,Price FROM cart WHERE C_ID = %s"
        val = session['user_CID']
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        for row in mycursor:
            Cart_C_ID = row[0]
            Cart_P_ID = row[1]
            Cart_P_Quan = row[2]
            Cart_price = row[3]
        sql = "INSERT INTO order_list (C_ID, P_ID, P_Quantity, PM_ID, Price) VALUES ( %s, %s, %s, %s, %s)"
        val = (Cart_C_ID, Cart_P_ID, Cart_P_Quan, session['PM_ID'], Cart_price)
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        db.commit()
        sql = "DELETE FROM cart WHERE C_ID=%s"
        val = (Cart_C_ID)
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        db.commit()

    return render_template('Complete.html', name = session['username'])

@app.route('/OrderList')
def OrderList():
    mycursor = db.cursor()
    sql = "SELECT P_Quantity,Price,Created_At FROM order_list WHERE C_ID = %s"
    val = session['user_CID']
    mycursor.execute(sql, val)
    HISTArray = []
    row = None
    for row in mycursor:
        HISTArray.append(row)

    sql = "SELECT P_ID FROM order_list WHERE C_ID = %s"
    mycursor.execute(sql, val)
    ProductID = []
    for row in mycursor:
        ProductID.append(row)

    ProductName = ['']
    for i in range(len(ProductID)):
        sql = "SELECT P_Name FROM product WHERE P_ID = %s"
        val = ProductID[i]
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        ProductName.append(myresult)

    EmptyMessage = ''
    if row == 0:
        EmptyMessage = "You never buy a product from us!"

    ProductN_Table = tabulate(ProductName, headers = ['Product Name'], tablefmt='html')
    HISTTable = tabulate(HISTArray, headers = ['Quantity', 'Price(HK$)', 'Date'], tablefmt='html')

    return render_template('Order_List.html', name = session['username'], HISTTable = HISTTable, ProductN_Table = ProductN_Table, Empty = EmptyMessage)

@app.route('/Logout')
def Logout():
    session.pop('username',None)
    return render_template('Logout.html', name = newuser)

@app.route('/Q&A')
def QAndA():
    return render_template('Q&A.html', name = newuser)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8000)


db = pymysql.connect(host="localhost", user="newuser", password="password", database="website_db")

newuser = "New Comer"
lock = threading.Lock()

@app.route('/')
def index():
    if 'username' in session: # if user is logged in
        return render_template('Index_Logined.html', name = session['username'])
    else:   #if user is not logged in
        return render_template('Index.html', name = newuser)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Get product ID to search the product price
    P_ID = request.form['product_id']
    mycursor = db.cursor()
    sql = "SELECT P_Price FROM product WHERE P_ID = %s"
    val = (P_ID)
    mycursor.execute(sql, val)
    for row in mycursor:
        P_price = row[0]

    # Add row to the 'cart' table
    sql = "INSERT INTO cart (C_ID, P_ID, P_Quantity, Price) VALUES (%s, %s, %s, %s)"
    val = (session['user_CID'], P_ID, 1, P_price)
    mycursor.execute(sql, val)
    db.commit()
    POPUP = "The product added into your cart!"
    
    #send message to confirm
    return render_template('Index_Logined.html', POPMessage = POPUP)

@app.route('/Sign_Up', methods=['GET', 'POST'])
def SignUp():
    #Get user's name,Email, password, gender, phone number and address
    if request.method == 'POST':
        username = request.form['name']
        userEmail = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        UserPhNum = request.form['phone']
        UserAddr = request.form['address']
        SignUpmessage = ''

        try:
            valid = validate_email(userEmail)
        except ValueError as e:
            SignUpmessage = 'Unvalid Email address, please enter again.'
            return render_template('Sign_Up.html', name = newuser, SignUpmessage = SignUpmessage)

        # Add them into the 'customers' table
        mycursor = db.cursor()
        sql = "INSERT INTO customers (C_ID, C_NAME, C_Email, C_Password, gender, Phone_Num, Address) VALUES ( NULL, %s, %s, %s, %s, %s, %s)"
        val = (username, userEmail, password, gender, UserPhNum, UserAddr)
        mycursor.execute(sql, val)

        try:
            db.commit()
            sql = "INSERT INTO login (C_ID, C_NAME, C_Password) VALUES ( %s, %s, %s)"
            val = (mycursor.lastrowid, username, password)
            mycursor.execute(sql, val)
            db.commit()
            SignUpmessage = 'Sign Up success, wellcome to our store! Please login again!'
            return render_template('Sign_Up.html', name = username, SignUpmessage = SignUpmessage)
        except:
            db.rollback()
            SignUpmessage = 'Sign Up unsuccess, please enter the infomation again!'
            return render_template('Sign_Up.html', name = newuser, SignUpmessage = SignUpmessage)

    return render_template('Sign_Up.html', name = newuser)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user_CID = ''
        
        # find the user in the login table
        mycursor = db.cursor()
        sql = "SELECT C_ID FROM login WHERE C_Name = %s AND C_Password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        
        # If user is found
        if myresult:
            session['username'] = username
            session['user_CID'] = myresult
            message = "Sign in success! Please use home button to return to home page!"
            return render_template('Login.html', name = session['username'], SignInM = message)
        
        # If user is not found
        else:
            message = "Wrong User's name or password, please enter again."
            return render_template('Login.html', SignInM = message)

    if 'username' in session:
        return render_template('Index_Logined.html', name = session['username'])
    else:
        return render_template('Login.html', name = newuser)

@app.route('/Change_PW', methods=['GET', 'POST'])
def Change_PW():
    if request.method == 'POST':
        Old_Password = request.form['Old_password']
        New_Password = request.form['New_password']
        Confirm_Password = request.form['confirm_password']
        
        if New_Password != Confirm_Password:
            ChangePWM = 'You enter different new password, enter again'
            return render_template('Change_PW.html', name = session['username'], ChangePWM = ChangePWM)

        mycursor = db.cursor()
        sql = "SELECT C_Password FROM login WHERE C_ID = %s"
        val = (session['user_CID'])
        mycursor.execute(sql, val)
        for row in mycursor:
            OldPW = row[0]
        if Old_Password != OldPW:
            ChangePWM = 'You enter worng old password, enter again'
            return render_template('Change_PW.html', name = session['username'], ChangePWM = ChangePWM)
        else:
            sql = "UPDATE login SET C_Password = %s WHERE C_ID = %s"
            val = (New_Password, session['user_CID'])
            mycursor.execute(sql, val)
            db.commit()
            ChangePWM = 'Change password success! Please login again!'
            session.pop('username',None)
            return render_template('Change_PW.html', name = newuser, ChangePWM = ChangePWM)

    return render_template('Change_PW.html', name = session['username'])

@app.route('/Cart')
def Cart():
    mycursor = db.cursor()
    val = session['user_CID']
    sql = "SELECT SUM(Price) FROM cart WHERE C_ID = %s"
    mycursor.execute(sql, val)
    for row in mycursor:
        Cost = row[0]

    sql = "SELECT P_ID,P_Quantity,Price FROM cart WHERE C_ID = %s"
    mycursor.execute(sql, val)
    cartArray = []
    for row in mycursor:
        cartArray.append(row)
    
    EmptyMessage = ''
    CartTable = None
    if Cost == None:
        EmptyMessage = "You have nothing in the shopping cart!"
    else:
        CartTable = tabulate(cartArray, headers = ['Product Name', 'Quantity', 'Price(HK$)'], tablefmt='html')

    return render_template('Cart.html', name = session['username'], Cost = Cost, CartTable = CartTable, Empty = EmptyMessage)

@app.route('/Clear_Cart', methods=['POST'])
def Clear_Cart():
    mycursor = db.cursor()
    sql = "DELETE FROM cart WHERE C_ID = %s"
    val = session['user_CID']
    mycursor.execute(sql, val)
    db.commit()

    return redirect('/Cart')


@app.route('/Payment', methods=['GET', 'POST'])
def Payment():
    mycursor = db.cursor()
    sql = "SELECT SUM(Price) FROM cart WHERE C_ID = %s"
    val = session['user_CID']
    lock.acquire()
    mycursor.execute(sql, val)
    lock.release()
    Total_Fee = None
    session['PM_ID'] = None
    PM_Ture = str('')
    for row in mycursor:
        Total_Fee = row[0]

    if request.method == 'POST':
        if Total_Fee == None:
            return render_template('Total_None.html', name = session['username'])
        PM_Code_Py = request.form['PM_Code']
        if PM_Code_Py != '':
            sql = "SELECT PM_Discount_Value FROM promotion_list WHERE PM_CODE = %s"
            val = PM_Code_Py
            lock.acquire()
            mycursor.execute(sql, val)
            lock.release()
            myresult = mycursor.fetchone()
            # If promote code is found
            if myresult:
                PM_Value = myresult[0]
                Total_Fee -= PM_Value
                PM_Ture = str('Success! You get discount!')
                sql = "SELECT PM_ID FROM promotion_list WHERE PM_CODE = %s"
                val = PM_Code_Py
                lock.acquire()
                mycursor.execute(sql, val)
                lock.release()
                myresult = mycursor.fetchone()
                if myresult:
                    session['PM_ID'] = myresult
        else:
            PM_Ture = str('')
            session['PM_ID'] = None


    return render_template('Sell.html', name = session['username'], Payment = Total_Fee, PM_Ture = PM_Ture)

@app.route('/Complete')
def Complete():
    mycursor = db.cursor()
    Product_Num = None
    val = session['user_CID']
    sql = "SELECT COUNT(C_ID) FROM cart WHERE C_ID = %s"
    lock.acquire()
    mycursor.execute(sql, val)
    lock.release()
    myresult = mycursor.fetchone()
    Product_Num = myresult[0]
    for x in range(Product_Num):
        sql = "SELECT C_ID,P_ID,P_Quantity,Price FROM cart WHERE C_ID = %s"
        val = session['user_CID']
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        for row in mycursor:
            Cart_C_ID = row[0]
            Cart_P_ID = row[1]
            Cart_P_Quan = row[2]
            Cart_price = row[3]
        sql = "INSERT INTO order_list (C_ID, P_ID, P_Quantity, PM_ID, Price) VALUES ( %s, %s, %s, %s, %s)"
        val = (Cart_C_ID, Cart_P_ID, Cart_P_Quan, session['PM_ID'], Cart_price)
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        db.commit()
        sql = "DELETE FROM cart WHERE C_ID=%s"
        val = (Cart_C_ID)
        lock.acquire()
        mycursor.execute(sql, val)
        lock.release()
        db.commit()

    return render_template('Complete.html', name = session['username'])

@app.route('/OrderList')
def OrderList():
    mycursor = db.cursor()
    sql = "SELECT P_ID,P_Quantity,Price,Created_At FROM order_list WHERE C_ID = %s"
    val = session['user_CID']
    mycursor.execute(sql, val)
    HISTArray = []
    row = None
    for row in mycursor:
        HISTArray.append(row)

    EmptyMessage = ''
    if row == 0:
        EmptyMessage = "You never buy a product from us!"

    HISTTable = tabulate(HISTArray, headers = ['Product Name', 'Quantity', 'Price(HK$)', 'Date'], tablefmt='html')

    return render_template('Order_List.html', name = session['username'], HISTTable = HISTTable, Empty = EmptyMessage)

@app.route('/Logout')
def Logout():
    session.pop('username',None)
    return render_template('Logout.html', name = newuser)

@app.route('/Q&A')
def QAndA():
    return render_template('Q&A.html', name = newuser)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
