"""Adadd video_homework and lesson file

Revision ID: 3fc47c7a15bd
Revises: 6b26d87d5737
Create Date: 2024-08-07 20:22:07.274782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3fc47c7a15bd'
down_revision = '6b26d87d5737'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video_homework',
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('homework_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homework_id'], ['homework.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], )
    )
    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=2048),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', sa.String(length=255), nullable=True))
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=2048),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=2048),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=2048),
               existing_nullable=True)

    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=2048),
               existing_nullable=True)
        batch_op.drop_column('file')

    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=2048),
               existing_nullable=True)

    op.drop_table('video_homework')
    # ### end Alembic commands ###
