from app.controllers.activity_controller import activity_ns
from app.controllers.consumo_controller import consumo_ns
from app.controllers.dashboard_controller import dashboard_ns
from app.controllers.historial_controller import historial_ns
from app.controllers.sensor_controller import sensor_ns
from app.controllers.salon_controller import salon_ns
from app.controllers.user_controller import user_ns
from app.controllers.auth_controller import auth_ns
from app.controllers.chat_controller import chat_ns
from app.controllers.health.health_controller import health_ns
from app.controllers.report_controller import report_ns


def register_routes(api):
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(chat_ns, path='/api/chat')
    api.add_namespace(sensor_ns, path='/api/sensores')
    api.add_namespace(activity_ns, path='/api/actividades')
    api.add_namespace(user_ns, path='/api/usuarios')
    api.add_namespace(historial_ns, path='/api/historial')
    api.add_namespace(consumo_ns, path='/api/consumo')
    api.add_namespace(salon_ns, path='/api/salones')
    api.add_namespace(dashboard_ns, path='/api/dashboard')
    api.add_namespace(health_ns, path='/api/health')
    api.add_namespace(report_ns, path='/api/reportes')
