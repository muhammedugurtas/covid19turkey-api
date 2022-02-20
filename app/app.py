from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json
from jsonmerge import merge

app = Flask(__name__)

@app.route('/')
def index():
    veri = requests.get("https://covid19.saglik.gov.tr/")

    soup = BeautifulSoup(veri.content, "html.parser")

    tum = soup.find_all("script")

    doz1asisayisi = str(tum[8]).split("var doz1asisayisi = ")[1].split(";")[0].split("'")[1]
    doz2asisayisi = str(tum[8]).split("var doz2asisayisi = ")[1].split(";")[0].split("'")[1]
    doz3asisayisi = str(tum[8]).split("var doz3asisayisi = ")[1].split(";")[0].split("'")[1]
    gunlukasidozsayisi = str(tum[8]).split("var gunluksidozusayisi = ")[1].split(";")[0].split("'")[1]
    guncellenentarih = str(tum[8]).split("var asidozuguncellemesaati = ")[1].split(";")[0].split(",")[0].split("'")[1]
    denemejson = (str(tum[19]).split("var sondurumjson = ")[1][:-18]).split("var")[0].rstrip(";")

    jsonayarla = json.loads(denemejson)

    asilarjson = {
        "Asilar": {
            "Doz1AsiSayisi": doz1asisayisi,
            "Doz2AsiSayisi": doz2asisayisi,
            "Doz3AsiSayisi": doz3asisayisi,
            "GunlukAsiDozSayisi": gunlukasidozsayisi,
            "GuncellenenTarih": guncellenentarih
        }
    }

    gunlukdurumjson = {
        "GunlukDurum": {
            **jsonayarla[0]
        }
    }

    denemes = merge(asilarjson, gunlukdurumjson)

    return jsonify(denemes)
