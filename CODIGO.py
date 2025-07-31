

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
    

