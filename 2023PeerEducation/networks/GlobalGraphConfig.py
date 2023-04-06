'''
Created on 6 Sep 2020

@author: w
'''
from networks.FullyConnected import FullyConnected
from networks.Smallworld import SmallWorld
# from networks.Community import Community
from networks.Grid import Grid

class GlobalGraphConfig:

    """
        the java-like "forname" to create class seems not well-handled in python
        so use a dictionary
    """
    type_to_netclass = {"FC":FullyConnected
                        , "SW":SmallWorld
#                         , "SF":ScaleFree
#                         , "CM":Community
                        , "GR":Grid
                        }
