# Async Processing with Celery and Redis

This document describes the asynchronous task processing implementation using Celery and Redis in the Tim-n-Pet-Store system.

## Overview

The system now includes async processing capabilities for:
- **OCR document processing** in the veterinaria service
- **Excel/CSV inventory processing** in the petshop service
- **Report generation** for both services

## Architecture

### Celery Configuration
- **Broker**: Redis (runs on port 6379)
- **Backend**: Redis (for result storage)
- **Queues**: 
  - `veterinaria`: For veterinary service tasks
  - `petshop`: For pet shop service tasks

### Services

#### Veterinaria Service (Port 8002)
**New Endpoints:**
- `POST /historias-clinicas/` - Upload medical documents for OCR processing
- `GET /historias-clinicas/task/{task_id}` - Check OCR task status
- `POST /mascotas/{mascota_id}/reportes/` - Generate medical reports

**Celery Tasks:**
- `process_medical_document` - OCR processing for medical documents
- `generate_medical_report` - Generate consolidated medical reports

#### Petshop Service (Port 8004)
**New Endpoints:**
- `POST /upload-inventario/` - Upload inventory files (Excel/CSV)
- `GET /inventario/task/{task_id}` - Check inventory processing status
- `POST /reportes/inventario/` - Generate inventory reports

**Celery Tasks:**
- `process_inventory_file` - Process Excel/CSV files for inventory updates
- `update_product_prices` - Bulk price updates
- `generate_inventory_report` - Generate various inventory reports

## Usage Examples

### Document OCR Processing

```bash
# Upload a medical document
curl -X POST "http://localhost:8002/historias-clinicas/" \\
  -H "accept: application/json"

# Check task status
curl -X GET "http://localhost:8002/historias-clinicas/task/{task_id}" \\
  -H "accept: application/json"
```

### Inventory File Processing

```bash
# Upload inventory file
curl -X POST "http://localhost:8004/upload-inventario/" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@inventory.xlsx"

# Check processing status
curl -X GET "http://localhost:8004/inventario/task/{task_id}" \\
  -H "accept: application/json"
```

### Report Generation

```bash
# Generate inventory report
curl -X POST "http://localhost:8004/reportes/inventario/?store_id=1&report_type=stock_low" \\
  -H "accept: application/json"

# Generate medical report
curl -X POST "http://localhost:8002/mascotas/1/reportes/" \\
  -H "accept: application/json"
```

## Docker Services

### Celery Worker
Processes tasks from both queues:
```yaml
celery-worker:
  build:
    context: .
    dockerfile: backend.Dockerfile
  command: celery -A common.celery_app worker --loglevel=info --queues=veterinaria,petshop
  depends_on:
    - redis
    - postgresql
```

### Celery Flower (Monitoring)
Web interface for monitoring tasks:
```yaml
celery-flower:
  build:
    context: .
    dockerfile: backend.Dockerfile
  command: celery -A common.celery_app flower --port=5555
  ports:
    - "5555:5555"
```

Access Flower at: http://localhost:5555

## Development Setup

### 1. Start with Docker Compose
```bash
docker compose up -d
```

This will start:
- All microservices
- PostgreSQL database
- Redis broker
- Celery worker
- Celery Flower monitoring

### 2. Running Celery Locally (Development)

#### Start Redis
```bash
redis-server
```

#### Start Celery Worker
```bash
celery -A common.celery_app worker --loglevel=info
```

#### Start Celery Flower (Optional)
```bash
celery -A common.celery_app flower
```

## Task Types and Examples

### OCR Processing Tasks
- **Input**: Medical documents (PDF, images)
- **Processing**: Extract text using OCR (mock implementation)
- **Output**: Structured medical data

Example OCR result:
```json
{
  "task_id": "abc123",
  "file_path": "/tmp/radiografia.pdf",
  "document_type": "radiografia",
  "extracted_text": "RADIOGRAFÍA TORÁCICA\\nPaciente: Max (Canino)\\n...",
  "status": "completed",
  "confidence": 0.95
}
```

### Inventory Processing Tasks
- **Input**: Excel/CSV files with product data
- **Processing**: Parse and validate inventory data
- **Output**: Updated product records

Example inventory result:
```json
{
  "task_id": "def456",
  "processed_products": [
    {
      "sku": "PET001",
      "name": "Alimento para Perros Premium",
      "stock": 50,
      "price": 29.99
    }
  ],
  "total_processed": 25,
  "successful_updates": 23,
  "failed_updates": 2
}
```

## Testing

### Integration Tests
Run the integration tests to verify async processing:

```bash
# Set test database URL
export DATABASE_URL="sqlite:///./test.db"

# Run integration tests
pytest tests/test_integration.py -v
```

### Test Coverage
- Service connectivity tests
- Celery task endpoint tests  
- Cross-service workflow tests
- Error handling tests

## Error Handling

The system handles various error scenarios:
- **Task failures**: Automatic retries with exponential backoff
- **Service unavailability**: Graceful error responses
- **Invalid file formats**: Validation errors
- **Database errors**: Transaction rollbacks

## Monitoring

### Celery Flower Dashboard
- Task monitoring in real-time
- Worker status and performance
- Task history and results
- Queue monitoring

### Application Logs
- Task execution logs
- Error tracking
- Performance metrics

## Configuration

### Environment Variables
```bash
# Redis connection
REDIS_URL=redis://redis:6379/0

# Database connection  
DATABASE_URL=postgresql://user:password@postgresql/timon_petstore

# Task settings
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
```

### Queue Configuration
```python
task_routes={
    "veterinaria.app.tasks.*": {"queue": "veterinaria"},
    "petshop.app.tasks.*": {"queue": "petshop"},
}
```

## Future Enhancements

1. **Real OCR Integration**: Replace mock with actual OCR libraries (Tesseract, EasyOCR)
2. **File Storage**: Implement proper file storage (S3, MinIO)
3. **Task Scheduling**: Add periodic tasks for automated reports
4. **Result Persistence**: Store task results in database
5. **Notification System**: Email/SMS notifications for completed tasks