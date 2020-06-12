import os
from flask import (
    Flask,
    Response,
    redirect,
    url_for,
    request,
    session,
    abort,
    flash,
    render_template
    )
from flask_login import (
    LoginManager,
    current_user,
    UserMixin,
    login_required,
    login_user,
    logout_user
    )
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per day", "10 per hour"]
)

UPLOAD_FOLDER = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# config
app.config.update(
    DEBUG=True,
    SECRET_KEY=config.SECRET_KEY
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("6 per minute")
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == config.PASSWORD and username == config.USERNAME:
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect('/')
        else:
            return abort(401)
    else:
        return render_template('login.html')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    """ logout the admin user"""
    logout_user()
    flash('Logged out', 'success')
    return redirect('/login')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    """ Show error login fail"""
    flash('Login failed', 'danger')
    return redirect('/login')

# handle page not found failed


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# callback to reload the user object


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/', methods=['GET', 'POST'])
@login_required
def main_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash(f'file {file_path} uploaded')
            os.remove(file_path)
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    """when define home page in this function."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
