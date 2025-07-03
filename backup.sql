CREATE TABLE `test` (
  `rollnumber` varchar(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `batch` varchar(10) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rollnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 

CREATE TABLE `testcontent` (
  `content` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3