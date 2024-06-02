from datetime import datetime, timedelta

def t(x):
    base_date = '2000-01-01'
    labels = [
        (datetime.strptime(base_date, '%Y-%m-%d') + timedelta(days=x)).strftime('%Y-%m-%d')
        for x in range(x + 1)
        ]
    labels.reverse()
    return labels

print(t(7))