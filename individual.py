from NODE import node
import numpy as np
import pandas as pd
import random


class individual:
    def __init__(self):
        self.node_list=np.array([node.iloc[0],node.iloc[-1]])#路径表
        self.visited=self.node_list.copy() #已访问的集合
        self.unvisited=np.array(node.iloc[1:-1]) #未访问的集合
        self.fitness=0 #适应度
        self.distance=self.cal_distance() #路径中相邻距离
        self.TotalDistance=self.distance.sum() #总距离
        self.TotalPoint=0 #总分

    def reset(self,node_list,visited,unvisited,distance,TotalDistance,TotalPoint):
        self.node_list=node_list
        self.visited=visited
        self.unvisited=unvisited
        self.distance=distance
        self.TotalDistance=TotalDistance
        self.TotalPoint=TotalPoint

    def path_length(self,x1,x2,y1,y2):
        x=(x1-x2)**2
        y=(y1-y2)**2
        return np.sqrt(x+y)

    def cal_distance(self):
        distance=[]
        number_of_nodes = self.node_list.shape[0]
        for i in range(number_of_nodes - 1):
            D=self.path_length(self.node_list[i,1],self.node_list[i+1,1],self.node_list[i,2],self.node_list[i+1,2])
            distance.append(D)
        distance=np.array(distance)
        return distance

    def cal_TotalDistance(self):
        self.TotalDistance=self.distance.sum()

    def cal_TotalPoint(self):
        number_of_nodes = self.node_list.shape[0]
        for i in range(number_of_nodes):
            self.TotalPoint+=self.node_list[i,3]

    def cal_fitness(self):
        if self.TotalPoint==0:
            self.fitness=0
        else:
            self.fitness=self.TotalPoint**3/self.TotalDistance

    def insert_repeat_node(self):
        index=random.randint(0,len(self.visited)-1)
        insert_node=self.visited[index,:]
        insert_loc=len(self.node_list)-1
        self.node_list=np.insert(self.node_list,insert_loc,insert_node,axis=0)

        self.distance=self.cal_distance()
        self.cal_TotalDistance()

        self.cal_fitness()







