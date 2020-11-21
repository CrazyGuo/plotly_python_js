class TreeNode:
     def __init__(self, x):
         self.val = x
         self.left = None
         self.right = None

class Solution:
    def buildTree(self, preorder, inorder):
        return self.dfs(preorder, inorder)

    def dfs(self, preorder, inorder):
        if len(preorder) == 1:
            return TreeNode(preorder[0])
        root_val = preorder[0]
        root_index = inorder.index(root_val)

        #将中序数组划分为左右
        left_tree = inorder[0:root_index]
        right_tree = inorder[root_index+1:]
        #将前序划分为左右
        divd_flag_val = left_tree[-1]
        index2 = preorder.index(divd_flag_val)

        left_preorder = preorder[1:index2+1]
        right_preorder = preorder[index2+1:]

        #组装树
        left = self.dfs(left_preorder, left_tree)
        right = self.dfs(right_preorder, right_tree)
        root = TreeNode(root_val)
        root.left = left
        root.right = right
        return root
s = Solution()
s.buildTree([3,9],[9,3])




