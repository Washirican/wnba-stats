CREATE ROLE wnba_data_user WITH login password 'password';

CREATE DATABASE wnba_data WITH owner wnba_data_user;

-- Connect to WNBA Data DB

SET ROLE TO wnba_data_user;

CREATE schema wnba_data_user AUTHORIZATION wnba_data_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

-- Create Tables and set Table Owner 

--
-- Table structure dataset_info
--
CREATE TABLE IF NOT EXISTS  dataset_info (
    date_generated VARCHAR(45) NOT NULL,
    seasons_count VARCHAR(45) NOT NULL,
    teams_count VARCHAR(45) NOT NULL,
    players_count VARCHAR(45) NOT NULL,

    PRIMARY KEY (date_generated)
);

ALTER TABLE wnba_data_user.dataset_info OWNER TO wnba_data_user;

--
-- Table structure players
--
CREATE TABLE IF NOT EXISTS  players (
    player_id VARCHAR(45) NOT NULL,
    player_name VARCHAR(45) NOT NULL,
    active_flag VARCHAR(45) NOT NULL,
    rookie_season VARCHAR(45) NOT NULL,
    last_season VARCHAR(45) NOT NULL,
    unknown VARCHAR(45) NOT NULL,
    current_team VARCHAR(45) NOT NULL,

    PRIMARY KEY (player_id)
);

ALTER TABLE wnba_data_user.players OWNER TO wnba_data_user;


--
-- Table structure common_team_roster
--
CREATE TABLE IF NOT EXISTS common_team_roster(
    TeamID VARCHAR(45) NOT NULL,
    SEASON VARCHAR(45) NOT NULL,
    LeagueID VARCHAR(45) NOT NULL,
    PLAYER VARCHAR(45) NOT NULL,
    NICKNAME VARCHAR(45) NOT NULL,
    PLAYER_SLUG VARCHAR(45) NOT NULL,
    NUM VARCHAR(45) NOT NULL,
    POSITION VARCHAR(45),
    HEIGHT VARCHAR(45),
    WEIGHT VARCHAR(45),
    BIRTH_DATE VARCHAR(45),
    AGE VARCHAR(45),
    EXP VARCHAR(45),
    SCHOOL VARCHAR(45),
    PLAYER_ID VARCHAR(45) NOT NULL,
    HOW_ACQUIRED VARCHAR(45),
    PRIMARY KEY (PLAYER_ID)
);

ALTER TABLE wnba_data_user.common_team_roster OWNER TO wnba_data_user;


--
-- Table structure player_career_stats
--
CREATE TABLE IF NOT EXISTS  player_career_stats (
    PLAYER_ID VARCHAR(45) NOT NULL,
    SEASON_ID VARCHAR(45) NOT NULL,
    LEAGUE_ID VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    PLAYER_AGE VARCHAR(45) NOT NULL,
    GP VARCHAR(45) NOT NULL,
    GS VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    TOV VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL,

    PRIMARY KEY (PLAYER_ID, season_id)
);

ALTER TABLE wnba_data_user.player_career_stats OWNER TO wnba_data_user;


--
-- Table structure player_game_logs
--
CREATE TABLE IF NOT EXISTS  player_game_logs (
    SEASON_YEAR INT NOT NULL,
    PLAYER_ID INT NOT NULL,
    PLAYER_NAME VARCHAR(45) NOT NULL,
    NICKNAME VARCHAR(45) NOT NULL,
    TEAM_ID INT NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    TEAM_NAME VARCHAR(45) NOT NULL,
    GAME_ID INT NOT NULL,
    GAME_DATE TIMESTAMP NOT NULL,
    MATCHUP VARCHAR(45) NOT NULL,
    WL VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    TOV VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    BLKA VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PFD VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL,
    PLUS_MINUS VARCHAR(45) NOT NULL,
    NBA_FANTASY_PTS VARCHAR(45) NOT NULL,
    DD2 VARCHAR(45) NOT NULL,
    TD3 VARCHAR(45) NOT NULL,
    WNBA_FANTASY_PTS VARCHAR(45) NOT NULL,
    GP_RANK VARCHAR(45) NOT NULL,
    W_RANK VARCHAR(45) NOT NULL,
    L_RANK VARCHAR(45) NOT NULL,
    W_PCT_RANK VARCHAR(45) NOT NULL,
    MIN_RANK VARCHAR(45) NOT NULL,
    FGM_RANK VARCHAR(45) NOT NULL,
    FGA_RANK VARCHAR(45) NOT NULL,
    FG_PCT_RANK VARCHAR(45) NOT NULL,
    FG3M_RANK VARCHAR(45) NOT NULL,
    FG3A_RANK VARCHAR(45) NOT NULL,
    FG3_PCT_RANK VARCHAR(45) NOT NULL,
    FTM_RANK VARCHAR(45) NOT NULL,
    FTA_RANK VARCHAR(45) NOT NULL,
    FT_PCT_RANK VARCHAR(45) NOT NULL,
    OREB_RANK VARCHAR(45) NOT NULL,
    DREB_RANK VARCHAR(45) NOT NULL,
    REB_RANK VARCHAR(45) NOT NULL,
    AST_RANK VARCHAR(45) NOT NULL,
    TOV_RANK VARCHAR(45) NOT NULL,
    STL_RANK VARCHAR(45) NOT NULL,
    BLK_RANK VARCHAR(45) NOT NULL,
    BLKA_RANK VARCHAR(45) NOT NULL,
    PF_RANK VARCHAR(45) NOT NULL,
    PFD_RANK VARCHAR(45) NOT NULL,
    PTS_RANK VARCHAR(45) NOT NULL,
    PLUS_MINUS_RANK VARCHAR(45) NOT NULL,
    NBA_FANTASY_PTS_RANK VARCHAR(45) NOT NULL,
    DD2_RANK VARCHAR(45) NOT NULL,
    TD3_RANK VARCHAR(45) NOT NULL,
    WNBA_FANTASY_PTS_RANK VARCHAR(45) NOT NULL,
    AVAILABLE_FLAG VARCHAR(45) NOT NULL,
	MIN_SEC VARCHAR(45) NOT NULL,
    PRIMARY KEY (GAME_ID)
);

ALTER TABLE wnba_data_user.player_game_logs OWNER TO wnba_data_user;


--
-- Table structure season_totals_regular_season
--
CREATE TABLE IF NOT EXISTS  season_totals_regular_season (
    PLAYER_ID VARCHAR(45) NOT NULL,
    SEASON_ID VARCHAR(45) NOT NULL,
    LEAGUE_ID VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    PLAYER_AGE VARCHAR(45) NOT NULL,
    GP VARCHAR(45) NOT NULL,
    GS VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    TOV VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL,

    PRIMARY KEY (PLAYER_ID)
);

ALTER TABLE wnba_data_user.season_totals_regular_season OWNER TO wnba_data_user;



--
-- Table structure teams
--
CREATE TABLE IF NOT EXISTS  teams (
    team_id VARCHAR(45) NOT NULL,
    team_abbreviation VARCHAR(45) NOT NULL,
    team_name VARCHAR(45) NOT NULL,
    team_city VARCHAR(45) NOT NULL,
    team_state VARCHAR(45) NOT NULL,
    time_zone VARCHAR(45) NOT NULL,
    primary_color VARCHAR(45) NOT NULL,
    secondary_color VARCHAR(45) NOT NULL,
    url VARCHAR(45) NOT NULL,

    PRIMARY KEY (team_id)
);

ALTER TABLE wnba_data_user.teams OWNER TO wnba_data_user;


--
-- Table structure shot_chart_detail
--
CREATE TABLE IF NOT EXISTS  shot_chart_detail(
    GRID_TYPE VARCHAR(45) NOT NULL,
    GAME_ID VARCHAR(45) NOT NULL,
    GAME_EVENT_ID VARCHAR(45) NOT NULL,
    PLAYER_ID VARCHAR(45) NOT NULL,
    PLAYER_NAME VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_NAME VARCHAR(45) NOT NULL,
    PERIOD VARCHAR(45) NOT NULL,
    MINUTES_REMAINING VARCHAR(45) NOT NULL,
    SECONDS_REMAINING VARCHAR(45) NOT NULL,
    EVENT_TYPE VARCHAR(45) NOT NULL,
    ACTION_TYPE VARCHAR(45) NOT NULL,
    SHOT_TYPE VARCHAR(45) NOT NULL,
    SHOT_ZONE_BASIC VARCHAR(45) NOT NULL,
    SHOT_ZONE_AREA VARCHAR(45) NOT NULL,
    SHOT_ZONE_RANGE VARCHAR(45) NOT NULL,
    SHOT_DISTANCE VARCHAR(45) NOT NULL,
    LOC_X VARCHAR(45) NOT NULL,
    LOC_Y VARCHAR(45) NOT NULL,
    SHOT_ATTEMPTED_FLAG VARCHAR(45) NOT NULL,
    SHOT_MADE_FLAG VARCHAR(45) NOT NULL,
    GAME_DATE VARCHAR(45) NOT NULL,
    HTM VARCHAR(45) NOT NULL,
    VTM VARCHAR(45) NOT NULL,
    PRIMARY KEY (GAME_EVENT_ID)
);

ALTER TABLE wnba_data_user.shot_chart_detail OWNER TO wnba_data_user;

--
-- Create Team Game Logs table
--
CREATE TABLE IF NOT EXISTS  team_game_logs(
      SEASON_YEAR VARCHAR(45) NOT NULL,
      TEAM_ID VARCHAR(45) NOT NULL,
      TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
      TEAM_NAME VARCHAR(45) NOT NULL,
      GAME_ID VARCHAR(45) NOT NULL,
      GAME_DATE VARCHAR(45) NOT NULL,
      MATCHUP VARCHAR(45) NOT NULL,
      WL VARCHAR(45) NOT NULL,
      MIN VARCHAR(45) NOT NULL,
      FGM VARCHAR(45) NOT NULL,
      FGA VARCHAR(45) NOT NULL,
      FG_PCT VARCHAR(45) NOT NULL,
      FG3M VARCHAR(45) NOT NULL,
      FG3A VARCHAR(45) NOT NULL,
      FG3_PCT VARCHAR(45) NOT NULL,
      FTM VARCHAR(45) NOT NULL,
      FTA VARCHAR(45) NOT NULL,
      FT_PCT VARCHAR(45) NOT NULL,
      OREB VARCHAR(45) NOT NULL,
      DREB VARCHAR(45) NOT NULL,
      REB VARCHAR(45) NOT NULL,
      AST VARCHAR(45) NOT NULL,
      TOV VARCHAR(45) NOT NULL,
      STL VARCHAR(45) NOT NULL,
      BLK VARCHAR(45) NOT NULL,
      BLKA VARCHAR(45) NOT NULL,
      PF VARCHAR(45) NOT NULL,
      PFD VARCHAR(45) NOT NULL,
      PTS VARCHAR(45) NOT NULL,
      PLUS_MINUS VARCHAR(45) NOT NULL,
      GP_RANK VARCHAR(45) NOT NULL,
      W_RANK VARCHAR(45) NOT NULL,
      L_RANK VARCHAR(45) NOT NULL,
      W_PCT_RANK VARCHAR(45) NOT NULL,
      MIN_RANK VARCHAR(45) NOT NULL,
      FGM_RANK VARCHAR(45) NOT NULL,
      FGA_RANK VARCHAR(45) NOT NULL,
      FG_PCT_RANK VARCHAR(45) NOT NULL,
      FG3M_RANK VARCHAR(45) NOT NULL,
      FG3A_RANK VARCHAR(45) NOT NULL,
      FG3_PCT_RANK VARCHAR(45) NOT NULL,
      FTM_RANK VARCHAR(45) NOT NULL,
      FTA_RANK VARCHAR(45) NOT NULL,
      FT_PCT_RANK VARCHAR(45) NOT NULL,
      OREB_RANK VARCHAR(45) NOT NULL,
      DREB_RANK VARCHAR(45) NOT NULL,
      REB_RANK VARCHAR(45) NOT NULL,
      AST_RANK VARCHAR(45) NOT NULL,
      TOV_RANK VARCHAR(45) NOT NULL,
      STL_RANK VARCHAR(45) NOT NULL,
      BLK_RANK VARCHAR(45) NOT NULL,
      BLKA_RANK VARCHAR(45) NOT NULL,
      PF_RANK VARCHAR(45) NOT NULL,
      PFD_RANK VARCHAR(45) NOT NULL,
      PTS_RANK VARCHAR(45) NOT NULL,
      PLUS_MINUS_RANK VARCHAR(45) NOT NULL,
      AVAILABLE_FLAG VARCHAR(45) NOT NULL
  
--     PRIMARY KEY (GAME_EVENT_ID)
);

ALTER TABLE wnba_data_user.team_game_logs OWNER TO wnba_data_user;

--
-- Create table boxscore_player_stats
--
CREATE TABLE IF NOT EXISTS  boxscore_player_stats(
    GAME_ID VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    TEAM_CITY VARCHAR(45) NOT NULL,
    PLAYER_ID VARCHAR(45) NOT NULL,
    PLAYER_NAME VARCHAR(45) NOT NULL,
    NICKNAME VARCHAR(45) NOT NULL,
    START_POSITION VARCHAR(45) NOT NULL,
    COMMENT VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    TOvrs VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL,
    PLUS_MINUS VARCHAR(45) NOT NULL
  

--     PRIMARY KEY (GAME_EVENT_ID)
);

ALTER TABLE wnba_data_user.boxscore_player_stats OWNER TO wnba_data_user;



--
-- Create table boxscore_team_stats
--
CREATE TABLE IF NOT EXISTS  boxscore_team_stats(
    GAME_ID VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_NAME VARCHAR(45) NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    TEAM_CITY VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    TOvrs VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL,
    PLUS_MINUS VARCHAR(45) NOT NULL
  

--     PRIMARY KEY (GAME_EVENT_ID)
);

ALTER TABLE wnba_data_user.boxscore_team_stats OWNER TO wnba_data_user;




--
-- Create table boxscore_team_start_bench_stats
--
CREATE TABLE IF NOT EXISTS  boxscore_team_start_bench_stats(
    GAME_ID VARCHAR(45) NOT NULL,
    TEAM_ID VARCHAR(45) NOT NULL,
    TEAM_NAME VARCHAR(45) NOT NULL,
    TEAM_ABBREVIATION VARCHAR(45) NOT NULL,
    TEAM_CITY VARCHAR(45) NOT NULL,
    STARTERS_BENCH VARCHAR(45) NOT NULL,
    MIN VARCHAR(45) NOT NULL,
    FGM VARCHAR(45) NOT NULL,
    FGA VARCHAR(45) NOT NULL,
    FG_PCT VARCHAR(45) NOT NULL,
    FG3M VARCHAR(45) NOT NULL,
    FG3A VARCHAR(45) NOT NULL,
    FG3_PCT VARCHAR(45) NOT NULL,
    FTM VARCHAR(45) NOT NULL,
    FTA VARCHAR(45) NOT NULL,
    FT_PCT VARCHAR(45) NOT NULL,
    OREB VARCHAR(45) NOT NULL,
    DREB VARCHAR(45) NOT NULL,
    REB VARCHAR(45) NOT NULL,
    AST VARCHAR(45) NOT NULL,
    STL VARCHAR(45) NOT NULL,
    BLK VARCHAR(45) NOT NULL,
    TOvrs VARCHAR(45) NOT NULL,
    PF VARCHAR(45) NOT NULL,
    PTS VARCHAR(45) NOT NULL

  

--     PRIMARY KEY (GAME_EVENT_ID)
);

ALTER TABLE wnba_data_user.boxscore_team_start_bench_stats OWNER TO wnba_data_user;


-- From PGAdmin4
-- Table: wnba_data_user.boxscore_player_stats

-- DROP TABLE IF EXISTS wnba_data_user.boxscore_player_stats;

CREATE TABLE IF NOT EXISTS wnba_data_user.boxscore_player_stats
(
    game_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_city character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    nickname character varying(45) COLLATE pg_catalog."default" NOT NULL,
    start_position character varying(45) COLLATE pg_catalog."default",
    comment character varying(45) COLLATE pg_catalog."default",
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    tovrs character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default",
    plus_minus character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.boxscore_player_stats
    OWNER to wnba_data_user;

-- Table: wnba_data_user.boxscore_team_start_bench_stats

-- DROP TABLE IF EXISTS wnba_data_user.boxscore_team_start_bench_stats;

CREATE TABLE IF NOT EXISTS wnba_data_user.boxscore_team_start_bench_stats
(
    game_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_city character varying(45) COLLATE pg_catalog."default" NOT NULL,
    starters_bench character varying(45) COLLATE pg_catalog."default",
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    tovrs character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.boxscore_team_start_bench_stats
    OWNER to wnba_data_user;


-- Table: wnba_data_user.boxscore_team_stats

-- DROP TABLE IF EXISTS wnba_data_user.boxscore_team_stats;

CREATE TABLE IF NOT EXISTS wnba_data_user.boxscore_team_stats
(
    game_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_city character varying(45) COLLATE pg_catalog."default" NOT NULL,
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    tovrs character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default",
    plus_minus character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.boxscore_team_stats
    OWNER to wnba_data_user;

-- Table: wnba_data_user.common_team_roster

-- DROP TABLE IF EXISTS wnba_data_user.common_team_roster;

CREATE TABLE IF NOT EXISTS wnba_data_user.common_team_roster
(
    teamid character varying(45) COLLATE pg_catalog."default" NOT NULL,
    season character varying(45) COLLATE pg_catalog."default" NOT NULL,
    leagueid character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player character varying(45) COLLATE pg_catalog."default" NOT NULL,
    nickname character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_slug character varying(45) COLLATE pg_catalog."default" NOT NULL,
    num character varying(45) COLLATE pg_catalog."default" NOT NULL,
    "position" character varying(45) COLLATE pg_catalog."default",
    height character varying(45) COLLATE pg_catalog."default",
    weight character varying(45) COLLATE pg_catalog."default",
    birth_date character varying(45) COLLATE pg_catalog."default",
    age character varying(45) COLLATE pg_catalog."default",
    exp character varying(45) COLLATE pg_catalog."default",
    school character varying(45) COLLATE pg_catalog."default",
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    how_acquired character varying(45) COLLATE pg_catalog."default",
    CONSTRAINT common_team_roster_pkey PRIMARY KEY (player_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.common_team_roster
    OWNER to wnba_data_user;

-- Table: wnba_data_user.player_career_stats

-- DROP TABLE IF EXISTS wnba_data_user.player_career_stats;

CREATE TABLE IF NOT EXISTS wnba_data_user.player_career_stats
(
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    season_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    league_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_age character varying(45) COLLATE pg_catalog."default" NOT NULL,
    gp character varying(45) COLLATE pg_catalog."default",
    gs character varying(45) COLLATE pg_catalog."default",
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    tov character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.player_career_stats
    OWNER to wnba_data_user;

-- Table: wnba_data_user.player_game_logs

-- DROP TABLE IF EXISTS wnba_data_user.player_game_logs;

CREATE TABLE IF NOT EXISTS wnba_data_user.player_game_logs
(
    season_year integer NOT NULL,
    player_id integer NOT NULL,
    player_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    nickname character varying(45) COLLATE pg_catalog."default",
    team_id integer NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_id integer NOT NULL,
    game_date timestamp without time zone,
    matchup character varying(45) COLLATE pg_catalog."default",
    wl character varying(45) COLLATE pg_catalog."default",
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    tov character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    blka character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pfd character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default",
    plus_minus character varying(45) COLLATE pg_catalog."default",
    nba_fantasy_pts character varying(45) COLLATE pg_catalog."default",
    dd2 character varying(45) COLLATE pg_catalog."default",
    td3 character varying(45) COLLATE pg_catalog."default",
    wnba_fantasy_pts character varying(45) COLLATE pg_catalog."default",
    gp_rank character varying(45) COLLATE pg_catalog."default",
    w_rank character varying(45) COLLATE pg_catalog."default",
    l_rank character varying(45) COLLATE pg_catalog."default",
    w_pct_rank character varying(45) COLLATE pg_catalog."default",
    min_rank character varying(45) COLLATE pg_catalog."default",
    fgm_rank character varying(45) COLLATE pg_catalog."default",
    fga_rank character varying(45) COLLATE pg_catalog."default",
    fg_pct_rank character varying(45) COLLATE pg_catalog."default",
    fg3m_rank character varying(45) COLLATE pg_catalog."default",
    fg3a_rank character varying(45) COLLATE pg_catalog."default",
    fg3_pct_rank character varying(45) COLLATE pg_catalog."default",
    ftm_rank character varying(45) COLLATE pg_catalog."default",
    fta_rank character varying(45) COLLATE pg_catalog."default",
    ft_pct_rank character varying(45) COLLATE pg_catalog."default",
    oreb_rank character varying(45) COLLATE pg_catalog."default",
    dreb_rank character varying(45) COLLATE pg_catalog."default",
    reb_rank character varying(45) COLLATE pg_catalog."default",
    ast_rank character varying(45) COLLATE pg_catalog."default",
    tov_rank character varying(45) COLLATE pg_catalog."default",
    stl_rank character varying(45) COLLATE pg_catalog."default",
    blk_rank character varying(45) COLLATE pg_catalog."default",
    blka_rank character varying(45) COLLATE pg_catalog."default",
    pf_rank character varying(45) COLLATE pg_catalog."default",
    pfd_rank character varying(45) COLLATE pg_catalog."default",
    pts_rank character varying(45) COLLATE pg_catalog."default",
    plus_minus_rank character varying(45) COLLATE pg_catalog."default",
    nba_fantasy_pts_rank character varying(45) COLLATE pg_catalog."default",
    dd2_rank character varying(45) COLLATE pg_catalog."default",
    td3_rank character varying(45) COLLATE pg_catalog."default",
    wnba_fantasy_pts_rank character varying(45) COLLATE pg_catalog."default",
    available_flag character varying(45) COLLATE pg_catalog."default",
    min_sec character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.player_game_logs
    OWNER to wnba_data_user;

-- Table: wnba_data_user.players

-- DROP TABLE IF EXISTS wnba_data_user.players;

CREATE TABLE IF NOT EXISTS wnba_data_user.players
(
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    active_flag character varying(45) COLLATE pg_catalog."default" NOT NULL,
    rookie_season character varying(45) COLLATE pg_catalog."default" NOT NULL,
    last_season character varying(45) COLLATE pg_catalog."default" NOT NULL,
    unknown character varying(45) COLLATE pg_catalog."default" NOT NULL,
    current_team character varying(45) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT players_pkey PRIMARY KEY (player_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.players
    OWNER to wnba_data_user;

-- Table: wnba_data_user.season_totals_regular_season

-- DROP TABLE IF EXISTS wnba_data_user.season_totals_regular_season;

CREATE TABLE IF NOT EXISTS wnba_data_user.season_totals_regular_season
(
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    season_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    league_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_age character varying(45) COLLATE pg_catalog."default" NOT NULL,
    gp character varying(45) COLLATE pg_catalog."default",
    gs character varying(45) COLLATE pg_catalog."default",
    min character varying(45) COLLATE pg_catalog."default",
    fgm character varying(45) COLLATE pg_catalog."default",
    fga character varying(45) COLLATE pg_catalog."default",
    fg_pct character varying(45) COLLATE pg_catalog."default",
    fg3m character varying(45) COLLATE pg_catalog."default",
    fg3a character varying(45) COLLATE pg_catalog."default",
    fg3_pct character varying(45) COLLATE pg_catalog."default",
    ftm character varying(45) COLLATE pg_catalog."default",
    fta character varying(45) COLLATE pg_catalog."default",
    ft_pct character varying(45) COLLATE pg_catalog."default",
    oreb character varying(45) COLLATE pg_catalog."default",
    dreb character varying(45) COLLATE pg_catalog."default",
    reb character varying(45) COLLATE pg_catalog."default",
    ast character varying(45) COLLATE pg_catalog."default",
    stl character varying(45) COLLATE pg_catalog."default",
    blk character varying(45) COLLATE pg_catalog."default",
    tov character varying(45) COLLATE pg_catalog."default",
    pf character varying(45) COLLATE pg_catalog."default",
    pts character varying(45) COLLATE pg_catalog."default",
    CONSTRAINT season_totals_regular_season_pkey PRIMARY KEY (player_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.season_totals_regular_season
    OWNER to wnba_data_user;

-- Table: wnba_data_user.shot_chart_detail

-- DROP TABLE IF EXISTS wnba_data_user.shot_chart_detail;

CREATE TABLE IF NOT EXISTS wnba_data_user.shot_chart_detail
(
    grid_type character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_event_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    player_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    period character varying(45) COLLATE pg_catalog."default",
    minutes_remaining character varying(45) COLLATE pg_catalog."default",
    seconds_remaining character varying(45) COLLATE pg_catalog."default",
    event_type character varying(45) COLLATE pg_catalog."default",
    action_type character varying(45) COLLATE pg_catalog."default",
    shot_type character varying(45) COLLATE pg_catalog."default",
    shot_zone_basic character varying(45) COLLATE pg_catalog."default",
    shot_zone_area character varying(45) COLLATE pg_catalog."default",
    shot_zone_range character varying(45) COLLATE pg_catalog."default",
    shot_distance character varying(45) COLLATE pg_catalog."default",
    loc_x character varying(45) COLLATE pg_catalog."default",
    loc_y character varying(45) COLLATE pg_catalog."default",
    shot_attempted_flag character varying(45) COLLATE pg_catalog."default",
    shot_made_flag character varying(45) COLLATE pg_catalog."default",
    game_date character varying(45) COLLATE pg_catalog."default",
    htm character varying(45) COLLATE pg_catalog."default",
    vtm character varying(45) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.shot_chart_detail
    OWNER to wnba_data_user;

-- Table: wnba_data_user.team_game_logs

-- DROP TABLE IF EXISTS wnba_data_user.team_game_logs;

CREATE TABLE IF NOT EXISTS wnba_data_user.team_game_logs
(
    season_year character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_date character varying(45) COLLATE pg_catalog."default" NOT NULL,
    matchup character varying(45) COLLATE pg_catalog."default" NOT NULL,
    wl character varying(45) COLLATE pg_catalog."default" NOT NULL,
    min character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fgm character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fga character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg_pct character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3m character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3a character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3_pct character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ftm character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fta character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ft_pct character varying(45) COLLATE pg_catalog."default" NOT NULL,
    oreb character varying(45) COLLATE pg_catalog."default" NOT NULL,
    dreb character varying(45) COLLATE pg_catalog."default" NOT NULL,
    reb character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ast character varying(45) COLLATE pg_catalog."default" NOT NULL,
    tov character varying(45) COLLATE pg_catalog."default" NOT NULL,
    stl character varying(45) COLLATE pg_catalog."default" NOT NULL,
    blk character varying(45) COLLATE pg_catalog."default" NOT NULL,
    blka character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pf character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pfd character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pts character varying(45) COLLATE pg_catalog."default" NOT NULL,
    plus_minus character varying(45) COLLATE pg_catalog."default" NOT NULL,
    gp_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    w_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    l_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    w_pct_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    min_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fgm_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fga_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg_pct_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3m_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3a_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fg3_pct_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ftm_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    fta_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ft_pct_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    oreb_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    dreb_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    reb_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    ast_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    tov_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    stl_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    blk_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    blka_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pf_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pfd_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    pts_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    plus_minus_rank character varying(45) COLLATE pg_catalog."default" NOT NULL,
    available_flag character varying(45) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.team_game_logs
    OWNER to wnba_data_user;

-- Table: wnba_data_user.teams

-- DROP TABLE IF EXISTS wnba_data_user.teams;

CREATE TABLE IF NOT EXISTS wnba_data_user.teams
(
    team_id character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_city character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_state character varying(45) COLLATE pg_catalog."default" NOT NULL,
    time_zone character varying(45) COLLATE pg_catalog."default" NOT NULL,
    primary_color character varying(45) COLLATE pg_catalog."default" NOT NULL,
    secondary_color character varying(45) COLLATE pg_catalog."default" NOT NULL,
    url character varying(45) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT teams_pkey PRIMARY KEY (team_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.teams
    OWNER to wnba_data_user;