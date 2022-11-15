import numpy as np
def saltpepper(img):
    r = np.random.rand(480, 640) # カメラの画像と解像度をそろえる
    # 乱数配列の各要素と比較してノイズの色を変える
    img[(r<0.01)] = [255, 255, 255] # 白
    img[(r<0.005)] = [0, 255, 0] # 緑