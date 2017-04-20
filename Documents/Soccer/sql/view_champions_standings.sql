CREATE OR REPLACE FUNCTION public.view_champions_standings(IN search_name text)
RETURNS TABLE(team character varying,
              group character,
              pos integer,
              f integer,
              a integer,
              gd integer,
              pts integer
  AS $function$
  BEGIN
      RETURN QUERY
      SELECT champions_view.team AS team,
    	champions_view.group::character,
    	champions_view.pos,
      champions_view.p,
      champions_view.f,
      champions_view.a,
    	champions_view.gd,
    	champions_view.pts
      FROM champions_view
      WHERE LOWER(champions_view.team) ~ LOWER(search_name);
      END;
      $function$ LANGUAGE 'plpgsql' STABLE;
