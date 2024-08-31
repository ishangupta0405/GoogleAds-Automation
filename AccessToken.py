import webbrowser
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

# Your credentials
client_id = '76833370957-of0n583mj63utomv6h4brop2i9nh6f2s.apps.googleusercontent.com'
client_secret = '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'
redirect_uri = 'http://localhost:8080'  # Local server to capture the redirect

# Step 1: Construct the Authorization URL
auth_url = (
    'https://accounts.google.com/o/oauth2/v2/auth'
    '?response_type=code'
    f'&client_id={client_id}'
    f'&redirect_uri={redirect_uri}'
    '&scope=https://www.googleapis.com/auth/adwords'
    '&access_type=offline'
)

# print(auth_url)

# Step 2: Open the authorization URL in the user's browser
print("Opening the authorization URL in the browser...")
webbrowser.open(auth_url)

# Step 3: Set up a local server to capture the authorization code

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL to get the authorization code
        parsed_url = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_url.query)
        auth_code = query_params.get('code', None)
        
        if auth_code:
            auth_code = auth_code[0]
            print(f"Authorization code received: {auth_code}")
            # Exchange the authorization code for tokens
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'code': auth_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }
            response = requests.post(token_url, data=token_data)
            tokens = response.json()
            access_token = tokens['access_token']
            refresh_token = tokens['refresh_token']
            
            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")
            
            # Respond to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization complete. You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization code not found.")

# Start the server to listen for the redirect
server_address = ('', 8080)
httpd = HTTPServer(server_address, OAuthHandler)
print('Waiting for authorization response...')
httpd.handle_request()
