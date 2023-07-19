# Api Rest Python App
# Libraries / Bibliotecas
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
#...

# Start App
app = Flask(__name__, static_url_path='/path/to/static')

# Configure Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'register_dm'
# File photo DataBase
app.config['UPLOAD_FOLDER'] = '/static/image/uploads'
# charge images
upload_dir = os.path.join(app.static_folder, app.config['UPLOAD_FOLDER'])
os.makedirs(upload_dir, exist_ok=True)
#App MySQL
mysql = MySQL(app)
# Set secret key
app.secret_key = 'mysecretkey'

#Star Routes Projects
# Route: Home
@app.route('/')
def Index():
    return render_template('index.html')
#...

# Route: Register Drone
@app.route('/int_drone')
def int_drone():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM drones')
    data = cur.fetchall()
    return render_template('int_drone.html', drones=data)

@app.route('/register_drone', methods=['POST'])
def register_drone():
    if request.method == 'POST':
        serial_number = request.form['serial_number']
        model = request.form['model']
        weight_limit = request.form['weight_limit']
        battery_capacity = request.form['battery_capacity']
        state = request.form['state']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO drones (serial_number, model, weight_limit, battery_capacity, state) VALUES (%s, %s, %s, %s, %s)',
                    (serial_number, model, weight_limit, battery_capacity, state))
        mysql.connection.commit()
        flash('Drone registered successfully')
        return redirect(url_for('int_drone'))
# Edit Drone
@app.route('/edit_drone/<id>')
def get_drone(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM drones WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_drone.html', drones=data[0])

@app.route('/drone/update_drone/<id>', methods=['POST'])
def update_drone(id):
    if request.method == 'POST':
        serial_number = request.form['serial_number']
        model = request.form['model']
        weight_limit = request.form['weight_limit']
        battery_capacity = request.form['battery_capacity']
        state = request.form['state']

        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE drones
                    SET serial_number = %s,
                        model = %s,
                        weight_limit = %s,
                        battery_capacity = %s,
                        state = %s
                    WHERE id = %s
                    """, (serial_number, model, weight_limit, battery_capacity, state, id))
        mysql.connection.commit()
        flash('Drone updated successfully')
        return redirect(url_for('int_drone'))
# Delete Drone
@app.route('/drone/delete_drone/<string:id>')
def delete_drone(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM drones WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Drone deleted successfully')
    return redirect(url_for('int_drone'))
#...

#==========
# Route: Register Medication
@app.route('/int_medication')
def int_medication():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medications')
    data = cur.fetchall()
    return render_template('int_medication.html', medications=data)

@app.route('/register_medication', methods=['POST'])
def register_medication():
    if request.method == 'POST':
        print('Form full')
        name = request.form['name']
        weight = request.form['weight']
        code = request.form['code']
        image_path = request.files['image_path']

        if image_path.filename != '':
            filename = secure_filename(image_path.filename)
            image_path.save(os.path.join(app.root_path, 'static', 'image', 'uploads', filename))
        else:
            filename = None

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO medications (name, weight, code, image_path) VALUES (%s, %s, %s, %s)',
                    (name, weight, code, filename))
        mysql.connection.commit()
        flash('Medication registered successfully')
        return redirect(url_for('int_medication'))
#...

# Edit Medications
@app.route('/edit_medication/<id>')
def get_medication(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medications WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_medication.html', medications=data[0])

@app.route('/update_medication/<id>', methods=['POST'])
def update_medication(id):
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        code = request.form['code']
        image_path = request.form['image_path']

        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE medications
                    SET name = %s,
                        weight = %s,
                        code = %s,
                        image_path = %s
                    WHERE id = %s
                    """, (name, weight, code, image_path, id))
        mysql.connection.commit()
        flash('Medication updated successfully')
        return redirect(url_for('int_medication'))
# Delete Medications
@app.route('/delete_medication/<string:id>')
def delete_medication(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM medications WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Medication deleted successfully')
    return redirect(url_for('int_medication'))
#...

#==========
# Route: Drone Registers
@app.route('/int_drone/drone_registers')
def drone_registers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM drones')
    data = cur.fetchall()
    return render_template('drone_registered.html', drones=data)
# ...

# Route: Add Medications to Drone
@app.route('/add_medication_to_drone/<int:drone_id>', methods=['GET'])
def add_medications(drone_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medications')
    data = cur.fetchall()
    return render_template('add_medications.html', drone_id=drone_id, medications=data)
#...

# Add: Medications to drone
@app.route('/add_medication_to_drone/<int:drone_id>', methods=['POST'])
def add_medication_to_drone(drone_id):
    if request.method == 'POST':
        medication_ids = request.form.getlist('medications')
        print('Medication IDs:', medication_ids)

        cur = mysql.connection.cursor()

        # drone function or not
        cur.execute('SELECT * FROM drones WHERE id = %s', (drone_id,))
        drone_data = cur.fetchone()

        if not drone_data:
            return jsonify({'message': 'Drone not found'}), 404

        # medications function or not
        if not medication_ids:
            return jsonify({'message': 'No medications selected'}), 400

        placeholders = ','.join(['%s' for _ in medication_ids])
        query = 'SELECT * FROM medications WHERE id IN ({})'.format(placeholders)
        cur.execute(query, tuple(medication_ids))
        medication_data = cur.fetchall()

        if len(medication_data) != len(medication_ids):
            return jsonify({'message': 'One or more medications not found'}), 404

        # height medications
        total_weight = sum([med[2] for med in medication_data])

        # Verificar si el dron puede cargar ese peso 
        if drone_data[3] < total_weight:
            return jsonify({'message': 'Drone cannot carry that weight'}), 400

        # Actualizar estado del dron a LOADING solo si la batería está por encima del 25%
        if drone_data[4] >= 25:
            new_state = 'LOADING'
            cur.execute('UPDATE drones SET state = %s WHERE id = %s', (new_state, drone_id))
            mysql.connection.commit()

            # Crear entrada en la tabla loaded_medications para cada medicamento cargado en el dron
            for med in medication_data:
                cur.execute('INSERT INTO loaded_medications (drone_id, medication_id, quantity) VALUES (%s, %s, %s)',
                            (drone_id, med[0], 1))

            mysql.connection.commit()

            flash('Medications loaded to drone')
            return redirect(url_for('int_drone'))

        return jsonify({'message': 'Drone battery level is below 25% and cannot be loaded'}), 400
# ...

# Route Drones Loaded Medications.
@app.route('/loaded_drones')
def loaded_drones():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM drones WHERE state = "LOADING"')
    data = cur.fetchall()
    return render_template('loaded_drones.html', drones=data)

@app.route('/empty_drone/<string:id>')
def empty_drone(id):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE drones SET state = "EMPTY" WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Drone emptied successfully')
    return redirect(url_for('loaded_drones'))
#...

#==========
# Run App & Finish Projects
if __name__ == '__main__':
    app.run(port=8590, debug=True)
    #...
# email: bethocubans1990@gmail.com