import numpy as np
import pandas as pd
from NODE import node
from individual import individual
import random
import nGA
import copy

Tmax=50
population=60
max_number_of_generation=100
K=6
tsize=4


#初始化种群
pop_list=[]



for i in range(population):
    temp_node=individual()
    while True:
        insert_location=temp_node.node_list.shape[0]-1
        node_list_temp=temp_node.node_list.copy()
        node_distance_temp=temp_node.distance.copy()
        node_TotalDistance_temp=temp_node.TotalDistance
        node_visited_temp=temp_node.visited.copy()
        node_unvisited_temp=temp_node.unvisited.copy()
        node_TotalPoint_temp=temp_node.TotalPoint

        node_list_temp, node_visited_temp, node_unvisited_temp, node_TotalPoint_temp, node_distance_temp, \
        node_TotalDistance_temp=nGA.insert_vertex(insert_location,node_list_temp,node_distance_temp,node_visited_temp,node_unvisited_temp,node_TotalPoint_temp,np.array([-1,-1,-1,-1]))


        if node_TotalDistance_temp>Tmax:
            break

        temp_node.reset(node_list_temp, node_visited_temp, node_unvisited_temp,node_distance_temp,node_TotalDistance_temp,node_TotalPoint_temp)
        temp_node.cal_fitness()

    pop_list.append(temp_node)





for count in range(max_number_of_generation):
    #group selection
    selected_pop_list=[]#用于装经过选择后的个体

    for i in range(int(population/K)):

        for j in range(K):
            temp_pop_list=pop_list[j*int(population/K):(j+1)*int(population/K)].copy()
            #print(len(temp_pop_list))
            best_fitness=0
            best_individual=None
            index=-1

            for k in range(tsize):

                while True:
                    tem_a=random.randint(0,int(population/K)-1)
                    if index!=tem_a:
                        index=tem_a
                        break

                #print('index',index)
                selected_individual=copy.deepcopy(temp_pop_list[index])
                if selected_individual.fitness>=best_fitness:
                    best_fitness=selected_individual.fitness
                    best_individual=copy.deepcopy(selected_individual)
            selected_pop_list.append(best_individual)

    pop_list=selected_pop_list.copy()
    crossover_child=[]






    #交叉crossover
    for i in range(int(population/2)):
        parent1_index=random.randint(0,len(pop_list)-1)
        parent2_index=copy.deepcopy(parent1_index)
        #防止父母是同一个人
        while True:
            a_temp = random.randint(0, len(pop_list)-1)
            if a_temp!=parent2_index:
                parent2_index=a_temp
                break

        parent1=copy.deepcopy(pop_list[parent1_index])#父母一
        parent2=copy.deepcopy(pop_list[parent2_index])#父母二
        best_individual1=copy.deepcopy(parent1)
        best_individual2=copy.deepcopy(parent2)

        for j in range(1,len(parent1.node_list)-1):
            for k in range(1,len(parent2.node_list)-1):
                if parent1.node_list[j,0]==parent2.node_list[k,0]:

                    child1,child2=nGA.crossover(parent1,parent2,j,k)
                    #替换child和parent
                    if child1.TotalDistance<Tmax:
                        if best_individual1.fitness<best_individual2.fitness:
                            worse_of_best=copy.deepcopy(best_individual1)
                            tag=1
                        else:
                            worse_of_best=copy.deepcopy(best_individual2)
                            tag=2
                        if child1.fitness>worse_of_best.fitness and tag==1:
                            best_individual1=child1
                        elif child1.fitness>worse_of_best.fitness and tag==2:
                            best_individual2=child1

                    if child2.TotalDistance<Tmax:
                        if best_individual1.fitness<best_individual2.fitness:
                            worse_of_best=copy.deepcopy(best_individual1)
                            tag=1
                        else:
                            worse_of_best=copy.deepcopy(best_individual2)
                            tag=2
                        if child2.fitness>worse_of_best.fitness and tag==1:
                            best_individual1=child2
                        elif child2.fitness>worse_of_best.fitness and tag==2:
                            best_individual2=child2

        crossover_child.append(best_individual1)
        crossover_child.append(best_individual2)

    pop_list=crossover_child.copy()

    #print(len(pop_list))
    total_select=random.sample(range(0,population),int(population*0.3))
    #print(total_select)
    for i in total_select:

        #2-opt
        old_individual=copy.deepcopy(pop_list[i])
        new_individual=nGA.TwoOpt(old_individual,Tmax)
        #print('before insert',new_individual.node_list)

        #new_individual.insert_repeat_node()

        #print(new_individual.node_list)

        #每种变异1/2的可能
        choice=random.randint(1,2)

        if choice==1:
            new_individual=nGA.inserting_mutation(new_individual,Tmax)
        #print(new_individual.node_list)

        else:

        #print(new_individual.node_list)
            new_individual=nGA.delete_mutation(new_individual,Tmax)

        #print(new_individual.node_list)
        #print('=============================')

        pop_list[i]=new_individual





best_point=0
best_indi=None
for indi in pop_list:
    if indi.TotalPoint>best_point:
        best_point=indi.TotalPoint
        best_indi=indi

print(best_individual.TotalPoint,best_individual.node_list,best_individual.TotalDistance)









