import os
import random
import time
from Estructuras.Estructuras import *

# Comando MKDISK

def cmd_mkdisk(size, path, fit, unit):
        disco = MBR()
        try:
            if unit == 'K':
                total_size = 1024 * size
            elif unit == 'M':
                total_size = 1024 * 1024 * size
            else:
                print("Error: Unidad no válida")
                return
            if size <= 0:
                print("\tERROR: El parámetro size del comando MKDISK debe ser mayor a 0")
                return

            fit = fit[0].upper()
            disco.mbr_tamano = total_size
            disco.mbr_fecha_creacion = int(time.time())
            disco.disk_fit = fit
            disco.mbr_disk_signature = random.randint(100, 9999)

            if os.path.exists(path):
                print("\tERROR: Disco ya existente en la ruta: "+path)
                return

            folder_path = os.path.dirname(path)
            os.makedirs(folder_path, exist_ok=True)

            disco.mbr_Partition_1 = Particion()
            disco.mbr_Partition_2 = Particion()
            disco.mbr_Partition_3 = Particion()
            disco.mbr_Partition_4 = Particion()

            if path.startswith("\""):
                path = path[1:-1]

            if not path.endswith(".dsk"):
                print("\tERROR: Extensión de archivo no válida para la creación del Disco.")
                return

            try:
                with open(path, "w+b") as file:
                    file.write(b"\x00")
                    file.seek(total_size - 1)
                    file.write(b"\x00")
                    file.seek(0)
                    file.write(bytes(disco))
                print("\t>>>> MKDISK: Disco creado exitosamente <<<<")
            except Exception as e:
                print(e)
                print("\tERROR: Error al crear el disco en la ruta: "+path)
        except ValueError:
            print("\tERROR: El parámetro size del comando MKDISK debe ser un número entero")