import requests
import time
import numpy as np
import subprocess


def start_server():
    server = subprocess.Popen(["python", "server.py"])
    time.sleep(2)
    return server

def stop_server(server):
    server.terminate()

def run_performance_test(endpoint, duration):
    start_time = time.time()
    end_time = start_time + duration
    response_times = []

    while time.time() < end_time:
        start_request = time.time()
        response = requests.get(f'http://localhost:8090/{endpoint}/1/')
        end_request = time.time()

        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            continue

        response_times.append(end_request - start_request)

    return response_times


if __name__ == "__main__":
    server = start_server()
    duration = 60
    endpoint = "people"
    print("Starting performance test...")
    response_times = run_performance_test(endpoint, duration)
    stop_server(server)

    mean = np.mean(response_times)
    std_dev = np.std(response_times)

    print(f"\nResults for endpoint: /{endpoint}/1/")
    print(f"Mean response time: {mean:.4f} seconds")
    print(f"Standard deviation: {std_dev:.4f} seconds")