from collections import Counter
import pandas as pd

news_links =['aipl', 'ait', 'aspt', 'asc', 'aie', 'amov','ahel','aopl','asoc','acul','acn']
news_categories=['政治','科技','運動','證卷','產經','娛樂','生活','國際','社會','文化','兩岸']

# Filter condition: two words and specified POS
# 過濾條件:兩個字以上 特定的詞性
allowedPOS=['Na','Nb','Nc']


def get_top_words():
    df = pd.read_csv('cna_news_200_preprocessed.csv',sep='|')
    top_cate_words={} # final result
    counter_all = Counter() # counter for category '全部'
    for category in news_categories:

        df_group = df[df.category == category]

        # concatenate all filtered words in the same category
        words_group = []
        for row in df_group.token_pos:

            # filter words for each news
            filtered_words =[]
            for (word, pos) in eval(row):
                if (len(word) >= 2) & (pos in allowedPOS):
                    filtered_words.append(word)

            # concatenate filtered words  
            words_group += filtered_words

        # now we can count word frequency
        counter = Counter( words_group )

        # counter 
        counter_all += counter
        topwords = counter.most_common(200)

        # store topwords
        top_cate_words[category]= topwords

    # Process category '全部'
    top_cate_words['全部'] = counter_all.most_common(200)
    
    # To conveniently save data using pandas, we should convert dict to list.
    return list(top_cate_words.items())


def saveData(result):
    df_top_group_words = pd.DataFrame(result, columns = ['category','top_keys'])
    df_top_group_words.to_csv('cna_news_topkey_with_category_via_token_pos.csv', index=False)

if __name__ == "__main__":
    result = get_top_words()
    saveData(result)
