from PIL import ImageGrab
import pytesseract
import time
import pyautogui
import queue
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

typing_speed = float(input("1文字間隔のスピードを秒単位で入力してください（例: 0.1）: "))

class TypingQueue(queue.Queue):
    def clear(self):
        while not self.empty():
            self.get()

    def add_text(self, text):
        for char in text:
            self.put(char)

    def type_from_queue(self):
        if not self.empty():
            text_to_type = ''.join(list(self.queue))  # キューの内容を一括で取得
            self.clear()  # キューをクリア
            pyautogui.typewrite(text_to_type, interval=typing_speed)

# タイピングする文字列を管理するキュー
typing_queue = TypingQueue()

# 最後に認識した単語を保持する変数
last_text = ''

# 認識した文字を整える
def clean_text(text):
    # 小文字、一部の記号を除く全てを除外
    text = ''.join([char for char in text if char.islower() and not char.isdigit() and char not in "=()| " or char in "-?!,"])
    
    # 母音の定義
    vowels = 'aeiou'
    
    # 'n'で始まり、その後に母音が続いていない、'al'で始まる、',y'で始まる、文頭の','を除外(よく誤認識する文字)
    patterns = [
        (r'^n(?![aeiou])', ''),  # 'n'で始まり、その後に母音が続いていない場合
        (r'^al', ''),  # 'al'で始まる場合
        (r'^,y', ''),  # ',y'で始まる場合
        (r'^,', '')  # 文頭の','を除外
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    # 子音の後に','が来ていたらそれも除外
    text = re.sub(r'(?<=[^aeiou]),', '', text)
    
    return text

while True:
    # 画面の解像度を取得
    screen_width, screen_height = ImageGrab.grab().size

    # 画面の中心座標を計算
    center_x, center_y = screen_width / 2, screen_height / 2

    # ピクセルの範囲
    left = center_x - 250
    top = center_y - 110
    right = center_x + 250
    bottom = center_y - 80

    # 指定した範囲でスクリーンキャプチャを取得
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    
    # 画像から文字を認識
    text = pytesseract.image_to_string(screenshot, lang='eng').strip()
    
    # 文字を加工
    text_to_type = clean_text(text)

    # 新しい単語が前の単語と異なる場合、キューをクリアして新しいテキストを追加
    if text_to_type != last_text:
        print(text_to_type)
        typing_queue.clear()
        typing_queue.add_text(text_to_type)
        last_text = text_to_type

        # キューから文字を取り出してタイピング
        typing_queue.type_from_queue()

    time.sleep(0.01)


