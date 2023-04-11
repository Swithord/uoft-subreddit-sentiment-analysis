from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime as dt, timedelta
import requests
api = PushshiftAPI()

# d1 = dt.today()
# d2 = dt.today()
d2 = dt(2022, 12, 7, 00, 00)

while True:
    d1, d2 = d2, d2 - timedelta(days=5)
    print('getting ')
    posts = api.search_comments(subreddit='uoft',before=d1,after=d2)
    post_list = [post for post in posts]
    print(post_list)
    if len(post_list) > 1:
        time = post_list[-1]['created_utc']
        df = pd.DataFrame(post_list)
        print(post_list[0]['created_utc'], time)
        df[['title', 'selftext', 'author', 'upvote_ratio', 'created_utc']].to_csv('uoft_comments.csv', mode='a', header=False)