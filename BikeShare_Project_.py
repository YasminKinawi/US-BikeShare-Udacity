import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Input a small welcome message to user.
message='\nHello! Welcome to BikeShare data exploration\nfor cities Chicago, New York City, and Washington.\n'
print(message)

def get_filters():
    #Asks user to specify a city, month, and day to analyze.
    #Returns:
        #(str) city - name of the city to analyze
        #(str) month - name of the month to filter by, or "all" to apply no month filter
        #(str) day - name of the day of week to filter by, or "all" to apply no day filter

    #Asks user to enter their chosen city.
    while True:
        city=input('\nType the city you would like to explore: ').lower()
        if city not in CITY_DATA.keys():
            print('\nInvalid city name! The data is for Chicago, New York City, and Washington.')
            continue
        else:
            break
    #Asks user if they want to filter their chosen city's data by month and day.
    while True:
        q=input('\nWould you like to filter the data? Enter "yes" or "no": ').lower()
        a=['yes', 'no']
        if q in a:
            if q=='yes':
                while True:
                    month=input('\nEnter which month you want from January till June or "all": ').lower()
                    month_list=['january', 'february', 'march', 'april', 'may', 'june','all']
                    if month not in month_list:
                        print('\nInvalid Input! The data is for the first six months.')
                        continue
                    else:
                        break
                while True:
                    day=input('\nEnter which day of the week (example: Monday) or "all": ').lower()
                    week=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
                    if day not in week:
                        print('\nInvalid Input! Please type which day of the week.')
                        continue
                    else:
                        break
                message1='\nLet\'s have a look on {}\'s BikeShare data filtered by month(s) {} and weekday(s) {}.\n'
                print(message1.format(city.title(), month.title(), day.title()))
            else:
                if q=='no':
                    month='all'
                    day='all'
                    message2='\nLet\'s have a look on {}\'s BikeShare data for the first six months of 2017.\n'
                    print(message2.format(city.title()))
                    break
        else:
            print('\nIs that a "yes" or "no"!')
            continue
        break
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    #Loads data for the specified city and filters by month and day if applicable.
    #Args:
        #(str) city - name of the city to analyze
        #(str) month - name of the month to filter by, or "all" to apply no month filter
        #(str) day - name of the day of week to filter by, or "all" to apply no day filter
    #Returns:
        #df - Pandas DataFrame containing city data filtered by month and day

    # load data file into a dataframe
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day):
    #Displays statistics on the most frequent times of travel.
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month_name()

    if month == 'all':
        # display the most common month
        common_month=df['month'].mode()[0]
        print('\n{} is the most popular month.'.format(common_month))

    if day == 'all':
        # display the most common day of week
        common_day=df['day_of_week'].mode()[0]
        print('\n{} is the most common day of the week.'.format(common_day))
    # display the most common start hour
    common_hour=df['hour'].mode()[0]
    print('\n{} is the most ferquent hour.'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    #Displays statistics on the most popular stations and trip.
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    pop_start_station=df['Start Station'].mode()[0]
    # display most commonly used end station
    pop_end_station=df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    combine_station= df['Start Station'] + ' to ' + df['End Station']
    pop_combine=combine_station.mode()[0]
    print('{} is the most popular start station.\n{} is the most popular end station.\
        \nThe most frequent stations combined is from {}'.format(pop_start_station,pop_end_station,pop_combine))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_time=df['Trip Duration'].sum()
    # display mean travel time
    average_time=df['Trip Duration'].mean()

    print('\nTotal trip duration in seconds is: ', total_time)
    print('\nAverage trip duration in seconds is: ', average_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    #Displays statistics on bikeshare users.
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_count=df['User Type'].value_counts()
    print('\nStats. about user types:\n ',user_count)
    # Display counts of gender
    if city !='washington':
        gender_count=df['Gender'].value_counts()
        print('\nStats. about gender:\n ',gender_count)
    # Display earliest, most recent, and most common year of birth
        earliest_yob=df['Birth Year'].min()
        recent_yob=df['Birth Year'].max()
        common_yob=df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}.\nMost recent birth year: {}.\
            \nMost common birth year: {}.'.format(earliest_yob, recent_yob, common_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    #Display a sample of raw data (for example 10 rows)
    while True:
        q_raw=input('\nWould you like a sample of the raw data? Enter "yes" or "no": ').lower()
        a=['yes', 'no']
        if q_raw in a:
            if q_raw=='yes':
                i=0
                print(df.iloc[i:i+11])
        else:
            print('\nIs that a "yes" or "no"!')
            continue
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart=input('\nWould you like to restart? Enter "yes" or "no": \n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__' :
    main()
