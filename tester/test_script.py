import sys
import os
import requests

# get target host from environment, default to localhost
target_host = os.environ.get('TARGET_HOST', 'localhost')

try:
    # checking port 8080 : should return 200 or "Solved"
    url = f"http://{target_host}:8080/"
    print(f"Checking {url}")
    response = requests.get(url)
    
    if response.status_code != 200 or "Solved" not in response.text:
        print("Failed to confirm test on port 8080")
        sys.exit(1)
        
    # checking port 8081 : should return 500 error
    url = f"http://{target_host}:8081/"
    print(f"Checking {url}")
    response = requests.get(url)
    
    if response.status_code != 500:
        print("Failed to confrim error code on port 8081")
        sys.exit(1)

    print("Tests passed")
    sys.exit(0)

except requests.exceptions.RequestException as e:
    print(f"Error connecting to {target_host}: {e}")
    sys.exit(1)
    
    
