# import packages
import sqlite3
import json
import csv
from readjson import jsonreading
from db import database


# class database
class report:

    # this function will return a list of temperature and status
    @staticmethod
    def return_rows(file_name):

        sensehat_data_results, _, _ = database.getEnvironmentData()
        
        # initialize three lists
        date = []
        temp = []
        status = []
        
        for i in range(len(sensehat_data_results)):
            boolean = True
            for j in range(i + 1, len(sensehat_data_results)):
                if boolean == False:
                    break
                elif boolean == True:
                    curr_date_list = []
                    curr_temp_list = []
                    curr_hum_list = []
                    if sensehat_data_results[i][0].split()[0] == sensehat_data_results[j][0].split()[0]:
                        # extract the date to a variable names row_date
                        row_date = sensehat_data_results[i][0].split()[0]
                        # extract the temperature to a variable names row_temp
                        row_temp = sensehat_data_results[i][1]
                        # extract the humidity to a variable names row_hum
                        row_hum = sensehat_data_results[i][2]
                        # append the date of each row to the date list that we initalized at the top
                        curr_date_list.append(row_date)
                        # append the temperature of each row to the curr_temp_list list that we initalized at the top
                        curr_temp_list.append(row_temp)
                        # append the humidity of each row to the curr_hum_list list that we initalized at the top
                        curr_hum_list.append(row_hum)
                    
                    print('ELSE')
                    min_row_temp = min(curr_temp_list)
                    max_row_temp = max(curr_temp_list)
                    min_row_hum = min(curr_hum_list)
                    max_row_hum = max(curr_hum_list)

                    row_status = report.check_status(file_name, min_row_temp, max_row_temp,  min_row_hum, max_row_hum)
                    # append the date of each row to the date list that we initalized at the top
                    date.append(row_date)
                    # append the temperature of each row to the temp list that we initalized at the top
                    temp.append(row_temp)
                    # append the status of each row to the status list that we initalized at the top
                    status.append(row_status)
                    boolean = False

        return date, status  
    
    
    @staticmethod
    def check_status(file_name, min_temp, max_temp, min_hum, max_hum):
        """
        This function will check the status of one day
        based on the temperature and the humidity
        This function accepts four parameters:
        file_name: json filename since we're calling read_json function here
        temp: the temperature of one day
        hum: the humidity of one day
        This function will return the status of one day
        """
        # read a function and split the return values into four variables
        min_temperature, max_temperature, min_humidity, max_humidity =jsonreading.read_json(file_name)
        

        # check if the temperature and the humidity are within the specified range in the json file
        if ((min_temp > min_temperature) and (max_temp < max_temperature)) and ((min_hum > min_humidity) and (max_hum < max_humidity)):
            # if both temperature and humidity are within the specified range, then set status to 'OK'
            status = 'OK'
        # if temperature is less than the specified minimum temperature, then write a message to the status
        elif(min_temp < min_temperature):
            # define a variables and calculate the difference between the minumim temperature and the stored temperature
            temp_difference = min_temperature - min_temp
            # write a message to status 
            status = 'BAD: ' + str(temp_difference) + ' *C below minimum temperature'
        # if temperature is more than the specified maximum temperature, then write a message to the status
        elif(max_temp > max_temperature):
            # define a variables and calculate the difference between the maximum temperature and the stored temperature
            temp_difference = max_temp - min_temperature
            # write a message to status 
            status = 'BAD: ' + str(temp_difference) + ' *C above maximum temperature'
        # if humidity is less than the specified minimum humidity, then write a message to the status
        elif(min_hum < min_humidity):
            # define a variables and calculate the difference between the maximum humidity and the stored humidity
            hum_difference = min_humidity - min_hum
            # write a message to status
            status = 'BAD: ' + str(hum_difference) + ' below minimum humidity'
        # if humidity is more than the specified maximum humidity, then write a message to the status
        elif(max_hum > max_humidity):
            # define a variables and calculate the difference between the maximum humidity and the stored humidity
            hum_difference = max_hum - max_humidity
            # write a message to status
            status = 'BAD: ' + str(hum_difference) + ' above maximum humidity'
    
        # return the status
        return status

    @staticmethod
    def log_to_csv(file_name):

        date, status = report.return_rows(file_name)
        # open a csv file if it exists, otherwise create a new one
        with open('report.csv', mode='w') as csv_file:
            # specified the delimiter between columns and quotechar for each column
            csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # write the header of the csv file
            csv_file.writerow(["Date", "Status"])
            # iterate though the lists 'date' and 'status'
            for d, s in zip(date, status):
                # write each row of the list to the csv file
                csv_file.writerow([d, s])
    
    
    
    
    
    
    
    
    
    