"""Initial migration
Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-11 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=120), nullable=False),
        sa.Column('correo', sa.String(length=150), nullable=False, unique=True),
        sa.Column('rol', sa.String(length=50), nullable=False, server_default='usuario'),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_table(
        'actividades',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=120), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_table(
        'configuracion',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('modo_automatico', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('intensidad_led_default', sa.Integer(), nullable=False, server_default='70'),
        sa.Column('umbral_lux', sa.Integer(), nullable=False, server_default='300'),
        sa.Column('max_consumo', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_table(
        'sensores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('lux', sa.Float(), nullable=False),
        sa.Column('intensidad_led', sa.Integer(), nullable=False),
        sa.Column('consumo_energetico', sa.Float(), nullable=False),
        sa.Column('modo_automatico', sa.Boolean(), nullable=False),
        sa.Column('actividad_id', sa.Integer(), sa.ForeignKey('actividades.id'), nullable=True),
        sa.Column('registrado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_table(
        'historial_iluminacion',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sensor_id', sa.Integer(), sa.ForeignKey('sensores.id', ondelete='CASCADE'), nullable=False),
        sa.Column('lux', sa.Float(), nullable=False),
        sa.Column('intensidad_led', sa.Integer(), nullable=False),
        sa.Column('consumo_energetico', sa.Float(), nullable=False),
        sa.Column('modo_automatico', sa.Boolean(), nullable=False),
        sa.Column('actividad_id', sa.Integer(), sa.ForeignKey('actividades.id', ondelete='SET NULL'), nullable=True),
        sa.Column('registrado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_table(
        'consumo_energetico',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sensor_id', sa.Integer(), sa.ForeignKey('sensores.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_kwh', sa.Float(), nullable=False),
        sa.Column('periodo_inicio', sa.Date(), nullable=False),
        sa.Column('periodo_fin', sa.Date(), nullable=False),
        sa.Column('creado_en', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('consumo_energetico')
    op.drop_table('historial_iluminacion')
    op.drop_table('sensores')
    op.drop_table('configuracion')
    op.drop_table('actividades')
    op.drop_table('usuarios')
