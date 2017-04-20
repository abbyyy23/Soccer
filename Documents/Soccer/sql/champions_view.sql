CREATE OR REPLACE VIEW champions_view AS
SELECT 	champions_table.id,
	team.name AS team,
	champions_table.group,
	champions_table.pos,
  champions_table.p,
  champions_table.f,
  champions_table.a,
	champions_table.gd,
	champions_table.pts,
FROM champions_table
JOIN team ON team.id = league_table.team_id;
