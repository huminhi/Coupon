

__all__ = [
        'BIWEEKLY',
        'BIWEEKLY15',
        'BLINK',
        'DAY',
        'FORTNIGHT',
        'MONTHLY',
        'QUARTERLY',
        'WEEK',
        'WEEKLY',
        'add_month',
        'calc_date',
        'ensure_datetime',
        'get_cycle_due',
        'next_date',
        'next_month_year',
        'parse_datetime',
        'previous_date',
        'next_cycle',
        'start_cycle',
        'iter_cycle',
        'iter_days',
        ]


from datetime import date, datetime, time, timedelta
import logging


DT_FORMATS = (
        '%m%d%y',
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        )

(WEEKLY, BIWEEKLY, BIWEEKLY15, MONTHLY, QUARTERLY) = range(5)
DAY = timedelta(1)
WEEK = timedelta(7)
FORTNIGHT = timedelta(14)
BLINK = timedelta(0, 0, 0, 1)


def next_month_year(d, day):
    """ This returns a new date, one month from d, with the day set to day. """
    month = d.month + 1
    year = d.year
    if month >= 13:
        year += 1
        month -= 12
    return date(year, month, day)


def get_cycle_due(activation_date=None):
    """ This gets the cycle due date for a given activation date. """
    activation_date = activation_date or date.today()
    day = activation_date.day
    if day == 1:
        # 22nd of the same month
        return activation_date.replace(day=22)
    elif 1 < day <= 6:
        # 1st of next month
        return next_month_year(activation_date, 1)
    elif 6 < day <= 16:
        # 6th of next month
        return next_month_year(activation_date, 6)
    elif 16 < day <= 22:
        # 16th of next month
        return next_month_year(activation_date, 16)
    elif 22 < day <= 31:
        # 22nd of next month
        return next_month_year(activation_date, 22)


def parse_datetime(string, formats=DT_FORMATS):
    if string is None:
        return None
    string = string.split('.')[0]
    for f in formats:
        try:
            return datetime.strptime(string, f)
        except:
            pass
    return None


def previous_date(interval, current):
    if isinstance(current, date):
        previous = current = datetime.combine(current, time())
    else:
        previous = current.replace(hour=0, minute=0, second=0)
    if interval == WEEKLY:
        dow = current.isoweekday() % 7
        return (current-WEEK if dow == 0 else current-timedelta(dow))
    elif interval == BIWEEKLY:
        day = previous.day
        if previous < current:
            day += 1
        if day == 1:
            previous = add_month(previous, -1)
            previous += timedelta(15)
        elif day == 16:
            previous -= timedelta(15)
        else:
            if day > 16:
                day_to_sub = previous.day - 16
            elif day > 1:
                day_to_sub = previous.day - 1
            previous -= timedelta(day_to_sub)
    elif interval == MONTHLY:
        day = previous.day
        if previous < current:
            day += 1
        if day == 1:
            previous = add_month(previous, -1)
        else:
            day_to_sub = previous.day - 1
            previous -= timedelta(day_to_sub)
    elif interval == QUARTERLY:
        while True:
            previous = previous_date(MONTHLY, previous)
            month = previous.month
            if month in (1, 3, 6, 9):
                return previous
    else:
        raise Exception, 'Invalid date interval: %s' % (interval,)
    return previous

    # The old version, kept here for when it's needed to refer to. --Eric
    if isinstance(current, datetime):
        current = current.date()
    if interval == WEEKLY:
        dow = current.weekday() + 1
        if dow != 0:
            return current - timedelta(dow)
        else:
            return current - WEEK
    elif interval == BIWEEKLY:
        if current.day == 1:
            if current.month == 1:
                return date(current.year-1, 12, 16)
            else:
                return current.replace(month=current.month-1, day=16)
        elif current.day == 16:
            return current.replace(day=1)
        elif current.day > 16:
            return current.replace(day=16)
        elif current.day > 1:
            return current.replace(day=1)
    elif interval == BIWEEKLY16:
        pass
    elif interval == MONTHLY:
        if current.day == 1:
            if current.month == 1:
                return date(current.year-1, 12, current.day)
            else:
                return current.replace(month=current.month-1)
        else:
            return current.replace(day=1)
    elif interval == QUARTERLY:
        while True:
            current = previous_date(MONTHLY, current)
            if current.month in (1, 3, 6, 9):
                return current
    else:
        raise Exception, 'Invalid date interval: %s' % (interval,)


def add_month(dt, n=1):
    (day, month, year) = (dt.day, dt.month, dt.year)
    next_month = month + n
    while next_month > 12:
        year = year + 1
        next_month -= 12
    while next_month < 1:
        year = year - 1
        next_month += 12
    if day <= 28:
        return date(year, next_month, day)
    else:
        if next_month == 12:
            nm = 1
            yr = year + 1
        else:
            nm = next_month + 1
            yr = year
        new_dt = date(yr, nm, 1) - DAY
        if new_dt.day <= day:
            return datetime.combine(new_dt, dt.time())
        else:
            return datetime.combine(date(year, next_month, day), dt.time())


def next_date(interval, current):
    # sys.stderr.write('        (next-date %r %r)\n' % (interval, current))
    if isinstance(current, date):
        next = current = datetime.combine(current, time())
    else:
        next = current.replace(hour=0, minute=0, second=0)
    if interval == WEEKLY:
        dow = next.isoweekday() % 7
        if dow != 0:
            next += timedelta(7-dow)
        else:
            next += WEEK
    elif interval == BIWEEKLY:
        day = current.day
        if day < 16:
            day_to_add = 16 - day
            next += timedelta(day_to_add)
        else:
            next = add_month(current.replace(day=1))
    elif interval == BIWEEKLY15:
        day = current.day
        if day < 15:
            day_to_add = 15 - day
            next += timedelta(day_to_add)
        else:
            next = add_month(current.replace(day=1))
    elif interval == MONTHLY:
        return add_month(current.replace(day=1))
    elif interval == QUARTERLY:
        while True:
            next = next_date(MONTHLY, next)
            month = next.month
            if month in (1, 3, 6, 9):
                return next
    return next


def ensure_datetime(value, tm=time()):
    if isinstance(value, date):
        return datetime.combine(value, tm)
    else:
        return value


import sys
def calc_date(batch, dt):
    if batch.process_date is None:
        start = batch.created
    else:
        start = start_cycle(batch.period, batch.next_process_date)
    start = ensure_datetime(start)
    end = batch.next_process_date
    # sys.stderr.write('calc-date(created=%r, period=%r, dt=%r, start=%r, end=%r)' % (batch.created, batch.period, dt, start, end))
    dt = ensure_datetime(dt)
    next = None
    while True:
        try:
            next = next_cycle(batch.period, end)
            next = ensure_datetime(next)
            # sys.stderr.write('    TEST %s > %s\n' % (next, dt))
            if next > dt:
                break
            end = next
        except:
            logging.error('break on (calc-date <%r> "%s") => "%s"', batch, dt, next)
            raise
    # sys.stderr.write(' => (start=%r, end=%r)\n' % (start, end-BLINK))
    return (start, end-BLINK)


def start_cycle(period, current):
    if period == 7:
        return current - WEEK
    elif period == 14:
        return current - FORTNIGHT
    elif period == 15:
        return previous_date(BIWEEKLY, current)
    elif period == 31:
        return previous_date(MONTHLY, current)
    else:
        raise Exception, 'invoice period not supported: days=%s' % (period,)


def next_cycle(period, current):
    # sys.stderr.write('        (next-cycle %r %r)\n' % (period, current))
    if period == 7:
        return next_date(WEEKLY, current-DAY) + DAY
    elif period == 14:
        return next_date(WEEKLY, next_date(WEEKLY, current-DAY)) + DAY
    elif period == 15:
        return next_date(BIWEEKLY, current)
    elif period == 31:
        return next_date(MONTHLY, current)
    else:
        raise Exception, 'invoice period not supported: days=%s' % (period,)


def iter_cycle(start, end, period):
    start = start.date()
    end = end.date()
    while start < end:
        start = start_cycle(period, start)
        next = next_cycle(period, start)
        yield (start, next-DAY)
        start = next + DAY


def iter_days(start, end):
    start = start.date()
    end = end.date()
    while start < end:
        yield (start, start+DAY-BLINK)
        start += DAY

