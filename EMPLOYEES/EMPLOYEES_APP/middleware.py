import time
from datetime import datetime

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.requests_2xx = 0
        self.requests_4xx = 0
        self.requests_5xx = 0

    def __call__(self, request):
        self.total_requests += 1
        response = self.get_response(request)
        
        status_code = response.status_code
        
        if 200 <= status_code < 300:
            self.requests_2xx += 1
        elif 400 <= status_code < 500:
            self.requests_4xx += 1
        elif 500 <= status_code < 600:
            self.requests_5xx += 1
        
        # Вывод в консоль
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = (
            f"[{timestamp}] "
            f"Total: {self.total_requests}, "
            f"2xx: {self.requests_2xx}, "
            f"4xx: {self.requests_4xx}, "
            f"5xx: {self.requests_5xx}, "
            f"Path: {request.path}, "
            f"Status: {status_code}"
        )
        print(log_message)
        
        # Запись в файл metrics.log
        with open('metrics.log', 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
        
        return response