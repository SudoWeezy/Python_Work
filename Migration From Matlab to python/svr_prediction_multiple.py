
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor


# Create a random dataset

def svr_prediction(_input, _output, train):
    X = _input
    y = _output

#    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= train)
#
#    max_depth = train
    regr_multirf = MultiOutputRegressor(RandomForestRegressor())
    regr_multirf.fit(X, y)

    regr_rf = RandomForestRegressor()
    regr_rf.fit(X, y)

    # Predict on new data
#    y_multirf = regr_multirf.predict(X_test)
#    y_rf = regr_rf.predict(X_test)
    return(regr_rf)
# Plot the results
#fig = plt.figure()
#
#ax_best = fig.add_subplot(111, projection='3d')
#ax_best.scatter(y_test[:, 0], y_test[:, 1], y_test[:, 2], c = 'r', label="Test")
#ax_best.scatter(y_multirf[:, 0], y_multirf[:, 1], y_multirf[:, 2], c = 'g', label="multiRf prevision")
#ax_best.scatter(y_rf[:, 0], y_rf[:, 1], y_rf[:,2], c = 'b', label="Rf prevision")
#ax_best.set_xlabel('indicator_step')
#ax_best.set_ylabel('low_trigger')
#ax_best.set_zlabel('high_trigger')
#plt.title("Comparing random forests and the multi-output meta estimator")
#plt.legend()
#plt.show()
