import os
import praw
import asyncio
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit credentials from environment variables
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

# Parameters for subreddit and user lists from environment variables
SUBREDDIT = os.getenv('SUBREDDIT')
UPVOTE_USERS = os.getenv('UPVOTE_USERS').split(',')
DOWNVOTE_USERS = os.getenv('DOWNVOTE_USERS').split(',')

print(f'UPVOTE_USERS: {UPVOTE_USERS}')
print(f'DOWNVOTE_USERS: {DOWNVOTE_USERS}')

async def vote_on_item(item):
    author = item.author.name
    if author in UPVOTE_USERS:
        item.upvote()
        print(f'Upvoted post/comment by {author}: {item.id}')
    elif author in DOWNVOTE_USERS:
        item.downvote()
        print(f'Downvoted post/comment by {author}: {item.id}')
    # Introduce a random delay between actions
    await asyncio.sleep(random.uniform(2, 5))

async def check_subreddit():
    subreddit = reddit.subreddit(SUBREDDIT)
    processed_posts = set()
    processed_comments = set()
    
    while True:
        for submission in subreddit.new(limit=10):
            if submission.id not in processed_posts:
                await vote_on_item(submission)
                processed_posts.add(submission.id)
                
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if comment.id not in processed_comments:
                    await vote_on_item(comment)
                    processed_comments.add(comment.id)
                    
        # Introduce a random delay between each subreddit check
        await asyncio.sleep(random.uniform(30, 90))

async def main():
    await check_subreddit()

# Run the main function
asyncio.run(main())
