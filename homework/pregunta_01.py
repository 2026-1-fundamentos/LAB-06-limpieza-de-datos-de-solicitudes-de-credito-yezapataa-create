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
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)
    df.dropna(inplace=True)

    df["sexo"] = df["sexo"].str.lower().str.strip()
    df["tipo_de_emprendimiento"] = (
        df["tipo_de_emprendimiento"].str.lower().str.strip()
    )

    df["idea_negocio"] = (
        df["idea_negocio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    df["barrio"] = (
        df["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    df["línea_credito"] = (
        df["línea_credito"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(float).astype(int)
    df["estrato"] = df["estrato"].astype(float).astype(int)

    def clean_date(x):
        x = str(x).strip()
        for sep in ["/", "-"]:
            if sep in x:
                parts = x.split(sep)
                if len(parts) == 3:
                    if len(parts[0]) == 4:
                        return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                    elif len(parts[2]) == 4:
                        return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        return x

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(clean_date)

    df.drop_duplicates(inplace=True)

    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()