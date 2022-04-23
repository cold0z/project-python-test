from datetime import datetime


def duration_time(code_date):
    
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    time_code = datetime.strptime(code_date, fmt)
    now = datetime.now()
    diff = now-time_code
    return diff.seconds/60