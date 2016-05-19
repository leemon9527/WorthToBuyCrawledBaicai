/*
Navicat MySQL Data Transfer

Source Server         : localhost_root
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : worthtobuy

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2016-05-19 15:33:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for page_info
-- ----------------------------
DROP TABLE IF EXISTS `page_info`;
CREATE TABLE `page_info` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `page_url` varchar(500) DEFAULT NULL,
  `is_crawled` varchar(5) DEFAULT NULL,
  `release_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8;
