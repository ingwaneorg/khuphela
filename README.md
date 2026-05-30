# khuphela

*khuphela* — "download" in isiZulu.

A small training API for Data Engineering ETL exercises (DE5M3). It serves fake customer data through three endpoint patterns, each demonstrating a different authentication approach that students must handle in their extraction code.

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The API and its Swagger docs will be available at `http://localhost:8000`.

## Endpoints

All endpoints return customer records with these fields:
`customer_id`, `first_name`, `last_name`, `email`, `phone`, `postcode`

### No authentication

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/customer` | All customers |
| GET | `/customer/<id>` | Single customer by ID |

### Header authentication (`X-API-Key`)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/customer1` | All customers |
| GET | `/customer1/<id>` | Single customer by ID |

Requires the header: `X-API-Key: <key>`

Default dev key: `training-key-header`

### Query parameter authentication

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/customer2` | All customers |
| GET | `/customer2/<id>` | Single customer by ID |

Requires the query param: `?api_key=<key>`

Default dev key: `training-key-param`

### Other

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/version` | API version |

## Error responses

- `401` — missing or invalid API key
- `404` — customer ID not found

## Deployment

Deployed to Google Cloud Run. See `bin/deploy.sh`.

Keys in production are set via environment variables:
- `TRAINING_API_KEY_HEADER`
- `TRAINING_API_KEY_PARAM`
