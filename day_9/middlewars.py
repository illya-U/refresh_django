import os
from pathlib import Path


class MyCustomLogger:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logs_file = os.path.join(Path(__file__).resolve().parent, "log.log")
        with open(logs_file, "a") as f:
            f.write(f"[LOGS]: {str(request)}\n")

        response = self.get_response(request)
        return response
