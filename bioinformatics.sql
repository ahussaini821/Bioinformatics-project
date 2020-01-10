-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bioinformatics
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table ` inhibitors`
--

DROP TABLE IF EXISTS ` inhibitors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE ` inhibitors` (
  `id inhibitors` int(11) NOT NULL AUTO_INCREMENT,
  ` inhibitors name` varchar(45) NOT NULL,
  `kinase name` varchar(45) NOT NULL,
  `Chemical Structure` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id inhibitors`),
  UNIQUE KEY `id inhibitors_UNIQUE` (`id inhibitors`),
  UNIQUE KEY ` inhibitors name_UNIQUE` (` inhibitors name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table ` inhibitors`
--

LOCK TABLES ` inhibitors` WRITE;
/*!40000 ALTER TABLE ` inhibitors` DISABLE KEYS */;
/*!40000 ALTER TABLE ` inhibitors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `basic  information`
--

DROP TABLE IF EXISTS `basic  information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `basic  information` (
  `idbasic  information` int(11) NOT NULL AUTO_INCREMENT,
  `kinase name` varchar(45) NOT NULL,
  `protein name` varchar(45) NOT NULL,
  `protein family` varchar(45) NOT NULL,
  `kinase target` varchar(45) NOT NULL,
  `location of the gene in the chromosomes` varchar(45) DEFAULT NULL,
  `kinase sequence` varchar(45) DEFAULT NULL,
  `protein domains` varchar(45) DEFAULT NULL,
  `protein structure` varchar(45) DEFAULT NULL,
  `target functions` varchar(45) DEFAULT NULL,
  `target residues` varchar(45) DEFAULT NULL,
  `target residue location` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idbasic  information`),
  UNIQUE KEY `idbasic  information_UNIQUE` (`idbasic  information`),
  UNIQUE KEY `kinase name_UNIQUE` (`kinase name`),
  UNIQUE KEY `protein name_UNIQUE` (`protein name`),
  KEY `3_idx` (`protein family`),
  KEY `target_idx` (`kinase target`),
  CONSTRAINT `family` FOREIGN KEY (`protein family`) REFERENCES `search one to more family` (`protein family`),
  CONSTRAINT `one to one 2` FOREIGN KEY (`protein name`) REFERENCES `search one to one` (`protein name`),
  CONSTRAINT `one to one1` FOREIGN KEY (`kinase name`) REFERENCES `search one to one` (`kinase name`),
  CONSTRAINT `target` FOREIGN KEY (`kinase target`) REFERENCES `search one to more kinase target` (`kinase target`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basic  information`
--

LOCK TABLES `basic  information` WRITE;
/*!40000 ALTER TABLE `basic  information` DISABLE KEYS */;
/*!40000 ALTER TABLE `basic  information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship more to more`
--

DROP TABLE IF EXISTS `relationship more to more`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relationship more to more` (
  `idrelationship more to more` int(11) NOT NULL AUTO_INCREMENT,
  ` inhibitors` varchar(45) NOT NULL,
  `kinase name` varchar(45) NOT NULL,
  `protein name` varchar(45) NOT NULL,
  PRIMARY KEY (`idrelationship more to more`),
  KEY `more to more 1_idx` (` inhibitors`),
  KEY `more to more 2_idx` (`kinase name`),
  KEY `more to more 3_idx` (`protein name`),
  CONSTRAINT `more to more 1` FOREIGN KEY (` inhibitors`) REFERENCES ` inhibitors` (` inhibitors name`),
  CONSTRAINT `more to more 2` FOREIGN KEY (`kinase name`) REFERENCES `basic  information` (`kinase name`),
  CONSTRAINT `more to more 3` FOREIGN KEY (`protein name`) REFERENCES `basic  information` (`protein name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship more to more`
--

LOCK TABLES `relationship more to more` WRITE;
/*!40000 ALTER TABLE `relationship more to more` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship more to more` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search one to more family`
--

DROP TABLE IF EXISTS `search one to more family`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search one to more family` (
  `idsearch one to more` int(11) NOT NULL AUTO_INCREMENT,
  `protein family` varchar(45) NOT NULL,
  PRIMARY KEY (`idsearch one to more`),
  UNIQUE KEY `idsearch one to more_UNIQUE` (`idsearch one to more`),
  UNIQUE KEY `protein family_UNIQUE` (`protein family`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search one to more family`
--

LOCK TABLES `search one to more family` WRITE;
/*!40000 ALTER TABLE `search one to more family` DISABLE KEYS */;
/*!40000 ALTER TABLE `search one to more family` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search one to more kinase target`
--

DROP TABLE IF EXISTS `search one to more kinase target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search one to more kinase target` (
  `idsearch one to more kinase target` int(11) NOT NULL AUTO_INCREMENT,
  `kinase target` varchar(45) NOT NULL,
  `target functions` varchar(45) DEFAULT NULL,
  `target residues` varchar(45) DEFAULT NULL,
  `target residue location` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idsearch one to more kinase target`),
  UNIQUE KEY `idsearch one to more kinase target_UNIQUE` (`idsearch one to more kinase target`),
  UNIQUE KEY `kinase target_UNIQUE` (`kinase target`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search one to more kinase target`
--

LOCK TABLES `search one to more kinase target` WRITE;
/*!40000 ALTER TABLE `search one to more kinase target` DISABLE KEYS */;
/*!40000 ALTER TABLE `search one to more kinase target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search one to one`
--

DROP TABLE IF EXISTS `search one to one`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search one to one` (
  `idsearch one to one` int(11) NOT NULL AUTO_INCREMENT,
  `kinase name` varchar(45) NOT NULL,
  `protein name` varchar(45) NOT NULL,
  PRIMARY KEY (`idsearch one to one`),
  UNIQUE KEY `kinase name_UNIQUE` (`kinase name`),
  UNIQUE KEY `protein name_UNIQUE` (`protein name`),
  UNIQUE KEY `idsearch one to one_UNIQUE` (`idsearch one to one`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search one to one`
--

LOCK TABLES `search one to one` WRITE;
/*!40000 ALTER TABLE `search one to one` DISABLE KEYS */;
INSERT INTO `search one to one` VALUES (1,'name','name');
/*!40000 ALTER TABLE `search one to one` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-11  0:42:32
