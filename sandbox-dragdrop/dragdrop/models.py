from operator import attrgetter

import sqlalchemy as sa
import sqlalchemy.orm

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_utils import ChoiceType

from dataclasses import KW_ONLY
from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List

from .extensions import db

class OperatorType(Enum):
    """
    The type of operator a worker is performning on a truck.
    """
    # NOTE
    # - for each of these, there needs to be an association table with the
    #   trucks
    DRIVER = auto()
    BUCKET = auto()


class Pad(db.Model):
    """
    A pad trucks operate on.
    """
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String)

    truck_on_pad_objects = sa.orm.relationship(
        'TruckOnPad',
        back_populates = 'pad',
        cascade = 'all, delete-orphan',
    )

    trucks = association_proxy(
        'truck_on_pad_objects',
        'truck',
        creator = lambda truck: TruckOnPad(truck=truck),
    )


class Truck(db.Model):
    """
    A truck.
    """
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String)

    truck_on_pad_objects = sa.orm.relationship(
        'TruckOnPad',
        back_populates = 'truck',
        cascade = 'all, delete-orphan',
    )

    truck_operator_objects = sa.orm.relationship(
        'TruckOperator',
        back_populates = 'truck',
        cascade = 'all, delete-orphan',
    )

    operators = association_proxy(
        'truck_operator_objects',
        'worker',
        creator = lambda worker_and_type: TruckOperator(
                worker = worker_and_type[0],
                operator_type = worker_and_type[1],
            ),
    )


class TruckOnPad(db.Model):
    """
    A truck on a pad association object.
    """
    truck_id = sa.Column(
        sa.ForeignKey('truck.id'),
        primary_key = True,
    )
    pad_id = sa.Column(
        sa.ForeignKey('pad.id'),
        primary_key = True,
    )

    truck = sa.orm.relationship(
        'Truck',
        back_populates = 'truck_on_pad_objects',
    )

    pad = sa.orm.relationship(
        'Pad',
        back_populates = 'truck_on_pad_objects',
    )


class TruckOperator(db.Model):
    """
    A worker operating a truck and the job they're performing.
    """

    truck_id = sa.Column(
        sa.ForeignKey(
            'truck.id',
        ),
        primary_key = True,
    )

    truck = sa.orm.relationship(
        'Truck',
        back_populates = 'truck_operator_objects',
    )

    worker_id = sa.Column(
        sa.ForeignKey(
            'worker.id',
        ),
        primary_key = True,
    )

    worker = sa.orm.relationship(
        'Worker',
    )

    operator_type = sa.Column(
        ChoiceType(
            OperatorType,
            impl = sa.Integer(),
        ),
        sa.CheckConstraint(
            f'operator_type IN {tuple(map(attrgetter("value"), OperatorType))}',
        ),
    )


class Worker(db.Model):
    """
    A person working.
    """
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    employee_number = sa.Column(sa.String)


@dataclass
class DragDrop:
    _: KW_ONLY
    pads: List[Pad]
    trucks: List[Truck]
    workers: List[Worker]
