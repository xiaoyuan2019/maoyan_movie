"""empty message

Revision ID: b22a7c7e90b7
Revises: ffaf615286a0
Create Date: 2019-09-23 17:07:07.731198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b22a7c7e90b7'
down_revision = 'ffaf615286a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('action2019', sa.Column('detail_id', sa.String(length=32), nullable=False))
    op.add_column('comedy2019', sa.Column('detail_id', sa.String(length=32), nullable=False))
    op.add_column('top100', sa.Column('detail_id', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('top100', 'detail_id')
    op.drop_column('comedy2019', 'detail_id')
    op.drop_column('action2019', 'detail_id')
    # ### end Alembic commands ###