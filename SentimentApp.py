import streamlit as st
from newspaper import Article
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    return article

def show_title_info(article):
    st.markdown('## Title Info')
    st.markdown('#### Title')
    st.write(article.title)

    title_blob = TextBlob(article.title)

    st.markdown('#### Sentiment')
    st.write(f'{title_blob.polarity}')
    st.markdown('#### Subjectivity')
    st.write(f'{title_blob.subjectivity}')

def show_article_info(article):
    st.markdown('## Article Info')
    content_blob = TextBlob(article.text)

    data = {
        'sentence': [],
        'polarity': [],
        'subjectivity': []
    }

    for sentence in content_blob.sentences:
        data['sentence'].append(str(sentence))
        data['polarity'].append(sentence.polarity)
        data['subjectivity'].append(sentence.subjectivity)

    df = pd.DataFrame(data)

    st.markdown('#### Avg Subjectivity')
    st.write(f"{round(df['subjectivity'].mean(), 2)}")
    st.markdown('#### Avg Polarity')
    st.write(f"{round(df['polarity'].mean(), 2)}")

    st.markdown('#### Select a sentiment')
    option = st.selectbox(label='', options=['positive', 'neutral', 'negative'])

    show_stats(option, df)
    
    st.markdown('---')
    st.markdown('#### All sentences')
    st.table(df)

def show_stats(sentiment, df):
    if sentiment == 'positive':
        group = df[df['polarity'] > 0].reset_index(drop=True)
    elif sentiment == 'negative':
        group = df[df['polarity'] < 0].reset_index(drop=True)
    else:
        group = df[df['polarity'] == 0].reset_index(drop=True)

    sentences = ''

    for i in range(len(group)):
        sentences += group.iloc[i]['sentence']
        
    blob = TextBlob(sentences)

    words = []

    stop_words = stopwords.words('english')
    for w in blob.words:
        if w not in stop_words and not w.startswith("'"):
            words.append(w)

    unique_words = Counter(words).keys()
    word_counts = Counter(words).values()

    counts = pd.DataFrame()
    counts['word'] = unique_words
    counts['count'] = word_counts

    top_three = counts.sort_values('count', ascending=False)[:3].reset_index(drop=True)

    st.markdown(f'#### Most common words used in {sentiment} sentences')
    st.write(top_three)

def main():
    st.title('Article Analysis')

    st.markdown('### Enter the link to a news article')
    url = st.text_input(label='')

    try:
        article = get_article(url)
        show_title_info(article)
        show_article_info(article)
    except:
        st.markdown('### Invalid URL')

if __name__ == '__main__':
    main()
