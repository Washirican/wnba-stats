TABLE common_team_roster;

SELECT * FROM common_team_roster;

DELETE FROM common_team_roster;

INSERT INTO common_team_roster VALUES
(1611661322, '2024', '10', 'Shakira Austin', 'Shakira', 'shakira-austin', '0', 'C-F', '6-5', '190', 'JUL 25, 2000', 23.0, '2', 'Mississippi', 1631022, None);

SELECT * FROM common_team_roster WHERE school = 'Connecticut';

select * from players where active_flag::integer = 1;

select player, age, exp from common_team_roster WHERE age::float <= 25 order by age;

select player, age, school from common_team_roster order by school;

select distinct school, count(*) over (partition by school) as player_count from common_team_roster order by player_count DESC;

select distinct exp, count(*) over (partition by exp) as count from common_team_roster order by count DESC;

select player, exp from common_team_roster where exp = 'R' order by player;

select distinct age, count(*) over (partition by age) as count from common_team_roster order by age DESC;
