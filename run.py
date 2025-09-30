from function.core import checkModules
modules = ['pdfplumber', 'pandas', 'flask', 'waitress']
checkModules(modules)

from webbrowser import open_new
from threading import Thread
from waitress import serve
from app import app

def open_browser():
    open_new("http://localhost")

if __name__ == "__main__":
    Thread(target=open_browser).start()
    serve(app, host="0.0.0.0", port=80)
