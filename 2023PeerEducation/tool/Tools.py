from __future__ import division

import random
import math
import csv
import os
import datetime
import operator
from collections import Counter
from queue import Queue

import numpy as np
import pickle
import ast
import platform
import re
import copy
from ast import literal_eval


class Tools:

    @staticmethod
    def convertToFigName(s):
        s = str(s)
        return s.replace("]","").replace("[","").replace(",","_").replace(" ", "").replace("'","")
    
    @staticmethod
    def getOthersInList(_list, v):
        new_l = []
        for e in _list:
            if e != v:
                new_l.append(e)
        return new_l

    @staticmethod
    def createFileDirIfNotExist(filename):
        if os.path.dirname(filename) != "":
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != exc.EEXIST:
                        raise

    @staticmethod
    def bstr_to_valuestr(list2d):
        return literal_eval(list2d.decode())

    @staticmethod
    def removeNoneValueKeys(_dict):
#         print(_dict)
        for key in _dict.keys():
            if _dict[key] == None:
                _dict.pop(key)

    @staticmethod
    def testVarAdd(random_number):
        dice = range(6)
        d1_list = []
        d2_list = []
        for _ in range(random_number):
            d1_list.append(random.choice(dice))
            d2_list.append(random.choice(dice))

#         print d1_list
#         print d2_list
        d1_list = np.array(d1_list)
        d2_list = np.array(d2_list)
        d1_add_d2 = d1_list + d2_list
        d1_mi_d2 = d1_list - d2_list
#         print d1_add_d2
#         print d1_mi_d2
        var1 = np.var(d1_list, axis = 0, ddof = 1)
        var2 = np.var(d2_list, axis = 0, ddof = 1)

#         print var1 + var2, var1 + var2 + np.cov(d1_list, d2_list)[0][1], np.var(d1_add_d2, axis = 0, ddof = 1), np.var(d1_mi_d2, axis = 0, ddof = 1)

    @staticmethod
    def getCovariance(x, y):
        mean_x = np.mean(x, axis = 0)
        mean_y = np.mean(y, axis = 0)

        n = len(x)
#         print mean_x, mean_y
        joint_vary_list = []
        for i in range(n):
            x_e = x[i]
            y_e = y[i]
            joint_vary_list.append((x_e - mean_x) * (y_e - mean_y))
#         print joint_vary_list
        return np.sum(joint_vary_list, axis = 0) / (n - 1)

    @staticmethod
    def getVariance(l):
        mean = np.mean(l, axis = 0)
        sq_dis_to_mean_list = []
        for e in l:
            sq_dis_to_mean_list.append(math.pow(e - mean, 2))
        return np.mean(sq_dis_to_mean_list, axis = 0)

    @staticmethod
    def appendDynamicsWithLastValue(dynamics, append_number):
        lastvalue = dynamics[-1]
        added_episode = lastvalue[0] + 1
        for _ in range(append_number):
            added_lastvalue = copy.copy(lastvalue)
            added_lastvalue[0] = added_episode  # episode + 1
            dynamics.append(added_lastvalue)
            added_episode += 1
        return dynamics

    @staticmethod
    def makeRepeatedDynamicsSameLen(dynamics_list):
        max_len = -1
        for dynamics in dynamics_list:
            if len(dynamics) > max_len:
                max_len = len(dynamics)

        for dynamics in dynamics_list:
            append_number = max_len - len(dynamics)
            Tools.appendDynamicsWithLastValue(dynamics, append_number)
#             print len(dynamics)
        return dynamics_list

    @staticmethod
    def meanRepeats(_list):
        mean_res = {}
#         for e in _list:
#             print(e)
#         print(_list)
        mean_v = np.mean(_list, axis = 0)
        dim_mean_res = Tools.dim(mean_v)
#             print(mean_res)
#             print(dim_mean_res)
#             print(type(dim_mean_res) == list)
        if len(dim_mean_res) == 1:
#                 print(mean_v)
            mean_res["_mean"] = Tools.to1dList(mean_v)
        elif len(dim_mean_res) == 2:
            mean_res["_mean"] = Tools.to2dList(mean_v)
        else:
            assert False
        
        mean_res["_std"] = np.std(_list, axis = 0)
        return mean_res

    @staticmethod
    def meanDictRepeats(dict_list):
        """
            dict_list = [{"name":value1}, {"name":value2},...]
        """
        assert len(dict_list) > 0
        key_names = dict_list[0].keys()
        mean_res = {}
        for keyn in key_names:
#             print keyn
            v_under_keyn_list = []
            for _dict in dict_list:
                v_under_keyn_list.append(_dict[keyn])
#             print len(v_under_keyn_list), v_under_keyn_list
            if len(Tools.dim(v_under_keyn_list)) == 3:
                Tools.makeRepeatedDynamicsSameLen(v_under_keyn_list)
#             print(v_under_keyn_list)
            mean_v = np.mean(v_under_keyn_list, axis = 0)
            dim_mean_res = Tools.dim(mean_v)
#             print(mean_res)
#             print(dim_mean_res)
#             print(type(dim_mean_res) == list)
            if len(dim_mean_res) == 1:
#                 print(mean_v)
                mean_res[keyn + "_mean"] = Tools.to1dList(mean_v)
            elif len(dim_mean_res) == 2:
                mean_res[keyn + "_mean"] = Tools.to2dList(mean_v)
            else:
                assert False
#             print(mean_res[keyn + "_mean"])
#             print(len(mean_res[keyn + "_mean"]))
            mean_res[keyn + "_std"] = np.std(v_under_keyn_list, axis = 0)
        return mean_res

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

    @staticmethod
    def to1dList(list1d):
        new_list1d = []
        for row_data in list1d:
            new_list1d.append(row_data)
        return new_list1d

    @staticmethod
    def to2dList(list2d):
        new_list2d = []
        for row_data in list2d:
            new_row = []
            for data in row_data:
                new_row.append(data)
            new_list2d.append(new_row)
        return new_list2d

    @staticmethod
    def messageBoxYN(message, func):
        while True:
            yn = input("%s [y/n]" % (message))
            if re.findall("^[Nn]$", yn):
                break
            elif re.findall("^[Yy]$", yn):
                func()
                break
            else:
                print ("Please input [y/n].")

    @staticmethod
    def messageBoxYNConti(message):
        while True:
            yn = input("%s [y/n]" % (message))
            if re.findall("^[Nn]$", yn):
                return False
            elif re.findall("^[Yy]$", yn):
                return True
            else:
                print ("Please input [y/n].")

    @staticmethod
    def isMyMacBook():
        osname = platform.system()
        if osname == "Darwin":
            return True

    @staticmethod
    def evaltuple(_tuple):
        if isinstance(_tuple, str):
            _tuple = ast.literal_eval(_tuple)
        return _tuple

    @staticmethod
    def getDivisibleList(num):
        divisible_list = []
        sq = math.sqrt(num)

        i = 0
        while i <= sq:
            i += 1
            if num % i == 0:
                divisible_list.append(i)
        return divisible_list

    @staticmethod
    def getPercentile(l, degree):
        max_i = -1
        min_i = -1
        length = len(l)
        for i in range(length):
            if degree == l[i]:
                if min_i == -1:
                    min_i = i
                    max_i = i
                else:
                    max_i = i

        return ((min_i + 1) + (max_i + 1)) / (2 * length)

    @staticmethod
    def dim(l):
        if type(l) != list and type(l) != np.ndarray:
            return []
        return [len(l)] + Tools.dim(l[0])

    @staticmethod
    def unionList(l1, l2):
        return list(set(l1).union(l2))

    @staticmethod
    def intersectionList(l1, l2):
        return list(set(l1).intersection(l2))

    @staticmethod
    def argmaxAllIndexes(l):
        indexes = np.argwhere(l == np.max(l))
        results = []
        for i in indexes:
            results.append(i[0])
        return results

    @staticmethod
    def isclose(a, b, rel_tol = 1e-09, abs_tol = 0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    @staticmethod
    def fixedPartition(total_num, proportion_list):

        assert Tools.isclose(np.sum(proportion_list), 1)
        index_list = list(range(total_num))
        ready = [[6], [6, 7, 11], [6, 7, 11, 12, 16], [6, 7, 11, 12, 16, 17, 21]]
        result_list = []
        x = []
        sum = int ((round(proportion_list[1] * len(index_list)) - 1) / 2)
        for i in range(len(index_list)):
            if i in ready[sum]:
                pass
            else:
                x.append(i)
        result_list.append(x)
        result_list.append(ready[sum])
        print(result_list)
        return result_list

    @staticmethod
    def randomPartition(total_num, proportion_list):
        """
            example:
            total_num = [0, 1, 2, 3, 4, 5, 6,7,8]
            proportion_list = [0.4, 0.6]
            -> [[2, 0, 4, 6], [3, 5, 7, 8, 1]]
        """
        assert Tools.isclose(np.sum(proportion_list), 1)

        index_list = list(range(total_num))
        random.shuffle(index_list)
        result_list = []
        start = 0
        for idx, p in enumerate(proportion_list):
            if idx == len(proportion_list) - 1:
                end = len(index_list)
            else:
                end = start + round(p * len(index_list))
            result_list.append(index_list[start:end])
            start = end
#         print(result_list)

        return result_list

    """
        memory-saving code, leave for future work
    """
#         partition_size_list = []
#         sum_partition_size = 0
#         for idx, prop in enumerate(proportion_list):
#             if idx == len(proportion_list) - 1:
#                 partition_size_list.append(total_num - sum_partition_size)
#             else:
#                 partition_size = round(prop * total_num)
#                 partition_size_list.append(partition_size)
#                 sum_partition_size += partition_size
#         print(partition_size_list)
#
#         result_list = []
#
#         for _id in range(total_num):
#
#         for partition_size in partition_size_list:
#             partition_list = []
#             for _ in range(partition_size):

    @staticmethod
    def partitionByProportion(list_in, proportionList):
        '''
            example:
            list_in = [0, 1, 2, 3, 4, 5, 6,7,8]
            proportionList = [0.4, 0.6]
            
            -> [[2, 0, 4], [3, 5, 7, 8, 1, 6]]
        '''
#         print proportionList
        assert Tools.isclose(np.sum(proportionList), 1)
        random.shuffle(list_in)  # do not do like this later
        resultList = []
        start = 0
        for idx, p in enumerate(proportionList):
            if idx == len(proportionList) - 1:
                end = len(list_in)
            else:
                end = start + int(p * len(list_in))
            resultList.append(list_in[start:end])
            start = end
        return resultList

    @staticmethod
    def writeStringToFile(s, path):
        f = open(path, "w")
        f.write(s)
        f.close()

    @staticmethod
    def read_text(filename):
        with open(filename, 'r') as file:
            return file.read()

    @staticmethod
    def getRandomAndThenDel(l):
        length = len(l)
        assert length > 0
        index = random.randint(0, length - 1)
        element = l[index]
        del l[index]
        return element

    @staticmethod
    def getFunctionName(fun):
        fstr = fun.__str__()
        return fstr.split(' ')[1]

    @staticmethod
    def matrixAddFor2DList(l1, l2):
        assert len(l1) > 0 and len(l2) > 0
        assert len(l1[0]) > 0 and len(l2[0]) > 0
        assert len(l1) == len(l2)
        assert len(l1[0]) == len(l2[0])

        row = len(l1)
        column = len(l1[0])

        res = []
        for i in range(0, row):
            rowData = []
            for j in range(0, column):
                rowData.append(l1[i][j] + l2[i][j])
            res.append(rowData)
#         print res
        return res

    @staticmethod
    def matrixDivFor2DList(l, d):
        assert len(l) > 0
        assert len(l[0]) > 0.

        row = len(l)
        column = len(l[0])
        res = []
        for i in range(0, row):
            rowData = []
            for j in range(0, column):
                rowData.append(l[i][j] / d)
            res.append(rowData)
#         print res
        return res

    @staticmethod
    def createDir(filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != exc.EEXIST:
                    raise

    @staticmethod
    def saveCsv(filename = None, csv_list = None):
        if os.path.dirname(filename) != "":
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != exc.EEXIST:
                        raise

        with open(filename, 'w')  as f:
            writer = csv.writer(f)
            writer.writerows(csv_list)

    @staticmethod
    def merge_two_dicts(x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z

    @staticmethod
    def readCSVAsFloat(path):
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            dy = list(reader)
        dy = [[float(y) for y in x] for x in dy]  # convert to float
#         print dy
        return dy

    @staticmethod
    def merge_2csv_by_row(filename1, filename2, res_name):
        csv1 = Tools.readCSVAsFloat(filename1)
        csv2 = Tools.readCSVAsFloat(filename2)

        assert len(csv1) == len(csv2)
        for i in range(len(csv1)):
#             print row
            for j in range(len(csv2[i])):
                if j > 0:
                    csv1[i].append(csv2[i][j])
#         print csv1, res_name
        Tools.save2DList(res_name, csv1)

    @staticmethod
    def merge_2files_from_newrow(filename1, filename2, res_name):
        fin = open(filename1, "r")
        data1 = fin.read()
        fin.close()

        fin = open(filename2, "r")
        data2 = fin.read()
        fin.close()

        combined_data = data1 + data2
        fout = open(res_name, "w")
        fout.write(combined_data)
        fout.close()

    @staticmethod
    def saveText(text, filename):
        dir = os.path.dirname(filename)
        if dir != '' and not os.path.isdir(dir):
            os.makedirs(dir)
        with open(filename, 'w') as file:
            file.write(text)

    @staticmethod
    def getCurTimeStr():
        return datetime.datetime.now().strftime("%Y-%m-%d %H,%M,%S")

    @staticmethod
    def save_obj(obj, filename):
        dir = os.path.dirname(filename)
        if dir != '' and not os.path.isdir(dir):
            os.makedirs(dir)
        with open('' + filename + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_obj(name):
        with open('' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def getOther(e_list, e):
        other_list = []
        for el in e_list:
            if el != e:
                other_list.append(el)
        return other_list

    @staticmethod
    def findMost(l):
        Counter(l)
        if len(set(l)) == 1:
            result = Counter(l).most_common(1)[0][0]
        elif Counter(l).most_common(1)[0][1] == Counter(l).most_common(2)[1][1]:
            result = random.randint(0, 1)
        else:
            if Counter(l).most_common(1)[0][1] > Counter(l).most_common(2)[1][1]:
                result = Counter(l).most_common(1)[0][0]
            else:
                result = Counter(l).most_common(2)[1][0]
        return result

    @staticmethod
    def findQueueMost(queue):

        t = Queue()
        t.queue.clear()
        t = queue
        num = 0
        for i in range(t.qsize()):

            z = t.get()
            if z == 0:
                num = num + 1
            queue.put(z)

        if num > t.qsize()/2:
            result = 0
        elif num == t.qsize()/2:
            result = random.randint(0, 1)
        else:
            result = 1
        return result

    def findMostP(l):
        count = Counter(l)
        print(count)
        if len(set(l)) == 1:
            result = Counter(l).most_common(1)[0][0]
        elif Counter(l).most_common(1)[0][1] == Counter(l).most_common(2)[1][1]:
            result = random.randint(0, 1)
        else:
            sum = Counter(l).most_common(1)[0][1] + Counter(l).most_common(2)[1][1]
            flag = random.randint(0, sum-1)
            if Counter(l).most_common(1)[0][1] > Counter(l).most_common(2)[1][1]:
                if flag < Counter(l).most_common(1)[0][1]:
                    result = Counter(l).most_common(1)[0][0]
                else:
                    result = Counter(l).most_common(2)[1][0]
            else:
                if flag < Counter(l).most_common(2)[1][1]:
                    result = Counter(l).most_common(2)[1][0]
                else:
                    result = Counter(l).most_common(1)[0][0]
        print(result)
        return result
