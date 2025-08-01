import heapq
import os

grafo = {
    "Baños": {
        "Pailón del Diablo": {"distancia": 18, "costo": 3},
        "Puyo": {"distancia": 88, "costo": 9},
        "Tena": {"distancia": 173, "costo": 15}
    },
    "Pailón del Diablo": {
        "Baños": {"distancia": 18, "costo": 3},
        "Puyo": {"distancia": 70, "costo": 7},
        "Tena": {"distancia": 155, "costo": 13}
    },
    "Puyo": {
        "Baños": {"distancia": 88, "costo": 9},
        "Pailón del Diablo": {"distancia": 70, "costo": 7},
        "Tena": {"distancia": 85, "costo": 9}
    },
    "Tena": {
        "Baños": {"distancia": 173, "costo": 15},
        "Pailón del Diablo": {"distancia": 155, "costo": 13},
        "Puyo": {"distancia": 85, "costo": 9}
    }
}

jerarquia = {
    "Sierra": {
        "Espiritualidad": ["Baños"],
        "Naturaleza": ["Pailón del Diablo"],
        "Aguas termales": ["Baños"]
    },
    "Oriente": {
        "Naturaleza": ["Puyo", "Tena"]
    }
}

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
    print("\nMapa de lugares turísticos:")
    for ciudad, conexiones in grafo.items():
        for destino, info in conexiones.items():
            distancia = info["distancia"]
            costo = info["costo"]
            print(f"{ciudad} a {destino} ({distancia} km, ${costo})")

def consultar_ruta_optima():
    inicio = input("Punto turístico de origen: ")
    destino = input("Punto turístico destino: ")
    camino, costo = dijkstra(inicio, destino)
    if camino:
        print("Ruta óptima:", " a ".join(camino))
        print("Costo total: $", costo)
    else:
        print("Ruta no encontrada.")

def explorar_lugares():
    print("\nZonas y categorías turísticas:")
    for zona, categorias in jerarquia.items():
        print(f"- {zona}")
        for categoria, lugares in categorias.items():
            print(f"  > {categoria}: {', '.join(lugares)}")

def seleccionar_lugares(nombre_cliente):
    seleccion = []
    while True:
        lugar = input("Ingrese una ciudad o punto turístico (Para salir ingrese [0]): ")
        if lugar == '0':
            break
        if lugar not in grafo:
            print("Ese lugar no está disponible en el mapa. Intenta con otro.")
            continue
        seleccion.append(lugar)

    if not seleccion:
        print("No se seleccionaron lugares.")
        return

    archivo = f"rutas-{nombre_cliente}.txt"
    with open(archivo, "a") as f:
        for lugar in seleccion:
            f.write(f"{lugar}\n")
    print("Selección guardada en", archivo)

def listar_lugares(nombre_cliente):
    archivo = f"rutas-{nombre_cliente}.txt"
    if not os.path.exists(archivo):
        print("No hay selección guardada.")
        return
    with open(archivo, "r") as f:
        lugares = [line.strip() for line in f.readlines()]
    lugares = merge_sort(lugares)
    print("Lugares seleccionados (ordenados):", lugares)
    
    total = 0
    for i in range(len(lugares)-1):
        _, costo = dijkstra(lugares[i], lugares[i+1])
        total += costo
    print("Costo total: $", total)

    while True:
        try:
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
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

def menu_cliente(nombre_cliente):
    while True:
        try:
            print("\n--- MENÚ CLIENTE ---")
            print("1. Ver mapa")
            print("2. Consultar ruta óptima")
            print("3. Explorar lugares")
            print("4. Seleccionar lugares turísticos")
            print("5. Lista de lugares turísticos seleccionados")
            print("6. Salir")
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                ver_mapa()
            elif opcion == 2:
                consultar_ruta_optima()
            elif opcion == 3:
                explorar_lugares()
            elif opcion == 4:
                seleccionar_lugares(nombre_cliente)
            elif opcion == 5:
                listar_lugares(nombre_cliente)
            elif opcion == 6:
                print("¡Gracias por usar el sistema!")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

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