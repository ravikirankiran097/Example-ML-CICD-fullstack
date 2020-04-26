# coding: utf-8

import click
import mlflow
import mlflow.sklearn
import mlflow.tracking
import mlflow.xgboost
import numpy as np
import pandas as pd
import xgboost as xg
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss, mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC



def dataset(csv_path):
    features = pd.read_csv(csv_path)
    labels = features.pop('class')
    y = np.zeros_like(labels, dtype=int)
    y[labels == 'p'] = 1

    return features, y


def create_random_forest_model(scoring_method):
    random_forest_rfecv = RFECV(estimator=RandomForestClassifier(),
                                step=1,
                                cv=2,
                                n_jobs=-1,
                                scoring='accuracy')

    n_estimators = [100, 300, 500, 800, 1200]
    max_depth = [5, 8, 15, 25, 30]
    min_samples_split = [2, 5, 10, 15, 100]
    min_samples_leaf = [1, 2, 5, 10]

    forest_params = {'n_estimators': n_estimators,
                     'max_depth': max_depth,
                     'min_samples_split': min_samples_split,
                     'min_samples_leaf': min_samples_leaf}

    base_rf = RandomForestClassifier()

    forest_grid = GridSearchCV(base_rf,
                               forest_params,
                               cv=3,
                               verbose=1,
                               n_jobs=-1,
                               scoring=scoring_method
                               )

    rf_estimator_pipe = Pipeline(steps=[('feature_extraction', OneHotEncoder()),
                                        ('rf_feature_selection', random_forest_rfecv),
                                        ('rf_estimator', forest_grid)
                                        ])

    return rf_estimator_pipe


def create_xgboost_model(scoring_method, max_runs):
    xgb_rfecv = RFECV(estimator=SVC(kernel="linear"),
                      step=1,
                      cv=2,
                      scoring='accuracy')

    xgb_params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
    }

    base_xgb = xg.XGBClassifier(learning_rate=0.02,
                                n_estimators=600,
                                objective='binary:logistic',
                                silent=True, nthread=1)

    xgb_random_search = RandomizedSearchCV(base_xgb,
                                           param_distributions=xgb_params,
                                           n_iter=max_runs,
                                           scoring=scoring_method,
                                           n_jobs=-1,
                                           cv=3,
                                           verbose=3,
                                           )
    xgb_estimator_pipe = Pipeline(steps=[('feature_extraction', OneHotEncoder()),
                                         ('svc_feature_selection', xgb_rfecv),
                                         ('xgb_estimator', xgb_random_search)
                                         ])

    return xgb_estimator_pipe


def create_mushroom_model(scoring_method, max_runs):
    estimators = [
        ('random_forest', create_random_forest_model(scoring_method)),
        ('xgboost', create_xgboost_model(scoring_method, max_runs))
    ]

    mushroom_model = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(),
        n_jobs=-1
    )
    return mushroom_model


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


@click.command(help="Mushroom model hyperparameter optimization")
@click.option("--max-runs-xgb", type=click.INT, default=15,
              help="Maximum number of runs xgboost to evaluate.")
@click.option("--metric", type=click.STRING, default="roc_auc",
              help="Metric to optimize on.")
@click.argument('training_data', type=click.Path(exists=True))
def cli_interface(training_data, max_runs_xgb, metric):
    features, y = dataset(training_data)
    mushroom_model = create_mushroom_model(metric, max_runs_xgb)

    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)
    mlflow.xgboost.autolog()

    with mlflow.start_run():
        mushroom_model.fit(X_train, y_train)

        y_pred = mushroom_model.predict(X_test)
        y_pred_proba = mushroom_model.predict_proba(X_test)

        loss = log_loss(y_test, y_pred_proba)
        acc = accuracy_score(y_test, y_pred)
        (rmse, mae, r2) = eval_metrics(y_test, y_pred)

        # log metrics
        mlflow.log_param('max-runs-xgb', max_runs_xgb)
        mlflow.log_param('metric', metric)
        mlflow.log_metric('log_loss', loss)
        mlflow.log_metric('accuracy', acc)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(mushroom_model, "model")


if __name__ == '__main__':
    cli_interface()
