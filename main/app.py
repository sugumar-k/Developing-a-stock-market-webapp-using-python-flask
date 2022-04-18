from flask import Flask, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config["SECRET_KEY"]="thisissecretkey"
db = SQLAlchemy(app)

@app.route('/')
@app.route("/home")
def home():
    return render_template("base.html")

@app.route("/stocks")
def stocks_page():
    from models import Item
    items=Item.query.all()
    return render_template('stocks.html', items=items)

@app.route("/register",methods=['GET','POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    from form import RegisterForm
    from models import User
    form=RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                              email=form.email.data,                              
                              password=form.password.data)                    
        db.session.add(user)
        db.session.commit()
        flash("your account has been created ")
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


from flask_login import LoginManager
from flask_login import login_user,current_user,login_required,logout_user
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


@app.route("/login",methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
  
    
    from form import LoginForm
    from models import User
    form=LoginForm()
    if form.validate_on_submit():
       user=User.query.filter_by(username=form.username.data).first()
       if form.username.data==user.username and form.password.data==user.password:
            login_user(user,remember=True)
            flash("login successful","success")
            return redirect(url_for('stocks_page'))

    else:
        flash("login unsuccesful please check username and password","danger")
    return render_template("login.html",form=form)

@app.route('/account')
@login_required
def account_page(): 
    from models import User   
    items = User.query.all()
    return render_template('account.html', items=items)

@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home"))




if __name__ == '__main__':
    app.run(debug=True)