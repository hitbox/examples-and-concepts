import marshmallow as ma
import marshmallow_sqlalchemy as masql

from dragdrop import models

class PadSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Pad
        include_relationships = True
        load_instance = True


class TruckSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Truck
        load_instance = True

    operators = masql.fields.RelatedList(
        masql.fields.Nested(
            'WorkerSchema',
            only = [
                'id',
            ],
        )
    )


class TruckOnPadSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = models.TruckOnPad
        include_relationships = True
        load_instance = True


class TruckOperatorSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = models.TruckOperator
        include_relationships = True
        load_instance = True

    operator_type = ma.fields.Enum(
        models.OperatorType,
    )


class WorkerSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Worker
        load_instance = True


class DragDropSchema(masql.SQLAlchemySchema):
    # NOTES
    # - needs to be marshmallow_sqlalchemy subclass to pass the session onto fields.
    class Meta:
        load_instance = True

    pads = ma.fields.List(ma.fields.Nested(PadSchema))
    trucks = ma.fields.List(ma.fields.Nested(TruckSchema))
    workers = ma.fields.List(ma.fields.Nested(WorkerSchema))


dragdrop_schema = DragDropSchema()
pad_schema = PadSchema()
truck_on_pad_schema = TruckOnPadSchema()
truck_operator_schema = TruckOperatorSchema()
truck_schema = TruckSchema()
worker_schema = WorkerSchema()
