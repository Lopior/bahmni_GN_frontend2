from flask import Flask, render_template, jsonify, request, redirect, make_response
import requests
import json
import datetime
from dotenv import load_dotenv
import os
import pdfkit
from weasyprint import HTML

app = Flask(__name__)

load_dotenv()
url_backend = os.getenv('url_backend_var')

# Configura la ruta a wkhtmltopdf
path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
config_pdf = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notificacionges/<string:id_ges>', methods=['GET'])
def get_ges_data(id_ges):
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(f'{url_backend}/ges/{id_ges}')
        practitioner_user = request.args.get('practitioner')
        practitioner_user = practitioner_user.strip()  # Remove leading and trailing spaces
        practitioner_user = practitioner_user.replace('"', '')  # Remove double quotes
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            data = response.json()
            # Procesar los datos obtenidos
            # consultar el person id y name del practitioner
            response_practitioner = requests.get(f'{url_backend}/practitioner/{practitioner_user}')
            
            if response_practitioner.status_code == 200:
                data_practitioner = response_practitioner.json()
                data['notificador_id'] = data_practitioner['person_id']
                data['nombre_notificador'] = data_practitioner['given_name']+' '+data_practitioner['family_name']
                # Extraer fecha y hora actual
                now = datetime.datetime.now()
                data['fechahora_notificacion'] = now.strftime("%Y-%m-%d %H:%M:%S")
                return render_template('form_ges.html', data=data)
            else:
                return 'Error al obtener los datos del practitioner', 500
        else:
            return 'Error al obtener los datos del caso', 500
    except Exception as e:
        print("Error al notificar GES:", str(e))
        return jsonify({'cod': 'error', 'message': 'error al notificar GES'+str(e)})
    
@app.route('/api/notificacionges', methods=['POST'])
def post_ges_data():
    data = dict(request.form)
    # Hacer la solicitud POST al backend
    response = requests.post(url_backend+'/ges', json=json.dumps(data))
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        return render_template('form_ges_response.html', data=response.json())
    else:
        return 'Error al enviar los datos al backend', 500

@app.route('/api/notificaciongespaciente/<string:uuid_notificacion>', methods=['GET'])
def get_ges_paciente_data(uuid_notificacion):
    # Hacer la solicitud GET a la API
    response = requests.get(f'{url_backend}/ges?uuid={uuid_notificacion}')
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        return render_template('form_ges_paciente.html', data=data)
    else:
        return 'Error al obtener los datos del caso', 500

@app.route('/api/notificaciongespaciente', methods=['POST'])
def post_ges_data_paciente():
    try:
        data = dict(request.form)
        # Hacer la solicitud POST al backend
        response = requests.post(url_backend+'/ges/firma', json=json.dumps(data))
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            return render_template('form_ges_response.html', data=response.json())
        else:
            return 'Error al enviar los datos al backend', 500
    except Exception as e:
        print("Error al firmar notificacion GES:", str(e))
        return jsonify({'cod': 'error', 'message': 'error al firmar notificacion GES'+str(e)})
    
@app.route('/vernotificacionges/<string:id_ges>', methods=['GET'])
def view_ges_data(id_ges):
    # Hacer la solicitud GET a la API
    response = requests.get(f'{url_backend}/ges/{id_ges}')
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        return render_template('form_ver_ges.html', data=data)
    else:
        return 'Error al obtener los datos del caso', 500

@app.route('/api/vernotificacionges/pdf/<string:id_ges>', methods=['GET'])
def view_ges_data_pdf(id_ges):
    html = view_ges_data(id_ges)
    pdf = pdfkit.from_string(html, False, configuration=config_pdf)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

@app.route('/api/vernotificacionges/pdf2/<string:id_ges>', methods=['GET'])
def view_ges_data_pdf2(id_ges):
    html = view_ges_data(id_ges)
    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8092)