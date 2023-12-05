from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Report, report_schema, reports_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/reports', methods=['POST'])
@token_required
def create_report(current_user_token):
    name = request.json['name']
    city = request.json['city']
    country = request.json['country']
    details = request.json['details']
    report_date = request.json['report_date']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    report = Report(name, city, country, details, report_date,  user_token = user_token)

    db.session.add(report)
    db.session.commit()

    response = report_schema.dump(report)
    return jsonify(response)

@api.route('/reports', methods = ['GET'])
@token_required
def get_report(current_user_token):
    a_user = current_user_token.token
    reports = Report.query.filter_by(user_token = a_user).all()
    response = reports_schema.dump(reports)
    return jsonify(response)

@api.route('/reports/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    report = Report.query.get(id)
    response = report_schema.dump(report)
    return jsonify(response)

@api.route('/reports/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    report = Report.query.get(id) 
    report.name = request.json['name']
    report.city = request.json['city']
    report.country = request.json['country']
    report.details = request.json['details']
    report.report_date = request.json['report_date']
    report.user_token = current_user_token.token

    db.session.commit()
    response = report_schema.dump(report)
    return jsonify(response)


@api.route('/reports/<id>', methods = ['DELETE'])
@token_required
def delete_report(current_user_token, id):
    report = Report.query.get(id)
    db.session.delete(report)
    db.session.commit()
    response = report_schema.dump(report)
    return jsonify(response)