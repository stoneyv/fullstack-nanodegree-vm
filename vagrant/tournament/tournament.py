#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import pdb


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        return conn
    except:
        "tournament.py error:  unable to connect to database tournament"


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = 'delete from matches'
    cur.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = 'delete from players'
    cur.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    query = 'select count(*) from players'
    cur.execute(query)
    rows = cur.fetchall()
    if len(rows) == 1:
        count = int(rows[0][0])
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    query = 'insert into players (full_name) values(%s)'
    cur.execute(query, (name,))
    conn.commit()
    conn.close()
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()

    """ All/only registered players have results returned by using a
    left outer join of table players. Views resultRegisteredPlayers,
    results, winners, losers are defined in tournament.sql to make the
    query more readable.
    """
    part1 = 'SELECT id, full_name as name, wins,'
    part2 = ' matches FROM resultsRegisteredPlayers'
    query = part1 + part2

    cur.execute(query)

    results = [(row[0], row[1], row[2], row[3]) for row in cur]

    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    query = 'insert into matches (winner_id, loser_id) values(%s, %s)'
    cur.execute(query, (winner, loser))
    conn.commit()
    conn.close()
    return


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
    # Get the number of matches already played from the DB
    conn = connect()
    cur = conn.cursor()
    query = 'select count(match_id) from matches'
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    num_matches = int(rows[0][0])

    standings = playerStandings()
    # if this is the first round of the tournament
    # randomize the order of the players
    if num_matches == 0:
        random.shuffle(standings)

    # Pair up the players by the match standings
    pairs = []
    num_players = len(standings)
    for i in range(0, num_players-2, 2):
        pairs.append((standings[i][0], standings[i][1],
                      standings[i+1][0], standings[i+1][1]))

    # if the number of players is even, add the last pair
    if num_players % 2 == 0:
        j = num_players - 2
        pairs.append((standings[j][0], standings[j][1],
                      standings[j+1][0], standings[j+1][1]))

    return pairs
