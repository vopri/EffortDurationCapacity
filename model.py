from datetime import date, timedelta


def calc_effort(duration_in_days: float, capacity_in_fte: float) -> float:
    return duration_in_days * capacity_in_fte


def calc_duration(effort_in_pd: float, capacity_in_fte: float) -> float:
    return effort_in_pd / capacity_in_fte


def calc_capacity(effort_in_pd: float, duration_in_days: float) -> float:
    return effort_in_pd / duration_in_days


def count_workdays(from_: date, to: date) -> int:
    amount_of_days = (to - from_).days + 1
    amount_of_full_weeks, days_outside_of_full_weeks = divmod(amount_of_days, 7)
    amount_of_workdays = amount_of_full_weeks * 5
    if days_outside_of_full_weeks == 0:
        return amount_of_workdays
    amount_of_workdays += _add_days_outside_of_full_weeks(
        from_, to, amount_of_full_weeks
    )
    return amount_of_workdays


def _add_days_outside_of_full_weeks(from_, to, amount_of_full_weeks):
    additional_days = 0
    first_day_not_in_full_weeks = from_ + timedelta(days=amount_of_full_weeks * 7)
    date_ = to
    while date_ >= first_day_not_in_full_weeks:
        if date_.isoweekday() not in (6, 7):
            additional_days += 1
        date_ -= timedelta(days=1)
    return additional_days
