import requests

BASE = 'http://192.168.1.227:8000/'
# --- Root Endpoint ---
print("="*80)
response = requests.get(f'{BASE}/')
print(f"{BASE}: {response.status_code}")


BASE = 'http://192.168.1.227:8000/homesphere'
# --- HomeSphere Root Endpoint ---
print("="*80)
response = requests.get(f'{BASE}/')
print(f"{BASE}: {response.status_code}")


BASE = 'http://192.168.1.227:8000/homesphere/v1'
# --- HomeSphere Root Endpoint ---
print("="*80)
response = requests.get(f'{BASE}/')
print(f"{BASE}: {response.status_code}")  # returns HTML (Swagger UI), not JSON


BASE = 'http://192.168.1.227:8000/homesphere/v1'

# --- Version ---
print("="*80)
response = requests.get(f'{BASE}/version')
print(f"{BASE}/version: {response.status_code}")
print(response.json())

# --- Invalid Endpoint ---
print("="*80)
response = requests.get(f'{BASE}/invalid')
print(f"{BASE}/invalid: {response.status_code}")

# --- 404 - non-existent product ID ---
print("="*80)
response = requests.get(f'{BASE}/product/P999')
print(f"No auth - product not found: {response.status_code}")
print(response.json())

# --- Single product with header auth ---
print("="*80)
headers = {'X-API-Key': 'training-key-header'}
response = requests.get(f'{BASE}/product1/P001', headers=headers)
print(f"Header auth - single product: {response.status_code}")
print(response.json())

# --- Single product with query param auth ---
print("="*80)
response = requests.get(f'{BASE}/product2/P001', params={'api_key': 'training-key-param'})
print(f"Param auth - single product: {response.status_code}")
print(response.json())

#EOF
