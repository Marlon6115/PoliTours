
import os
import heapq
from collections import deque

grafo = {}
jerarquia = {}
ARCHIVO_RUTAS = "rutas.txt"

# Cargar datos desde el archivo al iniciar
if os.path.exists(ARCHIVO_RUTAS):
    with open(ARCHIVO_RUTAS, "r") as archivo:
        seccion = None
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue  # omitir líneas vacías o comentarios

            if linea == "[GRAFO]":
                seccion = "grafo"
                continue
            elif linea == "[JERARQUIA]":
                seccion = "jerarquia"
                continue

            if ":" not in linea:
                continue  # evita error si no hay ':'

            clave, valor = linea.split(":", 1)  # solo divide en el primer ':' encontrado

            if seccion == "grafo":
                grafo[clave.strip()] = eval(valor.strip())
            elif seccion == "jerarquia":
                jerarquia[clave.strip()] = eval(valor.strip())


def guardar_datos():
    with open(ARCHIVO_RUTAS, "w") as archivo:
        archivo.write("[GRAFO]\n")
        for ciudad, conexiones in grafo.items():
            archivo.write(f"{ciudad}:{conexiones}\n")
        archivo.write("[JERARQUIA]\n")
        for region, categorias in jerarquia.items():
            archivo.write(f"{region}:{categorias}\n")

def agregarCiudad():
    ciudad = input("Nombre de la nueva ciudad: ")
    if ciudad in grafo:
        print("La ciudad ya existe.")
        return

    grafo[ciudad] = {}
    while True:
        conectar = input("¿Conectar con otra ciudad? (s/n): ").lower()
        if conectar == 'n':
            break
        destino = input("Ciudad destino: ")
        distancia = int(input("Distancia (km): "))
        costo = int(input("Costo ($): "))
        grafo[ciudad][destino] = {"distancia": distancia, "costo": costo}
        if destino not in grafo:
            grafo[destino] = {}
        grafo[destino][ciudad] = {"distancia": distancia, "costo": costo}

    region = input("Región (ej. Sierra, Costa, Oriente): ")
    categoria = input("Categoría (ej. Naturaleza, Aventura): ")

    if region not in jerarquia:
        jerarquia[region] = {}
    if categoria not in jerarquia[region]:
        jerarquia[region][categoria] = []
    jerarquia[region][categoria].append(ciudad)
    guardar_datos()
    print("Ciudad agregada con éxito.")

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
            print("1. Agregar nueva ciudad")
            print("2. Listar ciudades")
            print("3. Consultar ciudad/punto turistico")
            print("4. Actualizar ciudad/punto turistico")
            print("5. Eliminar ciudad/punto turistico")
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
            usuarioAdmin = "Administrador.Alex"
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
                                        if usuario == usuarioUsuario and contrasena == contrasenaUsuario:
                                            acceso_concedido = True
                                            break
                        except FileNotFoundError:
                            print("No hay usuarios registrados aún. Regístrese primero.")
                            break
                        if acceso_concedido:
                            print("Acceso concedido")
                            # Aqui iria el menu de todo lo que puede hacer el usuario


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
    

