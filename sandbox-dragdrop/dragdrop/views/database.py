from pprint import pprint

import click
import sqlalchemy as sa

from flask import Blueprint

from dragdrop import initdata as _initdata
from dragdrop.extensions import db
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

database_bp = Blueprint('db', __name__)

database_bp.cli.help = 'Database utilities'

@database_bp.cli.command()
def create_all():
    """
    Create database objects.
    """
    db.create_all()

@database_bp.cli.command()
def initdata():
    """
    Initialize database data.
    """
    _initdata.init_all(10)
    db.session.commit()

MODEL_SCHEMA = [
    (Truck, truck_schema),
    (Pad, pad_schema),
    (Worker, worker_schema),
    (TruckOnPad, truck_on_pad_schema),
    (TruckOperator, truck_operator_schema),
]

ALL = 'all'

def lowerclassname(cls):
    return cls.__name__.lower()

@database_bp.cli.command()
@click.argument(
    'typename',
    default = ALL,
    type = click.Choice(
        [lowerclassname(model_class) for model_class, _ in MODEL_SCHEMA] + [ALL],
    ),
)
def dump_schema(typename):
    """
    Load objects from database and dump their data.
    """
    if typename != ALL:
        def predicate(model_class, schema):
            return lowerclassname(model_class) == typename
    else:
        def predicate(model_class, schema):
            return True

    model_schema = [
        (model_class, schema)
        for model_class, schema in MODEL_SCHEMA
        if predicate(model_class, schema)
    ]

    for model_class, schema in model_schema:
        instances = db.session.scalars(sa.select(model_class))
        data = schema.dump(instances, many=True)
        print(model_class.__name__)
        pprint(data)
