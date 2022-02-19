import json
from fastapi import FastAPI, status, Response
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
async def root():
    veri = requests.get("https://covid19.saglik.gov.tr/")

    soup = BeautifulSoup(veri.content, "html.parser")

    tum = soup.find_all("script")

    denemejson = (str(tum[19]).split("var sondurumjson = ")[1][:-18]).split("var")[0].rstrip(";")

    jsonayarla = json.loads(denemejson)

    return jsonayarla[0]