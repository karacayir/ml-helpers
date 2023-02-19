import optuna
import numpy as np
from sklearn.model_selection import cross_val_score


def find_best_hyperparameters_with_optuna(data, folds, param_space, metric, model):

    """
    Uses Optuna to find the best hyperparameters for a machine learning model.

    Parameters:
        data: The input data for the machine learning model.
        folds (int or sklearn.model_selection._BaseKFold): The number of folds to use in cross-validation, or an instance
            of a KFold or StratifiedKFold object.
        param_space (dict): A dictionary specifying the hyperparameter search space for the model.
        metric (str or callable): The name of the evaluation metric to optimize, or a callable object that takes two
            arguments (true labels and predicted labels) and returns a scalar value.
        model: The machine learning model to optimize.

    Returns:
        A dictionary of the best hyperparameters found by the hyperparameter search.
    """

    def objective(trial):
        # Get parameter values from the Optuna study
        param_values = {name: trial.suggest_uniform(name, low, high) for name, (low, high) in param_space.items()}

        # Train and evaluate the model with cross-validation
        scores = cross_val_score(model(**param_values), data, cv=folds, scoring=metric)
        return np.mean(scores)

    study = optuna.create_study()
    study.optimize(objective, n_trials=100)

    return study.best_params
