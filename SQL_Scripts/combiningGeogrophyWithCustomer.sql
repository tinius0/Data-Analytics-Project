--Enrich customer data by combining the customer information with their geographical information
SELECT
	c.CustomerID,
	c.CustomerName,
	c.Email,
	c.Gender,
	c.Age,
	c.GeographyID,
	g.Country,
	g.City
FROM
	dbo.customers as c
LEFT JOIN
	dbo.geography g
ON
	c.GeographyID = g.GeographyID; 