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
    # query =""" SELECT players.id,players.name,count(players.name) as w_t FROM players,matches
    #              WHERE players.id = matches.winner group by players.id order by w_t desc"""
    query = """ 
    SELECT matches_won.id,matches_won.name,matches_won.w_t,matches_played.w_t FROM matches_won LEFT JOIN matches_played 
    ON matches_won.id = matches_played.id
    """

    query2 ="""
    SELECT player_standings.id,player_standings.name,player_standings.wins as wins,COALESCE(matches_played.w_t,0)as matches from player_standings 
    LEFT JOIN matches_played ON player_standings.id = matches_played.id order by wins DESC; 
    """

    conn = connect()
    c = conn.cursor()
    c.execute(query2)
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
        try:
            print 'STD  : ',pls[i],' STD2 : ',pls[i+1]
            id1,name1,win1,matches1 = pls[i]
            id2,name2,win2,matches2 = pls[i+1]
            returnArr.append((id1,name1,id2,name2));
            if(i < plc):
                i = i + 2
        except:
            return returnArr



