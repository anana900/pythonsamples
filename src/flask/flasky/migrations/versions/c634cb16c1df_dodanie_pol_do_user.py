"""dodanie pol do User

Revision ID: c634cb16c1df
Revises: 4c70847c3642
Create Date: 2023-11-23 23:41:18.388045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c634cb16c1df'
down_revision = '4c70847c3642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('about_me', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('member_since', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('member_since')
        batch_op.drop_column('about_me')
        batch_op.drop_column('location')

    # ### end Alembic commands ###
