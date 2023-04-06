'''
Created on 20 Aug 2020

@author: w
'''
from tool.Tools import Tools
# 
# s = ["AlwaysTutorAndLearn", "HCR"]
# ss = str(s)
# print(Tools.convertToFigName(ss))
# [0.03, 0.03, 0.94] [0.1, 0.1, 0.8] [0.16, 0.16, 0.68]
res = Tools.randomPartition(30, [0.16, 0.16, 0.68])
print(res)

# ap_stat = {(0,0):0, (0,1):0, (1,0):0, (1,1):0}
# print ap_stat
# 
# ap_stat[(0,0)] += 1
# ap_stat[(0,0)] += 1
# 
# ap_stat[(1,0)] += 1
# print ap_stat

# episode_dynamics = [0.6,0.7,0.8,0.9]
# print(np.mean(episode_dynamics[-1-3:-1]))

# episode_dynamics = [[1,0.7,3]
#                     ,[2,0.8,4]
#                     ,[3,0.9,5]
#                     ,[4,0.99,6]
#                     ]
# 
# def checkCvgByLatestProp(episode_dynamics, m):
#     prop_list = []
#     for i in range(0, m):
#         latest_index = i - m
# #         print(latest_index)
#         prop_list.append(episode_dynamics[latest_index][1])
#     print(prop_list, np.mean(prop_list), np.mean(prop_list) >= 0.9)
#     return np.mean(prop_list) >= 0.9
# check = episode_dynamics[-4]
# print(check)
# 
# checkCvgByLatestProp(episode_dynamics, 4)

# 
# a=np.zeros(3)
# a[0]+=1
# print(a,max(a))

# print( ExpUtils.getExpHomoDmNameList())
# g = PCG(5)
# print(g.action_list)
# print(g.action_num)
# print(g.row_payoff_matrix)
# print(g.col_payoff_matrix)

# print(1.71==1.71)
# im = Image.open("1.png")
# im = im.convert('RGB')
# # print(im.getbbox())
# bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
# # print(bg.getbbox())
# diff = ImageChops.difference(im, bg)
# diff = ImageChops.add(diff, diff, 2.0, -100)
# bbox = diff.getbbox()
# print(diff)
# print(bbox)

# if bbox:
#     return im.crop(bbox)

# # l = {"name1":["dd","sf"], "name2":["safdsf"]}
# l = {"listing_ass_adopted":["WSLS","ImitateBestNeighbor"]
#         }
# # s = ",".join(str(i) for i in l)
# sl =[]
# for k, vals in l.items():
#     s = " AND ".join("%s NOT LIKE \"%%%s%%\"" % (k, v) for v in vals)
#     sl.append(s)
# #     print (s)
# print (" AND ".join(sl))

# s = " AND ".join("%s NOT LIKE \"%%%s%%\"" % (k, v) for v in vals for k, vals in l.items())
# print (s)
# s = ",".join((k, v) )
# print(s)

# list2d = [[1,2,3]
#         , [2,5,6]]
# list2d_2 = [[1,4,5]
#         , [2,6,7]]
# v_under_keyn_list = [list2d, list2d_2]
# m = np.mean(v_under_keyn_list, axis = 0)
# print(m)
# list2d = np.asarray(list2d)
#
# print(list2d[:,1:3])

# ac_freq = {(0, 0):0
#                    , (0, 1):0
#                    , (1, 0):0
#                    , (1, 1):0
#                    }
# print(ac_freq)
# a = (0, 0)
# ac_freq[a] += 1
# print(ac_freq)
#
# print(list(ac_freq.values()))
# a=[i for i in range(10)]
# print(a)

# print(os.listdir(ROOT_DIR+"/action_selection"))

# a=[1,2,3]
# b = [i for i in a]
# print(b, max(b))
# print(2/4)

# l = np.zeros(2)
# l = [0] * 2
# l[0] += 1
# l[0] += 1
# l[1] += 1
# l.clear()
# print(l)
# Tools.randomPartition(9, [0.4, 0.6])
# print(Tools.randomPartition(11, [0.1, 0.2, 0.3, 0.4]))

# l = [1, 2, 3]
# print(l)
#
# l.clear()
# print(l)

# sw = Smallworld(30, 3, 0.5)
# sw.draw()
# print sw.nodeNumber(), len(sw.G.nodes), sw.G.nodes

# pairs = sw.concurrentInteractionPairsInEpisode()
# print (pairs)

# g = IntersectionGame()
# print(g.action_set)
#
# fa = FixedAgent(g)
#
# print (fa.game, fa.neighbors, fa.rowAction())
