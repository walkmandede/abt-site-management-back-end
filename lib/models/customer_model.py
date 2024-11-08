from marshmallow import Schema, fields, ValidationError
import re
import json

# Custom validator for location field (GeoJSON or CSV latLng)
def validate_location(location):
    # Check if location is a CSV lat,lng format (e.g., "12.3456,78.9101")
    if re.match(r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$', location):
        return
    # Check if location is in valid GeoJSON format (Point type)
    try:
        geojson = json.loads(location)
        if (
            isinstance(geojson, dict)
            and geojson.get("type") == "Point"
            and isinstance(geojson.get("coordinates"), list)
            and len(geojson["coordinates"]) == 2
            and all(isinstance(coord, (int, float)) for coord in geojson["coordinates"])
        ):
            return
    except (json.JSONDecodeError, TypeError):
        pass
    raise ValidationError("Invalid location format. Expected 'lat,lng' or GeoJSON Point.")

# Define the schema
class ModelSchema(Schema):
    circuitId = fields.Str(required=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    location = fields.Str(required=True, validate=validate_location)

# Sample JSON data for testing
# json_data = {
#     "id": "123",
#     "circuitId": "circuit_001",
#     "name": "John Doe",
#     "phone": "123-456-7890",
#     "address": "123 Main St",
#     "location": "12.3456,78.9101"  # or '{"type": "Point", "coordinates": [12.3456, 78.9101]}'
# }

# Validate JSON data
# schema = ModelSchema()
# try:
#     validated_data = schema.load(json_data)
#     print("Data is valid:", validated_data)
# except ValidationError as err:
#     print("Validation errors:", err.messages)
