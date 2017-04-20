
-- search for competiton by name (simple query competition)
SELECT * FROM search_competition('Primera Division 2016/17');
-- search for team by name (simple query team)
SELECT * FROM search_team('manchester');
-- search for manager by name (simple query manager)
SELECT * FROM search_manager('zidane');
-- search for player by name (simple query player)
SELECT * FROM search_player('cristiano ronaldo');
-- search for stadium by name or team (simple query stadium)
SELECT * FROM search_stadium('santiago');
SELECT * FROM search_stadium('manchester united');
-- view fixtures by team (simple query fixture)
SELECT * FROM fixture_by('real madrid');
-- view the standings in a competiton or of a team (simple query league table)
SELECT * FROM view_standings('ac milan');
SELECT * FROM view_standings('Serie A 2016/17');
SELECT * FROM view_champions_standings('Paris Saint-Germain')
-- display the competitions a team participates in (comeptition team)
SELECT * FROM team_competitions('real madrid');
-- view the teams participating in a competition (competition team)
SELECT * FROM teams_in_competition('Champions League 2016/17');
-- view players in a team (team player)
SELECT * FROM players_in_team('real madrid');
-- team with most goals in a competition (league table aggregate)
SELECT * FROM most_goals('1. Bundesliga 2016/17');
-- count fixtures by status (fixture aggregate)
SELECT * FROM fixture_by_status();
-- player with the highest market value (player aggregate)
SELECT * FROM max_marketvalue();
-- manager average age(manager aggregate)
SELECT avg_age(manager.dob) FROM manager;
-- stadium with the most capacity (stadium aggregate)
SELECT * FROM max_capacity();
-- team with the highest squad market value (team aggregate)
SELECT * FROM max_squadvalue();
-- competition with the least matches (competition aggregate)
SELECT * FROM min_matches();
