# coding=utf-8

# import sys
import traceback
from sklearn.externals import joblib

'''ROC'''


def ROC(model, strategy, predict_y, target, log_path, thresholds=None, C=0.0, P=""):
    if thresholds is None:
        thresholds = [0.50]
    joblib.dump(predict_y, 'predict_y')
    joblib.dump(target, 'target')
    threshold_ks = {}
    fout = open(log_path, "a")
    try:
        for threshold in thresholds:
            TP, FN, FP, TN, positive = 0, 0, 0, 0, 0
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
            # print(TP, TN, FP, FN, TP+TN+FP+FN)
            KS_Value = (float(TP) / positive if positive != 0 else 0) - (float(FP)/(len(target) - positive) if len(target) - positive != 0 else 0)
            fout.write("Model=%s strategy=%s P=%s C=%f TP=%d TN=%d FP=%d FN=%d threshold=%f Positive=%d Negative=%d "
                       "Accuracy=%.4f"
                       " precision=%.4f TPR(recall)=%.4f FPR=%.4f KS_Value=%.4f\n" %
                       (model, str(strategy), P, C, TP, TN, FP, FN, threshold, positive, len(target) - positive, float(TP + TN) / len(target),
                        float(TP)/(TP+FP) if TP+FP != 0 else 0,
                        float(TP) / positive if positive != 0 else 0,
                        float(FP)/(len(target) - positive) if len(target) - positive != 0 else 0,
                        KS_Value))
            threshold_ks[threshold] = KS_Value
        threshold_ks = sorted(threshold_ks.items(), key=lambda d: d[1], reverse=True)
        fout.write(strategy+str(threshold_ks)+"\n")
        fout.close()
    except:
        traceback.print_exc()
        pass


if __name__ == '__main__':
    thresholds = [x/100 for x in range(100)]
    ROC('LR', joblib.load('../OfflineBuilder/predict_y'), joblib.load('../OfflineBuilder/target'), thresholds=thresholds)