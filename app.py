from flask import Flask, request
import os
from flask_restx import Api, Resource, fields
from functools import wraps

from version import __version__

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-for-development')

api = Api(
    app,
    version='1.0',
    title='Labs Training API',
    description='API for Data Engineering ETL training',
    prefix='/homesphere/v1',
    doc='/homesphere/v1/'
)

specs_model = api.model('Specs', {
    'rrp'            : fields.Float(required=True, description='Recommended retail price'),
    'warranty_years' : fields.Integer(required=True, description='Warranty in years'),
    'colour'         : fields.String(required=True, description='Colour'),
    'connectivity'   : fields.String(required=True, description='Connectivity type'),
})

product_model = api.model('Product', {
    'product_id' : fields.String(required=True, description='Product ID'),
    'name'       : fields.String(required=True, description='Product name'),
    'category'   : fields.String(required=True, description='Category'),
    'specs'      : fields.Nested(specs_model, required=True, description='Product specs'),
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

def products():
    return [
        {'product_id': 'P001', 'name': 'Smart Thermostat Pro',          'category': 'Thermostats', 'specs': {'rrp': 89.99,  'warranty_years': 2, 'colour': 'White', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P002', 'name': 'Smart Thermostat Lite',         'category': 'Thermostats', 'specs': {'rrp': 59.99,  'warranty_years': 1, 'colour': 'White', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P003', 'name': 'Motion Sensor',                 'category': 'Sensors',     'specs': {'rrp': 24.99,  'warranty_years': 1, 'colour': 'White', 'connectivity': 'Zigbee'}},
        {'product_id': 'P004', 'name': 'Door Sensor',                   'category': 'Sensors',     'specs': {'rrp': 18.99,  'warranty_years': 1, 'colour': 'White', 'connectivity': 'Zigbee'}},
        {'product_id': 'P005', 'name': 'Smart Camera Indoor',           'category': 'Cameras',     'specs': {'rrp': 129.99, 'warranty_years': 2, 'colour': 'Black', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P006', 'name': 'Smart Camera Outdoor',          'category': 'Cameras',     'specs': {'rrp': 149.99, 'warranty_years': 2, 'colour': 'Black', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P007', 'name': 'Smart Plug',                    'category': 'Smart Plugs', 'specs': {'rrp': 14.99,  'warranty_years': 1, 'colour': 'White', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P008', 'name': 'Smart Plug with Energy Monitor','category': 'Smart Plugs', 'specs': {'rrp': 19.99,  'warranty_years': 1, 'colour': 'White', 'connectivity': 'Wi-Fi'}},
        {'product_id': 'P009', 'name': 'Smart Hub',                     'category': 'Hubs',        'specs': {'rrp': 49.99,  'warranty_years': 2, 'colour': 'Black', 'connectivity': 'Wi-Fi'}},
    ]

def require_api_key_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.environ.get('TRAINING_API_KEY_HEADER', 'training-key-header')
        if api_key != expected_key:
            api.abort(401, 'Invalid or missing API key parameter')
        return f(*args, **kwargs)
    return decorated_function

def require_api_key_param(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.args.get('api_key')
        expected_key = os.environ.get('TRAINING_API_KEY_PARAM', 'training-key-param')
        if api_key != expected_key:
            api.abort(401, 'Invalid or missing API key parameter')
        return f(*args, **kwargs)
    return decorated_function

# Open access endpoints
@api.route('/product')
class ProductList(Resource):
    @api.marshal_list_with(product_model)
    def get(self):
        """Get all products - no authentication required"""
        return products()

@api.route('/product/<string:product_id>')
class Product(Resource):
    @api.marshal_with(product_model)
    @api.response(404, 'Product not found', error_model)
    def get(self, product_id):
        """Get a specific product by ID - no authentication required"""
        product = next((p for p in products() if p['product_id'] == product_id), None)
        if product is None:
            api.abort(404, 'Product not found')
        return product

# Header authentication endpoints
@api.route('/product1')
class Product1List(Resource):
    @api.marshal_list_with(product_model)
    @api.doc(security='apikey')
    @api.header('X-API-Key', 'API Key', required=True)
    @require_api_key_header
    def get(self):
        """Get all products - requires X-API-Key header"""
        return products()

@api.route('/product1/<string:product_id>')
class Product1(Resource):
    @api.marshal_with(product_model)
    @api.doc(security='apikey')
    @api.header('X-API-Key', 'API Key', required=True)
    @api.response(404, 'Product not found', error_model)
    @require_api_key_header
    def get(self, product_id):
        """Get a specific product by ID - requires X-API-Key header"""
        product = next((p for p in products() if p['product_id'] == product_id), None)
        if product is None:
            api.abort(404, 'Product not found')
        return product

# Query parameter authentication endpoints
@api.route('/product2')
class Product2List(Resource):
    @api.marshal_list_with(product_model)
    @api.doc(params={'api_key': 'API Key for authentication'})
    @require_api_key_param
    def get(self):
        """Get all products - requires api_key query parameter"""
        return products()

@api.route('/product2/<string:product_id>')
class Product2(Resource):
    @api.marshal_with(product_model)
    @api.doc(params={'api_key': 'API Key for authentication'})
    @api.response(404, 'Product not found', error_model)
    @require_api_key_param
    def get(self, product_id):
        """Get a specific product by ID - requires api_key query parameter"""
        product = next((p for p in products() if p['product_id'] == product_id), None)
        if product is None:
            api.abort(404, 'Product not found')
        return product

@api.route('/version')
class Version(Resource):
    def get(self):
        """Get API version"""
        return {'version': __version__}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
