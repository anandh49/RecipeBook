-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: recipes
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apple crumble`
--

DROP TABLE IF EXISTS `apple crumble`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apple crumble` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apple crumble`
--

LOCK TABLES `apple crumble` WRITE;
/*!40000 ALTER TABLE `apple crumble` DISABLE KEYS */;
INSERT INTO `apple crumble` VALUES (1,NULL,'55',NULL,NULL,'veg','Dessert',1),(2,'For the Apple Filling:',NULL,'Calories','310 kcal',NULL,NULL,0),(3,'4 medium apples (Granny Smith or any tart variety), peeled and sliced',NULL,'Protein','3g',NULL,NULL,0),(4,'2 tablespoons sugar (white or brown)',NULL,'Fats','13g',NULL,NULL,0),(5,'1 teaspoon cinnamon',NULL,'Fiber','4g',NULL,NULL,0),(6,'1 tablespoon lemon juice',NULL,'','',NULL,NULL,0),(7,'1 teaspoon vanilla extract',NULL,'','',NULL,NULL,0),(8,'1 tablespoon all-purpose flour',NULL,'','',NULL,NULL,0),(9,'For the Crumble Topping:',NULL,'','',NULL,NULL,0),(10,'¾ cup all-purpose flour',NULL,'','',NULL,NULL,0),(11,'½ cup rolled oats',NULL,'','',NULL,NULL,0),(12,'½ cup brown sugar',NULL,'','',NULL,NULL,0),(13,'½ teaspoon cinnamon',NULL,'','',NULL,NULL,0),(14,'⅓ cup cold unsalted butter, cubed',NULL,'','',NULL,NULL,0),(15,'Pinch of salt',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `apple crumble` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chicken biryani`
--

DROP TABLE IF EXISTS `chicken biryani`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chicken biryani` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chicken biryani`
--

LOCK TABLES `chicken biryani` WRITE;
/*!40000 ALTER TABLE `chicken biryani` DISABLE KEYS */;
INSERT INTO `chicken biryani` VALUES (1,'For Marination:',NULL,'Calories','550 kcal',NULL,NULL,0),(2,'500g chicken (bone-in preferred)',NULL,'Protein','28g',NULL,NULL,0),(3,'1 cup yogurt',NULL,'Carbs','55g',NULL,NULL,0),(4,'1½ tablespoons ginger-garlic paste',NULL,'Fats','22g',NULL,NULL,0),(5,'1 teaspoon turmeric powder',NULL,'Sugar','3g',NULL,NULL,0),(6,'1½ teaspoons red chili powder',NULL,'Fiber','2g',NULL,NULL,0),(7,'1 teaspoon garam masala',NULL,'Cholesterol','85mg',NULL,NULL,0),(8,'Salt to taste',NULL,'','',NULL,NULL,0),(9,'Juice of ½ lemon',NULL,'','',NULL,NULL,0),(10,'Handful of chopped mint and coriander leaves',NULL,'','',NULL,NULL,0),(11,'For Rice:',NULL,'','',NULL,NULL,0),(12,'2 cups basmati rice (soaked 30 mins)',NULL,'','',NULL,NULL,0),(13,'4–5 cups water',NULL,'','',NULL,NULL,0),(14,'1 bay leaf',NULL,'','',NULL,NULL,0),(15,'2–3 cloves',NULL,'','',NULL,NULL,0),(16,'2–3 green cardamoms',NULL,'','',NULL,NULL,0),(17,'1 small cinnamon stick',NULL,'','',NULL,NULL,0),(18,'Salt to taste',NULL,'','',NULL,NULL,0),(19,'Other Ingredients:',NULL,'','',NULL,NULL,0),(20,'2 medium onions (thinly sliced)',NULL,'','',NULL,NULL,0),(21,'2 tablespoons ghee',NULL,'','',NULL,NULL,0),(22,'2 tablespoons oil',NULL,'','',NULL,NULL,0),(23,'A pinch of saffron soaked in 2 tablespoons warm milk (optional)',NULL,'','',NULL,NULL,0),(24,'More mint and coriander for layering',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `chicken biryani` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chocolate cake`
--

DROP TABLE IF EXISTS `chocolate cake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chocolate cake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chocolate cake`
--

LOCK TABLES `chocolate cake` WRITE;
/*!40000 ALTER TABLE `chocolate cake` DISABLE KEYS */;
INSERT INTO `chocolate cake` VALUES (1,NULL,'80',NULL,NULL,'nonveg','dessert',1),(2,'1 and 3/4 cups all-purpose flour',NULL,'Calories','350 kcal',NULL,NULL,0),(3,'2 cups granulated sugar',NULL,'Protein','5 g',NULL,NULL,0),(4,'3/4 cup unsweetened cocoa powder',NULL,'Carbohydrates','52 g',NULL,NULL,0),(5,'2 teaspoons baking soda',NULL,'Fats','15 g',NULL,NULL,0),(6,'1 teaspoon baking powder',NULL,'Sugar','35 g',NULL,NULL,0),(7,'1 teaspoon salt',NULL,'Fiber','3 g',NULL,NULL,0),(8,'2 eggs',NULL,'Cholesterol','40 mg',NULL,NULL,0),(9,'1 cup whole milk',NULL,'','',NULL,NULL,0),(10,'1/2 cup vegetable oil',NULL,'','',NULL,NULL,0),(11,'2 teaspoons vanilla extract',NULL,'','',NULL,NULL,0),(12,'1 cup boiling water',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `chocolate cake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coffee`
--

DROP TABLE IF EXISTS `coffee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coffee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coffee`
--

LOCK TABLES `coffee` WRITE;
/*!40000 ALTER TABLE `coffee` DISABLE KEYS */;
INSERT INTO `coffee` VALUES (1,NULL,'7',NULL,NULL,'veg','Drinks',1),(2,'1 cup water',NULL,'Calories','90 kcal',NULL,NULL,0),(3,'1 to 1½ teaspoons ground coffee (instant or filter coffee powder)',NULL,'Protein','3g',NULL,NULL,0),(4,'½ cup milk (optional, for milk coffee)',NULL,'Carbs','10g',NULL,NULL,0),(5,'1 to 2 teaspoons sugar (adjust to taste)',NULL,'Fats','3g',NULL,NULL,0),(6,'Optional Add-ons:',NULL,'Sugar','5g',NULL,NULL,0),(7,'A pinch of cinnamon or cardamom',NULL,'Fiber','0g',NULL,NULL,0),(8,'Cocoa powder or vanilla essence',NULL,'Cholesterol','10mg',NULL,NULL,0);
/*!40000 ALTER TABLE `coffee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fish biryani`
--

DROP TABLE IF EXISTS `fish biryani`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fish biryani` (
  `ingredient` varchar(255) NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `meal_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fish biryani`
--

LOCK TABLES `fish biryani` WRITE;
/*!40000 ALTER TABLE `fish biryani` DISABLE KEYS */;
INSERT INTO `fish biryani` VALUES ('For the Fish Marinade','80','Calories','420 kcal','nonveg','Lunch'),('500 grams fish fillets (kingfish, salmon, or any firm fish)','80','Protein','28 g','nonveg','Lunch'),('1/2 cup yogurt','80','Carbohydrates','55 g','nonveg','Lunch'),('1 teaspoon turmeric powder','80','Fats','10 g','nonveg','Lunch'),('1 teaspoon red chili powder','80','Sugar','4 g','nonveg','Lunch'),('1 teaspoon garam masala','80','Fiber','3 g','nonveg','Lunch'),('1 teaspoon ginger-garlic paste','80','Cholesterol','45 mg','nonveg','Lunch'),('1/2 teaspoon salt','80','','','nonveg','Lunch'),('1 tablespoon lemon juice','80','','','nonveg','Lunch'),('For the Rice','80','','','nonveg','Lunch'),('2 cups basmati rice (soaked for 30 minutes)','80','','','nonveg','Lunch'),('4 cups water','80','','','nonveg','Lunch'),('2 bay leaves','80','','','nonveg','Lunch'),('4 cloves','80','','','nonveg','Lunch'),('2 cardamom pods','80','','','nonveg','Lunch'),('1 cinnamon stick','80','','','nonveg','Lunch'),('1 teaspoon salt','80','','','nonveg','Lunch'),('For the Biryani Masala','80','','','nonveg','Lunch'),('2 tablespoons oil or ghee','80','','','nonveg','Lunch'),('1 large onion, thinly sliced','80','','','nonveg','Lunch'),('2 tomatoes, chopped','80','','','nonveg','Lunch'),('1/2 cup chopped coriander leaves','80','','','nonveg','Lunch'),('1/4 cup chopped mint leaves','80','','','nonveg','Lunch'),('1 teaspoon cumin powder','80','','','nonveg','Lunch'),('1 teaspoon coriander powder','80','','','nonveg','Lunch'),('1/2 teaspoon garam masala','80','','','nonveg','Lunch'),('1/4 teaspoon saffron strands (soaked in 2 tablespoons warm milk)','80','','','nonveg','Lunch');
/*!40000 ALTER TABLE `fish biryani` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fried rice`
--

DROP TABLE IF EXISTS `fried rice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fried rice` (
  `ingredient` varchar(255) NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `meal_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fried rice`
--

LOCK TABLES `fried rice` WRITE;
/*!40000 ALTER TABLE `fried rice` DISABLE KEYS */;
INSERT INTO `fried rice` VALUES ('2 cups cooked and cooled rice (preferably day-old)','25','Calories','350 kcal','nonveg','dinner'),('2 tablespoons vegetable oil','25','Protein','10 g','nonveg','dinner'),('2 eggs, beaten','25','Carbohydrates','50 g','nonveg','dinner'),('1/2 cup diced carrots','25','Fats','12 g','nonveg','dinner'),('1/2 cup peas','25','Sugar','3 g','nonveg','dinner'),('1/2 cup diced onions','25','Fiber','3 g','nonveg','dinner'),('2 cloves garlic, minced','25','Cholesterol','80 mg','nonveg','dinner'),('1/2 cup cooked chicken, shrimp, or tofu (optional)','25','','','nonveg','dinner'),('2 tablespoons soy sauce','25','','','nonveg','dinner'),('1 teaspoon sesame oil','25','','','nonveg','dinner'),('1/2 teaspoon black pepper','25','','','nonveg','dinner'),('1/2 teaspoon salt (adjust to taste)','25','','','nonveg','dinner'),('2 green onions, chopped','25','','','nonveg','dinner');
/*!40000 ALTER TABLE `fried rice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grilled chicken with steamed veggies`
--

DROP TABLE IF EXISTS `grilled chicken with steamed veggies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grilled chicken with steamed veggies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grilled chicken with steamed veggies`
--

LOCK TABLES `grilled chicken with steamed veggies` WRITE;
/*!40000 ALTER TABLE `grilled chicken with steamed veggies` DISABLE KEYS */;
INSERT INTO `grilled chicken with steamed veggies` VALUES (1,'For the Grilled Chicken:',NULL,'Calories','320 kcal',NULL,NULL,0),(2,'2 boneless, skinless chicken breasts (approx. 150g each)',NULL,'Protein','38g',NULL,NULL,0),(3,'1 tablespoon olive oil',NULL,'Carbs','10g',NULL,NULL,0),(4,'1 tablespoon lemon juice','120','Fats','14g',NULL,NULL,0),(5,'1 teaspoon garlic powder (or 2 minced garlic cloves)',NULL,'Sugar','4g',NULL,NULL,0),(6,'1 teaspoon paprika',NULL,'Fiber','4g',NULL,NULL,0),(7,'½ teaspoon black pepper',NULL,'Cholesterol','~90mg',NULL,NULL,0),(8,'½ teaspoon salt',NULL,'','',NULL,NULL,0),(9,'1 teaspoon mixed herbs or Italian seasoning',NULL,'','',NULL,NULL,0),(10,'For the Steamed Veggies:',NULL,'','',NULL,NULL,0),(11,'½ cup broccoli florets',NULL,'','',NULL,NULL,0),(12,'½ cup carrot slices',NULL,'','',NULL,NULL,0),(13,'½ cup zucchini or bell pepper strips',NULL,'','',NULL,NULL,0),(14,'Salt and pepper to taste',NULL,'','',NULL,NULL,0),(15,'1 teaspoon olive oil or butter (optional)',NULL,'','',NULL,NULL,0),(16,'Lemon juice or herbs for garnish (optional)',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `grilled chicken with steamed veggies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gulab jamun`
--

DROP TABLE IF EXISTS `gulab jamun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gulab jamun` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gulab jamun`
--

LOCK TABLES `gulab jamun` WRITE;
/*!40000 ALTER TABLE `gulab jamun` DISABLE KEYS */;
INSERT INTO `gulab jamun` VALUES (1,'For the Jamuns:','50','Calories','150 kcal',NULL,NULL,0),(2,'1 cup khoya (mawa, grated)',NULL,'Protein','2g',NULL,NULL,0),(3,'3 tablespoons all-purpose flour (maida)',NULL,'Carbs','22g',NULL,NULL,0),(4,'2 tablespoons milk (or as needed to knead)',NULL,'Fats','6g',NULL,NULL,0),(5,'1/8 teaspoon baking soda',NULL,'Sugar','17g',NULL,NULL,0),(6,'Ghee or oil for deep frying',NULL,'Fiber','0.2g',NULL,NULL,0),(7,'For the Sugar Syrup:',NULL,'Cholesterol','10mg',NULL,NULL,0),(8,'1½ cups sugar',NULL,'','',NULL,NULL,0),(9,'1½ cups water',NULL,'','',NULL,NULL,0),(10,'3–4 green cardamom pods (lightly crushed)',NULL,'','',NULL,NULL,0),(11,'A few strands of saffron (optional)',NULL,'','',NULL,NULL,0),(12,'1 teaspoon rose water or a few drops of rose essence',NULL,'','',NULL,NULL,0),(13,'1 teaspoon lemon juice (to prevent crystallization)',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `gulab jamun` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `masala dosa`
--

DROP TABLE IF EXISTS `masala dosa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `masala dosa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `masala dosa`
--

LOCK TABLES `masala dosa` WRITE;
/*!40000 ALTER TABLE `masala dosa` DISABLE KEYS */;
INSERT INTO `masala dosa` VALUES (1,NULL,'45',NULL,NULL,'veg','Breakfast',1),(2,'For the Dosa Batter:',NULL,'Calories','250-300 kcal',NULL,NULL,0),(3,'2 cups rice (idli rice or parboiled rice)',NULL,'Protein','6-8g',NULL,NULL,0),(4,'½ cup urad dal (split black gram)',NULL,'Carbs','40-45g',NULL,NULL,0),(5,'¼ teaspoon fenugreek seeds',NULL,'Fats','6-8g',NULL,NULL,0),(6,'2 tablespoons poha (flattened rice)',NULL,'Sugar','2-3g',NULL,NULL,0),(7,'Salt to taste',NULL,'Fiber','3-5g',NULL,NULL,0),(8,'Water as needed',NULL,'Cholesterol','0mg',NULL,NULL,0),(9,'Oil or ghee for cooking',NULL,'','',NULL,NULL,0),(10,'For the Potato Masala Filling:',NULL,'','',NULL,NULL,0),(11,'3 large potatoes, boiled and mashed',NULL,'','',NULL,NULL,0),(12,'1 onion, thinly sliced',NULL,'','',NULL,NULL,0),(13,'1 green chili, chopped',NULL,'','',NULL,NULL,0),(14,'½ teaspoon mustard seeds',NULL,'','',NULL,NULL,0),(15,'½ teaspoon turmeric powder',NULL,'','',NULL,NULL,0),(16,'½ teaspoon cumin seeds',NULL,'','',NULL,NULL,0),(17,'8-10 curry leaves',NULL,'','',NULL,NULL,0),(18,'1 teaspoon ginger, grated',NULL,'','',NULL,NULL,0),(19,'½ teaspoon red chili powder (optional)',NULL,'','',NULL,NULL,0),(20,'¼ cup water',NULL,'','',NULL,NULL,0),(21,'Salt to taste',NULL,'','',NULL,NULL,0),(22,'1 tablespoon oil',NULL,'','',NULL,NULL,0),(23,'2 tablespoons chopped coriander leaves',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `masala dosa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mojito`
--

DROP TABLE IF EXISTS `mojito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mojito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mojito`
--

LOCK TABLES `mojito` WRITE;
/*!40000 ALTER TABLE `mojito` DISABLE KEYS */;
INSERT INTO `mojito` VALUES (1,NULL,'7',NULL,NULL,'veg','Drinks',1),(2,'10 fresh mint leaves',NULL,'Calories','40 kcal',NULL,NULL,0),(3,'½ lime, cut into 4 wedges',NULL,'Carbs','10g',NULL,NULL,0),(4,'2 teaspoons sugar (white or cane)',NULL,'Sugar','8g',NULL,NULL,0),(5,'1 cup club soda (chilled)',NULL,'Cholesterol','0mg',NULL,NULL,0),(6,'Ice cubes',NULL,'','',NULL,NULL,0),(7,'45 ml white rum (optional – omit for mocktail version)',NULL,'','',NULL,NULL,0),(8,'Extra mint sprig and lime slice for garnish',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `mojito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pancake`
--

DROP TABLE IF EXISTS `pancake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pancake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pancake`
--

LOCK TABLES `pancake` WRITE;
/*!40000 ALTER TABLE `pancake` DISABLE KEYS */;
INSERT INTO `pancake` VALUES (1,NULL,'25',NULL,NULL,'veg','Breakfast',1),(2,'1½ cups all-purpose flour',NULL,'Calories','95 kcal',NULL,NULL,0),(3,'3½ teaspoons baking powder',NULL,'Protein','3g',NULL,NULL,0),(4,'1 tablespoon sugar',NULL,'Carbohydrates','13g',NULL,NULL,0),(5,'¼ teaspoon salt',NULL,'Fats','4g',NULL,NULL,0),(6,'1¼ cups milk',NULL,'Sugar','2g',NULL,NULL,0),(7,'1 egg',NULL,'Fiber','0.5g',NULL,NULL,0),(8,'3 tablespoons melted butter (plus more for greasing)',NULL,'Cholesterol','25mg',NULL,NULL,0),(9,'1 teaspoon vanilla extract (optional)',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `pancake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pasta alfredo`
--

DROP TABLE IF EXISTS `pasta alfredo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasta alfredo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasta alfredo`
--

LOCK TABLES `pasta alfredo` WRITE;
/*!40000 ALTER TABLE `pasta alfredo` DISABLE KEYS */;
INSERT INTO `pasta alfredo` VALUES (1,NULL,'25',NULL,NULL,'veg','Lunch',1),(2,'For the Pasta:',NULL,'Calories','600 kcal',NULL,NULL,0),(3,'200g fettuccine or penne pasta',NULL,'','',NULL,NULL,0),(4,'Water for boiling',NULL,'','',NULL,NULL,0),(5,'Salt for seasoning',NULL,'','',NULL,NULL,0),(6,'For the Alfredo Sauce:',NULL,'','',NULL,NULL,0),(7,'2 tablespoons butter',NULL,'Sugar','3g',NULL,NULL,0),(8,'1 tablespoon olive oil',NULL,'Fiber','2g',NULL,NULL,0),(9,'4–5 garlic cloves (finely chopped)',NULL,'Cholesterol','85mg',NULL,NULL,0),(10,'1 cup heavy cream',NULL,'','',NULL,NULL,0),(11,'¾ cup grated Parmesan cheese (or processed cheese if unavailable)',NULL,'','',NULL,NULL,0),(12,'Salt to taste',NULL,'','',NULL,NULL,0),(13,'½ teaspoon black pepper',NULL,'','',NULL,NULL,0),(14,'A pinch of nutmeg (optional)',NULL,'','',NULL,NULL,0),(15,'Chopped parsley or oregano for garnish',NULL,'','',NULL,NULL,0),(16,'Optional Add-ins:',NULL,'','',NULL,NULL,0),(17,'½ cup steamed broccoli or sautéed mushrooms (for veg)',NULL,'','',NULL,NULL,0),(18,'Grilled chicken strips or shrimp (for non-veg)',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `pasta alfredo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `red velvet cake`
--

DROP TABLE IF EXISTS `red velvet cake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `red velvet cake` (
  `ingredient` varchar(255) NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `meal_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `red velvet cake`
--

LOCK TABLES `red velvet cake` WRITE;
/*!40000 ALTER TABLE `red velvet cake` DISABLE KEYS */;
INSERT INTO `red velvet cake` VALUES ('For the Cake','80','calories','450 kcal','nonveg','dessert'),('2 and 1/2 cups all-purpose flour','80','Protein','5 g','nonveg','dessert'),('1 and 1/2 cups granulated sugar','80','Carbohydrates','55 g','nonveg','dessert'),('1 teaspoon baking soda','80','Fats','24 g','nonveg','dessert'),('1 teaspoon salt','80','Sugar','38 g','nonveg','dessert'),('1 teaspoon cocoa powder','80','Fiber','1 g','nonveg','dessert'),('1 cup buttermilk','80','Cholesterol','55 mg','nonveg','dessert'),('1 cup vegetable oil','80','','','nonveg','dessert'),('2 eggs','80','','','nonveg','dessert'),('2 teaspoons vanilla extract','80','','','nonveg','dessert'),('1 teaspoon white vinegar','80','','','nonveg','dessert'),('2 tablespoons red food coloring','80','','','nonveg','dessert'),('For the Cream Cheese Frosting','80','','','nonveg','dessert'),('8 ounces cream cheese (softened)','80','','','nonveg','dessert'),('1/2 cup unsalted butter (softened)','80','','','nonveg','dessert'),('2 cups powdered sugar','80','','','nonveg','dessert'),('1 teaspoon vanilla extract','80','','','nonveg','dessert');
/*!40000 ALTER TABLE `red velvet cake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rice and fish curry`
--

DROP TABLE IF EXISTS `rice and fish curry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rice and fish curry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rice and fish curry`
--

LOCK TABLES `rice and fish curry` WRITE;
/*!40000 ALTER TABLE `rice and fish curry` DISABLE KEYS */;
INSERT INTO `rice and fish curry` VALUES (1,NULL,'40',NULL,NULL,'nonveg','Dinner',1),(2,'For the Fish Curry:',NULL,'Calories','420 kcal',NULL,NULL,0),(3,'500g firm fish (like rohu, kingfish, pomfret, or tilapia), cleaned and cut',NULL,'Protein','30g',NULL,NULL,0),(4,'2 tablespoons oil (coconut oil or vegetable oil)',NULL,'Fats','18g',NULL,NULL,0),(5,'1 teaspoon mustard seeds',NULL,'Fiber','2g',NULL,NULL,0),(6,'1 onion, finely chopped',NULL,'','',NULL,NULL,0),(7,'2 tomatoes, pureed or finely chopped',NULL,'','',NULL,NULL,0),(8,'1 tablespoon ginger-garlic paste',NULL,'','',NULL,NULL,0),(9,'½ teaspoon turmeric powder',NULL,'','',NULL,NULL,0),(10,'1 teaspoon red chili powder',NULL,'','',NULL,NULL,0),(11,'1½ teaspoons coriander powder',NULL,'','',NULL,NULL,0),(12,'1 teaspoon garam masala',NULL,'','',NULL,NULL,0),(13,'Salt to taste',NULL,'','',NULL,NULL,0),(14,'1 cup water (adjust consistency)',NULL,'','',NULL,NULL,0),(15,'Fresh coriander leaves for garnish',NULL,'','',NULL,NULL,0),(16,'½ cup coconut milk (optional for a creamy version)',NULL,'','',NULL,NULL,0),(17,'1 tablespoon tamarind pulp or juice of ½ lemon',NULL,'','',NULL,NULL,0),(18,'For Steamed Rice:',NULL,'','',NULL,NULL,0),(19,'1 cup basmati or short-grain rice',NULL,'','',NULL,NULL,0),(20,'2 cups water',NULL,'','',NULL,NULL,0),(21,'Pinch of salt',NULL,'','',NULL,NULL,0);
/*!40000 ALTER TABLE `rice and fish curry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scrambled eggs`
--

DROP TABLE IF EXISTS `scrambled eggs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scrambled eggs` (
  `ingredient` varchar(255) NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `meal_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scrambled eggs`
--

LOCK TABLES `scrambled eggs` WRITE;
/*!40000 ALTER TABLE `scrambled eggs` DISABLE KEYS */;
INSERT INTO `scrambled eggs` VALUES ('2 large eggs','7','Calories','250 kcal','nonveg','Breakfast'),('2 slices of bread (whole wheat, sourdough, or white)','7','Protein','14g','nonveg','Breakfast'),('1 tablespoon butter (or olive oil)','7','Carbohydrates','20g','nonveg','Breakfast'),('2 tablespoons milk (optional, for creamier eggs)','7','Fats','12 g','nonveg','Breakfast'),('Salt and black pepper to taste','7','Sugar','2 g','nonveg','Breakfast'),('¼ teaspoon paprika or chili flakes (optional)','7','Fiber','2 g','nonveg','Breakfast'),('Fresh herbs (chives, parsley, or cilantro) for garnish','7','Cholesterol','370 mg','nonveg','Breakfast');
/*!40000 ALTER TABLE `scrambled eggs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strawberry shake`
--

DROP TABLE IF EXISTS `strawberry shake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strawberry shake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(255) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `nutrition` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `meal_type` varchar(50) DEFAULT NULL,
  `is_metadata` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strawberry shake`
--

LOCK TABLES `strawberry shake` WRITE;
/*!40000 ALTER TABLE `strawberry shake` DISABLE KEYS */;
INSERT INTO `strawberry shake` VALUES (1,NULL,'6',NULL,NULL,'veg','Drinks',1),(2,'1 cup fresh or frozen strawberries (hulled)',NULL,'Calories','250 kcal',NULL,NULL,0),(3,'1 cup chilled milk (full-fat or low-fat)',NULL,'Protein','6g',NULL,NULL,0),(4,'2 scoops vanilla or strawberry ice cream',NULL,'Carbs','35g',NULL,NULL,0),(5,'1–2 tablespoons sugar or honey (adjust to taste)',NULL,'Fats','10g',NULL,NULL,0),(6,'4–5 ice cubes (optional)',NULL,'Sugar','25g',NULL,NULL,0),(7,'Whipped cream and chopped strawberries for garnish (optional)',NULL,'Fiber','2g',NULL,NULL,0);
/*!40000 ALTER TABLE `strawberry shake` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-10 14:11:43
