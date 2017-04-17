
CREATE OR REPLACE FUNCTION public.search_stadium(IN s_name text)
RETURNS TABLE(name character varying,
              location character varying,
              capacity integer,
              team_name character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT s.name,
           s.location,
           s.capacity,
           t.name
           FROM stadium as s
           JOIN team as t ON t.id = s.team_id
           WHERE LOWER(t.name) ~ (s_name)
           OR LOWER(s.name) ~ LOWER(s_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
