import numpy as np


class DBDO:
    
    @staticmethod
    def putTgtColTogetherInMultipleResults(list2d_list
                   , tgt_col):
#         print list2d_list
        list2d_list = np.asarray(list2d_list)
        res_list = []
        for trial in list2d_list:
#             print Tools.dim(trial)
#             print trial
#             print Tools.dim(trial)
            if len(res_list) == 0:  # add column of x-axis
                res_list.append(trial[0:len(trial), 0])

            res_list.append(trial[0:len(trial), tgt_col])

        return np.array(res_list).T.tolist()