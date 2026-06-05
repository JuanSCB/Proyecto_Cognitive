from flask_restx import fields
from app import api

user_model = api.model('Usuario', {
    'id': fields.Integer(readonly=True, description='ID del usuario'),
    'nombre': fields.String(required=True, description='Nombre completo'),
    'correo': fields.String(required=True, description='Correo electrónico')
})

activity_model = api.model('Actividad', {
    'id': fields.Integer(readonly=True, description='ID de la actividad'),
    'nombre': fields.String(required=True, description='Nombre de la actividad', example='Conferencia'),
    'descripcion': fields.String(description='Descripción de la actividad', example='Reunión general en sala principal'),
    'lux_minimo': fields.Integer(description='Valor mínimo de lux para la actividad', example=300),
    'lux_maximo': fields.Integer(description='Valor máximo de lux para la actividad', example=500)
})

salon_input = api.model('SalonInput', {
    'nombre': fields.String(required=True, description='Nombre del salón', example='Aula A101'),
    'ubicacion': fields.String(description='Ubicación del salón', example='Edificio B, piso 2'),
    'descripcion': fields.String(description='Descripción del salón', example='Sala para clases de informática'),
    'actividad_id': fields.Integer(required=False, description='ID de actividad asociada', example=4, nullable=True)
})

salon_update_input = api.model('SalonUpdateInput', {
    'nombre': fields.String(description='Nombre del salón', example='Aula A101'),
    'ubicacion': fields.String(description='Ubicación del salón', example='Edificio B, piso 2'),
    'descripcion': fields.String(description='Descripción del salón', example='Sala para clases de informática'),
    'actividad_id': fields.Integer(description='ID de actividad asociada', example=4, allow_null=True)
})

salon_model = api.model('Salon', {
    'id': fields.Integer(readonly=True, description='ID del salón'),
    'nombre': fields.String(description='Nombre del salón'),
    'ubicacion': fields.String(description='Ubicación del salón'),
    'descripcion': fields.String(description='Descripción del salón'),
    'actividad_id': fields.Integer(description='Actividad asociada'),
    'actividad_nombre': fields.String(description='Nombre de la actividad actual asociada', attribute='actividad_nombre'),
    'creado_en': fields.DateTime(description='Fecha de creación'),
    'actualizado_en': fields.DateTime(description='Fecha de última actualización')
})

dashboard_salon_model = api.model('DashboardSalon', {
    'salon_id': fields.Integer(description='ID del salón'),
    'nombre': fields.String(description='Nombre del salón'),
    'actividad_id': fields.Integer(description='Actividad actual asociada'),
    'actividad_nombre': fields.String(description='Nombre de la actividad actual asociada'),
    'lux': fields.Float(description='Último nivel de luminosidad registrado'),
    'lux_minimo': fields.Integer(description='Valor mínimo de lux para la actividad'),
    'lux_maximo': fields.Integer(description='Valor máximo de lux para la actividad'),
    'estado_iluminacion': fields.String(description='Estado de iluminación calculado'),
    'nivel_alerta': fields.String(description='Nivel de alerta del salón'),
    'intensidad_led': fields.Integer(description='Última intensidad LED registrada'),
    'consumo_energetico': fields.Float(description='Último consumo energético registrado'),
    'modo_automatico': fields.Boolean(description='Último modo automático registrado')
})

config_model = api.model('Configuracion', {
    'id': fields.Integer(readonly=True, description='ID de configuración'),
    'modo_automatico': fields.Boolean(required=True, description='Modo automático habilitado'),
    'intensidad_led_default': fields.Integer(required=True, description='Intensidad LED por defecto'),
    'umbral_lux': fields.Integer(required=True, description='Umbral de luminosidad ambiental'),
    'max_consumo': fields.Float(required=True, description='Máximo consumo energético permitido')
})

sensor_input = api.model('SensorInput', {
    'salon_id': fields.Integer(required=True, description='ID del salón asociado', example=1),
    'lux': fields.Float(required=True, description='Nivel de luminosidad ambiental', example=210.5),
    'intensidad_led': fields.Integer(required=True, description='Intensidad del LED', example=65),
    'consumo_energetico': fields.Float(required=True, description='Consumo energético en kWh', example=0.85),
    'modo_automatico': fields.Boolean(required=True, description='Modo automático/manual', example=True),
    'actividad_id': fields.Integer(required=False, description='ID de actividad asociada')
})

sensor_model = api.model('Sensor', {
    'id': fields.Integer(readonly=True, description='ID del registro de sensor'),
    'salon_id': fields.Integer(description='ID del salón asociado'),
    'lux': fields.Float(description='Nivel de luminosidad ambiental'),
    'intensidad_led': fields.Integer(description='Intensidad LED actual'),
    'consumo_energetico': fields.Float(description='Consumo energético actual'),
    'modo_automatico': fields.Boolean(description='Indica si el modo es automático'),
    'actividad_id': fields.Integer(description='Actividad asociada'),
    'registrado_en': fields.DateTime(description='Fecha y hora de registro')
})

consumption_model = api.model('ConsumoEnergetico', {
    'id': fields.Integer(readonly=True, description='ID del registro de consumo'),
    'sensor_id': fields.Integer(description='ID del sensor asociado'),
    'total_kwh': fields.Float(description='Consumo total en kWh'),
    'periodo_inicio': fields.Date(description='Fecha de inicio del periodo'),
    'periodo_fin': fields.Date(description='Fecha de fin del periodo'),
    'creado_en': fields.DateTime(description='Fecha de creación del registro')
})

paginated_sensor_model = api.model('PaginatedSensores', {
    'items': fields.List(fields.Nested(sensor_model), description='Registros de sensores por página'),
    'page': fields.Integer(description='Página actual', example=1),
    'limit': fields.Integer(description='Límite de registros por página', example=20),
    'total': fields.Integer(description='Total de registros disponibles', example=100)
})

average_lux_model = api.model('PromedioLux', {
    'promedio_lux': fields.Float(description='Valor promedio de lux'),
    'cantidad_registros': fields.Integer(description='Cantidad de registros utilizados para el cálculo')
})

total_consumo_model = api.model('ConsumoTotal', {
    'total_consumo': fields.Float(description='Consumo energético total en kWh')
})

health_model = api.model('HealthStatus', {
    'status': fields.String(description='Estado del servicio', example='ok'),
    'service': fields.String(description='Nombre del servicio', example='Sistema Inteligente de Iluminación'),
    'version': fields.String(description='Versión de la API', example='1.0')
})

statistics_model = api.model('EstadisticasReportes', {
    'promedio_lux': fields.Float(description='Promedio de lux en el historial'),
    'promedio_intensidad_led': fields.Float(description='Promedio de intensidad LED en el historial'),
    'total_consumo_energetico': fields.Float(description='Consumo energético total en kWh'),
    'cantidad_registros': fields.Integer(description='Cantidad total de registros'),
    'ultimo_registro': fields.Nested(sensor_model, description='Último registro de sensor', skip_none=True)
})

cumplimiento_iluminacion_model = api.model('CumplimientoIluminacion', {
    'salon_id': fields.Integer(description='ID del salón'),
    'porcentaje_adecuado': fields.Integer(description='Porcentaje de lecturas dentro del rango'),
    'porcentaje_insuficiente': fields.Integer(description='Porcentaje de lecturas por debajo del rango'),
    'porcentaje_excesivo': fields.Integer(description='Porcentaje de lecturas por encima del rango')
})

report_model = api.model('Reporte', {
    'total_registros': fields.Integer(description='Total de registros en el historial'),
    'energia_total': fields.Float(description='Consumo energético total en kWh'),
    'ultimo_registro': fields.Nested(sensor_model)
})
