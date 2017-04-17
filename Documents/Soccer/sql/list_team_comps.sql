
CREATE OR REPLACE FUNCTION public.team_competitions(IN team_name text)
RETURNS TABLE(name character varying,
              caption character varying,
              league character varying,
              number_of_teams integer,
              year integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT team.name,
           c.caption,
           c.league,
           c.number_of_teams,
           c.year
    FROM team
    JOIN competition_team AS ct ON ct.team_id = team.id
    JOIN competition AS c ON c.id = ct.competition_id
    WHERE  LOWER(team.name )~ LOWER(team_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
