import threading
import queue
import time
import random

documentos = queue.Queue()

for i in range(1, 25):
    tamano = random.randint(1, 5)
    documentos.put((i, tamano))

registro = {
    "Andre Candia": 0,
    "Ricardo Siles": 0,
    "Arturo Figueredo": 0,
    "Pablo Medina": 0
}

candado = threading.Lock()
procesados = []

def trabajar(nombre):
    for i in range(6):
        try:
            numero, tamano = documentos.get_nowait()
        except queue.Empty:
            break

        print(f"[PROCESANDO] {nombre} ha tomado el Documento {numero} ({tamano} MB)")

        time.sleep(tamano * 0.1)

        with candado:
            registro[nombre] += 1
            procesados.append(numero)

        print(f"[COMPLETADO] {nombre} terminó el Documento {numero}")
        documentos.task_done()

hilos = []

for nombre in registro:
    hilo = threading.Thread(target=trabajar, args=(nombre,))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

print("\nResumen por trabajador:")
total = 0

for trabajador, cantidad in registro.items():
    print(f"{trabajador}: {cantidad} documentos")
    total += cantidad

print(f"\nTotal de documentos procesados: {total}")
print(f"Documentos únicos: {len(set(procesados))}")

if total == 24 and len(set(procesados)) == 24 and all(
    cantidad == 6 for cantidad in registro.values()
):
    print("VERIFICACIÓN EXITOSA: Cada trabajador procesó 6 documentos.")
else:
    print("ERROR: Revisar el procesamiento de documentos.")
