import subprocess
import os
import json
import pandas as pd
import csv
        

def read_json_results_file(filepath):
    """
    Reads JSON and returns it as dict if file exists
    """
    with open(filepath,'r') as json_file:
        try:
            jsonfilecontent = json.load(json_file)
            return jsonfilecontent
        except ValueError:
            return False

    

def initialize_json_results_file(filepath):
    """
    Creates a JSON file according to a template
    """
    if os.path.isfile(filepath):
        print("Failed to initialize {filepath}. File is already present.".format(filepath=filepath))
        return False
    else:
        template = {"tests": []}
        
        out_file = open(filepath, "w") 
        json.dump(template, out_file, indent=4) 
        print ("Created '{filepath}'.".format(filepath=filepath))
    
    return True

def append_test_result_to_json_file(filepath, json_result):
    """
    Append test results to JSON file, creates the JSON file if it does not exist using initialize_json_results_file(filepath)
    """
    if not os.path.isfile(filepath):
        initialize_json_results_file(filepath)

    jsonfilecontent = read_json_results_file(filepath)

    if not jsonfilecontent:
        print("Failed to read {filepath}. File is corrupt.".format(filepath=filepath))
        return False
    
    json_file = open(filepath, "w") 
    jsonfilecontent['tests'].append(json_result)
    json.dump(jsonfilecontent, json_file, indent=4) 

    return True

def append_test_result_to_csv_file(outputfile, json_result):
    """
    Append test results to CSV file, creates the CSV file if it does not exist using predefined headers
    """
    headers = pd.read_csv("./src/templates/headers.extended.csv.tpl")
    df = headers.append(pd.json_normalize(json_result), ignore_index=True)   

    if os.path.isfile(outputfile):
        df.to_csv(outputfile, header=None, mode='a')

    else:
        df.to_csv(outputfile)
        print ("New file '{outputfile}' for test results was created.".format(outputfile=outputfile))

    return True


def speedtest_output_json():
    """
    Outputs test results in JSON dict format
    """
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

def speedtest_run_tests(numberoftests, outputfile, writeJSON = False):
    """
    Runs a given number of tests, writeJSON is optional parameter
    """
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

        json_result= speedtest_output_json()

        if (json_result):       
            print("Test #{i} completed".format(i=i+1+recorded))
            append_test_result_to_csv_file(outputfile, json_result)
            if writeJSON:
                append_test_result_to_json_file(outputfile.replace('csv', 'json'), json_result)
            print("")
        else:
            failed+=1
            print("Test #{i} failed.".format(i=i+1+recorded))

    print("Tests completed: {i} (failed: {failed})".format(i=i+1, failed=failed))
    print("")