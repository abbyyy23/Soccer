

CREATE OR REPLACE FUNCTION public.teams_in_competition(IN competition_name text)
RETURNS TABLE(name character varying,
              code character varying,
              squad_market_value character varying,
              competiton character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT team.name,
           team.code,
           team.squad_market_value,
           competition.caption
    FROM team
    JOIN competition_team ON competition_team.team_id = team.id
    JOIN competition ON competition.id = competition_team.competition_id
    WHERE LOWER(competition.caption) ~ LOWER(competition_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
