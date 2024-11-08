from marshmallow import ValidationError

class AppUtils:

    @staticmethod
    def validate_schema(schema, json_data):
        print(schema)
        print(json_data)
        print("____+++)____+_+_")
        try:
            result = schema.load(json_data)
            return None
        except ValidationError as e:
            print("Validation error:", e.messages)  # Optional: Print error details
            return e.messages
