import random
import string

w1 = [1] * 15
w2 = [2] * 5
w3 = [4] * 7
w4 = [5] * 2
w5 = [6] * 3
w6 = [7] * 2
w7 = [9] * 4
num=w1+w2+w3+w4+w5+w6+w7

roomDictOrig = {
    "A" : 25,
    "B" : 5,
    "C" : 28,
    "D" : 20,
    "E" : 46,
    "F" : 35
}
                                               #Var for counting the commute made by bot
# packet=[]                                                #Var for storing collection of packets selected by bot for commute
# visited=[]                                               #Var to recording visited packets
# secondPacket=[]                                          #Var for recording logic of Remaining - First
# commute=0
# packetCombo = {}                                              #Var for counting the commute made by bot

def generateRandomPacketCombo():
    packet=[]                                                #Var for storing collection of packets selected by bot for commute
    visited=[]                                               #Var to recording visited packets
    secondPacket=[]                                          #Var for recording logic of Remaining - First
    commute=0
    packetCombo = {}
    while (len(num)>=0):                                     # loop till all packed are picked and stored in go-down

        tempNum=num.copy()                                   # For inner while loop
        if(len(tempNum)>0):
            first=random.choice(tempNum)                     # Randomly select first packet
            remaining=10-first                               # Bot can carry only 10kg so 10 - selected packet
            packet.append(first)
            tempNum.remove(first)
            remainingLength=len(tempNum)
        else:
            break
        while (len(tempNum)>0):
            select=random.choice(tempNum)
            visited.append(select)                           # Record visited packets
            tempNum.remove(select)                           # Remove visited packets from list
            if((sum(secondPacket)+select)<=remaining):       # Calculating weight and it should not be more than 10 - first selected packet
                secondPacket.append(select)
            elif(len(visited)>=remainingLength):
    #             print("visited length", len(visited))
                break

        packet=packet+secondPacket                           #Combine first selected packet and remaining packet selection

        print("packet"+str(commute), packet)
        packetCombo.update({"combo"+str(commute): packet})
        commute+=1

        for pack in packet:                                  # Remove selected list of packets from original packet set in avoid repeated selection of same packets/boxes
            num.remove(pack)
        packet=[]
        secondPacket=[]
        visited=[]
    return packetCombo

def placePacketComboInRooms(packetCombo):
    roomDict = roomDictOrig.copy()
    for combo,packet1 in packetCombo.items():
        # print (combo, packet1)
        # print("Remaining storage space")
        # print(roomDict)
        currentRandomRoomList = list(roomDict.keys())
        randomRoom = random.choice(currentRandomRoomList)
        currentRandomRoomList.remove(randomRoom)
        remainingStorageCapacity = roomDict[randomRoom]
        # randomRoom, remainingStorageCapacity = random.choice(list(roomDict.items()))
        while (remainingStorageCapacity < sum(packet1)):
            # randomRoom, remainingStorageCapacity = random.choice(list(roomDict.items()))
            randomRoom = random.choice(currentRandomRoomList)
            currentRandomRoomList.remove(randomRoom)
            remainingStorageCapacity = roomDict[randomRoom]
            # print("Random room selected: " + randomRoom + " for combo: " + combo)
            # If list is empty it means our initial packet combo selection is incorrect
            if (len(currentRandomRoomList) == 0 and remainingStorageCapacity < sum(packet1)):
                # packetCombo = generateRandomPacketCombo()
                # break
                print("Initial packet combo is WRONG!!!")
                return False, None
        for pack in packet1:
            isPacketStored = False
            packetStoredInRoom = None
            while(not isPacketStored):

                if (pack <= roomDict[randomRoom]):               # Check if the current packet can be placed in the randomly selected room
                    roomDict[randomRoom] = roomDict[randomRoom] - pack
                    isPacketStored = True
                    packetStoredInRoom = randomRoom
                    # visitedRooms.append(randomRoom)
                    break
                # else:
                #     # First check if there is any suitable storage space available in the already visited rooms, if yes then use that room, if no then find a new random room
                #     if (len(visitedRooms) > 0):
                #         optionalAvailableRoom = None
                #         for room in set(visitedRooms):
                #             if (pack <= roomDict[room]):
                #                 optionalAvailableRoom = room
                #                 break
                #         #optionalAvailableRoom = findVisitedRoomWithEnoughStorageSpace(pack, visitedRooms)
                #         if (optionalAvailableRoom != None):
                #             roomDict[optionalAvailableRoom] = roomDict[optionalAvailableRoom] - pack
                #             isPacketStored = True
                #             packetStoredInRoom = optionalAvailableRoom

            # if (isPacketStored):
                # print (pack)
                # num.remove(pack)                                 # Remove selected list of packets from original packet set in avoid repeated selection of same packets/boxes

                # print("Packet " + str(pack) + " stored in room " + packetStoredInRoom)

                # print (packet1)
    return True, roomDict


# Evaluation function
def evaluate(currentRoomDict):
    # objective function calculation = sum of (remaining space/total room space) of utilized and difference of (unutilized room/total storage space of warehouse) of unutilzed
    objectiveFunction = 0
    for room in currentRoomDict:
        # This means room is utilized
        currRoomCapacity = currentRoomDict[room]
        origRoomCapacity = roomDictOrig[room]
        if (currRoomCapacity < origRoomCapacity):
            objectiveFunction = objectiveFunction + currRoomCapacity/origRoomCapacity
        # This means the room is unutilized i.e. empty, add negation of (total room capacity/sum of all room capacities)
        # i.e.  r/156, where r=room capacity of unutilized room
        else:
            objectiveFunction = objectiveFunction - (origRoomCapacity/156)
    return objectiveFunction


# Select an initial random room first
# randomRoom, remainingStorageCapacity = random.choice(list(roomDict.items()))
isSolutionAchieved = False
finalPacketCombo = {}
baseSolution = {}
while (not isSolutionAchieved):
    finalPacketCombo = generateRandomPacketCombo()
    isSolutionAchieved, baseSolution = placePacketComboInRooms(finalPacketCombo)
    print ("Is solution acheived" + str(isSolutionAchieved))

bestScore = evaluate(baseSolution)
print("Base Score so far", bestScore, 'Base Solution', baseSolution)
bestSolution = baseSolution
for i in range (0,1000):
    print("Best Score so far", bestScore, 'Solution', bestSolution)
    if bestScore == 0:
        break

    isSolutionAchieved, newSolution = placePacketComboInRooms(finalPacketCombo)

    if (not isSolutionAchieved):
        print("Edge case reached. Skipping")
        continue
    score = evaluate(newSolution)
    if score < bestScore:
        print("Better solution found")
        bestSolution = newSolution
        bestScore = score

print("Best Score found", bestScore, 'Best Solution', bestSolution)

# print("Remaining storage space")
# print(roomDictOrig)