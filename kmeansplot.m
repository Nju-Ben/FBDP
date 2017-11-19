k=4
load part-m-00000
for j=1:k
    temp=[]
for i=1:size(part_m_00000,1)
    if part_m_00000(i,3)==j
        temp=[temp;part_m_00000(i,1:2)];
    end
end
 plot(temp(:,1),temp(:,2),'*','color',[rand,rand,rand])
 hold on 
end