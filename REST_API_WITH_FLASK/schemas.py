from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=1, max=100))
    price = fields.Float(required=True, validate=Range(min=0))


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=1, max=80))


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), required=False)  # Sin dump_only para aceptar input
    tags = fields.List(fields.Nested(PlainTagSchema()), required=False)   # Sin dump_only para aceptar input


class TagSchema(PlainTagSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagUpdateSchema(Schema):
    name = fields.Str(validate=Length(min=1, max=80))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
