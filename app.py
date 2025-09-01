from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json

# Get the version number
from version import __version__

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-for-development')

def enriched_customers():
    enriched_customers = {
        'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],
        'first_name': ['John', 'Jane', 'Mike', 'Sarah', 'Bob', 'Alice'],
        'last_name': ['Smith', 'Doe', 'Johnson', 'Wilson', 'Brown', 'Cooper'],
        'email': ['john@email.com','jane@email.com','mike@techcorp.com','sarah@retailplus.com','bob@email.com','alice@freelance.com'],
        'phone': ['01234567890', '01987654321', '01555123456', '01777888999', '01111222333', '01444555666'],
        'postcode': ['SW1A1AA', 'M11AF', 'B11BB', 'LS12AJ', 'NE13NG', 'CF102HH'],
        'status': ['active', 'active', 'active', 'suspended', 'active', 'active'],
    }
    return enriched_customers

def regions():
    regions = {
        'postcode': ['SW1A1AA', 'M11AF', 'B11BB', 'LS12AJ', 'NE13NG', 'CF102HH'],
        'region': ['London', 'North West', 'West Midlands', 'Yorkshire and The Humber', 'North East', 'Wales'],
        'country': ['England', 'England', 'England', 'England', 'England', 'Wales'],
        'district': ['Westminster', 'Manchester', 'Birmingham', 'Leeds', 'Newcastle', 'Cardiff'],
        'longitude': [-0.1419, -2.2426, -1.8904, -1.5491, -1.6131, -3.1791],
        'latitude': [51.5014, 53.4794, 52.4796, 53.7997, 54.9738, 51.4816],
        'geo_enriched': [1, 1, 1, 1, 1, 1]
    }
    return regions

@app.route("/customer")
def api_customer():
    data = enriched_customers()
    return jsonify(data)

@app.route("/customer/<int:customer_id>")
def api_customer_by_id(customer_id):
    data = enriched_customers()
    try:
        index = data['customer_id'].index(customer_id)
        customer = {key: values[index] for key, values in data.items()}
        return jsonify(customer)
    except ValueError:
        return jsonify({'error': 'Customer not found'}), 404

@app.route("/region")
def api_region():
    data = regions()
    return jsonify(data)

@app.route("/region/<postcode>")
def api_region_by_postcode(postcode):
    data = regions()
    try:
        index = data['postcode'].index(postcode)
        region = {key: values[index] for key, values in data.items()}
        return jsonify(region)
    except ValueError:
        return jsonify({'error': 'Postcode not found'}), 404

@app.route("/company")
def api_company():
    companies = {
        'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],  # Links to customer records
        'company': ['', '', 'TechCorp Ltd', 'Retail Plus', '', 'Freelance Design'],
        'company_size': ['Individual', 'Individual', 'Medium (50-250 employees)', 'Large (250+ employees)', 'Individual', 'Micro (1-10 employees)'],
        'industry': ['Personal', 'Personal', 'Technology', 'Retail', 'Personal', 'Creative Services'],
        'annual_revenue': ['N/A', 'N/A', '£2M-£10M', '£10M+', 'N/A', '£0-£100K'],
        'is_business': [0, 0, 1, 1, 0, 1]
    }
    return jsonify(companies)

@app.route("/status")
def api_status():
    account_status = {
        'status': ['active', 'suspended']
    }
    return jsonify(account_status)

@app.route('/version')
def version():
    return __version__, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
