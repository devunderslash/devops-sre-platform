import requests
import json


class SimpleAPI:

    def __init__(self):
        self.api_key = "api_key"
        self.base_url = "https://api.simple.com/v1/"

    def get_data(self, endpoint):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
    def post_data(self, endpoint, data):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(f"{self.base_url}{endpoint}", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def main(self):
        # Example usage
        data = {"key": "value"}  # Replace with actual data
        try:
            endpoint = "example/endpoint"  # Replace with actual endpoint
            data = self.post_data(endpoint, data)  # Replace with actual data
            print("Data posted successfully:", data)
        except Exception as e:
            print(f"An error occurred: {e}")
            
if __name__ == "__main__":
    classCall = SimpleAPI()
    classCall.main()

