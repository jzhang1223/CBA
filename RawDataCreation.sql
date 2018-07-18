USE cbaDB;
DROP TABLE IF EXISTS cashFlow, fund, cashFlowType;

CREATE TABLE Fund(
	fundID VARCHAR(255), 
    PRIMARY KEY(fundID));

CREATE TABLE CashFlowType(
	typeID INT DEFAULT 0, 
	result ENUM('Distribution', 'Contribution'), 
	useCase VARCHAR(255),
    PRIMARY KEY AUTO_INCREMENT(typeID)
    );
    
CREATE TABLE CashFlow(
	cfID INT DEFAULT 0, 
	fundID VARCHAR(255), 
	cfDate DATE, 
	cashValue INT, 
	typeID INT, 
    notes VARCHAR(255),
    PRIMARY KEY AUTO_INCREMENT(cfID),
    FOREIGN KEY (fundID) REFERENCES fund(fundID),
    FOREIGN KEY (typeID) REFERENCES cashFlowType(typeID)
    );
    
SELECT * FROM fund;
SELECT * FROM CashFlowType;
SELECT * FROM CashFlow;


