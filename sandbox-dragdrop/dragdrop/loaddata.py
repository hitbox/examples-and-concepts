from dragdrop import query
from dragdrop.extensions import db
from dragdrop.models import DragDrop

# common data loading functions

def available_pads():
    return db.session.scalars(query.available_pads()).all()

def available_trucks():
    return db.session.scalars(query.available_trucks()).all()

def available_workers():
    return db.session.scalars(query.available_workers()).all()

def get_dropzones_as_object():
    return DragDrop(
        pads = available_pads(),
        trucks = available_trucks(),
        workers = available_workers(),
    )
