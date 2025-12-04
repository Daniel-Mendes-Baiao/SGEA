# worker.py
import time
import random

def worker_loop(wid, capacidade, inbox, retorno):
    """
    Worker processa fatias (time slice).
    'capacidade' influencia a velocidade: cada slot é processado normalmente,
    mas servidores mais fortes executam a slice mais rapidamente.
    """
    while True:
        msg = inbox.get()
        if msg == "EXIT":
            break

        task_id = msg["id"]
        slice_amount = msg["slice"]
        remaining = msg["remaining"]

        # velocidade aumenta conforme capacidade
        exec_time = slice_amount / capacidade

        time.sleep(exec_time)

        new_remaining = max(0, remaining - slice_amount)

        retorno.put({
            "worker": wid,
            "id": task_id,
            "remaining": new_remaining,
            "duration": exec_time,
            "cpu": random.uniform(40, 95),
            "memory": random.uniform(500, 1500)
        })
