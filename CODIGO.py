import os
import heapq
import random
from collections import deque

grafo = {}
jerarquia = {}
ARCHIVO_RUTAS = "rutas.txt"

if os.path.exists(ARCHIVO_RUTAS):
    with open(ARCHIVO_RUTAS, "r") as archivo:
        seccion = None
        for linea in archivo:
            linea = linea.strip()
            if linea == "[GRAFO]":
                seccion = "grafo"
                continue
            elif linea == "[JERARQUIA]":
                seccion = "jerarquia"
                continue

            if seccion == "grafo":
                try:
                    ciudad, conexiones = linea.split(":", 1)
                    grafo[ciudad] = eval(conexiones)
                except ValueError:
                    print(f"Error en la línea del archivo (GRAFO): {linea}")

            elif seccion == "jerarquia":
                try:
                    region, categorias = linea.split(":", 1)
                    jerarquia[region] = eval(categorias)
                except ValueError:
                    print(f"Error en la línea del archivo (JERARQUÍA): {linea}")

def dijkstra(inicio, fin):
    cola = [(0, inicio, [])]
    visitado = set()

    while cola:
        costo, ciudad, camino = heapq.heappop(cola)
        if ciudad in visitado:
            continue
        camino = camino + [ciudad]
        if ciudad == fin:
            return camino, costo
        visitado.add(ciudad)
        for vecino, info in grafo.get(ciudad, {}).items():
            if vecino not in visitado:
                heapq.heappush(cola, (costo + info["costo"], vecino, camino))
    return None, float("inf")

def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    mitad = len(lista) // 2
    izquierda = merge_sort(lista[:mitad])
    derecha = merge_sort(lista[mitad:])
    return merge(izquierda, derecha)

def merge(izq, der):
    resultado = []
    while izq and der:
        if izq[0] < der[0]:
            resultado.append(izq.pop(0))
        else:
            resultado.append(der.pop(0))
    resultado += izq + der
    return resultado

def ver_mapa():
    print("\nMapa de puntos turísticos:")
    indice = 1
    for ciudad, conexiones in grafo.items():
        for destino, info in conexiones.items():
            distancia = info["distancia"]
            costo = info["costo"]
            print(f"{indice}. {ciudad} a {destino} ({distancia} km, ${costo})")
            indice += 1


def consultar_ruta_optima():
    inicio = input("Punto turístico de origen: ")
    destino = input("Punto turístico destino: ")
    
    camino, costo = dijkstra(inicio, destino)
    
    if camino:
        distancia_total = 0
        for i in range(len(camino) - 1):
            ciudad_actual = camino[i]
            ciudad_siguiente = camino[i + 1]
            distancia_total += grafo[ciudad_actual][ciudad_siguiente]["distancia"]

        print("Ruta óptima:", " -> ".join(camino))
        print("Distancia total:", distancia_total, "km")
        print("Costo total: $", costo)
    else:
        print("Ruta no encontrada.")


def explorar_lugares():
    print("\nZonas y categorías:")
    for zona, categorias in jerarquia.items():
        print(f"- {zona}")
        for categoria, lugares in categorias.items():
            print(f"  > {categoria}: {', '.join(lugares)}")

def seleccionar_puntos(nombre):
    opciones = []
    indice = 1
    for ciudad, conexiones in grafo.items():
        for destino, info in conexiones.items():
            distancia = info["distancia"]
            costo = info["costo"]
            descripcion = f"{ciudad} a {destino} ({distancia} km, ${costo})"
            print(f"{indice}. {descripcion}")
            opciones.append(descripcion)
            indice += 1

    if not opciones:
        print("No hay trayectos disponibles.")
        return

    seleccion = []
    while True:
        entrada = int(input("Ingrese un punto turístico de la lista (o [0] para salir): "))
        if entrada == 0:
            break
        if entrada > len(opciones):
            print("Número fuera de rango.")
            continue
        if opciones[entrada - 1] in seleccion:
            print("Ya seleccionaste ese punto turístico.")
            continue
        seleccion.append(opciones[entrada - 1])
        print(f"[{opciones[entrada - 1]}] agregando.....")

    archivo = f"rutas-{nombre}.txt"
    try:
        with open(archivo, "a") as f:
            for punto in seleccion:
                f.write(f"{punto}\n")
        print(f"Selección guardada en '{archivo}'")
    except Exception as e:
        print(f"Error al guardar la selección: {e}")

def listar_puntos(nombre):
    archivo = f"rutas-{nombre}.txt"
    if not os.path.exists(archivo):
        print("No hay puntos turísticos guardados aún.")
        return

    print(f"\nPuntos turísticos seleccionados por {nombre}:")
    with open(archivo, "r") as f:
        lineas = f.readlines()
        if not lineas:
            print("Archivo vacío.")
            return
        for i, linea in enumerate(lineas, 1):
            print(f"{i}. {linea.strip()}")

def modificar_punto(nombre):
    archivo = f"rutas-{nombre}.txt"
    if not os.path.exists(archivo):
        print("No hay puntos turísticos guardados.")
        return

    with open(archivo, "r") as f:
        lineas = f.readlines()

    if not lineas:
        print("No hay puntos turísticos para modificar.")
        return

    print("\nSeleccione el punto turístico a modificar:")
    for i, linea in enumerate(lineas, 1):
        print(f"{i}. {linea.strip()}")

    while True:
        opcion = int(input("\n1. Actualizar\n2. Eliminar\n3. Salir\nSeleccione una opcion: "))
        if opcion == 1:
            viejo = input("Lugar a actualizar: ")
            nuevo = input("Nuevo nombre: ")
            lugares = [nuevo if l == viejo else l for l in lugares]
            with open(archivo, "w") as f:
                for l in lugares:
                    f.write(f"{l}\n")
            print("Nombre actualizado exitosamente")
            break
        elif opcion == 2:
            borrar = input("Lugar a eliminar: ")
            lugares = [l for l in lugares if l != borrar]
            with open(archivo, "w") as f:
                for l in lugares:
                    f.write(f"{l}\n")
            print("Lugar eliminado exitosamente")
            break
        elif opcion == 3:
            break
        else:
            print("Opción no válida.")

def menu_cliente(nombre):
    while True:
        print("\n--- MENÚ CLIENTE ---")
        print("1. Ver mapa")
        print("2. Consultar ruta óptima")
        print("3. Explorar lugares")
        print("4. Seleccionar lugares turísticos")
        print("5. Lista de lugares turísticos seleccionados")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_mapa()
        elif opcion == "2":
            consultar_ruta_optima()
        elif opcion == "3":
            explorar_lugares()
        elif opcion == "4":
            seleccionar_lugares(nombre_cliente)
        elif opcion == "5":
            listar_lugares(nombre_cliente)
        elif opcion == "6":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida.")

def iniciar_sesion():
    nombre_cliente = input("Usuario: ").strip()
    clave = input("Contraseña: ").strip()

    try:
        with open("usuarios.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    nombre_archivo, clave_archivo = partes
                    if nombre_cliente == nombre_archivo and clave == clave_archivo:
                        print("Inicio de sesión exitoso.")
                        menu_cliente(nombre_cliente)
                        return nombre_cliente
    except FileNotFoundError:
        print("No se encontró el archivo de usuarios.")

    print("Credenciales incorrectas.")
    return None

nombre_cliente = iniciar_sesion()