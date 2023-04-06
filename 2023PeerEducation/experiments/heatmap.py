

import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from tool.Tools import Tools


# uniform_data = np.random.rand(30, 100)
# print uniform_data
# data  = np.loadtxt('[G_ba,SL_sl_ALLN,acNum_2,agNum_30,episodes_1,le_Wolf]_rep0.csv',dtype=str,delimiter=',')
# data = Tool.readCSVAsFloat('[G_ba,SL_d,acNum_2,agNum_30,episodes_5,le_Wolf]_rep0.csv')
data = Tools.readCSVAsFloat('[G_ba,SL_sl_ALLN,acNum_2,agNum_30,episodes_1,le_Wolf]_rep0.csv')



ax = sns.heatmap(data, square=True)

# ax = sns.heatmap(uniform_data, square=True)

plt.show()
