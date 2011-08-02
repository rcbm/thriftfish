from datetime import *
class formatDatetime():
    # Convert a String from CL to datetime
    def craigslist_to_datetime(self, old_datetime):
        split_date = old_datetime.split('T')
        split_time = split_date[1].split('-')[0]
        format_time =  ''.join(split_date[0] + ' '+  split_time)
        new_datetime = datetime.strptime(format_time, '%Y-%m-%d %H:%M:%S')
        return new_datetime

    # Convert a String (thats already formatted) to datetime object
    def string_to_datetime(self, old_datetime):
        new_datetime = datetime.strptime(old_datetime, '%Y-%m-%d %H:%M:%S')
        return new_datetime

