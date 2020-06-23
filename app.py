import os
# splite3をimportする
import sqlite3
# randomを使えるようにする
import random
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabakoza'

from datetime import datetime

# ガチャトップページ
@app.route('/')
def index():

    return render_template('index.html')

# ガチャ実行後ページ
@app.route('/gacha/<int:money>',methods=["GET", "POST"])
def gacha(money):
        # 選んだ金額
    money = money # ボタンから取ってくる値 100 or 200 or 300
        # 残っている金額
    budget = money # 残金 最初はmoneyと同じ 

    while budget > 0:

        # データベースに接続
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select * from items where price <= ?",(budget,))
        conn.commit()
            # fetchoneはタプル型 fetchall
        candidate = c.fetchall()
        conn.close()

        if len(candidate) == 0:
            break
        
        # Pythonでリストからランダムに要素を選択するchoice,   
        # https://note.nkmk.me/python-random-choice-sample-choices/
        food = random.choice(candidate)
        # 残ったお金は 残金-ranndam.choiceしたfoodの値段
        budget = budget - int(food[1])
        # 空のmenuリストを用意
        menu = []
        menu.append(food)

    # コンソールに出力しながら開発
        print("---")
        print("投入金額 money", end=':')    
        print(money)
        print("候補リスト candidate", end=':')    
        print(candidate)
        print("選ばれたひとつ food", end=':')    
        print(food)
        print("選ばれたリスト menu", end=':')    
        print(menu)
        print("残金 budget", end=':')
        print(budget)
        print("---")

    #    while budget > 0 ループを抜けた後で
    # お釣り計算
    budget = money - budget

    # コンソールに出力しながら開発
    # print("---")
    # print("money")    
    # print(money)
    # print("---")
    # print("candidate")    
    # print(candidate)
    # print("---")
    # print("menu")    
    # print(menu)
    # print("---")
    # print("残金")
    # print(budget)
    # print("---")

    return render_template('gacha.html', money = money, menu = menu, budget = budget)



# お買い物計算ページ まだ中身はない。
@app.route('/calc',methods=["GET", "POST"])
def calc():
    return render_template('calc.html')



@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)  
#    app.run(debug=False)  
