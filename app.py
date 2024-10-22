from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Iniciamos la sesión con una lista vacía si no existe
@app.before_request
def init_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

# Ruta principal con el formulario de registro
@app.route('/', methods=['GET', 'POST'])
def registro_seminarios():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Creamos un nuevo inscrito
        nuevo_inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': ', '.join(seminarios)
        }

        # Guardamos en la sesión
        session['inscritos'].append(nuevo_inscrito)
        session.modified = True
        return redirect(url_for('listado_inscritos'))
    
    return render_template('registro_seminarios.html')

# Ruta para listar inscritos
@app.route('/inscritos')
def listado_inscritos():
    return render_template('listado_inscritos.html', inscritos=session['inscritos'])

# Ruta para eliminar un inscrito
@app.route('/eliminar/<int:index>', methods=['POST'])
def eliminar_inscrito(index):
    session['inscritos'].pop(index)
    session.modified = True
    return redirect(url_for('listado_inscritos'))

# Ruta para editar un inscrito (opcional)
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar_inscrito(index):
    if request.method == 'POST':
        session['inscritos'][index] = {
            'fecha': request.form['fecha'],
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'turno': request.form['turno'],
            'seminarios': ', '.join(request.form.getlist('seminarios'))
        }
        session.modified = True
        return redirect(url_for('listado_inscritos'))

    inscrito = session['inscritos'][index]
    return render_template('editar_inscrito.html', inscrito=inscrito, index=index)

if __name__ == "__main__":
    app.run(debug=True)
