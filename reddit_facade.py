# check  https://www.reddit.com/prefs/apps to fetch client id and secret
import praw
from config import secrets

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


def get_posts(subreddit_name, limit):
    # Fetch the top 5 latest posts from the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    new_posts = subreddit.hot(limit=limit)
    return new_posts

    # for post in new_posts:
    #     print(f'Title: {post.id}')
    #     print(f'Title: {post.title}')
    #     print(f'Author: {post.author}')
    #     print(f'Score: {post.score}')
    #     print(f'URL: {post.url}')
    #     print(f'URL: {post.selftext}')


def fetch_comments(post, limit):
    # Fetch the top 5 comments for the post
    post.comments.replace_more(limit=None)  # This loads all comments
    top_comments = post.comments.list()[:limit]
    return top_comments
    # for comment in top_comments:
    #     print(f'Comment Author: {comment.author}')
    #     print(f'Comment Score: {comment.score}')
    #     print(f'Comment Body: {comment.body}')
    #     print('---')





