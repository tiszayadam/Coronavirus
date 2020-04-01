# Coronavirus simulation

import random
import matplotlib.pyplot as plt



# -- parameters

populationsize = 200 #population size
duration = 100 #days
averagemeetsinitial = 0.2
averagemeets = averagemeetsinitial #per person per day
incubation = 7 #days
hospitaltime = 7 #days
totalrundown = incubation + hospitaltime #days
truedeathrate = 0.1 
showsimptomsrate = 0.5
withouttreatment = 2
deathrate = (truedeathrate*10)/((showsimptomsrate)*10)
immunity = True

healthcare = True
if(healthcare==True):
    healthcarecapacityratio=0.1  #of total population
    healthcarecapacity = healthcarecapacityratio*populationsize
else: healthcarecapacity = populationsize


socialdistancing = False
socialdistancedaveragemeets = 0.1
socialdistancingmeasures = False
if (socialdistancingmeasures==True):
    socialdistancingstart = 50
    socialdistancingdays = 30
    socialdistancingend = socialdistancingstart + socialdistancingdays
elif (socialdistancingmeasures==False):
    socialdistancingstart = duration+1
    socialdistancingdays = duration+1
    socialdistancingend = duration+1
    
curfew = False
curfewedaveragemeets = 0.01
curfewmeasures = False
if (curfewmeasures==True):
    curfewstart = 60
    curfewdays = 20
    curfewend = curfewstart + curfewdays
elif (curfewmeasures==False):
    curfewstart = duration+1
    curfewdays = duration+1
    curfewend = duration+1  
    
responddistancing = True
if(responddistancing==True):
    distancingatrate = 0.1
    socialdistancingdays = 30
    
respondcurfew = True
if(respondcurfew==True):
    curfewatrate = 0.2
    curfewdays = 20
    
# -- end of parameters
    
    
    
# -- setup

healthy = 0
infected = 1
dead = 2
immune = 3
nosimptoms = 4
inhospital = 5
inqueuetohospital = 6

person = list()
personcurrent = list()
personwhen = list()
for i in range(0,populationsize): #i: days
    person.append(healthy)
    personcurrent.append(healthy)
    personwhen.append(duration+1)

person[0]=infected #healthy, infected, inhospital, immune, dead, inqueuetohospital
personcurrent[0]=infected #healthy, infected, inhospital, nosimptoms, immune, dead, inqueuetohospital
personwhen[0]=0

infections = list()
infections.append(1)
knowninfections = list()
knowninfections.append(0)

newinfections = list()
newinfections.append(1)
knownnewinfections = list()
knownnewinfections.append(0)

alltimeinfections= list()
alltimeinfections.append(1)
knownalltimeinfections = list()
knownalltimeinfections.append(0)

deathtoll = list()
deathtoll.append(0)
newdeaths = list()
newdeaths.append(0)

hospital = list()
hospital.append(0)

untreateddead = list()
untreateddead.append(0)
untreated = list()
untreated.append(0)

if(immunity==True):
    immunes = list()
    immunes.append(0)
    
stage = "normal" #normal, socialdistancing, curfew
    
stageatday = list()
stageatday.append("normal")  

# -- end of setup



# -- run

for i in range(1,duration):

    infections.append(0)
    knowninfections.append(0)
    newinfections.append(0)
    knownnewinfections.append(0)
    alltimeinfections.append(alltimeinfections[i-1])
    knownalltimeinfections.append(knownalltimeinfections[i-1])
    deathtoll.append(0)
    newdeaths.append(0)
    untreated.append(0)
    untreateddead.append(untreateddead[i-1])
    hospital.append(hospital[i-1])
    if(immunity==True):
        immunes.append(0)
        
    # -- determine stage
    
    stage="normal"
        
    if(socialdistancingmeasures==True):
        if(socialdistancingstart<=i<socialdistancingend):
            socialdistancing=True
            
    if(responddistancing==True):
        if((populationsize*distancingatrate)<knowninfections[i-1] and socialdistancing==False and curfew==False):
            socialdistancing=True
            socialdistancingstart=i
            socialdistancingend=socialdistancingstart+socialdistancingdays
        if(i==socialdistancingend): socialdistancing=False     
        
    if(curfewmeasures==True):
        if(curfewstart<=i<curfewend):
            curfew=True
            
    if(respondcurfew==True):
        if((populationsize*curfewatrate)<knowninfections[i-1] and curfew==False):
            curfew=True
            curfewstart=i
            curfewend=curfewstart+curfewdays
        if(i==curfewend): curfew=False
        
    if(curfew==True):
        socialdistancing=False
        socialdistancingend=i
        
    if(curfew==True): stage="curfew"
    elif(socialdistancing==True): stage="socialdistancing"
    else: stage="normal"
    
    stageatday.append(stage)
            
    if(stage=="normal"):
        averagemeets = averagemeetsinitial      
    if(stage=="socialdistancing"):
        averagemeets = socialdistancedaveragemeets
    if(stage=="curfew"):
        averagemeets = curfewedaveragemeets
        
    # -- end of determine stage
    
    
        
    # -- model
    
    for p in range(0,populationsize-1):
        for q in range(p+1,populationsize):
            if(random.randrange(populationsize*100)<averagemeets*100):
                if(person[p]==infected and person[q]==healthy):
                    personcurrent[q]=infected
                    personwhen[q]=i
                if(person[p]==healthy and person[q]==infected):
                    personcurrent[p]=infected
                    personwhen[p]=i
                    
    # -- end of model
    
    
    
    # -- updating

    for s in range(1,hospitaltime):
        for t in range(0,populationsize):
            if(personwhen[t]==(i-s) and person[t]==inqueuetohospital and hospital[i]<healthcarecapacity):
                person[t]=inhospital
                personcurrent[t]=inhospital
                hospital[i]+=1
                    
    for r in range(0,populationsize): 
        
        if(person[r]==healthy and personcurrent[r]==infected): 
            newinfections[i]+=1
            alltimeinfections[i]+=1
            person[r]=infected
            
        if(personwhen[r]==(i-incubation)):
            if (random.randrange(100)<showsimptomsrate*100):
                if(hospital[i]<healthcarecapacity):
                    person[r]=inhospital
                    personcurrent[r]=inhospital
                    hospital[i]+=1
                else:
                    person[r]=inqueuetohospital
                    personcurrent[r]=inqueuetohospital
                knownnewinfections[i]+=1
                knownalltimeinfections[i]+=1
            else:
                personcurrent[r]=nosimptoms
                
        if(personwhen[r]==(i-totalrundown)):
            if(person[r]==inhospital): hospital[i]-=1
            if((random.randrange(100))<(deathrate*100) and person[r]==inhospital):
                person[r]=dead
                personcurrent[r]=dead
                newdeaths[i]+=1
            elif((random.randrange(100))<(deathrate*withouttreatment*100) and person[r]==inqueuetohospital):
                person[r]=dead
                personcurrent[r]=dead
                newdeaths[i]+=1
                untreateddead[i]+=1
            else: 
                if(immunity==True): 
                        person[r]=immune
                        personcurrent[r]=immune
                if(immunity==False): 
                        person[r]=healthy
                        personcurrent[r]=healthy
            if(i==14 and alltimeinfections[i]==1): print("patient zero did not infect anybody before illness detected/rundown, the probability of this is roughly", round((pow((1-averagemeetsinitial),incubation)*showsimptomsrate),3))               

        
        if(person[r]==infected or person[r]==inhospital or person[r]==inqueuetohospital): infections[i]+=1
        if(person[r]==inhospital or person[r]==inqueuetohospital): knowninfections[i]+=1
        if(person[r]==dead): deathtoll[i]+=1
        if(person[r]==inqueuetohospital): untreated[i]+=1
        if(immunity==True):
            if(person[r]==immune): immunes[i]+=1 
            
        # -- end of updating
        
        
            
# -- end of run            



# -- plotting 
        
        
plt.plot(infections, label="infections")
plt.plot(knowninfections, label="knowninfections")
#plt.plot(newinfections, label="newinfections")
#plt.plot(knownnewinfections, label="knownnewinfections")
#plt.plot(alltimeinfections, label="alltimeinfections")
#plt.plot(knownalltimeinfections, label="alltimeknowninfections")
plt.plot(deathtoll, label="deathtoll")
if(immunity==True):
        plt.plot(immunes, label="immunes")
#if(healthcare==True): plt.plot(inqueuetohospital, label="inqueuetohospital")
plt.xlabel("days")
plt.ylabel("people")
plt.legend()

#if (socialdistancingstart!=duration+1): plt.axvline(x=socialdistancingstart, ymin=0, ymax=populationsize, color='b')
#if (socialdistancingstart!=duration+1): plt.axvline(x=socialdistancingend, ymin=0, ymax=populationsize, color='c')
#if (curfewstart!=duration+1):plt.axvline(x=curfewstart, ymin=0, ymax=populationsize, color='r')
#if (curfewstart!=duration+1):plt.axvline(x=curfewend, ymin=0, ymax=populationsize, color='m')

# -- end of plotting


# improve plotting
# upload to github




