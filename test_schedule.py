import datetime

from stagtime import Timekeeper, URPING

def test_schedule():
    first_few_pings = [
        1184098754,
        1184102685,
        1184104776,
        1184105302,
        1184105815,
    ]
    tk = Timekeeper()
    tk.init(URPING)
    for expected in first_few_pings:
        assert tk.nextping() == expected
