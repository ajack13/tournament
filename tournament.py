#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM players")
    ct = c.fetchall()
    conn.close()
    return ct[0][0] 
       

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players(name) values(%s)",(name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query ="""
    SELECT player_standings.id,player_standings.name,player_standings.wins as wins,COALESCE(matches_played.played,0)as matches 
        from player_standings LEFT JOIN matches_played 
            ON player_standings.id = matches_played.id 
            order by wins DESC; 
    """

    conn = connect()
    c = conn.cursor()
    c.execute(query)
    ret = c.fetchall()
    conn.close()
    return ret

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches(winner,loser) values('%s','%s')"% (winner,loser,))
    conn.commit()
    conn.close()     
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    plc = countPlayers()   # player count
    pls = playerStandings()  #player standings
    returnArr = []
    for i,v in enumerate(pls):
        if(i == 0):
            id1,name1,win1,matches1 = pls[i]
            id2,name2,win2,matches2 = pls[i+1]
            returnArr.append((id1,name1,id2,name2))       
        elif(i%2 !=0):
            continue
        else:
            id1,name1,win1,matches1 = pls[i]
            id2,name2,win2,matches2 = pls[i+1]
            returnArr.append((id1,name1,id2,name2));
    return returnArr



