-- Create database tables

-- Table: wnba_data_user.players

-- DROP TABLE IF EXISTS wnba_data_user.players;

CREATE TABLE IF NOT EXISTS wnba_data_user.players
(
    player_id integer NOT NULL,
    player_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    active_flag integer NOT NULL,
    rookie_season integer NOT NULL,
    last_season integer NOT NULL,
    unknown integer NOT NULL,
    current_team character varying(45) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT players_pkey PRIMARY KEY (player_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.players
    OWNER to wnba_data_user;

-- Table: wnba_data_user.teams

-- DROP TABLE IF EXISTS wnba_data_user.teams;

CREATE TABLE IF NOT EXISTS wnba_data_user.teams
(
    team_id integer NOT NULL,
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


-- Table: wnba_data_user.team_game_logs

-- DROP TABLE IF EXISTS wnba_data_user.team_game_logs;

CREATE TABLE IF NOT EXISTS wnba_data_user.team_game_logs
(
    season_year integer NOT NULL,
    team_id integer NOT NULL,
    team_abbreviation character varying(45) COLLATE pg_catalog."default" NOT NULL,
    team_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    game_id integer NOT NULL,
    game_date date NOT NULL,
    matchup character varying(45) COLLATE pg_catalog."default",
    wl character varying(45) COLLATE pg_catalog."default",
    min real,
    fgm integer,
    fga integer,
    fg_pct real,
    fg3m integer,
    fg3a integer,
    fg3_pct real,
    ftm integer,
    fta integer,
    ft_pct real,
    oreb integer,
    dreb integer,
    reb integer,
    ast integer,
    tov real,
    stl integer,
    blk integer,
    blka integer,
    pf integer,
    pfd integer,
    pts integer,
    plus_minus real,
    gp_rank integer,
    w_rank integer,
    l_rank integer,
    w_pct_rank integer,
    min_rank integer,
    fgm_rank integer,
    fga_rank integer,
    fg_pct_rank integer,
    fg3m_rank integer,
    fg3a_rank integer,
    fg3_pct_rank integer,
    ftm_rank integer,
    fta_rank integer,
    ft_pct_rank integer,
    oreb_rank integer,
    dreb_rank integer,
    reb_rank integer,
    ast_rank integer,
    tov_rank integer,
    stl_rank integer,
    blk_rank integer,
    blka_rank integer,
    pf_rank integer,
    pfd_rank integer,
    pts_rank integer,
    plus_minus_rank integer,
    available_flag integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wnba_data_user.team_game_logs
    OWNER to wnba_data_user;


