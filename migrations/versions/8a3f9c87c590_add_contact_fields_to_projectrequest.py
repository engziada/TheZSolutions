"""Add contact fields to ProjectRequest

Revision ID: 8a3f9c87c590
Revises: 1ab85e4734e2
Create Date: 2025-01-09 03:52:58.079850

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '8a3f9c87c590'
down_revision = '1ab85e4734e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('features', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('contact_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('contact_email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('contact_phone', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('preferred_contact', sa.String(length=20), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('contact_info')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_info', sqlite.JSON(), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('preferred_contact')
        batch_op.drop_column('contact_phone')
        batch_op.drop_column('contact_email')
        batch_op.drop_column('contact_name')
        batch_op.drop_column('features')

    # ### end Alembic commands ###
