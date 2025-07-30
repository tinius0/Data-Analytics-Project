
SELECT
	EngagementID,
	ContentID,
	CampaignID,
	UPPER(REPLACE(ContentType,'Socialmedia','Social Media')) As ContentType,
	LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined)-1) As Views,--Extracts the views
	Right(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-',ViewsClicksCombined)) As Clicks, --Extracts the clicks
	Likes,
	FORMAT(CONVERT(DATE,EngagementDate), 'dd.MM.yy') As EngagmentDate --Convert from American formatting to european

FROM
	dbo.engagement_data
WHERE
	ContentType != 'NewsLetter'; --NewsLetter not relevant, as its not a hired campagin 