import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def conectar():
    """Crea y devuelve una conexión a la base de datos PostgreSQL."""
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conexion

def obtener_servicios():
    """Consulta todos los servicios y precios de la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre, precio FROM servicios;")
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return filas

def obtener_info_servicios_texto():
    """Trae los servicios de la BD y los arma como texto para el prompt."""
    servicios = obtener_servicios()

    lineas = []
    for nombre, precio in servicios:
        lineas.append(f"- {nombre}: ${precio}")

    return "\n".join(lineas)

def buscar_servicios(pregunta):
    """
    Busca servicios relevantes según las palabras clave de la pregunta.
    Separa la pregunta en palabras y busca servicios que contengan alguna.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    palabras_ignoradas = {
        "cuanto", "cuánto", "cuesta", "vale", "sale", "precio", "el", "la", "los",
        "las", "un", "una", "de", "del", "para", "mi", "que", "qué", "es", "por",
        "y", "a", "con", "cuestan", "valen", "tienen", "hacen", "hay"
    }

    palabras = pregunta.lower().replace("¿", "").replace("?", "").replace(",", "").split()
    palabras_clave = [p for p in palabras if p not in palabras_ignoradas and len(p) > 2]

    if not palabras_clave:
        cursor.close()
        conexion.close()
        return []

    condiciones = " OR ".join(["nombre ILIKE %s" for _ in palabras_clave])
    valores = ['%' + palabra + '%' for palabra in palabras_clave]

    consulta = f"SELECT nombre, precio FROM servicios WHERE {condiciones};"
    cursor.execute(consulta, valores)
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return filas

if __name__ == "__main__":
    resultados = buscar_servicios("baño")
    print("Resultados de buscar 'baño':")
    for nombre, precio in resultados:
        print(f" - {nombre}: ${precio}")