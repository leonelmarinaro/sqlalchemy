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


def seed_data():
    db = SessionLocal()

    # Crear Clientes de ejemplo
    cliente1 = Cliente(
        nombre="Cliente A",
        cuit="20-12345678-9",
        client_folder="cliente_a",
        correo_output="cliente_a@example.com",
        socio_responsable="Juan Perez",
        zip_password="password123",
        rango_consulta_dias=10,
        dias_ejecucion="Lunes, Martes",
        documentacion=True,
    )
    cliente2 = Cliente(
        nombre="Cliente B",
        cuit="20-98765432-1",
        client_folder="cliente_b",
        correo_output="cliente_b@example.com",
        socio_responsable="Maria Gomez",
        zip_password="securepass",
        rango_consulta_dias=15,
        dias_ejecucion="Miercoles, Jueves",
        documentacion=False,
    )

    # Añadir Clientes a la sesión
    db.add(cliente1)
    db.add(cliente2)
    db.flush()

    # Crear Jurisdicciones de ejemplo
    jurisdiccion1 = Jurisdiccion(codigo="J1", nombre="Jurisdiccion 1")
    jurisdiccion2 = Jurisdiccion(codigo="J2", nombre="Jurisdiccion 2")

    # Añadir Jurisdicciones a la sesión
    db.add(jurisdiccion1)
    db.add(jurisdiccion2)
    db.flush()

    # Crear ClienteJurisdiccion de ejemplo
    cliente_jurisdiccion1 = ClienteJurisdiccion(
        cliente_id=cliente1.id,
        jurisdiccion_id=jurisdiccion1.id,
        usuario="user1",
        password="pass1",
        fecha_desde="2024-01-01",
        fecha_hasta="2024-12-31",
    )
    cliente_jurisdiccion2 = ClienteJurisdiccion(
        cliente_id=cliente2.id,
        jurisdiccion_id=jurisdiccion2.id,
        usuario="user2",
        password="pass2",
        fecha_desde="2024-01-01",
        fecha_hasta="2024-12-31",
    )

    # Añadir ClienteJurisdiccion a la sesión
    db.add(cliente_jurisdiccion1)
    db.add(cliente_jurisdiccion2)
    db.flush()

    # Crear UsuariosAutorizados de ejemplo
    usuario1 = UsuariosAutorizados(
        username="usuario1", fecha_autorizacion=datetime.now()
    )
    usuario2 = UsuariosAutorizados(
        username="usuario2", fecha_autorizacion=datetime.now()
    )

    # Añadir UsuariosAutorizados a la sesión
    db.add(usuario1)
    db.add(usuario2)
    db.flush()

    # Crear UsuarioCliente de ejemplo
    usuario_cliente1 = UsuarioCliente(id_usuario=usuario1.id, id_cliente=cliente1.id)
    usuario_cliente2 = UsuarioCliente(id_usuario=usuario2.id, id_cliente=cliente2.id)

    # Añadir UsuarioCliente a la sesión
    db.add(usuario_cliente1)
    db.add(usuario_cliente2)
    db.flush()

    # Crear MonitoreoBots de ejemplo
    monitoreo1 = MonitoreoBots(username="bot1", estado="activo", cliente_id=cliente1.id)
    monitoreo2 = MonitoreoBots(
        username="bot2", estado="inactivo", cliente_id=cliente2.id
    )

    # Añadir MonitoreoBots a la sesión
    db.add(monitoreo1)
    db.add(monitoreo2)

    # Guardar cambios
    db.commit()
    db.close()

    print("Datos de ejemplo insertados correctamente")

def delete_cliente(cliente_id):
    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            # Primero, eliminar las relaciones en cliente_jurisdiccion
            db.query(ClienteJurisdiccion).filter(
                ClienteJurisdiccion.cliente_id == cliente_id
            ).delete(synchronize_session=False)

            # Luego, eliminar las relaciones en usuario_cliente
            db.query(UsuarioCliente).filter(
                UsuarioCliente.id_cliente == cliente_id
            ).delete(synchronize_session=False)

            # Luego, eliminar las relaciones en monitoreo_bots
            db.query(MonitoreoBots).filter(
                MonitoreoBots.cliente_id == cliente_id
            ).delete(synchronize_session=False)

            # Finalmente, eliminar el cliente
            db.delete(cliente)
            db.commit()
            print(f"Cliente con ID {cliente_id} eliminado correctamente.")
        else:
            print(f"No se encontró ningún cliente con ID {cliente_id}.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error al eliminar el cliente: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
    # delete_cliente()