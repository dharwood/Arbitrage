#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

class Session:
    
    def __init__(self, playerID, playerName, location, turns, vehicle, money):
        self.playerID = playerID
        self.playerName = playerName
        self.location = location
        self.turns = turns
        self.ship = vehicle
        self.money = money
    
