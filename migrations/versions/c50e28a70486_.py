"""empty message

Revision ID: c50e28a70486
Revises: 21f60aca1f47
Create Date: 2020-10-04 13:13:09.690629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50e28a70486'
down_revision = '21f60aca1f47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_hire_oder',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('hire_number', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('days_number', sa.Integer(), nullable=False),
    sa.Column('return_date', sa.DateTime(), nullable=False),
    sa.Column('needed_date', sa.DateTime(), nullable=False),
    sa.Column('given_date', sa.DateTime(), nullable=True),
    sa.Column('hire_notes', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hire_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer_hire_oder')
    # ### end Alembic commands ###