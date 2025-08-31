from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json

# Get the version number
from version import __version__

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-for-development')

@app.route("/api")
def block_api_root():
    return "Access to /api is not allowed", 403

@app.route("/api/customer")
def api_customer():
    enriched_customers = {
        'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],
        'first_name': ['John', 'Jane', 'Mike', 'Sarah', 'Bob', 'Alice'],
        'last_name': ['Smith', 'Doe', 'Johnson', 'Wilson', 'Brown', 'Cooper'],
        'email': ['john@email.com', 'jane@email.com', 'mike@techcorp.com', 
                  'sarah@retailplus.com', 'bob@email.com', 'alice@freelance.com'],
        'phone': ['01234567890', '01987654321', '01555123456', 
                  '01777888999', '01111222333', '01444555666'],
        'postcode': ['SW1A 1AA', 'M1 1AF', 'B1 1BB', 'LS1 2AJ', 'NE1 3NG', 'CF10 2HH']
    }
    return jsonify(enriched_customers)

@app.route("/api/region")
def api_region():
    regions = {
        'region_id': [1, 2, 3, 4, 5, 6],  # Links to customer records by position
        'postcode': ['SW1A 1AA', 'M1 1AF', 'B1 1BB', 'LS1 2AJ', 'NE1 3NG', 'CF10 2HH'],
        'region': ['London', 'North West', 'West Midlands', 'Yorkshire and The Humber', 'North East', 'Wales'],
        'country': ['England', 'England', 'England', 'England', 'England', 'Wales'],
        'district': ['Westminster', 'Manchester', 'Birmingham', 'Leeds', 'Newcastle', 'Cardiff'],
        'longitude': [-0.1419, -2.2426, -1.8904, -1.5491, -1.6131, -3.1791],
        'latitude': [51.5014, 53.4794, 52.4796, 53.7997, 54.9738, 51.4816],
        'geo_enriched': [1, 1, 1, 1, 1, 1]
    }
    return jsonify(regions)

@app.route("/api/company")
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

@app.route("/api/status")
def api_status():
    account_status = {
        'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],  # Links to customer records
        'status': ['active', 'active', 'active', 'suspended', 'active', 'active']
    }
    return jsonify(account_status)

@app.route('/version')
def version():
    return __version__, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
