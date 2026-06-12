"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
import os
import pandas as pd


def pregunta_01():
    # 1. Leer el archivo de entrada original
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    # 2. Eliminar la columna de índices basura si existe
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

    # 3. Eliminar valores nulos antes de empezar la homogeneización
    df.dropna(inplace=True)

    # 4. Limpieza de texto simple (Sin alterar guiones internos)
    df["sexo"] = df["sexo"].astype(str).str.lower().str.strip()
    df["tipo_de_emprendimiento"] = (
        df["tipo_de_emprendimiento"].astype(str).str.lower().str.strip()
    )
    df["barrio"] = df["barrio"].astype(str).str.lower().str.strip()

    # 5. Limpieza de texto con homologación de separadores (Idea y Línea de crédito)
    df["idea_negocio"] = (
        df["idea_negocio"]
        .astype(str)
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    df["línea_credito"] = (
        df["línea_credito"]
        .astype(str)
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    # 6. Limpieza y casteo estricto de Comuna y Estrato a números enteros
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(float).astype(int)
    df["estrato"] = df["estrato"].astype(float).astype(int)

    # 7. Limpieza limpia de Monto del Crédito (Evita dañar strings quitando decimales manualmente)
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    # 8. Estandarización de formatos de fecha mixtos a YYYY-MM-DD
    def clean_date(x):
        x = str(x).strip()
        for sep in ["/", "-"]:
            if sep in x:
                parts = x.split(sep)
                if len(parts) == 3:
                    if len(parts[0]) == 4:  # Formato: YYYY/MM/DD o YYYY-MM-DD
                        return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                    elif len(parts[2]) == 4:  # Formato: DD/MM/YYYY o DD-MM-YYYY
                        return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        return x

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(clean_date)

    # 9. Eliminar duplicados reales sobre la data perfectamente limpia
    df.drop_duplicates(inplace=True)

    # 10. Guardar el archivo final en el formato y ruta solicitada
    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()