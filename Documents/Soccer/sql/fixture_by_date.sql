
CREATE OR REPLACE FUNCTION public.fixture_by(IN game_day date)
RETURNS TABLE(competiton character varying,
              home character varying,
              away character varying,
              status character varying,
              game_date date,
              matchday integer,
              goals_home float,
              goals_away float,
              odds_home_win float,
              odds_away_win float
            )
AS $function$
BEGIN
    RETURN QUERY
    SELECT f.competition,
           f.home,
           f.away,
           f.status,
           f.date::timestamp::date ,
           f.matchday,
           f.goals_home,
           f.goals_away,
           f.odds_home_win,
           f.odds_away_win
    FROM fixture_view as f
    WHERE (f.date::timestamp::date) = game_day;
END;
$function$ LANGUAGE 'plpgsql' STABLE;
