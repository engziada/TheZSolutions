"""add job applications and project requests

Revision ID: add_job_applications_and_project_requests
Revises: 
Create Date: 2024-12-20 05:50:03.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_job_applications_and_project_requests'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create job_application table
    op.create_table(
        'job_application',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('years_of_experience', sa.Integer()),
        sa.Column('skills', sa.JSON()),
        sa.Column('portfolio_url', sa.String(length=200)),
        sa.Column('github_url', sa.String(length=200)),
        sa.Column('linkedin_url', sa.String(length=200)),
        sa.Column('resume_path', sa.String(length=200)),
        sa.Column('cover_letter', sa.Text()),
        sa.Column('status', sa.String(length=20), default='pending'),
        sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('admin_notes', sa.Text()),
        sa.Column('reviewed_by_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create project_request table
    op.create_table(
        'project_request',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50)),
        sa.Column('budget_min', sa.Float()),
        sa.Column('budget_max', sa.Float()),
        sa.Column('timeline', sa.String(length=50)),
        sa.Column('priority', sa.String(length=20), default='normal'),
        sa.Column('status', sa.String(length=20), default='new'),
        sa.Column('client_name', sa.String(length=100), nullable=False),
        sa.Column('client_email', sa.String(length=120), nullable=False),
        sa.Column('client_phone', sa.String(length=20)),
        sa.Column('company_name', sa.String(length=100)),
        sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('admin_notes', sa.Text()),
        sa.Column('reviewed_by_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create project_request_attachment table
    op.create_table(
        'project_request_attachment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_request_id', sa.Integer(), sa.ForeignKey('project_request.id'), nullable=False),
        sa.Column('filename', sa.String(length=200), nullable=False),
        sa.Column('file_path', sa.String(length=200), nullable=False),
        sa.Column('file_type', sa.String(length=50)),
        sa.Column('uploaded_at', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('project_request_attachment')
    op.drop_table('project_request')
    op.drop_table('job_application')
