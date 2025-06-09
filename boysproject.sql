-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 08, 2025 at 04:12 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `boysproject`
--

CREATE TABLE `predefined_messages` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `question` varchar(255) NOT NULL,
  `answer` text NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `display_order` int(11) NOT NULL DEFAULT 0,
  `show_in_faq` tinyint(1) NOT NULL DEFAULT 0,
  `show_in_chat` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `sold` int(11) NOT NULL DEFAULT 0,
  `ratings` int(11) NOT NULL DEFAULT 0,
  `average_rating` decimal(2,1) NOT NULL DEFAULT 0.0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `category`, `image`, `description`, `stock`, `sold`, `ratings`, `average_rating`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Mounting Upsize All', 'Mounting & Body', 'mounting-upsize-all.png', 'Universal mounting solution for various motorcycle types', 3901, 377, 192, '4.6', 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(2, 'Mounting Vario', 'Mounting & Body', 'mounting-vario.png', 'Specialized mounting for Vario and compatible models', 3006, 3100, 1600, '4.8', 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(3, 'Turbo SE Experience 60W', 'Lampu', 'turbo-se-60w.png', 'High-performance 60W LED lamp with advanced features', 90, 0, 0, '0.0', 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08');

-- --------------------------------------------------------

--
-- Table structure for table `product_options`
--

CREATE TABLE `product_options` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `product_id` bigint(20) UNSIGNED NOT NULL,
  `option_name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `is_required` tinyint(1) NOT NULL DEFAULT 0,
  `sort_order` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product_options`
--

INSERT INTO `product_options` (`id`, `product_id`, `option_name`, `display_name`, `is_required`, `sort_order`, `created_at`, `updated_at`) VALUES
(1, 1, 'motor_type', 'Motor Type', 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(2, 1, 'size', 'Size', 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(3, 2, 'motor_type', 'Motor Type', 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(4, 2, 'size', 'Size', 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(5, 3, 'quantity', 'Quantity', 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08');

-- --------------------------------------------------------

--
-- Table structure for table `product_option_values`
--

CREATE TABLE `product_option_values` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `product_option_id` bigint(20) UNSIGNED NOT NULL,
  `value` varchar(255) NOT NULL,
  `display_value` varchar(255) NOT NULL,
  `price_adjustment` decimal(10,2) NOT NULL DEFAULT 0.00,
  `is_default` tinyint(1) NOT NULL DEFAULT 0,
  `is_available` tinyint(1) NOT NULL DEFAULT 1,
  `sort_order` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product_option_values`
--

INSERT INTO `product_option_values` (`id`, `product_option_id`, `value`, `display_value`, `price_adjustment`, `is_default`, `is_available`, `sort_order`, `created_at`, `updated_at`) VALUES
(1, 1, 'aerox_old', 'Aerox Old', '0.00', 1, 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(2, 1, 'aerox_new', 'Aerox New', '0.00', 0, 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(3, 1, 'aerox_alpha', 'Aerox Alpha', '0.00', 0, 1, 3, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(4, 1, 'nmax_new', 'Nmax New', '0.00', 0, 1, 4, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(5, 1, 'nmax_neo', 'Nmax Neo', '0.00', 0, 1, 5, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(6, 1, 'lexy', 'Lexy', '0.00', 0, 0, 6, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(7, 2, '3cm', '3cm', '0.00', 1, 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(8, 2, '4cm', '4cm', '0.00', 0, 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(9, 2, '5cm', '5cm', '0.00', 0, 1, 3, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(10, 2, '6cm', '6cm', '0.00', 0, 1, 4, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(11, 2, '7cm', '7cm', '0.00', 0, 1, 5, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(12, 2, '8cm', '8cm', '0.00', 0, 1, 6, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(13, 2, '9cm', '9cm', '0.00', 0, 1, 7, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(14, 3, 'vario_led_old', 'Vario LED Old', '0.00', 1, 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(15, 3, 'vario_led_new', 'Vario LED New', '0.00', 0, 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(16, 3, 'beat_esp', 'Beat ESP', '0.00', 0, 1, 3, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(17, 3, 'scoopy_esp', 'Scoopy ESP', '0.00', 0, 1, 4, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(18, 4, '3cm', '3cm', '0.00', 1, 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(19, 4, '4cm', '4cm', '0.00', 0, 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(20, 4, '5cm', '5cm', '0.00', 0, 1, 3, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(21, 4, '6cm', '6cm', '0.00', 0, 1, 4, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(22, 4, '7cm', '7cm', '0.00', 0, 1, 5, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(23, 4, '8cm', '8cm', '0.00', 0, 1, 6, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(24, 4, '9cm', '9cm', '0.00', 0, 1, 7, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(25, 5, 'single', 'Single', '0.00', 1, 1, 1, '2025-06-05 21:58:08', '2025-06-05 21:58:08'),
(26, 5, 'pair', 'Pair', '20.00', 0, 1, 2, '2025-06-05 21:58:08', '2025-06-05 21:58:08');

-- --------------------------------------------------------

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_options`
--
ALTER TABLE `product_options`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_options_product_id_foreign` (`product_id`);

--
-- Indexes for table `product_option_values`
--
ALTER TABLE `product_option_values`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_option_values_product_option_id_foreign` (`product_option_id`);
INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `product_options`
--
ALTER TABLE `product_options`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `product_option_values`
--
ALTER TABLE `product_option_values`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `product_options`
--
ALTER TABLE `product_options`
  ADD CONSTRAINT `product_options_product_id_foreign` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_option_values`
--
ALTER TABLE `product_option_values`
  ADD CONSTRAINT `product_option_values_product_option_id_foreign` FOREIGN KEY (`product_option_id`) REFERENCES `product_options` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
