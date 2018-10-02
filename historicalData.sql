USE test;
SELECT * FROM historicaltransactions;
SELECT DISTINCT Fund FROM historicalTransactions;
SELECT COUNT(DISTINCT Fund) Fund FROM historicalTransactions;



SELECT YEAR(Date) AS cfYear, quarter(Date) AS cfDate, -sum(`cash_In/Out`) as total
FROM historicalTransactions
GROUP BY cfYear, cfDate
ORDER BY cfYear asc, cfDate asc;


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