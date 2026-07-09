# Order Service

ShopEasy order management API — standalone microservice repository.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/orders` | List orders |

## Local development

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask run --port 5001
```

## CI/CD

Runs Jenkins pipeline with `checkoutPlatformDeps()` for `helm-charts` and `platform-config`. See `product-service` for the full promotion pipeline.
