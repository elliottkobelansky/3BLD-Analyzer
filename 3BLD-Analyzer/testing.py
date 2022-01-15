import solve
import pandas as pd
from scipy import stats
import numpy as np
import re
from sklearn import linear_model, model_selection, metrics


def main():
    df = pd.read_csv("tomisession.csv")
    data = df.values.tolist()
    for x in data:
        try:
            x[0] = float(x[0])
        except:
            x[0] = -1 if "+" not in x[0] else float(x[0][:-1])

    data = [[x[0], solve.solve(x[1])] for x in data if x[0] != -1 and x[0] < 20]
    y = np.array([float(x[0]) for x in data])
    data = np.array([x[1] for x in data])
    bruh = np.array(solve.solve("F' R2 F2 D2 F U2 L2 U2 L2 B' L D' F' U' L B' F U")).reshape(1, -1)
    combined = np.column_stack([y, data])

    X_train, X_test, y_train, y_test = model_selection.train_test_split(data, y, test_size = 0.05)
    reg = linear_model.LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    deltas = y_test - y_pred
    for x, y, z in zip(y_test, y_pred, deltas):
        print(x, round(y, 2), round(z, 1))
    print(reg.coef_)
    print(metrics.mean_squared_error(y_test, y_pred))
    print(metrics.mean_absolute_error(y_test, y_pred))
    
if __name__ == "__main__":
    main()
