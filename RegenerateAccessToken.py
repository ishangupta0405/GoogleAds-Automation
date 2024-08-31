# Endpoint to refresh the access token
import requests


refresh_token_url = 'https://oauth2.googleapis.com/token'

# Data to send in the request
refresh_data = {
    'client_id': '76833370957-of0n583mj63utomv6h4brop2i9nh6f2s.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//0gTvykwN_4NQrCgYIARAAGBASNwF-L9IrEEsF8z-ycLEH7itryHLV5nCNYLfkaf-0wWd0kUG7AoNHLuO1aMjDTeZmyenG_bKI1co',
    'grant_type': 'refresh_token',
}

# Make the request
refresh_response = requests.post(refresh_token_url, data=refresh_data)

# Parse the response
new_tokens = refresh_response.json()
new_access_token = new_tokens['access_token']

print(f"New Access Token: {new_access_token}")
