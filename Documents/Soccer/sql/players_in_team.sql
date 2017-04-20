CREATE OR REPLACE FUNCTION public.players_in_team(IN team_name text)
RETURNS TABLE(name character varying,
              age float,
              contract_until date,
              player_position character varying,
              jersey_number character varying,
              market_value character varying,
              nationality character varying)
AS $function$
BEGIN
    RETURN QUERY
    SELECT p.name,
           EXTRACT(YEAR FROM (AGE(p.dob::timestamp))) AS age,
           p.contract_until,
           p.position,
           p.jersey_number,
           p.market_value,
           p.nationality
     FROM player as p
     JOIN team as t ON t.id = p.team_id
     WHERE LOWER(t.name) ~ LOWER(team_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
