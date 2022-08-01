from email import contentmanager
import re
from wsgiref.util import request_uri
from numpy import choose
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, redirect, request
import sys



city_dict = {}

with open ('city.txt', 'r') as f:
    content = f.read()

# clean up string in text file and split into keys(city) and values(id_num) in a dictionary
content = content.replace("\">", ";").replace("\"", "")
city_dict = dict(x.split(";") for x in content.strip().split("\n"))
city_dict = {y:int(x) for x, y in city_dict.items()}

# returns the id_number of a city given a city choice and a dictionary containing cities and
# their corresponding id numbers
def choose_city(city_choice, city_dict):
    for city, city_num in city_dict.items():
        if city_choice == city:
            return city_num

# example with Ho Chi Minh city, with data taken from 24h weather forecast
#city_number = choose_city("TP.HCM", city_dict)

def return_weather(id_number):
    url = 'https://www.24h.com.vn/du-bao-thoi-tiet-c568.html?province={}'.format(id_number)

    request_ = requests.get(url)
    soup = BeautifulSoup(request_.text, 'html.parser')

    title = soup.find('table', {'class': 'tabTop'})

    full_lines = title.find_all('td')

    linesArr = []
    # linesArr.append(title.get_text().upper())
    for line in full_lines:
        linesArr.append(line.get_text())

    return linesArr


# Print text here with line break
# for linea in linesArr:
#     print(linea + '\n', '='*5)
def produce_output(arr):
    output = ''
    for line in arr:
        output += line
    
    return output



app = Flask(__name__)
@app.route("/get-weather", methods=['POST'])
# request to get weather from api via json request
def get_weather():
    req_json = request.json
    city = req_json['city']
    city_number = choose_city(city, city_dict)
    arr = return_weather(city_number)

    output = produce_output(arr)
    
    return output

if __name__ == '__main__':
    app.run(debug=True)




