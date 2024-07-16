CREATE ROLE wnba_data_user WITH login password 'password';

CREATE DATABASE wnba_data WITH owner wnba_data_user;

-- Connect to WNBA Data DB

SET ROLE TO wnba_data_user;

CREATE schema wnba_data_user AUTHORIZATION wnba_data_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

-- Create Tables and set Table Owner 
--
-- Table structure players
--
CREATE TABLE IF NOT EXISTS  players (
    "player_id" VARCHAR(45) NOT NULL,
    "player_name" VARCHAR(45) NOT NULL,
    "active_flag" VARCHAR(45) NOT NULL,
    "rookie_season" VARCHAR(45) NOT NULL,
    "last_season" VARCHAR(45) NOT NULL,
    "unknown" VARCHAR(45) NOT NULL,
    "current_team" VARCHAR(45) NOT NULL,

    PRIMARY KEY ("player_id")
);

ALTER TABLE wnba_data_user.players OWNER TO wnba_data_user;


--
-- Table structure dataset_info
--
CREATE TABLE IF NOT EXISTS  dataset_info (
    "date_generated" VARCHAR(45) NOT NULL,
    "seasons_count" VARCHAR(45) NOT NULL,
    "teams_count" VARCHAR(45) NOT NULL,
    "players_count" VARCHAR(45) NOT NULL,

    PRIMARY KEY ("date_generated")
);

ALTER TABLE wnba_data_user.dataset_info OWNER TO wnba_data_user;
