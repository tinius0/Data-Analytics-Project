--Query to categorize products based on their price
--Can be used to clarify which categories a company sells the most of
SELECT 
	ProductID,
	ProductName,
	Price,
	--Everything is under the sports category, redundant here

	CASE -- Define prices as low, medium or high
		WHEN Price < 50 then 'Low' 
		WHEN Price BETWEEN 50 AND 200 then 'Medium'
		ELSE 'High'
	END AS PriceCategory --Creates the new Coloumn as PriceCategory 

FROM 
	dbo.products
