#!/usr/bin/env python

from flask import Flask,json, render_template, request, send_file
import os

#create instance of Flask app
app = Flask(__name__)

#decorator 
@app.route("/")
def hello():
    #it is a good idea to include information on how to use your API on the home route
    text = '''go to /all to see all events
              and /year/<year> to see events for a particular year'''
    return render_template('index.html', html_page_text=text)
  
@app.route("/all")
def all():
    json_url = os.path.join("data","data.json")
    data_json = json.load(open(json_url))
    
    #jsonify or json.dumps
    #return json.dumps(data_json)

    #render_template is always looking in templates folder
    return render_template('index.html',html_page_text=data_json)
 
@app.route("/add")
def form():
    form_url = os.path.join("templates","form.html")
    return send_file(form_url)

@app.route("/patient_ID/<patient_ID>",methods=['GET', 'POST'])
def add_patient_ID(patient_ID):
    json_url = os.path.join("data","data.json")
    data_json = json.load(open(json_url))
    data = data_json["devices"]
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['devices']
        patient_ID = request.view_args['patient_ID']
        output_data = [x for x in data if x['patient_ID']==patient_ID]
        
        #can show with jsonify or embedded in a particular template
        #return jsonify(output_data)
        
        #render template is always looking in tempate folder
        return render_template('events.html',html_page_text=output_data)

    elif request.method == 'POST':
        device = request.form['device']

        #case sensitive, so be careful!
        serial_number= request.form['serial_number']
        issuer = request.form['issuer']
        reading = request.form['reading']
        patient_ID = request.form['patient_ID']
        issue_date = request.form['issue_date']
        status = request.form['status']
        new_device= { "device":device,
                    "serial_number":serial_number,
                    "issuer":issuer,
                    "reading":reading,
                    "patient_ID":patient_ID,
                    "issue_date":issue_date,
                    "status":status
                    }

        with open(json_url,"r+") as file:
            data_json = json.load(file)
            data_json['devices'].append(new_device)
            file.seek(0)
            json.dump(data_json, file, indent=1)
        
        #Adding text
        text_success = "Data successfully added: " + str(new_device)
        return render_template('index.html', html_page_text=text_success)
    
if __name__ == "__main__":
    app.run(debug=True)
