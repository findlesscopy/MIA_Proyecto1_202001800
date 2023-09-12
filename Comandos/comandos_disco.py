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
        

        mbr = MBR()
        ebr = EBR()
        logica_ebr = EBR()
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
    existe_extendida = False
    tmp_nombres = []
    for particion in particiones:
        tmp_nombres.append(particion.part_name)
        if(particion.part_status == 'D'):
            tmp_size_deleted.append(particion.part_size)
        if(particion.part_type == 'E'):
            existe_extendida = True
    if name in tmp_nombres:
        print("\tERROR: Ya existe una partición con el nombre: "+name)
        return
    if type == 'P':
        print("\t> FDISK: Creando partición primaria...")
    elif type == 'E':
        print("\t> FDISK: Creando partición extendida...")
    elif type == 'L':
        print("\t> FDISK: Creando partición lógica...")
    # Particiones Primarias
    size_mbr = 14 + (struct.calcsize("<iii16s")*4)
    if mbr.disk_fit == "FF":
        tmp_size = size_mbr
        for particion in particiones:
            if type == 'P':
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == '1':
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == '0':
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size
                    break
                # si la particion ha sido eliminada, crear la particion en el primer espacio libre
                elif particion.part_status == 'D':
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size
                        tmp_size += size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return
                    
            elif type == 'E':
                if existe_extendida:
                    print("\tERROR: No se puede crear una partición extendida, porque ya existe una.")
                    return
                if particion.part_status == '1':
                    tmp_size += particion.part_size

                # si la particion no existe, crearla y crear un EBR
                elif particion.part_status == '0':
                    
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size

                    # crear EBR de la particion extendida
                    ebr.part_status = '1'
                    ebr.part_fit = fit
                    ebr.part_start = tmp_size
                    ebr.part_size = size
                    ebr.part_next = 1234
                    ebr.part_name = name
                    

                    break
                # si la particion ha sido eliminada, crear la particion en el primer espacio libre
                elif particion.part_status == 'D':
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size
                        tmp_size += size

                        ebr.part_status = '1'
                        ebr.part_fit = fit
                        ebr.part_start = tmp_size
                        ebr.part_size = size
                        ebr.part_next = -1
                        ebr.part_name = name
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return

            elif type == 'L':
                existe_extendida = False
                for particion in particiones:
                    if particion.part_type == 'E':
                        existe_extendida = True
                        particionLogica(particion, path, size, name, 'FF', fit)
                        return
                if not existe_extendida:
                    print("\tERROR: No existe una partición extendida para crear la partición lógica.")
                    return


    elif mbr.disk_fit == "BF":
        tmp_size = size_mbr
        for particion in particiones:
            if type == 'P':
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == '1':
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == '0':
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size
                    tmp_size += size

                    ebr.part_status = '1'
                    ebr.part_fit = fit
                    ebr.part_start = tmp_size
                    ebr.part_size = size
                    ebr.part_next = 1234
                    ebr.part_name = name
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas pequeño
                elif particion.part_status == 'D':
                    tmp_size_deleted.sort()
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return
            elif type == 'E':
                if particion.part_status == '1':
                    tmp_size += particion.part_size

                # si la particion no existe, crearla y crear un EBR
                elif particion.part_status == '0':
                    
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size

                    ebr.part_status = '1'
                    ebr.part_fit = fit
                    ebr.part_start = tmp_size
                    ebr.part_size = size
                    ebr.part_next = 1234
                    ebr.part_name = name
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas pequeño
                elif particion.part_status == 'D':
                    tmp_size_deleted.sort()
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size

                        ebr.part_status = '1'
                        ebr.part_fit = fit
                        ebr.part_start = tmp_size
                        ebr.part_size = size
                        ebr.part_next = 1234
                        ebr.part_name = name
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return
                    
            elif type == 'L':
                existe_extendida = False
                for particion in particiones:
                    if particion.part_type == 'E':
                        existe_extendida = True
                        particionLogica(particion, path, size, name, 'BF', fit)
                        return
                if not existe_extendida:
                    print("\tERROR: No existe una partición extendida para crear la partición lógica.")
                    return
                        
    elif mbr.disk_fit == "WF":
        tmp_size = size_mbr
        for particion in particiones:
            if type == 'P':
                # si la particion ya existe, solamente sumar el tamaño
                if particion.part_status == '1':
                    tmp_size += particion.part_size
                # si la particion no existe, crearla
                elif particion.part_status == '0':
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size
                    tmp_size += size
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas grande
                elif particion.part_status == 'D':
                    tmp_size_deleted.sort(reverse=True)
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size
                        tmp_size += size
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return    
            elif type == 'E':
                if particion.part_status == '1':
                    tmp_size += particion.part_size

                # si la particion no existe, crearla y crear un EBR
                elif particion.part_status == '0':
                    
                    particion.part_status = '1'
                    particion.part_type = type
                    particion.part_fit = fit
                    particion.part_size = size
                    particion.part_name = name
                    particion.part_start = tmp_size

                    ebr.part_status = '1'
                    ebr.part_fit = fit
                    ebr.part_start = tmp_size
                    ebr.part_size = size
                    ebr.part_next = 1234
                    ebr.part_name = name
                    break
                # si la particion ha sido eliminada, crear la particion en el tamaño mas grande
                elif particion.part_status == 'D':
                    tmp_size_deleted.sort(reverse=True)
                    tmp_size_deleted = tmp_size_deleted[0]
                    if tmp_size_deleted >= size:
                        particion.part_status = '1'
                        particion.part_type = type
                        particion.part_fit = fit
                        particion.part_size = size
                        particion.part_name = name
                        particion.part_start = tmp_size

                        ebr.part_status = '1'
                        ebr.part_fit = fit
                        ebr.part_start = tmp_size
                        ebr.part_size = size
                        ebr.part_next = 1234
                        ebr.part_name = name
                        break
                    else:
                        print("\tERROR: No hay espacio suficiente para crear la partición.")
                        return     
                    
            elif type == 'L':
                existe_extendida = False
                for particion in particiones:
                    if particion.part_type == 'E':
                        existe_extendida = True
                        particionLogica(particion, path, size, name, 'FF', fit)
                        return
                if not existe_extendida:
                    print("\tERROR: No existe una partición extendida para crear la partición lógica.")
                    return
    # escribir los cambios en el archivo
    try:
        with open(path, "rb+") as file:
            file.write(mbr.__bytes__())
            if type == 'P':
                print("\t> FDISK: Partición primaria creada exitosamente")
            if type == 'E':
                file.seek(ebr.part_start)
                file.write(ebr.__bytes__())
                print("\t> FDISK: Partición extendida creada exitosamente")
    except Exception as e:
        print(e)
        print("\tERROR: Error al crear la partición en el disco: "+path)
        return
    
    
    
def particionLogica(particion, path, size, name, fit_disco, fit):
    #print("Entre al metodo de particion Logica")
    tmp_last_ebr = EBR()
    new_ebr_tmp = EBR()
    # Leer el archivo hasta encontrar el ultimo EBR con next = -1
    punto_partida = particion.part_start
    encontrado = True
    tmp_nombres = []
    tmp_ebrs = []
    # leer el archivo y agregar los EBR que se encuentren a una lista
    try:
        with open(path, "rb") as file:
            while encontrado:
                file.seek(punto_partida)
                ebr_data = file.read()
                tmp_last_ebr.__setstate__(ebr_data)
                if tmp_last_ebr.part_next == 1234:
                    encontrado = False
                # si no es el ultimo, buscar el siguiente
                else:
                    tmp_ebrs.append(tmp_last_ebr)
                    tmp_nombres.append(tmp_last_ebr.part_name)
                    punto_partida = tmp_last_ebr.part_next 
    except Exception as e:
        print(e)
    
    print(tmp_nombres)

    if name in tmp_nombres:
        print("\tERROR: Ya existe una partición lógica con el nombre: "+name)
        return


    if fit_disco == 'FF':
        print("First Fit")
    elif fit_disco == 'BF':
        print("Best Fit")
    elif fit_disco == 'WF':
        print("Worst Fit")
 
    # Se encontro el ultimo EBR y ahora se modifica con los datos que se traen
    tmp_last_ebr.part_status = '1'
    tmp_last_ebr.part_fit = fit
    tmp_last_ebr.part_start = punto_partida
    tmp_last_ebr.part_size = size
    tmp_last_ebr.part_next = punto_partida + size
    tmp_last_ebr.part_name = name

    new_ebr_tmp.part_status = '0'
    new_ebr_tmp.part_fit = 'WF'
    new_ebr_tmp.part_start = punto_partida + size
    new_ebr_tmp.part_size = 0
    new_ebr_tmp.part_next = 1234
    new_ebr_tmp.part_name = ''

    #escribir los cambios en el archivo
    try:
        with open(path, "rb+") as file:
            file.seek(punto_partida)
            file.write(tmp_last_ebr.__bytes__())
            file.seek(punto_partida + size)
            file.write(new_ebr_tmp.__bytes__())
            print("\t> FDISK: Partición logica creada exitosamente")
    except Exception as e:
        print(e)
        print("\tERROR: Error al crear la partición en el disco: "+path)
    

    
def imprimirMBR(path):
    mbr = MBR()
    ebr = EBR()
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

            # Si hay EBR en cualquiera de las particiones leerlos
            if mbr.mbr_Partition_1.part_type == 'E':
                file.seek(mbr.mbr_Partition_1.part_start)
                ebr_data = file.read()
                ebr.__setstate__(ebr_data)
            if mbr.mbr_Partition_2.part_type == 'E':
                file.seek(mbr.mbr_Partition_2.part_start)
                ebr_data = file.read()
                ebr.__setstate__(ebr_data)
            if mbr.mbr_Partition_3.part_type == 'E':
                file.seek(mbr.mbr_Partition_3.part_start)
                ebr_data = file.read()
                ebr.__setstate__(ebr_data)
            if mbr.mbr_Partition_4.part_type == 'E':
                file.seek(mbr.mbr_Partition_4.part_start)
                ebr_data = file.read()
                ebr.__setstate__(ebr_data)



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
    # Si hay EBR imprimirlo
    if mbr.mbr_Partition_1.part_type == 'E':
        print("EBR 1:")
        print("\tStatus: "+str(ebr.part_status))
        print("\tFit: "+str(ebr.part_fit))
        print("\tStart: "+str(ebr.part_start))
        print("\tSize: "+str(ebr.part_size))
        print("\tNext: "+str(ebr.part_next))
        print("\tName: "+str(ebr.part_name))
    if mbr.mbr_Partition_2.part_type == 'E':
        print("EBR 2:")
        print("\tStatus: "+str(ebr.part_status))
        print("\tFit: "+str(ebr.part_fit))
        print("\tStart: "+str(ebr.part_start))
        print("\tSize: "+str(ebr.part_size))
        print("\tNext: "+str(ebr.part_next))
        print("\tName: "+str(ebr.part_name))
    if mbr.mbr_Partition_3.part_type == 'E':
        print("EBR 3:")
        print("\tStatus: "+str(ebr.part_status))
        print("\tFit: "+str(ebr.part_fit))
        print("\tStart: "+str(ebr.part_start))
        print("\tSize: "+str(ebr.part_size))
        print("\tNext: "+str(ebr.part_next))
        print("\tName: "+str(ebr.part_name))
    if mbr.mbr_Partition_4.part_type == 'E':
        print("EBR 4:")
        print("\tStatus: "+str(ebr.part_status))
        print("\tFit: "+str(ebr.part_fit))
        print("\tStart: "+str(ebr.part_start))
        print("\tSize: "+str(ebr.part_size))
        print("\tNext: "+str(ebr.part_next))
        print("\tName: "+str(ebr.part_name))
    