"""
Tareas asíncronas para el servicio de petshop.
Incluye procesamiento de archivos Excel para actualización de inventario.
"""

import uuid
from typing import Dict, Any, List

from common.celery_app import celery_app


@celery_app.task(bind=True)
def process_inventory_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Procesa un archivo de inventario (Excel/CSV) para actualizar productos.
    
    Args:
        file_path: Ruta al archivo del inventario
        file_type: Tipo de archivo (excel, csv)
    
    Returns:
        Diccionario con el resultado del procesamiento
    """
    try:
        task_id = self.request.id
        
        # Simular procesamiento del archivo
        processed_data = _mock_excel_processing(file_path, file_type)
        
        result = {
            "task_id": task_id,
            "file_path": file_path,
            "file_type": file_type,
            "processed_products": processed_data["products"],
            "total_processed": processed_data["total"],
            "successful_updates": processed_data["successful"],
            "failed_updates": processed_data["failed"],
            "status": "completed",
            "processing_time": 5.2,  # Simulado
        }
        
        return result
    
    except Exception as exc:
        # En caso de error, reintentar la tarea
        self.retry(countdown=60, max_retries=3, exc=exc)


def _mock_excel_processing(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Simulación de procesamiento de archivo Excel/CSV.
    En una implementación real, aquí se usaría pandas para leer el archivo.
    """
    # Simulación de datos procesados
    mock_products = [
        {
            "sku": "PET001",
            "name": "Alimento para Perros Premium",
            "stock": 50,
            "price": 29.99,
            "category": "Alimentos"
        },
        {
            "sku": "PET002", 
            "name": "Juguete Pelota",
            "stock": 25,
            "price": 8.50,
            "category": "Juguetes"
        },
        {
            "sku": "PET003",
            "name": "Collar Ajustable",
            "stock": 15,
            "price": 12.00,
            "category": "Accesorios"
        }
    ]
    
    return {
        "products": mock_products,
        "total": len(mock_products),
        "successful": len(mock_products),
        "failed": 0
    }


@celery_app.task
def update_product_prices(price_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Actualiza precios de productos en lote.
    
    Args:
        price_updates: Lista de actualizaciones de precios
    
    Returns:
        Diccionario con el resultado de las actualizaciones
    """
    try:
        successful_updates = []
        failed_updates = []
        
        for update in price_updates:
            try:
                # Simulación de actualización de precio
                successful_updates.append({
                    "sku": update["sku"],
                    "old_price": update.get("old_price", 0),
                    "new_price": update["new_price"],
                    "updated_at": "2024-01-15T10:30:00Z"
                })
            except Exception as e:
                failed_updates.append({
                    "sku": update.get("sku", "unknown"),
                    "error": str(e)
                })
        
        return {
            "total_updates": len(price_updates),
            "successful": len(successful_updates),
            "failed": len(failed_updates),
            "successful_updates": successful_updates,
            "failed_updates": failed_updates,
            "status": "completed"
        }
    
    except Exception as exc:
        return {
            "error": str(exc),
            "status": "failed"
        }


@celery_app.task
def generate_inventory_report(store_id: int, report_type: str) -> Dict[str, Any]:
    """
    Genera reportes de inventario.
    
    Args:
        store_id: ID de la tienda
        report_type: Tipo de reporte (stock_low, sales_summary, inventory_value)
    
    Returns:
        Diccionario con el reporte generado
    """
    try:
        report_data = _generate_mock_report(store_id, report_type)
        
        return {
            "store_id": store_id,
            "report_type": report_type,
            "report_id": str(uuid.uuid4()),
            "generated_at": "2024-01-15T10:30:00Z",
            "data": report_data,
            "status": "completed"
        }
    
    except Exception as exc:
        return {
            "error": str(exc),
            "status": "failed"
        }


def _generate_mock_report(store_id: int, report_type: str) -> Dict[str, Any]:
    """Genera datos simulados para reportes."""
    if report_type == "stock_low":
        return {
            "low_stock_products": [
                {"sku": "PET004", "name": "Shampoo Perros", "current_stock": 3, "min_stock": 10},
                {"sku": "PET005", "name": "Arena Gatos", "current_stock": 1, "min_stock": 5}
            ],
            "total_low_stock": 2
        }
    elif report_type == "sales_summary":
        return {
            "total_sales": 1250.75,
            "products_sold": 45,
            "top_products": [
                {"sku": "PET001", "name": "Alimento Premium", "quantity_sold": 15},
                {"sku": "PET002", "name": "Juguete Pelota", "quantity_sold": 8}
            ]
        }
    elif report_type == "inventory_value":
        return {
            "total_inventory_value": 15750.50,
            "total_products": 120,
            "categories": {
                "Alimentos": 8500.00,
                "Juguetes": 3200.50,
                "Accesorios": 4050.00
            }
        }
    
    return {"message": "Reporte no disponible"}