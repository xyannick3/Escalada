"""
CECI EST LE MAIN
"""


from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets
import psycopg2.extras
import db
from passlib.context import CryptContext
password_ctx=CryptContext(schemes=['bcrypt'])#configuration de la bibliothèque

app = Flask(__name__)

app.secret_key=b'3661837482e6ec2b355b0dfac16b7c15338627557c416988e8d1c3d43db02820'

class User(UserMixin) :
    """
    Cette classe permet de stocker les éléments de connections
    """
    def __init__ (self, user_id, nom,prenom, password,difficulte) :
        self.difficulte=difficulte
        self.id=user_id
        self.nom = nom
        self.prenom = prenom
        self.password = password

@app.route("/")
def homepage() :
    """
    permet d'afficher la page principale 
    """
    # if 'mail' not in session :
    #     return redirect('login')
    return render_template("homePage.html",ses=session)

login_manager=LoginManager()
login_manager.login_view= "login"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id) :
    return User.query.get(str(id))


@app.route("/difficulté/<select>")
def difficultés(select) :
    """
    affiche la table des difficultés si une ligne est selectionnée.
    """
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("select * from difficulte;")
            result=cur.fetchall()
    return render_template("difficultés.html",content=result,ses=session,select=str(select))

@app.route("/difficulté")
def difficulté():
    """
    affiche la table des difficulté sans selection.
    """
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("select * from difficulte;")
            result=cur.fetchall()

    return render_template("difficultés.html",content=result,ses=session,select='0')

@app.route("/sites")
def sites() :
    """
    Affiche la table des sites.
    """
    with db.connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("select * from siteesca;")
            result=cur.fetchall()
    return render_template("sites.html",content=result,ses=session)


@app.route("/site/<select>")
def site(select) :
    """
    Affiche un site et ses voies.
    """
    with db.connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute(
                " select distinct mail from siteesca, estguidede where siteesca.codepostal=estguidede.codepostal and idse=%s;",
            (select,))
            guides=cur.fetchall()
            cur.execute(
                "select voie.idv, voie.nom, voie.longueur, voie.fr from siteesca, voie where (siteesca.idse = voie.idse) AND (siteesca.idse=%s);"
                ,(select,))
            result=cur.fetchall()
    return render_template("site.html",content=result,ses=session,guides=guides)


@app.route("/register",methods=["GET","POST"])
def register() :
    """
    Fiche d'inscription
    """
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
        elif ((nom is None) or
              (prenom is None) or
              (email is None) or
              (psw1 is None) or
              (psw2 is None)) :
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
        elif fr not in ['1','2','3','4','5a','5b','5c','6a','6b','6c',
                        '7a','7b','7c','8a','8b','8c','9a','9c']:
            print(8)
            flash('difficulté non existante',category='error')

        else :
            print(9)
            new_ser=User(user_id=email,nom=nom,prenom=prenom,password=psw1,difficulte=fr)
            with db.connect() as conn :
                with conn.cursor() as cur :
                    print("test")
                    cur.execute(
                        "INSERT INTO utilisateur (mail,mdp,nom,prenom,fr) VALUES (%s,%s,%s,%s,%s)",
                        (new_ser.id,password_ctx.hash(new_ser.password) 
                         ,new_ser.nom,new_ser.prenom,new_ser.difficulte))
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
    """
    page de la connexion.
    """
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
    """
    affiche la liste des cordées.
    """
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute("select * from cordee;")
            result =  cur.fetchall()

    return render_template('cordees.html',content=result)

@app.route("/cordee/<select>")
def cordeeselect(select) :
    """
    affiche une cordée selectionnée.
    """
    if 'mail' not in session :
        return redirect('login')
    nom=[]
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute("select mail from partiec where idcordee=%s;",(select,))
            result = cur.fetchall()
            cur.execute("select * from cordee where idcordee=%s;",(select,))
            cordee=cur.fetchall()
            print(cordee)
            for item in result :
                cur.execute("select nom,prenom from utilisateur where mail=%s", (item[0],))
                res=cur.fetchall()
                res=res[0]
                nom.append((item[0],f"{res[0]} {res[1]}"))
    return render_template('cordee.html', content=nom,cordee=cordee[0])

@app.route("/user/<select>", methods=["POST","GET"])
def user(select) :
    """
    affiche la fiche d'un utilisateur, si l'utilisateur est l'utilisateur connecté, 
    permet d'accèder à la page de personalisation.
    """
    if 'mail' not in session :
        return redirect('login')

    if request.method == 'POST' :
        localite=request.form.get("localite")
        with db.connect() as conn :
            with conn.cursor() as cur:
                cur.execute("INSERT INTO estguidede (mail,codepostal) VALUES (%s,%s);",
                (session['mail'],localite,))
            conn.commit()

    with db.connect() as conn :
        with conn.cursor() as cur :
            cur.execute("select mail from utilisateur where mail=%s", (select,))
            result=cur.fetchall()

            print(result)
    if not result :
        abort(404)
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute('select * from localite;')
            localite=cur.fetchall()
            cur.execute('select * from utilisateur where mail=%s', (select,))
            result=cur.fetchall()
            cur.execute('select * from estguidede where mail=%s', (select,))
            guide=cur.fetchall()
            cur.execute('select * from partiec where mail=%s', (select,))
            cordee=cur.fetchall()
            lst=[]
            for elem in cordee :
                cur.execute('select * from cordee where idcordee = %s', (elem[0],))
                test=cur.fetchall()

                lst.append(test[0])
                print(lst)

    if session['mail']!=select :
        return render_template('user.html',content=result[0],guide=guide,cordee=cordee,lst=lst)


    return render_template('userselected.html',content=result[0],guide=guide,cordee=cordee,lst=lst,localite=localite)

@app.route('/disconnect')
def disconnect():
    """
    permet de se déconnecter
    """
    session.pop('mail')
    return redirect('login')

@app.route("/usersetting", methods=["POST","GET"])
def usersetting() :
    """
    page de configuration du compte.
    """
    if 'mail' not in session :
        return redirect('login')

    if request.method == "GET" :
        with db.connect() as conn :
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
                cur.execute("select * from utilisateur where mail= %s;", (session["mail"],))
                content=cur.fetchall()
                cur.execute("select * from difficulte;")
                difficulte=cur.fetchall()
        return render_template('usersetting.html',content=content[0],difficulte=difficulte)

    if request.method == "POST" :
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

        if resultemail and email!=session['mail']:
            flash('Email déjà utilisé.', category='error')
            print(1)
        elif (
            nom==None or prenom==None or email ==None or psw1==None or psw2==None) :
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
        elif fr not in ['1','2','3','4','5a','5b','5c','6a','6b',
                        '6c','7a','7b','7c','8a','8b','8c','9a','9c']:
            print(8)
            flash('difficulté non existante',category='error')

        else :
            print(9)
            new_ser=User(user_id=email,nom=nom,prenom=prenom,password=psw1,difficulte=fr)
            if email==session["mail"] :
                with db.connect() as conn :
                    with conn.cursor() as cur :
                        cur.execute(
                            "update utilisateur set mdp =%s, nom= %s, prenom =%s, fr=%s where mail=%s;",
                            (password_ctx.hash(psw1),nom,prenom,fr,email,))
                        conn.commit()
            else : 
                with db.connect() as conn :
                    with conn.cursor() as cur :
                        cur.execute("DELETE FROM utilisateur WHERE mail=%s",(session["mail"],))
                        cur.execute(
                            "INSERT INTO utilisateur (mail,mdp,nom,prenom,fr) VALUES (%s,%s,%s,%s,%s)",
                            (new_ser.id,password_ctx.hash(new_ser.password) ,
                             new_ser.nom,new_ser.prenom,new_ser.difficulte))
                        conn.commit()
            flash('User modified')
            session['mail']=new_ser.id
            return redirect(url_for('homepage',ses=session))


@app.errorhandler(404)
def page_not_found(error):
    """
    redirection pour l'erreur 404.
    """
    return render_template('404.html'), 404



@app.route('/voie/<select>')
def voie(select):
    """
    Cette fonction permet de selectioner les voies indépendante
    """
    if 'mail' not in session :
        return redirect('login')

    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur : 
            cur.execute("select * from voie where idv=%s;", (select,))
            res=cur.fetchall()
            cur.execute("select * from siteesca where idse='%s';", (res[0][5],))
            sit=cur.fetchall()
            cur.execute("select * from localite where codepostal=%s;", (sit[0][2],))
            ville=cur.fetchall()
            cur.execute("select * from typevoie where idtv=%s;",(res[0][3],))
            typ=cur.fetchall()
            cur.execute("select * from debouchevers where idv1=%s;",(select,))
            suivant=cur.fetchall()
            namesuivant=[]
            for elem in suivant :
                cur.execute("select * from voie where idv=%s;",(elem[1],))
                namesuivant=cur.fetchall()
            cur.execute("select * from debouchevers where idv2=%s;",(select,))
            precedent=cur.fetchall()
            longueurs=len(suivant)
            longueurp=len(precedent)
            nameprecedent=[]
            for elem in precedent :
                cur.execute("select * from voie where idv=%s;",(elem[0],))
                nameprecedent=cur.fetchall()
    return render_template('voie.html', content=res,site=sit[0],ville=ville[0],typ=typ[0],
                           suivant=suivant,namesuivant=namesuivant,precedent=precedent,
                           nameprecedent=nameprecedent,longueurs=longueurs,
                           longueurp=longueurp)


@app.route("/propositions")
def propositions() :
    """
    ceci va afficher la table des propositions
    """
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute('select * from estguidede where mail= %s;', (session['mail'],))
            estguide=cur.fetchall()

            cur.execute("select * from proposition;")
            res=cur.fetchall()
            lst_nmbr_participant=[]
            lst_nom_site=[]
            for elem in res:
                cur.execute("select * from participe where idpropo=%s; ",(elem[0],))
                num=cur.fetchall()
                cur.execute("select * from siteesca where idse=%s;",(elem[6],))
                nom=cur.fetchall()
                lst_nom_site.append(nom[0])
                lst_nmbr_participant.append(len(num))
        length=len(res)
    return render_template(
        'propositions.html',
        content=res,
        nbr=lst_nmbr_participant,
        nom=lst_nom_site,
        length=length,
        estguide=estguide)


@app.route('/proposition/<select>',methods=['POST','GET'])
def proposition(select) :
    """
    ici on a l'affichage de la proposition
    """
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute("select * from proposition where idpropo=%s", (select,))
            res=cur.fetchall()
            res=res[0]
            cur.execute("select * from siteesca where idse=%s;",(res[6],))
            nom=cur.fetchall()
            nom[0]=nom
            cur.execute("select * from participe where idpropo=%s;",(res[0],))
            participant=cur.fetchall()
            num=len(participant)
            # for elem in participant :
            #     cur.execute("select * from utilisateur where mail=%s",(elem[0],))

            #     ...

    return render_template('proposition.html',content=res,nbr=num,nom=nom,participant=participant)


@app.route('/join/<select>')
def join(select) :
    """
    permet de faire en sorte que l'utilisateur join une cordée 
    """
    print(select)
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute("select * from proposition where idpropo=%s;", (select,))
            res=cur.fetchall()
            res=res[0]
            cur.execute("select * from participe where idpropo=%s;", (select,))
            participant=cur.fetchall()
            num=len(participant)
            if num<res[3] :
                cur.execute("insert into participe (mail,idpropo) values (%s,%s);",
                            (session['mail'],select,))
                conn.commit()
                return render_template('join-success.html')
        return render_template('join-failure.html')

@app.route("/<email>/<idpropo>")
def remove(email,idpropo) :
    """
    pour enlever un joueur
    """
    
    if 'mail' not in session :
        return redirect('login')
    with db.connect() as conn :
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
            cur.execute("select mail from proposition where idpropo=%s;", (idpropo,))
            mail=cur.fetchall()
            if session['mail']!=mail[0][0] :
                print(session['mail'],"%",mail[0][0],'%')
                return redirect(url_for('proposition',select=idpropo))
            cur.execute("delete from participe where mail=%s;",(email,))
        conn.commit()
    return redirect(url_for('proposition',select=idpropo))

@app.route("/createpropo", methods=['GET','POST'])
def create_propo() :
    """
    permet de créer une proposition si l'utilisateur est un guide
    """
    if 'mail' not in session :
        redirect('login')
    if request.method=="GET" :
        with db.connect() as conn :
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
                cur.execute('select * from estguidede where mail=%s;',(session['mail'],))
                estguide=cur.fetchall()
                if not estguide :
                    return redirect('page_not_found')
                cur.execute('select * from siteesca where codepostal=%s;',(estguide[0][1],))
                sit=cur.fetchall()
                cur.execute('select * from difficulte;')
                diff=cur.fetchall()
        return render_template('createpropo.html',sites=sit,diff=diff)
    
    if request.method=='POST' :
        sit= request.form.get('site')
        description=request.form.get('description')
        date=request.form.get('datep')
        nb_max=request.form.get('nb_max')
        diff=request.form.get('difficulte')
        with db.connect() as conn : 
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
                cur.execute('insert into proposition (description,datep,nb_max,mail,fr,idse) values(%s,%s,%s,%s,%s,%s);',
                            (description,date,nb_max,session['mail'],diff,sit,))
            conn.commit()
        return redirect('propositions')
        
    

@app.route("/test")

def test() :
    """C'est un test pour le nouveau template"""
    return render_template('home.html')


@app.route("/transfer/<select>", methods=['GET','POST'])
def transfer(select):
    """
    Cette fonction assurera le transfert des données vers le menu cordée
    """
    if 'mail' not in session :
        return redirect('login')
    if request.method=='GET' :
        with db.connect() as conn :
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
                cur.execute('select * from typeesca;')
                typesca=cur.fetchall()
                cur.execute('select * from proposition where idpropo=%s;',(select,))
                propo=cur.fetchall()
                propo=propo[0]
                cur.execute('select * from voie where idse=%s;',(propo[6],))
                v=cur.fetchall()
        return render_template('transfer.html',typesca=typesca,v=v)
    if request.method=='POST' :
        nom=request.form.get('nomcordee')
        v=request.form.get('voie')
        typeesca=request.form.get('typeesca')
        with db.connect() as conn :
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur :
                cur.execute('select * from proposition where idpropo=%s;',(select,))
                propo=cur.fetchall()
                propo=propo[0]
                cur.execute('select * from participe where idpropo=%s;',(select,))
                membres=cur.fetchall()
                cur.execute('insert into cordee (nomcordee) VALUES (%s) RETURNING idcordee;',(nom,))
                newid=cur.fetchall()
                newid=newid[0]
                for item in membres :
                    cur.execute('insert into partiec (idcordee,mail) VALUES (%s,%s);',
                                (newid[0],item[0]))
                cur.execute("insert into grimper (idte,idcordee,idv,dateg) VALUES (%s,%s,%s,%s);",
                            (typeesca,newid,v,propo[2]))
                cur.execute('delete from participe where idpropo=%s;',(select,))
                cur.execute("delete from proposition where idpropo=%s;",(select,))
                conn.commit()
        return redirect(url_for('cordees'))

if __name__ == "__main__" :
    app.run() 
