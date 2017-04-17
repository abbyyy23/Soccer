CREATE OR REPLACE VIEW league_table_view AS
SELECT 	league_table.id,
	competition.caption AS competition,
	team.name AS team,
	league_table.pos,
	league_table.p,
  league_table.w,
  league_table.d,
  league_table.l,
	league_table.f,
	league_table.a,
	league_table.hw,
	league_table.hl,
	league_table.hga,
	league_table.aw,
  league_table.al,
  league_table.ad,
  league_table.agf,
  league_table.aga,
  league_table.gd,
  league_table.pts
FROM league_table
JOIN team ON team.id = league_table.team_id
JOIN competition ON competition.id = league_table.competition_id;
