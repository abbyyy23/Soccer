
CREATE OR REPLACE FUNCTION public.fixture_by_status()
RETURNS TABLE(fixture_status character varying,
              num bigint)
AS $function$
BEGIN
    RETURN QUERY
    SELECT fixture.status, COUNT(*)
    FROM fixture
    GROUP BY fixture.status;
END;
$function$ LANGUAGE 'plpgsql' STABLE;
