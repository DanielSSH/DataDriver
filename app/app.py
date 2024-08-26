from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'Local instance MySQL80'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Zonapets12345*'
app.config['MYSQL_DB'] = 'datadriverdb'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.before_request
def before_request():
    print("Antes de la petición...")

@app.after_request
def after_request(response):
    print("Después de la petición...")
    return response

@app.route('/')
def index():
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data = {
        'titulo': 'DATA DRIVER',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_conductores': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

@app.route('/conductores')
def listar_conductores():
    data = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT Cedula, Nombres, Apellidos, Licencia FROM conductores"
        cursor.execute(sql)
        conductores = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data['conductores'] = [dict(zip(columns, row)) for row in conductores]
        data['conductores'] = conductores
        data['mensaje'] = 'Éxito'
        cursor.close()
    except Exception as ex:
        print(f"Error: {ex}")  # Imprime el error para ayudar en la depuración
        data['mensaje'] = 'Error'
    return jsonify(data)

@app.route('/query_string')
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"

def pagina_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
