from flask import Flask, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json

import urllib.request
import urllib.parse

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

app = Flask(__name__)
app.debug = True
@app.route("/")
def home():
    return render_template('index.html', data=GetTotalCount())

def GetTotalCount():
    URL = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="
    res = requests.get(URL,headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('.w_bold')[0:4]
    #data = soup.select('.s_listin_dot > li')[0:4]
    result = list()
    for x in data:
        result.append(x.get_text().replace(',','').replace('명', ''))
    data = [
        {'name' : '확진자'   , 'tag' : 'danger'  , 'count' : result[0]},
        {'name' : '사망자'   , 'tag' : 'dark'    , 'count' : result[2]},
        {'name' : '검사진행' , 'tag' : 'warning' , 'count' : result[3]},
        {'name' : '격리해제' , 'tag' : 'primary' , 'count' : result[1]}]
    return data

def GetLocCount():
    URL = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun="
    res = requests.get(URL,headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table', attrs={'class':'num'})
    table_body = table.find('tbody')

    location = list()
    count = list()
    rows = table_body.find_all('tr')
    for row in rows:
        loc = row.find_all('th')
        loc = [ele.text.strip() for ele in loc]
        location.append(loc[0])
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        count.append(int(cols[1].replace(',','')))
    location = location[1:len(location)]
    count    = count[1:len(count)]
    data = dict(zip(location, count))
    return data

@app.route("/location")
def geoCoding():
    getData = GetLocCount()
    data = {
        "positions" : []
        }
    for k,v in getData.items():
        for x in range(v):
            if k == '서울':
                data['positions'].append({"lat":37.578623, "lng":126.988169})
            elif k == '부산':
                data['positions'].append({"lat":35.154887, "lng":129.056005})
            elif k == '대구':
                data['positions'].append({"lat":35.865870, "lng":128.591657})
            elif k == '인천':
                data['positions'].append({"lat":37.469301, "lng":126.700092})
            elif k == '광주':
                data['positions'].append({"lat":35.155374, "lng":126.835550})
            elif k == '대전':
                data['positions'].append({"lat":36.336850, "lng":127.394787})
            elif k == '울산':
                data['positions'].append({"lat":35.549282, "lng":129.261149})
            elif k == '세종':
                data['positions'].append({"lat":36.510528, "lng":127.255707})
            elif k == '경기':
                data['positions'].append({"lat":37.388105, "lng":127.268598})
            elif k == '강원':
                data['positions'].append({"lat":37.973851, "lng":128.313189})
            elif k == '충북':
                data['positions'].append({"lat":36.917677, "lng":127.823951})
            elif k == '충남':
                data['positions'].append({"lat":36.655106, "lng":126.790957})
            elif k == '전북':
                data['positions'].append({"lat":35.779773, "lng":127.091941})
            elif k == '전남':
                data['positions'].append({"lat":34.636756, "lng":126.695257})
            elif k == '경북':
                data['positions'].append({"lat":36.238331, "lng":128.881892})
            elif k == '경남':
                data['positions'].append({"lat":35.414577, "lng":128.226232})
            elif k == '제주':
                data['positions'].append({"lat":33.489764, "lng":126.527679})
    data = json.dumps(data, indent=2)
    return data

if __name__ == "__main__":
    app.run(host="withme.xyz", port=8080, use_reloader=False)
