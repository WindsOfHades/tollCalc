from datetime import datetime, timedelta

from workalendar.europe import Sweden


class DifferentDaysException(Exception):
    pass


class PassedTollTwiceSameTimeException(Exception):
    pass


def calculate_toll(vehicle, string_dates):
    total_fee = 0
    if is_toll_free(vehicle.get_type()):
        return total_fee

    dates = [datetime.strptime(d, "%Y-%m-%d %H:%M") for d in string_dates]
    validate_dates(dates)

    for date in dates:
        if (date > timedelta(hours=1) + vehicle.get_last_payment()):
            total_fee += get_fee(date)
            vehicle.set_last_payment(date)
        else:
            vehicle.set_last_payment(vehicle.get_last_payment())
        if total_fee >= 60:
            return 60

    return total_fee


def is_holiday(date):
    cal = Sweden()
    return not cal.is_working_day(date)


def is_toll_free(vehicle_type):
    toll_free_vehicles = ['MOTORBIKE', 'TRACTOR', 'EMERGENCY', 'DIPLOMAT', 'FOREIGN', 'MILITARY']
    if vehicle_type.upper() in toll_free_vehicles:
        return True


def get_fee(date):
    fee = 0
    if is_holiday(date):
        return fee

    passing_time = (date.hour, date.minute)

    if   (6, 00)  <= passing_time <= (6, 29):
        return 8
    elif (6, 30)  <= passing_time <= (6, 59):
        return 13
    elif (7, 00)  <= passing_time <= (7, 59):
        return 18
    elif (8, 00)  <= passing_time <= (8, 29):
        return 13
    elif (8, 30)  <= passing_time <= (14, 59):
        return 8
    elif (15, 00) <= passing_time <= (15, 29):
        return 13
    elif (15, 30) <= passing_time <= (16, 59):
        return 18
    elif (17, 00) <= passing_time <= (17, 59):
        return 13
    elif (18, 00) <= passing_time <= (18, 29):
        return 8
    else:
        return 0


def validate_dates(dates):
    _different_days(dates)
    _duplicate_dates(dates)


def _different_days(dates):
    max_interval =  max(dates) - min(dates)
    if max_interval > timedelta(days=1):
        raise DifferentDaysException('The vehicle passed on different days!')


def _duplicate_dates(dates):
    seen = set()
    for date in dates:
        if date in seen:
            raise PassedTollTwiceSameTimeException('{} is duplicated!'.format(date))
        seen.add(date)
