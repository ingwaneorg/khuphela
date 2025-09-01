from flask import Flask, request
import os
from flask_restx import Api, Resource, fields
from functools import wraps
import json

# Get the version number
from version import __version__

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-for-development')

# Initialize Flask-RESTX
api = Api(
    app, 
    version='1.0', 
    title='Labs Training API',
    description='API for Data Engineering ETL training',
    doc='/docs/'  # Documentation will be available at /docs/
)

# Define the customer model for documentation
customer_model = api.model('Customer', {
    'customer_id': fields.Integer(required=True, description='Customer ID'),
    'first_name' : fields.String(required=True, description='First name'),
    'last_name'  : fields.String(required=True, description='Last name'),
    'email'      : fields.String(required=True, description='Email address'),
    'phone'      : fields.String(required=True, description='Phone number'),
    'postcode'   : fields.String(required=True, description='UK postcode')
})

# Error model
error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

def enriched_customers():
    return {
        'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],
        'first_name' : ['John', 'Jane', 'Mike', 'Sarah', 'Bob', 'Alice'],
        'last_name'  : ['Smith', 'Doe', 'Johnson', 'Wilson', 'Brown', 'Cooper'],
        'email'      : ['john@email.com','jane@email.com','mike@techcorp.com','sarah@retailplus.com','bob@email.com','alice@freelance.com'],
        'phone'      : ['01234567890', '01987654321', '01555123456', '01777888999', '01111222333', '01444555666'],
        'postcode'   : ['SW1A1AA', 'M11AF', 'B11BB', 'LS12AJ', 'NE13NG', 'CF102HH'],
    }

# Decorator for header-based auth
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
@api.route('/customer')
class CustomerList(Resource):
    @api.marshal_list_with(customer_model)
    def get(self):
        """Get all customers - no authentication required"""
        return [dict(zip(enriched_customers().keys(), values)) 
                for values in zip(*enriched_customers().values())]

@api.route('/customer/<int:customer_id>')
class Customer(Resource):
    @api.marshal_with(customer_model)
    @api.response(404, 'Customer not found', error_model)
    def get(self, customer_id):
        """Get a specific customer by ID - no authentication required"""
        data = enriched_customers()
        try:
            index = data['customer_id'].index(customer_id)
            return {key: values[index] for key, values in data.items()}
        except ValueError:
            api.abort(404, 'Customer not found')

# Header authentication endpoints
@api.route('/customer1')
class Customer1List(Resource):
    @api.marshal_list_with(customer_model)
    @api.doc(security='apikey')
    @api.header('X-API-Key', 'API Key', required=True)
    @require_api_key_header
    def get(self):
        """Get all customers - requires X-API-Key header"""
        return [dict(zip(enriched_customers().keys(), values)) 
                for values in zip(*enriched_customers().values())]

@api.route('/customer1/<int:customer_id>')
class Customer1(Resource):
    @api.marshal_with(customer_model)
    @api.doc(security='apikey')
    @api.header('X-API-Key', 'API Key', required=True)
    @api.response(404, 'Customer not found', error_model)
    @require_api_key_header
    def get(self, customer_id):
        """Get a specific customer by ID - requires X-API-Key header"""
        data = enriched_customers()
        try:
            index = data['customer_id'].index(customer_id)
            return {key: values[index] for key, values in data.items()}
        except ValueError:
            api.abort(404, 'Customer not found')

# Query parameter authentication endpoints
@api.route('/customer2')
class Customer2List(Resource):
    @api.marshal_list_with(customer_model)
    @api.doc(params={'api_key': 'API Key for authentication'})
    @require_api_key_param
    def get(self):
        """Get all customers - requires api_key query parameter"""
        return [dict(zip(enriched_customers().keys(), values)) 
                for values in zip(*enriched_customers().values())]

@api.route('/customer2/<int:customer_id>')
class Customer2(Resource):
    @api.marshal_with(customer_model)
    @api.doc(params={'api_key': 'API Key for authentication'})
    @api.response(404, 'Customer not found', error_model)
    @require_api_key_param
    def get(self, customer_id):
        """Get a specific customer by ID - requires api_key query parameter"""
        data = enriched_customers()
        try:
            index = data['customer_id'].index(customer_id)
            return {key: values[index] for key, values in data.items()}
        except ValueError:
            api.abort(404, 'Customer not found')

@api.route('/version')
class Version(Resource):
    def get(self):
        """Get API version"""
        return {'version': __version__}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
