use test;
drop table if exists cashFlow, fund, cashFlowType;

create table Fund(fundID varchar(255), primary key (fundID));

create table CashFlowType(typeID int, 
	result enum('Distribution', 'Contribution'), 
	useCase varchar(255),
    primary key auto_increment (typeID)
    );
    
create table CashFlow(cfID int, 
	fundID varchar(255), 
	cfDate date, 
	cashValue int, 
	typeID int, 
    notes varchar(255),
    primary key auto_increment (cfID),
    foreign key (fundID) references fund(fundID),
    foreign key (typeID) references cashFlowType(typeID)
    );
    
insert into fund values('a1'),('python1');
select * from fund;