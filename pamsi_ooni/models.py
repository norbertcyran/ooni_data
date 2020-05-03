from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestResult(Base):
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True)
    country_code = Column(String(2))
    total_tampered = Column(Boolean, default=False)
    header_field_name_tampered = Column(Boolean, default=False)
    header_field_number_tampered = Column(Boolean, default=False)
    header_field_value_tampered = Column(Boolean, default=False)
    header_name_capitalization_tampered = Column(Boolean, default=False)
    header_name_diff = Column(Text, default='')
    start_time = Column(DateTime)
