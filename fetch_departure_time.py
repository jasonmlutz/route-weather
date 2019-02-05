""" Methods for fetching departure date/time from user.
"""
import time

def get_departure_time():
    """ Get user's departure time; either now or in the future.

    Parameters:
    none

    Returns:
    dept_time (str): A .isoformat() style string [YYYY]-[MM]-[DD]T[HH]:[MM]
    """
    print('\n 1. Leave now. \n 2. Specify future departure time.')
    while True:
        try:
            depart_now = int(input())
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if depart_now in range(1, 3):
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    if depart_now == 1:
        print('Thanks! Weather data will be based on an immediate departure.')
        departure_datetime = int(time.time())
    if depart_now == 2:
        print('Thanks! Let\'s get your departure date and time.')
        departure_year = input('Please enter your departure year YYYY: ')
        departure_month = input('Please enter your departure month MM: ')
        departure_day = input('Please enter your departure day DD: ')
        departure_hour = input('Please enter your departure hour HH, [0,23]: ')
        departure_minute = input('Please enter your departure day MM: ')
        departure_date = departure_year+'-'+departure_month+'-'+departure_day
        departure_time = departure_hour+':'+departure_minute
        departure_datetime = departure_date+'T'+departure_time+':00'
    return departure_datetime
