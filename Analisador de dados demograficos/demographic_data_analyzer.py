import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df.query('sex == "Male"')['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(
        df[(df.education == 'Bachelors')]['education'].value_counts().sum() *
        100 / len(df.salary), 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[(df.education == "Bachelors") |
                          (df.education == "Masters") |
                          (df.education == "Doctorate")].value_counts().sum()
    lower_education = df[(df.education != "Bachelors")
                         & (df.education != "Masters") &
                         (df.education != "Doctorate")].value_counts().sum()

    # percentage with salary >50K
    higher_education_rich = round(
        df[((df.education == "Bachelors") | (df.education == "Masters") |
            (df.education == "Doctorate"))
           & (df.salary == '>50K')].value_counts().sum() * 100 /
        higher_education, 1)

    lower_education_rich = round(
        df[((df.education != "Bachelors") & (df.education != "Masters") &
            (df.education != "Doctorate"))
           & (df.salary == '>50K')].value_counts().sum() * 100 /
        lower_education, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = min(df['hours-per-week'])

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[(df['hours-per-week'] == 1)
                         & (df.salary == '>50K')].value_counts().sum()

    rich_percentage = (df[(df['hours-per-week'] == 1) &
                          (df.salary == '>50K')].value_counts().sum() *
                       100) / (df[(df['hours-per-week']
                                   == 1)].value_counts().sum())

    # What country has the highest percentage of people that earn >50K?
    grupo = df.groupby(['native-country', 'salary']).size().unstack().reset_index()
    diff = grupo['>50K'] / grupo['<=50K']
    grupo['pct'] = diff
    pct = grupo.sort_values('pct', ascending = False)
    highest_earning_country = grupo.iloc[pct.index[0], 0]

    highest_earning_country_percentage = round((grupo.iloc[pct.index[0],2] *100 / grupo.iloc[pct.index[0], 1:-1].sum()), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & (
        df.salary == '>50K')]['occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print("Country with highest percentage of rich:",
              highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }