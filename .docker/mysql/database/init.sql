-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: mysql
-- Tiempo de generación: 25-11-2025 a las 00:34:40
-- Versión del servidor: 9.5.0
-- Versión de PHP: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pablogarciajcbd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `almacenes`
--

CREATE TABLE `almacenes` (
  `id` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `capacidad` int DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `almacenes`
--

INSERT INTO `almacenes` (`id`, `nombre`, `ubicacion`, `capacidad`, `activo`, `created_at`) VALUES
(1, 'AlmacÃ©n Principal', 'Calle Principal 123, Centro', 1000, 1, '2025-11-25 00:26:43'),
(2, 'AlmacÃ©n Secundario', 'Av. Comercio 456, Norte', 500, 1, '2025-11-25 00:26:43'),
(3, 'AlmacÃ©n Zona Sur', 'Calle Los Olivos 789, Sur', 750, 1, '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `activo`, `created_at`) VALUES
(1, 'ElectrÃ³nica', 'Productos electrÃ³nicos y tecnolÃ³gicos', 1, '2025-11-25 00:26:43'),
(2, 'Alimentos', 'Productos alimenticios no perecederos', 1, '2025-11-25 00:26:43'),
(3, 'Ropa', 'Prendas de vestir y accesorios', 1, '2025-11-25 00:26:43'),
(4, 'Hogar', 'ArtÃ­culos para el hogar y decoraciÃ³n', 1, '2025-11-25 00:26:43'),
(5, 'Oficina', 'Suministros y material de oficina', 1, '2025-11-25 00:26:43'),
(6, 'Deportes', 'ArtÃ­culos deportivos y fitness', 1, '2025-11-25 00:26:43'),
(7, 'Juguetes', 'Juguetes y entretenimiento infantil', 1, '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `documento` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` text,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `documento`, `telefono`, `email`, `direccion`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'CorporaciÃ³n ABC S.A.C.', '20111222333', '987111222', 'compras@abc.com', 'Av. Principal 1000, Lima', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(2, 'Distribuidora XYZ', '20222333444', '987222333', 'ventas@xyz.com', 'Jr. Comercio 500, Lima', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(3, 'Supermercados La Familia', '20333444555', '987333444', 'pedidos@lafamilia.com', 'Av. Los PrÃ³ceres 200, Lima', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(4, 'Tiendas Express', '20444555666', '987444555', 'contacto@express.com', 'Calle Lima 300, Callao', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(5, 'Comercial El Sol E.I.R.L.', '20555666777', '987123456', 'ventas@elsol.com', 'Av. Grau 800, Cercado', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(6, 'Inversiones Norte S.A.', '20666777888', '987234567', 'compras@invnorte.com', 'Jr. UniÃ³n 600, Los Olivos', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(7, 'Distribuciones del Sur', '20777888999', '987345678', 'pedidos@delsur.com', 'Av. AviaciÃ³n 1200, San Borja', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(8, 'Grupo Retail PerÃº', '20888999000', '987456789', 'contacto@retailperu.com', 'Calle Real 400, Miraflores', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(9, 'Mayoristas Asociados', '20999000111', '987567890', 'ventas@mayoristas.com', 'Jr. Cusco 300, BreÃ±a', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(10, 'Comercializadora Global', '20000111222', '987678901', 'global@comercial.com', 'Av. Colonial 2000, Callao', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(11, 'MarÃ­a LÃ³pez GarcÃ­a', '12345678', '987555666', 'mlopez@gmail.com', 'Jr. Las Flores 150, San Juan', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(12, 'JosÃ© RamÃ­rez Torres', '23456789', '987666777', 'jramirez@hotmail.com', 'Av. Los Jardines 250, Surco', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(13, 'Ana FernÃ¡ndez Ruiz', '34567890', '987777888', 'afernandez@yahoo.com', 'Calle Las Rosas 350, Miraflores', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(14, 'Carlos Mendoza Silva', '45678901', '987888999', 'cmendoza@gmail.com', 'Jr. Los Pinos 450, San Isidro', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(15, 'Patricia SÃ¡nchez Rojas', '56789012', '987999000', 'psanchez@outlook.com', 'Av. Universitaria 800, San Miguel', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(16, 'Roberto GarcÃ­a DÃ­az', '67890123', '988000111', 'rgarcia@gmail.com', 'Calle Lima 200, Pueblo Libre', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(17, 'Laura MartÃ­nez Cruz', '78901234', '988111222', 'lmartinez@hotmail.com', 'Jr. JunÃ­n 100, Magdalena', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(18, 'Fernando Torres Vega', '89012345', '988222333', 'ftorres@yahoo.com', 'Av. Brasil 1500, JesÃºs MarÃ­a', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(19, 'Carmen Flores Vargas', '90123456', '988333444', 'cflores@gmail.com', 'Calle 28 de Julio 600, Barranco', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(20, 'Diego Castillo Ramos', '01234567', '988444555', 'dcastillo@outlook.com', 'Jr. Huancayo 250, Lince', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(21, 'SofÃ­a Morales GuzmÃ¡n', '11111111', '988555666', 'smorales@gmail.com', 'Av. Javier Prado 3000, San Borja', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(22, 'Miguel Herrera Campos', '22222222', '988666777', 'mherrera@hotmail.com', 'Calle Los Tulipanes 150, Santiago', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(23, 'Isabel Romero Paredes', '33333333', '988777888', 'iromero@yahoo.com', 'Jr. Amazonas 500, Centro', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(24, 'AndrÃ©s PeÃ±a Salazar', '44444444', '988888999', 'apena@gmail.com', 'Av. La Marina 2800, San Miguel', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(25, 'Gabriela Quispe Luna', '55555555', '988999000', 'gquispe@outlook.com', 'Calle San MartÃ­n 350, Surquillo', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id` int NOT NULL,
  `numero_factura` varchar(50) DEFAULT NULL,
  `proveedor_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','completada','cancelada') DEFAULT 'pendiente',
  `notas` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`id`, `numero_factura`, `proveedor_id`, `usuario_id`, `fecha`, `total`, `estado`, `notas`, `created_at`) VALUES
(1, 'C-2024-001', 1, 2, '2024-10-01', 5850.00, 'completada', 'Compra inicial equipos electrÃ³nicos Q4', '2025-11-25 00:26:43'),
(2, 'C-2024-002', 2, 2, '2024-10-03', 2450.00, 'completada', 'ReposiciÃ³n productos alimenticios octubre', '2025-11-25 00:26:43'),
(3, 'C-2024-003', 3, 2, '2024-10-05', 3200.00, 'completada', 'Stock de ropa temporada primavera', '2025-11-25 00:26:43'),
(4, 'C-2024-004', 4, 2, '2024-10-08', 2800.00, 'completada', 'ArtÃ­culos para el hogar - colecciÃ³n nueva', '2025-11-25 00:26:43'),
(5, 'C-2024-005', 5, 2, '2024-10-10', 1890.00, 'completada', 'Material de oficina para trimestre', '2025-11-25 00:26:43'),
(6, 'C-2024-006', 1, 2, '2024-10-15', 2200.00, 'completada', 'Accesorios tecnolÃ³gicos varios', '2025-11-25 00:26:43'),
(7, 'C-2024-007', 2, 2, '2024-10-18', 1850.00, 'completada', 'Alimentos no perecederos', '2025-11-25 00:26:43'),
(8, 'C-2024-008', 3, 2, '2024-10-20', 2650.00, 'completada', 'ColecciÃ³n deportiva y casual', '2025-11-25 00:26:43'),
(9, 'C-2024-009', 4, 2, '2024-10-22', 1950.00, 'completada', 'DecoraciÃ³n y textiles hogar', '2025-11-25 00:26:43'),
(10, 'C-2024-010', 1, 2, '2024-10-25', 3450.00, 'completada', 'Equipamiento electrÃ³nico empresarial', '2025-11-25 00:26:43'),
(11, 'C-2024-011', 5, 2, '2024-11-01', 1420.00, 'completada', 'PapelerÃ­a inicio mes', '2025-11-25 00:26:43'),
(12, 'C-2024-012', 2, 3, '2024-11-03', 2180.00, 'completada', 'Stock alimentos noviembre', '2025-11-25 00:26:43'),
(13, 'C-2024-013', 1, 2, '2024-11-05', 4250.00, 'completada', 'Productos tecnolÃ³gicos premium', '2025-11-25 00:26:43'),
(14, 'C-2024-014', 3, 2, '2024-11-08', 2890.00, 'completada', 'Ropa y calzado variado', '2025-11-25 00:26:43'),
(15, 'C-2024-015', 4, 2, '2024-11-10', 2350.00, 'completada', 'Menaje y decoraciÃ³n', '2025-11-25 00:26:43'),
(16, 'C-2024-016', 5, 3, '2024-11-12', 1680.00, 'completada', 'Ãštiles escolares y oficina', '2025-11-25 00:26:43'),
(17, 'C-2024-017', 1, 2, '2024-11-15', 2950.00, 'completada', 'Juguetes campaÃ±a navideÃ±a', '2025-11-25 00:26:43'),
(18, 'C-2024-018', 2, 2, '2024-11-18', 1950.00, 'completada', 'Conservas y productos bÃ¡sicos', '2025-11-25 00:26:43'),
(19, 'C-2024-019', 3, 2, '2024-11-20', 2150.00, 'completada', 'Deportes y fitness', '2025-11-25 00:26:43'),
(20, 'C-2024-020', 1, 2, '2024-11-22', 1850.00, 'pendiente', 'Pedido accesorios fin de mes', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_compras`
--

CREATE TABLE `detalle_compras` (
  `id` int NOT NULL,
  `compra_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `detalle_compras`
--

INSERT INTO `detalle_compras` (`id`, `compra_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
(1, 1, 1, 2, 1500.00, 3000.00),
(2, 1, 2, 15, 25.00, 375.00),
(3, 1, 4, 2, 350.00, 700.00),
(4, 1, 5, 8, 60.00, 480.00),
(5, 1, 7, 6, 55.00, 330.00),
(6, 1, 11, 20, 18.00, 360.00),
(7, 1, 13, 10, 35.00, 350.00),
(8, 2, 16, 40, 12.50, 500.00),
(9, 2, 17, 30, 8.00, 240.00),
(10, 2, 18, 60, 2.50, 150.00),
(11, 2, 19, 50, 1.80, 90.00),
(12, 2, 20, 40, 15.00, 600.00),
(13, 2, 21, 35, 28.00, 980.00),
(14, 2, 23, 25, 3.20, 80.00),
(15, 3, 26, 18, 35.00, 630.00),
(16, 3, 27, 25, 45.00, 1125.00),
(17, 3, 28, 35, 18.00, 630.00),
(18, 3, 29, 12, 80.00, 960.00),
(19, 3, 30, 20, 38.00, 760.00),
(20, 3, 35, 40, 8.00, 320.00),
(21, 4, 38, 12, 45.00, 540.00),
(22, 4, 39, 18, 30.00, 540.00),
(23, 4, 40, 22, 35.00, 770.00),
(24, 4, 41, 10, 50.00, 500.00),
(25, 4, 42, 8, 85.00, 680.00),
(26, 4, 46, 14, 38.00, 532.00),
(27, 5, 48, 60, 12.00, 720.00),
(28, 5, 49, 50, 4.50, 225.00),
(29, 5, 50, 35, 6.00, 210.00),
(30, 5, 51, 12, 25.00, 300.00),
(31, 5, 52, 25, 15.00, 375.00),
(32, 5, 56, 30, 12.00, 360.00),
(33, 6, 2, 20, 25.00, 500.00),
(34, 6, 8, 15, 120.00, 1800.00),
(35, 6, 11, 25, 18.00, 450.00),
(36, 6, 12, 30, 12.00, 360.00),
(37, 6, 14, 20, 15.00, 300.00),
(38, 7, 16, 50, 12.50, 625.00),
(39, 7, 18, 80, 2.50, 200.00),
(40, 7, 19, 60, 1.80, 108.00),
(41, 7, 24, 40, 1.50, 60.00),
(42, 7, 25, 45, 12.00, 540.00),
(43, 7, 29, 30, 15.00, 450.00),
(44, 8, 28, 40, 18.00, 720.00),
(45, 8, 32, 18, 55.00, 990.00),
(46, 8, 34, 25, 22.00, 550.00),
(47, 8, 36, 15, 15.00, 225.00),
(48, 8, 58, 20, 35.00, 700.00),
(49, 8, 61, 18, 22.00, 396.00),
(50, 9, 38, 14, 45.00, 630.00),
(51, 9, 40, 18, 35.00, 630.00),
(52, 9, 43, 10, 25.00, 250.00),
(53, 9, 45, 8, 95.00, 760.00),
(54, 9, 49, 12, 28.00, 336.00),
(55, 10, 1, 3, 1500.00, 4500.00),
(56, 10, 4, 2, 350.00, 700.00),
(57, 10, 6, 5, 450.00, 2250.00),
(58, 10, 9, 4, 280.00, 1120.00),
(59, 11, 48, 45, 12.00, 540.00),
(60, 11, 49, 35, 4.50, 157.50),
(61, 11, 50, 28, 6.00, 168.00),
(62, 11, 53, 22, 8.00, 176.00),
(63, 11, 55, 30, 9.50, 285.00),
(64, 11, 57, 18, 12.00, 216.00),
(65, 12, 16, 60, 12.50, 750.00),
(66, 12, 17, 45, 8.00, 360.00),
(67, 12, 20, 38, 15.00, 570.00),
(68, 12, 22, 30, 22.00, 660.00),
(69, 12, 26, 25, 9.00, 225.00),
(70, 13, 1, 4, 1500.00, 6000.00),
(71, 13, 3, 8, 80.00, 640.00),
(72, 13, 5, 12, 60.00, 720.00),
(73, 13, 10, 10, 90.00, 900.00),
(74, 13, 15, 6, 20.00, 120.00),
(75, 14, 26, 22, 35.00, 770.00),
(76, 14, 27, 28, 45.00, 1260.00),
(77, 14, 30, 18, 38.00, 684.00),
(78, 14, 33, 14, 42.00, 588.00),
(79, 14, 37, 20, 15.00, 300.00),
(80, 15, 38, 16, 45.00, 720.00),
(81, 15, 42, 10, 85.00, 850.00),
(82, 15, 46, 14, 38.00, 532.00),
(83, 15, 47, 12, 42.00, 504.00),
(84, 15, 48, 18, 32.00, 576.00),
(85, 16, 48, 55, 12.00, 660.00),
(86, 16, 49, 48, 4.50, 216.00),
(87, 16, 50, 38, 6.00, 228.00),
(88, 16, 54, 28, 7.50, 210.00),
(89, 16, 55, 32, 9.50, 304.00),
(90, 16, 56, 35, 12.00, 420.00),
(91, 17, 64, 18, 55.00, 990.00),
(92, 17, 65, 22, 45.00, 990.00),
(93, 17, 66, 28, 18.00, 504.00),
(94, 17, 68, 15, 38.00, 570.00),
(95, 17, 70, 20, 28.00, 560.00),
(96, 18, 17, 40, 8.00, 320.00),
(97, 18, 22, 35, 22.00, 770.00),
(98, 18, 27, 30, 9.00, 270.00),
(99, 18, 28, 48, 1.50, 72.00),
(100, 18, 31, 25, 18.00, 450.00),
(101, 19, 58, 24, 35.00, 840.00),
(102, 19, 59, 28, 22.00, 616.00),
(103, 19, 60, 16, 40.00, 640.00),
(104, 19, 62, 20, 45.00, 900.00),
(105, 19, 64, 18, 25.00, 450.00),
(106, 20, 2, 30, 25.00, 750.00),
(107, 20, 11, 35, 18.00, 630.00),
(108, 20, 13, 20, 35.00, 700.00),
(109, 20, 15, 18, 20.00, 360.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_ventas`
--

CREATE TABLE `detalle_ventas` (
  `id` int NOT NULL,
  `venta_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `detalle_ventas`
--

INSERT INTO `detalle_ventas` (`id`, `venta_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
(1, 1, 1, 2, 2200.00, 4400.00),
(2, 2, 3, 1, 135.00, 135.00),
(3, 3, 6, 20, 18.90, 378.00),
(4, 3, 7, 15, 12.50, 187.50),
(5, 3, 9, 50, 3.50, 175.00),
(6, 3, 10, 10, 24.00, 240.00),
(7, 4, 13, 5, 35.00, 175.00),
(8, 4, 11, 1, 65.00, 65.00),
(9, 5, 6, 40, 18.90, 756.00),
(10, 5, 7, 30, 12.50, 375.00),
(11, 5, 8, 50, 4.20, 210.00),
(12, 5, 9, 30, 3.50, 105.00),
(13, 6, 16, 2, 55.00, 110.00),
(14, 6, 17, 1, 65.00, 65.00),
(15, 7, 19, 15, 20.00, 300.00),
(16, 7, 20, 10, 9.00, 90.00),
(17, 7, 21, 5, 11.50, 57.50),
(18, 8, 2, 3, 45.00, 135.00),
(19, 8, 5, 1, 110.00, 110.00),
(20, 8, 20, 5, 9.00, 45.00),
(21, 8, 19, 1, 20.00, 20.00),
(22, 9, 4, 1, 550.00, 550.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('90vtopiefjbh1e5vm4arqcbj9vxtzrq6', 'eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6Im1nb256YWxleiJ9:1vNgzD:klZdji91Q1vBonIeq5G3xNRWWJZjCy2WPCsy-Oyp_OA', '2025-12-09 00:32:51.222631');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_inventario`
--

CREATE TABLE `movimientos_inventario` (
  `id` int NOT NULL,
  `producto_id` int NOT NULL,
  `almacen_id` int NOT NULL,
  `tipo_movimiento` enum('entrada','salida','ajuste') NOT NULL,
  `cantidad` int NOT NULL,
  `usuario_id` int NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `motivo` text,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `movimientos_inventario`
--

INSERT INTO `movimientos_inventario` (`id`, `producto_id`, `almacen_id`, `tipo_movimiento`, `cantidad`, `usuario_id`, `referencia`, `motivo`, `fecha`) VALUES
(1, 1, 1, 'entrada', 2, 2, 'C-2024-001', 'Compra inicial de laptops', '2025-11-25 00:26:43'),
(2, 2, 1, 'entrada', 10, 2, 'C-2024-001', 'Compra de mouse inalÃ¡mbricos', '2025-11-25 00:26:43'),
(3, 4, 1, 'entrada', 1, 2, 'C-2024-001', 'Compra de monitor', '2025-11-25 00:26:43'),
(4, 5, 1, 'entrada', 4, 2, 'C-2024-001', 'Compra de auriculares', '2025-11-25 00:26:43'),
(5, 6, 2, 'entrada', 30, 2, 'C-2024-002', 'Entrada de arroz', '2025-11-25 00:26:43'),
(6, 7, 2, 'entrada', 25, 2, 'C-2024-002', 'Entrada de aceite', '2025-11-25 00:26:43'),
(7, 8, 2, 'entrada', 50, 2, 'C-2024-002', 'Entrada de azÃºcar', '2025-11-25 00:26:43'),
(8, 1, 1, 'salida', 2, 4, 'V-2024-001', 'Venta corporativa', '2025-11-25 00:26:43'),
(9, 3, 1, 'salida', 1, 4, 'V-2024-002', 'Venta al por menor', '2025-11-25 00:26:43'),
(10, 6, 2, 'salida', 20, 4, 'V-2024-003', 'Venta a distribuidor', '2025-11-25 00:26:43'),
(11, 7, 2, 'salida', 15, 4, 'V-2024-003', 'Venta a distribuidor', '2025-11-25 00:26:43'),
(12, 2, 1, 'ajuste', -1, 5, 'AJ-001', 'Producto daÃ±ado durante manipulaciÃ³n', '2025-11-25 00:26:43'),
(13, 8, 2, 'ajuste', 5, 5, 'AJ-002', 'Ajuste por inventario fÃ­sico', '2025-11-25 00:26:43'),
(14, 13, 1, 'ajuste', -2, 5, 'AJ-003', 'Productos con defecto de fÃ¡brica', '2025-11-25 00:26:43'),
(15, 19, 1, 'entrada', 25, 5, 'TRF-001', 'Transferencia de almacÃ©n 2 a 1', '2025-11-25 00:26:43'),
(16, 19, 2, 'salida', 25, 5, 'TRF-001', 'Transferencia de almacÃ©n 2 a 1', '2025-11-25 00:26:43'),
(17, 10, 2, 'entrada', 10, 5, 'TRF-002', 'RedistribuciÃ³n de stock', '2025-11-25 00:26:43'),
(18, 10, 1, 'salida', 10, 5, 'TRF-002', 'RedistribuciÃ³n de stock', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text,
  `categoria_id` int NOT NULL,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock_minimo` int DEFAULT '10',
  `stock_actual` int DEFAULT '0',
  `proveedor_id` int DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `codigo`, `nombre`, `descripcion`, `categoria_id`, `precio_compra`, `precio_venta`, `stock_minimo`, `stock_actual`, `proveedor_id`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'ELEC-001', 'Laptop HP 15.6\"', 'Laptop HP Intel Core i5, 8GB RAM, 256GB SSD', 1, 1500.00, 2200.00, 5, 12, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(2, 'ELEC-002', 'Mouse InalÃ¡mbrico Logitech', 'Mouse Ã³ptico inalÃ¡mbrico con receptor USB', 1, 25.00, 45.00, 20, 35, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(3, 'ELEC-003', 'Teclado MecÃ¡nico RGB', 'Teclado mecÃ¡nico gaming con iluminaciÃ³n RGB', 1, 80.00, 135.00, 10, 18, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(4, 'ELEC-004', 'Monitor LED 24\"', 'Monitor Full HD 1920x1080, 75Hz', 1, 350.00, 550.00, 8, 15, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(5, 'ELEC-005', 'Auriculares Bluetooth', 'Auriculares inalÃ¡mbricos con cancelaciÃ³n de ruido', 1, 60.00, 110.00, 15, 25, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(6, 'ELEC-006', 'Tablet Samsung 10\"', 'Tablet Android 64GB con lÃ¡piz Ã³ptico', 1, 450.00, 750.00, 8, 10, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(7, 'ELEC-007', 'Webcam Full HD', 'CÃ¡mara web 1080p con micrÃ³fono', 1, 55.00, 95.00, 15, 22, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(8, 'ELEC-008', 'Disco Duro Externo 1TB', 'HDD portÃ¡til USB 3.0', 1, 120.00, 185.00, 12, 28, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(9, 'ELEC-009', 'Impresora Multifuncional', 'Impresora WiFi con escÃ¡ner y copiadora', 1, 280.00, 450.00, 5, 8, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(10, 'ELEC-010', 'Router WiFi 6', 'Router dual band hasta 1200Mbps', 1, 90.00, 155.00, 10, 16, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(11, 'ELEC-011', 'Memoria USB 64GB', 'Pendrive USB 3.0 alta velocidad', 1, 18.00, 32.00, 30, 45, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(12, 'ELEC-012', 'Cable HDMI 2m', 'Cable HDMI 2.0 4K Ultra HD', 1, 12.00, 22.00, 40, 68, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(13, 'ELEC-013', 'Cargador PortÃ¡til 20000mAh', 'Power bank con doble puerto USB', 1, 35.00, 65.00, 20, 32, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(14, 'ELEC-014', 'Adaptador Bluetooth USB', 'Adaptador Bluetooth 5.0 para PC', 1, 15.00, 28.00, 25, 40, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(15, 'ELEC-015', 'Mousepad Gamer XXL', 'Alfombrilla gaming 90x40cm', 1, 20.00, 38.00, 15, 26, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(16, 'ALIM-001', 'Arroz Premium 5kg', 'Arroz grano largo extra premium', 2, 12.50, 18.90, 50, 145, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(17, 'ALIM-002', 'Aceite Vegetal 1L', 'Aceite vegetal 100% puro', 2, 8.00, 12.50, 30, 95, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(18, 'ALIM-003', 'AzÃºcar Blanca 1kg', 'AzÃºcar refinada blanca', 2, 2.50, 4.20, 100, 180, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(19, 'ALIM-004', 'Fideos Spaghetti 500g', 'Pasta italiana tipo spaghetti', 2, 1.80, 3.50, 80, 125, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(20, 'ALIM-005', 'CafÃ© Molido 250g', 'CafÃ© premium 100% arÃ¡bica', 2, 15.00, 24.00, 40, 68, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(21, 'ALIM-006', 'Leche Evaporada x12', 'Pack de 12 latas de leche evaporada', 2, 28.00, 42.00, 35, 72, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(22, 'ALIM-007', 'AtÃºn en Lata x6', 'Pack de 6 latas de atÃºn en aceite', 2, 22.00, 35.00, 40, 88, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(23, 'ALIM-008', 'Harina de Trigo 1kg', 'Harina preparada para todo uso', 2, 3.20, 5.50, 60, 110, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(24, 'ALIM-009', 'Sal de Mesa 1kg', 'Sal yodada de mesa', 2, 1.50, 2.80, 80, 140, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(25, 'ALIM-010', 'Galletas Surtidas x6', 'Pack de galletas variadas', 2, 12.00, 19.50, 50, 95, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(26, 'ALIM-011', 'Chocolate en Barra 90g', 'Chocolate con leche premium', 2, 3.50, 6.20, 70, 125, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(27, 'ALIM-012', 'Mermelada Fresa 500g', 'Mermelada de fresa casera', 2, 8.50, 14.00, 35, 62, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(28, 'ALIM-013', 'Conserva de Duraznos', 'Duraznos en almÃ­bar lata 820g', 2, 9.00, 15.50, 45, 78, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(29, 'ALIM-014', 'Avena en Hojuelas 500g', 'Avena integral en hojuelas', 2, 5.50, 9.80, 55, 98, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(30, 'ALIM-015', 'Mayonesa 475g', 'Mayonesa tradicional', 2, 6.80, 11.50, 40, 72, 2, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(31, 'ROPA-001', 'Camisa Manga Larga', 'Camisa formal de algodÃ³n para caballero', 3, 35.00, 65.00, 15, 32, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(32, 'ROPA-002', 'PantalÃ³n Jean Dama', 'Jean denim stretch para dama', 3, 45.00, 85.00, 20, 48, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(33, 'ROPA-003', 'Polo Deportivo', 'Polo deportivo dry-fit unisex', 3, 18.00, 35.00, 30, 72, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(34, 'ROPA-004', 'Zapatillas Running', 'Zapatillas deportivas para running', 3, 80.00, 150.00, 12, 26, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(35, 'ROPA-005', 'Vestido Casual', 'Vestido de algodÃ³n manga corta', 3, 38.00, 72.00, 18, 34, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(36, 'ROPA-006', 'Chaqueta Jean', 'Chaqueta denim unisex', 3, 55.00, 105.00, 12, 22, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(37, 'ROPA-007', 'Shorts Deportivos', 'Shorts dry-fit para deporte', 3, 22.00, 42.00, 25, 48, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(38, 'ROPA-008', 'Blusa Elegante', 'Blusa de gasa para dama', 3, 32.00, 62.00, 20, 38, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(39, 'ROPA-009', 'Zapatillas Urbanas', 'Zapatillas casuales estilo urbano', 3, 65.00, 125.00, 15, 28, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(40, 'ROPA-010', 'Medias Deportivas x3', 'Pack de 3 pares de medias', 3, 8.00, 15.50, 40, 76, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(41, 'ROPA-011', 'Gorra Ajustable', 'Gorra deportiva ajustable', 3, 15.00, 28.00, 30, 58, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(42, 'ROPA-012', 'Chompa Polar', 'Chompa polar con cierre', 3, 42.00, 80.00, 14, 25, 3, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(43, 'HOGA-001', 'Juego de SÃ¡banas 2 plazas', 'SÃ¡banas 100% algodÃ³n egipcio', 4, 45.00, 85.00, 10, 22, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(44, 'HOGA-002', 'Almohada ViscoelÃ¡stica', 'Almohada memory foam ergonÃ³mica', 4, 30.00, 55.00, 15, 32, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(45, 'HOGA-003', 'Toallas Set x4', 'Set de 4 toallas de baÃ±o premium', 4, 35.00, 65.00, 20, 38, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(46, 'HOGA-004', 'Cortinas Blackout 2x2m', 'Cortinas blackout con aros', 4, 50.00, 95.00, 8, 18, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(47, 'HOGA-005', 'EdredÃ³n Queen Size', 'EdredÃ³n acolchado antialÃ©rgico', 4, 85.00, 155.00, 8, 14, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(48, 'HOGA-006', 'Organizador de Closet', 'Organizador colgante 6 niveles', 4, 25.00, 45.00, 15, 28, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(49, 'HOGA-007', 'Alfombra 160x230cm', 'Alfombra decorativa antideslizante', 4, 95.00, 175.00, 6, 11, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(50, 'HOGA-008', 'Espejo de Pared 60cm', 'Espejo decorativo redondo', 4, 38.00, 72.00, 10, 18, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(51, 'HOGA-009', 'Set Cubiertos x24', 'Juego de cubiertos acero inoxidable', 4, 42.00, 78.00, 12, 22, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(52, 'HOGA-010', 'Vajilla 20 Piezas', 'Vajilla de porcelana para 4 personas', 4, 68.00, 125.00, 8, 15, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(53, 'HOGA-011', 'LÃ¡mpara de Mesa LED', 'LÃ¡mpara escritorio con regulador', 4, 32.00, 58.00, 15, 28, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(54, 'HOGA-012', 'Cojines Decorativos x4', 'Set de 4 cojines con fundas', 4, 28.00, 52.00, 18, 34, 4, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(55, 'OFIC-001', 'Papel Bond A4 x500', 'Resma papel bond blanco A4 75gr', 5, 12.00, 20.00, 50, 155, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(56, 'OFIC-002', 'Lapiceros Azul x12', 'Caja de 12 lapiceros punta fina', 5, 4.50, 9.00, 40, 98, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(57, 'OFIC-003', 'Archivador Palanca', 'Archivador palanca lomo ancho', 5, 6.00, 11.50, 30, 68, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(58, 'OFIC-004', 'Calculadora CientÃ­fica', 'Calculadora cientÃ­fica 252 funciones', 5, 25.00, 45.00, 10, 22, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(59, 'OFIC-005', 'Engrapador MetÃ¡lico', 'Engrapador hasta 40 hojas', 5, 15.00, 28.00, 20, 42, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(60, 'OFIC-006', 'Corrector LÃ­quido x6', 'Pack de 6 correctores lÃ­quidos', 5, 8.00, 15.00, 35, 72, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(61, 'OFIC-007', 'Carpeta Manila x50', 'Pack de 50 carpetas manila A4', 5, 18.00, 32.00, 25, 58, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(62, 'OFIC-008', 'Resaltadores x6 colores', 'Set de 6 resaltadores fluorescentes', 5, 9.50, 17.50, 30, 64, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(63, 'OFIC-009', 'Tijera Profesional', 'Tijera de oficina 8 pulgadas', 5, 7.50, 14.00, 25, 48, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(64, 'OFIC-010', 'Post-it Pack x4', 'Pack de 4 blocks de notas adhesivas', 5, 12.00, 22.00, 40, 82, 5, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(65, 'DEPO-001', 'BalÃ³n de FÃºtbol NÂ°5', 'BalÃ³n profesional cosido a mano', 6, 35.00, 65.00, 15, 32, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(66, 'DEPO-002', 'Colchoneta Yoga', 'Colchoneta antideslizante con bolso', 6, 22.00, 42.00, 20, 42, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(67, 'DEPO-003', 'Mancuernas 5kg Par', 'Par de mancuernas hexagonales', 6, 40.00, 75.00, 10, 22, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(68, 'DEPO-004', 'Cuerda de Saltar', 'Cuerda ajustable con contador', 6, 12.00, 22.00, 30, 58, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(69, 'DEPO-005', 'Guantes de Box', 'Guantes profesionales 12oz', 6, 45.00, 85.00, 12, 24, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(70, 'DEPO-006', 'Banda ElÃ¡stica Set x3', 'Set de 3 bandas de resistencia', 6, 18.00, 35.00, 25, 48, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(71, 'DEPO-007', 'Botella Deportiva 1L', 'Botella tÃ©rmica acero inoxidable', 6, 25.00, 45.00, 20, 38, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(72, 'DEPO-008', 'Kit de Pesas 20kg', 'Set de barras y discos ajustables', 6, 85.00, 155.00, 8, 14, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(73, 'JUGT-001', 'Lego Set ConstrucciÃ³n', 'Set de 500 piezas para construcciÃ³n', 7, 55.00, 95.00, 12, 25, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(74, 'JUGT-002', 'MuÃ±eca Interactiva', 'MuÃ±eca con sonidos y movimientos', 7, 45.00, 85.00, 15, 28, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(75, 'JUGT-003', 'Rompecabezas 1000 piezas', 'Rompecabezas paisaje premium', 7, 18.00, 35.00, 25, 48, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(76, 'JUGT-004', 'Auto Control Remoto', 'Auto RC recargable con luces', 7, 65.00, 120.00, 10, 18, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(77, 'JUGT-005', 'Peluche Oso 60cm', 'Peluche gigante suave', 7, 38.00, 72.00, 15, 28, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(78, 'JUGT-006', 'Juego de Mesa Monopoly', 'Juego clÃ¡sico familiar', 7, 42.00, 78.00, 12, 22, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(79, 'JUGT-007', 'Pelota Inflable Grande', 'Pelota de playa 75cm', 7, 8.00, 15.50, 30, 58, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(80, 'JUGT-008', 'Set Dinosaurios x12', 'ColecciÃ³n de figuras de dinosaurios', 7, 28.00, 52.00, 18, 34, 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id` int NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `ruc` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` text,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id`, `nombre`, `ruc`, `telefono`, `email`, `direccion`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'TecnoDistribuidora S.A.', '20123456789', '987654321', 'ventas@tecnodist.com', 'Av. TecnologÃ­a 100', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(2, 'Alimentos del Valle', '20234567890', '987654322', 'contacto@alimentosvalle.com', 'Jr. Comercio 200', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(3, 'Textiles Modernos', '20345678901', '987654323', 'info@textilesmodernos.com', 'Av. Industrial 300', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(4, 'Hogar y Confort', '20456789012', '987654324', 'ventas@hogaryconfort.com', 'Calle DiseÃ±o 400', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(5, 'PapelerÃ­a Central', '20567890123', '987654325', 'pedidos@papeleriacentral.com', 'Jr. Oficinas 500', 1, '2025-11-25 00:26:43', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`, `descripcion`, `created_at`) VALUES
(1, 'Administrador', 'Acceso total al sistema', '2025-11-25 00:26:43'),
(2, 'Gerente', 'GestiÃ³n de inventario y reportes', '2025-11-25 00:26:43'),
(3, 'Vendedor', 'Registro de ventas y consultas', '2025-11-25 00:26:43'),
(4, 'Almacenero', 'GestiÃ³n de stock y almacenes', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `rol_id` int NOT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `email`, `password`, `nombre_completo`, `rol_id`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'admin@inventario.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador Sistema', 1, 0, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(2, 'superadmin', 'superadmin@superadmin.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Super Administrador', 1, 1, '2025-11-25 00:26:43', '2025-11-25 00:31:20'),
(3, 'jperez', 'jperez@inventario.com', '56976bf24998ca63e35fe4f1e2469b5751d1856003e8d16fef0aafef496ed044', 'Juan PÃ©rez', 2, 0, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(4, 'mgonzalez', 'mgonzalez@inventario.com', '7439033334ff7f5d2d164c47fe54b5819c0f7cd1225ecbc3bbac5bc80206b01f', 'MarÃ­a GonzÃ¡lez', 3, 0, '2025-11-25 00:26:43', '2025-11-25 00:26:43'),
(5, 'crodriguez', 'crodriguez@inventario.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Carlos RodrÃ­guez', 4, 0, '2025-11-25 00:26:43', '2025-11-25 00:26:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id` int NOT NULL,
  `numero_factura` varchar(50) DEFAULT NULL,
  `cliente_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','completada','cancelada') DEFAULT 'pendiente',
  `tipo_pago` enum('efectivo','tarjeta','transferencia') DEFAULT 'efectivo',
  `notas` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id`, `numero_factura`, `cliente_id`, `usuario_id`, `fecha`, `total`, `estado`, `tipo_pago`, `notas`, `created_at`) VALUES
(1, 'V-2024-001', 1, 4, '2024-10-02', 4850.00, 'completada', 'transferencia', 'Venta corporativa - Equipos oficina', '2025-11-25 00:26:43'),
(2, 'V-2024-002', 11, 4, '2024-10-04', 285.00, 'completada', 'efectivo', 'Venta retail local', '2025-11-25 00:26:43'),
(3, 'V-2024-003', 2, 4, '2024-10-06', 1450.00, 'completada', 'transferencia', 'Pedido distribuciÃ³n XYZ', '2025-11-25 00:26:43'),
(4, 'V-2024-004', 12, 4, '2024-10-08', 425.00, 'completada', 'tarjeta', 'Venta productos mixtos', '2025-11-25 00:26:43'),
(5, 'V-2024-005', 3, 4, '2024-10-10', 2850.00, 'completada', 'transferencia', 'Pedido supermercado grande', '2025-11-25 00:26:43'),
(6, 'V-2024-006', 13, 4, '2024-10-12', 180.00, 'completada', 'efectivo', 'Venta particular', '2025-11-25 00:26:43'),
(7, 'V-2024-007', 4, 4, '2024-10-14', 650.00, 'completada', 'tarjeta', 'Venta tienda express', '2025-11-25 00:26:43'),
(8, 'V-2024-008', 14, 4, '2024-10-16', 320.00, 'completada', 'efectivo', 'Productos varios', '2025-11-25 00:26:43'),
(9, 'V-2024-009', 5, 4, '2024-10-18', 1250.00, 'completada', 'transferencia', 'Pedido comercial El Sol', '2025-11-25 00:26:43'),
(10, 'V-2024-010', 15, 4, '2024-10-20', 495.00, 'completada', 'tarjeta', 'Compra productos hogar', '2025-11-25 00:26:43'),
(11, 'V-2024-011', 6, 4, '2024-10-22', 2150.00, 'completada', 'transferencia', 'Venta corporativa Norte', '2025-11-25 00:26:43'),
(12, 'V-2024-012', 16, 4, '2024-10-24', 385.00, 'completada', 'efectivo', 'Venta retail', '2025-11-25 00:26:43'),
(13, 'V-2024-013', 7, 4, '2024-10-26', 1680.00, 'completada', 'transferencia', 'Pedido Distribuciones Sur', '2025-11-25 00:26:43'),
(14, 'V-2024-014', 17, 4, '2024-10-28', 245.00, 'completada', 'tarjeta', 'Compra personal', '2025-11-25 00:26:43'),
(15, 'V-2024-015', 8, 4, '2024-10-30', 3250.00, 'completada', 'transferencia', 'Venta mayorista Retail PerÃº', '2025-11-25 00:26:43'),
(16, 'V-2024-016', 18, 4, '2024-11-01', 528.00, 'completada', 'efectivo', 'Venta productos oficina', '2025-11-25 00:26:43'),
(17, 'V-2024-017', 9, 4, '2024-11-03', 1850.00, 'completada', 'transferencia', 'Pedido Mayoristas Asociados', '2025-11-25 00:26:43'),
(18, 'V-2024-018', 19, 4, '2024-11-05', 375.00, 'completada', 'tarjeta', 'Compra electrÃ³nicos', '2025-11-25 00:26:43'),
(19, 'V-2024-019', 10, 4, '2024-11-07', 2450.00, 'completada', 'transferencia', 'Venta Comercializadora Global', '2025-11-25 00:26:43'),
(20, 'V-2024-020', 20, 4, '2024-11-09', 680.00, 'completada', 'efectivo', 'Venta productos deportivos', '2025-11-25 00:26:43'),
(21, 'V-2024-021', 1, 4, '2024-11-11', 4200.00, 'completada', 'transferencia', 'RenovaciÃ³n equipamiento ABC', '2025-11-25 00:26:43'),
(22, 'V-2024-022', 21, 4, '2024-11-13', 295.00, 'completada', 'tarjeta', 'Compra personal hogar', '2025-11-25 00:26:43'),
(23, 'V-2024-023', 3, 4, '2024-11-15', 1980.00, 'completada', 'transferencia', 'ReposiciÃ³n supermercado', '2025-11-25 00:26:43'),
(24, 'V-2024-024', 22, 4, '2024-11-17', 425.00, 'completada', 'efectivo', 'Venta productos variados', '2025-11-25 00:26:43'),
(25, 'V-2024-025', 4, 4, '2024-11-19', 850.00, 'completada', 'tarjeta', 'Pedido Express', '2025-11-25 00:26:43'),
(26, 'V-2024-026', 23, 4, '2024-11-20', 385.00, 'completada', 'efectivo', 'Compra ropa', '2025-11-25 00:26:43'),
(27, 'V-2024-027', 6, 4, '2024-11-21', 1550.00, 'completada', 'transferencia', 'Venta corporativa', '2025-11-25 00:26:43'),
(28, 'V-2024-028', 24, 4, '2024-11-22', 695.00, 'completada', 'tarjeta', 'Productos tecnolÃ³gicos', '2025-11-25 00:26:43'),
(29, 'V-2024-029', 2, 4, '2024-11-23', 2250.00, 'completada', 'transferencia', 'Gran pedido XYZ', '2025-11-25 00:26:43'),
(30, 'V-2024-030', 25, 4, '2024-11-24', 325.00, 'completada', 'efectivo', 'Venta juguetes', '2025-11-25 00:26:43'),
(31, 'V-2024-031', 7, 4, '2024-11-25', 1480.00, 'completada', 'transferencia', 'Pedido mensual', '2025-11-25 00:26:43'),
(32, 'V-2024-032', 11, 4, '2024-11-25', 255.00, 'completada', 'tarjeta', 'Compra personal', '2025-11-25 00:26:43'),
(33, 'V-2024-033', 5, 4, '2024-11-26', 3850.00, 'completada', 'transferencia', 'Pedido grande El Sol', '2025-11-25 00:26:43'),
(34, 'V-2024-034', 12, 4, '2024-11-26', 485.00, 'completada', 'efectivo', 'Venta productos mixtos', '2025-11-25 00:26:43'),
(35, 'V-2024-035', 1, 4, '2024-11-27', 1250.00, 'pendiente', 'transferencia', 'Pedido pendiente entrega', '2025-11-25 00:26:43');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `almacenes`
--
ALTER TABLE `almacenes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `proveedor_id` (`proveedor_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_compras_fecha` (`fecha`);

--
-- Indices de la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `compra_id` (`compra_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `venta_id` (`venta_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_idx` (`expire_date`);

--
-- Indices de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `almacen_id` (`almacen_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `proveedor_id` (`proveedor_id`),
  ADD KEY `idx_productos_codigo` (`codigo`),
  ADD KEY `idx_productos_categoria` (`categoria_id`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ruc` (`ruc`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `rol_id` (`rol_id`),
  ADD KEY `idx_usuarios_username` (`username`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_ventas_fecha` (`fecha`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `almacenes`
--
ALTER TABLE `almacenes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  ADD CONSTRAINT `detalle_compras_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalle_compras_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD CONSTRAINT `detalle_ventas_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalle_ventas_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD CONSTRAINT `movimientos_inventario_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `movimientos_inventario_ibfk_2` FOREIGN KEY (`almacen_id`) REFERENCES `almacenes` (`id`),
  ADD CONSTRAINT `movimientos_inventario_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
