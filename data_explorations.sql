TABLE boxscore_player_stats;
TABLE boxscore_team_start_bench_stats;
TABLE boxscore_team_stats;
TABLE common_team_roster;
TABLE dataset_info;
TABLE player_career_stats;
TABLE player_game_logs;
TABLE players;
TABLE season_totals_regular_season;

TABLE shot_chart_detail;

TABLE team_game_logs;
TABLE teams;

-- Delete table data
-- DELETE FROM common_team_roster;
-- DELETE FROM dataset_info;
-- DELETE FROM player_career_stats;
-- DELETE FROM player_game_logs;
-- DELETE FROM players;
-- DELETE FROM season_totals_regular_season;
DELETE FROM shot_chart_detail;
-- DELETE FROM teams;
-- DELETE FROM boxscore_player_stats;
-- DELETE FROM boxscore_team_start_bench_stats;
-- DELETE FROM boxscore_team_stats;

INSERT INTO player_career_stats VALUES
(1631086, '2024-25', '10', 1611661325, 'IND', 24.0, 20, 1, 13.3, 1.2, 3.4, 0.338, 0.5, 1.6, 0.281, 0.8, 1.0, 0.8, 0.5, 1.0, 1.5, 0.7, 0.5, 0.2, 0.8, 2.0, 3.6)
;

SELECT * FROM teams WHERE team_id::integer = 1611661329;

SELECT * FROM teams WHERE team_id::integer = 1611661323;

SELECT * FROM teams WHERE team_id::integer = 1611661330;

select * FROM players where player_id::integer = 100940;

select * FROM players where player_id::integer = 1630149;

select * FROM common_team_roster where player_id::integer = 100940;

SELECT team_id FROM teams ORDER BY team_id;

SELECT * FROM common_team_roster WHERE school = 'Connecticut';

select * from players where active_flag::integer = 1;

select player, age, exp from common_team_roster WHERE age::float <= 25 order by age;

select player, age, school from common_team_roster order by school;

select distinct school, count(*) over (partition by school) as player_count from common_team_roster order by player_count DESC;

select distinct exp, count(*) over (partition by exp) as count from common_team_roster order by count DESC;

select player, exp from common_team_roster where exp = 'R' order by player;

select distinct age, count(*) over (partition by age) as count from common_team_roster order by age DESC;

SELECT t.team_city, t.team_name, ctr.* from common_team_roster ctr join teams t on ctr.teamid = t.team_id;

SELECT t.team_city, t.team_name, ctr.player, ctr.player_id from common_team_roster ctr join teams t on ctr.teamid = t.team_id WHERE t.team_name='Sky';

SELECT game_id, player_name, matchup, pts, reb, ast, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct FROM player_game_logs where game_id = 1022400146 order by game_date ;

SELECT * FROM shot_chart_detail;

SELECT * FROM players WHERE player_name like '%Hull%';

SELECT * FROM team_game_logs WHERE team_abbreviation = 'SEA';

SELECT * FROM team_game_logs WHERE game_id = '1022400147';

SELECT DISTINCT game_id FROM team_game_logs;

SELECT count(*) FROM common_team_roster;

SELECT count(*) FROM players WHERE active_flag::integer = 1;

select ctr.player_id, ctr.player, p.player_id, p.player_name from common_team_roster ctr LEFT JOIN players p USING (player_id) WHERE p.player_id is NULL;

SELECT * FROM common_team_roster where player_id::integer = 1641698;

select team_id, matchup, game_id, game_date from team_game_logs order by game_id desc, game_date desc;

select player_id from common_team_roster;

SELECT DISTINCT game_id FROM team_game_logs;

SELECT * FROM player_game_logs where player_id = 1630149;

select * from player_career_stats WHERE player_id::integer = 1642288;

select p.player_name, pcs.* from player_career_stats pcs join players p using (player_id) WHERE player_id::integer = 204365;

select count(distinct game_id) from wnba_data_user.boxscore_player_stats;

select count(distinct player_id) from wnba_data_user.boxscore_player_stats;

select count(distinct game_id) from wnba_data_user.shot_chart_detail;

select count(distinct player_id) from wnba_data_user.shot_chart_detail;

select count(distinct game_id) from wnba_data_user.player_game_logs;

select count(distinct player_id) from wnba_data_user.player_game_logs;

select * from wnba_data_user.player_game_logs where min::float < 5 order by min asc;

select * from shot_chart_detail where game_id::integer = 1022400135;

select game_id, count(game_event_id) as game_events from shot_chart_detail group by game_id order by game_events desc;

SELECT player_id FROM common_team_roster ORDER BY player_id;

SELECT distinct player_id FROM wnba_data_user.player_game_logs ORDER BY player_id;

SELECT DISTINCT player_name FROM wnba_data_user.shot_chart_detail ORDER by player_name;
