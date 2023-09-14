from Global.Global import particiones_montadas
from Estructuras.MBR import *
from Estructuras.EBR import *

def cmd_reporte_mbr(path, id):
    #buscar en particiones montadas el id
    mbr = MBR()
    particiones =   []
    for particion in particiones_montadas:
        nombre = particion.get('id')
        if nombre == id:
            print("Se encontro la particion")
            dir = particion.get('path')
            particiones  = leer_particiones_desde_archivo(dir) 
            mbr = leer_mbr_desde_archivo(path)

    dot = "digraph G {\n"
    dot += "node [shape=plaintext]\n"
    dot += "graph [rankdir=LR]\n"
    dot += "mbr [label=<\n"
    dot += "<table border='0' cellborder='1' cellspacing='0'>\n"
    dot += "<tr><td colspan='2' bgcolor='lightblue'><b>MBR</b></td></tr>\n"
    dot += "<tr><td><b>Nombre</b></td><td><b>Valor</b></td></tr>\n"
    dot += "<tr><td>mbr_tamano</td><td>{}</td></tr>\n".format(mbr.mbr_tamano)
    dot += "<tr><td>mbr_fecha_creacion</td><td>{}</td></tr>\n".format(mbr.mbr_fecha_creacion)
    dot += "<tr><td>mbr_disk_signature</td><td>{}</td></tr>\n".format(mbr.mbr_disk_signature)
    dot += "<tr><td>disk_fit</td><td>{}</td></tr>\n".format(mbr.disk_fit)
    
    #particiones
    index1 = 0
    for part in particiones:
        index1 += 1
        dot += "<tr><td colspan='2' bgcolor='lightblue'><b>Particion {}</b></td></tr>\n".format(index1)
        dot += "<tr><td><b>Nombre</b></td><td><b>Valor</b></td></tr>\n"
        dot += "<tr><td>part_status</td><td>{}</td></tr>\n".format(part.part_status)
        dot += "<tr><td>part_type</td><td>{}</td></tr>\n".format(part.part_type)
        dot += "<tr><td>part_fit</td><td>{}</td></tr>\n".format(part.part_fit)
        dot += "<tr><td>part_start</td><td>{}</td></tr>\n".format(part.part_start)
        dot += "<tr><td>part_size</td><td>{}</td></tr>\n".format(part.part_size)
        dot += "<tr><td>part_name</td><td>{}</td></tr>\n".format(part.part_name)

        if part.part_type == 'E':
            ebr_list = leer_ebr_desde_archivo(dir, part.part_start)
            index = 0
            for ebr in ebr_list:
                index += 1
                if ebr.part_next == 1234:
                    break
                dot += "<tr><td colspan='2' bgcolor='lightyellow'><b>Particion Logica {}</b></td></tr>\n".format(index)
                dot += "<tr><td><b>Nombre</b></td><td><b>Valor</b></td></tr>\n"
                dot += "<tr><td>part_status</td><td>{}</td></tr>\n".format(ebr.part_status)
                dot += "<tr><td>part_fit</td><td>{}</td></tr>\n".format(ebr.part_fit)
                dot += "<tr><td>part_start</td><td>{}</td></tr>\n".format(ebr.part_start)
                dot += "<tr><td>part_size</td><td>{}</td></tr>\n".format(ebr.part_size)
                dot += "<tr><td>part_next</td><td>{}</td></tr>\n".format(ebr.part_next)
                dot += "<tr><td>part_name</td><td>{}</td></tr>\n".format(ebr.part_name)
                
        else:
            continue
                
    
    dot += "</table>\n"
    dot += ">];\n"
    dot += "}"
    print(dot)


def leer_ebr_desde_archivo(path, inicio):
    tmp_size = inicio
    ebr_list = []
    with open(path, "rb+") as file:
        while True:
            file.seek(tmp_size)
            ebr_data = file.read()  # Leer EBR
            ebr = EBR()
            ebr_list.append(ebr)
            ebr.__setstate__(ebr_data)
            if ebr.part_next == 1234:
                break
            tmp_size = ebr.part_next
    return ebr_list

def leer_particiones_desde_archivo(path):
    try:
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

    return particiones

def leer_mbr_desde_archivo(path):
    mbr = MBR()
    try:

        with open(path, "rb") as file:
            mbr_data = file.read()
            mbr.mbr_tamano = struct.unpack("<i", mbr_data[0:4])[0]
            mbr.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
            mbr.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
            mbr.disk_fit = mbr_data[12:14].decode("utf-8")
    except Exception as e:
        print(e)

    return mbr



def cmd_reporte_disk(path, id):
    #buscar en particiones montadas el id
    mbr = MBR()
    particiones =   []
    for particion in particiones_montadas:
        nombre = particion.get('id')
        if nombre == id:
            print("Se encontro la particion")
            dir = particion.get('path')
            particiones  = leer_particiones_desde_archivo(dir) 
            mbr = leer_mbr_desde_archivo(path)

    size_disco = mbr.mbr_tamano

    # hacer la representación visual del disco con tamaño de particiones y espacio libre

    dot = "digraph G {\n"
    dot += "node [shape=plaintext]\n"
    dot += "graph [rankdir=LR]\n"
    dot += "disk [label=<\n"
    dot += "<table border='0' cellborder='1' cellspacing='0' cellpadding='50'>\n"
    dot += "<tr><td colspan='2' bgcolor='lightblue'><b>MBR ocupa el {}% del disco</b> </td>\n".format(126*100/size_disco)

    for part in particiones:
        if part.part_type == 'E':
            dot += "<td colspan='2' bgcolor='lightblue'><b>Partición Extendida</b><br/><b>Ocupa el {}% del disco</b></td>\n".format(part.part_size*100/size_disco)
            ebr_list = leer_ebr_desde_archivo(dir, part.part_start)
            dot += "<td>\n<table border='0' cellborder='1' cellspacing='0' cellpadding='50'><tr>"
            for ebr in ebr_list:
                if ebr.part_next == 1234:
                    break
                dot += "<td bgcolor='lightyellow'>"
                dot += "<b>Partición Lógica</b><br/>"
                dot += "<b>Ocupa el {}% del disco</b><br/>".format(ebr.part_size*100/size_disco)
                dot += "</td>"
            dot += "</tr></table>\n</td>\n"
        else:
            # Agregar celdas para particiones primarias
            dot += "<td colspan='2' bgcolor='lightblue'><b>Partición {}</b><br/><b>Ocupa el {}% del disco</b></td>\n".format(part.part_type, part.part_size*100/size_disco)

    dot += "</tr>\n"
    dot += "</table>\n"
    dot += ">];\n"
    dot += "}"

    print(dot)