-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Gegenereerd op: 04 nov 2019 om 20:51
-- Serverversie: 10.1.38-MariaDB
-- PHP-versie: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `osrs`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `item`
--

CREATE TABLE `item` (
  `id` int(10) NOT NULL,
  `time` bigint(64) NOT NULL,
  `price` int(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Gegevens worden geëxporteerd voor tabel `item`
--

INSERT INTO `item` (`id`, `time`, `price`) VALUES
(11248, 1571356800000, 2950),
(11248, 1571443200000, 2935),
(11248, 1571529600000, 2988),
(11248, 1571616000000, 2985),
(11248, 1571702400000, 3025),
(11248, 1571788800000, 3014),
(11248, 1571875200000, 2999),
(11248, 1571961600000, 2935),
(11248, 1572048000000, 2933),
(11248, 1572134400000, 2948),
(11248, 1572220800000, 2982),
(11248, 1572307200000, 3055),
(11248, 1572393600000, 3035),
(11248, 1572480000000, 3014),
(11248, 1572566400000, 2993),
(11248, 1572652800000, 2968),
(11248, 1572739200000, 2964),
(11248, 1572825600000, 3038);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `itemname`
--

CREATE TABLE `itemname` (
  `itemID` int(30) NOT NULL,
  `itemName` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Gegevens worden geëxporteerd voor tabel `itemname`
--

INSERT INTO `itemname` (`itemID`, `itemName`) VALUES
(11248, 'Eclectic Impling Jar');

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id`,`time`);

--
-- Indexen voor tabel `itemname`
--
ALTER TABLE `itemname`
  ADD PRIMARY KEY (`itemID`);

--
-- Beperkingen voor geëxporteerde tabellen
--

--
-- Beperkingen voor tabel `item`
--
ALTER TABLE `item`
  ADD CONSTRAINT `item_ibfk_1` FOREIGN KEY (`id`) REFERENCES `itemname` (`itemID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
