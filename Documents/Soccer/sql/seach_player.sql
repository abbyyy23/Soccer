
CREATE OR REPLACE FUNCTION public.search_player(IN player_name text)
RETURNS TABLE(name character varying,
              age integer,
              contract_until date,
              player_position character varying,
              jersey_number character varying,
              market_value character varying,
              nationality character varying,
              team_name character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT p.name,
           EXTRACT(YEAR FROM (AGE(p.dob::timestamp))) AS age, 
           p.contract_until,
           p.position,
           p.jersey_number,
           p.market_value,
           p.nationality,
           t.name
     FROM player as p
     JOIN team as t ON t.id = p.team_id
     WHERE LOWER(p.name) ~ LOWER(player_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
