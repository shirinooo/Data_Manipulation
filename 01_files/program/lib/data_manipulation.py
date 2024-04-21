import os

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    return os.path.exists(filename)


# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()

import csv

def get_file_contents(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.readlines()
    else:
        return "This file cannot be found!"



# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row):

    result = []
    file_contents = get_file_contents(filename)

    target_records = [row for row in file_contents if "25/12/2004" in row]

    if include_header_row:
        result.append(file_contents[0])

    result.extend(target_records)

    return result        

        
        


# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;

def christmas_day_average_air_quality(filename):
    
    xmas_air_quality = christmas_day_air_quality(filename, True)

    pt08_s1_values = [float(row.split(';')[3].replace(',', '.')) for row in xmas_air_quality[1:]]

    average_pt08_s1 = round(sum(pt08_s1_values) / len(pt08_s1_values), 2)

    return average_pt08_s1


# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together

from collections import defaultdict

def get_averages_for_month(filename):

    file_contents = get_file_contents(filename)

    monthly_averages = defaultdict(list)
    
    for row in file_contents[1:]:
        date_parts = row.split(';')[0].split('/')
        if len(date_parts) == 3:
            month = int(date_parts[1])
        
        pt08_s1 = row.split(';')[3].replace(',', '.')
        if pt08_s1:
            pt08_s1_value = float(pt08_s1)

        monthly_averages[month].append(pt08_s1_value)

    return {month: round(sum(values) / len(values), 2) for month, values in monthly_averages.items()}

    
    
# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"
def create_march_data(filename):
    output_filename = filename.replace('AirQuality.csv', 'AirQualityMarch.csv')
    
    if os.path.exists(filename):
        with open(filename,'r') as input_file, open(output_filename, 'w', newline='') as output_file:
            original_file = csv.reader(input_file)
            march_file = csv.writer(output_file)

            header_row = next(original_file)
            march_file.writerow(header_row)
            #print("Header written to output file")

            for row in original_file:
                date_parts = row[0].split('/')
                if len(date_parts) == 3 and date_parts[1] == '03':
                    march_file.writerow(row)
                    #print("Row written to output file:", row)
    
    print("Output file exists:", os.path.exists(output_filename))

# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):
    output_dir = os.path.join(os.path.dirname(filename), "monthly_responses")
    os.makedirs(output_dir, exist_ok=True)

    original_file_content = get_file_contents(filename)
    header_row = original_file_content[0]

    #organise data by month and year
    monthly_data = defaultdict(list)
    for row in original_file_content[1:]:
        if row != "" and not ';;;' in row:
            date_parts = row.split(';')[0].split('/')
            #print(date_parts)
            #print(row)
            month_year = f"{date_parts[1]}-{date_parts[2]}"

            monthly_data[month_year].append(row)
    print(monthly_data['01-2005'])
            
    
    # write data to monthly files
    for month_year, data in monthly_data.items():
        output_filename = os.path.join(output_dir, f"{month_year}.csv")
        #print("Writing data to:", output_filename)
        with open(output_filename, 'w', newline='') as output_file:
            output_file.write(header_row)
            for row in data:
                output_file.write(row)

        #print("Output file exists:", os.path.exists(output_filename))
