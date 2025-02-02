from datetime import datetime

class PlayerValidation:
    @staticmethod
    def validate(data):
        errors = []

        # Validate and convert dob
        try:
            data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date format for dob. Expected format: yyyy-mm-dd")

        # Validate and convert joined_group_date
        try:
            data['joined_group_date'] = datetime.strptime(data['joined_group_date'], '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date format for joined_group_date. Expected format: yyyy-mm-dd")

        # Add more validations as needed
        if not isinstance(data['id'], int):
            errors.append("Invalid type for id. Expected int")

        if not isinstance(data['name'], str):
            errors.append("Invalid type for name. Expected str")

        return errors, data