TABLE common_team_roster;
TABLE dataset_info;
TABLE player_career_stats;
TABLE player_game_logs;
TABLE players;
TABLE season_totals_regular_season;
TABLE shot_chart_detail;
TABLE teams;

-- Delete table data
-- DELETE FROM wnba_data_user.common_team_roster;
-- DELETE FROM wnba_data_user.dataset_info;
-- DELETE FROM wnba_data_user.player_career_stats;
-- DELETE FROM wnba_data_user.player_game_logs;
-- DELETE FROM wnba_data_user.players;
-- DELETE FROM wnba_data_user.season_totals_regular_season;
-- DELETE FROM wnba_data_user.shot_chart_detail;
-- DELETE FROM wnba_data_user.teams;

-- INSERT INTO common_team_roster VALUES
-- (1611661322, '2024', '10', 'Shakira Austin', 'Shakira', 'shakira-austin', '0', 'C-F', '6-5', '190', 'JUL 25, 2000', 23.0, '2', 'Mississippi', 1631022, None);
SELECT * FROM teams WHERE team_id::integer = 1611661329;

SELECT * FROM teams WHERE team_id::integer = 1611661323;

SELECT * FROM teams WHERE team_id::integer = 1611661330;

select * FROM players where player_id::integer = 1629497;

select * FROM players where player_id::integer = 1630150;

select * FROM common_team_roster where player_id::integer = 1629497;


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
