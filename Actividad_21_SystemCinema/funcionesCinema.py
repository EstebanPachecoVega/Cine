#Esteban Elias Pacheco Vega
"""
Escribe un programa en Python para gestionar la venta de entradas de cine.
"""
from tabulate import tabulate
import os
import msvcrt
import time
import csv
import os
import re

#Definición del tamaño de la sala de cine (por ejemplo, 10 filas por 10 columnas)
NUM_FILAS = 10
NUM_COLUMNAS = 10

#Valor base de la entrada al cine
PRECIO_BASE_TICKET = 4000

#Estructura de datos para los asientos
asientos = [['O' for _ in range(NUM_COLUMNAS)] for _ in range(NUM_FILAS)]

#Lista para almacenar las ventas realizadas
historial_ventas = []

def limpiar():
    print('<<Press any key to continue>>')
    msvcrt.getch()
    os.system('cls')

def espera():
    time.sleep(1)   #Añade un retraso de 1 segundo

def printR(texto):  #Color rojo
    print(f'\033[31m{texto}\033[0m')

def printA(texto):  #Color Verde
    print(f'\033[32m{texto}\033[0m')

def printV(texto):  #Color Amarillo
    print(f'\033[33m{texto}\033[0m')

def menu():
    printV("Bienvenido al sistema de gestión de venta de entradas de cine")
    print("1) Mostrar asientos disponibles")
    print("2) Comprar entrada")
    print("3) Mostrar ventas realizadas")
    print("4) Generar archivo CSV de ventas")
    print("5) Salir")

def validarTelefono(numero):
    #Validación formato de número de teléfono
    return re.match(r'^\+?[\d\s-]{5,}$', numero) is not None #Al menos 5 caracteres para permitir códigos de país largos

def telefonoDuplicado(telefono):
    #Verificar si el número de teléfono ya está en la lista de contactos
    for cliente in historial_ventas:
        if cliente[3] == telefono:
            return True
    return False

def validarNombre(nombre):
    #Verificar si el nombre no está vacío, no contiene solo espacios y que tenga al menos 3 caracteres
    return bool(nombre.strip() and len(nombre.strip()) >= 3)

def asientos_Disponibles():
    print("Estado actual de los asientos:")
    for fila in range(NUM_FILAS):
        for columna in range(NUM_COLUMNAS):
            print(asientos[fila][columna], end=' ')
        print()  #Salto de línea entre filas
    print()

#INFORMACIÓN DEL CLIENTE
def comprar_ticket():
    asientos_Disponibles()
    
    while True:
        try:
            fila = int(input("Ingrese el número de fila del asiento que desea (1-{}): ".format(NUM_FILAS))) - 1
            columna = int(input("Ingrese el número de columna del asiento que desea (1-{}): ".format(NUM_COLUMNAS))) - 1
            
            if fila < 0 or fila >= NUM_FILAS or columna < 0 or columna >= NUM_COLUMNAS:
                print("Número de fila o columna fuera de rango. Intente de nuevo.")
                continue
            
            if asientos[fila][columna] == 'X':
                print("Este asiento ya está ocupado. Por favor, elija otro.")
                continue
            
            #Marcar el asiento como ocupado ('X')
            asientos[fila][columna] = 'X'
            
            #Validamos nombre del contacto
            while True:
                nombre = input("Ingrese el nombre del cliente: ").strip().title()
                if validarNombre(nombre):
                    break
                else:
                    printR('El nombre no puede estar vacío, contener solo espacios o tener menos de 3 caracteres. Por favor, ingrese un nombre válido.')
            #        
            edad = int(input("Ingrese la edad del cliente: "))
            #Validación del número de teléfono
            while True:
                telefono = input("Ingrese el número de teléfono del cliente: ").strip()
                if not validarTelefono(telefono):
                    printR('Número de teléfono no válido. Debe contener solo dígitos, espacios, guiones y opcionalmente un prefijo "+" para el código de país.')
                elif telefonoDuplicado(telefono):
                    printR('Número de teléfono duplicado. Por favor, ingrese un número diferente.')
                else:
                    break            
            #Calcular precio del ticket con descuentos
            precio_ticket = PRECIO_BASE_TICKET
            if edad < 18:
                precio_ticket *= 0.8  # Descuento del 20% para menores de 18 años
            elif edad > 65:
                precio_ticket *= 0.85  # Descuento del 15% para adultos mayores de 65 años
            precio_ticket = round(precio_ticket)

            num_asiento = fila + 1, columna + 1
            #Agregar venta a historial de ventas
            historial_ventas.append([num_asiento, nombre, edad, telefono, precio_ticket])
            printA("Venta realizada correctamente.")
            break
            
        except ValueError:
            printR("Error: Ingrese un valor válido.")
        except IndexError:
            printR("Error: Número de fila o columna fuera de rango.")

def mostrar_ventas():
    printV("Historial de ventas realizadas:")
    ventas_totales = 0
    if len(historial_ventas) > 0:
        encabezado = ['Asiento', 'Cliente', 'Edad', 'Teléfono', 'Total pagado']
        print(tabulate(historial_ventas, headers=encabezado, tablefmt='grid'))
        ventas_totales = sum(venta[4] for venta in historial_ventas)
        printA(f"Total recaudado hasta el momento: ${ventas_totales}\n")
    else:
        printR('No hay ventas registradas.')
def generar_ventas_csv():
    if len(historial_ventas) > 0:
        nombre_archivo = input("Ingrese el nombre del archivo CSV para guardar las ventas (por ejemplo, 'ventas.csv'): ")
        if not nombre_archivo.endswith('.csv'):
            nombre_archivo += '.csv'
    
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv, delimiter=',')
            historial_ventas.insert(0,['Número de asiento', 'Nombre', 'Edad', 'Teléfono', 'Total Pagado'])
            writer.writerows(historial_ventas)
            historial_ventas.pop(0)
            #writer.writeheader()
            #for venta in historial_ventas:
            #    writer.writerow(venta)
            printA(f"Archivo CSV '{nombre_archivo}' generado exitosamente.")
    else:
        printR('No hay ventas registradas.')
def main():
    while True:
        limpiar()
        menu()
        try:
            opcion = input("Seleccione: ")
            
            if opcion == '1':
                asientos_Disponibles()
            elif opcion == '2':
                comprar_ticket()
            elif opcion == '3':
                mostrar_ventas()
            elif opcion == '4':
                generar_ventas_csv()
            elif opcion == '5':
                espera()
                printA("Gracias por utilizar nuestro sistema. ¡Hasta luego!")
                break
            else:
                printR("Opción no válida. Por favor, ingrese un número del 1 al 5.")
        
        except ValueError:
            printR("Error: Ingrese un valor válido (número del 1 al 5).")
        except Exception as e:
            printR(f"Error inesperado: {e}")