"""empty message

Revision ID: 53af70884387
Revises: b6df0682b149
Create Date: 2021-08-26 20:30:32.170383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53af70884387'
down_revision = 'b6df0682b149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
