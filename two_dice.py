import numpy as np
import random

class FreeDice:
    def __init__(self,initialCounts,tp):
        self.name = 'Free Die'
        self.history = []
        self.tp = tp
        self.counts = initialCounts
        
    def roll(self):
        y = random.randint(1,6)
        x = random.randint(1,6)
        y = x+y
        n = sum(self.counts)
        cy = self.counts[y-2]
        cpy = cy/n 
        ty = np.round(self.tp*n)[y-2]
        self.history.append(y)
        
        
        return y,0,abs(cy-ty),abs(cpy-self.tp[y-2])

class RestrictedDice:
    
    def __init__(self,initialCounts,tp,threshold=2):
        self.counts = initialCounts
        self.rejections = np.zeros(len(initialCounts))
        self.p_hat = self.counts/sum(self.counts)
        self.freeDice = FreeDice(initialCounts,tp)
        self.maxRejectionsPerSample = 100
        self.tp = tp
        self.threshold = threshold
        self.history = []
        
    def roll(self):
        rc = 0
        n = sum(self.counts)
        #print(n)
        while(True):
            y,_,_,_ = self.freeDice.roll()
            cy = self.counts[y-2]
            ty = np.round(self.tp*n)[y-2]
            #print(cy,ty)
            #if(cy> ty + self.threshold and rc< self.maxRejectionsPerSample):
            #    rc+=1
            #    self.rejections[y-2]+=1
            #    continue
            cpy = cy/sum(self.counts)
            
            if(cpy > self.tp[y-2]+0.002 and rc < 100):
                #print('f')
                rc+=1
                continue
            elif rc>=100:
                #print('accept')
                p1 = self.counts/sum(self.counts)
                y = np.argmin(p1-self.tp)+2
                print('accept ',y,min(p1-self.tp))
                
            self.counts[y-2]+=1
            self.history.append(y)
            return y,rc,abs(cy-ty),abs(cpy-self.tp[y-2])

K = 100
tc = np.array([1,2,3,4,5,6,5,4,3,2,1])
tp = tc/42
tp = np.around(tp,4)
print(tp)

freeDice = FreeDice(tc,tp)
restrictedDice = RestrictedDice(tc,tp,threshold=0)
l1 = []
l2 = []
l3 = []
l4 = []
for i in range(K):
    s1,rc1,d1,dp1=freeDice.roll()
    s2,rc2,d2,dp2=restrictedDice.roll()
    l1.append(d1)
    l2.append(d2)
    l3.append(dp1)
    l4.append(dp2)
    #print(d1,d2)
#%matplotlib inline
import matplotlib.pyplot as plt

plt.plot(range(K),np.cumsum(l1),marker='o')
plt.plot(range(K),np.cumsum(l2))   
plt.figure()
plt.plot(range(K),l3,marker='o')
plt.plot(range(K),l4) 
