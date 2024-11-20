import tweepy
from groq import Groq

# Twitter API 
api_key = ''
api_secret_key = ''
access_token = ''
access_token_secret = ''

# Groq API 
groq_api_key = ""

# Twitter API
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print(e)

 # Groq API
client = Groq(api_key=groq_api_key)
#keywords
keyword = "teknoloji"
tweets = api.search_tweets(q=keyword, count=5)

for tweet in tweets:
    # Comments
    prompt = f"{tweet.text} hakkında teknoloji üzerine bir yorum yap:"
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Sen bir teknoloji uzmanısın."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192"  # Model Names
    )
    comment = response.choices[0].message.content.strip()

    # Comment
    api.update_status(f"@{tweet.user.screen_name} {comment}", in_reply_to_status_id=tweet.id)
