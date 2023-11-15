"""add author to message

Revision ID: 56acacfa976d
Revises: d7f38e3787e3
Create Date: 2023-11-13 17:15:03.174143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56acacfa976d'
down_revision = 'd7f38e3787e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'visitors', ['author'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author')

    # ### end Alembic commands ###
