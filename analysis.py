import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load datasets
users_df = pd.read_csv('users.csv')
repos_df = pd.read_csv('repositories.csv')

# Convert date columns to datetime
users_df['created_at'] = pd.to_datetime(users_df['created_at'])
repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])

top_5_followers = users_df.sort_values(
    by='followers', ascending=False).head(5)['login'].tolist()
print(','.join(top_5_followers))


# --------------
# Question 2: 5 Earliest Registered Users

earliest_5 = users_df.sort_values(by='created_at').head(5)['login'].tolist()
print(','.join(earliest_5))

# --------------
# Question 3: 3 Most Popular Licenses

top_licenses = repos_df['license_name'].dropna(
).value_counts().head(3).index.tolist()
print(','.join(top_licenses))

# --------------
# Question 4: Majority Company

majority_company = users_df['company'].mode()[0]
print(majority_company)

# --------------
# Question 5: Most Popular Programming Language

top_language = repos_df['language'].value_counts().idxmax()
print(top_language)

# --------------
# Question 6: Second Most Popular Language Post-2020

post_2020 = users_df[users_df['created_at'] > '2020-01-01']
post_repos = repos_df[repos_df['login'].isin(post_2020['login'])]
top_languages_post = post_repos['language'].value_counts()
if len(top_languages_post) >= 2:
    second_top_language = top_languages_post.index[1]
    print(second_top_language)
else:
    print(top_languages_post.index.tolist())

# --------------
# Question 7: Language with Highest Average Stars

stars_per_language = repos_df.groupby('language')['stargazers_count'].mean()
highest_avg_stars_lang = stars_per_language.idxmax()
print(highest_avg_stars_lang)

# --------------
# Question 8: Top 5 Leader Strength Users

users_df['leader_strength'] = users_df['followers'] / \
    (1 + users_df['following'])
top_leaders = users_df.sort_values(
    by='leader_strength', ascending=False).head(5)['login'].tolist()
print(','.join(top_leaders))

# --------------
# Question 9: Correlation Between Followers and Repos

correlation = users_df['followers'].corr(users_df['public_repos'])
print(f"{correlation:.3f}")

# --------------
# Question 10: Regression Slope of Followers on Repos

X = users_df[['public_repos']].values
y = users_df['followers'].values
reg = LinearRegression().fit(X, y)
slope = reg.coef_[0]
print(f"{slope:.3f}")

# --------------
# Question 11: Correlation Between Projects and Wiki Enabled

# Drop rows with missing values
proj_wiki = repos_df[['has_projects', 'has_wiki']].dropna()
correlation_pw = proj_wiki['has_projects'].corr(proj_wiki['has_wiki'])
print(f"{correlation_pw:.3f}")

# --------------
# Question 12: Hireable Users Follow More

hireable = users_df[users_df['hireable'] == True]
not_hireable = users_df[users_df['hireable'] != True]

avg_following_hire = hireable['following'].mean()
avg_following_not_hire = not_hireable['following'].mean()

difference = avg_following_hire - avg_following_not_hire
print(f"{difference:.3f}")

# --------------
# Question 13: Impact of Bio Length on Followers

# Calculate bio word count
users_with_bio = users_df[users_df['bio'].notna() & (
    users_df['bio'] != '')].copy()
users_with_bio['bio_word_count'] = users_with_bio['bio'].apply(
    lambda x: len(x.split()))

X_bio = users_with_bio[['bio_word_count']].values
y_followers = users_with_bio['followers'].values

reg_bio = LinearRegression().fit(X_bio, y_followers)
slope_bio = reg_bio.coef_[0]
print(f"{slope_bio:.3f}")

# --------------
# Question 14: Users Creating Repos on Weekends

# 5=Saturday, 6=Sunday
repos_df['created_weekday'] = repos_df['created_at'].dt.weekday
weekend_repos = repos_df[repos_df['created_weekday'] >= 5]

top_weekend_creators = weekend_repos['login'].value_counts().head(
    5).index.tolist()
print(','.join(top_weekend_creators))

# --------------
# Question 15: Hireable Users Sharing Emails More

total_hireable = hireable.shape[0]
total_not_hireable = not_hireable.shape[0]

fraction_hireable = hireable['email'].notna().sum(
) / total_hireable if total_hireable > 0 else 0
fraction_not_hireable = not_hireable['email'].notna().sum(
) / total_not_hireable if total_not_hireable > 0 else 0

difference_email = fraction_hireable - fraction_not_hireable
print(f"{difference_email:.3f}")

# --------------
# Question 16: Most Common Surname

# Extract surnames
users_with_name = users_df[users_df['name'].notna() & (
    users_df['name'] != '')].copy()
users_with_name['surname'] = users_with_name['name'].apply(
    lambda x: x.strip().split()[-1])

surname_counts = users_with_name['surname'].value_counts()
max_count = surname_counts.max()
common_surnames = surname_counts[surname_counts == max_count].index.tolist()
common_surnames_sorted = sorted(common_surnames)
print(','.join(common_surnames_sorted))
