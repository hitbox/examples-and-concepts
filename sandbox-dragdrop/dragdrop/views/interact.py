import code

from pprint import pprint

import sqlalchemy as sa

from flask import Blueprint

from dragdrop import loaddata
from dragdrop.extensions import db
from dragdrop.models import OperatorType
from dragdrop.models import Pad
from dragdrop.models import Truck
from dragdrop.models import TruckOnPad
from dragdrop.models import TruckOperator
from dragdrop.models import Worker
from dragdrop.schema import dragdrop_schema
from dragdrop.schema import pad_schema
from dragdrop.schema import truck_on_pad_schema
from dragdrop.schema import truck_operator_schema
from dragdrop.schema import truck_schema
from dragdrop.schema import worker_schema

interact_bp = Blueprint('interact', __name__)

interact_bp.cli.help = 'Interactive shell'

MODELS = [
    Pad,
    Truck,
    TruckOnPad,
    TruckOperator,
    Worker,
]

SCHEMAS = [
    dragdrop_schema,
    pad_schema,
    truck_on_pad_schema,
    truck_operator_schema,
    truck_schema,
    worker_schema,
]

@interact_bp.cli.command()
def shell():
    """
    Interactive shell to test changing "nested" relations and saving to
    database.
    """
    # NOTES
    # - code.InteractiveConsole just keeps a reference to the dict passed in
    context = dict(
        (class_.__name__, class_) for class_ in MODELS
    )

    context['pprint'] = pprint

    context['db'] = db
    context['sa'] = sa

    context['OperatorType'] = OperatorType
    context['dragdrop_schema'] = dragdrop_schema
    context['pad_schema'] = pad_schema
    context['truck_on_pad_schema'] = truck_on_pad_schema
    context['truck_operator_schema'] = truck_operator_schema
    context['truck_schema'] = truck_schema
    context['worker_schema'] = worker_schema

    def load():
        context['trucks'] = loaddata.available_trucks()
        context['workers'] = loaddata.available_workers()
        context['pads'] = loaddata.available_pads()
        context['dragdrop'] = dict(
            trucks = context['trucks'],
            workers = context['workers'],
            pads = context['pads'],
        )

    load()
    context['load'] = load

    code.interact(local=context)
