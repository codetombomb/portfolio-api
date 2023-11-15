"""add sender type to messsage

Revision ID: 5e3686493d50
Revises: a2d3945f7d08
Create Date: 2023-11-15 13:12:11.177204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e3686493d50'
down_revision = 'a2d3945f7d08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender_type', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('sender_type')

    # ### end Alembic commands ###
