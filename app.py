from flask import Flask
from routes.home import home
from routes.bulanan import bulanan
from routes.compress import compress

app = Flask(__name__, template_folder="pages", static_folder="static")

app.register_blueprint(home)
app.register_blueprint(bulanan)
# app.register_blueprint(tahunan)
app.register_blueprint(compress)

if __name__ == "__main__":
    # Timer(1.5, open_browser).start()
    # app.run(debug=False)
    app.run(debug=True) # debug digunakan untuk mengaktifkan reloader dan mengaktifkan log terminal
    # open_browser()