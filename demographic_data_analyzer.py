import numpy as np
import pandas as pd

df_raw = pd.read_csv('/workspaces/codespaces-jupyter/census-income.csv', header=None, quotechar='"')
df = df_raw[0].str.split(',', expand=True)

#Give each column a proper name
cols = [
    'age', 'class_of_worker', 'industry_code', 'occupation_code', 'education',
    'wage_per_hour', 'enrolled_in_edu', 'marital_status', 'major_industry',
    'major_occupation', 'race', 'hispanic_origin', 'sex', 'member_labor_union',
    'reason_unemployment', 'employment_stat', 'capital_gains', 'capital_losses',
    'dividends', 'tax_filer_stat', 'region_prev_res', 'state_prev_res',
    'detailed_household_and_family', 'detailed_household_summary',
    'instance_weight', 'migration_code_msa', 'migration_code_reg',
    'migration_code_within_reg', 'live_in_metro', 'migration_prev_sunbelt',
    'num_persons_worked_for_employer', 'family_members_under18',
    'country_of_birth_father', 'country_of_birth_mother', 'country_of_birth_self',
    'citizenship', 'own_business_or_self_employed', 'fill_inc_questionnaire',
    'veterans_benefits', 'weeks_worked_in_year', 'year', 'salary'
]
df.columns = cols


df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))


df['age'] = pd.to_numeric(df['age'])
df['weeks_worked_in_year'] = pd.to_numeric(df['weeks_worked_in_year'])

# Calculations.
race_count = df['race'].value_counts()
print(f"Race Count:\n{race_count}\n")


average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)
print(f"Average Age of Men: {average_age_men}")


percentage_bachelors = round(
    len(df[df['education'] == 'Bachelors degree(BA AB BS)']) / len(df) * 100, 1
)
print(f"Percentage of Bachelors Degree Holders: {percentage_bachelors}%")


advanced_edu = df['education'].isin([
    'Bachelors degree(BA AB BS)',
    'Masters degree(MA MS MEng MEd MSW MBA)',
    'Doctorate degree(PhD EdD)'
])
higher_education_rich = round(
    len(df[advanced_edu & (df['salary'] == '50000+.')]) / len(df[advanced_edu]) * 100, 1
)
print(f"Percentage of Higher Education Workers Earning >50K: {higher_education_rich}%")


lower_education_rich = round(
    len(df[~advanced_edu & (df['salary'] == '50000+.')]) / len(df[~advanced_edu]) * 100, 1
)
print(f"Percentage of Lower Education Workers Earning >50K: {lower_education_rich}%")


min_work_hours = df['weeks_worked_in_year'].min()
print(f"Minimum Hours Worked Per Week: {min_work_hours}")


min_workers = df[df['weeks_worked_in_year'] == min_work_hours]
rich_percentage = round(
    len(min_workers[min_workers['salary'] == '50000+.']) / len(min_workers) * 100, 1
)
print(f"Percentage of Min Hours Workers Earning >50K: {rich_percentage}%")


country_rich_pct = df.groupby('country_of_birth_self')['salary'].apply(
    lambda x: round((x == '50000+.').sum() / len(x) * 100, 1)
)
highest_earning_country = country_rich_pct.idxmax()
highest_earning_country_percentage = country_rich_pct.max()
print(f"Highest Earning Country: {highest_earning_country}")
print(f"Percentage of Residents Earning >50K: {highest_earning_country_percentage}%")


india_high_earners = df[
    (df['country_of_birth_self'] == 'India') & (df['salary'] == '50000+.')
]
top_IN_occupation = india_high_earners['major_occupation'].value_counts().idxmax()
print(f"Top Occupation in India: {top_IN_occupation}")

