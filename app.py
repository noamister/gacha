import os
# splite3をimportする
import sqlite3
# randomを使えるようにする
import random
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session , url_for
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

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
        # 空のmenuリストを用意
    menu = []

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
        menu.append(food)

        # コンソールに出力しながら開発
        print("---ガチャループ中---")
        print("候補 candidate ", end=': ')    
        print(candidate)
        print("お菓子追加 food", end=': ')    
        print(food)
        print("残金 budget   ", end=': ')
        print(budget)

    #    while budget > 0 ループを抜けた後で
    # お菓子の合計額は
    total = money - budget
    # budgetはおつり

    # コンソールに出力しながら開発
    print("---ガチャループ終了---")
    print("投入金額 money ", end=': ')    
    print(money)
    print("ガチャ結果 menu", end=': ')    
    print(menu)
    print("おつり budget ", end=': ')
    print(budget)
    print("---")

    # # データベースからitemを取ってくる タプルで
    # conn = sqlite3.connect("service.db")
    # c = conn.cursor()
    # c.execute("select name, price, img from foods") # item全てDBから取得
    # foods_tuple = c.fetchall() #このitemsタプル
    # print(foods_tuple)
    # c.close()

    # food0 = foods_tuple[0]
    # for food in foods_tuple:
    # print(food)

    # # データベースからitemを取ってくる リストで
    # conn = sqlite3.connect("service.db")
    # c = conn.cursor()
    # c.execute("select id, name, price, img from foods") # item全てDBから取得
    # foods_list = [] #このitems_listリストは最初は空だが、for文で埋まっていく
    # for row in c.fetchall():  #fetchaiiは多次元配列（リストの中のリスト）でくる。わかりにくい。
    #     # インデックス管理わかりにくい => idやtaskというkey,キーバリューで管理するためにデータの整形
    #     foods_list.append({"id":row[0], "name":row[1], "price":row[2], "img":row[3] }) #appendでその後ろの（）内のデータを追加する。
    # print(foods_list)
    # c.close()

    # 初期値０
    sumi1 = 0
    sumi2 = 0
    sumi3 = 0
    sumi4 = 0
    sumi5 = 0
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]

    # ここからtannnoさんのコピペ タプルに変更
    i1 = ('うまい棒', 10, 'img001')
    i2 = ('ブラックサンダー', 30, 'img002')
    i3 = ('ココアシガレット', 30, 'img003')
    i4 = ('ガリガリ君', 75, 'img004')
    i5 = ('ハーゲンダッツ', 275, 'img005')
    ci1 = menu.count(i1)
    ci2 = menu.count(i2)
    ci3 = menu.count(i3)
    ci4 = menu.count(i4)
    ci5 = menu.count(i5)
    sumi1 = ci1*10
    sumi2 = ci2*30
    sumi3 = ci3*30
    sumi4 = ci4*75
    sumi5 = ci5*275
 
    #↓ここからprintで上を確認
    print(i1)
    print(ci1)
    print(sumi1)
    # ここまでtannnoさんのコピペ

    for i in range(ci1):
        list1.append(1)
    print(list1)
    for i in range(ci2):
        list2.append(2)
    print(list2)
    for i in range(ci3):
        list3.append(3)
    print(list3)
    for i in range(ci4):
        list4.append(4)
    print(list4)
    for i in range(ci5):
        list5.append(5)
    print(list5)
    # お釣りbudgetを、紙幣とコインで表示する。

    bill10000 = int(budget / 10000)
    budget = budget % 10000
    bill5000 = int(budget / 5000)
    budget = budget % 50000
    bill1000 = int(budget / 1000)
    budget = budget % 10000
    coin500 = int(budget / 500)
    budget = budget % 5000
    coin500 = int(budget / 500)
    budget = budget % 5000
    coin100 = int(budget / 100)
    budget = budget % 100
    coin50 = int(budget / 50)
    budget = budget % 50
    coin10 = int(budget / 10)
    budget = budget % 10
    coin5 = int(budget / 5)
    coin1 = budget % 5

    print("紙幣とコイン枚数 1万、5千、千、500、100、50、10、５、１の順")
    print(bill10000)
    print(bill5000)
    print(bill1000)
    print(coin500)
    print(coin100)
    print(coin50)
    print(coin10)
    print(coin5)
    print(coin1)

    # おつりが五円か0円かでトレイイメージを変更する。

    if coin5 == 1:
        tray_image = ('../static/img/tray5yen.png')
        # tray_image = ../static/img/tray5yen.png
    else:
        tray_image = ('../static/img/tray.png')
        # tray_image = ../static/img/tray.png
    
    # gacha.html画面に値を渡す
    # return render_template('gacha.html', money = money, menu = menu, budget = budget, total = total)
    return render_template('gacha.html', money = money, menu = menu, budget = budget, total = total, ci1 = ci1, ci2 = ci2, ci3 = ci3, ci4 = ci4, ci5 = ci5, sumi1 = sumi1, sumi2 = sumi2, sumi3 = sumi3, sumi4 = sumi4, sumi5 = sumi5, list1 = list1, list2 = list2, list3 = list3, list4 = list4, list5 = list5, bill10000 = bill10000, bill5000 = bill5000 ,bill1000 = bill1000, coin500 = coin500,coin100 = coin100,coin50 = coin50,coin10 = coin10, coin5 = coin5, coin1 = coin1, tray_image = tray_image)

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
