##     INTEGRANTES:        ##
##  MAICOL JOSSA CAMPAÑA   ##
##  MIGUEL FAJARDO         ##
#############################

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'spbYO0JJOPUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
db = sqlite3.connect('data.db', check_same_thread=False)
def base():
    global categories
    categories=db.execute("""select * from Categorias where ID_USUARIO = ?""",(session['Usuarios'][0],)).fetchall()
  
#-------------------------------------------------------------------------principal
@app.route('/', methods=['GET','POST'])
def inicio_2():
    if request.method == 'GET':
        return render_template('paginas/inicio_2.html')

    Correo=request.form.get('i_correo')
    Contraseña=request.form.get('i_contraseña')
    
    cursor=db.cursor()
    
    Usuarios = cursor.execute("""select * from Usuarios where
    Email = ? and Contraseña = ?""", (Correo,Contraseña,)).fetchone()
    
    db.commit()
    
    if  Usuarios is None:
        flash('Las Credenciales No Son Validas.','error')
        return redirect(request.url)
    
    session['Usuarios'] = Usuarios
    print(session['Usuarios'])
    
    return redirect(url_for('inicio'))

#------------- finalizar sesion
@app.route('/Logout')
def Logout():
    session.clear()
    return redirect(url_for('inicio_2'))

#------------menu
@app.route('/Inicio')
def inicio():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    return render_template('paginas/inicio.html')

#listado de productos 
@app.route('/Productos')
def productos():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    productos = db.execute('select * from Productos')
    productos = productos.fetchall()
    return render_template('paginas/productos.html', productos=productos)

#creando producto 
@app.route('/Crear Producto', methods=['GET','POST'])
def crear_prod():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        base()
        return render_template('paginas/crear_prod.html', Categorias=categories)
    
    Nombre=request.form.get('Nombre')
    Precio=request.form.get('Precio')
    Categoria=request.form.get('Categoria')
    
    cursor=db.cursor()
    
    cursor.execute("""insert into Productos (
            Nombre, 
            Precio,
            Categoria,
            ID_USUARIO
        )values (?,?,?,?)
    """, (Nombre,Precio,Categoria,session['Usuarios'][0],))
    
    db.commit()
    
    return redirect(url_for('productos'))

#eliminar prodcutos 
@app.route('/Eliminar Producto', methods=['GET','POST'])
def eliminar_prod():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        return render_template('paginas/eliminar_prod.html')
    
    ID=request.form.get('EIDP')
    cursor = db.cursor()
    cursor.execute("""delete from Productos where ID = ?""",(ID))
    
    db.commit()
    
    return redirect(url_for('productos'))

#editar producto
@app.route('/Editar Producto', methods=['GET','POST'])
def editar_prod():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        base()
        return render_template('paginas/editar_prod.html', Categorias=categories )
    
    ID=request.form.get('e_id')
    Nombre=request.form.get('e_nombre')
    Precio=request.form.get('e_precio')
    Categoria=request.form.get('e_categoria')
    
    cursor = db.cursor()
    cursor.execute("""update Productos set
                Nombre=?,
                Precio=?, 
                Categoria=?
                WHERE ID=?
    """,(Nombre,Precio,Categoria,ID))
    
    db.commit()
    
    return redirect(url_for('productos'))

#listado de usuarios
@app.route('/Usuarios')
def usuarios():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    usuarios = db.execute('select * from Usuarios')
    usuarios = usuarios.fetchall()
    return render_template('paginas/usuarios.html', usuarios=usuarios)

#creando usuarios
@app.route('/Crear Usuario', methods=['GET','POST'])
def registrarse():
    if request.method == 'GET':
        return render_template('paginas/crear_usua.html')

    Nombre=request.form.get('C_usuario')
    Email=request.form.get('C_correo')
    Contraseña=request.form.get('C_contraseña')

    #validando correo,nombre
    if (Nombre==""):
        flash('El campo nombre es requerido','error')
        return redirect(url_for('inicio_2'))

    Usuario = db.execute('select * from Usuarios where  Email= "'+ Email+'"').fetchall()
    if (len(Usuario)>0):
        flash('Ya existe un usuario con este E-mail','error')
        return redirect(url_for('inicio_2'))

    try:
        cursor=db.cursor()
        cursor.execute("""insert into Usuarios (
                Nombre, 
                Email,
                Contraseña
            )values (?,?,?)
         """, (Nombre,Email,Contraseña,))
    
        db.commit()
    except:
        flash('No se ha podido guardar el usuario', 'error')
        return redirect(url_for('inicio_2'))
    
    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('inicio_2'))

#eliminar usuarios
@app.route('/Eliminar Usuarios', methods=['GET','POST'])
def eliminar_usua():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        return render_template('paginas/eliminar_usua.html')
    
    DNombre=request.form.get('DNombre')
    cursor = db.cursor()
    cursor.execute("""delete from Usuarios where ID = ?""",(DNombre,))
    
    db.commit()
    
    return redirect(url_for('usuarios'))    

#editar usuario
@app.route('/Editar usuario', methods=['GET','POST'])
def editar_usua():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        return render_template('paginas/editar_usua.html')

    ID=request.form.get('IdP')
    Nombre=request.form.get('EditarNombreP')
    Correo=request.form.get('EditarCorreoP')
    Contraseña=request.form.get('EditarContraseñaP')

    try:
        cursor = db.cursor()
        cursor.execute("""update Usuarios set
                Nombre=?,
                Email=?, 
                Contraseña=?
                WHERE ID=?
        """,(Nombre,Correo,Contraseña,ID))
        db.commit()

    except:
        flash('No se ha podido guardar el usuario', 'error')
        return redirect(url_for('Usuarios'))

    flash('Usuario editado correctamente', 'success')
    
    
    return redirect(url_for('usuarios'))


#listado de categorias
@app.route('/Categorias')
def categorias():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    categorias = db.execute('select * from Categorias')
    categorias = categorias.fetchall()
    return render_template('paginas/categorias.html', categorias = categorias)

#creando categorias
@app.route('/Crear Categoria', methods=['GET','POST'])
def crear_cat():
    if request.method == 'GET':
        return render_template('paginas/crear_cat.html')
    
    Categoria=request.form.get('NuevaCategoria')
    cursor=db.cursor()
    
    cursor.execute("""insert into Categorias (
            Categoria,
            ID_USUARIO
        )values (?,?)
    """, (Categoria,session['Usuarios'][0],))
    
    db.commit()
    
    return redirect(url_for('categorias'))

#eliminar categoria
@app.route('/Eliminar Categoria', methods=['GET','POST'])
def eliminar_cat():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        return render_template('paginas/eliminar_cat.html')
    
    Categoria=request.form.get('EIDC')
    cursor = db.cursor()
    cursor.execute("""delete from Categorias where ID = ?""",(Categoria))
    
    db.commit()
    
    return redirect(url_for('categorias'))  

#editar categoria 
@app.route('/Editar Categoria', methods=['GET','POST'])
def editar_cat():
    if not 'Usuarios' in session:
        return redirect(url_for('inicio_2'))
    
    if request.method == 'GET':
        return render_template('paginas/editar_cat.html')
    
    ID=request.form.get('IDC')
    Nombre=request.form.get('EditarNombreC')
    
    cursor = db.cursor()
    cursor.execute("""update Categorias set
                Categoria=?
                WHERE ID=?
    """,(Nombre,ID))
    
    db.commit()
    
    return redirect(url_for('categorias'))

app.run(debug=True)


