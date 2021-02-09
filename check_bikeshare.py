import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def month_filter():
    """ Filters the DataFrame by month. """
    to_stay = True  #  Used for conditional in while loop.
    print("\nLet's get the month to look at.")
    while to_stay:
        print("All, January, February, March, April, May, June")
        month = input("\nWhich month will we use? ")
        month = month.lower()
        month.strip()
        if month not in months:
            print("\n\tThat really does not compute. Let's do that again.")
            continue
        else:
            print("\n\tThat is an excellent month. We'll use " + month.title() + ".")
            to_stay = False
    return month

def day_filter():
    """ Filers by day of week by user's request. """
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("\n\nWhich day (or all) to use for statistical purposes.")
    to_stay = True
    while to_stay:
        print("\nAll, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday")
        day = input("\nPlease enter the day: ")
        day = day.lower()
        day.strip()
        if day not in days:
            print("\tI just could not find that anywhere in my files. Can we do this again?\n")
            continue
        else:
            print("\n\tWe will use " + day.title() + " as a search filter.\n")
            to_stay = False
    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("\nWe have three cities for data exploration: Chicago, New York City, and Washington. ")

    to_stay = True  # For use with iterating in while loop
    while to_stay:
        print("Chicago, New York City, or Washington\n")
        city = input("Let's start with the city: ")
        city = city.lower()
        city.strip()
        # Is user input a valid response?
        if city not in cities:
            print("Not quite getting that one.  Let's try again.\n")
            continue
        else:
            print("\n\tGood! " + city.title() + " is a good city to use.")
            to_stay = False
    # TO DO: get user input for month (all, january, february, ... , june)
    # REFACTORED if / elif / else for functionality 
    data_answers = ['m', 'd', 'n']  # 'm' for month, 'd' for day, 'n' for no filter
    to_loop_again = True
    while to_loop_again:
        data_filter = input("\n\nWould you like to filter by [m]onth, by [d]ay, or [n]one at all? ")
        data_filter.lower().strip()
        if data_filter == 'm':
            month = month_filter()
            day = 'all'
            to_loop_again = False
        elif data_filter == 'd':
            day = day_filter()
            month = 'all'
            to_loop_again = False
        elif data_filter == 'n':
            print("\n\tThe data will be unfiltered.")
            month = 'all'
            day = 'all'
            to_loop_again = False
        else:
            print()
            continue    
    print('-'*40)
    return city, month, day

     
        
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read the file for the user-chosen city.
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert Start Time column to datetime for analysis.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Filter by month if applicable.  If 'All' is chosen, don't filter.
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_int = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['Start Time'].dt.month == month_int]

    # filter by day of week if applicable. Don't filter if 'All' is chosen.
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        # df = df[df['Start Time'].dt.dayofweek == days.index(day)]
        day_int = days.index(day) + 1
        df = df[df['Start Time'].dt.dayofweek == day_int]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
            * Displays greatest rental month
            * Displays greatest rental day of week
            * Shows most common rental hour 
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month

    popular_month = int(df['month'].mode())

    # REFACTOR the month most traveled print line:
    print("\nThe month most traveled: {}".format(months[popular_month].title()))


    # TO DO: display the most common day of week
    df['days_of_week'] = df['Start Time'].dt.dayofweek # days_of_week is a column of days by index
    
    the_mode_of_days = (df['days_of_week'].mode()).to_string()[5]
    
    print("The most popular day of the week traveled was ", days[int(the_mode_of_days)].title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = int(df['hour'].mode()) + 1
    print("The most popular start time hour was ", popular_hour, ": 00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays bike station statistics:

            * Most common start Station
            * Most common end station
            * Most common start-end combination
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    best_start_station = (df['Start Station'].mode())
    print("\n\nThe most common start station was: \n\t", best_start_station)
    print(best_start_station)

    # TO DO: display most commonly used end station
    best_end_station = (df['End Station'].mode())
    print("\nThe most common end station was: \n\t")
    print(best_end_station)
    
    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + "\n  and " + df['End Station']
    best_combo = df['Station Combo'].mode()
    print("\nAnd the most frequent start - end combination of stations was: \n\t")
    print(best_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = int(df['Trip Duration'].sum())
    print("\n\nThe total trip duration for the time period was ", total_travel, " seconds.")

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("\nThe average trip duration for the time period was ", mean_travel, " seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    subscribers = 0
    customers = 0
    x = 0   # for use as a counter
    # For loop will sum up the amount of Subscribers and Customers
    # REFACTOR the for loop
    for user_type in df['User Type']:
        if user_type == 'Subscriber':
            subscribers += 1
        else:
            customers += 1
        x += 1
    
    print("\n\nThe number of subscribers was ", subscribers)
    print("\nThe number of customers was ", customers)

    # TO DO: Display counts of gender. Washington is treated differently.
    if city == 'washington':
        print("\n\nThe gender is not reported for Washington.")
    else:
        female = 0
        male = 0
        for person in df['Gender']:
            if person == 'Male':
                male += 1
            elif person == 'Female':
                female += 1
            else:
                pass
        print("\n\nNote that the data is collected only of subscribers:")
        print("\nTotal of males: " + str(male))
        print("Total of females: " + str(female))

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print("\n\nThe earliest birth year was " + str(df['Birth Year'].min()))
        print("The latest birth year was " + str(df['Birth Year'].max()))
        print("The most common year of birth was " + str(df['Birth Year'].mode()))
    else:
        print("\n\nNo birth year data is available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Finding out if user wants to see raw data.  If so, data is provided
    5 lines at a time. User must press enter to see more rows. """
    to_stay = True
    while to_stay:
        see_raw = input("\n\n\nWould you like to see the raw data? (yes/no) ")
        if see_raw.lower() != 'yes':
            to_stay = False
        else:
            print("\n\nResults are presented 5 rows per unit. Press ENTER to see more.")
            print("\nEnter 'x' to exit.")
            our_iter = df.shape[1]  # Need to know how many rows to be able to iterate over.
            counter = 0  # For set of 5 rows at a time.
            loop_again = True
            while loop_again:
                internal_counter = 0  # For index of each individual line.
                for index, row in df.iterrows():
                    print(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    if (index == our_iter):
                        loop_again = False
                        break
                    counter +=1
                    if counter%5 == 0:
                        is_x = input()
                        if is_x == 'x':
                            loop_again = False
                            break
                
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
