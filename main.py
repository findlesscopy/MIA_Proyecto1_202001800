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
#Particiones en el disco2


entrada = '''
mkdisk -unit=K -size=51200 -path="./home/archivos/Disco2.dsk" -fit=BF

fdisk -type=L -unit=K -name="Part11" -size=10240 -path="./home/archivos/Disco2.dsk" -fit=BF 
fdisk -type=L -unit=K -name="Part12" -size=10240 -path="./home/archivos/Disco2.dsk" -fit=BF 
fDisk -type=P -unit=K -name="Part11" -size=10240 -path="./home/archivos/Disco2.dsk" -fit=BF 
fDisk -type=P -unit=M -name="Part12" -size=5 -path="./home/archivos/Disco2.dsk" -fit=FF 
fDisk -type=P -unit=K -name="Part13" -size=5120 -path="./home/archivos/Disco2.dsk" -fit=WF 
fdisk -type=E -unit=M -name="Part14" -size=20 -path="./home/archivos/Disco2.dsk" 

fdisk -type=L -unit=K -name="Part15" -size=1536 -path="./home/archivos/Disco2.dsk" 
fdisk -type=L -unit=K -name="Part15" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part17" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part18" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part19" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part20" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part21" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part22" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part23" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part24" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part25" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part26" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF
fdisk -type=L -unit=K -name="Part27" -size=1536 -path="./home/archivos/Disco2.dsk" -fit=FF 
''' 

# def inicio():
#         while True:
#             print("--------===Bienvenido a la consola de comandos===--------")
#             print("->Ingrese un comando<-")

#             print("->Si desea terminar con la aplicación ingrese \"exit\"<-")
#             comando = input("->")
#             if comando == "exit":
#                 break
#             else:
#                 parse(comando)
#             input("\nPresione Enter para continuar....")

if __name__ == "__main__":
    #inicio()
    parse(entrada)