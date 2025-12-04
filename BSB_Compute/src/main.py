# main.py
import json
import os
import time
import random
from multiprocessing import Process, Queue

from scheduler import Scheduler
from worker import worker_loop
from ipc import enviar_tarefa, receber_resposta
from utils import ts


def carregar_config():
    base = os.path.dirname(os.path.abspath(__file__))
    cfg = os.path.join(base, "..", "config.json")
    cfg = os.path.abspath(cfg)

    with open(cfg, "r") as f:
        return json.load(f)


def iniciar_workers(servidores):
    filas = {}
    processos = []
    retorno = Queue()

    for s in servidores:
        q = Queue()
        filas[s["id"]] = q
        p = Process(target=worker_loop, args=(s["id"], s["capacidade"], q, retorno))
        p.start()
        processos.append(p)

    return filas, retorno, processos


def servidor_disponivel(estados):
    for sid, st in estados.items():
        for i in range(len(st["slots"])):
            if st["slots"][i] is None:
                return sid, i
    return None, None


def executar(policy, config):

    print("\n" + "=" * 60)
    print(f"=== INICIANDO SIMULAÇÃO: {policy.upper()} ===")
    print("=" * 60)

    start = time.time()

    tarefas = []
    for req in config["requisicoes"]:
        tarefas.append({
            "id": req["id"],
            "prioridade": req["prioridade"],
            "remaining": req["tempo_exec"],
            "arrival": random.uniform(0.1, 1.2),
            "state": "NEW",

            "t_arrival": None,
            "t_start": None,
            "t_finish": None
        })

    servidores = config["servidores"]

    estados = {
        s["id"]: {
            "cap": s["capacidade"],
            "slots": [None] * s["capacidade"],
            "busy": 0
        }
        for s in servidores
    }

    filas, retorno, procs = iniciar_workers(servidores)

    scheduler = Scheduler(policy)
    quantum = config["quantum"]

    fila_global = []

    # ========================= LOOP PRINCIPAL ==========================
    while True:
        elapsed = time.time() - start

        # LIBERA CHEGADA
        for t in tarefas:
            if t["state"] == "NEW" and elapsed >= t["arrival"]:
                t["state"] = "READY"
                t["t_arrival"] = elapsed
                fila_global.append(t)

                pr_txt = {1: "Alta", 2: "Média", 3: "Baixa"}[t["prioridade"]]
                print(f"{ts(start)} Requisição {t['id']} ({pr_txt}) entrou na fila")

        # ORDENAR FILA PELA POLÍTICA
        scheduler.reorder(fila_global)

        # DESPACHAR SE HOUVER SLOT LIVRE
        sid, slot = servidor_disponivel(estados)
        while sid is not None and fila_global:

            t = scheduler.next_task(fila_global)

            if t["t_start"] is None:
                t["t_start"] = elapsed

            enviar_tarefa(filas[sid], {
                "id": t["id"],
                "remaining": t["remaining"],
                "slice": min(quantum, t["remaining"])
            })

            estados[sid]["slots"][slot] = t["id"]
            t["state"] = "RUNNING"
            t["server"] = sid

            pr_txt = {1: "Alta", 2: "Média", 3: "Baixa"}[t["prioridade"]]
            print(f"{ts(start)} Requisição {t['id']} ({pr_txt}) atribuída ao Servidor {sid} (slot {slot})")

            sid, slot = servidor_disponivel(estados)

        # RECEBER RESULTADOS DO WORKER
        while True:
            resp = receber_resposta(retorno)
            if not resp:
                break

            tid = resp["id"]
            sid = resp["worker"]
            duration = resp["duration"]

            t = next(x for x in tarefas if x["id"] == tid)

            estados[sid]["busy"] += duration

            slot_index = estados[sid]["slots"].index(tid)
            estados[sid]["slots"][slot_index] = None

            t["remaining"] = resp["remaining"]

            if t["remaining"] == 0:
                t["state"] = "DONE"
                t["t_finish"] = time.time() - start
                print(f"{ts(start)} Servidor {sid} concluiu Requisição {tid}")
            else:
                t["state"] = "READY"
                fila_global.append(t)

        if all(t["state"] == "DONE" for t in tarefas):
            break

        time.sleep(0.02)

    # ========================= MÉTRICAS ==============================
    total_time = time.time() - start

    tempos_resposta = [(t["t_finish"] - t["t_arrival"]) for t in tarefas]
    tempo_medio = sum(tempos_resposta) / len(tempos_resposta)

    throughput = len(tarefas) / total_time

    utilizacao = (
        sum(st["busy"] for st in estados.values()) /
        (total_time * len(estados)) * 100
    )

    print("\n" + "-" * 60)
    print("Resumo Final:")
    print(f"Tempo médio de resposta: {tempo_medio:.2f}s")
    print(f"Utilização média da CPU: {utilizacao:.1f}%")
    print(f"Throughput: {throughput:.2f} tarefas/segundo")
    print("-" * 60)

    for q in filas.values():
        q.put("EXIT")
    for p in procs:
        p.join()


if __name__ == "__main__":
    cfg = carregar_config()
    executar("rr", cfg)
