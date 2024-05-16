from marshmallow import Schema, ValidationError, fields

class TaskSchema(Schema):
    name = fields.Bool(required=True, error_messages={ 'required': 'Name is required' })
    description = fields.Bool(required=True, error_messages={ 'required': 'Description is required' })