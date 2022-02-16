# GSU
Repository for my Econ Master program


SELECT DATE_PART('year', created) AS Year, DATE_PART('month', created) AS Month, DATE_PART('day',created) AS Day, COUNT(*) AS obs FROM wsb_submissions GROUP BY DATE_PART('day', created), DATE_PART('month', created), DATE_PART('year', created) ORDER BY Year, Month, Day;
