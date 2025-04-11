"""
Todavia no está funcionando, pero la idea es importar los datos de los clientes desde un archivo Excel.
"""

import os
import pandas as pd
from library_app.db import SessionLocal
from library_app.models.models import (
    Cliente,
    Jurisdiccion,
    ClienteJurisdiccion,
    UsuariosAutorizados,
    UsuarioCliente,
    MonitoreoBots,
)
from datetime import datetime


def import_from_excel(excel_folder_path):
    """
    Import data from Excel files in the specified folder
    """
    if not os.path.exists(excel_folder_path):
        print(f"Error: Folder path '{excel_folder_path}' does not exist")
        return

    db = SessionLocal()
    try:
        # Process Clientes Excel
        clientes_file = os.path.join(excel_folder_path, "clientes.xlsx")
        if os.path.exists(clientes_file):
            process_clientes(clientes_file, db)

        # Process Jurisdicciones Excel
        jurisdicciones_file = os.path.join(excel_folder_path, "jurisdicciones.xlsx")
        if os.path.exists(jurisdicciones_file):
            process_jurisdicciones(jurisdicciones_file, db)

        # Process ClienteJurisdiccion Excel
        cliente_jurisdiccion_file = os.path.join(
            excel_folder_path, "cliente_jurisdiccion.xlsx"
        )
        if os.path.exists(cliente_jurisdiccion_file):
            process_cliente_jurisdiccion(cliente_jurisdiccion_file, db)

        # Process UsuariosAutorizados Excel
        usuarios_file = os.path.join(excel_folder_path, "usuarios_autorizados.xlsx")
        if os.path.exists(usuarios_file):
            process_usuarios(usuarios_file, db)

        # Process MonitoreoBots Excel
        monitoreo_file = os.path.join(excel_folder_path, "monitoreo_bots.xlsx")
        if os.path.exists(monitoreo_file):
            process_monitoreo(monitoreo_file, db)

        # Commit all changes
        db.commit()
        print("Data import completed successfully")

    except Exception as e:
        db.rollback()
        print(f"Error during import: {e}")
    finally:
        db.close()


def process_clientes(file_path, db):
    """Process the clientes Excel file"""
    print(f"Importing clientes from {file_path}")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        cliente = Cliente(
            nombre=row.get("nombre"),
            cuit=row.get("cuit"),
            client_folder=row.get("client_folder"),
            correo_output=row.get("correo_output"),
            socio_responsable=row.get("socio_responsable"),
            zip_password=row.get("zip_password"),
            rango_consulta_dias=row.get("rango_consulta_dias", 7),
            dias_ejecucion=row.get("dias_ejecucion"),
            documentacion=row.get("documentacion", True),
        )
        db.add(cliente)

    db.flush()
    print(f"Imported {len(df)} clientes")


def process_jurisdicciones(file_path, db):
    """Process the jurisdicciones Excel file"""
    print(f"Importing jurisdicciones from {file_path}")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        jurisdiccion = Jurisdiccion(codigo=row.get("codigo"), nombre=row.get("nombre"))
        db.add(jurisdiccion)

    db.flush()
    print(f"Imported {len(df)} jurisdicciones")


def process_cliente_jurisdiccion(file_path, db):
    """Process the cliente_jurisdiccion Excel file"""
    print(f"Importing cliente_jurisdiccion from {file_path}")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        cliente_jurisdiccion = ClienteJurisdiccion(
            cliente_id=row.get("cliente_id"),
            jurisdiccion_id=row.get("jurisdiccion_id"),
            usuario=row.get("usuario"),
            password=row.get("password"),
            consultar=row.get("consultar", True),
            fecha_desde=row.get("fecha_desde"),
            fecha_hasta=row.get("fecha_hasta"),
        )
        db.add(cliente_jurisdiccion)

    db.flush()
    print(f"Imported {len(df)} cliente_jurisdiccion relationships")


def process_usuarios(file_path, db):
    """Process the usuarios_autorizados Excel file"""
    print(f"Importing usuarios_autorizados from {file_path}")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        usuario = UsuariosAutorizados(
            username=row.get("username"),
            fecha_autorizacion=row.get("fecha_autorizacion", datetime.now()),
        )
        db.add(usuario)

    db.flush()
    print(f"Imported {len(df)} usuarios_autorizados")

    # Process UsuarioCliente relationships if they're in the same file
    if "id_cliente" in df.columns:
        for _, row in df.iterrows():
            # Look up the usuario we just added
            usuario = (
                db.query(UsuariosAutorizados)
                .filter_by(username=row.get("username"))
                .first()
            )
            if usuario and row.get("id_cliente"):
                usuario_cliente = UsuarioCliente(
                    id_usuario=usuario.id, id_cliente=row.get("id_cliente")
                )
                db.add(usuario_cliente)

        db.flush()
        print(f"Imported usuario_cliente relationships")


def process_monitoreo(file_path, db):
    """Process the monitoreo_bots Excel file"""
    print(f"Importing monitoreo_bots from {file_path}")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        monitoreo = MonitoreoBots(
            username=row.get("username"),
            estado=row.get("estado"),
            iniciado=row.get("iniciado"),
            finalizado=row.get("finalizado"),
            cliente_id=row.get("cliente_id"),
        )
        db.add(monitoreo)

    db.flush()
    print(f"Imported {len(df)} monitoreo_bots")


if __name__ == "__main__":
    # Specify the folder containing your Excel files
    excel_folder = "data/clientes"

    # Create folder if it doesn't exist
    if not os.path.exists(excel_folder):
        os.makedirs(excel_folder)
        print(f"Created folder: {excel_folder}")
        print("Please place your Excel files in this folder and run the script again")
    else:
        import_from_excel(excel_folder)
