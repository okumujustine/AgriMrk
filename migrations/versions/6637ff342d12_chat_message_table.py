"""chat-message-table

Revision ID: 6637ff342d12
Revises: cf277cbd7d51
Create Date: 2020-11-10 21:51:29.755977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6637ff342d12'
down_revision = 'cf277cbd7d51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_message',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('thread_id', sa.BigInteger(), nullable=True),
    sa.Column('sender_phone', sa.BigInteger(), nullable=False),
    sa.Column('receiver_phone', sa.BigInteger(), nullable=False),
    sa.Column('message', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['chat_thread.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_message')
    # ### end Alembic commands ###
