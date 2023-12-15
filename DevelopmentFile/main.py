from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets 
import psycopg2.extras
import db
from passlib.context import CryptContext
password_ctx=CryptContext(schemes=['bcrypt'])#configuration de la bibliothèque

app = Flask(__name__)

app.secret_key=b'3661837482e6ec2b355b0dfac16b7c15338627557c416988e8d1c3d43db02820'

class User(UserMixin) : 
    def __init__ (self, user_id, nom,prenom, password,difficulte) :
        self.difficulte=difficulte
        self.id=user_id
        self.nom = nom
        self.prenom = prenom 
        self.password = password

@app.route("/")
def homepage() : 
    if 'mail' not in session : 
        return redirect('login')
    return render_template("homePage.html",ses=session)

login_manager=LoginManager()
login_manager.login_view= "login"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id) : 
    return User.query.get(str(id))


@app.route("/difficulté")
def difficulté():
    
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("select * from difficulte;")
            result=cur.fetchall()

    return render_template("difficultés.html",content=result,ses=session)

@app.route("/sites")
def sites() :
    with db.connect() as conn: 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("select * from siteesca;")
            result=cur.fetchall()
    return render_template("sites.html",content=result,ses=session)


@app.route("/site/<select>")
def site(select) :
    with db.connect() as conn: 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select voie.idv, voie.nom, voie.longueur, voie.fr from siteesca, voie where (siteesca.idse = voie.idse) AND (siteesca.idse=%s);",(select,))
            result=cur.fetchall()
    return render_template("site.html",content=result,ses=session)
    #SELECT voie.nom, voie.longueur, voie.fr from siteesca, voie where (siteesca.idse= voie.idse) AND (siteesca.idse=X);



@app.route("/register",methods=["GET","POST"])
def register() :
    if request.method=="POST" : 
        nom= request.form.get("nom")
        prenom = request.form.get("prenom")
        email=request.form.get("id")
        psw1=request.form.get("psw1")
        psw2=request.form.get("psw2")
        fr=request.form.get('niveau')

        with db.connect() as conn : 
            with conn.cursor() as cur : 
                cur.execute("select mail from utilisateur where mail=%s; ",(email,))
                resultemail = cur.fetchall()
        
        if resultemail :
            flash('Email déjà utilisé.', category='error')
            print(1)
        elif nom==None or prenom==None or email ==None or psw1==None or psw2==None :
            flash('veuillez remplir les valeurs')
            print(nom,prenom,email,psw1,psw2,fr)
        elif psw1!=psw2 : 
            flash('Les mots de passes ne sont pas les même', category='error')
            print(3)
        elif (len(nom)>25 or len(nom)<2) : 
            print(4)
            flash('taille du nom incorrecte.', category='error')
        elif (len(prenom)>25 or len(prenom)<2) :
            print(5)
            flash('taille du prénom incorrecte.', category='error')
        elif ('@' not in email) or len(email)<10 or len(email)>320 : 
            print(6)
            flash('email incorrecte', category='error')
        elif len(psw1)>25 : 
            print(7)
            flash('taille du mot de passe incorrecte', category='error')
        elif fr not in ['1','2','3','4','5a','5b','5c','6a','6b','6c','7a','7b','7c','8a','8b','8c','9a','9c']:
            print(8)
            flash('difficulté non existante',category='error')
            
        else : 
            print(9)
            new_ser=User(user_id=email,nom=nom,prenom=prenom,password=psw1,difficulte=fr)
            with db.connect() as conn :
                with conn.cursor() as cur :
                    print("test")
                    cur.execute("INSERT INTO utilisateur (mail,mdp,nom,prenom,fr) VALUES (%s,%s,%s,%s,%s)",(new_ser.id,password_ctx.hash(new_ser.password) ,new_ser.nom,new_ser.prenom,new_ser.difficulte))
                    conn.commit()
                    flash('User created')
                    session['mail']=new_ser.id
                    return redirect(url_for('homepage',ses=session))

    with db.connect() as conn : 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select * from difficulte;")
            result=cur.fetchall()
        print(result)
    return render_template('register.html',diff=result,ses=session)


@app.route("/login",methods=["GET","POST"])
def login() :
    if request.method == "POST": 
        log=request.form.get('id')
        psw=request.form.get('psw')
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("select mdp from utilisateur where mail=%s ",(log,))
                result=cur.fetchall()
                if not result :
                    return render_template("loginfailure.html",ses=session)
        password=result[0][0]
        
        if password_ctx.verify(psw,password) :  
            session['mail']=log
            return render_template("loginsuccesful.html",content=log)
        else : return render_template("loginfailure.html")
    else : 
        return render_template('login.html')


@app.route("/cordees",methods=["GET","POST"])
def cordees() : 
    if 'mail' not in session : 
            return redirect('login')
    with db.connect() as conn : 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select * from cordee;")
            result =  cur.fetchall()
    
    return render_template('cordees.html',content=result)

@app.route("/cordee/<select>")
def cordeeselect(select) : 
    if 'mail' not in session :
        return redirect('login')
    nom=[]
    with db.connect() as conn : 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select mail from partiec where idcordee=%s;",(select,))
            result = cur.fetchall()
            cur.execute("select * from cordee where idcordee=%s;",(select,))
            cordee=cur.fetchall()
            
            for item in result : 
                cur.execute("select nom,prenom from utilisateur where mail=%s", (item[0],))
                res=cur.fetchall()
                res=res[0]
                nom.append((item[0],f"{res[0]} {res[1]}"))
    return render_template('cordee.html', content=nom,cordee=cordee)

@app.route("/user/<select>")
def user(select) :
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn : 
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select * from utilisateur where mail=%s", (select,))
            result=cur.fetchall()
            result=result[0]

    return render_template("user.html",content=result)
if __name__ == "__main__" :
    app.run()