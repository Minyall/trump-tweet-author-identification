import pandas as pd
import numpy as np
from src.load_pickle import load_pickle
from src.cross_val_data import cross_val_data
from src.standardize import standardize
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def main():
    # Load the data
    (X_train, X_val, X_test,
     X_train_tfidf, X_val_tfidf, X_test_tfidf,
     X_train_pos, X_val_pos, X_test_pos,
     X_train_ner, X_val_ner, X_test_ner,
     y_train, y_val, y_test) = load_pickle('pickle/old_pickle/data.pkl')

    # Performing cross-validation, don't need to separate train and validation
    (X_train, X_train_tfidf, X_train_pos, X_train_ner,
     X_test, X_test_tfidf, X_test_pos, X_test_ner) = cross_val_data(X_train,
                                                                    X_val,
                                                                    X_test)
    # Concatenate all training DataFrames
    X_train = pd.concat([X_train, X_train_tfidf,
                         X_train_pos, X_train_ner], axis=1)
    X_test = pd.concat([X_test, X_test_tfidf,
                        X_test_pos, X_test_ner], axis=1)
    y_train = pd.concat([y_train, y_val], axis=0)

    # Standardize the X data
    feature = ['favorite_count', 'is_retweet', 'retweet_count', 'is_reply',
               'compound', 'v_negative', 'v_neutral', 'v_positive', 'anger',
               'anticipation', 'disgust', 'fear', 'joy', 'negative',
               'positive', 'sadness', 'surprise', 'trust', 'tweet_length',
               'avg_sentence_length', 'avg_word_length', 'commas',
               'semicolons', 'exclamations', 'periods', 'questions', 'quotes',
               'ellipses', 'mentions', 'hashtags', 'urls', 'is_quoted_retweet',
               'all_caps', 'tweetstorm', 'hour', 'hour_20_02', 'hour_14_20',
               'hour_08_14', 'hour_02_08', 'start_mention']

    (X_train, X_test) = standardize(feature, X_train, X_test)

    feat = np.load('pickle/top_features.npz')['arr_0']

    result = svc_grid_search(np.array(X_train[feat[:50]]),
                             np.array(y_train).ravel())
    print(result.best_params_, result.best_score_)


def svc_grid_search(X, y):
    parameters = {'C': [.01, .1, 1, 10, 100],
                  'kernel': ['rbf', 'poly', 'sigmoid'],
                  'degree': [2, 3, 4],
                  'gamma': ['auto'],
                  'shrinking': [True, False],
                  'coef0': [0., .1, 1]}

    '''
    Results:
    Fitting 3 folds for each of 270 candidates, totalling 810 fits
    [Parallel(n_jobs=1)]: Done 810 out of 810 | elapsed: 407.4min finished
    {'C': 100, 'coef0': 1, 'degree': 2, 'gamma': 'auto', 'kernel': 'poly',
    'shrinking': False} 0.892531737257
    '''

    svc = SVC()
    clf = GridSearchCV(svc, parameters, verbose=True)
    clf.fit(X, y)

    return clf


if __name__ == '__main__':
    main()