import json

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from dragdrop import loaddata
from dragdrop.dragdrop import dragdrop_load
from dragdrop.dragdrop import dropzones_data
from dragdrop.extensions import db
from dragdrop.forms import DragDropForm

main_bp = Blueprint('main', __name__)

def boolstring(s):
    # try for integer-like boolean
    try:
        n = int(s)
    except ValueError:
        pass
    else:
        return bool(n)
    # try common words' first letters
    if s.lower() in ('false', 'no', 'true', 'yes') or len(s) == 1:
        return bool(s.lower()[0:1] in 'ty')

@main_bp.route('/')
def index():
    return redirect(url_for('.dragdrop'))

@main_bp.route('/dragdrop', methods=['GET', 'POST'])
def dragdrop():

    form = DragDropForm(data=request.form)

    if request.method == 'POST' and form.validate():
        data = json.loads(form.dragdrop_json.data)
        dragdrop_load(data, db.session)
        db.session.commit()
        return redirect(url_for(request.endpoint))

    truck_operators_data = loaddata.get_dropzones_as_object()
    context = dict(
        form = form,
    )

    if boolstring(request.args.get('custom', '')):
        # TODO
        # - optional use custom html elements
        raise NotImplementedError
    else:
        dropzones_data = dropzones_data(truck_operators_data)

    context.update(dropzones_data)
    return render_template('dragdrop.html', **context)
