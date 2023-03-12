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
######## antes de entregar borrar!!!!!!!!!!!!!!
def consultar_usu():
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("SELECT * FROM usuarios")
    usu= cur.fetchall()
    con.close()  

    return usu

###############

# MODELO ADQUISICIÓN (datos manualmente)

def crear_tabla_manual_adquisicion():
    """Crea la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd)
    cur = con.cursor() 
    cur.execute("""CREATE TABLE IF NOT EXISTS manual_adquisicion(
        usuario TEXT NOT NULL,
        Anos_en_Mercado INTEGER NOT NULL,
        Cash_flow_mil_EUR_2021 FLOAT NOT NULL,
        EBITDA_mil_EUR_2021 FLOAT NOT NULL,
        Inmovilizado_mil_EUR_2021 FLOAT NOT NULL,
        Fondos_propios_mil_EUR_2021 FLOAT NOT NULL,
        Valor_agregado_mil_EUR_2021 FLOAT NOT NULL,
        Total_pasivo_ratio FLOAT NOT NULL,
        Inmovilizado_mil_EUR_ratio FLOAT NOT NULL,
        Capital_suscrito_mil_EUR_2021 FLOAT NOT NULL,
        Capital_social_mil_EUR FLOAT NOT NULL,
        Gastos_financieros_mil_EUR_ratio FLOAT NOT NULL,
        Gastos_de_personal_mil_EUR_2021 FLOAT NOT NULL,
        Resultado_financiero_mil_EUR_ratio FLOAT NOT NULL,
        Total_pasivo_y_capital_propio_mil_EUR_2021 FLOAT NOT NULL,
        Total_activo_mil_EUR_2021 FLOAT NOT NULL,
        Gastos_financieros_mil_EUR_2021 FLOAT NOT NULL,
        Pasivo_fijo_mil_EUR_2021 FLOAT NOT NULL,
        total_funding FLOAT NOT NULL,
        prediccion FLOAT NOT NULL
        )
    """)
    con.close()

    return None

def guardar_manual_adquisicion(usuario:str, Anos_en_Mercado:int, Cash_flow_mil_EUR_2021:float, EBITDA_mil_EUR_2021:float, Inmovilizado_mil_EUR_2021:float,
                               Fondos_propios_mil_EUR_2021:float, Valor_agregado_mil_EUR_2021:float, Total_pasivo_ratio:float, Inmovilizado_mil_EUR_ratio:float,
                               Capital_suscrito_mil_EUR_2021:float, Capital_social_mil_EUR:float, Gastos_financieros_mil_EUR_ratio:float, Gastos_de_personal_mil_EUR_2021:float,
                               Resultado_financiero_mil_EUR_ratio:float, Total_pasivo_y_capital_propio_mil_EUR_2021:float, Total_activo_mil_EUR_2021:float, Gastos_financieros_mil_EUR_2021:float,
                               Pasivo_fijo_mil_EUR_2021:float,  total_funding:float, prediccion:float):
    """Inserta busquedas 

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("""INSERT INTO manual_adquisicion VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (usuario, Anos_en_Mercado, Cash_flow_mil_EUR_2021, EBITDA_mil_EUR_2021, Inmovilizado_mil_EUR_2021,
                                                                            Fondos_propios_mil_EUR_2021, Valor_agregado_mil_EUR_2021, Total_pasivo_ratio, Inmovilizado_mil_EUR_ratio,
                                                                            Capital_suscrito_mil_EUR_2021, Capital_social_mil_EUR, Gastos_financieros_mil_EUR_ratio, Gastos_de_personal_mil_EUR_2021,
                                                                            Resultado_financiero_mil_EUR_ratio, Total_pasivo_y_capital_propio_mil_EUR_2021, Total_activo_mil_EUR_2021, Gastos_financieros_mil_EUR_2021,
                                                                            Pasivo_fijo_mil_EUR_2021, total_funding, prediccion
                                                                            ))
    con.commit()
    con.close()

    return None


def ver_manual_adquisicion(usuario:str):
    """Consulta contenido de la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("SELECT Anos_en_Mercado, Cash_flow_mil_EUR_2021, EBITDA_mil_EUR_2021, Inmovilizado_mil_EUR_2021,Fondos_propios_mil_EUR_2021, Valor_agregado_mil_EUR_2021, Total_pasivo_ratio, Inmovilizado_mil_EUR_ratio, Capital_suscrito_mil_EUR_2021, Capital_social_mil_EUR, Gastos_financieros_mil_EUR_ratio, Gastos_de_personal_mil_EUR_2021, Resultado_financiero_mil_EUR_ratio, Total_pasivo_y_capital_propio_mil_EUR_2021, Total_activo_mil_EUR_2021, Gastos_financieros_mil_EUR_2021, Pasivo_fijo_mil_EUR_2021, total_funding, prediccion FROM manual_adquisicion WHERE usuario = ?", (usuario,))
    resultado = cur.fetchall()
    con.close()
    
    return resultado


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
        prediccion FLOAT NOT NULL
        )
    """)
    con.close()

    return None

def guardar_empresa_adquisicion(usuario:str, empresa:str, prediccion:float):
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

# MODELO VALORACIÓN (datos manualmente)

def crear_tabla_manual_valoracion():
    """Crea la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd)
    cur = con.cursor() 
    cur.execute("""CREATE TABLE IF NOT EXISTS manual_valoracion(
        usuario TEXT NOT NULL,
        Precio_Venta FLOAT NOT NULL,
        Activo_circulante_mil_EUR_2021 FLOAT NOT NULL,
        Fondos_propios_mil_EUR_2021 FLOAT NOT NULL,
        Total_activo_mil_EUR_2021 FLOAT NOT NULL,
        Total_pasivo_y_capital_propio_mil_EUR_2021 FLOAT NOT NULL,
        Fondo_de_maniobra_mil_EUR_2021 FLOAT NOT NULL,
        Deudores_mil_EUR_2021 FLOAT NOT NULL,
        Beneficio_neto_mil_EUR FLOAT NOT NULL,
        Ingresos_de_explotacion_mil_EUR_2021 FLOAT NOT NULL,
        Importe_neto_Cifra_de_Ventas_mil_EUR_2021 FLOAT NOT NULL,
        Pasivo_liquido_mil_EUR_2021 FLOAT NOT NULL,
        Total_pasivo_2021 FLOAT NOT NULL,
        total_funding FLOAT NOT NULL,
        Pasivo_fijo_mil_EUR_2021 FLOAT NOT NULL,
        Gastos_financieros_mil_EUR_2021 FLOAT NOT NULL,
        Resultado_Explotacion_mil_EUR_2021 FLOAT NOT NULL,
        EBIT_mil_EUR_2021 FLOAT NOT NULL,
        PER FLOAT NOT NULL,
        Resultado_del_Ejercicio_mil_EUR_2021 FLOAT NOT NULL,
        Result_ordinarios_antes_Impuestos_mil_EUR_2021 FLOAT NOT NULL,
        Importe_neto_Cifra_de_Ventas_mil_EUR_ratio FLOAT NOT NULL,
        prediccion FLOAT NOT NULL
        )
    """)
    con.close()

    return None

def guardar_manual_valoracion(usuario:str, Precio_Venta:float, Activo_circulante_mil_EUR_2021:float, Fondos_propios_mil_EUR_2021:float, Total_activo_mil_EUR_2021:float, Total_pasivo_y_capital_propio_mil_EUR_2021:float,
                               Fondo_de_maniobra_mil_EUR_2021:float, Deudores_mil_EUR_2021:float, Beneficio_neto_mil_EUR:float, Ingresos_de_explotacion_mil_EUR_2021:float, Importe_neto_Cifra_de_Ventas_mil_EUR_2021:float,
                               Pasivo_liquido_mil_EUR_2021:float, Total_pasivo_2021:float, total_funding:float, Pasivo_fijo_mil_EUR_2021:float, Gastos_financieros_mil_EUR_2021:float, Resultado_Explotacion_mil_EUR_2021:float,
                               EBIT_mil_EUR_2021:float, PER:float, Resultado_del_Ejercicio_mil_EUR_2021:float, Result_ordinarios_antes_Impuestos_mil_EUR_2021:float, Importe_neto_Cifra_de_Ventas_mil_EUR_ratio:float, prediccion:float):
    """Inserta busquedas 

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("""INSERT INTO manual_valoracion VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (usuario, Precio_Venta, Activo_circulante_mil_EUR_2021, Fondos_propios_mil_EUR_2021, Total_activo_mil_EUR_2021, Total_pasivo_y_capital_propio_mil_EUR_2021,
                                                                  Fondo_de_maniobra_mil_EUR_2021, Deudores_mil_EUR_2021, Beneficio_neto_mil_EUR, Ingresos_de_explotacion_mil_EUR_2021, Importe_neto_Cifra_de_Ventas_mil_EUR_2021,
                                                                  Pasivo_liquido_mil_EUR_2021, Total_pasivo_2021, total_funding, Pasivo_fijo_mil_EUR_2021, Gastos_financieros_mil_EUR_2021, Resultado_Explotacion_mil_EUR_2021,
                                                                  EBIT_mil_EUR_2021, PER, Resultado_del_Ejercicio_mil_EUR_2021, Result_ordinarios_antes_Impuestos_mil_EUR_2021, Importe_neto_Cifra_de_Ventas_mil_EUR_ratio, prediccion))
    con.commit()
    con.close()

    return None


def ver_manual_valoracion(usuario:str):
    """Consulta contenido de la tabla busquedas

    Returns:
        _type_: _description_
    """
    con = sqlite.connect(bbdd) 
    cur = con.cursor() 
    cur.execute("SELECT  Precio_Venta, Activo_circulante_mil_EUR_2021, Fondos_propios_mil_EUR_2021, Total_activo_mil_EUR_2021, Total_pasivo_y_capital_propio_mil_EUR_2021, Fondo_de_maniobra_mil_EUR_2021, Deudores_mil_EUR_2021, Beneficio_neto_mil_EUR, Ingresos_de_explotacion_mil_EUR_2021, Importe_neto_Cifra_de_Ventas_mil_EUR_2021, Pasivo_liquido_mil_EUR_2021, Total_pasivo_2021, total_funding, Pasivo_fijo_mil_EUR_2021, Gastos_financieros_mil_EUR_2021, Resultado_Explotacion_mil_EUR_2021, EBIT_mil_EUR_2021, PER, Resultado_del_Ejercicio_mil_EUR_2021, Result_ordinarios_antes_Impuestos_mil_EUR_2021, Importe_neto_Cifra_de_Ventas_mil_EUR_ratio, prediccion FROM manual_valoracion WHERE usuario = ?", (usuario,))
    resultado = cur.fetchall()
    con.close()
    
    return resultado


# MODELO ADQUISICIÓN (datos empresa)

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