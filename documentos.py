import threading
import time

documentos = []
for i in range(1, 25):
    documento = f"Documento {i}"
    documentos.append(documento)

registro = {
    "Andre Candia": 0,
    "Ricardo Siles": 0,
    "Arturo Figueredo": 0,
    "Pablo Medina": 0
}

candado = threading.Lock()

def trabajar(nombre):
    while True:
        candado.acquire()

        if len(documentos) == 0:
            candado.release()
            break

        documento = documentos.pop(0)
        registro[nombre] += 1
        
        print(f"[PROCESANDO] {nombre} ha tomado el {documento}")

        candado.release()
        time.sleep(0.1)

hilos = []
for i in range(4):
    nombre = list(registro.keys())[i]
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
print(f"Total de documentos procesados: {total}")