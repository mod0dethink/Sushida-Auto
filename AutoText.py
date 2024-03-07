from PIL import ImageGrab
import pytesseract
import time
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'UR PATH TO TESSERACT'

typing_speed = float(input("1文字間隔のスピードを秒単位で入力してください（例: 0.1）: "))

while True:
    # 画面の解像度を取得
    screen_width, screen_height = ImageGrab.grab().size

    # 画面の中心座標を計算
    center_x, center_y = screen_width / 2, screen_height / 2

    # ピクセルの範囲
    offset = 100  # フルスクリーンにしたときのちょうどいいoffset
    left = center_x - 200
    top = center_y - 100 - offset  # 上に移動
    right = center_x + 200
    bottom = center_y + 100 - offset  # 上に移動

    # 指定した範囲でスクリーンキャプチャを取得
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    # 画像から文字を認識
    text = pytesseract.image_to_string(screenshot, lang='eng')

    # 認識した文字を加工（小文字のみ,"-"と","を保持）
    text_to_type = ''.join(filter(lambda x: x.islower() or x == "-" or x == ",", text))
    print(text_to_type)
    
    # 認識したテキストを1文字ずつタイピング
    for char in text_to_type:
        pyautogui.typewrite(char)
        time.sleep(typing_speed)  # 0.01秒間隔でタイピング

    time.sleep(0.01)