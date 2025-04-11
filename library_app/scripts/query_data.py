from library_app.db import SessionLocal
from library_app.models.models import (
    Cliente,
    Jurisdiccion,
    ClienteJurisdiccion,
    UsuariosAutorizados,
    UsuarioCliente,
    MonitoreoBots,
    ClienteProcessor,
)
import datetime
import sqlalchemy as sa
from sqlalchemy import and_
import pandas as pd
# from library_app.processors.cliente_processor import ClienteProcessor


def query_data():
    today = datetime.date.today()
    day_name = today.strftime("%A")  # Full day name (e.g., "Monday")

    # Map English day names to Spanish
    day_name_es = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }.get(day_name)

    print("\n--- Clientes ---")
    cliente_processors = []

    with SessionLocal() as db:
        clientes = (
            db.query(Cliente)
            .filter(Cliente.documentacion == True)
            .filter(Cliente.dias_ejecucion.like(f"%{day_name_es}%"))
            .filter(
                ~sa.exists().where(
                    and_(
                        MonitoreoBots.cliente_id == Cliente.id,
                        MonitoreoBots.estado == "Correcto",
                        sa.func.cast(MonitoreoBots.finalizado, sa.Date) == today,
                    )
                )
            )
            .all()
        )

        # Get the IDs of filtered clients
        cliente_ids = [cliente.id for cliente in clientes]

        for cliente in clientes:
            print(f"ID: {cliente.id}, Nombre: {cliente.nombre}, CUIT: {cliente.cuit}")
            print(f"Jurisdicciones: {len(cliente.cliente_jurisdicciones)}")
            print("---")

        # Query ClienteJurisdiccion records for the filtered clients
        print("\n--- Jurisdicciones de Clientes Filtrados ---")
        cliente_jurisdicciones = (
            db.query(ClienteJurisdiccion)
            .filter(ClienteJurisdiccion.cliente_id.in_(cliente_ids))
            .filter(ClienteJurisdiccion.consultar)
            .all()
        )

        for cj in cliente_jurisdicciones:
            jurisdiccion = db.query(Jurisdiccion).get(cj.jurisdiccion_id)
            cliente = db.query(Cliente).get(cj.cliente_id)
            print(f"Cliente: {cliente.nombre} (ID: {cj.cliente_id})")
            print(f"Jurisdicción: {jurisdiccion.clase} (ID: {cj.jurisdiccion_id})")
            print(f"Usuario: {cj.usuario}, Consultar: {cj.consultar}")
            print("---")

        # Create a ClienteProcessor for each client
        for cliente in clientes:
            # Get all jurisdictions for this client
            jurisdicciones = [
                cj for cj in cliente_jurisdicciones if cj.cliente_id == cliente.id
            ]

            # Create DataFrame with client and jurisdiction data
            juris_data = []
            for cj in jurisdicciones:
                jur = db.query(Jurisdiccion).get(cj.jurisdiccion_id)
                juris_data.append(
                    {
                        "cliente_id": cliente.id,
                        "cliente_nombre": cliente.nombre,
                        "correo_output": cliente.correo_output,
                        "socio_responsable": cliente.socio_responsable,
                        "jurisdiccion_id": cj.jurisdiccion_id,
                        "jurisdiccion_clase": jur.clase,
                        "jurisdiccion_codigo": jur.codigo,
                        "usuario": cj.usuario,
                        "password": cj.password,
                        "consultar": cj.consultar,
                        "fecha_login_error": cj.fecha_login_error,
                    }
                )

            # Create DataFrame
            group_df = pd.DataFrame(juris_data)

            # Create ClienteProcessor
            if not group_df.empty:
                inicio = datetime.datetime.now()
                processor = ClienteProcessor(
                    cliente=cliente.nombre,
                    group=group_df,
                    cuit_cliente=cliente.cuit,
                    inicio=inicio,
                    client_folder=cliente.client_folder,
                )
                cliente_processors.append(processor)

        return {
            "clientes": clientes,
            "cliente_jurisdicciones": cliente_jurisdicciones,
            "cliente_processors": cliente_processors,
        }


if __name__ == "__main__":
    query_data()
