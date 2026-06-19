class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.request_count_since_last_log = 0

    def __call__(self, request):
        response = self.get_response(request)
        
        self.total_requests += 1
        self.request_count_since_last_log += 1
        
        status_code = response.status_code
        if 200 <= status_code < 300:
            self.status_2xx += 1
        elif 400 <= status_code < 500:
            self.status_4xx += 1
        elif 500 <= status_code < 600:
            self.status_5xx += 1
        
        # Выводим статистику каждые 5 запросов
        if self.request_count_since_last_log >= 5:
            self._log_metrics()
            self.request_count_since_last_log = 0
        
        return response

    def _log_metrics(self):
        print("МЕТРИКИ ЗАПРОСОВ")
        print(f"Всего запросов: {self.total_requests}")
        print(f"2xx (успешные): {self.status_2xx}")
        print(f"4xx (ошибки клиента): {self.status_4xx}")
        print(f"5xx (ошибки сервера): {self.status_5xx}")
        
        with open('metrics.log', 'a', encoding='utf-8') as f:
            f.write(f"Total: {self.total_requests}, 2xx: {self.status_2xx}, 4xx: {self.status_4xx}, 5xx: {self.status_5xx}\n")