"""add avatar url and full name to admins

Revision ID: 8d3562545a51
Revises: 51e0b88980da
Create Date: 2023-11-30 21:46:19.069592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d3562545a51'
down_revision = '51e0b88980da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('picture')

    # ### end Alembic commands ###
