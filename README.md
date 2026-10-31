## Interpretación de los resultados por trabajador

El programa utiliza cuatro hilos que representan a Andre Candia, Ricardo Siles, Arturo Figueredo y Pablo Medina. Cada trabajador procesa exactamente 6 documentos de una cola compartida queue.Queue, completando los 24 documentos solicitados. El programa utiliza threading.Lock() para proteger la actualización del registro compartido y join() para esperar a que todos los trabajadores finalicen. Aunque el orden de procesamiento puede variar debido a la concurrencia, cada trabajador siempre completa 6 documentos. Finalmente, el programa verifica que los 24 documentos fueron procesados una sola vez, sin duplicados.

## Preguntas de análisis

### 1. ¿Por qué `queue.Queue` es apropiada para compartir trabajos?

queue.Queue es apropiada porque permite que los cuatro hilos compartan los documentos de manera segura y ordenada. En mi programa cargamos 24 documentos mediante put() y cada trabajador retira los suyos con get_nowait(). La cola evita que dos trabajadores obtengan el mismo documento, sin necesitar un Lock adicional para retirarlo. Además, usamos un ciclo for de 6 iteraciones por trabajador para garantizar que Andre, Ricardo, Arturo y Pablo procesen exactamente 6 documentos cada uno, sumando los 24. Después de terminar cada documento, llamamos a task_done() para marcar su procesamiento como finalizado.

### 2. ¿Qué protege `Lock` y qué pasaría si se actualizara el resumen sin él?

En mi código, `threading.Lock()` protege la sección donde los trabajadores acceden a la lista de documentos y actualizan el diccionario `registro`. Cuando un trabajador ejecuta `candado.acquire()`, obtiene el permiso para acceder a los datos compartidos. Después de retirar un documento y actualizar su contador, ejecuta `candado.release()` para permitir que otro hilo continúe. Esto evita que varios trabajadores modifiquen los datos compartidos al mismo tiempo.

Si no utilizáramos `Lock`, podrían producirse condiciones de carrera, especialmente si varios hilos intentaran consultar y modificar la lista simultáneamente. También podrían existir problemas de actualización de contadores compartidos, dependiendo de cómo se realicen las operaciones. En mi programa, el candado permite mantener el control sobre la distribución de documentos y la actualización del registro.

### 3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?

Si cada documento tuviera que guardarse en un archivo real, modificaría la función `trabajar()` para que, además de retirar el documento, lo escribiera en el disco. Utilizaríamos `open()` junto con `with` para crear y escribir archivos de forma segura, asegurándonos de que se cierren correctamente. También agregaría manejo de errores mediante `try-except`, por si ocurre algún problema al guardar un documento.Si todos los trabajadores escribieran en un mismo archivo, utilizaríamos un `Lock` para evitar que las escrituras se mezclen o generen conflictos. Si cada documento se guardara en un archivo diferente, podríamos permitir que los trabajadores escribieran de forma independiente, utilizando nombres únicos para cada archivo. Finalmente, actualizaría el contador del trabajador solamente después de confirmar que el archivo se guardó correctamente.

## Conclusión

Esta práctica nos permitió comprender cómo funcionan los hilos en Python y cómo se pueden distribuir tareas entre varios trabajadores.

Utilizamos cuatro hilos, una lista compartida de 24 documentos y un `Lock` para controlar el acceso a los datos.

Con `join()` esperamos a que todos los trabajadores terminen antes de mostrar el resumen final.

El programa permite procesar los 24 documentos sin asignarlos dos veces y muestra cuántos documentos fueron atendidos por cada trabajador.

Aprendimos que la sincronización es importante para evitar condiciones de carrera y mantener la integridad de los datos compartidos.