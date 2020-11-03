from pathlib import Path

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    fig_names = Path('plotly_window/templates/figs').glob('*.html')
    fig_names = sorted(['figs/' + p.name for p in fig_names])
    return render_template('plots.html', fig_names=fig_names)


if __name__ == '__main__':
    app.run(debug=True)
