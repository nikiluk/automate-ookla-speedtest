import subprocess
import os
import json
import pandas as pd
import csv

def speedtest_json_result_to_json(outputfile, json_result):
    #todo
    print("speedtest_json_result_to_json")

def speedtest_json_result_to_csv(outputfile, json_result):
    headers = pd.read_csv("./src/templates/headers.extended.csv.tpl")
    df = headers.append(pd.json_normalize(json_result), ignore_index=True)   

    if os.path.isfile(outputfile):
        df.to_csv(outputfile, header=None, mode='a')

    else:
        df.to_csv(outputfile)
        print ("New file '{outputfile}' for test results was created.".format(outputfile=outputfile))


def speedtest_json():

    try:
        speedtest_result = subprocess.run(".\speedtest --format=json-pretty --unit=Mbps", shell=True, capture_output=True, text=True)
        json_result = json.loads(speedtest_result.stdout)

        if (json_result['type'] == "result"):
            print("Download: {download_speed} Mbps".format(download_speed=json_result['download']['bandwidth']*8/1000000))
            print("Upload: {upload_speed} Mbps".format(upload_speed=json_result['upload']['bandwidth']*8/1000000))

            return json_result
        else:
            return False
    except:
        return False

def speedtest_run_tests(numberoftests, outputfile):
    if os.path.isfile(outputfile):
        f = open(outputfile,"r+")
        reader_file = csv.reader(f)
        recorded = len(list(reader_file))-1 #not counting headers

    else:
        recorded = 0
    
    print("Running {numberoftests} tests and appending results to '{outputfile}'".format(numberoftests=numberoftests, outputfile=outputfile))
    if (recorded>0):
        print("It already contains {recorded} results.".format(recorded=recorded))

    #initialize
    failed = 0

    for i in range(numberoftests):
        print("---")
        print("Running speed test #{i}".format(i=i+1+recorded))

        json_result= speedtest_json()

        if (json_result):       
            print("Test #{i} completed".format(i=i+1+recorded))
            speedtest_json_result_to_csv(outputfile, json_result)
            print("")
        else:
            failed+=1
            print("Test #{i} failed.".format(i=i+1+recorded))

    print("Tests completed: {i} (failed: {failed})".format(i=i+1, failed=failed))
    print("")