-- SELECT  replace(trim(trailing '€'from player.market_value),',','')::integer FROM player


CREATE OR REPLACE FUNCTION public.max_marketvalue()
RETURNS TABLE(player character varying,
               marketvalue integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT player.name,
           replace(trim(trailing '€'from player.market_value),',','')::integer
    FROM player
    WHERE  replace(trim(trailing '€'from player.market_value),',','')::integer =
    (SELECT MAX(replace(trim(trailing '€'from player.market_value),',','')::integer)
    FROM player);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
