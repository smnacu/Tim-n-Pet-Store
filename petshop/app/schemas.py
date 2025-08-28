from pydantic import BaseModel
from typing import List, Optional

# --- Esquemas para Proveedor ---
class ProveedorBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Producto ---
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    proveedor_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    proveedor: Optional[Proveedor] = None

    class Config:
        orm_mode = True

# --- Esquemas para Punto de Venta (TPV) ---
class VentaItem(BaseModel):
    producto_id: int
    cantidad: int

class Venta(BaseModel):
    items: List[VentaItem]
    # Aquí se podrían añadir otros detalles de la venta como cliente_id, total, etc.
