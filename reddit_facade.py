# check  https://www.reddit.com/prefs/apps to fetch client id and secret

import praw
import yaml


secrets = yaml.safe_load(open('secret.yaml', 'r'))
# Reddit API credentials
reddit_client_id = secrets['client_id']
reddit_client_secret = secrets['client_secret']
reddit_user_agent = 'python script'

# Create a Reddit API instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# Specify the subreddit you want to fetch posts and comments from
subreddit_name = 'python'  # Change this to your desired subreddit

# Fetch the top 5 latest posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
new_posts = subreddit.new(limit=5)

# Iterate through the posts and fetch the top 5 comments for each post
for post in new_posts:
    print(f'Title: {post.id}')
    print(f'Title: {post.title}')
    print(f'Author: {post.author}')
    print(f'Score: {post.score}')
    print(f'URL: {post.url}')

    # Fetch the top 5 comments for the post
    post.comments.replace_more(limit=None)  # This loads all comments
    top_comments = post.comments.list()[:5]

    for comment in top_comments:
        print(f'Comment Author: {comment.author}')
        print(f'Comment Score: {comment.score}')
        print(f'Comment Body: {comment.body}')
        print('---')

    print('---')

# media  (dict)
# selftext
#{comment.author}")
        #print(f"Comment Text: {comment.body}

