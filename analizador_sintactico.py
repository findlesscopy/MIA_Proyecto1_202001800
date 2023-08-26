import ply.yacc as yacc
from lexer import *

precedence = ()

def p_init(t):
    'init : list_commands'
    t[0] = t[1]

def p_list_commands(t):
    '''list_commands : list_commands commands
                    | commands'''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_commands(t):
    '''commands : command_execute
                | command_mkdisk
                | command_rmdisk
                | command_fdisk
                | command_mount
                | command_unmount
                | command_mkfs
                | command_login
                | command_logout
                | command_mkgrp
                | command_rmgrp
                | command_mkusr
                | command_rmusr
                | command_mkfile
                | command_cat'''
    t[0] = t[1]

def p_command_execute(t):
    'command_execute : EXECUTE GUION PATH IGUAL CADENA '
    # t[0] : t[1]
    print(t[5])
    t[0] = t[1]

def p_command_mkdisk(t):
    '''command_mkdisk : MKDISK parameters_mkdisk'''
    #print(t[2])
    _size, _path, _unit, _fitsym = None, None, None, None
    for dict in t[2]:
        if 'size' in dict:
            _size = dict['size']
        elif 'path' in dict:
            _path = dict['path']
        elif 'unit' in dict:
            _unit = dict['unit']
        elif 'fitsym' in dict:
            _fitsym = dict['fitsym']

    _unit = _unit if _unit != None else 'M'
    _fitsym = _fitsym if _fitsym != None else 'FF'
    print(_size, _path, _unit, _fitsym)
    t[0] = t[1]
    

def p_parameters_mkdisk(t):
    '''parameters_mkdisk : parameters_mkdisk parameter_mkdisk
                        | parameter_mkdisk'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_mkdisk(t):
    '''parameter_mkdisk : param_size
                        | param_path
                        | param_unit
                        | param_fit'''
    t[0] = t[1]

def p_command_rmdisk(t):
    'command_rmdisk : RMDISK GUION PATH IGUAL CADENA'
    print(t[5])
    t[0] = t[1]

def p_command_fdisk(t):
    'command_fdisk : FDISK parameters_fdisk'
    _size, _path, _name, _unit, _type, _fitsym, _delete, _add = None, None, None, None, None, None, None, None
    for dict in t[2]:
        if 'size' in dict:
            _size = dict['size']
        elif 'path' in dict:
            _path = dict['path']
        elif 'name' in dict:
            _name = dict['name']
        elif 'unit' in dict:
            _unit = dict['unit']
        elif 'type' in dict:
            _type = dict['type']
        elif 'fitsym' in dict:
            _fitsym = dict['fitsym']
        elif 'delete' in dict:
            _delete = dict['delete']
        elif 'add' in dict:
            _add = dict['add']

    _unit = _unit if _unit != None else 'K'
    _type = _type if _type != None else 'P'
    _fitsym = _fitsym if _fitsym != None else 'WF'
    print(_size, _path, _name, _unit, _type, _fitsym, _delete, _add)
    t[0] = t[1]

def p_parameters_fdisk(t):
    '''parameters_fdisk : parameters_fdisk parameter_fdisk
                        | parameter_fdisk'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_fdisk(t):
    '''parameter_fdisk : param_size
                | param_path
                | param_unit
                | param_name
                | param_type
                | param_fit
                | param_delete
                | param_add'''
    t[0] = t[1]

def p_command_mount(t):
    'command_mount : MOUNT parameters_mount'
    _path, _name = None, None
    for dict in t[2]:
        if 'path' in dict:
            _path = dict['path']
        elif 'name' in dict:
            _name = dict['name']

    print(_path, _name)
    t[0] = t[1]

def p_parameters_mount(t):
    '''parameters_mount : parameters_mount parameter_mount
                        | parameter_mount'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_mount(t):
    '''parameter_mount : param_path
                | param_name'''
    t[0] = t[1]

def p_command_unmount(t):
    'command_unmount : UNMOUNT GUION ID_DISK IGUAL CADENA'
    print(t[5])
    t[0] = t[1]

def p_command_mkfs(t):
    'command_mkfs : MKFS parameters_mkfs'
    _id, _type, _fs= None, None, None
    for dict in t[2]:
        if 'id' in dict:
            _id = dict['id']
        elif 'type' in dict:
            _type = dict['type']
        elif 'fs' in dict:
            _fs = dict['fs']

    _fs = _fs if _fs != None else '2FS'

    print(_id, _type, _fs)
    t[0] = t[1]

def p_parameters_mkfs(t):
    '''parameters_mkfs : parameters_mkfs parameter_mkfs
                        | parameter_mkfs'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_mkfs(t):
    '''parameter_mkfs : param_id
                | param_type
                | param_fs'''
    t[0] = t[1]

def p_command_login(t):
    'command_login : LOGIN parameters_login'
    _user, _password, _id= None, None, None
    for dict in t[2]:
        if 'user' in dict:
            _user = dict['user']
        elif 'password' in dict:
            _password = dict['password']
        elif 'id' in dict:
            _id = dict['id']

    print(_user, _password, _id)
    t[0] = t[1]

def p_parameters_login(t):
    '''parameters_login : parameters_login parameter_login
                        | parameter_login'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_login(t):
    '''parameter_login : param_user
                | param_password
                | param_id'''
    t[0] = t[1]

def p_command_logout(t):
    'command_logout : LOGOUT'
    t[0] = t[1]

def p_command_mkgrp(t):
    'command_mkgrp : MKGRP GUION NAME IGUAL CADENA'
    print(t[5])
    t[0] = t[1]

def p_command_rmgrp(t):
    'command_rmgrp : RMGRP GUION NAME IGUAL CADENA'
    print(t[5])
    t[0] = t[1]

def p_command_mkusr(t):
    'command_mkusr : MKUSR parameters_mkusr'
    _user, _password, _grp= None, None, None
    for dict in t[2]:
        if 'user' in dict:
            _user = dict['user']
        elif 'password' in dict:
            _password = dict['password']
        elif 'grp' in dict:
            _grp = dict['grp']

    print(_user, _password, _grp)
    t[0] = t[1]

def p_parameters_mkusr(t):
    '''parameters_mkusr : parameters_mkusr parameter_mkusr
                        | parameter_mkusr'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_mkusr(t):
    '''parameter_mkusr : param_user
                | param_password
                | param_grp'''
    t[0] = t[1]

def p_command_rmusr(t):
    'command_rmusr : RMUSR GUION USER IGUAL CADENA'
    print(t[5])
    t[0] = t[1]

def p_command_mkfile(t):
    'command_mkfile : MKFILE parameters_mkfile'
    _path, _r, _size, _cont= None, None, None, None
    for dict in t[2]:
        if 'path' in dict:
            _path = dict['path']
        elif 'r' in dict:
            _r = dict['r']
        elif 'size' in dict:
            _size = dict['size']
        elif 'cont' in dict:
            _cont = dict['cont']

    print(_path, _r, _size, _cont)
    t[0] = t[1]

def p_parameters_mkfile(t):
    '''parameters_mkfile : parameters_mkfile parameter_mkfile
                        | parameter_mkfile'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
        #print(t[0])
    else:
        t[0] = [t[1]]
        #print(t[0])

def p_parameter_mkfile(t):
    '''parameter_mkfile : param_path
                | param_r
                | param_size
                | param_cont'''
    t[0] = t[1]

def p_command_cat(t):
    '''command_cat : CAT parameters_cat'''
    var_file = None
    for dict in t[2]:
        if 'file' in dict:
            var_file = dict['file']

    print(var_file)
    t[0] = t[1]

def p_parameters_cat(t):
    '''parameters_cat : parameters_cat parameter_cat
                        | parameter_cat'''
    if len(t) == 3:
        t[0] = t[1]+ [t[2]]
    else:
        t[0] = [t[1]]

def p_parameter_cat(t):
    '''parameter_cat : param_file'''
    t[0] = t[1]
    
def p_param_size(t):
    'param_size : GUION SIZE IGUAL ENTERO'
    t[0] = {'size' : t[4] }

def p_param_path(t):
    'param_path : GUION PATH IGUAL CADENA'
    t[0] = {'path' : t[4] }

def p_param_unit(t):
    'param_unit : GUION UNIT IGUAL UNIDAD'
    t[0] = {'unit' : t[4] }

def p_param_fit(t):
    'param_fit : GUION FIT IGUAL FITSYM'
    t[0] = {'fitsym' : t[4] }

def p_param_name(t):
    'param_name : GUION NAME IGUAL CADENA'
    t[0] = {'name' : t[4] }

def p_param_type(t):
    '''param_type : GUION TYPE IGUAL TIPO
                | GUION TYPE IGUAL FULL'''
    t[0] = {'type' : t[4] }

def p_param_delete(t):
    'param_delete : GUION DELETE IGUAL FULL'
    t[0] = {'delete' : t[4] }

def p_param_add(t):
    'param_add : GUION ADD IGUAL ENTERO'
    t[0] = {'add' : t[4] }

def p_param_id(t):
    'param_id : GUION ID_DISK IGUAL CADENA'
    t[0] = {'id' : t[4] }

def p_param_fs(t):
    'param_fs : GUION FS_DISK IGUAL FS'
    t[0] = {'fs' : t[4] }

def p_param_user(t):
    'param_user : GUION USER IGUAL CADENA'
    t[0] = {'user' : t[4] }

def p_param_password(t):
    'param_password : GUION PASSWORD IGUAL CADENA'
    t[0] = {'password' : t[4] }

def p_param_grp(t):
    'param_grp : GUION GRP IGUAL CADENA'
    t[0] = {'grp' : t[4] }

def p_param_r(t):
    'param_r : GUION ERRE'
    t[0] = {'r' : True }

def p_param_cont(t):
    'param_cont : GUION CONT IGUAL CADENA'
    t[0] = {'cont' : t[4] }

def p_param_file(t):
    'param_file : GUION FILE ENTERO IGUAL CADENA'
    t[0] = {'file' : t[5] }

def p_error(t):
    global errores
    if t:
        errores.append("Error sintáctico en '%s'" % t.value)
    else:
        errores.append("Error sintáctico en EOF")

# llevarla al main
def parse(input):
    global errores
    global parser
    parser = yacc.yacc()
    lexer.lineno = 1
    return parser.parse(input)

entrada = '''
execute -path="/home/Disco1.dsk"
mkdisk -size=300 -path="/home/Disco1.dsk" -unit=M -fit=WF
rmdisk -path="/home/Disco1.dsk"
fdisk -size=300 -path="/home/Disco1.dsk" -name="Particion1"
mount -path="/home/Disco2.dsk" -name="Part1"
mount -name="Part3" -path="/home/Disco3.dsk"
unmount -id="061Disco1"
mkfs -type=full -id="061Disco1" -fs=3fs

login -user="root" -pass="123" -id="061Disco1"
logout
mkgrp -name="Grupo1"
rmgrp -name="usuarios"
mkusr -user="user1" -pass="usuario" -grp="usuarios2"
rmusr -user="user1"

mkfile -size=15 -path="/home/user/docs/a.txt" -r
mkfile -path="/home/user/docs/b.txt" -r -cont="/home/Documents/b.txt"
cat -file1="/home/a.txt" -file2="/home/b.txt" -file3="/home/c.txt"
''' 
parse(entrada)