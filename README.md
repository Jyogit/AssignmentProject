# AssignmentProject
This is a project/program to calculate the average speed of the International Space Station after extracting timestamp, latitude and longitude from a given json url at multiple intervals.

The main program file: extract_json.py

Usage: 
    $ python extract_json.py [TIME_DURATION] [POLLING_INTERVAL]
        - TIME_DURATION (int) maximum time in seconds for program execution.
        - POLLING_INTERVAL (int) time duration between two polls to read the response from url.

Examples:
    $ python extract_json.py
    $ python extract_json.py 60 5
    $ python extract_json.py 300 10
    $ python extract_json.py 120

The extracted data along with calculated distance and speed is printed on the standard output as well as saved in a csv file.
The average speed is printed on the standard output as per the requirement.
