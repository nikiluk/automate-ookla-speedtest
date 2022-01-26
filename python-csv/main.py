
# By Jamie Pond -- Github: jamierpond

import subprocess
import datetime
import time
from csv import writer


def append_to_csv(csv_to_append_to, list_to_append):
    with open(csv_to_append_to, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_to_append)
        f_object.close()


def get_time_str(num_seconds_elapsed):
    return time.strftime("%Hh%Mm%Ss", time.gmtime(num_seconds_elapsed))


# Edit the values you want before you run the script here.
# I've had success with even appending to files on my remote
# Google Drive (so many computers can feed into the same database!)
output_csv         = r"Y:\speedtest_output.csv"
interval_seconds   = 2
hours_to_run_for   = 0.5  # half an hour
seconds_to_run_for = hours_to_run_for * 60 * 60
print("Running for", get_time_str(seconds_to_run_for))


if __name__ == '__main__':
    num_tests = 0
    start_time = int(time.time())
    end_time   = start_time + seconds_to_run_for

    while int(time.time()) < end_time:
        date_and_time = datetime.datetime.utcnow()
        print("Start speed test...")
        output = subprocess.check_output("speedtest --format=csv")
        output_with_time_prepended = str(date_and_time) + "," + str(output.decode("utf-8")).replace('"', "")
        output_list = output_with_time_prepended.split(",")
        # TODO THERE SOMETHING INCORRECT ABOUT HOW THE DOWNLOAD SPEED IS INTERPRETED HERE...
        print("Finished speed test with download speed:", str(float(output_list[6]) / 1000000.0), "Mbps")
        append_to_csv(output_csv, output_list)
        num_tests += 1
        print("Number of tests completed:", num_tests, "in", get_time_str(time.time() - start_time))
        time.sleep(interval_seconds)

    print("Finished testing!")
