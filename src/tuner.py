import numpy as np
import optuna
from sklearn.model_selection import cross_val_score


def find_best_hyperparameters_with_optuna(X, y, folds, param_space, metric, model, n_trials):
    """
    Uses Optuna to find the best hyperparameters for a machine learning model.

    Parameters:
        X: The input data for the machine learning model.
        y: The target data for the machine learning model.
        folds (int or sklearn.model_selection._BaseKFold): The number of folds to use in cross-validation, or an instance
            of a KFold or StratifiedKFold object.
        param_space (dict): A dictionary specifying the hyperparameter search space for the model.
        metric (str or callable): The name of the evaluation metric to optimize, or a callable object that takes two
            arguments (true labels and predicted labels) and returns a scalar value.
        model: The machine learning model to optimize.
        n_trials (int): Number of trials will be performed by Optuna.

    Returns:
        A dictionary of the best hyperparameters found by the hyperparameter search.
    """

    def objective(trial):
        # Get parameter values from the Optuna study
        param_values = {}
        for name, search_space in param_space.items():
            if isinstance(search_space, tuple):
                # For numerical parameters, sample from a uniform distribution
                low, high = search_space
                if all([isinstance(item, int) for item in [low, high]]):
                    param_values[name] = trial.suggest_int(name, low, high)
                else:
                    param_values[name] = trial.suggest_float(name, low, high)
            elif isinstance(search_space, list):
                # For categorical parameters, choose one of the values
                param_values[name] = trial.suggest_categorical(name, search_space)
            else:
                raise ValueError(f"Invalid search space type for hyperparameter {name}")

        # Train and evaluate the model with cross-validation
        scores = cross_val_score(model(**param_values), X, y, cv=folds, scoring=metric)
        return np.mean(scores)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    return study.best_params
