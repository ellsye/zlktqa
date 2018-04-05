"""empty message

Revision ID: 651794c81655
Revises: 560393aac194
Create Date: 2018-04-05 17:54:36.198669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '651794c81655'
down_revision = '560393aac194'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'create_time')
    # ### end Alembic commands ###
