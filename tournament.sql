-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

-- =========================================================================== 
-- Auther 		: Ajay
-- Created date : 15th sept
-- ===========================================================================
--   author      date      		description
-- ----------   ----------     -----------------------------------------------
-- Ajay         15th sept		created players,matches table
-- Ajay			21st sept		created views for matches_won,matches_played
-- Ajay         28th sept		created view for player_standings
-- Ajay			1st	 oct		passed all test cases
-- Ajay 		5th  oct 		Added DROP and CREATE database on import
-- ===========================================================================

--on import of sql file create new database and connect to it
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
--Tables

--Create players table 
--	id = Primary key
-- 	name = name of the player 
CREATE TABLE players(id SERIAL primary key,name TEXT); 

--Create matches table
--	id = primary key
--	winner = primary key of the winning player 
CREATE TABLE matches(id SERIAL primary key ,
				winner INTEGER REFERENCES players(id),
				loser INTEGER REFERENCES players(id));

-- Views


--View for number of matches won by each player and sorts the wins in descending

CREATE VIEW matches_won AS select players.id,COALESCE(count(players.id),0)as won from players,matches 
							where players.id = matches.winner 
							group by players.id order by won desc;


--View for number of matches played by each player and sorts by matches played in descending
CREATE VIEW matches_played AS select players.id,COALESCE(count(players.name),0)as played from players,matches 
							WHERE players.id = matches.winner OR players.id = matches.loser 
							group by players.id order by played desc;


--View for payer standings sorted by highest number of wins 
CREATE VIEW player_standings AS select players.id,players.name,COALESCE(matches_won.won,0) as wins 
							from players left join matches_won 
							ON players.id = matches_won.id; 





