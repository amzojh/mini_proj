"""create table

Revision ID: d3b83bf53170
Revises: 
Create Date: 2019-09-28 17:21:51.830513

"""
from alembic import op
import sqlalchemy as sa

from Database.Model.dart import dartReportType, dartReportList

# revision identifiers, used by Alembic.
revision = 'd3b83bf53170'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        dartReportType.__tablename__,
        dartReportType.id,
        dartReportType.symbol,
        dartReportType.company_name,
        dartReportType.sector,
        dartReportType.industry,
        dartReportType.market
    )

    op.create_table(
        dartReportList.__tablename__,
        dartReportList.id,
        dartReportList.symbol,
        dartReportList.issue_company,
        dartReportList.issue_date,
        dartReportList.report_link,
        dartReportList.report_name,
        dartReportList.disclosure_company, 
        dartReportList.report_id
    )
    pass


def downgrade():

    op.drop_table(dartReportType.__tablename__)
    op.drop_table(dartReportList.__tablename__)

    pass
