import pandas as pd
import numpy as np

node_list=[[1,10.50,14.40,0],[2,18.00,15.90,10],
                      [3,18.30,13.30,10],[4,16.50,9.30,10],[5,15.40,11.00,10],
                      [6,14.90,13.20,5],[7,16.30,13.30,5],[8,16.40,17.80,5],
                      [9,15.00,17.90,5],[10,16.10,19.60,10],[11,15.70,20.60,10],
                      [12,13.20,20.10,10],[13,14.30,15.30,5],[14,14.00,5.10,10],
                      [15,11.40,6.70,15],[16,8.30,5.00,15],[17,7.90,9.80,10],
                      [18,11.40,12.00,5],[19,11.20,17.60,5],[20,10.10,18.70,5],
                      [21,11.70,20.30,10],[22,10.20,22.10,10],[23,9.70,23.80,10],
                      [24,10.10,26.40,15],[25,7.40,24.00,15],[26,8.20,19.90,15],
                      [27,8.70,17.70,10],[28,8.90,13.60,10],[29,5.60,11.10,10],
                      [30,4.90,18.90,10],[31,7.30,18.80,10],[32,11.20,14.10,0]]
#the first column represents the number of each node, the second column represent X coordinate of each node, the third column represent Y coordinate of each node, the fourth column represent the point of each node.
node_info = np.asarray(node_list,dtype=object)

node = pd.DataFrame(data=node_info,columns=['Node','X','Y','Point'])

a=np.array(node.iloc[1:-1])
#print(a[0,1])
