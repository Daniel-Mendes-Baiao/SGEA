# ipc.py
def enviar_tarefa(fila, msg):
    fila.put(msg)

def receber_resposta(fila, block=False, timeout=0.01):
    try:
        return fila.get(block=block, timeout=timeout)
    except:
        return None
