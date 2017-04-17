
CREATE OR REPLACE FUNCTION public.search_manager(IN manager_name text)
RETURNS TABLE(name character varying,
              dob date,
              nationality character varying,
              team_name character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT m.name,
           m.dob,
           m.nationality,
           t.name
    FROM manager as m
    JOIN team as t ON t.id = m.team_id
    WHERE LOWER(m.name) ~ (manager_name)
END;
$function$ LANGUAGE 'plpgsql' STABLE;
