from flask import Flask, request, jsonify, render_template, redirect,  session
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'pushkar' 
CORS(app)  


cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="pushkar")

cur = cnx.cursor(dictionary=True)

@app.route("/")
def home():
    if session.get("email"):
        return render_template("projectAlpha_home.html" , email = session.get("email")) 
    return render_template("projectAlpha_home.html" , email = None)
 
 
@app.route("/credit")
def credit():
    
    return render_template("credit.html") 

@app.route("/loginuser")
def loginuser():
    if session.get("email"):
        
        return redirect("/")
    return render_template("login.html")

@app.route("/playgame1")
def playgame1():
    if session.get("email"):
         
          return render_template("game1.html")
      
    return redirect("/loginuser")

@app.route("/game1intro")
def Game1():
    if session.get("email"):
         
          return render_template("game1_intro.html")
      
    return redirect("/loginuser")


@app.route("/playgame2")
def playgame2():
    if session.get("email"):
         
          return render_template("game2.html")
      
    return redirect("/loginuser")

@app.route("/game2")
def Game2():
    if session.get("email"):
         
          return render_template("game2_introPage.html")
      
    return redirect("/loginuser")


@app.route("/playgame3")
def playgame3():
    if session.get("email"):
         
          return render_template("game3.html")
      
    return redirect("/loginuser")

@app.route("/game3")
def Game3():
    if session.get("email"):
         
          return render_template("game3_intro.html")
      
    return redirect("/loginuser")

@app.route("/finalreport")
def finalreport():
    if session.get("email"):
         
          return render_template("report.html")
      
    return redirect("/loginuser")

@app.route("/registeruser")
def register_file():
    if session.get("email"):
       
        return redirect("/")
    return render_template("signup.html")

@app.route('/register', methods=['POST'])
def register():
    
    if session.get("email"):
       
        return jsonify({ "message" : "Already logged in!" }) , 400
    
    content = request.json
    email = content['email']  
    password = content['password']

    # Check if user already exists
    check_query = "SELECT * FROM users WHERE email = %s"
    cur.execute(check_query, (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    cur.execute(query, (email, password))

    user_id = cur.lastrowid


    query2 = "INSERT INTO gamestate (stage, stateid) VALUES (%s, %s)"
    cur.execute(query2, (0, user_id)) 
    
    cnx.commit()
    
    return jsonify({"message": "Registration successful"}), 201


@app.route('/login', methods=['POST'])
def login():
    
    if session.get("email"):
       
        return jsonify({ "message" : "Already logged in!" }) , 400
  
    content = request.json
    email = content['email']
    password = content['password']

    # Check if user exists
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query, (email,))
    user = cur.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Directly compare passwords
    if user['password'] == password:
        session['email'] = user['email']
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Incorrect password"}), 401


@app.route('/logout')
def logout():
    
    session.pop('email', None)
    return redirect("/")


@app.route("/home")
def home_render():
    return render_template("projectAlpha_home.html")

if __name__ == '__main__':
    app.run(debug=True)
    