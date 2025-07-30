--Clear whitespace issue in the Review text coloumn 
SELECT
	ReviewID,
	CustomerID,
	ProductID,
	ReviewDate,
	Rating,
	--Clear reviewtext by replacing double spaces with singles to improve readability
	REPLACE(ReviewText,'  ',' ') As ReviewText --smplifies python usage 
FROM
	dbo.customer_reviews

