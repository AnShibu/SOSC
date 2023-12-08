from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

veg = {
    'eggplant': (20, 25),
    'tomato': (18, 24),
    'carrot': (15, 22),
    'apple': (13, 18),
}

def get_temperature(city_name):
    url = f'https://wttr.in/{city_name}?format=%t'
    try:
        data = requests.get(url)
        data.raise_for_status()  # Raise an HTTPError for bad responses
        temperature = int(re.search(r'\d+', data.text).group())
        return temperature
    except requests.exceptions.RequestException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        chosen_crop = request.form.get('crop')

        temperature = get_temperature(city)

        if temperature is not None:
            temperature_range = veg.get(chosen_crop)

            if temperature_range:
                if temperature_range[0] <= temperature <= temperature_range[1]:
                    result = f"The chosen crop ({chosen_crop}) can grow in the provided temperature ({temperature} degrees Celsius)."
                else:
                    result = f"The chosen crop ({chosen_crop}) may not grow in the provided temperature ({temperature} degrees Celsius)."
            else:
                result = "Invalid crop choice. Please choose a crop from the provided list."
        else:
            result = "Error fetching temperature data."

        return render_template('index.html', result=result, city=city, temperature=temperature)

    return render_template('index.html', temperature=None)

@app.route('/get_temperature', methods=['POST'])
def get_temperature_route():
    city = request.form.get('city')
    temperature = get_temperature(city)
    return render_template('index.html', city=city, temperature=temperature)

if __name__ == '__main__':
    app.run(debug=True)
