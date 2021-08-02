

from flask import Flask,session,g,render_template,redirect,url_for,request
from blueprint_test import bp
from db_helper import get_db
from fonksiyon_app import login_required


app = Flask(__name__)
app.secret_key=b'_5#y2L"F4Q8z\n\xec]/'








@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


app.register_blueprint(bp)

# @app.route('/isler')
# def isler():
#     db= get_db()
#     db.row_factory = make_dicts
#     cr = db.cursor()
#     cr.execute('select * from isler')
#     items=cr.fetchall()
#     print(items)
#
#
#     return "isler_items"



@app.route('/')
@login_required
def hello_world():

    return redirect(url_for('auth.login'))




@app.route('/anasayfa')
@login_required
def anasayfa():
    if "username" not in session:
        return redirect(url_for('auth.login'))
    db = get_db()

    cr = db.cursor()
    # params = []
    # q= request.args.get("query")
    # if q:
    #     sql =+" where is_icerik like '%?%'"
    #     params.append(q)

    print( (session["user_id"]))
    sql="select * from isler where kullanici_id=?"
    cr.execute(sql,str(session["user_id"]))

    db.commit()


    #print(params)
    items = cr.fetchall()
    # print(items)
    return render_template('anasayfa.html',items=items)


@app.route('/duzenle/<id>',methods=["GET","POST"])
@login_required
def duzenle(id):
    db=get_db()
    cr=db.cursor()

    if request.method == "POST":
        is_baslik=request.form.get("is_baslik")
        is_icerik=request.form.get("is_icerik")

        sql="update isler set is_baslik=? , is_icerik=? where is_id=?"
        cr.execute(sql,(is_baslik,is_icerik,id))
        db.commit()

        return redirect(url_for("anasayfa"))

    sql='select * from isler where is_id=?'
    cr.execute(sql,(id,))
    item_id=cr.fetchone()
    print(item_id)
    return render_template("duzenle.html",item_id=item_id)


@app.route('/sil/<id>',methods=["GET","POST"])
@login_required
def sil(id):
    db = get_db()
    cr = db.cursor()
    if request.method == "GET":
        is_baslik = request.form.get("is_baslik")
        is_icerik = request.form.get("is_icerik")

        sql="DELETE FROM isler WHERE is_id =?"
        cr.execute(sql, (id,))
        db.commit()

        return redirect(url_for("anasayfa"))


    return render_template("sil.html")



@app.route('/ekle',methods=["GET","POST"])
@login_required
def ekle():

    if request.method == "POST":
        is_baslik=request.form.get("is_baslik")
        is_icerik=request.form.get("is_icerik")

        db=get_db()
        cr=db.cursor()
        sql="insert into isler(is_baslik,is_icerik,kullanici_id) values(?,?,?) "
        cr.execute(sql,(is_baslik,is_icerik,session["user_id"]))
        db.commit()
        isler=cr.fetchall()
        print("isşler")
        print(isler)

        return redirect(url_for("anasayfa"))


    return render_template("ekle.html")





if __name__ == '__main__':
    app.run(debug=True)
