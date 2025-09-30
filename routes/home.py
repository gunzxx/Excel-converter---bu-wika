from flask import Blueprint, render_template, current_app
from pathlib import Path
from datetime import datetime

home = Blueprint('home', __name__)

@home.route('/')
def home_get():
    folderStatic = Path(current_app.static_folder)/'output/bulanan'
    results = [f.name for f in folderStatic.glob('*.xlsx')]
    reports = [
        [
            report,
            datetime.fromtimestamp(float(report[:-5])).strftime("%d-%m-%Y %H:%M:%S")
        ]
        for report in results
    ]
    reports.reverse()

    return render_template('bulanan.html', reports=reports)