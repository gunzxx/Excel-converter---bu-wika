import webbrowser
from threading import Timer
from flask import Flask
from routes.home import home
from routes.bulanan import bulanan
from routes.tahunan import tahunan

app = Flask(__name__, template_folder="pages", static_folder="static")

app.register_blueprint(home)
app.register_blueprint(bulanan)
app.register_blueprint(tahunan)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    app.run()
    app.run(debug=True)