--Common table exstension to find and tag duplicate records
WITH DuplicateRecords AS (
	SELECT
		JourneyID,
		CustomerID,
		ProductID,
		VisitDate,
		Stage, --Where in the customer journey we find ourselves 
		Action,--The action taken by a customer such as clicking and liking
		Duration,
		ROW_NUMBER() OVER (
			--Partition uniqe groups and number of occurences 
			PARTITION BY CustomerID,ProductID,VisitDate,Stage,Action
			ORDER BY JourneyID
		) AS row_num --Numbers each row with own partition, row_num > 1 is a excact duplicate
	FROM
		dbo.customer_journey
)
--Verification query
SELECT * 
FROM DuplicateRecords
WHERE row_num > 1
ORDER BY JourneyID

--Remove duplicates and fix NULL durations with a sub query (This is going into BI)
SELECT
	JourneyID,
	CustomerID,
	ProductID,
	VisitDate,
	Stage,
	Action,
	COALESCE(Duration,avg_Duration) As Duration --Replaces NULL durations with the average duration for each date
FROM
	(
	SELECT
		JourneyID,
		CustomerID,
		ProductID,
		VisitDate,
		UPPER(Stage) As Stage, --Upper to have standardization
		Action,
		Duration,
		AVG(Duration) OVER (PARTITION BY VisitDate) As avg_duration,
		ROW_NUMBER() OVER(
			PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action
			ORDER BY JourneyID
			) As row_num
		FROM
			dbo.customer_journey
	) As sub_query 
WHERE 
	row_num = 1; --Keeps only the first apperance of data and now with avg_duration for a day instead of NULL