from flask import Flask,render_template,request,Response,url_for
import pymysql
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db_config = {
    'host' : 'localhost',
    'database' : 'bookstore',
    'password' : 'root',
    'user' : 'root'
}
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("home.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/adminlogin1")
def adimlogin1():
    return render_template("admin_login.html")
@app.route("/adminlogin2",methods=["POST","GET"])
def adminlogin2():
    username = request.form["username"]
    password = request.form["password"]
    if (username == "admin"):
        if (password == "admin"):
            return render_template("admin_dashboard.html")
        else:
            return render_template("errorpage.html",message="Invalid Password !")
    else:
        return render_template("errorpage.html",message = "Invalid Username !")
@app.route("/admin_addproducts1")
def admin_addproducts1():
    return render_template("admin_addproducts.html")

@app.route("/add_products",methods=["POST","GET"])
def add_products():
    pname = request.form["product_name"]
    pimage = request.files["product_image"]
    pgenere = request.form["product_genre"]
    paprice = request.form["actual_price"]
    pdprice = request.form["discounted_price"]
    pquantity = request.form["quantity"]
    pimage = pimage.read()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO PRODUCTS (PNAME,PIMAGE,PGENERE,PAPRICE,PDPRICE,PQUANTITY) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(pname,pimage,pgenere,paprice,pdprice,pquantity))
    conn.commit()

    return render_template("admin_dashboard.html",data="YES")

@app.route("/admin_manageproducts1")
def admin_manageproducts1():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    x = cursor.fetchall()

    data = []
    for value in x:
        k = list(value)
        k[2] = url_for('product_image',product_id = k[0])
        data.append(k)
    
    return render_template("admin_manageproducts.html",details=data)
@app.route("/product_image/<int:product_id>")
def product_image(product_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PIMAGE FROM PRODUCTS WHERE PID = %s"
    cursor.execute(query,(product_id))
    x = cursor.fetchone()
    return Response(x,mimetype='image/png')
@app.route("/admin_deleteproduct/<int:product_id>")
def admin_deleteproduct(product_id):
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM PRODUCTS WHERE PID = %s"
    cursor.execute(query,(product_id))
    conn.commit()


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    x = cursor.fetchall()

    data = []
    for value in x:
        k = list(value)
        k[2] = url_for('product_image',product_id = k[0])
        data.append(k)
    return render_template("admin_manageproducts.html",details=data)
@app.route("/user_signup1")
def user_signup1():
    return render_template("user_signup.html")
@app.route("/user_signup2",methods=["POST","GET"])
def user_signup2():
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    upassword = request.form["password"]
    cpassword = request.form["cpassword"]

    if upassword != cpassword:
        return render_template("errorpage.html",message="Password Does not Match !")
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_EMAIL = %s"
    cursor.execute(query,(email))
    x = cursor.fetchone()

    if x == None:
        otp = random.randint(1111,9999)

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        username = " "
        password = " "

        from_email = "sample@codegnan.com"
        to_email = email
        subject = "Your OTP for Bookstore Account Verification"
        body = f'''
Dear {email},\n
Thank you for registering with Bookstore Name! We are excited to have you as a part of our community.\n
To complete your registration and verify your identity, please use the following One-Time Password (OTP): {otp}\n
If you did not request this OTP or believe it was sent in error, please ignore this email. Your account remains secure.\n
Thank you for choosing Bookstore !\n
Note: If you need any assistance, feel free to reach out to our support team at support@gmail.com.\n\n\n
Best regards,\n
The Book store Team\n
+91 9988998899\n
support@gmail.com
        '''

        msg = MIMEMultipart()
        msg["To"] = to_email
        msg["From"] = from_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(username,password)
        server.send_message(msg)
        server.quit()

        return render_template("otpverify.html",name=name,email=email,mobile=mobile,password=upassword,otp=otp)
    else:
        return render_template("errorpage.html",message="Email already Exists !")
@app.route("/user_signup3",methods=["POST","GET"])
def user_signup3():
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    
    if otp == cotp:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO USERS (USER_NAME,USER_EMAIL,USER_MOBILE,USER_PASSWORD) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(name,email,mobile,password))
        conn.commit()
        return render_template("user_login.html")
    else:
        return render_template("errorpage.html",message="Invalid OTP")
@app.route("/user_login1")
def user_login1():
    return render_template("user_login.html")
@app.route("/user_login2",methods=["POST","GET"])
def user_login2():
    email = request.form["email"]
    password = request.form["password"]


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_EMAIL = %s"
    cursor.execute(query,(email))
    x = cursor.fetchone()
    
    if x == None:
        return render_template("errorpage.html",message="No User Exist !")
    if x[4] == password:
        conn= pymysql.connect(**db_config)
        cursor=conn.cursor()
        query="SELECT * FROM PRODUCTS"
        cursor.execute(query,)
        y=cursor.fetchall()

        products = []
        for item in y:
            data =list(item)
            data[2]=url_for('product_image',product_id=data[0])
            if data[-1] > 0:
                products.append(data)
        
        return render_template("user_home.html",user_id=x[0],products=products)
    
    else:
        return render_template("errorpage.html",message="Invalid Password")

@app.route("/add_to_cart/<int:productid>/<int:userid>")
def add_to_cart(productid,userid):
    

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USER_ID = %s AND PRODUCT_ID = %s"
    cursor.execute(query,(userid,productid))
    x = cursor.fetchone()
    if x == None:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO CART VALUES (%s,%s,%s)"
        cursor.execute(query,(userid,productid,1))
        conn.commit()
    else:
        x = list(x)
        x[2] += 1

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET QUANTITY = %s WHERE USER_ID=%s AND PRODUCT_ID = %s"
        cursor.execute(query,(x[2],x[0],x[1]))
        conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PQUANTITY FROM PRODUCTS WHERE PID = %s"
    cursor.execute(query,(productid))
    qty = cursor.fetchone()
    
    qty = int(qty[0])

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE PRODUCTS SET PQUANTITY = %s WHERE PID=%s"
    cursor.execute(query,(qty-1,productid))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    y = cursor.fetchall()

    products = []
    for item in y:
        data = list(item)
        data[2] = url_for('product_image',product_id = data[0])
        if data[-1] > 0:
            products.append(data)

    return render_template("user_home.html",user_id=userid,products = products,msg = "YES")


@app.route("/shopping_cart/<int:userid>")
def shopping_cart(userid):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PRODUCT_ID,QUANTITY FROM CART WHERE USER_ID = %s"
    cursor.execute(query,(userid))
    data1 = cursor.fetchall()

    data2 = list(data1)
    final_data = []
    for item in data2:
        sample = []
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT PID,PNAME,PIMAGE,PDPRICE FROM PRODUCTS WHERE PID = %s"
        cursor.execute(query,(item[0]))
        data3 = cursor.fetchone()
        data3 = list(data3)
        data3[2] = url_for('product_image',product_id = data3[0])
        sample.append(data3)
        sample.append(item[1])
        final_data.append(sample)
    total = 0
    for item in final_data:
        total = total + item[0][3] * item[1]
    
    return render_template("shopping_cart.html",data = final_data,user_id = userid ,total = total)

@app.route("/delete_cart_item/<int:productid>/<int:userid>/<int:qty>")
def delete_cart_item(productid,userid,qty):
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE USER_ID = %s AND PRODUCT_ID = %s"
    cursor.execute(query,(userid,productid))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PQUANTITY FROM PRODUCTS WHERE PID = %s"
    cursor.execute(query,(productid))
    x = cursor.fetchone()


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE PRODUCTS SET PQUANTITY = %s WHERE PID = %s"
    cursor.execute(query,(int(x[0])+int(qty),productid))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PRODUCT_ID,QUANTITY FROM CART WHERE USER_ID = %s"
    cursor.execute(query,(userid))
    data1 = cursor.fetchall()

    data2 = list(data1)
    final_data = []
    for item in data2:
        sample = []
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT PID,PNAME,PIMAGE,PDPRICE FROM PRODUCTS WHERE PID = %s"
        cursor.execute(query,(item[0]))
        data3 = cursor.fetchone()
        data3 = list(data3)
        data3[2] = url_for('product_image',product_id = data3[0])
        sample.append(data3)
        sample.append(item[1])
        final_data.append(sample)
    total = 0
    for item in final_data:
        total = total + item[0][3] * item[1]
    
    return render_template("shopping_cart.html",data = final_data,user_id = userid ,total = total)

@app.route("/user_login_updated/<int:userid>")
def user_login_updated(userid):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    y = cursor.fetchall()

    products = []
    for item in y:
        data = list(item)
        data[2] = url_for('product_image',product_id = data[0])
        if data[-1] > 0:
            products.append(data)
    return render_template("user_home.html",user_id=userid,products = products)
@app.route("/sucess",methods=["POST","GET"])
def sucess():
    user_id = request.form["userid"]
    payment_id = request.form["razorpay_payment_id"]
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS SELECT * FROM CART WHERE USER_ID = %s"
    cursor.execute(query,(user_id))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE USER_ID = %s"
    cursor.execute(query,(user_id))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    y = cursor.fetchall()

    products = []
    for item in y:
        data = list(item)
        data[2] = url_for('product_image',product_id = data[0])
        if data[-1] > 0:
            products.append(data)
      
    return render_template("user_home.html",user_id=user_id,products = products)
@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/forgot_password1",methods=["POST","GET"])
def forgot_password1():
    email = request.form["email"]
  

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_EMAIL = %s"
    cursor.execute(query,(email))
    x = cursor.fetchone()
   
    if x is None:
        return render_template("errorpage.html",message="No email Exist !")
    else:
        otp = random.randint(1111,9999)

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        username = " "
        password = " "


        from_email = "sample@codegnan.com"
        to_email = email
        subject = "Your OTP for Bookstore Password Reset Verification"
        body = f'''
Dear {email},\n
Thank you for registering with Bookstore Name! We are excited to have you as a part of our community.\n
To complete your registration and verify your identity, please use the following One-Time Password (OTP): {otp}\n
If you did not request this OTP or believe it was sent in error, please ignore this email. Your account remains secure.\n
Thank you for choosing Bookstore !\n
Note: If you need any assistance, feel free to reach out to our support team at support@gmail.com.\n\n\n
Best regards,\n
The Book store Team\n
+91 9988998899\n
support@gmail.com
        '''

        msg = MIMEMultipart()
        msg["To"] = to_email
        msg["From"] = from_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(username,password)
        server.send_message(msg)
        server.quit()
        return render_template("forgot_password1.html",email=email,otp=otp)
    
@app.route("/forgot_password3",methods=["POST","GET"])
def forgot_password3():
    email = request.form["email"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    if otp == cotp:
        return render_template("forgot_password2.html",email=email)
    else:
        return render_template("errorpage.html",message="Invlaid OTP")
    
@app.route("/forgot_password4",methods=["POST","GET"])
def forgot_pasword4():
    email = request.form["email"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    if password == cpassword:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query  = "UPDATE USERS SET USER_PASSWORD = %s WHERE USER_EMAIL = %s"
        cursor.execute(query,(password,email))
        conn.commit()
        return render_template("user_login.html")
    else:
        return render_template("errorpage.html",message="Passwords are not same")
    
@app.route("/update_user/<int:user_id>")
def update_user(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_ID = %s"
    cursor.execute(query,(user_id))
    data = cursor.fetchone()
    
    return render_template("update_user.html",user_id=data[0],user_name=data[1],user_mobile=data[3]) 
@app.route("/update_user1",methods=["POST","GET"])
def update_user1():
    user_id = request.form["user_id"]
    user_name = request.form["name"]
    user_mobile = request.form["mobile"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE USERS SET USER_NAME = %s WHERE USER_ID = %s"
    cursor.execute(query,(user_name,user_id))
    conn.commit()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE USERS SET USER_MOBILE = %s WHERE USER_ID = %s"
    cursor.execute(query,(user_mobile,user_id))
    conn.commit()
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_ID = %s"
    cursor.execute(query,(user_id))
    x = cursor.fetchone()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query,)
    y = cursor.fetchall()

    products = []
    for item in y:
        data = list(item)
        data[2] = url_for('product_image',product_id = data[0])
        if data[-1] > 0:
            products.append(data)
    return render_template("user_home.html",user_id=x[0],products = products)

@app.route("/user_orders1/<int:user_id>")
def user_orders(user_id):

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ORDERS WHERE USER_ID = %s"
    cursor.execute(query,(user_id))
    data = cursor.fetchall()
   

    data1 = []
    for item in data:
        qty = item[-1]

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM PRODUCTS WHERE PID = %s"
        cursor.execute(query,(item[1]))
        x = cursor.fetchone()
      
        genere = x[-4]
        image = url_for('product_image',product_id = item[1])
        name = x[1]
        data1.append([image,name,genere,qty])
 
    return render_template("user_orders.html",details=data1)

if __name__ == "__main__":
    app.run(port=5078)
 