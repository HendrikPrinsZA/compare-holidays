DROP TABLE IF EXISTS `holidays`;

CREATE TABLE `holidays` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `country_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  `title` varchar(255) NOT NULL,
  `is_on_weekend` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
  PRIMARY KEY (`id`),
  UNIQUE KEY `country_id_date` (`country_id`, `date`),
  KEY `holidays_country_id_foreign` (`country_id`),
  CONSTRAINT `holidays_country_id_foreign` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`)
) ENGINE=InnoDB;
