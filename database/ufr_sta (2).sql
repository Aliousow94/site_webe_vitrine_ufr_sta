-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 09 juil. 2026 à 15:15
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `ufr_sta`
--

-- --------------------------------------------------------

--
-- Structure de la table `activite`
--

CREATE TABLE `activite` (
  `id` int(11) NOT NULL,
  `titre` varchar(200) DEFAULT NULL,
  `date_activite` date DEFAULT NULL,
  `lieu` varchar(150) DEFAULT NULL,
  `organisateur` varchar(150) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `activite`
--

INSERT INTO `activite` (`id`, `titre`, `date_activite`, `lieu`, `organisateur`, `description`) VALUES
(5, 'journée d\'exelence ', '2026-06-24', 'Anexe du rectorat', 'UFR STA', 'L’Amicale des Étudiants de l’UFR Sciences et Technologies Avancées de l’Université Amadou Mahtar Mbow (UAM), dirigée par M. Moctar SALL, a organisé, le samedi 09 mai 2026, une grande Journée de l’Excellence dédiée à la célébration du mérite académique, de l’engagement estudiantin et de la promotion de l’excellence au sein de l’institution universitaire.\r\nCette importante manifestation s’est tenue sous le haut parrainage du Professeur Amadou Dahirou GUEYE, Vice-Recteur chargé des Affaires pédagogiques et de la Vie universitaire. Elle a également enregistré la présence du représentant du Directeur de l’UFR, M. Aidara NGOM, Chef des Services Administratifs, du Dr Thierno Mohamadane Mansour SOW, Chef du Département Mathématiques, Informatique et Modélisation, du Dr Makha NDAO, Chef du Département Sciences de la Mer et de l’Univers, ainsi que des enseignants-chercheurs et de nombreux étudiants de l’UFR.');

-- --------------------------------------------------------

--
-- Structure de la table `actualite`
--

CREATE TABLE `actualite` (
  `id` int(11) NOT NULL,
  `titre` varchar(200) DEFAULT NULL,
  `date_publication` date DEFAULT NULL,
  `description` text DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `actualite`
--

INSERT INTO `actualite` (`id`, `titre`, `date_publication`, `description`, `photo`) VALUES
(17, 'Conference sur Mathematique appliquées', '2025-04-20', 'Le 30 avril 2025, l’UFR Sciences et Technologies Avancées (STA) a organisé une conférence scientifique animée par Abdou Sène. Cette rencontre a mis en lumière les applications des mathématiques dans la résolution de défis scientifiques et sociétaux. Elle a également favorisé les échanges autour de la recherche, de l’innovation et de la modélisation.', 'aidara.jpg'),
(22, 'Jeu Olimpique de la jeunesse(joj)', '2026-06-11', 'En raison de l\'organisation des Jeux Olympiques de la Jeunesse (JOJ) de Dakar 2026 et du lancement simultané de grands travaux de modernisation des infrastructures, les autorités administratives de l\'Université Amadou Mahtar Mbow annoncent la fermeture temporaire du campus. L\'établissement suspendra ses activités en présentiel à compter de ce mois-ci, pour une réouverture officielle prévue en janvier 2027.', 'images_2.jpg');

-- --------------------------------------------------------

--
-- Structure de la table `administrateur`
--

CREATE TABLE `administrateur` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `motdepasse` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `administrateur`
--

INSERT INTO `administrateur` (`id`, `nom`, `email`, `motdepasse`) VALUES
(1, 'Aliou', 'mamadoualiousow543@gmail.com', 'STA');

-- --------------------------------------------------------

--
-- Structure de la table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `sujet` varchar(200) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `date_envoi` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `contact`
--

INSERT INTO `contact` (`id`, `nom`, `email`, `sujet`, `message`, `date_envoi`) VALUES
(2, 'Mamadou Aliou SOW', 'aliou22@gmail.com', 'Reclamation de note', 'je veut consulter mes copies car j\'ai constater des erreur sur mes notes de mathematique et physique ', '2026-07-07 12:30:55'),
(3, 'ABdou Ba ', 'abdou333@gmail.com', 'Justification d\'absence ', 'La semaine passée j\'etais absent la cause etait que je me sentais pas bien ', '2026-07-07 12:32:16');

-- --------------------------------------------------------

--
-- Structure de la table `departement`
--

CREATE TABLE `departement` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `responsable` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `departement`
--

INSERT INTO `departement` (`id`, `nom`, `description`, `responsable`, `contact`) VALUES
(2, 'Mathematique Informatique et Modelisation(MIM)', 'Ce Departement a pour objectif de permettre aux étudiants d’acquérir des connaissances fondamentales, de développer des compétences analytiques et de résolution de problèmes, d’explorer les intersections interdisciplinaires et de préparer aux spécialisations et à la recherche scientifique.', 'Thierno Mouhamadane Mansour SOW', ' thierno.sow@uam.edu.sn'),
(3, 'Science de la Matiere et de l\'Univers(SMU)', 'Ce departement  a pour objectif d’offrir aux étudiants la possibilité d’acquérir une formation qui leur permette d’accéder au plus haut niveau des connaissances académiques tant en recherche que dans le domaine professionnel. Elle prépare les étudiants aux métiers de la protection et de l’aménagement des côtes, des ports, des plateformes offshores pétrolières et gazières (Génie côtier, Génie portuaire, Génie maritime), de la gestion des ressources marines et des écosystèmes côtiers et marins, de la biodiversité marine, de l’économie bleue et la résilience climatique et des territoires littoraux.', 'Dr Makha Ndao', 'makha.ndao@uam.edu.sn');

-- --------------------------------------------------------

--
-- Structure de la table `enseignant`
--

CREATE TABLE `enseignant` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `grade` varchar(100) DEFAULT NULL,
  `departement` varchar(100) DEFAULT NULL,
  `departement_id` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `domaine_recherche` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `enseignant`
--

INSERT INTO `enseignant` (`id`, `nom`, `photo`, `grade`, `departement`, `departement_id`, `email`, `domaine_recherche`) VALUES
(1, 'Dr Ibrahima Coulibaly', 'derecteur.png', 'Enseignant-Chercheur', NULL, 2, 'coulibaly@gmail.com', 'Statistique descriptive '),
(2, 'Dr Thierno Mouhamadane Mansour Sow', '700306103_122195059628429789_9183672534653754568_n.jpg', 'Enseignant-Chercheur', NULL, 2, 'thierno.sow@uam.edu.sn', 'Algebre lineaire'),
(3, 'Dr Dahirou Gueye ', '700272300_122195059106429789_3220444134498499447_n.jpg', 'Professeur', NULL, 2, 'dahirou.gueye@uam.edu.sn', 'Inteligence Artificielle '),
(4, 'Dr Makha Ndow', 'images6.jpg', 'Enseignant-Chercheur', NULL, 3, 'makha.ndao@uam.edu.sn', 'Mecanique generale');

-- --------------------------------------------------------

--
-- Structure de la table `formation`
--

CREATE TABLE `formation` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `niveau` varchar(50) DEFAULT NULL,
  `duree` varchar(50) DEFAULT NULL,
  `admission` text DEFAULT NULL,
  `debouches` text DEFAULT NULL,
  `programme` text DEFAULT NULL,
  `departement_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `formation`
--

INSERT INTO `formation` (`id`, `nom`, `niveau`, `duree`, `admission`, `debouches`, `programme`, `departement_id`) VALUES
(3, 'Mathematique Physique Informatique (MPI)', 'Licence', '3ans', 'Obtenir un bac scientifique(S2,S1) avec une moyenne superieur ou egale a 12 en Mathematique et physique', 'Enseignant ou Enseignant-chercheur.\r\nDéveloppeurs, ingénieurs logiciels, architectes de données, analystes en sécurité informatique, administrateurs et intégrateur d’applications,\r\nadministrateurs en réseaux et systèmes, spécialistes en intelligence artificielle, en IoT, data scientists, etc.\r\nLes entreprises de divers secteurs, comme l\'industrie pharmaceutique, l\'énergie, l\'aérospatiale, font appel à des experts en mathématiques et en physique pour des postes de recherche et développement, visant à améliorer les produits et les technologies existantes.\r\nLes mathématiques sont fondamentales dans les domaines de la finance, de l\'assurance et de la gestion des risques. Cette filière offre donc des opportunités dans les métiers du secteur tertiaire, comme : les Banques et les assurances (actuariat, audit, analyste quantitatif, trader, gestionnaire de portefeuille, finance et ingénierie financièr;', 'La licence 1 est composée de deux semestre :\r\nsemestre 1: les matiére enseignés sont :\r\nUE Mathematique : Analyse 1,Algebre 1\r\nUE Physique: Mecanique du point, Electricite\r\nUE Informatique: Programation , Logique Combinatoire \r\nsemestre 2: les matiere endeignées sont : analyse 2, Algebre 2, Statistique,Langage C, VHDL, Optique geopmetrique,electromagnetique', 2),
(4, 'Science de la Maire et du Littorale', 'Licence', '3ans', 'faire les serie suivant : S1,S2,S4,S5', 'Enseignant-Chercheur ou Chercheur dans le secteur public et/ou privé ;\r\nChercheur en biologie et écologie marine en laboratoires de recherche institutionnelle ;\r\nChargé de mission/ingénieur d’étude en environnement littoral et marin en laboratoires de recherche institutionnelle, bureaux d’études, collectivités territoriales, agences d’état et d’industries de la mer, services recherche d’entreprise et développement ou environnement d’entreprises privées, conservatoires et parcs marins, associations environnementales ;\r\nChargé de mission/ingénieur d’étude dans le domaine des ressources marines vivantes dans des organisations professionnelles, entreprises aquacoles, l’administration des pêches et de l’aquaculture.', 'La licence 1 est composée de deux semestre :\r\nsemestre 1: les matiére enseignés sont :\r\nUE Mathematique : Analyse 1,Algebre 1\r\nUE Physique: Mecanique du point, Electricite\r\nUE Informatique: Programation , Logique Combinatoire \r\nsemestre 2: les matiere endeignées sont : analyse 2, Algebre 2, Statistique,Langage C, VHDL, Optique geopmetrique,electromagnetique', 3);

-- --------------------------------------------------------

--
-- Structure de la table `galerie`
--

CREATE TABLE `galerie` (
  `id` int(11) NOT NULL,
  `titre` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `date_album` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `galerie`
--

INSERT INTO `galerie` (`id`, `titre`, `description`, `date_album`) VALUES
(3, 'Celebration du 7eme edition  de la Journée internationale des gens de mer ', '\'Agence Nationale des Affaires Maritimes (ANAM) a célébré, le 25 juin 2026, la 7ᵉ édition de la Journée internationale des gens de mer au Grand Théâtre National Doudou Ndiaye Rose de Dakar, autour du thème : « Transporter le commerce mondial, supporter les risques ».\r\nSur invitation de l\'ANAM, les étudiants de l\'UFR Sciences, Technologies et Avancées (STA) de l\'UAM ont pris part à cette importante journée. Ils étaient accompagnés par le Chef du Département Sciences de la Matière et de l\'Univers (SMU), le Dr Makha NDAO, ainsi que par le Vice-Recteur chargé de la Recherche, de l\'Innovation et du Partenariat, le Pr Issa SAKHO.\r\nLes étudiants ont assisté aux différentes allocutions des autorités présentes et ont également représenté l\'UAM à travers un stand mis à disposition par l\'ANAM. Ce stand a permis de présenter les différentes formations offertes par les filières de l\'UFR STA.', '2026-07-09');

-- --------------------------------------------------------

--
-- Structure de la table `photo_activite`
--

CREATE TABLE `photo_activite` (
  `id` int(11) NOT NULL,
  `id_activite` int(11) NOT NULL,
  `photo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `photo_activite`
--

INSERT INTO `photo_activite` (`id`, `id_activite`, `photo`) VALUES
(10, 5, 'act5_images4.jpg'),
(11, 5, 'act5_700004968_122195059694429789_3402960598023567389_n.jpg');

-- --------------------------------------------------------

--
-- Structure de la table `photo_galerie`
--

CREATE TABLE `photo_galerie` (
  `id` int(11) NOT NULL,
  `galerie_id` int(11) NOT NULL,
  `photo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `photo_galerie`
--

INSERT INTO `photo_galerie` (`id`, `galerie_id`, `photo`) VALUES
(2, 3, 'gal3_733374118_122199737552429789_9175251622167559630_n.jpg');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activite`
--
ALTER TABLE `activite`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `actualite`
--
ALTER TABLE `actualite`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `administrateur`
--
ALTER TABLE `administrateur`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `departement`
--
ALTER TABLE `departement`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `enseignant`
--
ALTER TABLE `enseignant`
  ADD PRIMARY KEY (`id`),
  ADD KEY `departement_id` (`departement_id`);

--
-- Index pour la table `formation`
--
ALTER TABLE `formation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `departement_id` (`departement_id`);

--
-- Index pour la table `galerie`
--
ALTER TABLE `galerie`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `photo_activite`
--
ALTER TABLE `photo_activite`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_activite` (`id_activite`);

--
-- Index pour la table `photo_galerie`
--
ALTER TABLE `photo_galerie`
  ADD PRIMARY KEY (`id`),
  ADD KEY `galerie_id` (`galerie_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `activite`
--
ALTER TABLE `activite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `actualite`
--
ALTER TABLE `actualite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT pour la table `administrateur`
--
ALTER TABLE `administrateur`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `departement`
--
ALTER TABLE `departement`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `enseignant`
--
ALTER TABLE `enseignant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `formation`
--
ALTER TABLE `formation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `galerie`
--
ALTER TABLE `galerie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `photo_activite`
--
ALTER TABLE `photo_activite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT pour la table `photo_galerie`
--
ALTER TABLE `photo_galerie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `enseignant`
--
ALTER TABLE `enseignant`
  ADD CONSTRAINT `enseignant_ibfk_1` FOREIGN KEY (`departement_id`) REFERENCES `departement` (`id`);

--
-- Contraintes pour la table `formation`
--
ALTER TABLE `formation`
  ADD CONSTRAINT `formation_ibfk_1` FOREIGN KEY (`departement_id`) REFERENCES `departement` (`id`);

--
-- Contraintes pour la table `photo_activite`
--
ALTER TABLE `photo_activite`
  ADD CONSTRAINT `photo_activite_ibfk_1` FOREIGN KEY (`id_activite`) REFERENCES `activite` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `photo_galerie`
--
ALTER TABLE `photo_galerie`
  ADD CONSTRAINT `photo_galerie_ibfk_1` FOREIGN KEY (`galerie_id`) REFERENCES `galerie` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
