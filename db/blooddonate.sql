-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 28, 2024 at 10:27 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `blooddonate`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminlogin`
--

CREATE TABLE IF NOT EXISTS `adminlogin` (
  `user` varchar(50) NOT NULL,
  `psw` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `adminlogin`
--

INSERT INTO `adminlogin` (`user`, `psw`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `bloodstock`
--

CREATE TABLE IF NOT EXISTS `bloodstock` (
  `bid` int(50) NOT NULL AUTO_INCREMENT,
  `did` int(50) NOT NULL,
  `dname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `blood` varchar(50) NOT NULL,
  `units` varchar(50) NOT NULL,
  `dat` varchar(50) NOT NULL,
  PRIMARY KEY (`bid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `bloodstock`
--

INSERT INTO `bloodstock` (`bid`, `did`, `dname`, `email`, `blood`, `units`, `dat`) VALUES
(1, 1, 'rindhi', 'rindhi@gmail.com', 'A+', '3', '2024-03-02'),
(2, 2, 'siva', 'siva@gmail.com', 'O+', '4', '2024-09-12'),
(11, 1, 'rindhi', 'rindhi@gmail.com', 'A+', '1', '2024-05-28');

-- --------------------------------------------------------

--
-- Table structure for table `donar`
--

CREATE TABLE IF NOT EXISTS `donar` (
  `did` int(50) NOT NULL AUTO_INCREMENT,
  `dname` varchar(50) NOT NULL,
  `pwd` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mbl` varchar(50) NOT NULL,
  `blood` varchar(50) NOT NULL,
  `dob` varchar(50) NOT NULL,
  `addr` varchar(50) NOT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `donar`
--

INSERT INTO `donar` (`did`, `dname`, `pwd`, `email`, `mbl`, `blood`, `dob`, `addr`) VALUES
(1, 'rindhi', '1234', 'rindhi@gmail.com', '6374034623', 'A+', '2024-05-23', 'coimbatore'),
(2, 'siva', '1234', 'siva@gmail.com', '7373345678', 'O+', '2024-05-07', 'Madurai'),
(3, 'viki', 'viki', 'viki@gmail.com', '6374034623', 'O+', '2024-05-19', 'Chennai');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE IF NOT EXISTS `patient` (
  `pid` int(50) NOT NULL AUTO_INCREMENT,
  `pname` varchar(50) NOT NULL,
  `psw` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mob` varchar(50) NOT NULL,
  `blood` varchar(50) NOT NULL,
  `dat` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`pid`, `pname`, `psw`, `email`, `mob`, `blood`, `dat`, `address`) VALUES
(1, 'sakshi', '1234', 'sakshi@gmail.com', '9047872534', 'B+', '2024-05-13', 'madurai'),
(2, 'shri', '1234', 'shri@gmail.com', '7373345418', 'AB+', '2024-05-13', 'coimbatore');
