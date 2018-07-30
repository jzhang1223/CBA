-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: cbaDB
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CashFlow`
--

DROP TABLE IF EXISTS `CashFlow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CashFlow` (
  `cfID` int(11) NOT NULL AUTO_INCREMENT,
  `fundID` varchar(255) DEFAULT NULL,
  `cfDate` date DEFAULT NULL,
  `cashValue` int(11) DEFAULT NULL,
  `typeID` int(11) NOT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cfID`),
  KEY `fundID` (`fundID`),
  KEY `cashflow_ibfk_2` (`typeID`),
  CONSTRAINT `cashflow_ibfk_1` FOREIGN KEY (`fundID`) REFERENCES `fund` (`fundid`),
  CONSTRAINT `cashflow_ibfk_2` FOREIGN KEY (`typeID`) REFERENCES `cashflowtype` (`typeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CashFlow`
--

LOCK TABLES `CashFlow` WRITE;
/*!40000 ALTER TABLE `CashFlow` DISABLE KEYS */;
/*!40000 ALTER TABLE `CashFlow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `cashflowjointype`
--

DROP TABLE IF EXISTS `cashflowjointype`;
/*!50001 DROP VIEW IF EXISTS `cashflowjointype`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `cashflowjointype` AS SELECT 
 1 AS `typeID`,
 1 AS `cfID`,
 1 AS `fundID`,
 1 AS `cfDate`,
 1 AS `cashValue`,
 1 AS `notes`,
 1 AS `result`,
 1 AS `useCase`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `CashFlowType`
--

DROP TABLE IF EXISTS `CashFlowType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CashFlowType` (
  `typeID` int(11) NOT NULL AUTO_INCREMENT,
  `result` enum('Distribution','Contribution','Balance') DEFAULT NULL,
  `useCase` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`typeID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CashFlowType`
--

LOCK TABLES `CashFlowType` WRITE;
/*!40000 ALTER TABLE `CashFlowType` DISABLE KEYS */;
INSERT INTO `CashFlowType` VALUES (1,'Contribution','Expenses'),(2,'Contribution','Investment'),(3,'Contribution','Subject to Recall'),(4,'Contribution','Return of Capital'),(5,'Distribution','Standard'),(6,'Distribution','Subject to Recall'),(7,'Distribution','Return of Capital'),(8,'Distribution','Income'),(9,'Balance','Quarterly Valuation'),(10,'Balance','Initial Commitment'),(11,'Distribution','Expenses');
/*!40000 ALTER TABLE `CashFlowType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fund`
--

DROP TABLE IF EXISTS `Fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fund` (
  `fundID` varchar(255) NOT NULL,
  PRIMARY KEY (`fundID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fund`
--

LOCK TABLES `Fund` WRITE;
/*!40000 ALTER TABLE `Fund` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'cbaDB'
--
/*!50003 DROP FUNCTION IF EXISTS `capitalCalled` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `capitalCalled`(fund VARCHAR(255), endDate DATE) RETURNS int(11)
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `capitalCommited` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `capitalCommited`(fund VARCHAR(255)) RETURNS int(11)
    DETERMINISTIC
BEGIN
		RETURN (SELECT SUM(cashValue) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND
                    useCase = 'Initial Commitment');

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `nextQtr` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `nextQtr`(fund VARCHAR(255), endDate DATE) RETURNS date
    DETERMINISTIC
BEGIN
		RETURN (SELECT MAX(cfDate) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate >= endDate AND 
                    useCase = 'Quarterly Valuation');
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `previousQtr` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `previousQtr`(fund VARCHAR(255), endDate DATE) RETURNS date
    DETERMINISTIC
BEGIN
		RETURN (SELECT MAX(cfDate) 
				FROM `CashFlowJoinType`
                WHERE fundID = fund AND 
					cfDate < endDate AND 
                    useCase = 'Quarterly Valuation');

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `remainingCommitment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `remainingCommitment`(fund VARCHAR(255), endDate DATE) RETURNS int(11)
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

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `cashflowjointype`
--

/*!50001 DROP VIEW IF EXISTS `cashflowjointype`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `cashflowjointype` AS select `cashflow`.`typeID` AS `typeID`,`cashflow`.`cfID` AS `cfID`,`cashflow`.`fundID` AS `fundID`,`cashflow`.`cfDate` AS `cfDate`,`cashflow`.`cashValue` AS `cashValue`,`cashflow`.`notes` AS `notes`,`cashflowtype`.`result` AS `result`,`cashflowtype`.`useCase` AS `useCase` from (`cashflow` join `cashflowtype` on((`cashflow`.`typeID` = `cashflowtype`.`typeID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-30 11:52:25
