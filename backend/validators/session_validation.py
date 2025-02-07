from datetime import datetime

class SessionValidation:
    @staticmethod
    def validate(data):
        errors = []

        # Validate and convert datetime
        try:
            data['datetime'] = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M')
        except ValueError:
            errors.append("Invalid date format for datetime. Expected format: yyyy-mm-dd HH:MM")

        # Add more validations as needed
        if not isinstance(data['location'], str):
            errors.append("Invalid type for location. Expected str")

        return errors, data
