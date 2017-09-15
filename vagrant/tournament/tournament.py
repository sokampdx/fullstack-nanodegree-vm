#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def run_execute_only_query(sql):
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def run_query_with_result(sql):
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    return result

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    sql = "DELETE from matches;"
    run_execute_only_query(sql)

def deletePlayers():
    """Remove all the player records from the database."""
    sql = "DELETE from players;"
    run_execute_only_query(sql)

def countPlayers():
    """Returns the number of players currently registered."""
    sql = "SELECT count(*) from players;"
    result = run_query_with_result(sql)
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    sql = """INSERT INTO players (player_name) VALUES (%s);"""
    conn = connect()
    c = conn.cursor()
    c.execute(sql, (name,))
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

    sql = "SELECT * FROM standings;"
    result = run_query_with_result(sql)
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql = """INSERT INTO matches (winner_id, loser_id) VALUES(%s, %s)"""
    conn = connect()
    c = conn.cursor()
    c.execute(sql, (winner, loser))
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

    sql = "SELECT player_id, player_name FROM standings;"
    result = run_query_with_result(sql)
    matches = []
    for i in range(0, len(result), 2):
        match = result[i] + result[i + 1]
        matches.append(tuple(match))
    return matches
