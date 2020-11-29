import numpy as np
import random

class FreeDice:
    def __init__(self):
        self.name = 'Free Die'
        
    def roll(self):
        y = random.randint(1,6)
        x = random.randint(1,6)
        y = x+y
        
        return y

class RestrictedDice:
    
    def __init__(self,initialCounts,tp,threshold=2):
        self.counts = initialCounts
        self.rejections = np.zeros(len(initialCounts))
        self.p_hat = self.counts/sum(self.counts)
        self.freeDice = FreeDice()
        self.maxRejectionsPerSample = 100
        self.tp = tp
        self.threshold = threshold
        self.history = []
        
    def roll(self):
        rc = 0
        n = sum(self.counts)
        #print(n)
        while(True):
            y = self.freeDice.roll()
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
            return y,rc #,abs(cy-ty),abs(cpy-self.tp[y-2])
K = 100
tc = np.array([1,2,3,4,5,6,5,4,3,2,1])
tc1 = np.array([1,2,3,4,5,6,5,4,3,2,1])

tp = tc/sum(tc)
#tp = np.around(tp,4)
print(tp)
restrictedDice = RestrictedDice(tc,tp,threshold=0)
freeDice = FreeDice()
fdCounts = np.zeros(len(tc)) + tc


while True:
    x = input('Hit enter to roll x to exit\n')
    if(x=='x'):
        exit(0)
    else:
        print(restrictedDice.roll()[0])
        
        n = sum(restrictedDice.counts)
        print(n)
        p1 = restrictedDice.counts/sum(restrictedDice.counts)
        c1 = 1.0*restrictedDice.counts
        
        y_free = freeDice.roll()
        fdCounts[y_free-2]+=1
        p2 = fdCounts/sum(fdCounts)
        c2 = fdCounts
        
        
        c3 = np.round(tp*n)

        print(1.0*np.array(range(2,13)))
        print(c1)
        print(c2)
        print(c1-c3, np.linalg.norm(c1-c3,1),np.linalg.norm(c2-c3,1))
        print(c1-c3, np.linalg.norm(c1-c3,1),np.linalg.norm(c2-c3,1))
        dp1 = np.linalg.norm(p1-tp,1)
        dp2 = np.linalg.norm(p2-tp,1)
        


        #print(c1-c3, np.linalg.norm(c1-c3,1))

        print(dp1,dp2)
        #print()
