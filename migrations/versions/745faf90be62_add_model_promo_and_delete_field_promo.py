"""add model Promo and delete field promo

Revision ID: 745faf90be62
Revises: b67cb6e4f80f
Create Date: 2024-10-31 22:45:31.971289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '745faf90be62'
down_revision = 'b67cb6e4f80f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alias', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_promo',
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('promo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['promo_id'], ['promo.id'], )
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('promo')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('promo', mysql.TEXT(), nullable=True))

    op.drop_table('course_promo')
    op.drop_table('promo')
    # ### end Alembic commands ###
