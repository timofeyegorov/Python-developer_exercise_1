import requests
import json
from flask import Flask


def get_valutes_list():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = json.loads(response.text)
    valutes = list(data['Valute'].values())
    return valutes


app = Flask(__name__)

up_arrow = "\u2191"
down_arrow = "\u2193"
table_heads = ['ID', 'NumCode', 'CharCode', 'Nominal', 'Name', 'Value', 'Previous']

def create_html(valutes):
    text = '<h1>Курс валют</h1>'
    text += '<table border="2">'
    text += '<tr>'
    for table_head in table_heads:
        if table_head in ['Value', 'Previous']:
            text += f'<th colspan=2>{table_head}</th>'
        else:
            text += f'<th>{table_head}</th>'
    text += '</tr>'
    for valute in valutes:
        text += '<tr>'
        for idx, v in enumerate(list(valute.values())):
            text += f'<td>{v}</td>'
            if idx == 4:
                if list(valute.values())[5] > list(valute.values())[6]:
                    text += f'<td bgcolor="#c9f76f">{up_arrow}</td>'
                else:
                    text += f'<td bgcolor="#FF0000">{down_arrow}</td>'
            if idx == 5:
                if list(valute.values())[6] > list(valute.values())[5]:
                    text += f'<td bgcolor="#c9f76f">{up_arrow}</td>'
                else:
                    text += f'<td bgcolor="#FF0000">{down_arrow}</td>'
        text += '</tr>'

    text += '</table>'
    return text


@app.route("/")
def index():
    valutes = get_valutes_list()
    html = create_html(valutes)
    return html


if __name__ == "__main__":
    app.run()