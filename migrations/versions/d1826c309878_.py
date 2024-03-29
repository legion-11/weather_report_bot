"""empty message

Revision ID: d1826c309878
Revises: 
Create Date: 2019-07-25 00:09:23.195670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1826c309878'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('user_chat_id', sa.String(length=20), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('notification_time', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_user_chat_id'), 'User', ['user_chat_id'], unique=True)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_user_chat_id'), table_name='User')
    op.drop_table('User')
    # ### end Alembic commands ###
