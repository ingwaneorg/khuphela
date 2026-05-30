# khuphela

*khuphela* — "download" in isiZulu.

A small training API for Data Engineering ETL exercises (DE5M3). It serves smart home product data through three endpoint patterns, each demonstrating a different authentication approach that students must handle in their extraction code.

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The API and its Swagger docs will be available at `http://localhost:8000`.

## Endpoints

All endpoints return product records with these fields:
`product_id`, `name`, `category`, `specs` (nested: `rrp`, `warranty_years`, `colour`, `connectivity`)

### No authentication

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/product` | All products |
| GET | `/product/<id>` | Single product by ID (e.g. `P001`) |

### Header authentication (`X-API-Key`)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/product1` | All products |
| GET | `/product1/<id>` | Single product by ID |

Requires the header: `X-API-Key: <key>`

Default dev key: `training-key-header`

### Query parameter authentication

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/product2` | All products |
| GET | `/product2/<id>` | Single product by ID |

Requires the query param: `?api_key=<key>`

Default dev key: `training-key-param`

### Other

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/version` | API version |

## Error responses

- `401` — missing or invalid API key
- `404` — product ID not found

## Deployment

Deployed to Google Cloud Run. See `bin/deploy.sh`.

Keys in production are set via environment variables:
- `TRAINING_API_KEY_HEADER`
- `TRAINING_API_KEY_PARAM`
