CREATE DATABASE  IF NOT EXISTS `gestion_seguridad` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `gestion_seguridad`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: gestion_seguridad
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `activo`
--

DROP TABLE IF EXISTS `activo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activo` (
  `activo_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `tipo_activo_id` int DEFAULT NULL,
  PRIMARY KEY (`activo_id`),
  KEY `fk_tipo_activo_id` (`tipo_activo_id`),
  CONSTRAINT `fk_tipo_activo_id` FOREIGN KEY (`tipo_activo_id`) REFERENCES `tipo_activo` (`tipo_activo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activo`
--

LOCK TABLES `activo` WRITE;
/*!40000 ALTER TABLE `activo` DISABLE KEYS */;
INSERT INTO `activo` VALUES (27,'Base de dato',4),(28,'Computador',4),(29,'Televisor',1),(30,'Router',11),(31,'Controles',5),(32,'Servidor',7),(33,'Monitor',9);
/*!40000 ALTER TABLE `activo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activo_amenaza`
--

DROP TABLE IF EXISTS `activo_amenaza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activo_amenaza` (
  `activo_amenaza_id` int NOT NULL AUTO_INCREMENT,
  `activo_id` int DEFAULT NULL,
  `amenaza_id` int DEFAULT NULL,
  `valoracion_amenaza_id` int DEFAULT NULL,
  PRIMARY KEY (`activo_amenaza_id`),
  KEY `fk_activo_id` (`activo_id`),
  KEY `fk_tipo_amenaza_id` (`amenaza_id`),
  KEY `fk_valoracion_amenazas_id_idx` (`valoracion_amenaza_id`),
  CONSTRAINT `fk_activo_id` FOREIGN KEY (`activo_id`) REFERENCES `activo` (`activo_id`),
  CONSTRAINT `fk_tipo_amenaza_id` FOREIGN KEY (`amenaza_id`) REFERENCES `amenaza` (`amenaza_id`),
  CONSTRAINT `fk_valoracion_amenazas_id` FOREIGN KEY (`valoracion_amenaza_id`) REFERENCES `valoracion_amenazas` (`valoracion_amenazas_id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activo_amenaza`
--

LOCK TABLES `activo_amenaza` WRITE;
/*!40000 ALTER TABLE `activo_amenaza` DISABLE KEYS */;
INSERT INTO `activo_amenaza` VALUES (128,27,1,3),(129,27,2,5),(130,27,10,2),(131,28,4,3),(132,28,12,1),(133,28,45,1),(134,28,28,1),(135,29,1,1),(136,30,34,1),(137,30,1,1),(138,30,2,1),(139,31,17,1),(140,31,15,1),(141,32,2,1),(142,32,7,2),(143,32,15,3),(144,33,4,1);
/*!40000 ALTER TABLE `activo_amenaza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activo_escala_valor`
--

DROP TABLE IF EXISTS `activo_escala_valor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activo_escala_valor` (
  `activo_escala_valor_id` int NOT NULL AUTO_INCREMENT,
  `detalle_valor_id` int DEFAULT NULL,
  `escala_valor_id` int DEFAULT NULL,
  `activo_amenaza_id` int DEFAULT NULL,
  PRIMARY KEY (`activo_escala_valor_id`),
  KEY `fk_activo_escala_valor` (`escala_valor_id`),
  KEY `fk_valor_id` (`detalle_valor_id`),
  KEY `fk_activo_tipo_amenaza_id_idx` (`activo_amenaza_id`),
  CONSTRAINT `fk_activo_tipo_amenaza_id` FOREIGN KEY (`activo_amenaza_id`) REFERENCES `activo_amenaza` (`activo_amenaza_id`),
  CONSTRAINT `fk_valor_id` FOREIGN KEY (`detalle_valor_id`) REFERENCES `detalle_valor` (`detalle_valor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=419 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activo_escala_valor`
--

LOCK TABLES `activo_escala_valor` WRITE;
/*!40000 ALTER TABLE `activo_escala_valor` DISABLE KEYS */;
INSERT INTO `activo_escala_valor` VALUES (368,3,1,128),(369,2,1,128),(370,1,1,128),(371,3,2,129),(372,2,2,129),(373,1,2,129),(374,3,3,130),(375,2,3,130),(376,1,3,130),(377,3,3,131),(378,2,3,131),(379,1,2,131),(380,3,3,132),(381,2,4,132),(382,1,4,132),(383,3,2,133),(384,2,3,133),(385,1,1,133),(386,3,3,134),(387,2,3,134),(388,1,3,134),(389,3,1,135),(390,2,1,135),(391,1,1,135),(392,3,1,136),(393,2,1,136),(394,1,1,136),(395,3,1,137),(396,2,1,137),(397,1,1,137),(398,3,1,138),(399,2,1,138),(400,1,1,138),(401,3,1,139),(402,2,1,139),(403,1,1,139),(404,3,1,140),(405,2,1,140),(406,1,1,140),(407,3,3,141),(408,2,3,141),(409,1,3,141),(410,3,2,142),(411,2,3,142),(412,1,1,142),(413,3,1,143),(414,2,1,143),(415,1,1,143),(416,3,3,144),(417,2,3,144),(418,1,3,144);
/*!40000 ALTER TABLE `activo_escala_valor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activo_salvaguarda`
--

DROP TABLE IF EXISTS `activo_salvaguarda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activo_salvaguarda` (
  `activo_salvaguarda_id` int NOT NULL AUTO_INCREMENT,
  `salvaguarda_id` int NOT NULL,
  `valoracion_salvaguarda_id` int NOT NULL,
  `activo_amenaza_id` int DEFAULT NULL,
  PRIMARY KEY (`activo_salvaguarda_id`),
  KEY `fk_salvaguarda_id_idx` (`salvaguarda_id`),
  KEY `fk_valoracion_salvaguarda_id_idx` (`valoracion_salvaguarda_id`),
  KEY `fk_activosalvaguarda_activo_amenaza_id_idx` (`activo_amenaza_id`),
  CONSTRAINT `fk_activosalvaguarda_activo_amenaza_id` FOREIGN KEY (`activo_amenaza_id`) REFERENCES `activo_amenaza` (`activo_amenaza_id`),
  CONSTRAINT `fk_salvaguarda_id` FOREIGN KEY (`salvaguarda_id`) REFERENCES `salvaguarda` (`salvaguarda_id`),
  CONSTRAINT `fk_valoracion_salvaguarda_id` FOREIGN KEY (`valoracion_salvaguarda_id`) REFERENCES `valoracion_salvaguarda` (`valoracion_salvaguarda_id`)
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activo_salvaguarda`
--

LOCK TABLES `activo_salvaguarda` WRITE;
/*!40000 ALTER TABLE `activo_salvaguarda` DISABLE KEYS */;
INSERT INTO `activo_salvaguarda` VALUES (124,44,4,128),(125,89,5,129),(126,46,2,130),(127,41,2,131),(128,41,5,132),(129,35,1,133),(130,21,4,134),(131,18,5,135),(132,18,1,136),(133,18,1,137),(134,18,1,138),(135,18,1,139),(136,18,1,140),(137,52,2,141),(138,64,5,142),(139,18,1,143),(140,43,2,144);
/*!40000 ALTER TABLE `activo_salvaguarda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `amenaza`
--

DROP TABLE IF EXISTS `amenaza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenaza` (
  `amenaza_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `tipo_amenaza_id` int DEFAULT NULL,
  PRIMARY KEY (`amenaza_id`),
  KEY `fk_amenaza_id` (`tipo_amenaza_id`),
  CONSTRAINT `fk_amenaza_id` FOREIGN KEY (`tipo_amenaza_id`) REFERENCES `tipo_amenaza` (`tipo_amenaza_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenaza`
--

LOCK TABLES `amenaza` WRITE;
/*!40000 ALTER TABLE `amenaza` DISABLE KEYS */;
INSERT INTO `amenaza` VALUES (1,'[N.1] Fuego',1),(2,'[N.2] Daños por agua',1),(3,'[N.*] Desastres naturales',1),(4,'[I.1] Fuego',2),(5,'[I.2] Daños por agua',2),(6,'[I.*] Desastres industriales',2),(7,'[I.3] Contaminación mecánica',2),(8,'[I.4] Contaminación electromagnética',2),(9,'[I.5] Avería de origen físico o lógico',2),(10,'[I.6] Corte del suministro eléctrico',2),(11,'[I.7] Condiciones inadecuadas de temperatura o humedad',2),(12,'[I.8] Fallo de servicios de comunicaciones',2),(13,'[I.9] Interrupción de otros servicios y suministros esenciales',2),(14,'[I.10] Degradación de los soportes de almacenamiento de la información',2),(15,'[I.11] Emanaciones electromagnéticas',2),(16,'[E.1] Errores de los usuarios',3),(17,'[E.2] Errores del administrador',3),(18,'[E.3] Errores de monitorización',3),(19,'[E.4] Errores de configuración',3),(20,'[E.7] Deficiencias en la organización',3),(21,'[E.8] Difusión de software dañino',3),(22,'[E.9] Errores de [re-]encaminamiento',3),(23,'[E.10] Errores de secuencia',3),(24,'[E.14] Escapes de información',3),(25,'[E.15] Alteración accidental de la información',3),(26,'[E.18] Destrucción de información',3),(27,'[E.19] Fugas de información',3),(28,'[E.20] Vulnerabilidades de los programas (software)',3),(29,' [E.21] Errores de mantenimiento / actualización de programas (software)',3),(30,'[E.23] Errores de mantenimiento / actualización de equipos (hardware)',3),(31,'[E.24] Caída del sistema por agotamiento de recursos',3),(32,'[E.25] Pérdida de equipos',3),(33,'[E.28] Indisponibilidad del personal',3),(34,'[A.3] Manipulación de los registros de actividad (log)',4),(35,'[A.4] Manipulación de la configuración',4),(36,'[A.5] Suplantación de la identidad del usuario',4),(37,'[A.6] Abuso de privilegios de acceso',4),(38,'[A.7] Uso no previsto ',4),(39,'[A.8] Difusión de software dañino',4),(40,'[A.9] [Re-]encaminamiento de mensajes',4),(41,'[A.10] Alteración de secuencia',4),(42,'[A.11] Acceso no autorizado',4),(43,'[A.12] Análisis de tráfico',4),(44,'[A.13] Repudio',4),(45,'[A.14] Interceptación de información (escucha)',4),(46,'[A.15] Modificación deliberada de la información',4),(47,'[A.18] Destrucción de información',4),(48,'[A.19] Divulgación de información',4),(49,'[A.22] Manipulación de programas',4),(50,'[A.23] Manipulación de los equipos',4),(51,'[A.24] Denegación de servicio',4),(52,'[A.25] Robo',4),(53,'[A.26] Ataque destructivo',4),(54,'[A.27] Ocupación enemiga',4),(55,'[A.28] Indisponibilidad del persona',4),(56,'[A.29] Extorsión',4),(57,'[A.30] Ingeniería social (picaresca)',4);
/*!40000 ALTER TABLE `amenaza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_valor`
--

DROP TABLE IF EXISTS `detalle_valor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_valor` (
  `detalle_valor_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`detalle_valor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_valor`
--

LOCK TABLES `detalle_valor` WRITE;
/*!40000 ALTER TABLE `detalle_valor` DISABLE KEYS */;
INSERT INTO `detalle_valor` VALUES (1,'[D] Disponibilidad'),(2,'[I] Integridad'),(3,'[C] Confidencialidad');
/*!40000 ALTER TABLE `detalle_valor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `escala_valor`
--

DROP TABLE IF EXISTS `escala_valor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escala_valor` (
  `escala_valor_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `valor` int DEFAULT NULL,
  PRIMARY KEY (`escala_valor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `escala_valor`
--

LOCK TABLES `escala_valor` WRITE;
/*!40000 ALTER TABLE `escala_valor` DISABLE KEYS */;
INSERT INTO `escala_valor` VALUES (1,'Bajo',1),(2,'Medio',2),(3,'Alto',3),(4,'Ninguna',0);
/*!40000 ALTER TABLE `escala_valor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumen_activo_amenaza`
--

DROP TABLE IF EXISTS `resumen_activo_amenaza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resumen_activo_amenaza` (
  `resumen_antes_salvaguarda_id` int NOT NULL AUTO_INCREMENT,
  `activo_amenaza_id` int NOT NULL,
  `riesgo_potencial` decimal(18,2) NOT NULL,
  `impacto_potencial` decimal(18,2) NOT NULL,
  `riesgo_residual` decimal(18,2) DEFAULT NULL,
  `impacto_residual` decimal(18,2) DEFAULT NULL,
  PRIMARY KEY (`resumen_antes_salvaguarda_id`),
  KEY `fk_resumenantes_activoamenaza_id_idx` (`activo_amenaza_id`),
  CONSTRAINT `fk_resumenantes_activoamenaza_id` FOREIGN KEY (`activo_amenaza_id`) REFERENCES `activo_amenaza` (`activo_amenaza_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumen_activo_amenaza`
--

LOCK TABLES `resumen_activo_amenaza` WRITE;
/*!40000 ALTER TABLE `resumen_activo_amenaza` DISABLE KEYS */;
INSERT INTO `resumen_activo_amenaza` VALUES (1,128,3.00,3.00,1.20,1.20),(2,129,0.06,6.00,0.00,1.20),(3,130,90.00,9.00,72.00,7.20),(4,131,8.00,8.00,6.40,6.40),(5,132,300.00,3.00,60.00,0.60),(6,133,600.00,6.00,600.00,6.00),(7,134,900.00,9.00,360.00,3.60),(8,135,300.00,3.00,60.00,0.60),(9,136,300.00,3.00,300.00,3.00),(10,137,300.00,3.00,300.00,3.00),(11,138,300.00,3.00,300.00,3.00),(12,139,300.00,3.00,300.00,3.00),(13,140,300.00,3.00,300.00,3.00),(14,141,900.00,9.00,720.00,7.20),(15,142,60.00,6.00,12.00,1.20),(16,143,3.00,3.00,3.00,3.00),(17,144,900.00,9.00,720.00,7.20);
/*!40000 ALTER TABLE `resumen_activo_amenaza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salvaguarda`
--

DROP TABLE IF EXISTS `salvaguarda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salvaguarda` (
  `salvaguarda_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo_salvaguarda_id` int DEFAULT NULL,
  PRIMARY KEY (`salvaguarda_id`),
  KEY `fk_tipo_salvaguarda_id_idx` (`tipo_salvaguarda_id`),
  CONSTRAINT `fk_tipo_salvaguarda_id` FOREIGN KEY (`tipo_salvaguarda_id`) REFERENCES `tipo_salvaguarda` (`tipo_salvaguarda_id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salvaguarda`
--

LOCK TABLES `salvaguarda` WRITE;
/*!40000 ALTER TABLE `salvaguarda` DISABLE KEYS */;
INSERT INTO `salvaguarda` VALUES (18,'Protecciones Generales',1),(19,'Identificación y autenticación',1),(20,'Control de acceso lógico',1),(21,'Segregación de tareas',1),(22,'Gestión de incidencias',1),(23,'Herramientas de seguridad',1),(24,'Herramienta contra código dañino',1),(25,'Herramienta de detección / prevención de intrusión',1),(26,'Herramienta de chequeo de configuración',1),(27,'Herramienta de análisis de vulnerabilidades',1),(28,'Herramienta de monitorización de tráfico',1),(29,'Herramienta de monitorización de contenidos',1),(30,'Herramienta para análisis de logs',1),(31,'Honey net / honey pot',1),(32,'Verificación de las funciones de seguridad',1),(33,'Gestión de vulnerabilidades',1),(34,'Registro y auditoría',1),(35,'Protección de la Información',2),(36,'Copias de seguridad de los datos (backup)',2),(37,'Aseguramiento de la integridad',2),(38,'Cifrado de la información',2),(39,'Uso de firmas electrónicas',2),(40,'Uso de servicios de fechado electrónico (time stamping)',2),(41,'Gestión de claves criptográficas',3),(42,'Gestión de claves de cifra de información',3),(43,'Gestión de claves de firma de información',3),(44,'Gestión de claves para contenedores criptográficos',3),(45,'Gestión de claves de comunicaciones',3),(46,'Gestión de certificados',3),(47,'Protección de los Servicios',4),(48,'Aseguramiento de la disponibilidad',4),(49,'Aceptación y puesta en operación',4),(50,'Se aplican perfiles de seguridad',4),(51,'Explotación',4),(52,'Gestión de cambios (mejoras y sustituciones)',4),(53,'Terminación',4),(54,'Protección de servicios y aplicaciones web',4),(55,'Protección del correo electrónico',4),(56,'Protección del directorio',4),(57,'Protección del servidor de nombres de dominio (DNS)',4),(58,'Teletrabajo',4),(59,'Voz sobre IP',4),(60,'Protección de las Aplicaciones Informáticas',5),(61,'Copias de seguridad (backup)',5),(62,'Puesta en producción',5),(63,'Se aplican perfiles de seguridad',5),(64,'Explotación / Producción',5),(65,'Cambios (actualizaciones y mantenimiento)',5),(66,'Terminación',5),(67,'Protección de los Equipos Informáticos',6),(68,'Puesta en producción',6),(69,'Se aplican perfiles de seguridad',6),(70,'Aseguramiento de la disponibilidad',6),(71,'Operación',6),(72,'Cambios (actualizaciones y mantenimiento)',6),(73,'Terminación',6),(74,'Informática móvil',6),(75,'Reproducción de documentos',6),(76,'Protección de la centralita telefónica (PABX)',6),(77,'Protección de las Comunicaciones',7),(78,'Entrada en servicio',7),(79,'Se aplican perfiles de seguridad',7),(80,'Aseguramiento de la disponibilidad',7),(81,'Autenticación del canal',7),(82,'Protección de la integridad de los datos intercambiados',7),(83,'Protección criptográfica de la confidencialidad de los datos intercambiados',7),(84,'Operación',7),(85,'Cambios (actualizaciones y mantenimiento)',7),(86,'Terminación',7),(87,'Internet: uso de acceso a',7),(88,'Seguridad Wireless (WiFi)',7),(89,'Telefonía móvil',7),(90,'Segregación de las redes en dominios',7),(91,'Puntos de interconexión: conexiones entre zonas de confianza',8),(92,'Sistema de protección perimetral',8),(93,'Protección de los equipos de frontera',8),(94,'Protección de los Soportes de Información',9),(95,'Aseguramiento de la disponibilidad',9),(96,'Protección criptográfica del contenido',9),(97,'Limpieza de contenidos',9),(98,'Destrucción de soportes',9),(99,'Elementos Auxiliares',10),(100,'Aseguramiento de la disponibilidad',10),(101,'Instalación',10),(102,'Suministro eléctrico',10),(103,'Climatización',10),(104,'Protección del cableado',10),(105,'Protección de las Instalaciones',11),(106,'Diseño',11),(107,'Defensa en profundidad',11),(108,'Control de los accesos físicos',11),(109,'Aseguramiento de la disponibilidad',11),(110,'Terminación',11),(111,'Gestión del Personal',12),(112,'Formación y concienciación',12),(113,'Aseguramiento de la disponibilidad',12),(114,'Organización',13),(115,'Gestión de riesgos',13),(116,'Planificación de la seguridad',13),(117,'Inspecciones de seguridad',13),(118,'Continuidad del negocio',14),(119,'Análisis de impacto (BIA)',14),(120,'Plan de Recuperación de Desastres (DRP)',14),(121,'Relaciones Externas',15),(122,'Acuerdos para intercambio de información y software',15),(123,'Acceso externo',15),(124,'Servicios proporcionados por otras organizaciones',15),(125,'Personal subcontratado',15),(126,'Adquisición / desarrollo',16),(127,'Servicios: Adquisición o desarrollo',16),(128,'Aplicaciones: Adquisición o desarrollo',16),(129,'Equipos: Adquisición o desarrollo',16),(130,'Comunicaciones: Adquisición o contratación',16),(131,'Soportes de Información: Adquisición',16),(132,'Productos certificados o acreditados',16);
/*!40000 ALTER TABLE `salvaguarda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_activo`
--

DROP TABLE IF EXISTS `tipo_activo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_activo` (
  `tipo_activo_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tipo_activo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_activo`
--

LOCK TABLES `tipo_activo` WRITE;
/*!40000 ALTER TABLE `tipo_activo` DISABLE KEYS */;
INSERT INTO `tipo_activo` VALUES (1,'[info] Activos esenciales: información'),(2,'[service] Activos esenciales: Servicio'),(3,'[D] Datos/Informacion'),(4,'[K] Claves criptograficas'),(5,'[S] Servicios'),(6,'[SW] Software - Aplicaciones informaticas'),(7,'[HW] Equipamiento Informatico (Hardware)'),(8,'[COM] Redes de comunicaciones'),(9,'[Media] Soportes de Informacion'),(10,'[Aux] Equipamiento auxiliar'),(11,'[L] Instalaciones'),(12,'[P] Personal');
/*!40000 ALTER TABLE `tipo_activo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_amenaza`
--

DROP TABLE IF EXISTS `tipo_amenaza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_amenaza` (
  `tipo_amenaza_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tipo_amenaza_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_amenaza`
--

LOCK TABLES `tipo_amenaza` WRITE;
/*!40000 ALTER TABLE `tipo_amenaza` DISABLE KEYS */;
INSERT INTO `tipo_amenaza` VALUES (1,'[N] Desastres naturales '),(2,'[I] De origen industrial '),(3,'[E] Errores y fallos no intencionados'),(4,'[A] Ataques intencionados');
/*!40000 ALTER TABLE `tipo_amenaza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_salvaguarda`
--

DROP TABLE IF EXISTS `tipo_salvaguarda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_salvaguarda` (
  `tipo_salvaguarda_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`tipo_salvaguarda_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_salvaguarda`
--

LOCK TABLES `tipo_salvaguarda` WRITE;
/*!40000 ALTER TABLE `tipo_salvaguarda` DISABLE KEYS */;
INSERT INTO `tipo_salvaguarda` VALUES (1,'Protecciones generales u horizontales'),(2,'Protección de los datos / información'),(3,'Protección de las claves criptográficas'),(4,'Protección de los servicios'),(5,'Protección de las aplicaciones (software)'),(6,'Protección de los equipos (hardware)'),(7,'Protección de las comunicaciones'),(8,'Protección en los puntos de interconexión con otros sistemas'),(9,'Protección de los soportes de información'),(10,'Protección de los elementos auxiliares'),(11,'Seguridad física – Protección de las instalaciones'),(12,'Salvaguardas relativas al personal'),(13,'Salvaguardas de tipo organizativo'),(14,'Continuidad de operaciones'),(15,'Externalización'),(16,'Adquisición y desarrollo');
/*!40000 ALTER TABLE `tipo_salvaguarda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valoracion_amenazas`
--

DROP TABLE IF EXISTS `valoracion_amenazas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valoracion_amenazas` (
  `valoracion_amenazas_id` int NOT NULL AUTO_INCREMENT,
  `opciones` varchar(45) NOT NULL,
  `probabilidad` decimal(18,2) NOT NULL,
  `criterio` varchar(45) NOT NULL,
  PRIMARY KEY (`valoracion_amenazas_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valoracion_amenazas`
--

LOCK TABLES `valoracion_amenazas` WRITE;
/*!40000 ALTER TABLE `valoracion_amenazas` DISABLE KEYS */;
INSERT INTO `valoracion_amenazas` VALUES (1,'Muy frecuente (MF)',100.00,'A diario'),(2,'Frecuente (F)',10.00,'Mensualmente'),(3,'Normal (N)',1.00,'Una vez al año'),(4,'Poco frecuente (PF)',0.10,'Cada varios años'),(5,'Muy poco frecuente (MPF)',0.01,'Siglos');
/*!40000 ALTER TABLE `valoracion_amenazas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valoracion_salvaguarda`
--

DROP TABLE IF EXISTS `valoracion_salvaguarda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valoracion_salvaguarda` (
  `valoracion_salvaguarda_id` int NOT NULL AUTO_INCREMENT,
  `factor` decimal(18,2) NOT NULL,
  `nivel` varchar(45) NOT NULL,
  PRIMARY KEY (`valoracion_salvaguarda_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valoracion_salvaguarda`
--

LOCK TABLES `valoracion_salvaguarda` WRITE;
/*!40000 ALTER TABLE `valoracion_salvaguarda` DISABLE KEYS */;
INSERT INTO `valoracion_salvaguarda` VALUES (1,0.00,'L0 Inexistente'),(2,0.20,'L1 Inicial'),(3,0.40,'L2 Reproducible'),(4,0.60,'L3 Proceso definido'),(5,0.80,'L4 Gestionado y medible'),(6,1.00,'L5 Optimizado');
/*!40000 ALTER TABLE `valoracion_salvaguarda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'gestion_seguridad'
--

--
-- Dumping routines for database 'gestion_seguridad'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-19 18:53:17
