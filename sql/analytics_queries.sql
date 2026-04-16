
-- ============================================================
-- AD CAMPAIGN PERFORMANCE ANALYTICS - SQL QUERIES
-- ============================================================

-- Query 1: Cohort ROAS by Campaign Type
SELECT 
    Campaign_Type,
    COUNT(*) as Ad_Count,
    ROUND(SUM(Spent), 2) as Total_Spent,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue), 2) as Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
GROUP BY Campaign_Type
ORDER BY ROAS DESC;

-- Query 2: Audience Segment ROAS Ranking
SELECT 
    age,
    gender,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS,
    RANK() OVER (ORDER BY SUM(Revenue) / NULLIF(SUM(Spent), 0) DESC) as Rank
FROM ads
WHERE Spent > 0
GROUP BY age, gender
ORDER BY ROAS DESC;

-- Query 3: Top 10 Interest Categories by ROAS
SELECT 
    interest as Interest_ID,
    COUNT(*) as Ad_Count,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
WHERE Spent > 0 AND Total_Conversion > 0
GROUP BY interest
HAVING COUNT(*) >= 5
ORDER BY ROAS DESC
LIMIT 10;

-- Query 4: Campaign Performance Summary
SELECT 
    xyz_campaign_id as Campaign,
    Campaign_Type as Type,
    SUM(Impressions) as Impressions,
    SUM(Clicks) as Clicks,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Spent), 2) as Spent,
    ROUND(SUM(Revenue), 2) as Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
GROUP BY xyz_campaign_id, Campaign_Type
ORDER BY Revenue DESC;
