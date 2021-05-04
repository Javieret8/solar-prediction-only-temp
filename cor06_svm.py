import pickle
import pandas as pd
import numpy as np
import StatsFunctions as stats
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

class cor06_svm():
    """
    This class represents the best model/configuration from Córdoba (RIA station).
    
    It uses a SVM model and the following input configuration (being rs the predicted value):
        ['tx', 'tn', 'ra', 'deltat', 'energyt', 'hormintx', 'tx_prev', 'tn_next', 'rs']

    """
    def __init__(self):
        # import model
        filename = "models/svm_cor06_Tx_Tn_Ra_deltaT_EnergyT_HorminTx_Tx_prev_Tn_next_Rs.sav"
        with open(filename, 'rb') as file:
            self.model = pickle.load(file)

        # define required inputs
        self.parameters = ['tx', 'tn', 'ra', 'delta_t', 'energyt', 'hormin_tx', 'tx_prev', 'tn_next', 'rs']

    def import_dataset(self, fileLocation, fileType):
        """
        This function import a dataset and convert it into a pandas Dataframe
        Inputs:
            fileLocation: "data/dataSet.csv"
            fileType: string with csv, excel or txt
        """
        if fileType == 'csv' or fileType == 'txt':
            self.dfData = pd.read_csv(fileLocation)
        elif fileType == 'excel':
            self.dfData = pd.read_excel(fileLocation)
        else:
            AssertionError('this fileType does not exit, use excel, csv and txt instead')

        # filter nan values
        self.dfData.dropna(inplace=True)
        self.dfData.reset_index(drop=True, inplace=True)
        # filter the parameters
        self.dfData = self.dfData.filter(self.parameters)

    def getStandardDataTest(self):
        """
        Split data to train and test
        """
        # from training original dataset
        mean_list = [24.42, 11.03, 28.78, 13.38, 402.95, 15.20, 24.42, 11.02]
        std_list = [8.54, 6.26, 9.64, 4.578, 177.87, 1.78, 8.53, 6.27]

        # we have the input data as x, and the output as y
        self.x_test = np.array(self.dfData.iloc[:, :-1])
        self.y_test = np.array(self.dfData.iloc[:, -1])

        # standarization
        scaler = StandardScaler()
        scaler.mean_ = mean_list
        scaler.scale_ = std_list

        # x_train and x_test
        self.x_test = np.array(scaler.transform(self.x_test))

        return self.x_test, self.y_test

    def predictValues(self):
        self.y_pred = np.array(self.model.predict(self.x_test))
        return self.y_pred

    def statAnalysis(self):
        rmse = stats.get_root_mean_square_error(self.y_test, self.y_pred)
        rrmse = stats.get_root_mean_square_error(self.y_test, self.y_pred) / np.mean(self.y_test)
        mbe = stats.get_mean_bias_error(self.y_test, self.y_pred)
        r2 = stats.get_coefficient_of_determination(self.y_test, self.y_pred)
        nse = stats.get_nash_suteliffe_efficiency(self.y_test, self.y_pred)

        return rmse, rrmse, mbe, r2, nse

if __name__ == '__main__':
    mlModel = cor06_svm()
    mlModel.import_dataset("data/data-daily-asheville-example.csv", 'csv')
    mlModel.getStandardDataTest()
    mlModel.predictValues()
    rmse, rrmse, mbe, r2, nse = mlModel.statAnalysis()
    print(rmse, rrmse, mbe, r2, nse)