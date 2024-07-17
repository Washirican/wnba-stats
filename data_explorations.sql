TABLE common_team_roster;

TABLE teams;

TABLE player_game_logs;

table shot_chart_detail;

DELETE FROM player_game_logs;

-- INSERT INTO common_team_roster VALUES
-- (1611661322, '2024', '10', 'Shakira Austin', 'Shakira', 'shakira-austin', '0', 'C-F', '6-5', '190', 'JUL 25, 2000', 23.0, '2', 'Mississippi', 1631022, None);

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

SELECT game_id, player_name, matchup, pts, reb, ast FROM player_game_logs order by game_date;