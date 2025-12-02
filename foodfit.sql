-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.4.7 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando datos para la tabla users.userrs: 6 rows
DELETE FROM `userrs`;
/*!40000 ALTER TABLE `userrs` DISABLE KEYS */;
INSERT INTO `userrs` (`id`, `nombre`, `paterno`, `materno`, `correo`, `password`) VALUES
	(1, 'Luis', 'Antonio', 'Marin', ' ', ' '),
	(2, 'Jesus', '0', ' ', 'antoninoluisjesus0312@gmail.com', '123456789'),
	(3, 'Jesus', '0', ' ', 'ycam1016@gmail.com', '123456789'),
	(4, 'Antonio', '0', ' ', 'cocorrol1611@gmail.com', '123456'),
	(5, 'juanito', '0', ' ', 'juanito@gmail.com', '1234567'),
	(6, 'pepe', '0', ' ', 'pepe@gmail.com', 'pepe123');
/*!40000 ALTER TABLE `userrs` ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
