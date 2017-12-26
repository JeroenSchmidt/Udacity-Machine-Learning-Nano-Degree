#NOTE, this class has to be writen to a py script inorder for joblib Parallel to work in jupyter notebooks on windows

from joblib import Parallel, delayed
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer, fbeta_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import model_selection

#clf = RandomForestClassifier(random_state=10)
clf = GradientBoostingClassifier(random_state=10)


seed = 123

scorer = make_scorer(fbeta_score, beta=2)

def train_model_n_estimators(X, y, n_est):
    clf.set_params(n_estimators=n_est)
    kfold = model_selection.KFold(n_splits=3, random_state=seed)
    scores = model_selection.cross_val_score(clf, X,y, cv=kfold, scoring=scorer)
    return scores.mean()*100

def train_model_max_depth(X, y, max_depth):
    clf.set_params(max_depth=max_depth)
    kfold = model_selection.KFold(n_splits=3, random_state=seed)
    scores = model_selection.cross_val_score(clf, X,y, cv=kfold, scoring=scorer)
    return scores.mean()*100

def train_model_min_samples_leaf(X, y, min_samples_leaf):
    clf.set_params(min_samples_leaf=min_samples_leaf)
    kfold = model_selection.KFold(n_splits=3, random_state=seed)
    scores = model_selection.cross_val_score(clf, X,y, cv=kfold, scoring=scorer)
    return scores.mean()*100