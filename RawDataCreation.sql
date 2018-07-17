USE cbaDB;
DROP TABLE IF EXISTS cashFlow, fund, cashFlowType;

CREATE TABLE Fund(
	fundID VARCHAR(255), 
    PRIMARY KEY(fundID));

CREATE TABLE CashFlowType(
	typeID INT, 
	result ENUM('Distribution', 'Contribution'), 
	useCase VARCHAR(255),
    PRIMARY KEY AUTO_INCREMENT(typeID)
    );
    
CREATE TABLE CashFlow(
	cfID INT, 
	fundID VARCHAR(255), 
	cfDate DATE, 
	cashValue INT, 
	typeID INT, 
    notes VARCHAR(255),
    PRIMARY KEY AUTO_INCREMENT (cfID),
    FOREIGN KEY (fundID) REFERENCES fund(fundID),
    FOREIGN KEY (typeID) REFERENCES cashFlowType(typeID)
    );
    
INSERT INTO fund VALUES('a1'),('python1');
INSERT INTO CashFlowType (result, useCase) VALUES ('Contribution', 'Expenses'),
								('Contribution', 'Investment'),
                                ('Distribution', 'Standard'),
                                ('Distribution', 'Subject to Recall'),
                                ('Distribution', 'Return of Capital');
SELECT * FROM fund;
SELECT * FROM CashFlowType;
SELECT typeID FROM CashFlowType WHERE result = 'Contribution' AND useCase = 'Investment';
SELECT * FROM CashFlow;
