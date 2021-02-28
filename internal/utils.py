from datetime import datetime,date

def months_in_reverse():
    cur_month=datetime.today().month
    cur_year=datetime.today().year
    months_forward=[(cur_month+i) for i in range(1,13)]
    months_backward=list()
    for i in months_forward[::-1]:
        m=i if i<=12 else i-12
        months_backward.append(m)
    return months_backward

