"""Initial

Revision ID: d92675e13a99
Revises: 
Create Date: 2021-10-23 19:11:01.538588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd92675e13a99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('chats',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.Column('chat_name', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.login'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=False),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.login'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('chat_id', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['client_id'], ['clients.login'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id', 'chat_id')
    )
    op.create_table('messages',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('message_id', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('chat_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id')
    )
    op.create_table('user_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timezone', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks_results',
    sa.Column('task_id', sa.String(), nullable=True),
    sa.Column('message_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['messages.message_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.task_id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_results')
    op.drop_table('user_settings')
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('chats')
    op.drop_table('clients')
    # ### end Alembic commands ###
