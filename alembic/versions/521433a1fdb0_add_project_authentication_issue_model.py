"""Add_project_authentication_issue_model

Revision ID: 521433a1fdb0
Revises: 726cb0f70c6d
Create Date: 2020-08-19 11:08:20.747708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "521433a1fdb0"
down_revision = "726cb0f70c6d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project_authentication_issue",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issue_created", sa.Boolean(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["git_projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("project_authentication_issue")
    # ### end Alembic commands ###
