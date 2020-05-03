# OONI data fetcher
Fetch and parse data from [OONI Probe](https://www.measurementlab.net/tests/ooni/).


## Install

1. Install [poetry](https://python-poetry.org/docs/)
2. Run `poetry install`
3. Run `poetry shell`
4. Run `alembic upgrade head`
5. To populate DB with MLab data, run `python populate_db.py`

The M-Lab OONI Probe Data Set, 11.2014 - 07.2016. https://measurementlab.net/tests/ooni