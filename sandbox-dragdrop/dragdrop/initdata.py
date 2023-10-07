from .extensions import db
from .models import Pad
from .models import Truck
from .models import Worker

def init_workers(num):
    for id_ in range(num):
        worker = Worker(
            id = id_,
            name = f'worker-{id_}',
            employee_number = f'#{id_*200:05d}',
        )
        db.session.add(worker)

def init_trucks(num):
    for id_ in range(num//2):
        truck = Truck(
            id = id_,
            name = f'truck-{id_}',
        )
        db.session.add(truck)

def init_pads(num):
    for id_ in range(num//2):
        pad = Pad(
            id = id_,
            name = f'pad-{id_}',
        )
        db.session.add(pad)

def init_all(num):
    init_workers(num)
    init_trucks(num)
    init_pads(num)
