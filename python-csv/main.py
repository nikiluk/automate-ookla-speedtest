
import os
import subprocess
import datetime
import time
from csv import writer

# Edit the values you want before you run the script here.
# I've had success with even appending to files on my remote
# Google Drive (so many computers can feed into the same database!)
output_csv         = "Y:\speedtest_output.csv"
interval_seconds   = 2
hours_to_run_for   = 24
seconds_to_run_for = 120  # hours_to_run_for * 60 * 60


def append_to_csv(csv_to_append, list):
    with open(csv_to_append, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()


if __name__ == '__main__':

    start_time = int(time.time())
    end_time   = start_time + seconds_to_run_for

    while int(time.time()) < end_time:
        date_and_time = datetime.datetime.utcnow()
        print("Start speed test...")
        output = subprocess.check_output("speedtest --format=csv")
        print("Finished speed test!")
        output_with_time_prepended = str(date_and_time) + ", " + str(output.decode("utf-8")).replace('"', "")
        output_list = output_with_time_prepended.split(",")
        append_to_csv(output_csv, output_list)
        time.sleep(interval_seconds)

    print("Finished testing!")






