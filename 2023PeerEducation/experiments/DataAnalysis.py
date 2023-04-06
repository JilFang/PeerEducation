
from tables.TTrailResultsView import TTrailResultsView
import numpy as np
from tool.Tools import Tools
from tool.DrawTools import DrawTools
import math


def nameMapping(assname):
    _dict = {"ImitateBestNeighbor": "IBN"
           , "QLearning":"SL"
           , "MostObserved":"MI"
           , "MostInLocal":"MN"
           , "AllRandom":"RA"
           , "Fixed":"FA"
           }
    if assname in _dict.keys():
        return _dict[assname]
    else:
        return assname


def ass_cvg_analysis():
    # T1 T2
    exp_name = "T2"
    # WSLS ImitateOppoAction HCR
    listing_ass_adopted = ["HCR"]

    game_name = "PCGLMoreHalf"
#     res = TTrailResultsView.getByExpNameAss(exp_name, listing_ass_adopted)
    res = TTrailResultsView.getByExpNameAssGame(exp_name
                                            , listing_ass_adopted, game_name)
    print(len(res))
    cvg_to_ja_count = [0, 0, 0, 0]
    for record in res:
        ep_dy = record["episode_dynamics"]
        last_epi_ja_dis = ep_dy[-1]

        ja00 = last_epi_ja_dis[1]
        ja01 = last_epi_ja_dis[2]
        ja10 = last_epi_ja_dis[3]
        ja11 = last_epi_ja_dis[4]

        if ja00 == 15:
            cvg_to_ja_count[0] += 1
        if ja01 == 15:
            cvg_to_ja_count[1] += 1
        if ja10 == 15:
            cvg_to_ja_count[2] += 1
        if ja11 == 15:
            cvg_to_ja_count[3] += 1
        print(last_epi_ja_dis)
#         print(ja00,ja01,ja10,ja11)

    print(cvg_to_ja_count)
    print(len(res))

"""
T1
cvg_to_ja_count
ImitateOppoAction:
[256, 232, 258, 254]

WSLS:
[0, 0, 0, 0]

HCR:
[537, 0, 0, 463]


T2:
HCR Teach Learn 2, 2
[919, 0, 0, 80]

HCR Teach Learn 1.5, 1.5
[819, 0, 0, 181]
"""


def fixed_beheavior_cvg_analysis():
    exp_name = "T3"
    # ImitateOppoAction WSLS HCR
    listing_ass_adopted = ["AlwaysTutorAndLearn", "WSLS"]
    game_name = "PCG"
    # [0.03,0.97] [0.1, 0.9] [0.16,0.84]
#     listing_ass_proportion = [0.16,0.84]
    listing_ass_proportion_list = [[0.03,0.97], [0.1, 0.9], [0.16,0.84]]
    for listing_ass_proportion in listing_ass_proportion_list:
        res = TTrailResultsView.getByExpNameAssGameProp(exp_name
                                                , listing_ass_adopted
                                                , game_name
                                                , listing_ass_proportion)
        print(len(res))
        cvg_to_ja_count = [0, 0, 0, 0]
        for record in res:
            ep_dy = record["episode_dynamics"]
            last_epi_ja_dis = ep_dy[-1]
    
            ja00 = last_epi_ja_dis[1]
            ja01 = last_epi_ja_dis[2]
            ja10 = last_epi_ja_dis[3]
            ja11 = last_epi_ja_dis[4]
    
            if ja00 == 15:
                cvg_to_ja_count[0] += 1
            if ja01 == 15:
                cvg_to_ja_count[1] += 1
            if ja10 == 15:
                cvg_to_ja_count[2] += 1
            if ja11 == 15:
                cvg_to_ja_count[3] += 1
    #         print(last_epi_ja_dis)
    #         print(ja00,ja01,ja10,ja11)
    
        print(listing_ass_adopted, listing_ass_proportion, cvg_to_ja_count)
        print(len(res))


"""

['AlwaysTutorAndLearn', 'ImitateOppoAction'] 
[0.03, 0.97] [1000, 0, 0, 0]
[0.1, 0.9] [1000, 0, 0, 0]
[0.16, 0.84] [1000, 0, 0, 0]

['AlwaysTutorAndLearn', 'WSLS']
[0.03, 0.97] [995, 0, 0, 0]
[0.1, 0.9] [1000, 0, 0, 0]
[0.16, 0.84] [1000, 0, 0, 0]

["AlwaysTutorAndLearn", "HCR"]
[0.03,0.97]: [778, 0, 0, 0]
[0.1, 0.9]: [977, 0, 0, 0]
[0.16,0.84]: [1000, 0, 0, 0]

"""


def fixed_oppo_beheavior_cvg_analysis():
    exp_name = "T4"
    game_name = "PCG"
    
    listing_ass_adopted_list = [["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "ImitateOppoAction"]
                                    , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "WSLS"]
                                    , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "HCR"]]
#     listing_ass_adopted_list = [["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "HCR"]]
    
    listing_ass_proportion_list = [[0.03, 0.03, 0.94], [0.1, 0.1, 0.8], [0.16, 0.16, 0.68]]
    
    ag_num = 30
    inter_num = 15
    
    for listing_ass_adopted in listing_ass_adopted_list:
        for listing_ass_proportion in listing_ass_proportion_list:
            res = TTrailResultsView.getByExpNameAssGameProp(exp_name
                                                , listing_ass_adopted
                                                , game_name
                                                , listing_ass_proportion)
            print(len(res))
            cvg_to_ja_count = [0, 0, 0, 0]
            for record in res:
                ep_dy = record["episode_dynamics"]
                last_epi_ja_dis = ep_dy[-1]
        
                ja00 = last_epi_ja_dis[1]
                ja01 = last_epi_ja_dis[2]
                ja10 = last_epi_ja_dis[3]
                ja11 = last_epi_ja_dis[4]
                
                cvg_threshold = inter_num - int(math.ceil(ag_num*listing_ass_proportion[0]))
#                 print(cvg_threshold)
                if ja00 == cvg_threshold:
                    cvg_to_ja_count[0] += 1
                if ja01 == cvg_threshold:
                    cvg_to_ja_count[1] += 1
                if ja10 == cvg_threshold:
                    cvg_to_ja_count[2] += 1
                if ja11 == cvg_threshold:
                    cvg_to_ja_count[3] += 1
        #         print(last_epi_ja_dis)
        #         print(ja00,ja01,ja10,ja11)
        
            print(listing_ass_adopted, listing_ass_proportion, cvg_to_ja_count)
"""
['AlwaysTutorAndLearn', 'AlwaysNotTutorOrLearn', 'ImitateOppoAction'] 

[0.03, 0.03, 0.94] [4, 4, 3, 4]
[0.16, 0.16, 0.68] [0, 0, 3, 1]
[0.1, 0.1, 0.8] [0, 3, 4, 1]

['AlwaysTutorAndLearn', 'AlwaysNotTutorOrLearn', 'WSLS'] 

[0.03, 0.03, 0.94] [0, 0, 0, 0]
[0.1, 0.1, 0.8] [0, 0, 0, 0]
[0.16, 0.16, 0.68] [0, 0, 0, 0]

['AlwaysTutorAndLearn', 'AlwaysNotTutorOrLearn', 'HCR'] 

[0.03, 0.03, 0.94] [518, 0, 0, 482]
[0.1, 0.1, 0.8] [442, 0, 0, 455]
[0.16, 0.16, 0.68] [331, 0, 0, 347]


"""
if __name__ == "__main__":
#     ass_cvg_analysis()
#     fixed_beheavior_cvg_analysis()
    fixed_oppo_beheavior_cvg_analysis()
    print("Done")
