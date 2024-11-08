from marshmallow import Schema, fields, ValidationError
from datetime import datetime

# Custom validator for date-time strings (ISO 8601 format)
def validate_datetime(dt_string):
    try:
        datetime.fromisoformat(dt_string)
    except ValueError:
        raise ValidationError("Invalid date-time format. Expected ISO 8601 format.")

# Custom validator for type field (b2b or sme)
def validate_type(value):
    if value not in ['b2b', 'sme']:
        raise ValidationError("Invalid type. Expected 'b2b' or 'sme'.")

# Custom validator for progress field (received, surveyed, activated)
def validate_progress(value):
    if value not in ['received', 'surveyed', 'activated']:
        raise ValidationError("Invalid progress. Expected 'received', 'surveyed' or 'activated'.")

# Schema for FAT object
class FatSchema(Schema):
    fatId = fields.Str(required=True)
    port = fields.Str(required=True)
    opticalLevelAtFat = fields.Str(required=True)
    opticalLevelAtAtb = fields.Str(required=True)

# Schema for Pole objects
class PoleSchema(Schema):
    poleId = fields.Str(required=True)
    methods = fields.Str(required=True)
    image = fields.Str(required=True)

# Schema for Images object
class ImagesSchema(Schema):
    f1 = fields.Str(required=True)
    f7 = fields.Str(required=True)
    h1 = fields.Str(required=True)
    h11 = fields.Str(required=True)
    AN = fields.Str(required=True)

# Schema for DateTimes object
class DateTimesSchema(Schema):
    receivedDateTime = fields.Str(required=True, validate=validate_datetime)
    surveyOrderDateTime = fields.Str(required=True, validate=validate_datetime)
    surveyedDateTime = fields.Str(required=True, validate=validate_datetime)
    activationDateTime = fields.Str(required=True, validate=validate_datetime)

# Main schema for the JSON data
class DataSchema(Schema):
    id = fields.Str(required=True)
    siteId = fields.Str(required=True)
    customerId = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate_type)
    progress = fields.Str(required=True, validate=validate_progress)
    poles = fields.List(fields.Nested(PoleSchema), required=True)
    FAT = fields.Nested(FatSchema, required=True)
    images = fields.Nested(ImagesSchema, required=True)
    dateTimes = fields.Nested(DateTimesSchema, required=True)

# Sample JSON data for testing
# json_data = {
#     "id": "123",
#     "siteId": "site_001",
#     "customerId": "cust_123",
#     "type": "b2b",
#     "progress": "received",
#     "poles": [
#         {
#             "poleId": "pole_01",
#             "methods": "method_01",
#             "image": "image_01.jpg"
#         }
#     ],
#     "FAT": {
#         "fatId": "fat_01",
#         "port": "8080",
#         "opticalLevelAtFat": "level_1",
#         "opticalLevelAtAtb": "level_2"
#     },
#     "images": {
#         "f1": "image_f1.jpg",
#         "f7": "image_f7.jpg",
#         "h1": "image_h1.jpg",
#         "h11": "image_h11.jpg",
#         "AN": "image_AN.jpg"
#     },
#     "dateTimes": {
#         "receivedDateTime": "2024-11-08T12:00:00",
#         "surveyOrderDateTime": "2024-11-08T13:00:00",
#         "surveyedDateTime": "2024-11-08T14:00:00",
#         "activationDateTime": "2024-11-08T15:00:00"
#     }
# }

# Validate JSON data
# schema = DataSchema()
# try:
#     validated_data = schema.load(json_data)
#     print("Data is valid:", validated_data)
# except ValidationError as err:
#     print("Validation errors:", err.messages)
