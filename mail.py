import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import smtplib
from email.mime.text import MIMEText
from new import calculate_threat_scores

def send_mail():
    # Initialize NLTK's SentimentIntensityAnalyzer
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

    # Sample text for sentiment analysis
    text = "This movie was terrible. I didn't like it at all."

    # Perform sentiment analysis
    sentiment_score = sia.polarity_scores(text)['compound']

    # Define threshold for negative sentiment
    threshold = 1

    threat_index = calculate_threat_scores(sentiment_score, threshold)

    # Check if sentiment score is below the threshold
    if threat_index < threshold:
        # Send email alert
        sender_email = ""
        receiver_email = ""
        password = ""

        message = MIMEText(f"The following text has negative sentiment: {text}")
        message['Subject'] = 'Negative Sentiment Alert'
        message['From'] = ''
        message['To'] = ''

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
