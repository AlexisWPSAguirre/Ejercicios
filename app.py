from flask import Flask, render_template, request, redirect, url_for
 #Llos template de html para trabajarlos en python con flask
#/El objeto rquest Accede al metodo que se esta enviando 
# 
import sqlite3 #librería de python para conectar a un db
app = Flask(__name__)  #Instancia 
db = sqlite3.connect('data.db', check_same_thread=False) #Para que ejecutarse en el mismo hilo

@app.route('/') #/ Significa ruta raíz  @Decorador, para indicar a flask que URL debe activar
 #/Las rutas se habilitan por defecto en metodo GET, para poder usar POST se debe especificar 
def inicio():
    return render_template('index.html')

@app.route('/saludo/<nombre>/<int:edad>')#Una variable de la ruta, para numerico se especifica con int:
def saludar(nombre,edad): #Se recupera el nombre en el parametro del def
    return render_template('saludo.html', name = nombre, age = edad) #Sistema clave y valor, enviando parametros al template de html

@app.route('/contacto', methods=['GET', 'POST'])#Una variable de la ruta, para numerico se especifica con int:
def contacto(): #Se recupera el nombre en el parametro del def
    #Obteniendo información
    if request.method == 'GET':
        return render_template('contacto.html') #Sistema clave y valor, enviando parametros al template de html
    elif request.method == 'POST':
        nombres = request.form.get('nombres')
        correo = request.form.get('correo')
        celular = request.form.get('celular')
        observacion = request.form.get('observacion')
        return 'Guardando información ' + nombres + correo + celular + observacion #Guardando información de formulario


@app.route('/usuarios', )
def usuarios(): #Se trabaja la consulta a base de datos en esta función
    usuarios = db.execute('select * from CRUD') #Consulta
    usuarios = usuarios.fetchall()       #Metodo fetchall 
    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    correos = request.form.get('email')
    passwords = request.form.get('password')
    cursor = db.cursor()#Permite ejecutar consultas de tipo insert update o delete
    cursor.execute(""" insert into CRUD(
        nombres,
        apellidos,
        email,
        password    
        ) values (?,?,?,?)
    """,(nombres,apellidos,correos,passwords)) 
    db.commit() #Al igual que en gift, confirma que los cambios sean guardados
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['GET','POST'])
def editar_usuarios(id):
    if request.method == 'GET':
        usuario = db.execute("""SELECT * FROM CRUD WHERE id=? """,(str(id),)).fetchone()
        return render_template('usuarios/editar.html',usuario=usuario)
    nw_nombres = request.form.get('nombres')
    nw_apellidos = request.form.get('apellidos')
    nw_correos = request.form.get('email')
    nw_passwords = request.form.get('password')
    cursor = db.cursor()
    cursor.execute("""
    UPDATE CRUD 
    SET nombres = ?, 
    apellidos = ?, 
    email = ?, 
    password = ? 
    WHERE id = ?
     """,(nw_nombres,nw_apellidos,nw_correos,nw_passwords,id))
    db.commit()
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>', methods=['GET','POST'])
def eliminar_usuarios(id):
    print(id)   
    cursor = db.cursor()
    cursor.execute("""
    DELETE FROM CRUD 
    WHERE id = ?
    """,(id,))
    db.commit()
    return redirect(url_for('usuarios'))
app.run(debug=True) #Parametro Debug para reiniciar el server  uff