-- Table definitions for the tournament project.
--
-- Put your SQL 'CREATE table' statements in this file; also 'CREATE VIEW'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Connect to the tournament database
\c tournament

DROP TABLE IF EXISTS players, matches CASCADE;

CREATE TABLE players ( full_name text not null,
                       id SERIAL);
 
CREATE TABLE matches ( winner_id INTEGER not null,
                       loser_id INTEGER not null,
                       match_id SERIAL);

CREATE VIEW winners as 
SELECT winner_id as id,
       count(winner_id) as numWins
FROM matches 
GROUP BY winner_id;

CREATE VIEW losers as
SELECT loser_id as id,
       count(loser_id) as numLosses 
FROM matches 
GROUP BY loser_id;

CREATE VIEW results as
SELECT coalesce(winners.id,losers.id) as id,
       coalesce(numwins,0) as numOfWins,
       coalesce(numlosses,0) as numOfLosses 
FROM winners FULL OUTER JOIN losers on winners.id = losers.id;

CREATE VIEW resultsRegisteredPlayers as
SELECT players.id, 
       players.full_name, 
       coalesce(numofwins,0) as wins,
       coalesce(numofwins,0) + coalesce(numoflosses,0) as matches
FROM players LEFT OUTER JOIN results on players.id = results.id 
ORDER BY wins DESC;
