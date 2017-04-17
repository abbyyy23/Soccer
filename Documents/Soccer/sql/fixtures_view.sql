CREATE OR REPLACE VIEW fixture_view AS
SELECT fixture.id,
competition.caption AS competition,
(SELECT name FROM team WHERE team.id = fixture_team.home_team) AS home,
(SELECT name FROM team WHERE team.id = fixture_team.away_team) AS away,
fixture.status AS status,
fixture.date,
fixture.matchday,
result.goals_home,
result.goals_away,
result.odds_home_win,
result.odds_away_win
FROM team
JOIN fixture_team ON fixture_team.home_team = team.id
JOIN fixture ON fixture.id = fixture_team.id
JOIN competition ON competition.id = fixture.competition_id
JOIN result ON result.fixture_id = fixture.id
