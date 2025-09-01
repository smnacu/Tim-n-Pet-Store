from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Modelo estándar para respuestas de error.
    """

    error: str
    detail: Optional[str] = None
    status_code: int


def validate_positive_integer(value: int, field_name: str) -> int:
    """
    Valida que un entero sea positivo.
    """
    if value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} debe ser un número positivo",
        )
    return value


def validate_email_format(email: str) -> str:
    """
    Validación básica de formato de email.
    """
    if "@" not in email or "." not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de email inválido"
        )
    return email.lower()


def validate_string_not_empty(value: str, field_name: str) -> str:
    """
    Valida que un string no esté vacío.
    """
    if not value or not value.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} no puede estar vacío",
        )
    return value.strip()


def handle_database_error(error: Exception) -> HTTPException:
    """
    Maneja errores de base de datos de forma consistente.
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {str(error)}",
    )
