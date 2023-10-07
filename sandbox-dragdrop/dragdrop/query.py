import sqlalchemy as sa

from .models import Pad
from .models import Truck
from .models import TruckOnPad
from .models import TruckOperator
from .models import Worker

def available_workers():
    """
    Workers not operating a truck.
    """
    query = sa.select(
        Worker,
    ).where(
        Worker.id.not_in(
            sa.select(TruckOperator.worker_id),
        ),
    )
    return query

def available_trucks():
    """
    Trucks not already on a pad.
    """
    query = sa.select(
        Truck,
    ).where(
        Truck.id.not_in(
            sa.select(TruckOnPad.truck_id),
        ),
    )
    return query

def available_pads():
    # just all over them but in the actual app there will be unavailable
    query = sa.select(Pad)
    return query
