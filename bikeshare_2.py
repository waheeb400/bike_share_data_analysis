import time
import pandas as pd
import numpy as np

City_Data = { 'chicago': 'data/chicago.csv', 'Chicago': 'data/chicago.csv',
             'New York City': 'data/new_york_City.csv', 'New york City': 'data/new_york_City.csv',
              'new york City': 'data/new_york_City.csv', 'washington': 'data/washington.csv',
             'Washington': 'data/washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    City = ''
    #Running this loop to ensure the correct user input gets selected else repeat
    while City not in City_Data.keys():
        print("\nWelcome to this program. Please choose your City:")
        City = input().lower()

        if City not in City_Data.keys():
            print("\nPlease check your input is not correct.")
      

    Month_Data = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in Month_Data.keys():
        print("\nPlease enter the month")
        month = input().lower()

        if month not in Month_Data.keys():
            print("\nInvalid input is in correct.")
 
   
    #Creating a list to store all the days including the 'all' option
    Day_List = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in Day_List:
        print("\nPlease enter a day in the week :")
        day = input().lower()

        if day not in Day_List:
            print("\nInvalid input is Not correct.")
    print('-'*80)
    #Returning the City, month and day selections
    return City, month, day

#Function to load data from .csv files
def load_data(City, month, day):
    #Load data for City
    Data_Frame = pd.read_csv(City_Data[City])

    #Convert the Start Time column to datetime
    Data_Frame['Start Time'] = pd.to_datetime(Data_Frame['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    Data_Frame['month'] = Data_Frame['Start Time'].dt.month
    Data_Frame['day_of_week'] = Data_Frame['Start Time'].dt.day

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        Data_Frame = Data_Frame[Data_Frame['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        Data_Frame = Data_Frame[Data_Frame['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (Data_Frame) with relevant columns
    return Data_Frame

#Function to calculate all the time-related statistics for the chosen data
def time_stats(Data_Frame):
  
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses mode method to find the most popular month
    Commen_Month = Data_Frame['month'].mode()[0]

    print(f"Most Popular Month (1 = January,...,6 = June): {Commen_Month}")

    #Uses mode method to find the most popular day
    Commen_Day = Data_Frame['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {Commen_Day}")

    #Extract hour from the Start Time column to create an hour column
    Data_Frame['hour'] = Data_Frame['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    Commen_Hour = Data_Frame['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {Commen_Hour}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate station related statistics
def station_stats(Data_Frame):
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    Most_Start_Station = Data_Frame['Start Station'].mode()[0]

    print(f"The most commonly used start station: {Most_Start_Station}")

    #Uses mode method to find the most common end station
    Most_End_Station = Data_Frame['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {Most_End_Station}")

    Data_Frame['Start To End'] = Data_Frame['Start Station'].str.cat(Data_Frame['End Station'], sep=' to ')
    combo = Data_Frame['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function for trip duration related statistics
def trip_duration_stats(Data_Frame):
    start_time = time.time()

    #Uses sum method to calculate the total trip duration
    TD = Data_Frame['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(TD, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #Calculating the average trip duration using mean method
    AD = round(Data_Frame['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(AD, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def user_stats(Data_Frame):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = Data_Frame['User Type'].value_counts()

    print(f"The types of users :\n\n{user_type}")

    try:
        gender = Data_Frame['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    try:
        earliest = int(Data_Frame['Birth Year'].min())
        recent = int(Data_Frame['Birth Year'].max())
        common_year = int(Data_Frame['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to display the data frame itself as per user request
def display_data(Data_Frame):
    Response_List = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    while rdata not in Response_List:
        print("\nDo you wish to view the raw data?")
        rD = input().lower()
        if rD == "yes":
            print(Data_Frame.head())
        elif rD not in Response_List:
            print("\nPlease check your input.")
            print("Input does correct .")
    
    #Extra while loop here to ask user if they want to continue viewing data
    
    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        City, month, day = get_filters()
        Data_Frame = load_data(City, month, day)

        display_data(Data_Frame)
        time_stats(Data_Frame)
        station_stats(Data_Frame)
        trip_duration_stats(Data_Frame)
        user_stats(Data_Frame)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()