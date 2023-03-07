from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from crypt import methods
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moneyData.db'
app.config['SECRET_KEY'] = os.urandom(24)#暗号化キー
db=SQLAlchemy(app)



class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    money = db.Column(db.Integer, nullable=False)
    paymenttype = db.Column(db.String(4),nullable=False)#1か2
    created_at = db.Column(db.DateTime, nullable = False ,default = datetime.now(pytz.timezone('Asia/Tokyo')))



@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        datas = Data.query.all()
        
        plus=0#収入合計
        mynus=0#支出合計
        for data in datas:
            if data.money>0:
                plus+=data.money
            else:
                mynus+=data.money
        
        sum=plus+mynus #合計
        count = db.session.query(Data).count()

        return render_template("index.html",datas=datas,sum=sum,plus=plus,mynus=mynus,count=count)


@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        money = request.form.get('money')
        payment = request.form.get('paymenttype')

        money = float(money)
        if payment=="+":
            paymenttype="収入"
            
        else:
            paymenttype="支出"
            money = money*(-1)
            
        created_at = datetime.now(pytz.timezone('Asia/Tokyo'))
        
        data = Data(title=title, money=money, paymenttype=paymenttype,created_at=created_at)
        db.session.add(data)
        db.session.commit()
        return redirect('/')

    else:
        return render_template("add.html")

@app.route('/<int:id>/delete', methods=['GET']) #可変なURLを設定している
def delete(id):

    data = Data.query.get(id) #インスタンス化している

    db.session.delete(data)
    db.session.commit()#データベースのコミット
    return redirect('/')  #index.htmlを読み込む宣言

@app.route('/delete_all', methods=['GET']) #全てのデータを削除する
def delete_all():
    
    datas = db.session.query(Data).filter(Data.id == Data.id).all()#idのみを全て射影している
    for data in datas:
        db.session.delete(data)
        db.session.commit()

    return redirect('/')  #index.htmlを読み込む宣言



@app.route('/<int:id>/update', methods=['GET','POST']) #可変なURLを設定している
def update(id):

    data = Data.query.get(id) #インスタンス化している

    if request.method == 'GET':
        data.money=abs(data.money)
        return render_template('update.html',data=data) 

    else:
        data.title = request.form.get('title')
        data.money = request.form.get('money')
        payment = request.form.get('paymenttype')

        data.money = float(data.money)
        if payment=="+":
            data.paymenttype="収入"
        else:
            data.paymenttype="支出"
            data.money = data.money*(-1)
        
        created_at = datetime.now(pytz.timezone('Asia/Tokyo'))

        db.session.commit()#データベースのコミット

        return redirect("/")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__=='__main__':
    app.run(debug=True)