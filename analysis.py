import pandas
import csv
import sklearn
import numpy
import scipy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics



class Analysis(object):

    data = pandas.read_csv('..\keys\Data.csv')
    tweets = data
    tweets["source_num"] = tweets.Source.map({True :1, False :0})
    X = tweets.Translation
    y = tweets.source_num
        
    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state = 1)
    vect = CountVectorizer()
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

        
    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    a = metrics.accuracy_score(y_test, y_pred_class)
    c = metrics.classification_report(y_test,y_pred_class)
    print("\n Accuracy score = ",a,"\n\n",c,"\n")






    def analyse_text(*args):
        
        print("Please enter your text or the tweet you have found:\n")
        while(1):
            i = input()
            if(i == "exit" or i == ""):
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
            heading = ["Prediction","Text","Source","Time"]
            w.writerow(heading)
            rows = len(Analysis.tweets["source_num"])

            for index in range(rows):
                example = [Analysis.tweets.Text[index]]
                source = [Analysis.data.Source[index]]
                date = Analysis.data.Time[index]
                rt = [Analysis.data.Retweet[index]]
                prediction = Analysis.vect.transform(example)
                example_prediction = Analysis.nb.predict(prediction)
                evaluation = [example_prediction[0],Analysis.tweets.Translation[index],source[0],date]
                if(example_prediction[0] == 1 and source[0] == False and Analysis.data.Retweet[index] == False):
                    w.writerow(evaluation)      

            
        print("\nEval.csv created with a list of predictions.")
        
    
if __name__ == '__main__':
    a = Analysis()
    a.scan_data()
    a.analyse_text()
