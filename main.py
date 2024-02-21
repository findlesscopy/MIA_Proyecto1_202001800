from Analizadores.analizador_sintactico import parse

# del archivo de entrada Facil
# mkdisk -size=50 -unit=M -path="./home/archivos/Disco1.dsk" -fit=FF
# mkdisk -unit=K -size=51200 -path="./home/archivos/Disco2.dsk" -fit=BF
# mkDisk -size=10 -path="./home/archivos/Disco3.dsk"
# mkdisk -size=51200 -path="./home/archivos/mis archivos/Disco4.dsk" -unit=K
# mkDisk -size=20 -path="./home/archivos/mis archivos/Disco5.dsk" -unit=M -fit=WF
# funcionan
# error de disco
# mkdisk -param=x -size=30 -path="./home/archivos/Disco.dsk" 
# ELMINACION DE DISCOS
# rmDisk -path="./home/Disco3.dsk" # Error no existe
# rmDisk -path="./home/archivos/Disco3.dsk"
# RMDISK -path="./home/archivos/mis archivos/Disco4.dsk"
#CREACION DE PARTICIONES
#Particiones en el disco1 (funcionan)
# fdisk -type=P -unit=K -name="Part1" -size=7680 -path="./home/archivos/Disco1.dsk" -fit=BF 
# fdisk -type=E -unit=K -name="Part2" -size=7680 -path="./home/archivos/Disco1.dsk" -fit=FF
# fdisk -type=E -unit=K -name="Part3" -size=7680 -path="./home/archivos/Disco1.dsk" -fit=WF 
# fdisk -type=P -unit=K -name="Part3" -size=7680 -path="./home/archivos/Disco1.dsk" -fit=WF
# fdisk -type=P -unit=K -name="Part4" -size=7680 -path="./home/archivos/Disco1.dsk" -fit=BF
# FDISK -type=L -unit=k -name="Part5" -size=1280 -path="./home/archivos/Disco1.dsk" -fit=BF 
# fdisk -type=L -unit=K -name="Part6" -size=1280 -path="./home/archivos/Disco1.dsk" -fit=WF
# fdisk -type=L -unit=K -name="Part7" -size=1280 -path="./home/archivos/Disco1.dsk" -fit=wf
# fdisk -type=L -unit=K -name="Part8" -size=1280 -path="./home/archivos/Disco1.dsk" -fit=FF
# fdisk -type=L -unit=K -name="Part9" -size=1280 -path="./home/archivos/Disco1.dsk" -fit=BF
# fdisk -type=L -unit=K -name="Part9" -size=1024 -path="./home/archivos/Disco1.dsk" -fit=BF

# rep -name=mbr -path="./home/archivos/Disco2.dsk" -id="001Disco2"

# mkfs -type=full -id="001Disco2" -fs=2fs

# rep -name=sb -path="./home/archivos/Disco2.dsk" -id="001Disco2"

# login -user="root" -pass="123" -id="001Disco2"

# mkgrp -name="Grupo1"

# mkusr -user="Jose" -pass="asd" -grp="Grupo1"

# rmusr -user="Jose"

# rmgrp -name="Grupo1"
#Particiones en el disco2


entrada = '''
#Calificacion MIA 2023 - Parte 1

#CREACION DE DISCOS

#Disco con primer ajuste
mkdisk -size=75 -unit=M -path="/tmp/d1.dsk"

#Tamaño de 50mb
mkdisk -unit=M -path="/tmp/d2.dsk" -fit=BF -size=50

#Debe crear discos en MB
mkdisk -size=101 -path="/tmp/d3.dsk" -fit=WF            	 
mkdisk -size=1 -path="/tmp/eliminar 1.dsk"
mkdisk -size=1 -path="/tmp/eliminar 2.dsk"

#CREACION DE PARTICIONES PRIMARIAS Y EXTENDIDAS

#Crear particiones d1.dsk
fdisk -type=P -unit=M -name="Part1" -size=25 -path="/tmp/d1.dsk"
fdisk -type=P -unit=M -name="Part2" -size=25 -path="/tmp/d1.dsk"
fdisk -type=P -unit=M -name="Part3" -size=20 -path="/tmp/d1.dsk"
fdisk -type=P -unit=M -name="Part4" -size=5 -path="/tmp/d1.dsk"

#Crear particiones d2.dsk
#Error, no existe extendida
fdisk -type=L -unit=M -name="Part6" -size=25 -path="/tmp/d2.dsk"
#Ocupa los 10MB del disco
fdisk -type=E -unit=M -name="Part1" -size=10 -path="/tmp/d2.dsk"  -fit=FF
#Error, ya existe una extendida
fdisk -type=E -unit=M -name="Part7" -size=25 -path="/tmp/d2.dsk"  -fit=WF
fdisk -type=L -unit=K -name="Part2" -size=1024 -path="/tmp/d2.dsk"
fdisk -type=L -unit=K -name="Part3" -size=1024 -path="/tmp/d2.dsk"
fdisk -type=L -unit=K -name="Part4" -size=1024 -path="/tmp/d2.dsk"

#Crear particiones d3.dsk
fdisk -type=E -unit=M -name="Part1" -size=25 -path="/tmp/d3.dsk"  -fit=BF
fdisk -type=P -unit=M -name="Part2" -size=25 -path="/tmp/d3.dsk"  -fit=BF
fdisk -type=P -unit=M -name="Part3" -size=25 -path="/tmp/d3.dsk"  -fit=BF
fdisk -type=P -unit=M -name="Part4" -size=25 -path="/tmp/d3.dsk"  -fit=BF
#error, ya existen 4 particiones
fdisk -type=P -unit=M -name="Part1" -size=25 -path="/tmp/d3.dsk"  -fit=BF
fdisk -type=L -unit=K -name="Part5" -size=1024 -path="/tmp/d3.dsk"  -fit=BF
fdisk -type=L -unit=K -name="Part6" -size=1024 -path="/tmp/d3.dsk"  -fit=BF

#MOUNT
mount -path="/tmp/d1.dsk" -name="Part1"
mount -path="/tmp/d2.dsk" -name="Part1"
mount -path="/tmp/d3.dsk" -name="Part1"


#CAMBIO DE TAMAÑO  DE PARTICIONES

#ELIMINACION DE PARTICIONES PRIMARIAS
fdisk -delete=full -name="Part2" -path="/tmp/d1.dsk" -size=25

#ELIMINACION DE PARTICIONES LOGICAS
fdisk -delete=full -name="Part3" -path="/tmp/d2.dsk" -size=25

#ELIMINACION DE PARTICIONES EXTENDIDAS
fdisk -delete=full -name="Part1" -path="/tmp/d3.dsk" -size=25

#ELIMINACION DE DISCOS

#Debe de mostrar error por no existir
rmdisk -path="/home/a eliminar disco/no_existo.dsk"
rmdisk -path="/tmp/eliminar 1.dsk"
rmdisk -path="/tmp/eliminar 2.dsk"


#UNMOUNT
unmount -id="001d3"


#Cerrar el programa para validar
#Debe dar error porque no deberia estar montado nada
pause

''' 

def inicio():
        while True:
            print("--------===Bienvenido a la consola de comandos===--------")
            print("->Ingrese un comando<-")

            print("->Si desea terminar con la aplicación ingrese \"exit\"<-")
            comando = input("->")
            if comando == "exit":
                break
            else:
                parse(comando)
            input("\nPresione Enter para continuar....")

if __name__ == "__main__":
    inicio()
    #parse(entrada)