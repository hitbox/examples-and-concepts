import json

from markupsafe import Markup

from .. import models
from ..html import Card
from ..html import List

from .htmlmodels import Draggable
from .htmlmodels import Dropzone

def pad_card(pad):
    return Card(
        header = pad.name,
        body = Dropzone(
            data = json.dumps({'id': pad.id}),
            list_name = 'trucks',
            # drop trucks onto pads
            types = ['truck'],
            children = map(draggable_truck, pad.trucks),
        ),
    )

def draggable_pad(pad):
    return Draggable(
        pad_card(pad),
        draggable_type = 'pad',
        draggable_data = json.dumps({'id': pad.id}),
    )

def draggable_worker(worker):
    return Draggable(
        Card(
            header = worker.name,
            body = worker.employee_number,
        ),
        draggable_type = 'worker',
        draggable_data = json.dumps({
            'id': worker.id,
        }),
    )

def _truck_operators_for_type(truck, operator_type):
    return (
        truck_operator.worker
        for truck_operator in truck.truck_operator_objects
        if truck_operator.operator_type == operator_type
    )

def _truck_operator_dropzone(truck, operator_type):
    """
    Dropzone for workers on trucks with associated operator_type.
    """
    return Dropzone(
        data = json.dumps({
            'operator_type': operator_type.value,
        }),
        types = [
            'worker',
        ],
        # draggables already dropped in this zone:
        children = map(
            draggable_worker,
            _truck_operators_for_type(
                truck,
                operator_type,
            ),
        ),
    )

def _get_truck_operator_cards(truck):
    """
    Card showing operator type and a dropzone to put workers; for each type of
    operator.
    """
    for operator_type in models.OperatorType:
        card = Card(
            header = operator_type.name.title(),
            body = _truck_operator_dropzone(
                truck,
                operator_type,
            )
        )
        yield card

def draggable_truck(truck):
    """
    Draggable truck with dropzones for operators by operator type.
    """
    return Draggable(
        Card(
            header = truck.name,
            # drop workers into operator dropzones by operator type
            body = List(
                html_list = _get_truck_operator_cards(truck),
                # RENAME data attribute name?
                data_list_name = 'operators',
            ),
        ),
        draggable_type = 'truck',
        draggable_data = json.dumps({'id': truck.id}),
    )

def dropzones_data(truck_operators_data):
    return dict(
        pads_dropzone = Dropzone(
            children = map(pad_card, truck_operators_data.pads),
            list_name = 'pads',
            types = ['pad'],
        ),
        trucks_dropzone = Dropzone(
            list_name = 'trucks',
            types = ['truck'],
            children = map(draggable_truck, truck_operators_data.trucks),
        ),
        workers_dropzone = Dropzone(
            list_name = 'workers',
            types = ['worker'],
            children = map(
                draggable_worker,
                truck_operators_data.workers,
            ),
        ),
    )

def load_truck_operator(data, session):
    worker = session.get(Worker, {'id': data['id']})
    operator_type = models.OperatorType(data['operator_type'])
    ident = dict(
        truck_id = truck_id,
        worker_id = data['worker_id'],
    )
    truck_operator = session.get(models.TruckOperator, ident)
    return truck_operator

def load_truck(data, session):
    truck = session.get(models.Truck, {'id': data['id']})
    truck.truck_operator_objects = [
        models.TruckOperator(
            worker = session.get(
                models.Worker,
                {
                    'id': operator_data['id'],
                }
            ),
            operator_type = models.OperatorType(
                operator_data['operator_type']
            ),
        )
        for operator_data in data['operators']
        if 'operator_type' in operator_data
        and 'id' in operator_data # worker_id
    ]
    return truck

def load_pad(data, session):
    ident = {'id': data['id']}
    pad = session.get(
        models.Pad,
        ident,
        execution_options = dict(
            no_autoflush = True,
        )
    )
    pad.trucks = [
        load_truck(truck_data, session)
        for truck_data in data['trucks']
    ]
    return pad

def dragdrop_load(data, session):
    """
    """
    # TODO
    # - move to class methods of the models?
    # - rename as `populate_` or something?
    pads = [load_pad(pad_data, session) for pad_data in data['pads']]
    trucks = [load_truck(truck_data, session) for truck_data in data['trucks']]
    # NOTE: workers have no nested relationships
