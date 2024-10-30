# Toronto GitHub Data Analysis

- **Data Collection Process:** Utilized the GitHub API to scrape data on users located in Toronto with over 100 followers. Implemented data cleaning techniques to standardize company names and handle missing values. To optimize performance, the script loads existing CSV files if available and fetches only the first page of repositories per user.
- **Interesting Finding:** Discovered that "Ahmed" is the most common surname among developers in Toronto, indicating a significant presence of developers from regions where "Ahmed" is prevalent.
- **Actionable Recommendation:** Recommend developers focus on enhancing repository features like projects and wikis to increase visibility and follower count, as these features are correlated with higher engagement metrics.

## Files

- `users.csv`: Contains detailed information about GitHub users in Toronto with over 100 followers.
- `repositories.csv`: Contains repository data for the aforementioned users.
- `datacollection.py`: Python script used for data scraping from the GitHub API.
- `analysis.py`: Python script used for analyzing the scraped data.
- `.env`: Environment variables file containing your GitHub Personal Access Token.
- `requirements.txt`: Lists all Python dependencies required for the project.

## Analysis Results

Below are the answers to the project's analytical questions based on the scraped data:

1. **Top 5 Users by Followers:**
   aneagoie, ZhangMYihua, susanli2016, thedaviddias, ange-yaghi

2. **5 Earliest Registered Users:**
   jamesmacaulay, michaelklishin, myles, nwjsmith, vito

3. **3 Most Popular Licenses:**
   MIT License, Apache License 2.0, Other

4. **Majority Company:**
   UNIVERSITY OF TORONTO

5. **Most Popular Programming Language:**
   JavaScript

6. **Second Most Popular Language Post-2020:**
   TypeScript

7. **Language with Highest Average Stars per Repository:**
   Cython

8. **Top 5 Leader Strength Users:**
   aneagoie, nayuki, GrapheneOS, hlissner, rspivak

9. **Correlation Between Followers and Repos:**
   0.056

10. **Regression Slope of Followers on Repos:**
    0.253

11. **Correlation Between Projects and Wiki Enabled:**
    0.398

12. **Hireable Users Follow More People Than Non-Hireable Users:**
    -13.334

13. **Impact of Bio Length on Followers:**
    8.381

14. **Users Creating Repositories on Weekends:**
    tomhodgins, davepagurek, DjDeveloperr, joeyism, EmilyGraceSeville7cf

15. **Hireable Users Sharing Emails More Often:**
    0.135

16. **Most Common Surname:**
    Ahmed
