from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB config (داکر کانتینر MongoDB)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/phonebook"
mongo = PyMongo(app)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user:
            return "User already exists. Go to login."

        hashpass = generate_password_hash(request.form['password'])
        users.insert_one({
            'name': request.form['name'],
            'email': request.form['email'],
            'password': hashpass
        })
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'email': request.form['email']})

        if user and check_password_hash(user['password'], request.form['password']):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return redirect('/dashboard')
        return "Invalid credentials"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# ---------------- API ----------------

@app.route('/api/contacts', methods=['GET', 'POST'])
def contacts():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    contacts_collection = mongo.db.contacts

    if request.method == 'POST':
        data = request.get_json()
        contacts_collection.insert_one({
            'user_id': session['user_id'],
            'name': data['name'],
            'phone': data['phone']
        })
        return jsonify({'message': 'Contact added'}), 201

    else:  # GET
        contacts = list(contacts_collection.find({'user_id': session['user_id']}).sort('name' , 1))
        for c in contacts:
            c['_id'] = str(c['_id'])  # تبدیل ObjectId به str برای ارسال به فرانت
        return jsonify(contacts)


@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    result = mongo.db.contacts.delete_one({
        '_id': ObjectId(contact_id),
        'user_id': session['user_id']
    })

    if result.deleted_count == 1:
        return jsonify({'message': 'Deleted'})
    else:
        return jsonify({'error': 'Not found'}), 404
    
@app.route('/health')
def health():
    return "OK", 200

    
# ---------------- MAIN ----------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
