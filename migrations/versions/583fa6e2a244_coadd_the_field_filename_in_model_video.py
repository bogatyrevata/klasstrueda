"""coadd the field filename in model Video

Revision ID: 583fa6e2a244
Revises: cec14cccc96d
Create Date: 2024-11-22 09:04:04.883661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583fa6e2a244'
down_revision = 'cec14cccc96d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filename', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.drop_column('filename')

    # ### end Alembic commands ###
