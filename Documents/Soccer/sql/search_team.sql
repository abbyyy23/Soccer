CREATE OR REPLACE FUNCTION public.search_team(IN team_name text)
RETURNS TABLE(code character varying,
              name character varying,
              squad_market_value character varying,
              manager_name character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT t.code,
           t.name,
           t.squad_market_value,
           m.name
     FROM team as t
     JOIN manager as m ON m.team_id = t.id
     WHERE LOWER(t.name) ~ LOWER(team_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
