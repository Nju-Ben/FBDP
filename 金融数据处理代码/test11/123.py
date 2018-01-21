def circle(num):
    s=[]
    while(num!=0):
        x=num%2
        s.append(x)
        num=int(num/2)
    return s

def dit2bit(num1,num2):
    s1=circle(num1)
    s2=circle(num2)
    s3=[]
    s4=[]
    l1=len(s1)
    l2=len(s2)
    count=0
    if l1<l2:
        for i in range(0,l2-l1):
#             x=s2.pop()
#             if x==1:
#                 count=count+1
            s4.append(s2.pop())
            s3.append(0)
        for i in range(l2-l1,l2):
#             if s1.pop()!=s2.pop():
#                 count=count+1
            s4.append(s2.pop())
            s3.append(s1.pop())
    elif l1>l2:
        for i in range(0,l1-l2):
#             x=s1.pop()
#             if x==1:
#                 count=count+1
            s3.append(s2.pop())
            s4.append(0)
        for i in range(l2-l1,l2):
#             if s1.pop()!=s2.pop():
#                 count=count+1
            s4.append(s2.pop())
            s3.append(s1.pop())
    else:
        for i in range(0,l1):
            if s1.pop()!=s2.pop():
                count=count+1
    #return count
            #s4.append(s2.pop())
            #s3.append(s1.pop())
    print(s3)
    print(s4)
    return s1
    
    


a=1
b=3
#print(circle(4))
#print(max(a,b))
x=dit2bit(a,b)
print(x)
b=11



