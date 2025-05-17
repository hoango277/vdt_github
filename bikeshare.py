import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['Chicago', 'New York', 'Washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

    print("Hello! Let's explore some US bikeshare data!")

    def get_valid_input(prompt, valid_options):
        while True:
            try:
                user_input = input(prompt).title()
                if user_input in valid_options:
                    return user_input
                else:
                    print(f"Invalid input. Please choose from {valid_options}.")
            except KeyboardInterrupt:
                print("\nNo input taken. Exiting program.")
                exit()

    city = get_valid_input(
        "\nWould you like to see data for Chicago, New York, or Washington?\n",
        cities
    )
    print(f"\nLooks like you want to hear about {city}!")

    month = get_valid_input(
        "\nWhich month would you like to filter by? January, February, March, April, May, June, or All?\n",
        months
    )

    day = get_valid_input(
        "\nWhich day would you like to filter by? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?\n",
        days
    )

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): name of the city to analyze
        month (str): name of the month to filter by, or "all" to apply no month filter
        day (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df (pd.DataFrame): DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.title()])

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month.lower() != 'all':
        month_num = months.index(month.title()) + 1  # months list phải có trong scope
        df = df[df['month'] == month_num]

    # Filter by day of week if applicable
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print('The most common month: {}\n'.format(common_month))

    # display the most common day of week
    common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('The most common day of week: {}\n'.format(common_day_of_week))

    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('The most common start hour: {}\n'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station: {}\n'.format(common_start_station))

    # display most commonly used end station
    common_end_station  = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station: {}\n'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    print('The most frequent start station and end station trip: Start Station - {}; End Station - {}\n'.format(common_start_station, common_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {}\n'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {}\n'.format(round(mean_travel_time, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n{}'.format(user_types))

    # Display counts of gender
    if {'Gender', 'Birth Year'}.issubset(df.columns):
        gender = df['Gender'].value_counts()
        print('\nCounts of gender:\n{}'.format(gender))

    # Display earliest, most recent, and most common year of birth

        birth_year_earliest = df['Birth Year'].min()
        birth_year_recent = df['Birth Year'].max()
        birth_year_common = df['Birth Year'].value_counts().idxmax()

        print('\nThe earliest year of birth: {}\n'.format(int(birth_year_earliest)))
        print('The most recent year of birth: {}\n'.format(int(birth_year_recent)))
        print('The most common year of birth: {}\n'.format(int(birth_year_common)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw_data(df):
    """
    Display raw data if you want to see.
    """
    row = 0
    while True:
        raw_data = input("\nWould you like to view individual trip data? Type 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            print(df.iloc[row:row+5])
            row += 5
        elif raw_data.lower() == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df2 = pd.read_csv(CITY_DATA[city.title()])

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df2)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
