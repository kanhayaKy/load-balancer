from strategy import RoundRobinStrategy

BE_SERVERS = [
    ("localhost", 8000),
    ("localhost", 8001),
    ("localhost", 8002),
]


SELECTION_STRATEGY = RoundRobinStrategy

HEALTH_CHECK_INTERVAL_SECONDS = 10
