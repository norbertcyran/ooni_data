"""Add request_line_capitalization_tampered column

Revision ID: cc1832473f52
Revises: be564f658817
Create Date: 2020-05-04 00:31:55.082170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc1832473f52'
down_revision = 'be564f658817'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('test_results') as batch_op:
        batch_op.add_column(sa.Column('request_line_capitalization_tampered', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('test_results') as batch_op:
        batch_op.drop_column('request_line_capitalization_tampered')
    # ### end Alembic commands ###
