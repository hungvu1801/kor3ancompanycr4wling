from sqlalchemy import (MetaData, Table, Column, Integer, String, Date, ForeignKey, 
    DateTime, Boolean, UniqueConstraint, String, TEXT)
from sqlalchemy.sql import func


def create_table_company_master(engine, metadata) -> None:
    _ = Table(
        "tbl_company_master", metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column("company_name_kor", String(100)),
        Column("company_name_eng", String(100)),
        Column("company_code", String(50)),
        Column("representative", String(100)),
        Column("market_listing", String(20)),
        Column("corp_registration_no", String(20)),
        Column("tax_id", String(50), unique=True),
        Column("address", String(255)),
        Column("website", String(255)),
        Column("ir_website", String(255)),
        Column("tel", String(50)),
        Column("fax", String(50)),
        Column("industry", String(255)),
        Column("est_date", Date),
        Column("end_month_fy", Integer),
        Column("url_", String(255)),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime, onupdate=func.now()),
        UniqueConstraint("tax_id", name="uq_tax_id")
        )
    metadata.create_all(engine)

def create_table_company_deepsearch(engine, metadata) -> None:
    _ = Table(
        "tbl_company_deepsearch", metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('id_com', Integer, ForeignKey("tbl_company_master.id", ondelete="CASCADE")),
        Column('eng_search', TEXT),
        Column('kor_search', TEXT),
        Column('is_valid', Boolean, ),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime, onupdate=func.now()),
              )
    metadata.create_all(engine)

def create_table_company_code_staging(engine, metadata) -> None:
    _ = Table(
        "tbl_company_code_staging", metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('corp_code', String(100)),
        Column('company_name_kor', String(100)),
        Column('company_name_eng', String(100)),
        Column('stock_code', String(100)),
        Column('modify_date', Date),
        Column('created_at', DateTime, default=func.now()),
        Column('updated_at', DateTime, onupdate=func.now()),
              )
    metadata.create_all(engine)


def create_table_company_code(engine, metadata) -> None:
    _ = Table(
        "tbl_company_code", metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('id_com', Integer, ForeignKey("tbl_company_master.id", ondelete="CASCADE")),
        Column('corp_code', String(100)),
        Column('company_name_kor', String(100)),
        Column('company_name_eng', String(100)),
        Column('stock_code', String(100)),
        Column('modify_date', String(100)),
        Column('created_at', DateTime, default=func.now()),
        Column('updated_at', DateTime, onupdate=func.now()),
              )
    metadata.create_all(engine)