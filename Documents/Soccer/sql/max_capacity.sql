
CREATE OR REPLACE FUNCTION public.max_capacity()
RETURNS TABLE(stadium character varying,
              team character varying,
              capacity float)
AS $function$
BEGIN
    RETURN QUERY
    SELECT stadium.name,
           team.name,
           stadium.capacity
    FROM stadium
    JOIN team ON team.id = stadium.team_id
    WHERE  stadium.capacity=
    (SELECT MAX(stadium.capacity) FROM stadium);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
