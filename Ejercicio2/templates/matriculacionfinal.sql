-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 16-11-2023 a las 00:31:05
-- Versión del servidor: 5.7.39
-- Versión de PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `matriculacionfinal`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agencia`
--

CREATE DATABASE IF NOT EXISTS `matriculacionfinal` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `matriculacionfinal`;



CREATE TABLE `agencia` (
  `id` tinyint(3) UNSIGNED NOT NULL,
  `descripcion` varchar(30) COLLATE utf8_spanish2_ci NOT NULL,
  `direccion` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `telefono` varchar(15) COLLATE utf8_spanish2_ci NOT NULL,
  `horainicio` time NOT NULL,
  `horafin` time NOT NULL,
  `foto` varchar(20) COLLATE utf8_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `agencia`
--

INSERT INTO `agencia` (`id`, `descripcion`, `direccion`, `telefono`, `horainicio`, `horafin`, `foto`) VALUES
(1, 'Los Chillos', 'Los Chillos, Gnral. Rumiñahui', '099 980 7371', '09:00:00', '16:30:00', 'chillos.webp'),
(2, 'Cotocollao', 'Bicentenario, Parque Bicentenario', '023952300', '08:30:00', '15:30:00', 'bicentenario.jpg'),
(3, 'Quitumbe', 'Florida Alta,  Calle Alcantaras', '022254151', '09:00:00', '16:30:00', 'guajalo.jpg'),
(4, 'Florida', 'Guajalo, Av Pucará y Mariscal Sucre', '022254151', '08:00:00', '16:00:00', 'floridaAlta.jpg'),
(5, 'Carapungo', 'San Isidro del Inca, De los Guayabos ', '022402436', '07:00:00', '15:00:00', 'inca.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `color`
--

CREATE TABLE `color` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `descripcion` varchar(50) COLLATE utf8_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `color`
--

INSERT INTO `color` (`id`, `descripcion`) VALUES
(2, 'Negro'),
(3, 'Rojo'),
(4, 'Azul'),
(5, 'Plomo'),
(6, 'Verde'),
(7, 'Negro'),
(8, 'Plata'),
(9, 'Morado'),
(10, 'Naranja');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `descripcion` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `pais` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `direccion` varchar(16) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `foto` varchar(20) COLLATE utf8_spanish2_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`id`, `descripcion`, `pais`, `direccion`, `foto`) VALUES
(1, 'Chévrolet', 'USA', 'Michigan', 'chevrolet.jpg'),
(2, 'Fiat', 'Italia', 'Turin', 'fiat.jpg'),
(4, 'Great Wall', 'China', 'Baoding', 'GreatWall.jpg'),
(5, 'Toyota', 'Japón', 'Aichi', 'toyota.jpg'),
(6, 'Volkswagen', 'Alemania', 'Stadtmitte', 'volkswagen.jpg'),
(7, 'Honda', 'Japón', 'Tokio', 'honda.jpg'),
(8, 'Ford', 'USA', 'Michigan', 'ford.jpg'),
(9, 'Nissan', 'Japón', 'Yakohama', 'nissan.jpg'),
(10, 'Renault', 'Francia', 'Billancourt', 'renault.jpg'),
(11, 'Hyundai', 'Corea del Sur', 'Seul', 'hyundai.jpg'),
(12, 'BMW', 'Alemania', 'Munich', 'bmw.jpg'),
(13, 'Mercedes-Benz', 'Alemania', 'Stuttgart', 'mercedes.jpg'),
(14, 'Audi', 'Alemania', 'Ingolstadt', 'audi.jpg'),
(15, 'Kia', 'Corea del Sur', 'Seul', 'kia.jpg'),
(16, 'Mazda', 'Japón', 'Hiroshima', 'mazda.jpg'),
(17, 'Volvo', 'Suecia', 'Gotemburgo', 'volvo.jpg'),
(18, 'Peugeot', 'Francia', 'Malmaison', 'peugeot.jpg'),
(19, 'Subaru', 'Japón', 'Tokio', 'subaru.jpg'),
(20, 'Jeep', 'USA', 'Hills', 'jeep.jpg'),
(21, 'CHANGAN', 'EEUU', 'CHANGAN', 'changan.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matricula`
--

CREATE TABLE `matricula` (
  `id` int(10) UNSIGNED NOT NULL,
  `fecha` date NOT NULL,
  `vehiculo` mediumint(8) UNSIGNED NOT NULL,
  `agencia` tinyint(3) UNSIGNED NOT NULL,
  `anio` year(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `matricula`
--

INSERT INTO `matricula` (`id`, `fecha`, `vehiculo`, `agencia`, `anio`) VALUES
(2, '2023-05-19', 5, 1, 2018),
(3, '2023-05-19', 5, 1, 2019),
(4, '2023-05-19', 5, 1, 2000),
(6, '2023-05-26', 5, 5, 2023);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `placa` char(7) COLLATE utf8_spanish2_ci NOT NULL,
  `marca` smallint(5) UNSIGNED NOT NULL,
  `motor` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `chasis` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `combustible` enum('Gasolina','Diesel','Eléctrico') COLLATE utf8_spanish2_ci NOT NULL,
  `anio` year(4) NOT NULL,
  `color` smallint(5) UNSIGNED NOT NULL,
  `foto` varchar(20) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `avaluo` decimal(8,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`id`, `placa`, `marca`, `motor`, `chasis`, `combustible`, `anio`, `color`, `foto`, `avaluo`) VALUES
(5, 'PCH3465', 5, 'dede', 'Dede', 'Eléctrico', 2017, 3, 'toyota_celeste.jpg', '25415.00'),
(6, 'PHH2354', 4, 'sswe', 'eddede', 'Gasolina', 1980, 3, 'BMW_Azul.jpg', '23541.36'),
(7, 'CHH3465', 10, 'edcdede', 'Dedede', 'Gasolina', 2017, 9, 'Ferrari_negro.jpg', '25412.00'),
(8, 'HGF1234', 12, 'abcd', '1234', 'Eléctrico', 2020, 6, 'Honda_Rojo.jpg', '30000.00'),
(9, 'AAA666', 7, 'QWERTYU', 'ASDFGH', 'Gasolina', 2023, 3, 'KOtIaNbdxjhK.jpg', '55000.00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agencia`
--
ALTER TABLE `agencia`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `color`
--
ALTER TABLE `color`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `matricula`
--
ALTER TABLE `matricula`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehiculo` (`vehiculo`),
  ADD KEY `agencia` (`agencia`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `marca` (`marca`),
  ADD KEY `color` (`color`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `agencia`
--
ALTER TABLE `agencia`
  MODIFY `id` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `color`
--
ALTER TABLE `color`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `matricula`
--
ALTER TABLE `matricula`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `matricula`
--
ALTER TABLE `matricula`
  ADD CONSTRAINT `matricula_agencia` FOREIGN KEY (`agencia`) REFERENCES `agencia` (`id`),
  ADD CONSTRAINT `matricula_vehiculo` FOREIGN KEY (`vehiculo`) REFERENCES `vehiculo` (`id`);

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `vehiculo_color` FOREIGN KEY (`color`) REFERENCES `color` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vehiculo_marca` FOREIGN KEY (`marca`) REFERENCES `marca` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
