import sqlite3 as sqlite
bbdd="base_datos_morado_reto7.db"

def crear_tabla():
    con = sqlite.connect(bbdd)
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        correo TEXT NOT NULL,
        usuario TEXT PRAMARY KEY NOT NULL,
        contraseña TEXT NOT NULL
        )
    """)
    con.close()
    return None

#para añadir valores
def insert_usuarios(nombre:str,apellido:str,correo:str,usuario:str,contraseña:str)->str:
    try:
        con = sqlite.connect(bbdd)
        cur = con.cursor()
        cur.execute("""INSERT INTO usuarios VALUES (?,?,?,?,?)
            """, (nombre,apellido,correo,usuario,contraseña))
        con.commit()
        msg=True
    except:
        con.rollback()
        msg=False
    finally:
        con.close()
    return msg

def nombre_existe(usuario:str):
    con = sqlite.connect(bbdd)
    cur = con.cursor()
    cur.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,)) 
    email_res = cur.fetchone()
    con.close()
    return email_res is not None

def comprobar_contraseña(usuario:str,contraseña:str):
    con=sqlite.connect(bbdd)
    cur=con.cursor()
    cur.execute("SELECT contraseña FROM usuarios WHERE usuario = ?",
                (usuario,))
    contra=cur.fetchone()[0]
    con.close()
    return contraseña == contra




# MODELO ADQUISICIÓN (datos empresa)

def crear_tabla_empresa_adquisicion():
    """Crea la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd)
    cur = con.cursor() 
    cur.execute("""CREATE TABLE IF NOT EXISTS empresa_adquisicion(
        usuario TEXT NOT NULL,
        empresa TEXT NOT NULL,
        prediccion TEXT NOT NULL
        )
    """)
    con.close()

    return None

def guardar_empresa_adquisicion(usuario:str, empresa:str, prediccion:str):
    """Inserta busquedas 

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("""INSERT INTO empresa_adquisicion VALUES (?, ?, ?)""", (usuario, empresa, prediccion))
    con.commit()
    con.close()

    return None


def ver_empresa_adquisicion(usuario:str):
    """Consulta contenido de la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("SELECT empresa, prediccion FROM empresa_adquisicion WHERE usuario = ?", (usuario,))
    resultado = cur.fetchall()
    con.close()
    
    return resultado



###################################################

# MODELO VALORACION (datos empresa)

def crear_tabla_empresa_valoracion():
    """Crea la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd)
    cur = con.cursor() 
    cur.execute("""CREATE TABLE IF NOT EXISTS empresa_valoracion(
        usuario TEXT NOT NULL,
        empresa TEXT NOT NULL,
        prediccion FLOAT NOT NULL
        )
    """)
    con.close()

    return None

def guardar_empresa_valoracion(usuario:str, empresa:str, prediccion:float):
    """Inserta busquedas 

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("""INSERT INTO empresa_valoracion VALUES (?, ?, ?)""", (usuario, empresa, prediccion))
    con.commit()
    con.close()

    return None


def ver_empresa_valoracion(usuario:str):
    """Consulta contenido de la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("SELECT empresa, prediccion FROM empresa_valoracion WHERE usuario = ?", (usuario,))
    resultado = cur.fetchall()
    con.close()
    
    return resultado