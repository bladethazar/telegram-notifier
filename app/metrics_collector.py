import prometheus_client
from prometheus_client import Counter, Gauge
from prometheus_client.exposition import generate_latest


class MetricsCollector:
    def __init__(self):
        self.messages_sent_total = Counter('telegram_messages_sent_total', 'Total number of messages sent')
        self.photos_sent_total = Counter('telegram_photos_sent_total', 'Total number of photos sent')
        self.error_count_total = Counter('telegram_notifier_errors_total', 'Total number of errors occured in telegram-notifier')

    def increment_messages_sent(self):
        self.messages_sent_total.inc()

    def increment_photos_sent(self):
        self.photos_sent_total.inc()

    def increment_error_count(self):
        self.error_count_total.inc()

    @staticmethod
    def get_metrics():
        return generate_latest()


metrics_collector = MetricsCollector()
