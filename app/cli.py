import uuid

import typer
from rich import print
from sqlalchemy.orm import Session

from app.core.database import session_local
from app.core.security import get_password_hash
from app.modules.user.models import UserModel

# Inicializamos la aplicación de comandos con Type
cli_app = typer.Typer(help="Consola Feriados.")


@cli_app.command()
def create_root_user(
    email: str = typer.Option(
        ..., prompt="Correo electrónico: ", help="Email del usuario"
    ),
    password: str = typer.Option(
        ...,
        prompt="Contraseña",
        hide_input=True,
        confirmation_prompt=True,
        help="Contraseña del usuario.",
    ),
):
    """Crear usuario root."""
    print(
        "[yellow] Conectando a la base de datos y validando credenciales ...[/yellow]"
    )

    db: Session = session_local()
    try:
        # 1. Validar si ya existe.
        user_exists = db.query(UserModel).filter(UserModel.email == email).first()
        if user_exists:
            print(
                f"[red] X Error: El usuario con el email '{email}' ya se encuentra creado. [/red]"
            )
            raise typer.Exit(code=1)

        # 2.Encriptar contraseña y guardar
        hashed_password = get_password_hash(password)
        new_user = UserModel(
            id=uuid.uuid4(),
            email=email,
            password_hash=hashed_password,
            is_active=True,
        )
        db.add(new_user)
        db.commit()

        print("\n[bold green] ¡Usuario Root creado exitosamente![/bold green]")
        print(f"[green] Email registrado: [/green] [bold white] {email}[/bold white]")
    except Exception as e:
        db.rollback()
        print(
            f"[bold red] Ocurrió un error inesperado al insertar en la BD: [/bold red] {e}"
        )
        raise typer.Exit(code=1)
    finally:
        db.close()


if __name__ == "__main__":
    cli_app()
