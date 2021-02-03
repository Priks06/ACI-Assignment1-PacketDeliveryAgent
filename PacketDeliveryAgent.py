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

# The following dictionary consists of room names and their respective remaining storage space
roomDict = {
    "A" : 25,
    "B" : 5,
    "C" : 28,
    "D" : 20,
    "E" : 46,
    "F" : 35
}

packet=[]                                                #Var for storing collection of packets selected by bot for commute
visited=[]                                               #Var to recording visited packets
secondPacket=[]                                          #Var for recording logic of Remaining - First
commute=0                                                #Var for counting the commute made by bot
visitedRooms = []
# Select an initial random room first
randomRoom, remainingStorageCapacity = random.choice(list(roomDict.items()))
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
    commute+=1

    for pack in packet:
        isPacketStored = False
        packetStoredInRoom = None
        while(not isPacketStored):
            if (pack <= roomDict[randomRoom]):               # Check if the current packet can be placed in the randomly selected room
                roomDict[randomRoom] = roomDict[randomRoom] - pack
                isPacketStored = True
                packetStoredInRoom = randomRoom
                visitedRooms.append(randomRoom)
                break
            else:
                # First check if there is any suitable storage space available in the already visited rooms, if yes then use that room, if no then find a new random room
                if (len(visitedRooms) > 0):
                    optionalAvailableRoom = None
                    for room in set(visitedRooms):
                        if (pack <= roomDict[room]):
                            optionalAvailableRoom = room
                            break
                    #optionalAvailableRoom = findVisitedRoomWithEnoughStorageSpace(pack, visitedRooms)
                    if (optionalAvailableRoom != None):
                        roomDict[optionalAvailableRoom] = roomDict[optionalAvailableRoom] - pack
                        isPacketStored = True
                        packetStoredInRoom = optionalAvailableRoom
                randomRoom, remainingStorageCapacity = random.choice(list(roomDict.items()))
        if (isPacketStored):
            num.remove(pack)                                 # Remove selected list of packets from original packet set in avoid repeated selection of same packets/boxes
            print("Packet " + str(pack) + " stored in room " + packetStoredInRoom)
    packet=[]
    secondPacket=[]
    visited=[]

print("Remaining storage space")
print(roomDict)

def findVisitedRoomWithEnoughStorageSpace(packetSize, visitedRooms):
    for room in set(visitedRooms):
        if (roomDict[room] <= packetSize):
            return room
    return None