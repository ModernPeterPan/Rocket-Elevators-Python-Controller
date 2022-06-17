elevatorID = 1
floorRequestButtonID = 1
callButtonID = 1


class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'I dunno'
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1

        for i in range(0, _amountOfFloors):
            global callButtonID
            if i < _amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 1)
                self.callButtonList.append(callButton)
                callButtonID = + 1
            if i > 1:
                callButton = CallButton(callButtonID, buttonFloor, 1)
                self.callButtonList.append(callButton)
                callButtonID = + 1
            buttonFloor = + 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        #global elevatorID
        for i in range(_amountOfElevators):
            elevator = Elevator(i, _amountOfFloors)
            self.elevatorList.append(elevator)
            i += 1

    def requestElevator(self, requestedFloor, direction):
        elevator = self.findElevator(requestedFloor, direction)
        elevator.floorRequestList.append(requestedFloor)
        elevator.move()
        elevator.operateDoors()
        return elevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = None

        for elevator in self.elevatorList:
            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif elevator.status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            
            bestElevator = bestElevatorInformations["bestElevator"]
            bestScore = bestElevatorInformations["bestScore"]
            referenceGap = bestElevatorInformations["referenceGap"]
        return bestElevator


    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap

        return {
            "bestScore" : bestScore,
            "referenceGap" : referenceGap,
            "bestElevator" : bestElevator
            }


class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'my ass eat grass'
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.overweight = False
        self.obstruction = False

        self.createFloorRequestButtons(_amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        global floorRequestButtonID
        for i in range(0, _amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButtonID += 1

    def requestFloor(self, requestedFloor):
        self.floorRequestList.append(requestedFloor)
        self.sortFloorList()
        self.move()
        self.operateDoors()

    def move(self):
        while len(self.floorRequestList) >= 1:
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up'
                while self.currentFloor < destination:
                    self.currentFloor += 1
            elif self.currentFloor > destination:
                self.direction = 'down'
                while self.currentFloor > destination:
                    self.currentFloor -= 1
            self.status = 'stopped'
            self.floorRequestList.pop(0)
        self.status = 'idle'

    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    def operateDoors(self):
        self.door.status = 'opened'
        #Wait 5 seconds
        if not self.overweight:
            self.door.status = 'closing'
            if not self.obstruction:
                self.door.status = 'closed'
            else:
                self.operateDoors()
        else:
            while self.overweight:
                print('overweight alarm')
            self.operateDoors()


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = 'fuck you all'
        self.floor = _floor
        self.direction = _direction


class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = "I'm not having fun debugging tbh"
        self.floor = _floor


class Door:
    def __init__(self, _id, ):
        self.ID = _id
        self.status = "does it matter?"

#door = Door(1)
#column = Column(1, 10, 5)
#elevator = column.requestElevator(1, "up")