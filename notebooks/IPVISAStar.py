# coding: utf-8

"""
This code is part of the course 'Innovative Programmiermethoden für Industrieroboter' (Author: Bjoern Hein). It is based on the slides given during the course, so please **read the information in theses slides first**

License is based on Creative Commons: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) (pls. check: http://creativecommons.org/licenses/by-nc/4.0/)
"""

import networkx as nx


def aStarVisualize(planner, solution, ax = None, nodeSize = 300):
    graph = planner.graph
    collChecker = planner._collisionChecker
    # get a list of positions of all nodes by returning the content of the attribute 'pos'
    pos = nx.get_node_attributes(graph,'pos')
    pos_xy  = {k: v[:2] for k, v in pos.items()}
    color = nx.get_node_attributes(graph,'color')
    
    # get a list of degrees of all nodes
    #degree = nx.degree_centrality(graph)
    
    # draw graph (nodes colorized by degree)
    open_nodes = [node for node,attribute in graph.nodes(data=True) if attribute['status']=="open"]
    draw_nodes = nx.draw_networkx_nodes(graph, pos_xy, node_color='#FFFFFF', nodelist=open_nodes, ax = ax, node_size=nodeSize)
    draw_nodes.set_edgecolor("b")
    open_nodes = [node for node,attribute in graph.nodes(data=True) if attribute['status']=="closed"]
    draw_nodes = nx.draw_networkx_nodes(graph, pos_xy, node_color='#0000FF', nodelist=open_nodes, ax = ax, node_size=nodeSize)
    # nx.draw_networkx_nodes(graph, pos_xy,  cmap=plt.cm.Blues, ax = ax, node_size=nodeSize)
    nx.draw_networkx_edges(graph,pos_xy,
                               edge_color='b',
                               width=3.0
                            )
    
    collChecker.drawObstacles(ax)
    
    # draw nodes based on solution path
    Gsp = nx.subgraph(graph,solution)
    pos_sol = nx.get_node_attributes(Gsp,'pos')

    if solution:
        print("Found solution")
        nx.draw_networkx_nodes(Gsp,pos_xy,
                            node_size=nodeSize,
                             node_color='g')
        
        # draw edges based on solution path
        nx.draw_networkx_edges(Gsp,pos_xy,alpha=0.8,edge_color='g',width=10,arrows=True)

        nx.draw_networkx_nodes(graph,pos_xy,nodelist=[solution[0]],
                            node_size=300,
                            node_color='#00dd00',  ax = ax)
        nx.draw_networkx_labels(graph,pos_xy,labels={solution[0]: "S"},  ax = ax)

        nx.draw_networkx_nodes(graph,pos_xy,nodelist=[solution[-1]],
                                    node_size=300,
                                    node_color='#DD0000',  ax = ax)
        nx.draw_networkx_labels(graph,pos_xy,labels={solution[-1]: "G"},  ax = ax)

    try:
        if solution:
            collChecker.drawRobot(ax,
                                  pos_sol
                                  )
        else:
            pos_start_goal = pos
            keys_list = list(pos_start_goal.keys())

            # Identifizieren Sie die Schlüssel, die behalten werden sollen
            keys_to_keep = {keys_list[0], keys_list[-1]}

            # Iterieren Sie über eine Kopie der Schlüssel und löschen Sie Unerwünschte
            for key in list(pos_start_goal.keys()):
                if key not in keys_to_keep:
                    del pos_start_goal[key]
        
            collChecker.drawRobot(ax,
                                  pos_start_goal
                                  )
    except:
        print("Failed to draw robot")
        pass


