# General information
Service to search recommended sku by other sku

# Environment variables
 | Name | Default | Description| 
 | --- | --- | --- |
 | APP_PORT | "" | Application port |
 | LISTEN_HOST | "0.0.0.0" | Container host |
 | WORKERS | "5" | Gunicorn workers |
 | THREADS | "2" | Gunicorn threads |

# [Dependencies](requirements.txt)

# Run service
1. Clone repository.
2. Set environment variables in `.env` file.
3. Run command `docker-compose up -d --build`

# Viewing logs
 - Run command `docker logs <container_id>`

# Usage
Request:
```
GET localhost:port/
payload:
{
    "sku": str,
    "rec_min": Optional[float]
}
```
Response:
```
{
    "sku_found": int,
    "result": [str, str, ...]
}
```