from flask import Flask
from flask import render_template

from pagetabs import PageTabs

app = Flask(__name__)

@app.route('/')
def index():
    """
    Demo page tabs
    """
    choices = [(f'tab-{index}', f'Tab {index+1}') for index in range(3)]
    pagetabs = PageTabs(choices)
    context = dict(
        pagetabs = pagetabs,
    )
    return render_template('pagetabs.html', **context)
