from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GENERATE_ENDPOINT = os.environ.get('GENERATE_ENDPOINT')
GENERATE_ENDPOINT_CHAT = os.environ.get('GENERATE_ENDPOINT_CHAT')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        gen_fossil_brown_coal = data.get('gen_fossil_brown_coal') or 582.0
        gen_fossil_gas = data.get('gen_fossil_gas') or 5537.0
        gen_fossil_hard_coal = data.get('gen_fossil_hard_coal') or 4039.0
        gen_fossil_oil = data.get('gen_fossil_oil') or 331.0
        gen_hydro = data.get('gen_hydro') or 454.0
        gen_other_renewable = data.get('gen_other_renewable') or 97.0
        gen_wind_onshore = data.get('gen_wind_onshore') or 7556.0
        total_load_actual = data.get('total_load_actual') or 31648.0
        price = data.get('price') or 40.61
        max_seq_len = data.get('max_seq_len') or 1024
        max_gen_len = data.get('max_gen_len') or 1024
        temperature = data.get('temperature') or 0.0

        prompt = f"""Generate a report on the electricity usage and pricing based on the following information entered by the user:
        - generation fossil brown coal/lignite: {gen_fossil_brown_coal} This column represents the amount of electricity generated from burning brown coal or lignite, measured in megawatts (MW).
        - generation fossil gas: {gen_fossil_gas} This column represents the amount of electricity generated from burning natural gas, measured in megawatts (MW).
        - generation fossil hard coal: {gen_fossil_hard_coal} This column represents the amount of electricity generated from burning hard coal, also known as anthracite or bituminous coal, measured in megawatts (MW).
        - generation fossil oil: {gen_fossil_oil} This column represents the amount of electricity generated from burning oil or petroleum, measured in megawatts (MW).
        - generation hydro pumped storage consumption: {gen_hydro} This column represents the amount of electricity generated from pumped storage hydroelectric power plants, measured in megawatts (MW).
        - generation other renewable: {gen_other_renewable} This column represents the amount of electricity generated from other renewable energy sources, such as solar, biomass, geothermal, or tidal energy, measured in megawatts (MW).
        - generation wind onshore: {gen_wind_onshore} This column represents the amount of electricity generated from onshore wind turbines, measured in megawatts (MW).
        - total load actual: {total_load_actual} This column represents the total electricity demand or consumption at a given time, measured in megawatts (MW).
        Based on these parameters, the price of electricity (in EUR/MWh) is: {price}."""

        generate_response = requests.post(GENERATE_ENDPOINT, json={
            "prompts": [prompt],
            "parameters": {"": max_seq_len, "max_gen_len": max_gen_len, "temperature": temperature}
        })

        if generate_response.status_code == 200:
            return generate_response.json(), 200
        else:
            return jsonify({'error': 'Failed to invoke generate endpoint'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict-chat', methods=['POST'])
def predict_chat():
    try:
        data = request.get_json()

        gen_fossil_brown_coal = data.get('gen_fossil_brown_coal') or 582.0
        gen_fossil_gas = data.get('gen_fossil_gas') or 5537.0
        gen_fossil_hard_coal = data.get('gen_fossil_hard_coal') or 4039.0
        gen_fossil_oil = data.get('gen_fossil_oil') or 331.0
        gen_hydro = data.get('gen_hydro') or 454.0
        gen_other_renewable = data.get('gen_other_renewable') or 97.0
        gen_wind_onshore = data.get('gen_wind_onshore') or 7556.0
        total_load_actual = data.get('total_load_actual') or 31648.0
        price = data.get('price') or 40.61
        max_gen_len = data.get('max_gen_len') or 1024
        temperature = data.get('temperature') or 0.0

        prompt = f"""Display the following report table based on user inputs in tabular text format and write a single-paragraph report summarizing the electricity usage and forecast price:
        
        ### Table

        Generation from fossil brown coal/lignite: {gen_fossil_brown_coal} MW
        Generation from fossil gas: {gen_fossil_gas} MW
        Generation from fossil hard coal:  {gen_fossil_hard_coal} MW
        Generation from fossil oil: {gen_fossil_oil} MW
        Generation from hydro pumped storage: {gen_hydro} MW
        Generation from other renewable sources: {gen_other_renewable} MW
        Generation from onshore wind: {gen_wind_onshore} MW

        ### Totals:
        Total actual load: {total_load_actual} MW

        Forecast price: {price} EUR/MWh

        ### Short analysis:
        Please write a short analysis on the data above."""

        generate_response = requests.post(GENERATE_ENDPOINT_CHAT, json={
            "input_data": {"input_string":[[ {"role": "user", "content": prompt}]]},
            "parameters": {"max_gen_len": max_gen_len, "temperature": temperature}
        })

        if generate_response.status_code == 200:
            return generate_response.json(), 200
        else:
            return jsonify({'error': 'Failed to invoke generate endpoint'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
