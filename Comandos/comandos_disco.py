import os
import random
import sys
import time
from Estructuras.MBR import *
from Estructuras.Transition import *
from Estructuras.EBR import *
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

        fit = fit
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

# Comando RMDISK
def cmd_rmdisk(path):
    if path:
        try:
            if os.path.isfile(path):
                if not path.endswith(".dsk"):
                    print("\tERROR: Extensión de archivo no válida para la eliminación del Disco.") 
                if  input("\t> RMDISK: ¿Está seguro que desea eliminar el disco? (S/N): ").upper() == "S":
                    os.remove(path)
                    print("\t> RMDISK: Disco eliminado exitosamente") 
                else:
                    print("\t> RMDISK: Eliminación del disco cancelada correctamente") 
            else:
                print("\tERROR: El disco no existe en la ruta indicada.") 
        except Exception as e:
            print("\tERROR: Error al intentar eliminar el disco: "+str(e)) 

# Comando FDISK
def cmd_fdisk(size, path, name, unit, type, fit, delete, add):
    #parametros obligatorios size, path, name
    if size is None:
        print("\t> FDISK: No se encuentra en parámetro size.")
        return
    elif path is None:
        print("\t> FDISK: No se encuentra en parámetro path.")
        return
    elif name is None:
        print("\t> FDISK: No se encuentra en parámetro name.")
        return
    else:
        if delete != None:
            #eliminarParticion(name, path)
            print("Eliminar particion")
        elif add != None:
            #agregarParticion(add, name, path, unit)
            print("Agregar particion")
        else:
            crearParticion(size, path, name, unit, type, fit)
            #print("Crear particion")

def crearParticion(size, path, name, unit, type, fit):
    
    if size <= 0:
        print("\tERROR: El parámetro size del comando FDISK debe ser mayor a 0")
        return
    
    if unit == "B":
        size = size
    elif unit == "K":
        size = size * 1024
    elif unit == "M":
        size = size * 1024 * 1024
    
    if type not in ["P", "E", "L"]:
        print("\tERROR: El parámetro type del comando FDISK debe ser P, E o L")
        return
    
    if fit not in ["BF", "FF", "WF"]:
        print("\tERROR: El parámetro fit del comando FDISK debe ser BF, FF o WF")
        return
    
    if path.startswith("\""):
        path = path[1:-1]

    if not path.endswith(".dsk"):
        print("\tERROR: Extensión de archivo no válida para la creación del Disco.")
        return
    
    if not os.path.exists(path):
        print("\tERROR: No existe el disco en la ruta: "+path)
        return
    
    try:
        print("\t> FDISK: Creando partición...")

        mbr = MBR()

        with open(path, "rb") as file:
            mbr_data = file.read()
            mbr.mbr_tamano = struct.unpack("<i", mbr_data[0:4])[0]
            mbr.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
            mbr.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
            mbr.disk_fit = mbr_data[12:14].decode("utf-8")

            partition_size = struct.calcsize("<iii16s")*4
            partition_data = mbr_data[14:14 + partition_size]
            mbr.mbr_Partition_1.__setstate__(partition_data[0:28]) 
            mbr.mbr_Partition_2.__setstate__(partition_data[28:56]) 
            mbr.mbr_Partition_3.__setstate__(partition_data[56:84]) 
            mbr.mbr_Partition_4.__setstate__(partition_data[84:112])

    except Exception as e:
        print(e)

    particiones = [mbr.mbr_Partition_1, mbr.mbr_Partition_2, mbr.mbr_Partition_3, mbr.mbr_Partition_4]
    
    tmp_size_deleted = []
    for particion in particiones:
        if(particion.part_status == "D"):
            tmp_size_deleted.append(particion.part_size)
    # Particiones Primarias
    size_mbr = sys.getsizeof(mbr) + struct.calcsize("<iii16s")*4
    if mbr.disk_fit == "FF":
        tmp_size = size_mbr
        for particion in particiones:
            if particion.part_type == "P":
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == "1":
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == "0":
                    particion.part_status = "1"
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.start = tmp_size
                    tmp_size += size
                    break
                # si la particion ha sido eliminada, crear la particion en el primer espacio libre
                elif particion.part_status == "D":
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = "1"
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.start = tmp_size
                        tmp_size += size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return
            elif particion.part_type == "E":
                print("\tERROR: Ya existe una partición extendida en el disco.")
                return
    elif mbr.disk_fit == "BF":
        tmp_size = size_mbr
        for particion in particiones:
            if particion.part_type == "P":
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == "1":
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == "0":
                    particion.part_status = "1"
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.start = tmp_size
                    tmp_size += size
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas pequeño
                elif particion.part_status == "D":
                    tmp_size_deleted.sort()
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = "1"
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.start = tmp_size
                        tmp_size += size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return
                
    elif mbr.disk_fit == "WF":
        tmp_size = size_mbr
        for particion in particiones:
            if particion.part_type == "P":
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == "1":
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == "0":
                    particion.part_status = "1"
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.start = size_mbr + tmp_size
                    tmp_size += size
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas grande
                elif particion.part_status == "D":
                    tmp_size_deleted.sort(reverse=True)
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = "1"
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.start = size_mbr + tmp_size
                        tmp_size += size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return         
    
    # escribir los cambios en el archivo
    try:
        with open(path, "rb+") as file:
            file.write(mbr.__bytes__())
        print("\t> FDISK: Partición creada exitosamente")
    except Exception as e:
        print(e)
        print("\tERROR: Error al crear la partición en el disco: "+path)
        return
    
def imprimirMBR(path):
    mbr = MBR()
    try:
        with open(path, "rb") as file:
            mbr_data = file.read()
            mbr.mbr_tamano = struct.unpack("<i", mbr_data[:4])[0]
            mbr.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
            mbr.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
            mbr.disk_fit = mbr_data[12:14].decode('utf-8')

            partition_size = struct.calcsize("<iii16s")*4
            partition_data = mbr_data[14:14 + partition_size]
            mbr.mbr_Partition_1.__setstate__(partition_data[0:28]) 
            mbr.mbr_Partition_2.__setstate__(partition_data[28:56]) 
            mbr.mbr_Partition_3.__setstate__(partition_data[56:84]) 
            mbr.mbr_Partition_4.__setstate__(partition_data[84:112])
    except Exception as e:
        print(e)

    print("Tamaño: "+str(mbr.mbr_tamano))
    print("Fecha: "+str(mbr.mbr_fecha_creacion))
    print("Signature: "+str(mbr.mbr_disk_signature))
    print("Fit: "+str(mbr.disk_fit))
    print("Particion 1:")
    print("\tStatus: "+str(mbr.mbr_Partition_1.part_status))
    print("\tType: "+str(mbr.mbr_Partition_1.part_type))
    print("\tFit: "+str(mbr.mbr_Partition_1.part_fit))
    print("\tStart: "+str(mbr.mbr_Partition_1.part_start))
    print("\tSize: "+str(mbr.mbr_Partition_1.part_size))
    print("\tName: "+str(mbr.mbr_Partition_1.part_name))
    print("Particion 2:")
    print("\tStatus: "+str(mbr.mbr_Partition_2.part_status))
    print("\tType: "+str(mbr.mbr_Partition_2.part_type))
    print("\tFit: "+str(mbr.mbr_Partition_2.part_fit))
    print("\tStart: "+str(mbr.mbr_Partition_2.part_start))
    print("\tSize: "+str(mbr.mbr_Partition_2.part_size))
    print("\tName: "+str(mbr.mbr_Partition_2.part_name))
    print("Particion 3:")
    print("\tStatus: "+str(mbr.mbr_Partition_3.part_status))
    print("\tType: "+str(mbr.mbr_Partition_3.part_type))
    print("\tFit: "+str(mbr.mbr_Partition_3.part_fit))
    print("\tStart: "+str(mbr.mbr_Partition_3.part_start))
    print("\tSize: "+str(mbr.mbr_Partition_3.part_size))
    print("\tName: "+str(mbr.mbr_Partition_3.part_name))
    print("Particion 4:")
    print("\tStatus: "+str(mbr.mbr_Partition_4.part_status))
    print("\tType: "+str(mbr.mbr_Partition_4.part_type))
    print("\tFit: "+str(mbr.mbr_Partition_4.part_fit))
    print("\tStart: "+str(mbr.mbr_Partition_4.part_start))
    print("\tSize: "+str(mbr.mbr_Partition_4.part_size))
    print("\tName: "+str(mbr.mbr_Partition_4.part_name))
