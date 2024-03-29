"""empty message

Revision ID: 21f60aca1f47
Revises: f2e64f36637f
Create Date: 2020-10-01 19:04:27.736357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21f60aca1f47'
down_revision = 'f2e64f36637f'
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
    sa.Column('product_name', sa.Integer(), nullable=False),
    sa.Column('days_number', sa.Integer(), nullable=False),
    sa.Column('return_date', sa.DateTime(), nullable=False),
    sa.Column('needed_date', sa.DateTime(), nullable=False),
    sa.Column('given_date', sa.DateTime(), nullable=True),
    sa.Column('hire_notes', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hire_number')
    )
    op.alter_column('product', 'sale_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'sale_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.drop_table('customer_hire_oder')
    # ### end Alembic commands ###
