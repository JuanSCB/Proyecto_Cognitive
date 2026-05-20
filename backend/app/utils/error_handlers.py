from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from app.utils.exceptions import APIError


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({'error': True, 'message': error.description}), error.code

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({'error': True, 'message': error.message}), error.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({'error': True, 'message': str(error.orig)}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({'error': True, 'message': str(error)}), 400

    @app.errorhandler(Exception)
    def handle_exception(error):
        status_code = getattr(error, 'code', 500)
        return jsonify({'error': True, 'message': str(error)}), status_code
