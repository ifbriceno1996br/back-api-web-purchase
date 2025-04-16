from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Crear roles
    role_admin = crud.crud_role.get_role_by_name(db, name="admin")
    if not role_admin:
        role_admin_in = schemas.role.RoleCreate(
            name="admin",
            description="Administrador del sistema"
        )
        role_admin = crud.crud_role.create_with_user(db=db, obj_in=role_admin_in)

    role_supervisor = crud.crud_role.get_role_by_name(db, name="supervisor")
    if not role_supervisor:
        role_supervisor_in = schemas.role.RoleCreate(
            name="supervisor",
            description="Supervisor de solicitudes"
        )
        role_supervisor = crud.crud_role.create_with_user(db=db, obj_in=role_supervisor_in)

    role_user = crud.crud_role.get_role_by_name(db, name="user")
    if not role_user:
        role_user_in = schemas.role.RoleCreate(
            name="user",
            description="Usuario normal"
        )
        role_user = crud.crud_role.create_with_user(db=db, obj_in=role_user_in)

    # Crear usuario admin
    user_admin = crud.crud_user.get_user_by_email(db, email="admin@example.com")
    if not user_admin:
        user_admin_in = schemas.user.UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="Administrador",
            role_ids=[role_admin.id]
        )
        user_admin = crud.crud_user.create_user(db=db, user=user_admin_in)

    # Crear usuario supervisor
    user_supervisor = crud.crud_user.get_user_by_email(db, email="supervisor@example.com")
    if not user_supervisor:
        user_supervisor_in = schemas.user.UserCreate(
            email="supervisor@example.com",
            password="supervisor123",
            full_name="Supervisor",
            role_ids=[role_supervisor.id]
        )
        user_supervisor = crud.crud_user.create_user(db=db, user=user_supervisor_in)

    # Crear usuario normal
    user_normal = crud.crud_user.get_user_by_email(db, email="user@example.com")
    if not user_normal:
        user_normal_in = schemas.user.UserCreate(
            email="user@example.com",
            password="user123",
            full_name="Usuario Normal",
            role_ids=[role_user.id]
        )
        user_normal = crud.crud_user.create_user(db=db, user=user_normal_in)
