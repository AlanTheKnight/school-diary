def get_quarter_by_date(datestring: str) -> int:
    """
    Returns a number of a quarter by the date stamp string.
    If quarter does not exit, return 0 instead.
    """
    converted_date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    year = converted_date.year
    for i in range(0, 4):
        start = datetime.date(year, TERMS[i][0][1], TERMS[i][0][0])
        end = datetime.date(year, TERMS[i][1][1], TERMS[i][1][0])
        if start <= converted_date <= end:
            return i + 1
    else:
        return 0
        