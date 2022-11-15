import os
import numpy as np
import cv2
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index1.html", 
                            title="Test by Flask and OpenCV")
@app.route("/send", methods=["POST"])
def send(): # ファイル読み込み
    img_file = request.files["img_file"]
    filename = secure_filename(img_file.filename) #ファイル名を加工
    p_fname = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    img_file.save(p_fname) # 一度保存
    raw_img = cv2.imread(p_fname) # 同じデータを読み込む

    raw_img_url = os.path.join(app.config["UPLOAD_FOLDER"],
                                "raw_"+filename)
    if os.path.exists(raw_img_url):
        #同じ名前のファイルが存在していたら消去
        os.remove(raw_img_url)
    os.rename(p_fname, raw_img_url) #ファイル名変更
    # 画像処理（ここではグレイスケール化）
    after_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
    # 画像処理したものを uploadsディレクトリに保存
    after_img_url = os.path.join(
    app.config["UPLOAD_FOLDER"], "after_"+filename)
    cv2.imwrite(after_img_url, after_img)
    time = int(os.stat(after_img_url).st_mtime) #保存時刻を記録
    return render_template(
    "index.html", title="After Processing the Image",
    raw_img_url=raw_img_url,
    after_img_url= after_img_url + "?" + str(time))
    # 画像処理したものを強制更新してブラウザに表示

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)