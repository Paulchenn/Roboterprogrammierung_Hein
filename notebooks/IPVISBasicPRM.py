# coding: utf-8

"""
This code is part of the course "Introduction to robot path planning" (Author: Bjoern Hein).

License is based on Creative Commons: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) (pls. check: http://creativecommons.org/licenses/by-nc/4.0/)
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np


def basicPRMVisualize(planner, solution, ax = None, nodeSize = 100):
    """ Draw graph, obstacles and solution in a axis environment of matplotib.
    """
    # get a list of positions of all nodes by returning the content of the attribute 'pos'
    graph = planner.graph
    collChecker = planner._collisionChecker

    collChecker.drawObstacles(ax)
    
    pos = nx.get_node_attributes(graph,'pos')
    pos_xy  = {k: v[:2] for k, v in pos.items()}
    
    # draw graph (nodes colorized by degree)
    nx.draw_networkx_nodes(graph,
                           pos_xy,
                           cmap=plt.cm.Blues,
                           ax = ax,
                           node_size=nodeSize
                           )
    nx.draw_networkx_edges(graph,
                           pos_xy,
                           ax = ax
                           )
    Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
    G0=graph.subgraph(Gcc[0])# = largest connected component

    # how largest connected component
    nx.draw_networkx_edges(G0,
                           pos_xy,
                           edge_color='b',
                           width=3.0,
                           ax = ax
                           )

    
    # draw nodes based on solution path
    Gsp = nx.subgraph(graph,
                      solution
                      )
    pos_sol = nx.get_node_attributes(Gsp,'pos')
    
    nx.draw_networkx_nodes(Gsp,
                           pos_xy,
                           node_size=nodeSize*1.5,
                           node_color='g',
                           ax = ax
                           )
        
    # draw edges based on solution path
    nx.draw_networkx_edges(Gsp,
                           pos_xy,
                           alpha=0.8,
                           edge_color='g',
                           width=10,
                           ax = ax
                           )
        
    # draw start and goal
    print(graph.nodes())
    if "start" in graph.nodes(): 
        print("draw start")
        nx.draw_networkx_nodes(graph,
                               pos_xy,
                               nodelist=["start"],
                               node_size=nodeSize*1.5,
                               node_color='#00dd00',
                               ax = ax
                               )
        nx.draw_networkx_labels(graph,
                                pos_xy,
                                labels={"start": "S"},
                                ax = ax
                                )


    if "goal" in graph.nodes():
        print("draw goal")
        nx.draw_networkx_nodes(graph,
                               pos_xy,
                               nodelist=["goal"],
                               node_size=nodeSize*1.5,
                               node_color='#DD0000',
                               ax = ax
                               )
        nx.draw_networkx_labels(graph,
                                pos_xy,
                                labels={"goal": "G"},
                                ax = ax
                                )

    try:
        if len(pos_sol) > 0:
            collChecker.drawRobot(ax,
                                  pos_sol
                                  )
        else:
            pos_start_goal = {key: value for key, value in pos.items() if key in {'start', 'goal'}}
        
            collChecker.drawRobot(ax,
                                  pos_start_goal
                                  )
    except:
        print("Failed to draw robot")
        pass
