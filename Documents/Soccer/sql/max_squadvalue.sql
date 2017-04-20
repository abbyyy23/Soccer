
CREATE OR REPLACE FUNCTION public.max_squadvalue()
RETURNS TABLE(team character varying,
               marketvalue integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT team.name,
           replace(trim(trailing '€'from team.squad_market_value),',','')::integer
    FROM team
    WHERE  replace(trim(trailing '€'from team.squad_market_value),',','')::integer =
    (SELECT MAX(replace(trim(trailing '€'from team.squad_market_value),',','')::integer)
    FROM team);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
