"""empty message

Revision ID: c5d3a633af1b
Revises: 
Create Date: 2020-09-26 11:54:06.365086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5d3a633af1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('sale_type', sa.String(length=20), nullable=True))
    op.execute("UPDATE product SET sale_type = 'sale'")
    op.alter_column('product', 'sale_type', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'sale_type')
    # ### end Alembic commands ###
