USE cbaDB;
SELECT * FROM fund;
SELECT * FROM CashFlowType;
SELECT * FROM CashFlow;
select * from `CashFlowJoinType`;
SELECT COUNT(*) FROM CashFlow;

SHOW PROCESSLIST;

# Getting GB data accross funds
SELECT * FROM CashFlow JOIN CashFlowType USING (typeID) WHERE fundID LIKE '%gb%' ORDER BY fundID DESC;

SELECT * FROM cbadb.CashFlow WHERE typeID = 3;

SELECT * FROM CashFlow INNER JOIN CashFlowType USING (typeID) ORDER BY CFID;
SELECT * FROM CashFlow INNER JOIN CashFlowType ON(CashFlow.typeID = CashFlowType.typeID);


# Creating the view of CashFlow joined with CashFlowType
DROP VIEW IF EXISTS `CashFlowJoinType`;
CREATE VIEW `CashFlowJoinType` AS SELECT * FROM CashFlow INNER JOIN CashFlowType USING(typeID);

DROP VIEW IF EXISTS `CommitmentJoinDistribution`;
CREATE VIEW `CommitmentJoinDistribution` AS        
SELECT * FROM `CashFlowJoinType`
WHERE   (result = 'Contribution' AND
        (useCase = 'Investment' OR 
        useCase = 'Subject to Recall' OR
        useCase = 'Expenses')) OR
        (result = 'Distribution' AND
        (useCase = 'Standard' OR
        useCase = 'Return of Capital' OR
        useCase = 'Expenses'));

# INCOMPLETE TODO
DROP FUNCTION IF EXISTS calculateGrowth
DELIMITER //
CREATE FUNCTION calculateGrowth (fund VARCHAR(255), startDate DATE, endDate DATE)
	RETURNS INT
	BEGIN
		RETURN (SELECT nextQtrValue(fund, ))
		




END//
DELIMITER ;


# By default, if you are on the same date as a quarter evaluation, it will choose the CURRENT date.
# Finds the value of the previous qtr evaluation
DROP FUNCTION IF EXISTS previousQtrValue;
DELIMITER //
CREATE FUNCTION previousQtrValue (fund VARCHAR(255), endDate DATE)
	RETURNS INT
    DETERMINISTIC
	BEGIN
		RETURN (SELECT IFNULL((SELECT cashValue
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate <= endDate AND 
                    useCase = 'Quarterly Valuation'
                ORDER BY cfDate DESC
                LIMIT 1), 0));

END//
DELIMITER ;

DROP FUNCTION IF EXISTS previousQtrDate;
DELIMITER //
CREATE FUNCTION previousQtrDate (fund VARCHAR(255), endDate DATE)
	RETURNS DATE
    DETERMINISTIC
	BEGIN
		RETURN (SELECT IFNULL((SELECT MAX(cfDate)
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate <= endDate AND 
                    useCase = 'Quarterly Valuation'), '00-00-00'));

END//
DELIMITER ;

# By default, if you are on the same date as a quarter evaluation, it will NOT choose the current date
# Currently does not check for errors!
DROP FUNCTION IF EXISTS nextQtrValue;
DELIMITER //
CREATE FUNCTION nextQtrValue (fund VARCHAR(255), endDate DATE)
	RETURNS INT
    DETERMINISTIC
	BEGIN
		RETURN (SELECT cashValue
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate > endDate AND 
                    useCase = 'Quarterly Valuation'
                ORDER BY cfDate ASC
                LIMIT 1);
END//
DELIMITER ;


#Currently does not check for errors!
DROP FUNCTION IF EXISTS nextQtrDate;
DELIMITER //
CREATE FUNCTION nextQtrDate (fund VARCHAR(255), endDate DATE)
	RETURNS DATE
    DETERMINISTIC
	BEGIN
		RETURN (SELECT IFNULL((SELECT MIN(cfDate)
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate > endDate AND 
                    useCase = 'Quarterly Valuation'), '9999-12-31')) ;
END//
DELIMITER ;

DROP FUNCTION IF EXISTS remainingCommitment;
DELIMITER //
CREATE FUNCTION remainingCommitment(fund VARCHAR(255), endDate DATE)
	RETURNS INT
    DETERMINISTIC
	BEGIN
		RETURN (SELECT SUM(cashValue) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate <= endDate AND 
                    (useCase = 'Investment' OR 
					useCase = 'Subject to Recall' OR
                    useCase = 'Initial Commitment' OR
                    (cashValue < 0 AND 
						(result = 'Distribution' OR
						result = 'Contribution')
                        )));

END//
DELIMITER ;

DROP FUNCTION IF EXISTS capitalCommited;
DELIMITER //
CREATE FUNCTION capitalCommited(fund VARCHAR(255))
	RETURNS INT
    DETERMINISTIC
	BEGIN
		RETURN (SELECT SUM(cashValue) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND
                    useCase = 'Initial Commitment');

END//
DELIMITER ;

DROP FUNCTION IF EXISTS capitalCalled;
DELIMITER //
CREATE FUNCTION capitalCalled(fund VARCHAR(255), endDate DATE)
    RETURNS INT
    DETERMINISTIC
    BEGIN
        RETURN (SELECT -SUM(cashValue) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate <= endDate AND 
                    result = 'Contribution' AND
                    (useCase = 'Investment' OR 
					useCase = 'Subject to Recall' OR
                    useCase = 'Expenses'
                    #(cashValue < 0 AND 
					#	(result = 'Distribution' OR
					#	result = 'Contribution')
                    #    )
                        ));
END//
DELIMITER ;

DROP FUNCTION IF EXISTS totalDistributions;
DELIMITER //
CREATE FUNCTION totalDistributions(fund VARCHAR(255), endDate DATE)
    RETURNS INT
    DETERMINISTIC
    BEGIN
        RETURN (SELECT SUM(cashValue)
                FROM `CashFlowJoinType`
                WHERE fundID = fund AND
                cfDate <= endDate AND
                result = 'Distribution' AND
                (useCase = 'Standard' OR
                useCase = 'Return of Capital' OR
                useCase = 'Expenses'));
END//
DELIMITER ;

DROP FUNCTION IF EXISTS totalNav;
DELIMITER //
# Returns the nav for previous dates up until the previous qtr, in addition to the previous qtr, if exists
CREATE FUNCTION totalNav(fund VARCHAR(255), endDate DATE)
    RETURNS INT
    DETERMINISTIC
    BEGIN
        RETURN (SELECT IFNULL(
                    (SELECT -SUM(cashValue)
                    FROM `CashFlowJoinType`
                    WHERE fundID = fund AND
                    cfDate <= endDate AND
                    cfDate > previousQtrDate(fund, endDate) AND
                    (useCase = 'Investment' OR
                    useCase = 'Standard' OR
                    useCase = 'Return of Capital' OR
                    useCase = 'Income')), 0) +
                    (SELECT previousQtrValue(fund, endDate)));
END//
DELIMITER ;
                



use cbaDB;
select remainingCommitment('CCDD062016AF', '18/4/2');
select capitalCommited('CCDD062016AF');
select capitalCalled('CCDD062016AF', '18/4/2');
select totalDistributions('CCDD062016AF', '18/4/2');
select totalNav('CCDD062016AF', '18/4/2');
select totalNav('CCDD062016AF', '18/3/31');
select previousQtr('CCDD062016AF', '18/4/2');
SELECT nextQtr('CCDD062016AF', '18/4/2');
                
                

# Was and still is dropped b/c can't return a table directly
DROP PROCEDURE IF EXISTS irrCashFlows;
DELIMITER //
CREATE PROCEDURE irrCashFlows(fund VARCHAR(255), endDate DATE)
BEGIN
    SELECT cfDate, cashValue FROM `CommitmentJoinDistribution`
    WHERE fundID = fund AND 
            cfDate <= endDate
    UNION
    (SELECT (SELECT cfDate FROM `CommitmentJoinDistribution`
                WHERE fundID = fund AND cfDate <= endDate ORDER BY cfDate DESC LIMIT 1) as cfDate,
            totalNav(fund,endDate) as cashValue) order by cfDate ASC;
END//
DELIMITER ;



        
        
        
select cfID from CashFlow as cf union all select fundID from Fund order by cfID;
        
