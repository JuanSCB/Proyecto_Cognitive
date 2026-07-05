from flask_restx import Namespace, Resource
from app.services.ai_service import AIService
from app.decorators import require_role

ai_ns = Namespace('ai', description='Análisis inteligente del salón')


@ai_ns.route('/analyze-room/<int:idSalon>')
class AIAnalysisResource(Resource):
    @require_role('alumno')
    def post(self, idSalon, usuario_id=None, usuario_role=None):
        """Genera un diagnóstico inteligente del salón utilizando los datos reales almacenados."""
        try:
            result = AIService.analyze_room(idSalon)
            return result, 200
        except ValueError as exc:
            return {'error': True, 'message': str(exc)}, 404
        except Exception as exc:
            return {'error': True, 'message': f'No fue posible generar el análisis: {str(exc)}'}, 500
