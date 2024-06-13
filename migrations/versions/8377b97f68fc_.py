"""empty message

Revision ID: 8377b97f68fc
Revises: 98a3a33aa456
Create Date: 2024-04-01 20:51:28.848751

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8377b97f68fc'
down_revision = '98a3a33aa456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=255), nullable=True))
        batch_op.drop_column('firstname')
        batch_op.drop_column('lastname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lastname', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('firstname', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
