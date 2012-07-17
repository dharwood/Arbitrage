class Session:
    
    def __init__(self, playerID, playerName, location, turns, vehicle, money):
        self.playerID = playerID
        self.playerName = playerName
        self.location = location
        self.turns = turns
        self.ship = vehicle
        self.money = money
    
