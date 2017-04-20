
CREATE OR REPLACE FUNCTION public.most_goals(IN competition_name text)
RETURNS TABLE(team character varying,
              number_goals integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT league_table_view.team,
           league_table_view.f
    FROM league_table_view
    WHERE  league_table_view.f = (SELECT MAX(league_table_view.f) FROM league_table_view
    WHERE LOWER(league_table_view.competition )~ LOWER(competition_name));
END;
$function$ LANGUAGE 'plpgsql' STABLE;
