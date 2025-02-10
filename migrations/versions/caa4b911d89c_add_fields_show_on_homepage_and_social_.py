"""add fields show_on_homepage and social contacts in Artist model

Revision ID: caa4b911d89c
Revises: 1e110891469f
Create Date: 2025-01-28 12:39:40.334046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caa4b911d89c'
down_revision = '1e110891469f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('show_on_homepage', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('facebook', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('instagram', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('youtube', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('vkontakte', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.drop_column('vkontakte')
        batch_op.drop_column('youtube')
        batch_op.drop_column('instagram')
        batch_op.drop_column('facebook')
        batch_op.drop_column('show_on_homepage')

    # ### end Alembic commands ###
