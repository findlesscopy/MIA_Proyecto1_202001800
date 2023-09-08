from Analizadores.analizador_sintactico import parse

# execute -path="/home/Disco1.dsk"
# mkdisk -size=3000 -unit=K -path="./home/user/Disco1.dsk"
# rmdisk -path="./home/user/Disco1.dsk"
# fdisk -size=300 -path="/home/Disco1.dsk" -name="Particion1"
# mount -path="/home/Disco2.dsk" -name="Part1"
# mount -name="Part3" -path="/home/Disco3.dsk"
# unmount -id="061Disco1"
# mkfs -type=full -id="061Disco1" -fs=3fs

# login -user="root" -pass="123" -id="061Disco1"
# logout
# mkgrp -name="Grupo1"
# rmgrp -name="usuarios"
# mkusr -user="user1" -pass="usuario" -grp="usuarios2"
# rmusr -user="user1"

# mkfile -size=15 -path="/home/user/docs/a.txt" -r
# mkfile -path="/home/user/docs/b.txt" -r -cont="/home/Documents/b.txt"
# cat -file1="/home/a.txt" -file2="/home/b.txt" -file3="/home/c.txt"
# mkdisk -size=10 -path="./home/user/Disco1.dsk"
# fdisk -size=3 -path="./home/user/Disco1.dsk" -name="Particion1" 
# fdisk -size=1000 -unit=K -path="./home/user/Disco1.dsk" -name="Particion1"
# fdisk -size=1000 -path="./home/user/Disco1.dsk" -unit=K -name="Particion3"
# fdisk -unit=K -size= -path="./home/user/Disco1.dsk" -name="Particion4"
# mkdisk -size=10 -path="./home/user/Disco1.dsk"
entrada = '''
mkdisk -size=75 -unit=M -path="./home/Disco1.dsk"
fdisk -type=P -unit=M -name="Part1" -size=15 -path="./home/Disco1.dsk"
fdisk -type=P -unit=M -name="Part2" -size=20 -path="./home/Disco1.dsk"
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