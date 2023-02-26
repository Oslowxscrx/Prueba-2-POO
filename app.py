from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

app = Flask(__name__)
key = Fernet.generate_key()

host = 'localhost'
port = 5432
dbname = 'PRUEBA2_ON'
user = 'postgres'
password = 1234


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM gato_on')
    users = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    raza = new_user['raza']
    edad = new_user['edad']
    nombre = new_user['nombre']
    duenio = new_user['duenio']
    direccion = new_user['direccion']
    numero = new_user['numero']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO gato_on (raza, edad, nombre, duenio, direccion, numero) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *',
                (raza, edad, nombre, duenio, direccion, numero  ))
    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM gato_on WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()

    conn.commit()

    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(user)


@app.put('/api/users/<id>')
def update_users(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user = request.get_json()
    raza = new_user['raza']
    edad = new_user['edad']
    nombre = new_user['nombre']
    duenio = new_user['duenio']
    direccion = new_user['direccion']
    numero = new_user['numero']

    cur.execute(
        'UPDATE gato_on SET raza = %s, edad = %s, nombre = %s, duenio = %s, direccion = %s, numero = %s WHERE id = %s RETURNING *', (raza, edad, nombre, duenio, direccion, numero, id))
    update_user = cur.fetchone()
    
    conn.commit()
    
    conn.close()
    cur.close()
    
    if update_user is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(update_user)


@app.get('/api/users/<id>')
def get_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM gato_on WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User Not Found'}), 404

    print(user)

    return jsonify(user)

@app.get('/')
def home():
    return send_file('static/index.html')
    

if __name__ == '__main__':
    app.run(debug=True)