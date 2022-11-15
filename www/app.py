#!/usr/bin/python3
from flask import Flask, render_template, request
#flask モジュールをインポート
app = Flask(__name__)

@app.route("/") #ルートディレクトリを設定(この場合は~/www)
def hello_world():
    name = request.args.get("name")
    return render_template(
        "index.html", 
        title="flask test", 
        name=name
    ) #HTMLを返す

if __name__ == "__main__": #メイン関数のおまじない
    app.run(host="0.0.0.0", debug=True)