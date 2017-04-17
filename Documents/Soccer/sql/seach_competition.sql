CREATE OR REPLACE FUNCTION public.search_competition(IN competition_name text)
RETURNS TABLE(caption character varying,
              league character varying,
              number_of_games integer,
              number_of_matchdays integer,
              number_of_teams integer,
              year integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT c.caption,
           c.league,
           c.number_of_games,
           c.number_of_matchdays,
           c.number_of_teams,
           c.year
     FROM competition as c
     WHERE LOWER(c.caption) ~ LOWER(competition_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
