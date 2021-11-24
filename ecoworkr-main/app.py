import flask
from flask.templating import render_template_string
import json
from jinja2 import Template
from flask import request, redirect, url_for, render_template_string

from flask import Flask, render_template
import math

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route("/home")
def home():
	return redirect("/", code=302)

@app.route('/reduce_your_footprint', methods=('GET', 'POST'))
def reduce_your_footprint():
    return render_template('reduce-your-footprint.html')

@app.route('/about-the-project', methods=('GET', 'POST'))
def about_the_project():
    return render_template('about-the-project.html')

@app.route('/result', methods=('GET', 'POST'))

def calculate_emissions():
    
        request.method == 'POST'

        Others = request.form ['others']
        camera = request.form ['camera']
        screenshare = request.form ['screenshare']
        together = request.form ['together']
        Hours = request.form ['hours']
      
        others = float(Others)
        hours = float(Hours)

        #if camera == "Off":
        #    audio_bitrate_up = 10
        #    audio_bitrate_down = 10
        #else:
        #    audio_bitrate_up = 0
        #    audio_bitrate_down = 0

        audio_bitrate_up = 10
        audio_bitrate_down = 10
        
        if camera == "On" and others == 1:
            video_bitrate_up = 150
            video_bitrate_down = 150
        elif camera == "On" and others > 1:
            video_bitrate_up = 150
            video_bitrate_down = 200
        else: 
            video_bitrate_up = 0
            video_bitrate_down = 0
        
        if screenshare == "Yes" and others == 1:
            screenshare_bitrate_up = 200
            screenshare_bitrate_down = 200
        elif screenshare == "Yes" and others > 1:
            screenshare_bitrate_up = 250
            screenshare_bitrate_down = 250
        else:
            screenshare_bitrate_up = 0
            screenshare_bitrate_down = 0
    
        if together == "Yes" and others > 1:
            together_bitrate_up = 1000
            together_bitrate_down = 1500
        else:
            together_bitrate_up = 0
            together_bitrate_down = 0
  
        total_bitrate_up = audio_bitrate_up + video_bitrate_up + screenshare_bitrate_up + together_bitrate_up
        total_bitrate_down = audio_bitrate_down + video_bitrate_down + screenshare_bitrate_down + together_bitrate_down
  
        bitrate_up_GB_hour = (total_bitrate_up / (8*(10**6))) * 3600
        bitrate_down_GB_hour = (total_bitrate_down / (8*(10**6))) * 3600
        data_usage = ((bitrate_up_GB_hour * hours) + (bitrate_down_GB_hour * hours)) * others
  
        from django.shortcuts import render
        import requests
        import json
        url = "https://beta.api.climatiq.io/estimate"
        payload = json.dumps({
            "emission_factor": "aws-eu-west-2-networking",
            "parameters": {
                "amount": data_usage,
                "amount_unit": "GB"
                }
            })
        headers = {
                'Authorization': #key,
                'Content-Type': 'application/json'
                }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json()
        emissions = round(response_data["co2e"] * 1000, 2)

        car_equivalent = round((emissions / 116) * 1000, 0)
        
        return  render_template('result.html', result=emissions, result2 = car_equivalent)


if __name__ == '__main__':
    app.run(debug=True)
