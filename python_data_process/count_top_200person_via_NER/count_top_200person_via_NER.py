from collections import Counter
import pandas as pd

df = pd.read_csv('cna_news_200_preprocessed.csv',sep='|')

allowedNE=['PERSON']
news_categories=['政治','科技','運動','證卷','產經','娛樂','生活','國際','社會','文化','兩岸']

def ne_word_frequency( a_news_ne ):
    filtered_words =[]
    for _,_,ne,word in a_news_ne:
        if (len(word) >= 2) & (ne in allowedNE):
            filtered_words.append(word)
    counter = Counter( filtered_words )
    return counter.most_common( 200 )


def get_top_ner_words():
    top_cate_ner_words={}
    words_all=[]
    for category in news_categories:
        df_group = df[df.category == category]
        words_group = []

        # concatenate terms in a category
        for row in df_group.entities:
            words_group += eval(row)

        # concatenate all terms
        words_all += words_group

        # Get top words by calling ne_word_frequency() function
        topwords = ne_word_frequency( words_group )
        top_cate_ner_words[category] = topwords

    topwords_all = ne_word_frequency(words_all)
    top_cate_ner_words['全部'] = topwords_all
    
    return list(top_cate_ner_words.items())
    # return top_cate_ne_words

def saveData(data):
    df_hotPersons = pd.DataFrame(data, columns = ['category','top_keys'])
    df_hotPersons.to_csv('news_top_person_by_category_via_ner.csv', sep=',', index=False)

if __name__ == "__main__":
    hotPersons = get_top_ner_words()
    saveData(hotPersons)

