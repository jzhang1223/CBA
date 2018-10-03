USE test;

SELECT DISTINCT(Activity) FROM historicaltransactions
ORDER BY Activity asc;


SELECT DISTINCT Activity FROM historicalTransactions
ORDER BY Activity;
SELECT COUNT(DISTINCT Fund) Fund FROM historicalTransactions;
SELECT * FROM historicalTransactions;


# Extracts Contribution Values bucketed by year and quarter
# view: `historicalContributions`
SELECT Fund, YEAR(Date) AS cfYear, QUARTER(Date) AS cfQuarter, -SUM(`cash_In/Out`) AS total
FROM historicalTransactions
WHERE Activity LIKE '%CC%'
GROUP BY cfYear, cfQuarter, Fund
ORDER BY Fund ASC, cfYear ASC, cfQuarter ASC;
select * from `historicalContributions`;
#**** There are some gaps in the quarters for each year. When retrieving from the table, try and check for the year and qtr first.


# Extracts Distribution Values bucketed by year and quarter
# view: `historicalDistributions`
SELECT Fund, YEAR(Date) AS cfYear, QUARTER(Date) AS cfQuarter, SUM(`cash_In/Out`) AS total
FROM historicalTransactions
WHERE Activity LIKE '%DD%'
GROUP BY cfYear, cfQuarter, Fund
ORDER BY Fund ASC, cfYear ASC, cfQuarter ASC;

select * from `historicalDistributions`;

# Extracts individual adjustment data

SELECT * 
FROM historicalTransactions 
WHERE Activity LIKE '%Adj%' OR Activity LIKE '%Update%';

# Selects the last Market_Value item for each quarter
# view: `historicalNav`
SELECT t1.cfDate, cfYear, cfQuarter, t1.Fund, Market_Value
FROM(SELECT Year(Date) AS cfYear, QUARTER(Date) AS cfQuarter, MAX(Date) as cfDate, Fund
    FROM historicalTransactions
    WHERE Market_Value > 0
    GROUP BY cfYear, cfQuarter, Fund) as t1
INNER JOIN (SELECT Market_Value, Date as cfDate, Fund
    FROM historicalTransactions) AS t2 ON (t1.cfDate = t2.cfDate AND t1.Fund = t2.Fund)
ORDER BY Fund ASC, cfYear ASC, cfQuarter;
    
select * from `historicalNav`;
    
    
    
SELECT COUNT(DISTINCT DATE) FROM historicalTransactions;
SELECT COUNT(DATE) FROM historicalTransactions;
SELECT COUNT(*) FROM historicalTransactions
WHERE DATE IS NULL;
SELECT COUNT(*) FROM historicalTransactions
WHERE Activity LIKE '%DD%';

SELECT hn.cfYear, hn.cfQuarter, hn.Fund, Market_Value, hd.total AS Distributions, hc.total AS Contributions
FROM `historicalNav` AS hn 
    JOIN `historicalDistributions` AS hd 
    #ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
        JOIN `historicalContributions` AS hc
        #ON(hc.cfYear = hd.cfYear AND hc.Fund = hd.Fund AND hc.cfQuarter = hd.cfQuarter)
ORDER BY hn.Fund, hn.cfYear, hn.cfQuarter;

SELECT hn.cfYear, hn.cfQuarter, hn.Fund, Market_Value, hd.total AS Distributions, hc.total AS Contributions
FROM `historicalNav` AS hn 
    LEFT JOIN `historicalDistributions` AS hd
        ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
        LEFT JOIN `historicalContributions` AS hc
            ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
        /*
    UNION
    
    SELECT hn1.cfYear, hn1.cfQuarter, hn1.Fund, Market_Value, hd1.total AS Distributions
    FROM `historicalNav` AS hn1 
    RIGHT JOIN `historicalDistributions` AS hd1
        ON(hn1.cfYear = hd1.cfYear AND hn1.Fund = hd1.Fund AND hn1.cfQuarter = hd1.cfQuarter)
        */

        
ORDER BY hn.Fund, hn.cfYear, hn.cfQuarter;

/*
### Used for setting up the historical transaction table.
UPDATE historicaltransactions 
SET Date = NULL 
WHERE Date = ''
*/

/*
### Used to extract funds with netted contribution and distribution transactions.
SELECT * FROM historicalTransactions
WHERE Activity LIKE '%C%' AND Activity LIKE '%D%'
ORDER BY Fund;
*/

/*
### Deleted funds with netted contribution and distribution transactions.
DELETE FROM historicalTransactions
WHERE Fund LIKE '%ABRY%';
*/

/*
# Fixed the 2 PEP transactions that had D#% instead of DD#%
UPDATE historicalTransactions
SET Activity = CONCAT('D', Activity)
WHERE Activity LIKE 'D#%';
*/