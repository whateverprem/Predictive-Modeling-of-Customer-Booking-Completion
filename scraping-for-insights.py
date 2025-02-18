import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches

# ---- Step 1: Scraping Reviews from the Website ----

def scrape_reviews(url):
    reviews = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    review_blocks = soup.find_all('div', {'class': 'text_content'})

    for block in review_blocks:
        review_text = block.get_text(strip=True)
        reviews.append(review_text)

    return reviews

# Define the URL for British Airways reviews
url = 'https://www.airlinequality.com/airline-reviews/british-airways/'

# Scrape the reviews
reviews = scrape_reviews(url)

# Store the reviews in a DataFrame and save to CSV
reviews_df = pd.DataFrame(reviews, columns=['Review'])
reviews_df.to_csv('data/british_airways_reviews.csv', index=False)

print(f"Scraped {len(reviews)} reviews from British Airways.")

# ---- Step 2: Cleaning the Data ----

def clean_text(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove anything that's not a letter or space
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

# Clean the reviews
reviews_df['Cleaned_Review'] = reviews_df['Review'].apply(clean_text)

# Save the cleaned data
reviews_df.to_csv('data/cleaned_british_airways_reviews.csv', index=False)

print("Data cleaning complete. Cleaned reviews saved.")

# ---- Step 3: Sentiment Analysis ----

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Apply sentiment analysis to the cleaned reviews
reviews_df['Sentiment'] = reviews_df['Cleaned_Review'].apply(get_sentiment)

# Save sentiment analysis results
reviews_df.to_csv('data/sentiment_british_airways_reviews.csv', index=False)

print("Sentiment analysis complete. Results saved.")

# ---- Step 4: Word Cloud Visualization ----

# Join all reviews into one long text string
all_reviews = ' '.join(reviews_df['Cleaned_Review'])

# Create the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)

# Save the word cloud image
wordcloud.to_file('wordcloud_british_airways.png')

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
