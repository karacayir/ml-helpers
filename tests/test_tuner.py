import unittest

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer
from sklearn.model_selection import KFold, StratifiedKFold

from src.tuner import find_best_hyperparameters_with_optuna


class TestTuner(unittest.TestCase):
    def setUp(self):
        # Generate a sample classification dataset for testing
        self.X, self.y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)

        # Define the machine learning model to optimize
        self.model = LogisticRegression

        # Define the hyperparameter search space
        self.param_space = {"C": (0.1, 10.0), "solver": ["lbfgs", "liblinear"]}

        # Define the evaluation metric to optimize
        self.metric = "accuracy"

        # Define number of trials performed by Optuna
        self.n_trials = 4

    def test_find_best_hyperparameters_with_optuna(self):
        # Test if the returned best_params dictionary is not empty
        folds = KFold(n_splits=5, shuffle=True, random_state=42)
        best_params = find_best_hyperparameters_with_optuna(
            self.X, self.y, folds, self.param_space, self.metric, self.model, self.n_trials
        )
        self.assertTrue(len(best_params) > 0)

        # Test if the best_params dictionary contains only the keys specified in the param_space dictionary
        for key in best_params.keys():
            self.assertIn(key, self.param_space.keys())

        # Test if the hyperparameter search space is properly defined
        with self.assertRaises(ValueError):
            folds = KFold(n_splits=5, shuffle=True, random_state=42)
            invalid_param_space = {"C": "invalid_param_value", "solver": ["lbfgs", "liblinear"]}
            find_best_hyperparameters_with_optuna(
                self.X, self.y, folds, invalid_param_space, self.metric, self.model, self.n_trials
            )

        # Test if the evaluation metric is properly defined
        with self.assertRaises(ValueError):
            folds = KFold(n_splits=5, shuffle=True, random_state=42)
            invalid_metric = "invalid_metric_name"
            find_best_hyperparameters_with_optuna(
                self.X, self.y, folds, self.param_space, invalid_metric, self.model, self.n_trials
            )

        # Test if the function works with different types of cross-validation objects
        folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        best_params = find_best_hyperparameters_with_optuna(
            self.X, self.y, folds, self.param_space, self.metric, self.model, self.n_trials
        )
        self.assertTrue(len(best_params) > 0)

        # Test if the function works with a callable metric
        def custom_metric(y_true, y_pred):
            return np.mean(np.abs(y_true - y_pred))

        scorer = make_scorer(custom_metric, greater_is_better=False)
        folds = KFold(n_splits=5, shuffle=True, random_state=42)
        best_params = find_best_hyperparameters_with_optuna(
            self.X, self.y, folds, self.param_space, scorer, self.model, self.n_trials
        )
        self.assertTrue(len(best_params) > 0)
