import os
import sys

import pandas as pd
from sklearn.model_selection import KFold
from datetime import datetime, timedelta
import numpy as np
import django

from auto_learning.hyp_param_search import HypParamSearch
from auto_learning.models import REGRESSION_MODELS

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from realestate.models import Rentproperty

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DB = os.environ['POSTGRES_DB']

ID = ['property_id']
X_COLS = ['close_station', 'floor_plan', 'area', 'age', 'floor', 'latitude', 'longititude', 'bath_toilet', 'auto_lock']
Y_COL = ['rent']


class PredictRent:
    def _get_all_today(self, address):
        """今日のaddress(区)に該当する物件情報をpandas dataframeにして取得"""
        last_record = Rentproperty.objects.order_by("-date").first()
        year = last_record.date.year
        month = last_record.date.month
        day = last_record.date.day
        start = datetime(year, month, day)
        end = start + timedelta(days=1)
        rp_all = Rentproperty.objects.filter(location__contains=address).filter(date__range=(start, end)).all().values()
        df = pd.DataFrame(list(rp_all))
        return df

    def predict(self, address):
        """return: diff, predicted_rent
        """
        df = self._get_all_today(address)
        df_sel = df[ID+X_COLS+Y_COL]
        df_sel = df_sel.dropna()
        id_df = df_sel[ID]
        x_df = df_sel[X_COLS]
        y_df = df_sel[Y_COL]
        x_df = pd.get_dummies(x_df)

        kf = KFold(n_splits=3)
        index = np.arange(y_df.shape[0])

        diff_list = []
        prediction_list = []
        id_list = []
        for train_index, test_index in kf.split(index):
            x_train = x_df.values[train_index]
            x_test = x_df.values[test_index]
            y_train = y_df.values.flatten()[train_index]
            y_test = y_df.values.flatten()[test_index]
            id_train = id_df.values.flatten()[train_index]
            id_test = id_df.values.flatten()[test_index]

            feature_selection = 'None'
            crossval_type = 'kfold'
            search_type = 'brute'
            metrics = 'r2'
            problem_type = 'regression'

            func = REGRESSION_MODELS['svr']
            est, params = func()
            hyp = HypParamSearch(x_train,
                                 y_train,
                                 x_test,
                                 y_test,
                                 est,
                                 problem_type,
                                 feature_selection,
                                 params,
                                 crossval_type,
                                 search_type,
                                 metrics)
            y_test_list, y_test_predicted_list, val_score, test_score, est = hyp.hyp_param_search()
            diff = y_test_predicted_list - y_test_list

            diff_list.extend(diff.tolist())
            prediction_list.extend(y_test_predicted_list.tolist())
            id_list.extend(id_test.tolist())
        
        diff_array = np.array(diff_list)
        prediction_array = np.array(prediction_list)
        id_array = np.array(id_list)

        return diff_array, prediction_array, id_array

    def insert_db_diff_prediction(self, diff_list, prediction_list, id_list):
        for diff, prediction, property_id in zip(diff_list, prediction_list, id_list):
            rp = Rentproperty.objects.get(property_id=int(property_id))
            rp.predicted_rent = float(prediction)
            rp.rent_diff = float(diff)
            rp.save()
        print('Update is completed')


if __name__ == '__main__':
    pr = PredictRent()
    diff_array, prediction_array, id_array = pr.predict('足立区')
    pr.insert_db_diff_prediction(diff_array, prediction_array, id_array)