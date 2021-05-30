import numpy as np
import random
from individual import individual
import copy
from NODE import node


#计算距离
def cal_distant(x1,y1,x2,y2):
    x=(x1-x2)**2
    y=(y1-y2)**2
    return np.sqrt(x+y)

#插入节点
def insert_vertex(insert_location,node_list_temp,node_distance_temp,node_visited_temp,node_unvisited_temp,node_TotalPoint_temp,insert_node=np.array([-1,-1,-1,-1])):
    #随机选取一个不在路径上的点
    delete=False
    if insert_node[0]==-1:
        insert_node_index = random.randint(0, node_unvisited_temp.shape[0] - 1)
        insert_node=node_unvisited_temp[insert_node_index,:].copy()
        delete=True

    else:
        i=0
        while i<len(node_unvisited_temp):
            if node_unvisited_temp[i,0]==insert_node[0]:
                insert_node_index=i
                delete=True#表示插入的点在前面没有经过
                break
            i+=1



    # 将点插入到指定位置
    node_list_temp=np.insert(node_list_temp,insert_location,insert_node,axis=0)


    #更新visited/unvisited/totalpoint
    if delete:
        node_visited_temp=np.insert(node_visited_temp,0,insert_node,axis=0)
        node_unvisited_temp=np.delete(node_unvisited_temp,insert_node_index,axis=0)
        node_TotalPoint_temp+=insert_node[3]

    #更新distance



    dis_front=cal_distant(insert_node[1],insert_node[2],node_list_temp[insert_location-1,1],node_list_temp[insert_location-1,2])
    dis_back=cal_distant(insert_node[1],insert_node[2],node_list_temp[insert_location+1,1],node_list_temp[insert_location+1,2])
    temp_list=np.array([dis_front,dis_back])
    node_distance_temp=np.insert(node_distance_temp,insert_location,temp_list)
    node_distance_temp=np.delete(node_distance_temp,insert_location-1)
    node_TotalDistance_temp=np.sum(node_distance_temp)

    return node_list_temp,node_visited_temp,node_unvisited_temp,node_TotalPoint_temp,node_distance_temp,node_TotalDistance_temp


def crossover(parent1,parent2,i,j):
    #生成孩子节点列表
    child1_node=parent1.node_list[1:i,:]
    child1_node=np.append(child1_node,parent2.node_list[j:-1,:],axis=0)
    child2_node = parent2.node_list[1:j, :]
    child2_node = np.append(child2_node, parent1.node_list[i:-1, :], axis=0)



    #实例化两个孩子
    child1=individual()
    child2=individual()

    child1_node_list, child1_distance,child1_node_visited, child1_node_unvisited, child1_TotalPoint, \
     child1_TotalDistance=child1.node_list,child1.distance,child1.visited,child1.unvisited,\
                          child1.TotalPoint,child1.TotalDistance

    child2_node_list, child2_distance, child2_node_visited, child2_node_unvisited, child2_TotalPoint, \
    child2_TotalDistance = child2.node_list, child2.distance, child2.visited, child2.unvisited, \
                           child2.TotalPoint, child2.TotalDistance




    #print('======================================')
    for x in range(len(child1_node)):
        child1_node_list,child1_node_visited,child1_node_unvisited,child1_TotalPoint,\
        child1_distance,child1_TotalDistance = insert_vertex(x+1,child1_node_list, child1_distance,child1_node_visited,
                                                             child1_node_unvisited, child1_TotalPoint,child1_node[x,:])


    child1.reset( child1_node_list,child1_node_visited,child1_node_unvisited,\
        child1_distance,child1_TotalDistance,child1_TotalPoint)
    child1.cal_fitness()

    for y in range(len(child2_node)):
        child2_node_list,child2_node_visited,child2_node_unvisited,child2_TotalPoint,\
        child2_distance,child2_TotalDistance = insert_vertex(y+1,child2_node_list, child2_distance, child2_node_visited, child2_node_unvisited,
                                                             child2_TotalPoint,child2_node[y,:])

    child2.reset( child2_node_list,child2_node_visited,child2_node_unvisited,\
        child2_distance,child2_TotalDistance,child2_TotalPoint)
    child2.cal_fitness()

    return child1,child2


def TwoOpt(old_individual,Tmax):
    length=len(old_individual.node_list)
    if length<=4:
        return old_individual
    s_node_index=random.randint(1,length-3)
    e_node_index=random.randint(2,length-2)
    while e_node_index<=s_node_index:
        e_node_index=random.randint(2,length-2)

    new_individual=individual()

    sub_sequence=copy.deepcopy(old_individual.node_list[s_node_index:e_node_index+1,:])#要调换的子序列
    new_node_list,  new_distance,new_node_visited, new_node_unvisited, new_TotalPoint,\
     new_TotalDistance=new_individual.node_list,new_individual.distance,new_individual.visited,new_individual.unvisited,\
                          new_individual.TotalPoint,new_individual.TotalDistance

    #0-s顺序不变
    for i in range(s_node_index-1):
        insert_node=copy.deepcopy(old_individual.node_list[i+1])
        new_node_list,new_node_visited,  new_node_unvisited, new_TotalPoint,new_distance, \
     new_TotalDistance=insert_vertex(i+1,new_node_list,new_distance,new_node_visited,  new_node_unvisited, new_TotalPoint, \
     insert_node)


    #s-e顺序调换
    i=e_node_index-s_node_index
    while i>=0:

        temp_length=len(new_node_list)
        insert_location=temp_length-1
        insert_node=copy.deepcopy(sub_sequence[i,:])
        new_node_list,  new_node_visited, new_node_unvisited, new_TotalPoint, new_distance,\
        new_TotalDistance = insert_vertex(insert_location, new_node_list, new_distance, new_node_visited, new_node_unvisited,
                                          new_TotalPoint, \
                                          insert_node)

        i-=1



    #e以后不调换顺序
    i=e_node_index+1
    while i<=length-2:
        insert_node=copy.deepcopy(old_individual.node_list[i,:])
        temp_length = len(new_node_list)
        insert_location = temp_length - 1
        new_node_list,  new_node_visited, new_node_unvisited, new_TotalPoint, new_distance,\
        new_TotalDistance = insert_vertex(insert_location, new_node_list, new_distance, new_node_visited,
                                          new_node_unvisited,
                                          new_TotalPoint, \
                                          insert_node)

        i+=1

    if new_TotalDistance>Tmax:
        return old_individual

    new_individual.reset(new_node_list,new_node_visited, new_node_unvisited,new_distance,new_TotalDistance,new_TotalPoint)
    new_individual.cal_fitness()

    return new_individual


def inserting_mutation(old_solution,Tmax):
    from random import choice
    in_element_index= random.randint(0, old_solution.unvisited.shape[0] - 1)
    in_element=old_solution.unvisited[in_element_index,:].copy()
    in_value=in_element[3]
    loc=0
    best_increase_value=0
    old_solution_TotalDistance=old_solution.TotalDistance
    for i in range(1,len(old_solution.node_list)):
        old_node_list,  old_node_visited, old_node_unvisited, old_TotalPoint,old_distance, \
        old_TotalDistance = old_solution.node_list,  old_solution.visited, old_solution.unvisited, \
                              old_solution.TotalPoint, old_solution.distance,old_solution.TotalDistance
        #print('old',old_solution.node_list)
        #print('list',old_node_list)
        old_node_list,old_node_visited,old_node_unvisited,old_TotalPoint,\
        old_distance,old_TotalDistance= insert_vertex(i,old_node_list, old_distance, old_node_visited, old_node_unvisited, old_TotalPoint, \
        in_element)
        increase=(old_TotalDistance-old_solution_TotalDistance)
        insertion_value=in_value**2/increase
        if insertion_value>best_increase_value and old_TotalDistance<Tmax:
            best_increase_value=insertion_value
            loc=i
    old_node_list,  old_node_visited, old_node_unvisited, old_TotalPoint,old_distance, \
    old_TotalDistance = old_solution.node_list,  old_solution.visited, old_solution.unvisited, \
                        old_solution.TotalPoint, old_solution.distance,old_solution.TotalDistance
    if loc!=0:
        new_node_list, new_node_visited, new_node_unvisited, new_TotalPoint, new_distance,\
        new_TotalDistance=insert_vertex(loc,old_node_list, old_distance, old_node_visited, old_node_unvisited, old_TotalPoint, \
    in_element)
        #print('total point',new_TotalPoint)
        new_individual=individual()
        new_individual.reset(new_node_list, new_node_visited, new_node_unvisited, new_distance, \
        new_TotalDistance, new_TotalPoint)
        new_individual.cal_fitness()
        return new_individual
    return old_solution


def delete_mutation(old_individual,Tmax):
    temp_list=old_individual.node_list
    node_index_list=[]#记录有无重复点

    #计数器
    i=1
    k=0#记录templist长度
    flag=0
    repeat_loc1=0
    repeat_loc2=0

    #判断有无重复点
    while i<=len(temp_list)-2:
        if k==0:
            node_index_list.append([temp_list[i,0],i])
            k+=1

        else:
            l=0
            for j in node_index_list:
                if temp_list[i,0]==j[0] and l!=k-1:
                    l+=j[1]
                    flag+=1
                    break



        if flag==0:
            node_index_list.append([temp_list[i,0],i])
            k+=1

        else:
            repeat_loc1+=i
            repeat_loc2+=l
            break

        i+=1

    #删除重复点
    if flag==1:
        new_individual1=individual()
        new_individual2=individual()

        new1_node_list, new1_node_visited, new1_node_unvisited, new1_TotalPoint, new1_distance, \
        new1_TotalDistance = new_individual1.node_list, new_individual1.visited, new_individual1.unvisited, \
                            new_individual1.TotalPoint, new_individual1.distance, new_individual1.TotalDistance

        new2_node_list, new2_node_visited, new2_node_unvisited, new2_TotalPoint, new2_distance, \
        new2_TotalDistance = new_individual2.node_list, new_individual2.visited, new_individual2.unvisited, \
                             new_individual2.TotalPoint, new_individual2.distance, new_individual2.TotalDistance

        #删除第一个重复位置
        m=1
        loc=1
        while m<=len(temp_list)-2:

            if m!=repeat_loc1:
                new1_node_list, new1_node_visited, new1_node_unvisited, new1_TotalPoint, new1_distance, \
                new1_TotalDistance = insert_vertex(loc, new1_node_list, new1_distance, new1_node_visited, new1_node_unvisited,
                                                  new1_TotalDistance, \
                                                  temp_list[m,:])
                loc+=1
            m+=1

        new_individual1.reset(new1_node_list, new1_node_visited, new1_node_unvisited, new1_distance, \
        new1_TotalDistance, new1_TotalPoint)
        new_individual1.cal_fitness()

        #删除第二个重复位置
        n=1
        loc=1
        while n <= len(temp_list) - 2:
            if n != repeat_loc2:
                new2_node_list, new2_node_visited, new2_node_unvisited, new2_TotalPoint, new2_distance, \
                new2_TotalDistance = insert_vertex(loc, new2_node_list, new2_distance, new2_node_visited,
                                                   new2_node_unvisited,
                                                   new2_TotalDistance, \
                                                   temp_list[n, :])
                loc+=1
            n+=1

        new_individual2.reset(new2_node_list, new2_node_visited, new2_node_unvisited, new2_distance, \
                              new2_TotalDistance, new2_TotalPoint)
        new_individual2.cal_fitness()

        if new_individual1.TotalDistance<new_individual2.TotalDistance:
            return new_individual1

        else:
            return new_individual2

    else:
        #print('in else')
        len_decrease = 0  # 存储结果
        delete_location = 0
        if (old_individual.TotalDistance > 0.88 * Tmax):
            for i in range(1, len(old_individual.node_list)):
                old_node_list, old_node_visited, old_node_unvisited, old_TotalPoint, old_distance, \
                old_TotalDistance = old_individual.node_list, old_individual.visited, old_individual.unvisited, \
                                    old_individual.TotalPoint, old_individual.distance, old_individual.TotalDistance
                deletion_point = copy.deepcopy(i)  # 删除位置
                j = 1
                new_individual = individual()  # 新的对象
                new_node_list, new_distance, new_node_visited, new_node_unvisited, new_TotalPoint, \
                new_TotalDistance = new_individual.node_list, new_individual.distance, new_individual.visited, new_individual.unvisited, \
                                    new_individual.TotalPoint, new_individual.TotalDistance
                loc = 1
                while j < len(old_individual.node_list - 1):
                    insertion_value = old_individual.node_list[j, :].copy()  # 一个个插入的值

                    if (j != deletion_point):
                        new_node_list, new_node_visited, new_node_unvisited, new_TotalPoint, \
                        new_distance, new_TotalDistance = insert_vertex(loc, new_node_list, new_distance,
                                                                        new_node_visited,
                                                                        new_node_unvisited, new_TotalPoint,
                                                                        insertion_value)

                        new_individual.reset(new_node_list, new_node_visited, new_node_unvisited, \
                                             new_distance, new_TotalDistance, new_TotalPoint)
                        loc += 1
                    j += 1
                decreaseValue = old_TotalDistance - new_TotalDistance

                if decreaseValue!=0:
                    temp_len_decrease = old_individual.node_list[deletion_point, 3] ** 2 / decreaseValue
                else:
                    temp_len_decrease= +999999999999

                if (len_decrease == 0 and temp_len_decrease > 0):
                    len_decrease = copy.deepcopy(temp_len_decrease)
                    delete_location = copy.deepcopy(deletion_point)
                elif (temp_len_decrease > 0 and temp_len_decrease < len_decrease):
                    len_decrease = copy.deepcopy(temp_len_decrease)
                    delete_location = copy.deepcopy(deletion_point)

            if (len_decrease != 0 and delete_location != 0):
                res_individual = individual()
                res_node_list, res_distance, res_node_visited, res_node_unvisited, res_TotalPoint, \
                res_TotalDistance = res_individual.node_list, res_individual.distance, res_individual.visited, res_individual.unvisited, \
                                        res_individual.TotalPoint, res_individual.TotalDistance
                m = 1
                loc = 1
                while m < len(old_individual.node_list)-1:
                    insertion_value = old_individual.node_list[m, :].copy()

                    if (m != delete_location):
                        res_node_list, res_node_visited, res_node_unvisited, res_TotalPoint, \
                        res_distance, res_TotalDistance = insert_vertex(loc, res_node_list, res_distance,
                                                                            res_node_visited,
                                                                            res_node_unvisited, res_TotalPoint,
                                                                            insertion_value)
                        res_individual.reset(res_node_list, res_node_visited, res_node_unvisited, \
                                                 res_distance, res_TotalDistance, res_TotalPoint)
                        loc += 1
                    m += 1

            return res_individual

        else:
            return old_individual













