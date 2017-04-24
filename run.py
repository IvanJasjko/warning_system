import os
import pandas as pd
from flask import *
from threading import Thread
from subprocess import Popen


app = Flask(__name__)
@app.route("/")
def show_warnings():
	
    pd.set_option('display.max_colwidth', -1)
    data = pd.read_csv('..\keys\Warnings.csv')
    data["Text"].replace(regex=True, inplace=True, to_replace=r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*',value=r'')
    name = data.iloc[-1]["Text"]

    recent = data["Text"]
    translation = data["Translation"]
    data["Time"] = pd.to_datetime(data["Time"])
    time = data["Time"].tolist()
    zone = pd.Timedelta(hours=3)
    link = data["Tweet_ID"].tolist()
    return render_template('view.html',name=name,recent=recent.tolist(),translation = translation.tolist(),time = time, zone = zone,link=link)

@app.route("/tables")
def show_tables():
    pd.set_option('display.max_colwidth', -1)
    data = pd.read_csv('..\keys\Warnings.csv')
    data = data[["Time","Text","Translation","User_Name"]]
    data["Text"].replace(regex=True, inplace=True, to_replace=r'\n|\r',value=r'')
    data["Translation"].replace(regex=True, inplace=True, to_replace=r'\n|\r',value=r'')
    data['Time'] = pd.DatetimeIndex(data['Time']) + pd.Timedelta(hours=3)
    df = data.reindex(index=data.index[::-1])
    return render_template('Table.html',tables=[df.to_html(index=False)])


def run_app():
	app.run(debug=False,threaded = True)

def run_stream():
	os.system("python controller.py")

def run_analysis():
	os.system("python analysis.py")

if __name__ == "__main__":
    p1 = Popen('python analysis.py', shell=True)
    p2 = Popen('python controller.py', shell=True)
    run_app()