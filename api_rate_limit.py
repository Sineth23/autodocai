import time

class APIRateLimit:
    def __init__(self, max_requests, interval):
        self.max_requests = max_requests
        self.interval = interval
        self.request_count = 0
        self.last_request_time = 0

    def wait_for_next_request(self):
        current_time = time.time()
        if self.request_count >= self.max_requests:
            time_diff = current_time - self.last_request_time
            if time_diff < self.interval:
                time.sleep(self.interval - time_diff)
            self.request_count = 0
        self.last_request_time = current_time
        self.request_count += 1
