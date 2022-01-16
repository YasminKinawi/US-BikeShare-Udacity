import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

message='\nHello! Welcome to BikeShare data exploration\nfor cities Chicago, New York City, and Washington.\n'
print(message)

def get_filters():
    while True:
        city=input('\nType the city you would like to explore: ').lower()
        if city not in CITY_DATA.keys():
            print('\nInvalid city name! The data is for Chicago, New York City, and Washington.')
            continue
        else:
            break

    while True:
        q=input('\nWould you like to filter the data? Type "yes" or "no": ').lower()
        a=['yes', 'no']
        if q in a:
            if q=='yes':
                while True:
                    month=input('\nType which month you want from January till June or "all": ').lower()
                    month_list=['january', 'february', 'march', 'april', 'may', 'june','all']
                    if month not in month_list:
                        print('Invalid Input! The data is for the first six months.')
                        continue
                    else:
                        break
                while True:
                    day=input('\nType which day of the week (example: Monday) or "all": ').lower()
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
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.month_name()

    common_month=df['month'].mode()[0]
    print('\n{} is the most popular month.'.format(common_month))

    common_day=df['day_of_week'].mode()[0]
    print('\n{} is the most common day of the week.'.format(common_day))

    common_day=df['day_of_week'].mode()[0]
    print('\n{} is the most common day of the week.'.format(common_day))

    common_hour=df['hour'].mode()[0]
    print('\n{} is the most ferquent hour.'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    pop_start_station=df['Start Station'].mode()[0]

    pop_end_station=df['End Station'].mode()[0]

    combine_station= df['Start Station'] + ' to ' + df['End Station']
    pop_combine=combine_station.mode()[0]
    print('{} is the most popular start station.\n{} is the most popular end station.\
        \nThe most frequent stations combined is from {}'.format(pop_start_station,pop_end_station,pop_combine))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time=df['Trip Duration'].sum()

    average_time=df['Trip Duration'].mean()

    print('\nTotal trip duration in seconds is: ', total_time)
    print('\nAverage trip duration in seconds is: ', average_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_count=df['User Type'].value_counts()
    print('\nStats. about user types:\n {}'.format(user_count))

    if 'Gender' in (df.columns):
        gender_count=df['Gender'].value_counts()
        print('\nStats. about gender:\n {}'.format(gender_count))
    if 'Birth Year' in (df.columns):
        earliest_yob=df['Birth Year'].min()
        recent_yob=df['Birth Year'].max()
        common_yob=df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}.\nMost recent birth year: {}.\
            \nMost common birth year: {}.'.format(earliest_yob, recent_yob, common_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
