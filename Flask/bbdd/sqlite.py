import sqlite3 as sqlite
bbdd="prueba_reto7.db"

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
    cur.execute("SELECT nombre FROM usuarios WHERE nombre = ?", (usuario,)) 
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