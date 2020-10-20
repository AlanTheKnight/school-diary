import datetime
from typing import Union
from diary import models


def get_current_quarter() -> int:
    """
    Return current quarter, 0 if now is holidays' time.
    """
    today = datetime.date.today()
    for q in models.Quarters.objects.all():
        if q.begin <= today <= q.end:
            return q.number
    return 0


def get_quarter_by_date(date: Union[str, datetime.date]) -> int:
    """
    Return a number of quarter by a date
    stamp string or date object.
    If quarter does not exist, return 0 instead.

    Args:
        date: datestring or datetime.date instance
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    for q in models.Quarters.objects.all():
        if q.begin <= date <= q.end:
            return q.number
    return 0


def load_from_session(session, values: dict) -> dict:
    """
    Loads data from session.

    Args:
        session: current session.
        values: dict containing needed values and their
            default values.
    """
    out = {}
    for key in values:
        out[key] = session.get(key, values[key])
    return out


def load_into_session(session, values: dict) -> None:
    """
    Loads data into the session.

    Args:
        session: current session
        values: dict containing values to load into session.
    """
    for key in values:
        session[key] = values[key]


def get_default_quarter():
    def_term = get_current_quarter()
    if def_term == 0:
        def_term = 1
    return def_term


def each_contains(d: dict, values: list):
    for i in values:
        if i in d:
            return False
    return True
