from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class patientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    reading = db.Column(db.String(200))
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(200), nullable=False)
    device = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Device %r' % self.id

@app.route('/', methods=['POST', 'GET'])
def addDevice():
    if request.method == 'POST':
        newDevice = request.form['device']
        newName = request.form['name']
        newSerialNumber = request.form['serial_number']
        newIssuer = request.form['issuer']
        newReading = request.form['reading']
        newStatus = request.form['status']

        newPatient = patientData(device=newDevice, name=newName, serial_number=newSerialNumber, issuer=newIssuer, status=newStatus, reading=newReading)

        try:
            db.session.add(newPatient)
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating records"

    else:
        patients = patientData.query.order_by(patientData.issue_date).all()
        return render_template('index.html', patients=patients)

@app.route('/delete/<int:id>')
def delete(id):
    patient_to_delete = patientData.query.get_or_404(id)

    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Error deleting task"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    patient = patientData.query.get_or_404(id)

    if request.method == 'POST':
        patient.device = request.form['device']
        patient.name = request.form['name']
        patient.serial_number = request.form['serial_number']
        patient.issuer = request.form['issuer']
        patient.reading = request.form['reading']
        patient.status = request.form['status']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating"
    else:
        return render_template('update.html', patient=patient)




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)