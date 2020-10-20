def load_from_session(session, values: dict) -> dict:
    out = {}
    for key in values:
        out[key] = session.get(key, values.get(key))
    return out


def load_into_session(session, values: dict) -> None:
    for key in values:
        session[key] = values[key]
