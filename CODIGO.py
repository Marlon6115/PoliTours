import os
import heapq

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

    try:
        opcion = int(input("Ingrese el número del punto turístico a modificar: "))
        if 1 <= opcion <= len(lineas):
            origen = input("Ingrese la ciudad de origen: ").strip()
            destino = input("Ingrese la ciudad de destino: ").strip()
            distancia = input("Ingrese la distancia en km: ").strip()
            costo = input("Ingrese el costo en $: ").strip()

            nueva_info = f"{origen} a {destino} ({distancia} km, ${costo})"
            lineas[opcion - 1] = nueva_info + "\n"

            with open(archivo, "w") as f:
                f.writelines(lineas)

            print("Punto turístico modificado correctamente.")
        else:
            print("Opción fuera del rango.")
    except ValueError:
        print("Opción no valida.")

def eliminar_punto(nombre):
    archivo = f"rutas-{nombre}.txt"
    if not os.path.exists(archivo):
        print("No hay puntos turísticos guardados.")
        return

    with open(archivo, "r") as f:
        lineas = f.readlines()

    if not lineas:
        print("No hay puntos turísticos para eliminar.")
        return

    print("\nSeleccione el punto turístico a eliminar:")
    for i, linea in enumerate(lineas, 1):
        print(f"{i}. {linea.strip()}")

    try:
        opcion = int(input("Ingrese el número del punto turístico a eliminar: "))
        if 1 <= opcion <= len(lineas):
            eliminado = lineas.pop(opcion - 1)
            with open(archivo, "w") as f:
                f.writelines(lineas)
            print(f"[{eliminado.strip()}] eliminado correctamente.")
        else:
            print("Opción fuera del rango.")
    except ValueError:
        print("Opción no valida")

def menu_cliente(nombre):
    while True:
        print("-----------------|||-----------------")
        print("\n---------- MENÚ CLIENTE -----------")
        print("1. Ver mapa")
        print("2. Consultar la ruta óptima")
        print("3. Explorar lugares")
        print("4. Seleccionar puntos turísticos")
        print("5. Lista de puntos turísticos")
        print("6. Actualizar punto turístico")
        print("7. Eliminar punto turístico")
        print("8. Salir")
        print("-----------------|||-----------------")


        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            ver_mapa()
        elif opcion == 2:
            consultar_ruta_optima()
        elif opcion == 3:
            explorar_lugares()
        elif opcion == 4:
            seleccionar_puntos(nombre)
        elif opcion == 5:
            listar_puntos(nombre)
        elif opcion == 6:
            modificar_punto(nombre)
        elif opcion == 7:
            eliminar_punto(nombre)
        elif opcion == 8:
            print("Gracias, vuelva pronto")
            break
        else:
            print("Opción no valida")

def guardar_datos():
    with open(ARCHIVO_RUTAS, "w") as archivo:
        archivo.write("[GRAFO]\n")
        for ciudad, conexiones in grafo.items():
            archivo.write(f"{ciudad}:{conexiones}\n")
        archivo.write("[JERARQUIA]\n")
        for region, categorias in jerarquia.items():
            archivo.write(f"{region}:{categorias}\n")

def agregarCiudad():
    ciudad1 = input("Nombre de la primera ciudad: ").strip()
    ciudad2 = input("Nombre de la segunda ciudad: ").strip()

    if ciudad1 in grafo and ciudad2 in grafo[ciudad1]:
        print("No se puede registrar una ruta ya existente entre esas dos ciudades.")
        return

    try:
        distancia = int(input(f"Distancia entre {ciudad1} y {ciudad2} (km): "))
        costo = int(input(f"Costo entre {ciudad1} y {ciudad2} ($): "))
    except ValueError:
        print("Distancia o costo no válido.")
        return

    if ciudad1 not in grafo:
        grafo[ciudad1] = {}
        region1 = input(f"Región de {ciudad1} (ej. Sierra, Costa, Oriente): ").strip()
        categoria1 = input(f"Categoría de {ciudad1} (ej. Naturaleza, Aventura): ").strip()

        if region1 not in jerarquia:
            jerarquia[region1] = {}
        if categoria1 not in jerarquia[region1]:
            jerarquia[region1][categoria1] = []
        jerarquia[region1][categoria1].append(ciudad1)

    if ciudad2 not in grafo:
        grafo[ciudad2] = {}
        region2 = input(f"Región de {ciudad2} (ej. Sierra, Costa, Oriente): ").strip()
        categoria2 = input(f"Categoría de {ciudad2} (ej. Naturaleza, Aventura): ").strip()

        if region2 not in jerarquia:
            jerarquia[region2] = {}
        if categoria2 not in jerarquia[region2]:
            jerarquia[region2][categoria2] = []
        jerarquia[region2][categoria2].append(ciudad2)

    grafo[ciudad1][ciudad2] = {"distancia": distancia, "costo": costo}
    grafo[ciudad2][ciudad1] = {"distancia": distancia, "costo": costo}

    guardar_datos()
    print(f"Ruta entre '{ciudad1}' y '{ciudad2}' registrada con éxito.")



def listarCiudades():
    if not grafo:
        print("No hay ciudades registradas.")
        return
    for ciudad, conexiones in grafo.items():
        print(f"\nCiudad: {ciudad}")
        for destino, datos in conexiones.items():
            print(f"  - Hacia {destino}: {datos['distancia']} km, ${datos['costo']}")

def consultarCiudad():
    ciudad = input("Ciudad a consultar: ")
    if ciudad not in grafo:
        print("No existe.")
        return
    print(f"Conexiones desde {ciudad}:")
    for destino, datos in grafo[ciudad].items():
        print(f"  - {destino}: {datos['distancia']} km, ${datos['costo']}")

def actualizarCiudad():
    ciudad = input("Ciudad a actualizar: ")
    if ciudad not in grafo:
        print("No existe.")
        return
    print("Actualizando conexiones:")
    grafo[ciudad] = {}
    while True:
        destino = input("Nuevo destino (vacío para terminar): ")
        if not destino:
            break
        distancia = int(input("Distancia: "))
        costo = int(input("Costo: "))
        grafo[ciudad][destino] = {"distancia": distancia, "costo": costo}
        if destino not in grafo:
            grafo[destino] = {}
        grafo[destino][ciudad] = {"distancia": distancia, "costo": costo}
    guardar_datos()
    print("Ciudad actualizada.")

def eliminarCiudad():
    ciudad = input("Ciudad a eliminar: ")
    if ciudad not in grafo:
        print("No existe.")
        return
    for destino in list(grafo[ciudad]):
        del grafo[destino][ciudad]
    del grafo[ciudad]

    for region in list(jerarquia):
        for categoria in list(jerarquia[region]):
            if ciudad in jerarquia[region][categoria]:
                jerarquia[region][categoria].remove(ciudad)
            if not jerarquia[region][categoria]:
                del jerarquia[region][categoria]
        if not jerarquia[region]:
            del jerarquia[region]

    guardar_datos()
    print("Ciudad eliminada.")

def menuAdmin():
    print("\nADMINISTRADOR DE RUTAS")
    while True:
        try:
            print("1. Agregar nuevo punto turístico")
            print("2. Listar puntos turístico")
            print("3. Consultar punto turistico")
            print("4. Actualizar punto turistico")
            print("5. Eliminar punto turistico")
            print("6. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                agregarCiudad()
            elif opcion == "2":
                listarCiudades()
            elif opcion == "3":
                consultarCiudad()
            elif opcion == "4":
                actualizarCiudad()
            elif opcion == "5":
                eliminarCiudad()
            elif opcion == "6":
                print("Saliendo del administrador de rutas.")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Error: Entrada no válida. Por favor, ingrese un número.")

def RegistrarUsuario():
    print("-----------------|||-----------------")
    nombre = input("Ingrese su nombre: ").strip().lower().capitalize()
    apellido = input("Ingrese su apellido: ").strip().lower().capitalize()
    while True:
        try:
            identificacion = int(input("Ingrese su identificacion: "))
            if identificacion > 0 and len(str(identificacion)) >= 10:
                break
            else:
                print("Identificacion no valida")
        except ValueError:
            print("Error: Ingrese una identificación valida")
            
    usuario = f"{nombre.lower()}.{apellido.lower()}@gmail.com"

    while True:
        try:
            edad = int(input("Ingrese su edad: "))
            if edad >= 18:
                break
            elif edad < 18:
                print("Debe ser mayor de 18 años para registrarse")
            else:
                print("Edad no valida. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un número valido para la edad")

    while True:
        print("Ingrese una contraseña debe tener al menos una mayuscula, una minuscula y un numero") 
        contrasena = input("Ingrese su contraseña: ").strip()
        if (any(c.isupper() for c in contrasena) and any(c.islower() for c in contrasena) and any(c.isdigit() for c in contrasena)):
            break
        else:
            print("Contraseña no valida. Debe tener al menos una mayuscula, una minuscula y un numero")
    
    print(f"Bienvenido {nombre} {apellido}, su usuario es: {usuario}")
    print("-----------------|||-----------------\n")

    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario};{contrasena};{nombre};{apellido};{identificacion};{edad}\n")


while True:
    try:
        print("\nBienvenido al Sistema de Rutas Turisticas Inteligentes")
        print("-----------------|||-----------------")
        print("1. Acceder como administrador")
        print("2. Acceder como usuario")
        print("3. Salir del sistema")
        print("-----------------|||-----------------")
        ingreso = int(input("Seleccione una opción: "))
        if ingreso == 1:
            contrasenaAdmin = "admin123"
            usuarioAdmin = "algoritmos"
            intentosAdmin = 0
            while intentosAdmin < 3:
                print("\nAcceso al sistema de administrador")
                print("-----------------|||-----------------")
                usuario1 = input("Ingrese el usuario de administrador: ")
                contrasena1 = input("Ingrese la contraseña de administrador: ")
                print("-----------------|||-----------------")
                intentosAdmin += 1
                if contrasena1 == contrasenaAdmin and usuario1 == usuarioAdmin:
                    print("Acceso concedido")
                    print("-----------------|||-----------------")
                    #Aqui iria el menu de todo lo que puede hacer el administrador
                    menuAdmin()
                    break
                elif intentosAdmin == 3:
                    print("Demasiados intentos fallidos. Saliendo del sistema ...")
                    break
                else:
                    print("Usuarios o contraseñas incorrectos")            
        elif ingreso == 2:
            print("\nAccediendo como usuario...")
            intentosUsuario = 0
            while intentosUsuario < 3:
                try:
                    print("-----------------|||-----------------")
                    opcionUsuario = input("1. Acceder al Sistema \n2. Registrarse \n3. Salir\nSeleccione una opción: ")
                    if opcionUsuario == "1":
                        usuario = input("Ingrese su usuario: ")
                        contrasena = input("Ingrese su contraseña: ")
                        acceso_concedido = False
                        
                        try:
                            with open("usuarios.txt", "r") as archivo:
                                for linea in archivo:
                                    datos = linea.strip().split(";")
                                    if len(datos) >= 2:
                                        usuarioUsuario = datos[0]
                                        contrasenaUsuario = datos[1]
                                        nombre = datos[2]
                                        if usuario == usuarioUsuario and contrasena == contrasenaUsuario:
                                            acceso_concedido = True
                                            break
                        except FileNotFoundError:
                            print("No hay usuarios registrados aún. Regístrese primero.")
                            break
                        if acceso_concedido:
                            print("Acceso concedido")
                            # Aqui iria el menu de todo lo que puede hacer el usuario
                            menu_cliente(nombre)

                            break
                        else:
                            intentosUsuario += 1
                            print("Usuario o contraseña incorrectos")
                
                    elif opcionUsuario == "2":
                        print("Registrandose...")
                        RegistrarUsuario()
                        break
                    elif opcionUsuario == "3":
                        print("Saliendo del sistema ...")
                        break
                    else:
                        print("Opcion no valida")
                except ValueError:
                    print("Error al ingresar una opcion")
            
        elif ingreso == 3:
            print("Saliendo del sistema ...")
            break
        else:
            print("Opcion no valida")
    except ValueError:
        print("Error al ingresar una opcion")
