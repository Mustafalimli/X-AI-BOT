import tweepy
import nltk
import firebase_admin
from firebase_admin import credentials, firestore

# Gerekli NLTK araçlarını indiriyoruz
nltk.download('punkt')

# Firebase yapılandırması (Firebase Admin SDK kullanarak)
cred = credentials.Certificate('path/to/your/firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# API anahtarlarını ve token'ları buraya ekleyin
api_key = 'fjpDiXtZkbIsJzRI6pvTAz7bl    '
api_secret_key = 'DQ5IsqqvqiZIOZp6AmY7OYu5NMzJ5ip21K9maXdx2oXsBMAA8E'
access_token = '1856843515541749760-ZRDH7D29m9qJbX5N0qqXFL9XlsBIzP'
access_token_secret = 'fgGIeVl4LljVBLjCW1yGY9SGIPSkCykoQGbL3A5d2FeEZ'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALjPwwEAAAAAaVLvQPLKDrjFKBQHV1Wb%2B07ZnFs%3Db4NSpWpUyYvQPaSC0vkjo963ABrIwOaGcMOFvaO7o69DRJhjcO' 

# Twitter API'ye bağlantı (OAuth1 kullanımı)
auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
api = tweepy.API(auth)

# Gönderiye yorum yapacak fonksiyon
def comment_on_tweet(tweet_id, comment):
    try:
        api.update_status(status=comment, in_reply_to_status_id=tweet_id)
        print(f"Yorum yapıldı: {comment}")
    except Exception as e:
        print(f"Yorum yaparken hata: {e}")

# Yapay zeka tabanlı yorum oluşturma fonksiyonu
def generate_comment(tweet_text):
    # Groq AI veya başka bir AI modeli ile yorum üretme
    # Bu kısımda Groq API kullanarak yorum üretilmesi gerektiğini varsayıyorum.
    
    # Örnek bir yorum olarak rastgele birkaç sözcük ekleyelim (bu kısmı Groq AI ile değiştirin)
    comment = f"Bu gönderi hakkında düşündüklerim: {tweet_text[:50]}..."
    return comment

# StreamingClient sınıfı
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_id = tweet.id
        tweet_text = tweet.text
        
        # Yapay zeka ile yorum oluşturma
        comment = generate_comment(tweet_text)

        # Yorum yapma
        comment_on_tweet(tweet_id, comment)

        # Firebase'e tweet bilgilerini kaydetme
        self.save_to_firebase(tweet_id, tweet_text, comment)

    def save_to_firebase(self, tweet_id, tweet_text, comment):
        try:
            doc_ref = db.collection('tweets').document(str(tweet_id))
            doc_ref.set({
                'tweet_text': tweet_text,
                'comment': comment,
                'status': 'commented'
            })
            print(f"Tweet bilgileri Firebase'e kaydedildi: {tweet_id}")
        except Exception as e:
            print(f"Firebase'e kaydederken hata: {e}")

# API anahtarlarıyla StreamingClient başlatma
client = MyStreamListener(bearer_token=bearer_token)

# Anahtar kelimelere göre stream başlatma
client.add_rules(tweepy.StreamRule("otomatik OR yorum OR bot"))
client.filter()
