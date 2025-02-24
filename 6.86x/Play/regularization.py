import numpy as np
import pandas as pd

from sklearn import linear_model

# Demonstrate that auto-correlated predictor variables dilute the Linear Regression coefficients
# Because the predictor values are 100x larger when measured in cm, they are considered more important by 100x in the model
def auto_correlated():
    df = pd.DataFrame()
    df['x0'] = np.arange(-10, 10.1, 0.1)
    df['x1'] = df.x0 / 100  # x1 is x0 converted from centimeters to meters
    df['y'] = 2 * df.x0 + 0.5
    df['y1'] = df.y + np.random.standard_normal(df.y.shape)


    model = linear_model.LinearRegression()
    model.fit(df[['x0']], df.y)
    print(f'\n{model} base model on x0 (unseen x measured in cm):')
    print(f'\ty = {model.coef_[0]:0.4} x0')


    model = linear_model.LinearRegression()
    model.fit(df[['x1']], df.y)
    print(f'\n{model} base model on x1 (unseen x measured in m):')
    print(f'\ty = {model.coef_[0]:0.4} x1')


    model = linear_model.LinearRegression()
    model.fit(df[['x0', 'x1']], df.y)
    print(f'\n{model} with auto-correlated predictors:')
    print(f'\ty = {model.coef_[0]:0.4} x0 + {model.coef_[1]:0.4} x1, coefficient ratio x0/x1: {np.inf if model.coef_[1]==0 else model.coef_[0] / model.coef_[1]:0.4}')

    model = linear_model.Lasso()
    model.fit(df[['x0', 'x1']], df.y)
    print(f'\n{model} with auto-correlated predictors:')
    print(f'\ty = {model.coef_[0]:0.4} x0 + {model.coef_[1]:0.4} x1, coefficient ratio x0/x1: {np.inf if model.coef_[1]==0 else model.coef_[0] / model.coef_[1]:0.4}')


if __name__ == '__main__':
    auto_correlated()
