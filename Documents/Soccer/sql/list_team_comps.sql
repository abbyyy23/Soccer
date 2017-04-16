BEGIN
    RETURN QUERY
    SELECT team.name,
           team.squad_market_value,
           c.caption,
           c.league,
           c.number_of_teams,
           c.year
    FROM team
    JOIN competition_team AS ct ON ct.team_id = team.id
    JOIN competition AS c ON c.id = ct.competition_id
    WHERE  LOWER(team.name )~ LOWER(team_name);
END;
