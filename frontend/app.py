from flask import Flask, render_template, jsonify, request
import requests
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notificacionges/<string:id_ges>', methods=['GET'])

def get_ges_data(id_ges):
    # Hacer la solicitud GET a la API
    response = requests.get(f'http://localhost:4000/ges/{id_ges}')
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        # Procesar los datos obtenidos
        #print(response.text)  # Imprimir el contenido de la respuesta en la consola
        print("*********** DATOS DESDE API BACKEND ***********")
        
        # Extraer fecha y hora actual
        now = datetime.datetime.now()
        data['fechahora_notificacion'] = now.strftime("%Y-%m-%d %H:%M:%S")
        print(data)
        return render_template('form_ges.html', data=data)
    else:
        # Manejar el caso de error en la solicitud
        return 'Error al obtener los datos del caso', 500

@app.route('/notificacionges', methods=['POST'])
def post_ges_data():
    data = dict(request.form)
    # Hacer la solicitud POST al backend
    response = requests.post('http://localhost:4000/ges', json=json.dumps(data))
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        return render_template('form_ges_response.html', data=response.json())
    else:
        # Manejar el caso de error en la solicitud
        return 'Error al enviar los datos al backend', 500

@app.route('/notificaciongespaciente/<string:uuid_notificacion>', methods=['GET'])
def get_ges_paciente_data(uuid_notificacion):
    # Hacer la solicitud GET a la API
    response = requests.get(f'http://localhost:4000/ges?uuid={uuid_notificacion}')
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        # Procesar los datos obtenidos
        #print(response.text)  # Imprimir el contenido de la respuesta en la consola
        print("*********** DATOS DESDE API BACKEND ***********")
        print(data)
        return render_template('form_ges_paciente.html', data=data)
    else:
        # Manejar el caso de error en la solicitud
        return 'Error al obtener los datos del caso', 500
    #data = "{}"
    #return render_template('form_ges_paciente.html', data=data)

@app.route('/notificaciongespaciente', methods=['POST'])
def post_ges_data_paciente():
    data = dict(request.form)
    print(data)
    print(data["firma_paciente"])
    # Hacer la solicitud POST al backend
    response = requests.post('http://localhost:4000/ges/firma', json=json.dumps(data))
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        return render_template('form_ges_response.html', data=response.json())
    else:
        # Manejar el caso de error en la solicitud
        return 'Error al enviar los datos al backend', 500
    
@app.route('/vernotificacionges/<string:id_ges>', methods=['GET'])
def view_ges_data(id_ges):
    # Hacer la solicitud GET a la API
    response = requests.get(f'http://localhost:4000/ges/{id_ges}')
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        # Procesar los datos obtenidos
        #print(response.text)  # Imprimir el contenido de la respuesta en la consola
        print("*********** DATOS DESDE API BACKEND ***********")
        print(data)
        return render_template('form_ver_ges.html', data=data)
    else:
        # Manejar el caso de error en la solicitud
        return 'Error al obtener los datos del caso', 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)


