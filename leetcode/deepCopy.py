class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors or []

class Solution:
    def deepcopy(self, node):
        if not node:
            return None
        #保存原节点 对应的 克隆后的新节点
        visted_dict = {}
        #1.第一个节点进入队列
        queue = [node]
        visted_dict[node] = Node(node.val)
        #2.开始广度遍历
        while queue:
            #3.队列表头的节点 以及对应的克隆节点
            origin_node = queue.pop()
            cloned_node = visted_dict[origin_node]
            for neighbor in origin_node.neighbors:
                #4.邻居未被访问过 则克隆并加入visted_dict
                if neighbor not in visted_dict:
                    visted_dict[neighbor] = Node(neighbor.val)
                    #入队
                    queue.append(neighbor)
                #复制邻居节点 
                cloned_node.neighbors.append(visted_dict[neighbor])
        return visted_dict[node]

if __name__ == '__main__':
    node1 = Node(val=1)
    node2 = Node(val=2, neighbors= [node1])
    node3 = Node(val=3, neighbors =[node2])
    node1.neighbors = [node3]

    s = Solution()
    res = s.deepcopy(node1)
    ll = res.neighbors