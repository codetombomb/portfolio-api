"""add visitor id and admin id to message table

Revision ID: a2d3945f7d08
Revises: bb60e4480082
Create Date: 2023-11-15 12:38:54.376905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2d3945f7d08'
down_revision = 'bb60e4480082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('visitor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'admins', ['admin_id'], ['id'])
        batch_op.create_foreign_key(None, 'visitors', ['visitor_id'], ['id'])
        batch_op.drop_column('sender_id')
        batch_op.drop_column('sender_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender_type', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('visitor_id')
        batch_op.drop_column('admin_id')

    # ### end Alembic commands ###
