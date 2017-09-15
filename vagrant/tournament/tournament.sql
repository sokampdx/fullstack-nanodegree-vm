-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW standings
;

DROP TABLE players CASCADE
;

DROP TABLE matches
;

CREATE TABLE players (
  player_id       serial PRIMARY KEY,
  player_name     varchar NOT NULL
)
;

CREATE TABLE matches (
  match_id    serial PRIMARY KEY,
  loser_id    integer REFERENCES players (player_id),
  winner_id   integer REFERENCES players (player_id)
)
;

CREATE VIEW standings AS
  SELECT p1.player_id, p1.player_name, COALESCE(match_won, 0), COALESCE(match_lose, 0) + COALESCE(match_won, 0) as match_played
  FROM 
    (
      players AS p1
      LEFT JOIN
      (
        SELECT winner_id, count(*) AS match_won FROM matches GROUP BY winner_id
      ) AS w
      ON p1.player_id = w.winner_id
    )
    INNER JOIN
    (
      players as p2
      LEFT JOIN
      (
        SELECT loser_id, count(*) AS match_lose FROM matches GROUP BY loser_id
      ) AS l 
      ON p2.player_id = l.loser_id
    )
    ON p1.player_id = p2.player_id
  ORDER BY match_won
;

