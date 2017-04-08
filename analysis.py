import pandas
import csv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from controller import translation_ar




class Analysis(object):

    data = pandas.read_csv('..\keys\Data.csv')
    tweets = data
    tweets["source_num"] = tweets.Source.map({True :1, False :0})
    X = tweets.Text
    y = tweets.source_num

    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state = 1)
    vect = CountVectorizer(max_df=1)
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    a = metrics.accuracy_score(y_test, y_pred_class)
    c = metrics.classification_report(y_test,y_pred_class)
    d = metrics.confusion_matrix(y_test,y_pred_class)
    #print("\n Accuracy score = ",a)






    def analyse_text(*args):

        print("Please enter your text or the tweet you have found:\n")
        while(1):
            i = input()
            i = translation_ar(i)
            if(i == ""):
                break
            tolist = [i]
            j = Analysis.vect.transform(tolist)
            pred_j = Analysis.nb.predict(j)
            if(pred_j == 1):
                print("\nThis is a warning, your observation has been recorded.\n")
            else:
                print("\nThis information is irrelevant.\n")



    def scan_data(*args):

        with open('../keys/Eval.csv','w+',encoding = 'utf-8-sig', newline='') as f:
            w = csv.writer(f)
            heading = ["Prediction","Time","User_ID","Translation"]
            w.writerow(heading)
            rows = len(Analysis.tweets["source_num"])

            for index in range(rows):
                example = [Analysis.tweets.Text[index]]
                source = [Analysis.data.Source[index]]
                date = Analysis.data.Time[index]
                translation = Analysis.tweets.Translation[index]
                rt = Analysis.data.Retweet[index]
                user_id = Analysis.data.User_ID[index]
                prediction = Analysis.vect.transform(example)
                example_prediction = Analysis.nb.predict(prediction)
                evaluation = [example_prediction[0],date,user_id,translation]
                if(example_prediction[0] == 1 and source[0] == False and rt == False):
                    w.writerow(evaluation)
        f.close()

    def format_data(*args):
        searchwords = 'planes | plane | aircraft | air strike | urgent | injured | killed | ' \
                      'approach | warning | spotted | helicopter | artillery | bomb |  explo'
        df = pandas.read_csv('..\keys\Eval.csv')
        df['Translation'].replace(regex=True,inplace=True,to_replace=r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*',value=r'<link>')
        df_new = df.drop_duplicates(subset='Translation')
        warnings = df_new[(df_new['Translation'].str.contains(searchwords,case=False)) & (df_new['Translation'].str.contains('aleppo | milking',case=False))]
        warnings.to_csv("..\keys\Warnings.csv", index=False, encoding='utf-8-sig')
        print("Analysis Rerun")



if __name__ == '__main__':
        a = Analysis()
        a.scan_data()
        a.format_data()
