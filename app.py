from flask import Flask
app = Flask(__name__)


@app.route('/')
def main_page():
    '''
    when define home page in this function
    '''
    return "Hello World"
