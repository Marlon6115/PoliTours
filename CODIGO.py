

def RegistrarUsuario():
    print("Registrando usuario...")
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
            print("Error: Ingrese una identificación válida")
            
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
        contrasena = input("Ingrese su contraseña: ")
        if 'a' in contrasena:
            break
    print("Usuario registrado exitosamente")
    print(f"Nombre: {nombre} {apellido}")
    print(f"Identificación: {identificacion}")
    print(f"Edad: {edad}")
    print(f"Usuario: {usuario}")
    print(f"Contraseña: {contrasena}")

while True:
    try:
        print("\nBienvenido al Sistema de Rutas Turisticas Inteligentes")
        print("-----------------|||-----------------")
        print("1. Acceder como administrador")
        print("2. Acceder como usuario")
        print("3. Salir del sistema")
        print("-----------------|||-----------------")
        ingreso = int(input("seleccione una opción: "))
        if ingreso == 1:
            contrasenaAdmin = "admin123"
            usuarioAdmin = "Administrador.Alex"
            intentosAdmin = 0
            while intentosAdmin < 3:
                print("\nAcceso al sistema de administrador")
                print("-----------------|||-----------------")
                contrasena = input("Ingrese la contraseña de administrador: ")
                usuario = input("Ingrese el usuario de administrador: ")
                print("-----------------|||-----------------")
                intentosAdmin += 1
                if contrasena == contrasenaAdmin and usuario == usuarioAdmin:
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
            print("-----------------|||-----------------")
            intentosUsuario = 0
            while intentosUsuario < 3:
                try:
                    opcionUsuario = input("1. Acceder al Sistema: \n2. Registrarse: \n3.Salir\nSeleccione una opción: ")
                    if opcionUsuario == "1":
                        contrasenaUsuario = "user123"
                        usuarioUsuario = "Usuario.Alex"
                        usuario = input("Ingrese su usuario: ")
                        contrasena = input("Ingrese su contraseña: ")
                        intentosUsuario += 1
                        if usuario == usuarioUsuario and contrasena == contrasenaUsuario:
                            print("Acceso concedido")
                            # Aqui iria el menu de todo lo que puede hacer el usuario


                            break
                        elif intentosUsuario == 3:
                            print("Demasiados intentos fallidos. Saliendo del sistema ...")
                            break
                        else:
                            print("Usuario o contraseña incorrectos")
                
                    elif opcionUsuario == "2":
                        print("Registrandose...")
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

with open("rutas.txt", "r") as archivo:
    contenido = archivo.read ()
    print (contenido)


