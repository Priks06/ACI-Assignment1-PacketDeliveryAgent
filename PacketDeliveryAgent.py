import random
import string
import math
import matplotlib.pyplot as plt

class PacketDeliveryAgent:

    def __init__(self):

        self.w1 = [1] * 15
        self.w2 = [2] * 5
        self.w3 = [4] * 7
        self.w4 = [5] * 2
        self.w5 = [6] * 3
        self.w6 = [7] * 2
        self.w7 = [9] * 4
        self.num=self.w1+self.w2+self.w3+self.w4+self.w5+self.w6+self.w7

        # The following dictionary consists of room names and their respective remaining storage space
        self.roomDict = {
            "A" : 25,
            "B" : 5,
            "C" : 28,
            "D" : 20,
            "E" : 46,
            "F" : 35
        }

        self.packet=[]                                                #Var for storing collection of packets selected by bot for commute
        self.visited=[]                                               #Var to recording visited packets
        self.secondPacket=[]                                          #Var for recording logic of Remaining - First
        self.commute=0                                                #Var for counting the commute made by bot
        self.visitedRooms = []
        # Select an initial random room first
        self.randomRoom, self.remainingStorageCapacity = random.choice(list(self.roomDict.items()))

    def generateRandomSolutionAndCalculateObjectiveFunctionValue(self):

        while (len(self.num)>=0):                                     # loop till all packed are picked and stored in go-down

            tempNum=self.num.copy()                                   # For inner while loop
            if(len(tempNum)>0):
                first=random.choice(tempNum)                     # Randomly select first packet
                remaining=10-first                               # Bot can carry only 10kg so 10 - selected packet
                self.packet.append(first)
                tempNum.remove(first)
                remainingLength=len(tempNum)
            else:
                break
            while (len(tempNum)>0):
                select=random.choice(tempNum)
                self.visited.append(select)                           # Record visited packets
                tempNum.remove(select)                           # Remove visited packets from list
                if((sum(self.secondPacket)+select)<=remaining):       # Calculating weight and it should not be more than 10 - first selected packet
                    self.secondPacket.append(select)
                elif(len(self.visited)>=remainingLength):
        #             print("visited length", len(visited))
                    break

            self.packet=self.packet+self.secondPacket                           #Combine first selected packet and remaining packet selection

            print("packet"+str(self.commute), self.packet)
            self.commute+=1

            for pack in self.packet:
                isPacketStored = False
                packetStoredInRoom = None
                while(not isPacketStored):
                    if (pack <= self.roomDict[self.randomRoom]):               # Check if the current packet can be placed in the randomly selected room
                        self.roomDict[self.randomRoom] = self.roomDict[self.randomRoom] - pack
                        isPacketStored = True
                        packetStoredInRoom = self.randomRoom
                        self.visitedRooms.append(self.randomRoom)
                        break
                    else:
                        # First check if there is any suitable storage space available in the already visited rooms, if yes then use that room, if no then find a new random room
                        if (len(self.visitedRooms) > 0):
                            optionalAvailableRoom = self.findVisitedRoomWithEnoughStorageSpace(pack, self.visitedRooms)
                            if (optionalAvailableRoom != None):
                                self.roomDict[optionalAvailableRoom] = self.roomDict[optionalAvailableRoom] - pack
                                isPacketStored = True
                                packetStoredInRoom = optionalAvailableRoom
                        self.randomRoom, self.remainingStorageCapacity = random.choice(list(self.roomDict.items()))
                if (isPacketStored):
                    self.num.remove(pack)                                 # Remove selected list of packets from original packet set in avoid repeated selection of same packets/boxes
                    print("Packet " + str(pack) + " stored in room " + packetStoredInRoom)
            self.packet=[]
            self.secondPacket=[]
            self.visited=[]

        print("Remaining storage space")
        print(self.roomDict)

        # Compute the objective function as x = Log(commutes) + Log(No of rooms visited) + Log(Remaining storage space)
        totalRemainingStorageSpace = 0
        for currRoomSpace in self.roomDict.values():
            totalRemainingStorageSpace = totalRemainingStorageSpace + currRoomSpace
        objectiveFunction = math.log2(self.commute) + math.log2(len(set(self.visitedRooms))) + math.log2(totalRemainingStorageSpace)
        print("Objective function value is : " + str(objectiveFunction))

        return objectiveFunction

    # Find previously visited room with sufficient space for the given packet
    def findVisitedRoomWithEnoughStorageSpace(self, packetSize, visitedRooms):
        for room in set(visitedRooms):
            if (packetSize <= self.roomDict[room]):
                return room
        return None


if __name__ == "__main__":
    objectiveFunctionValues = []
    serialNumbers = [i for i in range (1,101)]

    for i in range (0,100):
        packetDeliveryAgent = PacketDeliveryAgent()
        objectiveFunctionValue = packetDeliveryAgent.generateRandomSolutionAndCalculateObjectiveFunctionValue()
        objectiveFunctionValues.append(objectiveFunctionValue)
        #packetDeliveryAgent.clearData()

    # Plot the graph of attempt number against its objective function value
    plt.plot(serialNumbers, objectiveFunctionValues)
    plt.xlabel("Order")
    plt.ylabel("Running Time (secs)")
    plt.title("Number of Commutes")

    plt.show()