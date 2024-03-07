import cv2
import numpy as np
import pydirectinput
from mss import mss
import pyautogui
import win32api
import win32con

def move_mouse(x, y):
    win32api.SetCursorPos((x, y))

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

# スクリーンキャプチャの範囲
mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

# 画面の中央座標
center_x, center_y = mon['width'] // 2, mon['height'] // 2
# 検出範囲の半径
radius = 100

move_mouse(100,100)

while True:
    # スクリーンキャプチャを取得
    sct_img = sct.grab(mon)
    # OpenCVで扱える形式に変換
    img = np.array(sct_img)

    # 画面の中央を中心とした半径内のマスクを作成
    Y, X = np.ogrid[:mon['height'], :mon['width']]
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    circular_mask = dist_from_center <= radius

    # HSV変換前にマスクを適用
    img[~circular_mask] = 0  # 中心から半径外のピクセルを黒くする

    # BGRからHSVに変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 低いH値の赤色範囲
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    # 高いH値の赤色範囲
    lower_red2 = np.array([160, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # 両方のマスクを結合
    mask = cv2.bitwise_or(mask1, mask2)

    # ノイズ除去のためのモルフォロジー変換
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # マスクから輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # 赤色を検知したことを表示
        print("検知しました")
        # 最も大きな輪郭を見つける
        largest_contour = max(contours, key=cv2.contourArea)
        # 最も大きな輪郭の中心座標を計算
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

            # カーソルを識別した色の位置に移動（スクリーン全体の座標に変換）
            absolute_cx = mon['left'] + cx
            absolute_cy = mon['top'] + cy

            # マウス処理
            move_mouse(absolute_cx, absolute_cy)
            leftClick()

    # 'q'を押して終了
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break