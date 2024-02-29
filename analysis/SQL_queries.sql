--Count the nb of releases per seller
SELECT
	seller_name,
	COUNT(*) AS releases_nb
FROM catalogue_old
GROUP BY
	seller_name
ORDER BY 
	releases_nb DESC;

--Calculate the proportion of each genre  
WITH sub AS(
	SELECT
		DISTINCT genre,
		COUNT(release_id) OVER (PARTITION BY genre) AS count_genres,
		COUNT(release_id) OVER () AS count_total
	FROM catalogue_old
	)
SELECT
	genre,
	count_genres,
	ROUND(count_genres::decimal/count_total,2) AS genre_proportion
FROM sub
ORDER BY genre_proportion DESC;

--Calculate the avg price per genre
WITH 
	subquery AS (
		SELECT
			DISTINCT genre,
			COUNT(release_id) OVER (PARTITION BY genre) AS nb_releases,
			ROUND((AVG(price) OVER (PARTITION BY genre))::decimal,2) AS avg_per_genre,
			ROUND((AVG(price) OVER ())::decimal,2) AS global_avg
		FROM catalogue_old)

SELECT *
FROM subquery
WHERE nb_releases >= 1000
ORDER BY avg_per_genre DESC;

--Calculate the avg price per genre and media condition and compare it to the global avg price
WITH 
	subquery AS(
		SELECT
			DISTINCT genre,
			media_condition,
			COUNT(release_id) OVER (PARTITION BY genre, media_condition) AS releases_nb,
			ROUND((AVG(price) OVER (PARTITION BY genre, media_condition))::decimal,2) AS avg,
			ROUND((AVG(price) OVER ())::decimal,2) AS global_avg
		FROM catalogue_old)

SELECT *
FROM subquery
WHERE releases_nb >= 1000
ORDER BY avg DESC;

--Explore release_date
SELECT
	DISTINCT release_date,
	COUNT(release_id) OVER (PARTITION BY release_date)
FROM catalogue_old
ORDER BY release_date NULLS FIRST;
#executed in 125 ms

SELECT
	release_date,
	COUNT(release_id)
FROM catalogue_old
GROUP BY release_date
ORDER BY release_date NULLS FIRST;
#executed in 32 ms

--Decade function
CREATE OR REPLACE FUNCTION public.decade(release_date character varying) RETURNS character varying LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN 
    	CASE
			WHEN release_date::int BETWEEN 1950 AND 1959 THEN '1950s'
			WHEN release_date::int BETWEEN 1960 AND 1969 THEN '1960s'
			WHEN release_date::int BETWEEN 1970 AND 1979 THEN '1970s'
			WHEN release_date::int BETWEEN 1980 AND 1989 THEN '1980s'
			WHEN release_date::int BETWEEN 1990 AND 1999 THEN '1990s'
			WHEN release_date::int BETWEEN 2000 AND 2009 THEN '2000s'
			WHEN release_date::int BETWEEN 2010 AND 2019 THEN '2010s'
			WHEN release_date::int BETWEEN 2020 AND 2029 THEN '2020s'
			ELSE NULL
		 END;
END;
$function$
;
#
ChatGPT
#The records from the 1920s and 1930s were excluded because their quantity is negligible. The decade is null for these records.

--Proportion of discs in decades
WITH 
	subquery AS(
		SELECT
			DISTINCT public.decade(release_date) AS decade,
			COUNT(*) OVER (PARTITION BY public.decade(release_date)) AS count,
			COUNT(*) OVER () AS global_count
		FROM catalogue_old
		ORDER BY decade NULLS FIRST
		)
SELECT
	decade,
	ROUND(count::decimal/global_count,2) AS proportion
FROM subquery
ORDER BY proportion DESC;

--Avg price by decade
WITH
	sub AS(
		SELECT
			public.decade(release_date) AS decade,
			COUNT(release_id)AS count,
			ROUND(AVG(price)::decimal,2) AS avg
		FROM catalogue_old
		GROUP BY decade
		)
SELECT
	*
FROM sub
WHERE count >= 1000
ORDER BY avg DESC;

--Calculate the avg price per genre, media condition and decade and compare it to the global avg price
WITH 
	subquery AS(
		SELECT
			DISTINCT genre,
			media_condition,
			public.decade(release_date) AS decade,
			COUNT(release_id) OVER (PARTITION BY genre, media_condition, public.decade(release_date)) AS releases_nb,
			ROUND((AVG(price) OVER (PARTITION BY genre, media_condition, public.decade(release_date)))::decimal,2) AS avg,
			ROUND((AVG(price) OVER ())::decimal,2) AS global_avg
		FROM catalogue_old)

SELECT *
FROM subquery
WHERE 
	releases_nb >= 500 AND decade IS NOT NULL
ORDER BY avg DESC;











