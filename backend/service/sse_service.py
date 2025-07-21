class SseService:
    def __init__(self):
        self.subscribers = []  # Global list to track SSE clients

    def sse_send_to_all(self, message: str):
        dead_clients = []

        for messages, event in self.subscribers:
            try:
                messages.append(message)
                event.set()
            except Exception:
                dead_clients.append((messages, event))

        for client in dead_clients:
            self.subscribers.remove(client)