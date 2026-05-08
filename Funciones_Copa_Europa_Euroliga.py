### ============================================================
### utilidades.py — Funciones de scraping, limpieza y análisis
### ============================================================

import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
import numpy as np
from deep_translator import GoogleTranslator
import inspect


# --------------------------------------------------------------
# Ver lista de funciones del módulo
# --------------------------------------------------------------
def ver_lista_funciones():
    funciones = [f[0] for f in inspect.getmembers(__import__(__name__), inspect.isfunction)]
    print("\nFunciones disponibles en utilidades:\n")
    for f in funciones:
        print(" -", f)
    return funciones


# --------------------------------------------------------------
# Limpiar texto: quitar tildes, acentos y caracteres raros
# --------------------------------------------------------------
def limpiar_texto(x):
    if isinstance(x, str):
        x = unicodedata.normalize('NFKD', x)
        x = ''.join(c for c in x if not unicodedata.combining(c))
        x = ' '.join(x.split())
        return x
    return x


# --------------------------------------------------------------
# Funciones para inspeccionar tablas HTML
# --------------------------------------------------------------
def opciones_ver_etiquetas():
    print(""" 
    ver_etiquetas(url)
    tiene_cabeceras(tabla)
    tiene_filas(tabla)
    tiene_columnas(tabla)
    no_es_navbox(tabla)
    tiene_texto_util(tabla)
    """)

def ver_etiquetas(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup

def tiene_cabeceras(tabla):
    return tabla.find("th") is not None

def tiene_filas(tabla):
    filas = tabla.find_all("tr")
    return len(filas) >= 2

def tiene_columnas(tabla):
    primera = tabla.find("tr")
    if not primera:
        return False
    celdas = primera.find_all(["td", "th"])
    return len(celdas) >= 2

def no_es_navbox(tabla):
    clase = tabla.get("class", [])
    basura = ["navbox", "infobox", "sidebar", "metadata", "vertical-navbox"]
    return not any(b in clase for b in basura)

def tiene_texto_util(tabla):
    texto = tabla.get_text(" ", strip=True)
    return len(texto.split()) > 5


# --------------------------------------------------------------
# Añadir columna a un DataFrame
# --------------------------------------------------------------
def añadir_paises_df(df, lista_paises, nombre_columna):
    df[nombre_columna] = lista_paises
    return df


# --------------------------------------------------------------
# Opciones de visualización de DataFrames
# --------------------------------------------------------------
def opciones__visualizar_dataframe():
    print(""" 
    activar_vista_larga()
    restaurar_vista()
    """)

def activar_vista_larga():
    pd.set_option("display.max_rows", 1000)
    pd.set_option("display.max_columns", None)

def restaurar_vista():
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")


# --------------------------------------------------------------
# Comprobar número de tablas en una URL
# --------------------------------------------------------------
def opciones_comprobar_tablas():
    print(""" 
    comprobar_tablas(url)
    """)

def comprobar_tablas(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    print(f"Total tablas: {len(tables)}")


# --------------------------------------------------------------
# Eliminar duplicados dentro de una celda
# --------------------------------------------------------------
def eliminar_duplicados(df, columna):
    df[columna] = df[columna].apply(
        lambda x: " ".join(dict.fromkeys(str(x).split()))
    )


# --------------------------------------------------------------
# Traducir columna a inglés
# --------------------------------------------------------------
def traducir_paises_ingles(df, columna):
    df[columna] = df[columna].apply(
        lambda x: GoogleTranslator(source="auto", target="en").translate(str(x))
    )
    return df


# --------------------------------------------------------------
# Sacar valores únicos de una columna
# --------------------------------------------------------------
def sacar_valores_columna(df, columna):
    return df[columna].unique().tolist()


# --------------------------------------------------------------
# Sacar equipos ganadores por país a un data frame
# --------------------------------------------------------------
def winner_champions(lista_paises, df_trabajo):
    
    dfs = {}

    for country in lista_paises:
        df_temp = df_trabajo[df_trabajo["statenme"] == country]
        
        if df_temp.empty:
            print(f"⚠️ No existe {country} en el DataFrame.")
        else:
            dfs[country] = df_temp
            print(f"✔ Guardado dfs['{country}'] con {len(df_temp)} filas.")
    
    return dfs
# --------------------------------------------------------------
# Sacar equipos ganadores por país pero mas leible
# --------------------------------------------------------------
def diccionario_ganadores(df, columna):
    return df.groupby(columna).size().to_dict()


def resumen_ganadores(diccionario):
    for pais, df_pais in diccionario.items():
        print(f"{pais}: {len(df_pais)} títulos")


# --------------------------------------------------------------
# Cambiar nombres columna
# --------------------------------------------------------------
def cambiar_nombres_columna(lista_original,lista_nueva):
    df = df.rename(columns=dict(zip(lista_original, lista_nueva)))


# Listado de equipos campeones y número de títulos
def equipos_campeones(df_trabajo):
    equipos_campeones = (
        df_trabajo.groupby("team")
                  .size()
                  .reset_index(name="titulos")
                  .sort_values("titulos", ascending=False)
    )
    return equipos_campeones

