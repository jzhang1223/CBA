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


# Creating the view
DROP VIEW IF EXISTS `CashFlowJoinType`;
CREATE VIEW `CashFlowJoinType` AS SELECT * FROM CashFlow INNER JOIN CashFlowType USING(typeID);


# INCOMPLETE TODO
DROP FUNCTION IF EXISTS calculateGrowth
DELIMITER //
CREATE FUNCTION calculateGrowth (fund VARCHAR(255), startDate DATE, endDate DATE)
	RETURNS INT
	BEGIN
		RETURN (SELECT nextQtrValue(fund, 
		




END//
DELIMITER ;


# By default, if you are on the same date as a quarter evaluation, it will go to a more previous date.
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
					cfDate < endDate AND 
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
					cfDate < endDate AND 
                    useCase = 'Quarterly Valuation'), '00-00-00'));

END//
DELIMITER ;

# By default, if you are on the same date as a quarter evaluation, it will choose the current date
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
					cfDate >= endDate AND 
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
					cfDate >= endDate AND 
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
                    (useCase = 'Investment' OR 
					useCase = 'Subject to Recall' OR
                    (cashValue < 0 AND 
						(result = 'Distribution' OR
						result = 'Contribution')
                        )));
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
                result = 'Distribution');
END//
DELIMITER ;

DROP FUNCTION IF EXISTS totalNav;
DELIMITER //
# Returns the nav for previous dates up until the previous qtr, in addition to the previous qtr, if exists
CREATE FUNCTION totalNav(fund VARCHAR(255), endDate DATE)
    RETURNS INT
    DETERMINISTIC
    BEGIN
        RETURN (SELECT -SUM(cashValue)
                FROM `CashFlowJoinType`
                WHERE fundID = fund AND
                cfDate <= endDate AND
                cfDate > previousQtrDate(fund, endDate) AND
                (useCase = 'Investment' OR
                useCase = 'Expenses' OR
                useCase = 'Standard' OR
                useCase = 'Return of Capital' OR
                useCase = 'Income')) +
                (SELECT previousQtrValue(fund, endDate));
END//
DELIMITER ;
                



use cbaDB;
select remainingCommitment('BCPE112014', '15/10/15');
select capitalCommited('BCPE112014');
select capitalCalled('BCPE112014', '15/10/15');
select totalDistributions('BCPE112014', '15/10/15');
select totalNav('BCPE112014', '15/10/15');
select previousQtr('BCPE112014', '15/10/15');
select ifnull((select previousQtr('BCPE112014', '11/10/15')), 3);
SELECT nextQtr('BCPE112014', '15/10/15');

