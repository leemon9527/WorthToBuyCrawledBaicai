/*
Navicat MySQL Data Transfer

Source Server         : localhost_root
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : worthtobuy

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2016-05-19 15:33:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for worthtobuy
-- ----------------------------
DROP TABLE IF EXISTS `worthtobuy`;
CREATE TABLE `worthtobuy` (
  `id` varchar(20) NOT NULL,
  `name` varchar(500) DEFAULT NULL,
  `price` float(10,2) DEFAULT NULL,
  `mall` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `pic_url` varchar(500) DEFAULT NULL,
  `release_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
