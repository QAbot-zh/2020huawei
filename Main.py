# /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhong Xianyou
# Modify date: 2020-04-09 
""" 2.0: 修复了找环的逻辑, 可以完整找环了, 但是速度还不行, 使用cmp_to_key方法来进行最后的排序, 淘汰优先队列的排序方法 """
""" 3.0: 剔除了大量重复语句和无用的判断, 主要是对visit_link 和 部分数据结构作了修改, 改进了速度 """
""" 4.0: 使用双向寻环, 降低搜索数量级, 速度有提高 """
""" 5.0/6.0: 保留上一节点信息, 减少一层的搜索量 [减少不必要的元素重复索引, 减少不必要的条件判断, 减少对内存的操作]"""

class Graph(object):
    def __init__(self, *args, **kwargs):
        self.node_neighbors_from = {}
        self.node_neighbors_to = {}
        self.visited = {}
        self.belong_to_link = {}
        self.belong_to_link_last_node = {}
        self.visit_link = []

    def add_edge(self, edge):
        u, v = edge
        # 貌似try比if要快一丁丁
        try:
            self.node_neighbors_from[u].add(v)
        except:
            self.node_neighbors_from[u] = set([v])
        try:
            self.node_neighbors_to[v].add(u)
        except:
            self.node_neighbors_to[v] = set([u])
        
        self.visited[u] = 0
        self.visited[v] = 0
        self.belong_to_link[u] = -1
        self.belong_to_link[v] = -1
        self.belong_to_link_last_node[u] = -1
        self.belong_to_link_last_node[v] = -1
 
    def nodes(self):
        return self.node_neighbors_from.keys()
    

    #递归DFS
    def dfs_ring(self):
        self.result = [[] for i in range(7)]

        def dfs_pruning_reverse(node, link, depth):
            """ 剪枝 """
            if depth <= -3:
                return
            if node not in self.node_neighbors_to.keys():
                return
            depth -= 1
            for n in self.node_neighbors_to[node]:
                if self.visited[n] > 0:
                    continue
                self.belong_to_link[n] = link
                if depth == -1:
                    self.belong_to_link_last_node[n] = link
                self.visited[n] = 1
                dfs_pruning_reverse(n, link, depth)
                self.visited[n] = 0

        def dfs(node, path_head, depth):
            if depth == 6:
                return
            if node in self.node_neighbors_from.keys():
                depth += 1
                # path_head = self.visit_link[0]
                for n in self.node_neighbors_from[node]:
                    # print("父节点{}正在访问节点:{}".format(node, n))
                    # print("节点访问情况:{}".format(self.visit_link))
                    # print("depth = {}".format(depth))
                    # print("n belong to {}".format(self.belong_to_link[n]))
                    if self.visited[n] > 0:
                        # n 已经被访问过
                        continue
                    if depth>=4 and self.belong_to_link[n]!=path_head:
                        continue
                    # if n in self.visit_link:
                    #     # 当前链路出现小环
                    #     continue
                    if self.belong_to_link_last_node[n] == path_head:
                        if depth >= 2:
                            self.visit_link.append(n)
                            self.result[depth].append(self.visit_link.copy())
                            # print("找到一个长度3~7的环:{}".format(self.visit_link))
                            self.visit_link.pop()
                    
                    self.visited[n] = 1
                    self.visit_link.append(n)
                    dfs(n, path_head, depth)
                    self.visit_link.pop()
                    self.visited[n] = 0

        self.visit_link = []
        for node in sorted(self.nodes()):

            if self.visited[node]==0:
                self.visited[node] = 1
                self.visit_link.append(node)
                dfs_pruning_reverse(node, node, 0)
                dfs(node, node, 0)
                self.visit_link.pop()
        
        self.len_result = 0
        for i in range(2,7):
            self.len_result += len(self.result[i])

    def readData(self, test_data_filepath):
        with open(test_data_filepath,'r') as f:
            for line in f:
                account1, account2, money = list(map(int, line.split(',')))
                self.add_edge([account1, account2])


    def writeData(self, result_filepath):

        with open(result_filepath, 'w') as f:
            f.write(str(self.len_result)+"\n")
            for i in range(2,7):
                res = self.result[i]
                res.sort()
                for ring in res:
                    # 字符串操作虽然优雅但是费时
                    # f.writelines(str(ring)[1:-1].replace(' ', '')+"\n")
                    # f.writelines(str(ring)[1:-1]+"\n")
                    for i in range(len(ring)):
                        if(i == 0):
                            f.write(str(ring[i]))
                        else:
                            f.write(","+str(ring[i]))
                    f.write("\n")

    def process(self, test_data_filepath, result_filepath):
        self.readData(test_data_filepath)
        self.dfs_ring()
        self.writeData(result_filepath)

if __name__ == '__main__':
    REMOTE = True
    if REMOTE:
        test_data_filepath = "/data/test_data.txt"
        result_filepath = "/projects/student/result.txt"
    else:
        # test_data_filepath = "./test_data.txt"
        test_data_filepath = "./2020HuaweiCodecraft-TestData/77409/test_data.txt"
        result_filepath = "./result_main.txt"

    g = Graph()
    g.process(test_data_filepath, result_filepath)
    # del g
