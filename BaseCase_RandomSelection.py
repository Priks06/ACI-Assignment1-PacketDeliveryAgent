import random
import string
from sklearn.preprocessing import MinMaxScaler
import numpy as np

w1 = [1] * 15
w2 = [2] * 5
w3 = [4] * 7
w4 = [5] * 2
w5 = [6] * 3
w6 = [7] * 2
w7 = [9] * 4
origPacketsList = w1+w2+w3+w4+w5+w6+w7

roomDictOrig = {
    "A" : 25,
    "B" : 5,
    "C" : 28,
    "D" : 20,
    "E" : 46,
    "F" : 35
}

totalCapacityOfAllRooms = sum(roomDictOrig.values())

def generateRandomPacketCombo():
    packet=[]                                                #Var for storing collection of packets selected by bot for commute
    visited=[]                                               #Var to recording visited packets
    secondPacket=[]                                          #Var for recording logic of Remaining - First
    commute=0
    packetCombo = {}
    num = origPacketsList.copy()
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

        # print("packet"+str(commute), packet)
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
                # print("Initial packet combo is WRONG!!! No suitable room found for: " + combo)
                return False, None

        for pack in packet1:
            isPacketStored = False
            while(not isPacketStored):

                if (pack <= roomDict[randomRoom]):               # Check if the current packet can be placed in the randomly selected room
                    roomDict[randomRoom] = roomDict[randomRoom] - pack
                    isPacketStored = True
                    break

    return True, roomDict

def findOutUnutilizedRooms(currentRoomDict, isUtilized):
    unutilizedRoomsDict = []
    for room in currentRoomDict:
        if (not isUtilized and currentRoomDict[room] == roomDictOrig[room]):
            unutilizedRoomsDict.append(room)
        elif (isUtilized and currentRoomDict[room] < roomDictOrig[room]):
            unutilizedRoomsDict.append(room)
    return unutilizedRoomsDict

# Evaluation function
def evaluate(currentRoomDict):
    # Calculate total number of unused rooms
    unusedRooms = findOutUnutilizedRooms(currentRoomDict, False)
    unusedRoomsCapacityList = [currentRoomDict[room] for room in unusedRooms]
    # print(unusedRoomsCapacityList)
    usedRooms = findOutUnutilizedRooms(currentRoomDict, True)
    usedRoomsCapacityList = [currentRoomDict[room] for room in usedRooms]
    # print(usedRoomsCapacityList)

    scaler = MinMaxScaler()

    if (len(usedRoomsCapacityList) > 0):
        usedRoomsCapacityList=np.array(usedRoomsCapacityList)
        usedRoomsCapacityList=usedRoomsCapacityList.reshape(-1, 1)
        normalizedusedRoomsCapacityList = scaler.fit_transform(usedRoomsCapacityList)
        # print("Used:")
        # print(normalizedusedRoomsCapacityList)

    if (len(unusedRoomsCapacityList) > 0):
        unusedRoomsCapacityList=np.array(unusedRoomsCapacityList)
        unusedRoomsCapacityList=unusedRoomsCapacityList.reshape(-1, 1)
        normalizedunusedRoomsCapacityList = scaler.fit_transform(unusedRoomsCapacityList)
        # print("Unused:")
        # print(normalizedunusedRoomsCapacityList)

    totalUsedRoomCapacityNorm = 0
    if (len(usedRoomsCapacityList) > 0):
        totalUsedRoomCapacityNorm = sum(normalizedusedRoomsCapacityList)

    totalUnusedRoomCapacityNorm = 0
    if (len(unusedRoomsCapacityList) > 0):
        totalUnusedRoomCapacityNorm = sum(normalizedunusedRoomsCapacityList)

    objectiveFunction = totalUsedRoomCapacityNorm - totalUnusedRoomCapacityNorm

    return objectiveFunction


# Initialize best score to maximum possible number
finalBestScore = 999999
finalBestSolution = {}
finalPacketCombo = {}

for i in range (0,100):
    isSolutionAchieved = False
    packetCombo = {}
    baseSolution = {}
    while (not isSolutionAchieved):
        packetCombo = generateRandomPacketCombo()
        isSolutionAchieved, baseSolution = placePacketComboInRooms(packetCombo)
        # print ("Is solution acheived" + str(isSolutionAchieved))

    bestScore = evaluate(baseSolution)
    # print("Base Score so far", bestScore, 'Base Solution', baseSolution)
    bestSolution = baseSolution
    for j in range (0,100):
        # print("Best Score so far", bestScore, 'Solution', bestSolution)
        if bestScore == 0:
            break

        isSolutionAchieved, newSolution = placePacketComboInRooms(packetCombo)

        if (not isSolutionAchieved):
            # print("Edge case reached. Skipping")
            continue
        score = evaluate(newSolution)
        if score < bestScore:
            # print("Better solution found")
            bestSolution = newSolution
            bestScore = score

    # print("Best Score found in current selection of initial random packets", bestScore, 'Best Solution', bestSolution)

    # Check if the best score of current iteration is better than the previous iterations, if yes update that as the best solution
    if (bestScore < finalBestScore):
        print("Current selection of random packets has a better solution.")
        finalBestSolution = bestSolution
        finalBestScore = bestScore
        finalPacketCombo = packetCombo

print("Best Score found", finalBestScore, 'Best Solution', finalBestSolution)

print("\n****************SOLUTION BEGIN********************")
print("\nNumber of Commutes: ")
print(len(list(finalPacketCombo.keys())))
print("\nThe weight carried by the Robot in each commute: ")
print(finalPacketCombo)
print("\nThe number of rooms used to store the contingency: ")
utilizedRooms = findOutUnutilizedRooms(finalBestSolution, True)
print(utilizedRooms)
print("\nThe number of unused rooms: ")
unutilizedRooms = findOutUnutilizedRooms(finalBestSolution, False)
print(unutilizedRooms)
print("\nRemaining storage capacity in each room: ")
print(finalBestSolution)
print("\n****************SOLUTION END********************")