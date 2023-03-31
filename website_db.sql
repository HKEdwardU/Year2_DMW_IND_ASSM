-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost:3306
-- 產生時間： 2023 年 04 月 01 日 02:18
-- 伺服器版本： 8.0.32-0ubuntu0.22.04.2
-- PHP 版本： 8.1.2-1ubuntu2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `website_db`
--

-- --------------------------------------------------------

--
-- 資料表結構 `cart`
--

CREATE TABLE `cart` (
  `C_ID` int NOT NULL,
  `P_ID` int NOT NULL,
  `P_Quantity` smallint NOT NULL,
  `Price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `customers`
--

CREATE TABLE `customers` (
  `C_ID` int NOT NULL,
  `C_Name` varchar(50) NOT NULL,
  `C_Email` varchar(100) NOT NULL,
  `C_Password` varchar(50) NOT NULL,
  `gender` varchar(30) NOT NULL,
  `Phone_Num` varchar(30) NOT NULL,
  `Address` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `login`
--

CREATE TABLE `login` (
  `C_ID` int NOT NULL,
  `C_Name` varchar(50) NOT NULL,
  `C_Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `order_list`
--

CREATE TABLE `order_list` (
  `C_ID` int NOT NULL,
  `Order_ID` int NOT NULL,
  `P_ID` int NOT NULL,
  `P_Quantity` smallint NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `PM_ID` int DEFAULT NULL,
  `Created_At` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `product`
--

CREATE TABLE `product` (
  `P_ID` int NOT NULL,
  `P_Name` varchar(100) NOT NULL,
  `P_Description` text NOT NULL,
  `P_Price` decimal(10,2) NOT NULL,
  `P_IMG_URL` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `product`
--

INSERT INTO `product` (`P_ID`, `P_Name`, `P_Description`, `P_Price`, `P_IMG_URL`) VALUES
(1, 'Inter Arc A770', 'The Arc A770 is a performance-segment graphics card by Intel, launched on October 12th, 2022. Built on the 6 nm process,\n                     and based on the DG2-512 graphics processor, in its ACM-G10 variant, the card supports DirectX 12 Ultimate.', '3888.00', 'https://i.ibb.co/CzQqGTq/Intel-Arc-A770.jpg'),
(2, 'Intel i7 13700K', 'With 30MB of cache and a 5.4 GHz Turbo Boost Max 3.0 frequency, this processor is made to handle intense workloads.\n                     You can also overclock this processor for even greater performance. The Core i7-13700K also supports PCI Express\n                      5.0 and dual-channel DDR5 ECC memory at 5600 MHz.', '3550.00', 'https://i.ibb.co/558NG0h/Intel-i7-13700-K.jpg'),
(3, 'MSI RTX 4090', 'The NVIDIA GeForce RTX 4090 is the ultimate GeForce GPU. It brings an enormous leap in performance, efficiency,\n                     and AI-powered graphics. Experience ultra-high performance gaming, incredibly detailed virtual worlds with ray\n                      tracing, unprecedented productivity, and new ways to create.', '15800.00', 'https://i.ibb.co/gS7KJXV/RTX-4090-MSI.jpg'),
(4, 'AMD Ryzen 7 5800X', 'The AMD Ryzen 7 5800X processor is optimized for gaming: 8 Cores, 16 Threads and 36MB GameCache. Not to mention the\n                     native and boosted frequencies that allow you to enjoy your favorite games in the best conditions. Combine it with\n                      a high-performance graphics card and you\'ll be able to play any game smoothly.', '2000.00', 'https://i.ibb.co/wRHPdgj/AMD-Ryzen.jpg'),
(5, 'GIGABYTE RTX 3060TI', 'The Nvidia GeForce RTX 3060 Ti is a fast desktop graphics card based on the Ampere architecture. It uses the big GA104\n                     chip and offers 4,864 cores and 8 GB GDDR6 graphics memory. The performance in games and 4k resolution is slightly\n                      above a desktop RTX 2080 Super.', '3799.00', 'https://i.ibb.co/whnt5tB/RTX-3060-Ti-GIGABYTE.jpg'),
(6, 'MSI MPG Z790 CARBON WIFI', 'The MPG series brings out fashionable products by showing extremely unique styles and expressing a conceited attitude\n                     towards the challenge of the gaming world. With extraordinary performance and style, the MPG series defines the future\n                      of gaming fashion.', '3180.00', 'https://i.ibb.co/fd13SMH/MSI-MPG-Z790-CARBON-WIFI.webp'),
(7, 'Kingston Fury Beast RGB DDR5 5200 32GB Kit', 'DDR5 5200 32GB Kit (16x2)', '1450.00', 'https://i.ibb.co/qW67670/Kingston-Fury-Beast-RGB-DDR5-5200-32-GB-Kit.webp'),
(8, 'Intel Core i5-13600K', 'It features four Willow Cove CPU cores running at 2.4 GHz (base clock speed @ 28 W TDP) Boosting up to 4.2 GHz (1-core Boost).\n                     The all-core Boost clock speed sits at 3.8 GHz. This is a Hyper-Threading-enabled CPU, allowing for up to 8 concurrent processing\n                      threads.', '2290.00', 'https://i.ibb.co/Bg2TjJ7/Intel-Core-i5-13600-K.webp'),
(9, 'ADATA Premier DDR4 3200 U-DIMM 16GB', 'DDR4 3200 16GB', '283.00', 'https://i.ibb.co/v353vDQ/ADATA-Premier-DDR4-3200-U-DIMM-16-GB.webp'),
(10, 'MSI MPG B760I EDGE WIFI DDR4', 'The MPG series brings out fashionable products by showing extremely unique styles and expressing a conceited attitude towards the\n                     challenge of the gaming world. With extraordinary performance and style, the MPG series defines the future of gaming fashion.', '1570.00', 'https://i.ibb.co/xgQrmBm/MSI-MPG-B760-I-EDGE-WIFI-DDR4.webp');

-- --------------------------------------------------------

--
-- 資料表結構 `promotion_list`
--

CREATE TABLE `promotion_list` (
  `PM_ID` int NOT NULL,
  `PM_CODE` varchar(30) NOT NULL,
  `PM_Discount_Value` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `promotion_list`
--

INSERT INTO `promotion_list` (`PM_ID`, `PM_CODE`, `PM_Discount_Value`) VALUES
(1, 'decrease', '50.00'),
(2, 'Extradecrease', '150.00');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`C_ID`);

--
-- 資料表索引 `login`
--
ALTER TABLE `login`
  ADD UNIQUE KEY `Login` (`C_ID`);

--
-- 資料表索引 `order_list`
--
ALTER TABLE `order_list`
  ADD PRIMARY KEY (`Order_ID`),
  ADD KEY `P_ID` (`P_ID`),
  ADD KEY `C_ID` (`C_ID`),
  ADD KEY `P_ID_2` (`P_ID`);

--
-- 資料表索引 `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`P_ID`);

--
-- 資料表索引 `promotion_list`
--
ALTER TABLE `promotion_list`
  ADD PRIMARY KEY (`PM_ID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customers`
--
ALTER TABLE `customers`
  MODIFY `C_ID` int NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order_list`
--
ALTER TABLE `order_list`
  MODIFY `Order_ID` int NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `product`
--
ALTER TABLE `product`
  MODIFY `P_ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `promotion_list`
--
ALTER TABLE `promotion_list`
  MODIFY `PM_ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`C_ID`) REFERENCES `customers` (`C_ID`);

--
-- 資料表的限制式 `order_list`
--
ALTER TABLE `order_list`
  ADD CONSTRAINT `order_list_ibfk_1` FOREIGN KEY (`C_ID`) REFERENCES `customers` (`C_ID`),
  ADD CONSTRAINT `order_list_ibfk_2` FOREIGN KEY (`P_ID`) REFERENCES `product` (`P_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
