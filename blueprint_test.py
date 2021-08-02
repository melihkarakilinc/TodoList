from flask import Flask,Blueprint,request,app,session,render_template,redirect,url_for
from db_helper import get_db

bp=Blueprint('auth',__name__,url_prefix='/auth')





@bp.route('/login',methods=["GET","POST"])
def login():
    error_massage=""
    if request.method=="POST":

        username=request.form.get("username")
        password=request.form.get("password")
        if not username or not password:
            error_massage="Lütfen bilgileri eksiksiz giriniz !"
        else:
            db= get_db()
            cr=db.cursor()
            cr.execute("select * from users where email=? and sifre=?",(username,password))
            user=cr.fetchone()

            if not user:
                error_massage = "Lütfen bilgileri eksiksiz giriniz !"
            else:

                session["username"]= user["email"]
                session["user_id"]=user["id"]

                return redirect(url_for("anasayfa"))


    return render_template('login.html', error_massage=error_massage)

@bp.route('/cikis')
def cikis():
    session.pop("username",None)
    return redirect(url_for("auth.login"))

@bp.route('/kayit_ol',methods=['GET','POST'])
def kayit_ol():
    error_massage = ""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password_tekrar=request.form.get("password_tekrar")

        if not username or not password:
            error_massage="Lütfen bilgileri eksiksiz giriniz !"

        elif password != password_tekrar:
            error_massage="ŞİFRELER UYUŞMAMAKTADIR"

        else:
            db = get_db()
            cr = db.cursor()
            sql="insert into users(email, sifre) values (?,?)"
            cr.execute(sql,(username,password))
            db.commit()
            return redirect(url_for("auth.login"))




    return render_template("kayit_ol.html", error_massage=error_massage)