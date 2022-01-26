
import os
import subprocess
import csv
import datetime

from csv import writer

os.chdir(os.getcwd())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    now = datetime.datetime.utcnow()

    print("Start speed test...")
    output = subprocess.check_output("speedtest --format=csv")
    print("Finished speed test!")

    output_with_time_prepended = str(now) + ", " + str(output.decode("utf-8")).replace('"', "")
    print(output_with_time_prepended)

    output_list = output_with_time_prepended.split(",")

    with open('CSVFILE.csv', 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(output_list)
        # Close the file object
        f_object.close()




