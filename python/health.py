import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event


from config import BE_SERVERS, HEALTH_CHECK_INTERVAL_SECONDS


def is_healthy(address):
    try:
        url = f"http://{address[0]}:{address[1]}"
        resp = requests.get(url, timeout=1)
    except Exception as e:
        print(f"Error occured checking health for {url}", e)
        return None

    if resp.status_code == 200:
        return address

    return None


def check_server_health(server_urls):

    healthy_servers = []

    with ThreadPoolExecutor(10) as pool:
        results = pool.map(is_healthy, server_urls)

        healthy_servers = [result for result in results if result]

    return healthy_servers


def start_health_check(server):
    print("Starting health check ...")

    def health_check_task(stop_event):
        while not stop_event.is_set():
            print("Getting healthy servers ...")
            healthy_servers = check_server_health(BE_SERVERS)
            print(f"Healthy servers count = {len(healthy_servers)}")

            # Update the server's backend servers
            with server.lock:
                server.be_servers = healthy_servers

            print("Sleeping for 10 seconds")
            stop_event.wait(
                HEALTH_CHECK_INTERVAL_SECONDS
            )  # Wait for x seconds or stop if the event is set

    # Stop event to gracefully terminate the thread
    server.stop_event = Event()

    # Run the health check task in a background thread
    thread = Thread(target=health_check_task, args=(server.stop_event,))
    thread.daemon = True
    thread.start()

    print("Health check thread started.")
