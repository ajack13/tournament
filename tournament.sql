-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players(id SERIAL primary key,name TEXT);

CREATE TABLE matches(id SERIAL primary key ,
				winner INTEGER REFERENCES players(id),
				loser INTEGER REFERENCES players(id));

-- views

CREATE VIEW player_standings AS select players.id,players.name,COALESCE(matches_won.w_t,0) as wins from players left join matches_won ON players.id = matches_won.id; 


CREATE VIEW matches_won AS select players.id,players.name,COALESCE(count(players.id),0)as w_t from players left join matches 
						ON players.id = matches.winner group by players.id order by w_t desc;


CREATE VIEW matches_played AS select players.id,players.name,COALESCE(count(players.name),0)as w_t from players,matches 
							WHERE players.id = matches.winner OR players.id = matches.loser 
							group by players.id order by w_t desc;


