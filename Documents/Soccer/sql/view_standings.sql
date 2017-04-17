
CREATE OR REPLACE FUNCTION public.view_standings(IN search_name text)
RETURNS TABLE(competition character varying,
              team character varying,
              pos integer,
              p integer,
              w integer,
              d integer,
              l integer,
              f integer,
              hw integer,
              hl integer,
              hga integer,
              aw integer,
              al integer,
              ad integer,
              agf integer,
              aga integer,
              gd integer,
              pts integer)
AS $function$
BEGIN
    RETURN QUERY
    SELECT
    l.competition,
    l.team,
    l.p,
    l.w,
    l.d,
    l.l,
    l.f,
    l.hw,
    l.hl,
    l.hga,
    l.aw,
    l.al,
    l.ad,
    l.agf,
    l.aga,
    l.gd,
    l.pts
    FROM league_table_view as l
    WHERE LOWER(l.competition) ~ LOWER(search_name)
    OR LOWER(l.team) ~ LOWER(search_name);
END;
$function$ LANGUAGE 'plpgsql' STABLE;
