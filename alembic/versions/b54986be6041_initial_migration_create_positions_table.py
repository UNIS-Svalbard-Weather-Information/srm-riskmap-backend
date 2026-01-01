"""Initial migration: Create positions table

Revision ID: b54986be6041
Revises: 
Create Date: 2026-01-02 00:08:28.824871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b54986be6041'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the positions table
    op.create_table('positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.String(), nullable=False),
        sa.Column('geometry', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_positions')),
        sa.UniqueConstraint('event_id', name='uq_position_event_id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_positions_id'), 'positions', ['id'], unique=False)
    op.create_index(op.f('ix_positions_event_id'), 'positions', ['event_id'], unique=True)
    # Use execute instead of create_index to use IF NOT EXISTS
    op.execute('''
        CREATE INDEX IF NOT EXISTS idx_positions_geometry 
        ON positions USING gist (geometry)
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes first
    op.execute('DROP INDEX IF EXISTS idx_positions_geometry')
    op.drop_index(op.f('ix_positions_event_id'), table_name='positions')
    op.drop_index(op.f('ix_positions_id'), table_name='positions')
    
    # Drop the table
    op.drop_table('positions')