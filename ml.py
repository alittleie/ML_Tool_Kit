from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.metrics import accuracy_score as acc
from sklearn.linear_model import LogisticRegression as Lr
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.model_selection import GridSearchCV


class Ml:
    x_train = None
    x_test = None
    y_train = None
    y_test = None

    def tts(self, df, test_size=.2, random_state=1, stratify=None, transform=0):
        x = df.drop(axis=1, columns=['Target'])
        y = df['Target']

        if stratify == 1:
            stratify = y

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split\
            (x, y, test_size=test_size, random_state=random_state, stratify=stratify)

        # option 1 uses standard scalar to standardize x variables
        if transform == 1:
            stdsc = StandardScaler()
            self.x_train = stdsc.fit_transform(self.x_train)
            self.x_test = stdsc.transform(self.x_test)

        # option two uses Normalization
        elif transform == 2:
            mms = MinMaxScaler()
            self.x_train = mms.fit_transform(self.x_train)
            self.x_test = mms.transform(self.x_test)

    def model(self, mod='SVM', hyper=None):

        # goes through basic hyper parameter optimization test model and outputs accuracy
        def hyper_mod(model_type, params):
            gs = GridSearchCV(estimator=model_type, param_grid=params, scoring='accuracy', cv=5, n_jobs=-1,
                              verbose=2)
            grid = gs.fit(self.x_train, self.y_train)
            print(grid.best_params_)
            yscore = grid.predict(self.x_test)
            yscoretrain = grid.predict(self.x_train)
            print('Training Accuracy Score: ' + str(acc(self.y_train, yscoretrain)))
            print('Accuracy Score: ' + str(acc(self.y_test, yscore)))

        # does a quick model
        def quick_mod(model_type):
            quick_model = model_type
            quick_model.fit(self.x_train, self.y_train)
            yscore = quick_model.predict(self.x_test)
            yscoretrain = quick_model.predict(self.x_train)
            print(str(quick_model))
            print('Training Accuracy Score: ' + str(acc(self.y_train, yscoretrain)))
            print('Accuracy Score: ' + str(acc(self.y_test, yscore)))

        if mod == 'SVM':
            if hyper is not None:
                model = svm.SVC(kernel='poly', gamma=3, C=5, coef0=5, verbose= 2)
                param_grid = [[{'kernel': ['rbf'], 'gamma': [10, 20, 40, 90, 100, 200], 'C': [1], 'coef0': [.01],
                                'probability': [True]}],
                              [{'kernel': ['rbf'], 'gamma': [10, 15, 20, 25, 30, 40, 50, 70, 90, 100, 150, 200],
                                'C': [.01, .1, 3], 'coef0': [.01, .1, 1], 'probability': [True]}],
                              [{'kernel': ['linear', 'poly', 'rbf'], 'gamma': [.01, .1, 1, 2, 3, 5, 10],
                                'C': [.01, .1, 1, 3, 5, 10], 'coef0': [.01, .1, 1, 3, 5, 10],
                                'probability': [True, False]}]]
                param_grid = param_grid[hyper]
                hyper_mod(model, param_grid)
            else:
                model = svm.SVC(kernel='poly', gamma=3, C=5, coef0=5)
                quick_mod(model)

        elif mod == 'Lr':
            if hyper is not None:
                model = Lr(penalty='l2', C=1, solver='newton-cg', multi_class='multinomial')
                param_grid = [[{'penalty': ['l2', 'none', 'elasticnet', 'l1'], 'C': [.001, .01, .1, 1, ],
                                'solver': ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga'],
                                'multi_class': ['multinomial', 'ovr', 'auto']}],
                              [{'penalty': ['l2', 'none', 'elasticnet', 'l1'], 'C': [.001, .01, .1, 1, 10, 50, 100],
                                'solver': ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga'],
                                'multi_class': ['multinomial', 'ovr', 'auto']}], [
                                  {'penalty': ['l2', 'none', 'elasticnet', 'l1'],
                                   'C': [0001., .001, .01, .1, 1, 2, 4, 6, 10, 25, 50, 100],
                                   'solver': ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga'],
                                   'multi_class': ['multinomial', 'ovr', 'auto']}]]
                param_grid = param_grid[hyper]
                hyper_mod(model, param_grid)
            else:
                model = Lr(penalty='l2', C=1, solver='newton-cg', multi_class='multinomial')
                quick_mod(model)

        elif mod == 'Tree':
            if hyper is not None:
                model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=15, min_samples_split=2,
                                                    min_samples_leaf=1)
                param_grid = [[{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                'min_samples_split': [2, 3, 4, 5], 'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8]}],
                              [{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                'min_samples_split': [2, 3, 4, 5], 'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8]}],
                              [{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None],
                                'min_samples_split': [2, 3, 4, 5, None],
                                'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8, None]}]]
                param_grid = param_grid[hyper]
                hyper_mod(model, param_grid)

            else:
                model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=15, min_samples_split=2,
                                                    min_samples_leaf=1)
                quick_mod(model)

        elif mod == 'RF':
            if hyper is not None:
                model = RandomForestClassifier(criterion='entropy', max_depth=15, min_samples_split=2,
                                               min_samples_leaf=1)
                param_grid = [[{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                'min_samples_split': [2, 3, 4, 5], 'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8]}],
                              [{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                'min_samples_split': [2, 3, 4, 5], 'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8]}],
                              [{'criterion': ['gini', 'entropy'],
                                'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None],
                                'min_samples_split': [2, 3, 4, 5, None],
                                'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8, None]}]]
                param_grid = param_grid[hyper]
                hyper_mod(model, param_grid)

            else:
                model = RandomForestClassifier(criterion='entropy', max_depth=15, min_samples_split=2,
                                               min_samples_leaf=1)
                quick_mod(model)
