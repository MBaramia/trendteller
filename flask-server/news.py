import requests
from newspaper import Article
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
nltk.download('vader_lexicon')

# Initialize Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()
company_symbols = {
    0: 'Apple', 1: 'Amazon', 2: 'Google', 3: 'Microsoft', 4: 'Tesla', 
    5: 'JPMorgan', 6: 'Walmart', 7: 'Coca-Cola', 8: 'Pfizer', 9: 'Netflix'
}

def fetch_articles(api_key, pageSize=20):
    companies = ["Apple", "Amazon", "Alphabet", "Microsoft", "Tesla", "JPMorgan", "Walmart", "Coca-Cola", "Pfizer", "Netflix"]
    query = ' OR '.join(companies)  # Combines company names in a single query using OR
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': 'en',
        'pageSize': pageSize,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    return response.json().get('articles', []) if response.status_code == 200 else None

def analyze_sentiment(content):
    return sia.polarity_scores(content)

def extract_key_phrases(summary, sentiment_score):
    sentences = sent_tokenize(summary)
    key_sentences = []
    for sentence in sentences:
        score = sia.polarity_scores(sentence)['compound']
        if sentiment_score > 0 and score > 0.5:
            key_sentences.append(sentence)
        elif sentiment_score < 0 and score < -0.5:
            key_sentences.append(sentence)
    return " ".join(key_sentences) if key_sentences else summary

def determine_effect_score(sentiment_score):
    if abs(sentiment_score) > 0.5:
        return 2  # High impact
    elif abs(sentiment_score) > 0.1:
        return 1  # Moderate impact
    else:
        return 0  # Low impact

def generate_analysis(sentiment_score, key_phrases):
    if sentiment_score > 0:
        return f"The key information: '{key_phrases}', suggests positive implications for the company."
    elif sentiment_score < 0:
        return f"The key information: '{key_phrases}', suggests negative implications for the company."
    else:
        return "The sentiment of the article is neutral, indicating balanced or inconclusive implications for the company."

def assign_company_id(summary):
    # Reverse the company_symbols dictionary to search by symbol
    symbol_to_id = {symbol: company_id for company_id, symbol in company_symbols.items()}

    for symbol, company_id in symbol_to_id.items():
        if symbol in summary:
            return company_id
    return None  # Return None if no company symbol is found in the summary

def process_articles(api_key):
    articles = fetch_articles(api_key, 20)
    if not articles:
        print("Failed to fetch articles")
        return

    for article in articles:
        print(f"Date: {article['publishedAt']}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Link: {article['url']}")

        article_instance = Article(article['url'])
        try:
            article_instance.download()
            article_instance.parse()
            article_instance.nlp()
            summary = article_instance.summary
        except Exception as e:
            print(f"Failed to process the article: {str(e)}")
            summary = ""

        sentiment = analyze_sentiment(summary)
        sentiment_score = sentiment['compound']
        effect_score = determine_effect_score(sentiment_score)
        key_phrases = extract_key_phrases(summary, sentiment_score)
        analysis = generate_analysis(sentiment_score, key_phrases)
        company_id = assign_company_id(summary)

        print(f"Summary: {summary}")
        print(f"Analysis: {analysis}")
        print(f"Sentiment Score: {sentiment_score}")
        print(f"Effect Score: {effect_score}")
        print(f"Company ID: {company_id}")
        print("-" * 50)


if __name__ == "__main__":
    api_key = 'c8b60645ebf34d9693635b377b63afbf'
    process_articles(api_key)
