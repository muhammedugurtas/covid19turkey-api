from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    veri = requests.get("https://covid19.saglik.gov.tr/")

    soup = BeautifulSoup(veri.content, "html.parser")

    tum = soup.find_all("script")

    denemejson = (str(tum[19]).split("var sondurumjson = ")[1][:-18]).split("var")[0].rstrip(";")

    jsonayarla = json.loads(denemejson)

    return jsonify(jsonayarla)