#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

#This script is for setting things up if the user is going to be using sqlite for their database
#later, I can add in things to make mysql and postgres work in other scripts, but this will do for now

import sqlite3

conn = sqlite3.connect("./database") #placeholder path

conn.executescript("""
        create table player( idnum, name, vehicle, money, location, turns );
        create table vehicle_default( type, name, attacks, holds, cost);
        create table vehicle( idnum, type, attacks, holds, resources);
        create table areas( num, nodes, objects, connections);
        create table nodes_default( type, typename );
        create table nodes( name, typename, size, location, resourcebuy, resourcesell );
        """)

