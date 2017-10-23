# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
from sklearn.externals import joblib

'''ROC'''


def ROC(model, predict_y, target, threshold=0.5, C=0.0, P=""):
    joblib.dump(predict_y, 'predict_y')
    joblib.dump(target, 'target')
    TP, FN, FP, TN = 0, 0, 0, 0
    positive = 0
    try:
        for i in range(len(target)):
            positive += 1 if target[i] == 1 else 0
            if threshold < predict_y[i]:
                if target[i] == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if target[i] == 0:
                    TN += 1
                else:
                    FN += 1
        print "Model=%s P=%s C=%f TP=%d TN=%d FP=%d FN=%d Positive=%d\n Negative=%d Accuracy=%.4f precision=%.4f " \
              "TPR(sensitivity, recall)=%.4f FPR(1-specificity)=%.4f TNR=%.4f FNR=%.4f" % \
              (model, P, C, TP, TN, FP, FN, positive, len(target) - positive, float(TP + TN) / len(target),
               float(TP)/(TP+FP) if TP+FP != 0 else 0,
               float(TP) / positive if positive != 0 else 0,
               float(FP)/(len(target) - positive) if len(target) - positive != 0 else 0,
               float(TN) / (len(target) - positive) if len(target) - positive != 0 else 0,
               float(FN)/positive if positive != 0 else 0)
    except:
        traceback.print_exc()
        pass


if __name__ == '__main__':
    ROC('LR', joblib.load('predict_y'), joblib.load('target'))