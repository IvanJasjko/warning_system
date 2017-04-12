import pandas
import csv


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics

def run_model():

    data = pandas.read_csv('..\keys\Data.csv')
    tweets = data
    tweets["source_num"] = tweets.Source.map({True: 1, False: 0})
    X = tweets.Text
    y = tweets.source_num

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    vect = CountVectorizer(max_df=1)
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

    nb = BernoulliNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    a = metrics.accuracy_score(y_test, y_pred_class)
    c = metrics.classification_report(y_test, y_pred_class)
    d = metrics.confusion_matrix(y_test, y_pred_class)

    with open('../keys/Eval.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        rows = len(tweets["source_num"])
        heading = ["Prediction", "Time", "User_Name", "User_ID", "Translation", "Tweet_ID","Tweet"]
        w.writerow(heading)

        for index in range(rows):
            example = [tweets.Text[index]]
            source = [data.Source[index]]
            date = (data.Time[index])
            tweet_id = (data.Tweet_ID[index])
            raw_text = (data.Text[index])
            user_name = (data.User_Name[index])
            if tweet_id != "None":
                tweet_id = "https://twitter.com/statuses/" + data.Tweet_ID[index]
            translation = tweets.Translation[index]
            rt = data.Retweet[index]
            user_id = data.User_ID[index]
            prediction = vect.transform(example)
            example_prediction = nb.predict(prediction)
            evaluation = [example_prediction[0], date, user_name, user_id, translation, tweet_id,raw_text]
            if (example_prediction[0] == 1 and source[0] == False and rt == False):
                w.writerow(evaluation)

    f.close()

    key_words = 'planes | plane | aircraft | air strike | injured | killed | ' \
                'approaches | warning | spotted | helicopter | artillery | ' \
                'explosion | rockets | rocket | fire'

    df = pandas.read_csv('..\keys\Eval.csv')
    df['Translation'].replace(regex=True, inplace=True, to_replace=r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*',
                              value=r'<link>')
    df_new = df.drop_duplicates(subset='Translation')
    warnings = df_new[(df_new['Translation'].str.contains(key_words, case=False)) & (
        df_new['Translation'].str.contains('aleppo | milking', case=False))]
    warnings.to_csv("..\keys\Warnings.csv", index=False, encoding='utf-8-sig')


    print("[Analysis Rerun]", a)


if __name__ == '__main__':
    while(1):
        run_model()


