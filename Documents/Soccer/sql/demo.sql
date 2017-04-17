
-- display the competitions a team participates in
SELECT * FROM team_competitions('real madrid');
-- search for competiton by name (caption)
SELECT * FROM search_competition('Primera Division 2016/17');
-- search for team by name
SELECT * FROM search_team('manchester');
-- search for manager by name
SELECT * FROM search_manager('zidane');
-- search for player by name
SELECT * FROM search_player('cristiano ronaldo');
-- search for stadium by name or team
SELECT * FROM search_stadium('santiago');
SELECT * FROM search_stadium('manchester united');
-- view the standings in a competiton or
SELECT * FROM view_standings('ac milan');
SELECT * FROM view_standings('Serie A 2016/17');
-- view the teams participating in a competition
SELECT * FROM teams_in_competition('Champions League 2016/17');
-- view all fixtures of a team
SELECT * FROM fixture_by('real madrid');
