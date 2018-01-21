# from itertools import cycle
# c=cycle(['2','3','4'])
# n=0
# while (n<10):
#     print(next(c))
#     n=n+1;
# s = { '2':'abc', '3':'def','4':'ghi'}
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def constructMaximumBinaryTree(nums):
        t=max(nums)
        x=TreeNode(t)
        y=nums.index(max(nums))
        if len(nums[0:y]):
            x.left=constructMaximumBinaryTree(nums[0:y])
        else:
            x.left=None
        if len(nums[y+1:len(nums)]):
            x.right=constructMaximumBinaryTree(nums[y+1:len(nums)])
        else:
            x.right=None
        return x

def postorder(x):
    print(x.val)
    if x.left!=None:
        print("<-")
        postorder(x.left)
    else:
        return 0
    if x.right!=None:
        print("->")
        postorder(x.right)
    else:
        return 0


nums=[3,7,8,2,6,4]
x=constructMaximumBinaryTree(nums)
postorder(x)
#postorder(x)        
#a='234'
#def digui(x,n):
    #for i in x[0:n]:
        #x=x+i
        #print(x)
# for i in range(0,len(s)):
#     for j in range(1,len(s)):
#         for k in range(i,len(s)-j+1):
#             print(s[k],end='')
#             n=n+1;
#         print("")
# print(n)
# for i in s['2']:
#     #print(s['2'])
#     for j in s['3']:
#         print(i+j)