
class TeamValidation:
    @staticmethod
    def validate(data):
        errors = []

        if not isinstance(data['name'], str):
            errors.append("Invalid type for name. Expected str")

        if not isinstance(data['league'], str):
            errors.append("Invalid type for league. Expected str")

        if not isinstance(data['manager'], str):
            errors.append("Invalid type for manager. Expected str")

        if not isinstance(data['coach'], str):
            errors.append("Invalid type for coach. Expected str")

        if not isinstance(data['players'], list):
            errors.append("Invalid type for players. Expected list")

        return errors, data
