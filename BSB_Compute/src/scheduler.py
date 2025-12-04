# scheduler.py
class Scheduler:
    def __init__(self, policy):
        self.policy = policy.lower()

    def reorder(self, ready):
        if self.policy == "prioridade":
            ready.sort(key=lambda x: x["prioridade"])  # 1 = alta
        elif self.policy == "sjf":
            ready.sort(key=lambda x: x["remaining"])   # menor job primeiro
        # Round Robin não reordena

    def next_task(self, ready):
        if not ready:
            return None

        if self.policy == "rr":
            t = ready.pop(0)
            return t
        else:
            return ready.pop(0)
