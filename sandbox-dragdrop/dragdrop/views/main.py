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
    context.update(
        dropzones_data(truck_operators_data)
    )
    return render_template('dragdrop.html', **context)
