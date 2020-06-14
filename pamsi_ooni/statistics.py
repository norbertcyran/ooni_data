from typing import Tuple

import numpy as np
import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import Query

from .db import Session
from .models import TestResult


def get_tampered_requests() -> Query:
    session = Session()
    return session.query(TestResult).filter(or_(
        TestResult.total_tampered,
        TestResult.header_name_capitalization_tampered,
        TestResult.header_field_number_tampered,
        TestResult.header_field_name_tampered,
        TestResult.header_field_value_tampered,
        TestResult.request_line_capitalization_tampered
    ))


def get_monthly_tampering(country_code: str) -> pd.DataFrame:
    query = get_tampered_requests().filter_by(country_code=country_code)
    df = pd.read_sql(query.statement, query.session.bind)
    df.set_index('start_time', inplace=True)
    df = df.resample('M').count()
    df.index = df.index.to_period('M')
    ret_df = pd.DataFrame({'Month': df.index, 'Tampered': df.id.values})
    ret_df.set_index('Month')
    return ret_df


def tampering_linear_regression() -> Tuple[float]:
    query = get_tampered_requests()
    df = pd.read_sql(query.statement, query.session.bind)
    df = df.set_index('start_time', inplace=True)
    df = df.resample('M').count()
    y = np.array(df['id'].values, dtype=int)
    x = np.array(pd.to_datetime(df.index).values, dtype=float)


