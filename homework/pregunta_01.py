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
    # 1. Leer el archivo omitiendo la columna de índices basura si existe
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

    # 2. Eliminar filas completamente vacías o con nulos en las columnas importantes
    df.dropna(inplace=True)

    # 3. Limpieza estricta de columnas de texto (Minúsculas, quitar guiones/guiones bajos y espacios extremos)
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in columnas_texto:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.strip()
        )

    # 4. Limpieza estricta de la columna Comuna (Pasarla a entero para evitar que '1.0' y '1' rompan el drop_duplicates)
    df["comuna_ciudadano"] = (
        df["comuna_ciudadano"].astype(float).astype(int).astype(str).str.strip()
    )

    # 5. Limpieza de Estrato
    df["estrato"] = df["estrato"].astype(float).astype(int)

    # 6. Limpieza de Monto del crédito (Quitar símbolos monetarios, comas, puntos flotantes y dejarlo entero)
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    # 7. Normalización de Fechas al formato estándar YYYY-MM-DD
    def clean_date(x):
        x = str(x).strip()
        for sep in ["/", "-"]:
            if sep in x:
                parts = x.split(sep)
                if len(parts) == 3:
                    # Caso YYYY/MM/DD o YYYY-MM-DD
                    if len(parts[0]) == 4:
                        return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                    # Caso DD/MM/YYYY o DD-MM-YYYY
                    elif len(parts[2]) == 4:
                        return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        return x

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(clean_date)

    # 8. Eliminar los duplicados reales ahora que toda la data es completamente homogénea
    df.drop_duplicates(inplace=True)

    # 9. Guardar el archivo en la ruta requerida
    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()