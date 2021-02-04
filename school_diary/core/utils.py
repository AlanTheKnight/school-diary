def calculate_avg(data: list):
    avg = round(data[2] / data[3], 1) if data[3] != 0 else None
    sm_avg = round(data[0] / data[1], 1) if data[1] != 0 else None
    return (avg, sm_avg)


def get_needed_mark(amounts_sum, quantity, avg):
    """
    Give a number of '5's needed to get
    a certain mark in quarter result. Return 2
    values: an amount and what mark is needed to get.
    """
    if avg is None:
        return (1, 5)
    needed, needed_mark = 0, 0
    if avg <= 4.5:
        needed = 9 * quantity - 2 * amounts_sum + 1
        needed_mark = 5
    if avg <= 3.5:
        needed = (7 * quantity - 2 * amounts_sum) // 3 + 1
        needed_mark = 4
    if avg <= 2.5:
        needed = (5 * quantity - 2 * amounts_sum) // 5 + 1
        needed_mark = 3
    return needed, needed_mark
