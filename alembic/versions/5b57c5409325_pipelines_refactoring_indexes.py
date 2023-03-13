"""

Revision ID: 5b57c5409325
Revises: 68ce6a306b30
Create Date: 2023-03-10 12:27:59.043627

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "5b57c5409325"
down_revision = "68ce6a306b30"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_copr_build_targets_copr_build_group_id"),
        "copr_build_targets",
        ["copr_build_group_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_copr_build_group_id"),
        "pipelines",
        ["copr_build_group_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_koji_build_group_id"),
        "pipelines",
        ["koji_build_group_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_test_run_group_id"),
        "pipelines",
        ["test_run_group_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_sync_release_run_targets_sync_release_id"),
        "sync_release_run_targets",
        ["sync_release_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_sync_release_run_targets_sync_release_id"),
        table_name="sync_release_run_targets",
    )
    op.drop_index(op.f("ix_pipelines_test_run_group_id"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_koji_build_group_id"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_copr_build_group_id"), table_name="pipelines")
    op.drop_index(
        op.f("ix_copr_build_targets_copr_build_group_id"),
        table_name="copr_build_targets",
    )
    # ### end Alembic commands ###
