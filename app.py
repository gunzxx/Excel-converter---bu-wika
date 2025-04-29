from flask import Flask
from routes.home import home
from routes.bulanan import bulanan
from routes.tahunan import tahunan

app = Flask(__name__, template_folder="pages", static_folder="static")

app.register_blueprint(home)
app.register_blueprint(bulanan)
app.register_blueprint(tahunan)

if __name__ == "__main__":
    app.run(debug=True)