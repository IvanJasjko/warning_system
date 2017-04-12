from flask import *
import pandas as pd
app = Flask(__name__)

@app.route("/warnings")
def show_warnings():
    data = pd.read_csv('..\keys\Warnings.csv')
    data["Tweet"].replace(regex=True, inplace=True, to_replace=r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*',value=r'')
    name = data.iloc[-1]["Tweet"]

    recent = data["Tweet"]
    translation = data["Translation"]
    data["Time"] = pd.to_datetime(data["Time"])
    time = data["Time"].tolist()
    zone = pd.Timedelta(hours=3)
    link = data["Tweet_ID"].tolist()
    return render_template('view.html',name=name,recent=recent.tolist(),translation = translation.tolist(),time = time, zone = zone,link=link)

@app.route("/tables")
def show_tables():
    data = pd.read_csv('..\keys\Warnings.csv')
    data = data[["Time","Tweet","Translation","User_Name"]]
    data["Tweet"].replace(regex=True, inplace=True, to_replace=r'\n|\r',value=r'')
    data["Translation"].replace(regex=True, inplace=True, to_replace=r'\n|\r',value=r'')
    data['Time'] = pd.DatetimeIndex(data['Time']) + pd.Timedelta(hours=3)
    df = data.reindex(index=data.index[::-1])
    pd.set_option('display.max_colwidth', -1)
    return render_template('table.html',tables=[df.to_html(index=False)])

if __name__ == "__main__":
    app.run(debug=True)