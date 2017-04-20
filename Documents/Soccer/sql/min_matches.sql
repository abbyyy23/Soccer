
CREATE OR REPLACE FUNCTION public.min_matches()
RETURNS TABLE(competition character varying,
              num_games integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT competition.caption,
           competition.number_of_games
    FROM competition
    WHERE  competition.number_of_games=
    (SELECT MIN(competition.number_of_games) FROM competition);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
