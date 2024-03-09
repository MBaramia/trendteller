import requests
from newspaper import Article
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

# Ensure the necessary NLTK data packages are downloaded
nltk.download('punkt', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Dictionary mapping company IDs to their names
company_symbols = {
    0: 'Apple', 1: 'Amazon', 2: 'Google', 3: 'Microsoft', 4: 'Tesla',
    5: 'JPMorgan', 6: 'Walmart', 7: 'Coca-Cola', 8: 'Pfizer', 9: 'Netflix'
}

def analyze_sentiment(content):
    """Analyze the sentiment of content using NLTK's VADER."""
    return sia.polarity_scores(content)

def extract_key_phrases(summary, sentiment_score):
    """Extract key phrases from summary based on the sentiment score."""
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
    """Determine the effect score based on the sentiment score."""
    if abs(sentiment_score) > 0.5:
        return 2  # High impact
    elif abs(sentiment_score) > 0.1:
        return 1  # Moderate impact
    else:
        return 0  # Low impact

def generate_analysis(sentiment_score, key_phrases):
    """Generate an analysis based on sentiment score and key phrases."""
    if sentiment_score > 0:
        return f"The key information: '{key_phrases}', suggests positive implications for the company."
    elif sentiment_score < 0:
        return f"The key information: '{key_phrases}', suggests negative implications for the company."
    else:
        return "The sentiment of the article is neutral, indicating balanced or inconclusive implications for the company."

def assign_company_id(summary):
    """Assign a company ID based on the presence of company names in the summary."""
    symbol_to_id = {symbol: company_id for company_id, symbol in company_symbols.items()}
    for symbol, company_id in symbol_to_id.items():
        if symbol in summary:
            return company_id
    return None  # Return None if no company symbol is found in the summary

def process_articles(pageSize):
    api_key = 'c8b60645ebf34d9693635b377b63afbf'
    """Fetch, process, and return article data."""
    articles_data = []
    companies = list(company_symbols.values())
    query = ' OR '.join(companies)
    url = "https://newsapi.org/v2/everything"
    params = {'q': query, 'language': 'en', 'pageSize': pageSize, 'apiKey': api_key}
    response = requests.get(url, params=params)

    articles = response.json().get('articles', []) if response.status_code == 200 else []

    for article in articles:
        article_instance = Article(article['url'])
        try:
            article_instance.download()
            article_instance.parse()
            article_instance.nlp()
            summary = article_instance.summary
        except Exception as e:
            summary = "Failed to process the article."

        sentiment = analyze_sentiment(summary)
        sentiment_score = sentiment['compound']
        effect_score = determine_effect_score(sentiment_score)
        key_phrases = extract_key_phrases(summary, sentiment_score)
        analysis = generate_analysis(sentiment_score, key_phrases)
        company_id = assign_company_id(summary)

        articles_data.append({
            'date': article['publishedAt'],
            'title': article['title'],
            'source': article['source']['name'],
            'link': article['url'],
            'summary': summary,
            'analysis': analysis,
            'sentiment_score': sentiment_score,
            'effect_score': effect_score,
            'company_id': company_id
        })

    return articles_data
