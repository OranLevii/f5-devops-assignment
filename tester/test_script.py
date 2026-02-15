import sys
import os
import requests
import time
import threading

# get target host from environment, default to localhost
target_host = os.environ.get('TARGET_HOST', 'localhost')

print("Waiting 3s for Nginx to initialize SSL...")
time.sleep(3)

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

    url = f"https://{target_host}/"
    print(f"Checking {url}")
    response = requests.get(url, verify=False)  # ignore self signed cert warning

    if response.status_code != 200:
        print("Failed to confirm SSL test on port 443")
        sys.exit(1)


    # rate limit test
    print("Testing rate limiting on {target_host}:8080")
    # store status codes from threads
    results = [] 
    #function that each thread will run
    def attack():
        try:
            r = requests.get(f"http://{target_host}:8080/")
            results.append(r.status_code)
        except:
            pass # ignores failed requests

    # creates 20 threads that run the attack function
    threads = [threading.Thread(target=attack) for _ in range(20)]

    # start all threads
    for t in threads: t.start()

    # wait for all threads to finish
    for t in threads: t.join()

    blocked_count = results.count(429)
    success_count = results.count(200)

    if blocked_count > 0:
        print("Rate limit verified")
    else:
        print("Rate limit not triggered")
        

    print("Tests passed")
    sys.exit(0)

except requests.exceptions.RequestException as e:
    print(f"Error connecting to {target_host}: {e}")
    sys.exit(1)
    
    
