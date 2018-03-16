import os.path
import pickle
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
existing_data_filepath = os.path.join(current_dir, 'bikeshare_api_data.pickle')  # oh god pls dont mess with this file

stations = []
if os.path.isfile(existing_data_filepath):
    with open(existing_data_filepath, 'rb') as f:
        stations = pickle.load(f)

# manually adjusted for UTC to EST/EDT
beginning_of_day = datetime(2017, 12, 5, 19, 0, 0)
end_of_day = datetime(2017, 12, 6, 19, 1, 0)  # and 1 minute so we end at midnight too

filter_start = None
filter_end = None
ctr = 0
for station in stations:
    unix_timestamp = station['timestamp']
    unix_timestamp -= 60 * 60 * 5  # UTC to EST/EDT -5h
    datetime_timestamp = datetime.fromtimestamp(unix_timestamp)
    if datetime_timestamp >= beginning_of_day:
        print(datetime_timestamp.strftime('%m-%d %H:%M'))
        if datetime_timestamp <= end_of_day:
            if filter_start is None:
                filter_start = ctr
        else:
            filter_end = ctr
            break
    ctr += 1

filtered_data = stations[filter_start:filter_end]

filtered_data_filepath = os.path.join(current_dir, 'filtered_data_with_capacity.pickle')
with open(filtered_data_filepath, 'wb') as f:
    pickle.dump(filtered_data, f, pickle.HIGHEST_PROTOCOL)
