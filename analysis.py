import pandas
import update


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

def run_model():

    data = pandas.read_csv('..\keys\Data.csv')
    tweets = data

    tweets["Text"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    tweets["Translation"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    tweets["source_num"] = tweets.Source.map({True: 1, False: 0})

    X = tweets.Text
    y = tweets.source_num

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    vect = CountVectorizer(max_df=1)
    X_train_dtm = vect.fit_transform(X_train).toarray()
    X_test_dtm = vect.transform(X_test).toarray()

    nb = GaussianNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    a = metrics.accuracy_score(y_test, y_pred_class)
    c = metrics.classification_report(y_test, y_pred_class)
    d = metrics.confusion_matrix(y_test, y_pred_class)


    vect_data = vect.transform(tweets["Text"]).toarray()
    prediction = nb.predict(vect_data)
    tweets["Prediction"] = prediction

    pre_filter = tweets[(tweets.Prediction == 1) & (tweets.Retweet == False)]
   	

    pre_filter.to_csv("../keys/Eval.csv",index=False,encoding='utf-8-sig')


    key_words = 'plane | raid | air strike |' \
                'approaches | warning | spotted | helicopter | artillery | ' \
                'rockets | rocket | targeted'

    indicators = 'aleppo|milking|urgent|Idlib'
 
    df = pandas.read_csv('..\keys\Eval.csv')
    df['Translation'].replace(regex=True, inplace=True, to_replace=r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*',
                              value=r'<link>')
    df_new = df.drop_duplicates(subset='Translation')

    warnings = df_new[(df_new['Translation'].str.contains(key_words, case=False)) & (
        df_new['Translation'].str.contains(indicators, case=False))]

    warnings_nl = warnings[~warnings.Translation.str.contains('\<link>')]

    warnings_nl.to_csv("..\keys\Warnings.csv", index=False,encoding='utf-8-sig')


    print(d,"\n[Analysis Rerun]",a)


if __name__ == '__main__':
    while(1):
        run_model()
        update.update()



