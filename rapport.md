 

 

RAPPORT TECHNIQUE DÉTAILLÉ 

CONCEPTION ET DÉVELOPPEMENT D'UN SIMULATEUR DE MICROPROCESSEUR (MOTOROLA 6809) 

 

Module : Architecture des Ordinateurs & Programmation Système 

 
DEPARTEMENT INFORMATIQUE 

Filière : Licence Génie Informatique 

 

Année Universitaire : 2025 – 2026 

 

Auteurs :  

AKIL ILYASS  (Groupe 1)                 

LAFDAIGUI YOUNES (Groupe 2) 

Date : 21 Décembre 2025 

Prof : Hicham Benalla 

 

 

 

TABLE DES MATIÈRES DÉTAILLÉE 

INTRODUCTION GÉNÉRALE 

1.1. Contexte du projet et choix du processeur 

1.2. Problématique : De la théorie à la pratique 

1.3. Objectifs du livrable (Sim6809 Studio) 

FONDEMENTS THÉORIQUES 

2.1. L'Architecture de Von Neumann 

2.2. Le cycle d'instruction (Fetch-Decode-Execute) 

2.3. Spécificités du Motorola 6809 (CISC, Piles, Big Endian) 

ENVIRONNEMENT DE DÉVELOPPEMENT 

3.1. Langage Java : Gestion de la mémoire et Typage 

3.2. Apache Maven : Cycle de vie du projet 

3.3. JavaFX : Architecture du Graphe de Scène 

ARCHITECTURE LOGICIELLE (DESIGN PATTERNS) 

4.1. Le modèle MVC (Modèle-Vue-Contrôleur) 

4.2. Le pattern Observer pour la mémoire 

4.3. Diagramme de composants 

ANALYSE DÉTAILLÉE DU MODÈLE (com.sim6809.model) 

5.1. Classe Bus : Abstraction de la carte mère 

5.2. Classe Cpu6809 : L'Unité Centrale de Traitement 

5.3. Classe Asm : Algorithmique de compilation à deux passes 

ANALYSE DÉTAILLÉE DE L'INTERFACE (com.sim6809.ui) 

6.1. Classe MainApp : Le chef d'orchestre 

6.2. Moteur de rendu et AnimationTimer 

6.3. Ergonomie et Design "Ultimate UI" 

DÉFIS TECHNIQUES ET SOLUTIONS 

7.1. La problématique des entiers signés en Java 

7.2. Simulation des interruptions matérielles (IRQ/FIRQ) 

7.3. Gestion du temps et des cycles d'horloge 

 

GUIDE D'UTILISATION ET VALIDATION 

8.1. ALGORITHME DE COMPILATION (Asm.java) 

8.1.2 L'Algorithme "Two-Pass" 

8.2 GUIDE D'UTILISATION (INTERFACE GRAPHIQUE) 

8.3. DOCUMENTATION TECHNIQUE INTERNE 

8.3.1. Le Processeur (Cpu6809) 

8.3.2. La Mémoire (Bus) 

8.4 TABLEAU DE CORRESPONDANCE : DU MATÉRIEL AU LOGICIEL 

CONCLUSION ET PERSPECTIVES 

 

1. INTRODUCTION GÉNÉRALE 

1.1. Contexte du projet 

L'enseignement de l'architecture des ordinateurs repose souvent sur des concepts abstraits : registres, bus, signaux de contrôle. Le projet Sim6809 Studio vise à concrétiser ces notions en développant un émulateur logiciel du microprocesseur Motorola 6809. 

Lancé en 1978, le 6809 est considéré comme l'un des processeurs 8-bits les plus puissants et les plus élégants jamais conçus. Son jeu d'instructions orthogonal (toutes les instructions s'appliquent de manière cohérente aux registres) en fait le candidat idéal pour comprendre les mécanismes bas niveau sans la complexité excessive des processeurs modernes (x86, ARM). 

1.2. Problématique 

Comment simuler fidèlement, dans un langage de haut niveau orienté objet (Java), le comportement électrique et séquentiel d'un composant électronique des années 80, tout en offrant une visualisation moderne et interactive ? 

Le défi réside dans la traduction de signaux binaires en structures de données logicielles, et dans la synchronisation d'un temps d'exécution virtuel avec le temps réel de l'utilisateur. 

1.3. Objectifs du livrable 

Le logiciel final doit être un IDE (Environnement de Développement Intégré) complet, capable de : 

Éditer du code source assembleur. 

Assembler ce code en langage machine (opcodes). 

Exécuter le programme en visualisant les flux de données. 

Déboguer via une exécution pas-à-pas et l'inspection de la mémoire. 

 

2. FONDEMENTS THÉORIQUES 

Avant d'aborder le code, il est nécessaire de définir les concepts que nous simulons. 

2.1. L'Architecture de Von Neumann 

Notre simulateur respecte l'architecture de Von Neumann, caractérisée par : 

Une mémoire unique contenant à la fois les instructions du programme et les données. 

Une unité de traitement (CPU) contenant une Unité Arithmétique et Logique (UAL) et des registres. 

Un mécanisme séquentiel de lecture d'instructions via un Compteur Ordinal (PC - Program Counter). 

2.2. Spécificités du Motorola 6809 

Architecture 8-bits / 16-bits : Bien que le bus de données soit de 8 bits, le 6809 possède des registres de 16 bits (X, Y, U, S, PC) et permet de combiner les accumulateurs A et B en un registre virtuel D de 16 bits. 

Big Endian : Le 6809 stocke l'octet de poids fort à l'adresse mémoire la plus petite. Notre simulateur doit respecter cet ordre rigoureusement dans les méthodes readWord et writeWord. 

Double Pile : Contrairement à la plupart des processeurs qui n'ont qu'une pile système (S), le 6809 offre une pile utilisateur (U), permettant de séparer le contexte d'exécution du système de celui de l'application. 

 

3. ENVIRONNEMENT DE DÉVELOPPEMENT 

3.1. Le Langage Java (JDK 17) 

Java a été choisi pour sa robustesse et sa portabilité. 

Modélisation Objet : La POO permet de représenter physiquement les composants. La classe Bus est la carte mère, la classe Cpu est la puce. 

Gestion Mémoire : Le Garbage Collector libère le développeur de la gestion manuelle de la mémoire de l'hôte, permettant de se concentrer sur la gestion de la mémoire simulée. 

Typage Primitif : L'utilisation des types int (32 bits) pour simuler des registres 8 ou 16 bits nécessite une discipline rigoureuse de masquage binaire (& 0xFF), un point clé de ce projet. 

3.2. Apache Maven 

Maven automatise la production du logiciel. 

Dépendances : Le fichier pom.xml déclare les bibliothèques JavaFX (javafx-controls, javafx-fxml). Maven les télécharge et les lie au projet automatiquement, garantissant que le simulateur fonctionne sur n'importe quelle machine de développement. 

Structure : Le respect de l'arborescence standard (src/main/java, target/classes) facilite la lecture et la compilation via des commandes standardisées (mvn clean package). 

3.3. JavaFX 

Successeur de Swing, JavaFX offre une architecture moderne basée sur un Graphe de Scène (Scene Graph). 

Rendu Vectoriel : Les composants de l'interface (comme le schéma de l'UAL) sont des formes vectorielles (Shape), redimensionnables sans perte de qualité. 

CSS (Cascading Style Sheets) : L'apparence est séparée de la logique. Le thème "Dark Mode" et les couleurs syntaxiques des registres sont définis via des styles CSS, rendant le code Java plus propre. 

 

4. ARCHITECTURE LOGICIELLE GLOBALE 

Pour garantir la maintenabilité, nous appliquons le patron MVC (Modèle-Vue-Contrôleur). 

4.1. Séparation des Responsabilités 

Le Modèle (com.sim6809.model) : Contient l'état du système (RAM, Registres) et la logique métier. Il ne sait rien de l'interface graphique. Il peut théoriquement tourner dans une console textuelle. 

La Vue/Contrôleur (com.sim6809.ui) : MainApp observe le modèle, l'affiche à l'utilisateur, et transmet les commandes (Run, Step, Reset) au modèle. 

4.2. Communication via Observer Pattern 

Comment l'interface sait-elle qu'elle doit se mettre à jour ? 

La classe Bus implémente un mécanisme d'observation. 

L'interface s'enregistre comme écouteur (addListener). 

Dès qu'une instruction CPU écrit en mémoire (bus.write()), le Bus notifie l'interface. 

L'interface rafraîchit uniquement la zone concernée. 

 

5. ANALYSE DÉTAILLÉE DU MODÈLE (com.sim6809.model) 

C'est le cœur "Hardware" du projet. 

5.1. Classe Bus : L'Interconnexion 

Cette classe simule l'espace d'adressage de 64 Ko. 

Attributs : 

private final int[] ram = new int[65536]; : Le tableau représentant les cellules mémoire. Nous utilisons int pour stocker des valeurs non signées (0-255). 

Méthodes Critiques : 

read(int addr) : Retourne la valeur à l'adresse donnée. Applique addr & 0xFFFF pour simuler le bouclage d'adresse (Mirroring). 

write(int addr, int data) : Écrit une valeur. Applique data & 0xFF pour tronquer les données à 8 bits. Déclenche les notifyListeners. 

readWord / writeWord : Gèrent l'accès 16 bits en Big Endian (Poids fort à l'adresse addr, poids faible à addr+1). 

5.2. Classe Cpu6809 : Le Processeur 

Le processeur n'est pas simplement une boucle, c'est une Machine à États Finis (FSM). 

Le Cycle step() et l'Optimisation JVM : La méthode step() structure le cycle Fetch-Decode-Execute. L'étape de décodage utilise un switch(opcode). Bien que cette structure paraisse verbeuse en Java, elle est compilée par la JVM sous forme de Table de Saut (tableswitch/lookupswitch). Cela garantit une complexité temporelle de O(1) : le programme saute directement à la bonne instruction sans évaluer des centaines de conditions if/else. 

Gestion Mathématique des Drapeaux (Flags) : Le registre CC est le plus complexe à émuler. Le calcul des drapeaux (notamment V - Overflow) suit une logique booléenne stricte. 

Exemple du calcul de V (Débordement signé 8 bits) : Lors d'une soustraction R = A - B, le débordement se produit si l'on soustrait un positif d'un négatif (ou inversement) et que le signe du résultat est incohérent. La formule implémentée est : V = ((A ^ B) & (A ^ R) & 0x80) != 0. Cela isole le bit de poids fort (MSB) via le masque 0x80 pour détecter l'inversion de signe non désirée. 

Abstraction Matérielle : L'instruction TFR : L'instruction de transfert (TFR R1, R2) illustre l'abstraction objet. Au lieu d'écrire 100 cas (A->B, A->X...), le code utilise un système d'ID interne (0=D, 1=X, 2=Y... 11=DP). Les méthodes getRegVal(id) et setRegVal(id, val) agissent comme des multiplexeurs logiciels, rendant le code de transfert générique et compact. 

Cette classe est une machine à états complexe. 

Les Registres (L'État) : 

A, B : Accumulateurs 8 bits. 

X, Y : Index 16 bits. 

U, S : Pointeurs de pile 16 bits. 

PC : Compteur Ordinal 16 bits. 

CC : Code de Condition (Flags). 

DP : Direct Page (permet l'adressage court). 

Le Cycle Machine (step) : 

Cette méthode est le métronome. À chaque appel : 

Check Hardware : Vérifie si lineHALT est actif. 

Check Interrupts : Vérifie les lignes NMI, FIRQ, IRQ selon leur priorité et l'état des masques dans CC. 

Fetch : Lit l'opcode pointé par PC et incrémente PC. 

Decode & Execute : Un switch géant route l'opcode vers la méthode Java correspondante (ex: 0x86 -> lda_immediate()). 

L'Unité Arithmétique et Logique (UAL) : 

Des méthodes comme doAddA, doSubB effectuent les calculs et mettent à jour le registre CC. 

Exemple Flag Z (Zéro) : if (result == 0) CC |= 0x04; else CC &= ~0x04; 

Exemple Flag N (Négatif) : if ((result & 0x80) != 0) CC |= 0x08; (On teste le bit 7). 

Gestion des Piles (opPush, opPull) : 

Ces méthodes implémentent la logique unique du 6809 qui permet d'empiler plusieurs registres en une seule instruction via un "Post-Byte" (masque binaire). Le code itère sur les bits du masque pour savoir quels registres transférer. 

5.3. Classe Asm : Le Compilateur 

C'est le traducteur entre l'humain et la machine. 

Structure de Données (MAP) : Un tableau statique Def[] indexé par opcode (0-255) permet une recherche en O(1) pour le désassemblage. 

Algorithme d'Assemblage (2 Passes) : 

Passe 1 : Analyse lexicale. On parcourt le texte pour trouver les étiquettes (LABEL:) et on stocke leur adresse mémoire future dans une HashMap. On calcule la taille de chaque instruction pour avancer le compteur d'adresse virtuelle. 

Passe 2 : Génération de code. On relit le texte. On remplace les mnémoniques (LDA) par leurs opcodes (0x86). On remplace les étiquettes par leurs valeurs (calculées en Passe 1). On gère les modes d'adressage (Immédiat #, Direct, Étendu). 

Calcul des Sauts Relatifs : Pour les instructions BRA (Branch), l'assembleur calcule Offset = Cible - (PC_Actuel + 2). Si l'offset dépasse -128/+127, il faudrait passer à un saut long (LBRA), ce que gère notre logique étendue. 

 

6. ANALYSE DÉTAILLÉE DE L'INTERFACE (com.sim6809.ui) 

6.1. Classe MainApp : L'Orchestrateur 

Elle initialise le Bus, le Cpu, et construit l'interface graphique. Elle gère le cycle de vie de l'application JavaFX (start, stop). 

6.2. Moteur de Rendu et Multithreading 

Pour simuler un processeur cadencé à 1 MHz ou plus, on ne peut pas simplement faire une boucle while(true) car cela gèlerait l'interface graphique (UI Thread). 

Solution : AnimationTimer 

Nous utilisons cette classe spécifique à JavaFX qui appelle une méthode handle() à chaque rafraîchissement d'écran (60 fois par seconde). 

Java 

public void handle(long now) { 
   if (isRunning) { 
       for (int i = 0; i < 10; i++) { // Vitesse ajustable 
           cpu.step(); 
       } 
       refreshUI(); 
   } 
} 
 

Ce mécanisme permet d'exécuter un "paquet" d'instructions CPU (ici 10) entre chaque image affichée à l'écran, offrant une illusion de fluidité et de vitesse tout en gardant l'interface réactive. 

6.3. Ergonomie "Ultimate UI" 

L'interface a été conçue pour maximiser la densité d'information : 

Code Couleur Sémantique : Les noms des registres sont en BLEU (statique), les valeurs en VERT (données dynamiques), les drapeaux actifs en JAUNE (alertes). 

Représentation Binaire : Le registre CC est affiché sous forme de LEDs et de bits individuels (0/1) pour une lecture immédiate. 

Layout Adaptatif : L'utilisation de SplitPane permet à l'utilisateur de redimensionner la zone de code par rapport à la zone de mémoire selon ses besoins. 

 

7. DÉFIS TECHNIQUES ET SOLUTIONS 

7.1. Le problème des entiers signés en Java 

Défi : En Java, le type byte est signé (complément à deux). La valeur hexadécimale 0xFF est interprétée comme l'entier -1. 

Conséquence : Si on ajoute cet octet à une adresse mémoire (PC + offset), Java soustrait 1 au lieu d'ajouter 255. 

Solution : Nous n'utilisons jamais le type byte pour le stockage. Nous utilisons int. Lors de la lecture depuis le Bus, nous appliquons systématiquement & 0xFF pour forcer Java à considérer la valeur comme un entier positif entre 0 et 255. 

7.2. Boucles d'Interruption Infinies 

Défi : Dans une simulation naïve, si l'utilisateur clique sur le bouton "IRQ", la variable lineIRQ passe à true. Le CPU traite l'interruption, revient au programme principal (RTI), et au cycle suivant, voit que lineIRQ est toujours true. Il repart donc en interruption indéfiniment. 

Solution : Nous avons implémenté une logique de "consommation de signal" (Edge-Triggered simulation). Dès que le CPU accepte de traiter l'interruption dans checkInterrupts(), il remet immédiatement la variable lineIRQ à false. Cela simule le comportement d'un contrôleur d'interruption matériel qui acquitte le signal. 

7.3. Corruption de Pile (FIRQ vs IRQ) 

Défi : L'interruption FIRQ (Fast IRQ) ne sauvegarde que PC et CC pour aller vite. L'interruption IRQ sauvegarde tous les registres. Le bit E (Entire) du registre CC permet de savoir quel type de sauvegarde a été fait pour dépiler correctement avec RTI. 

Problème : Si une IRQ (mettant E=1) est interrompue ou suivie par une FIRQ, et que le simulateur ne gère pas proprement le bit E, le RTI du FIRQ risque de lire un E=1 et de dépiler trop de données, corrompant les registres. 

Solution : La méthode serviceInterrupt a été affinée pour forcer le nettoyage du bit E avant de l'empiler lors d'un FIRQ, garantissant l'intégrité de la pile quel que soit l'ordre des événements. 

7.4. Masquage Binaire et Arithmétique Modulaire 

Java ne possédant pas de types non signés natifs (le byte va de -128 à +127), l'émulation fidèle de la mémoire pose un risque de corruption de données par extension de signe. 

Le Risque : Si l'on charge l'octet 0xFF (255) dans un entier, Java l'interprète comme -1 (0xFFFFFFFF). Une addition PC + (-1) ferait reculer le pointeur au lieu de l'avancer de 255 cases. 

La Solution (Bitwise Masking) : L'application systématique du masque & 0xFF lors des lectures (bus.read()) et du masque & 0xFFFF pour les adresses force la JVM à "oublier" le signe négatif en mettant à zéro les bits de poids fort. C'est une implémentation logicielle de l'arithmétique modulaire stricte nécessaire pour simuler un bus physique. 

 

8. GUIDE D'UTILISATION ET VALIDATION 

8.1. ALGORITHME DE COMPILATION (Asm.java) 

Le moteur de compilation n'est pas un interpréteur ligne à ligne, mais un assembleur à deux passes qui génère du code binaire injecté dans le Bus. Il repose sur une Table de Définition (MAP) statique associant chaque opcode (ex: 0x86) à sa mnémonique ("LDA") et son mode d'adressage, garantissant une complexité algorithmique en O(1). 

8.1.2 L'Algorithme "Two-Pass" 

Passe 1 : Table des Symboles (Symbol Table) 

Objectif : Cartographier les adresses pour permettre les sauts vers l'avant (Forward Branching). 

Processus : Lecture séquentielle. Détection des directives ORG pour fixer le compteur ordinal. Repérage des étiquettes (ex: START:) et stockage du couple Nom -> Adresse dans une HashMap. 

Calcul : La méthode calculateSize() estime la taille de chaque instruction pour incrémenter le compteur d'adresse virtuelle. 

Passe 2 : Génération du Code Machine 

Parsing : Nettoyage des lignes (suppression commentaires, espaces) et séparation Mnémonique/Opérandes. 

Aliasing : Correction automatique (ex: ADD devient ADDA). 

Encodage : 

Immédiat (#) : Choix de l'opcode 8 bits (ex: 0x86). 

Mémoire : Choix entre Direct (Page Zéro) ou Étendu (16 bits). 

Relatif (Branch) : Calcul du décalage signé (Cible - PC - 2). 

Piles (PSH/PUL) : Conversion de la liste de registres (ex: "A,B,X") en un masque binaire unique (Post-byte). 

8.2 GUIDE D'UTILISATION (INTERFACE GRAPHIQUE) 

L'interface "Ultimate UI" est divisée en trois zones ergonomiques : 

Zone Gauche (Édition) : Éditeur de code syntaxique et Panneau de contrôle matériel (Boutons d'interruption). 

Zone Centrale (Monitoring) : 

VARS : Affiche les variables en Page Zéro ($00-$30). 

CONTEXTE : Désassemblage temps réel autour du PC et visualisation des deux piles (S et U). 

CONSOLE : Logs d'assemblage et erreurs. 

Zone Droite (Visualisation CPU) : Représentation graphique de l'UAL, registres colorés et LEDs d'état. 

Procédure Standard 

Programmation : Saisir le code dans l'éditeur et cliquer sur [ASSEMBLER]. Vérifier le message "PRÊT" dans la console. 

Exécution : 

[PAS À PAS] : Exécute une instruction (step()). Idéal pour voir l'évolution des Flags. 

[RUN] : Lance l'exécution continue (AnimationTimer à 60Hz). 

[STOP] : Pause l'exécution. 

[RESET] : Remet le CPU à zéro (PC=$FFFE) sans effacer la mémoire. 

[CLR MEM] : Efface la RAM (Variables et Piles). 

Simulation Matérielle : 

HALT (Rouge) : Coupe l'horloge CPU. 

IRQ / FIRQ / NMI : Déclenche les signaux d'interruption. 

Codes Couleurs : 

Bleu : Noms des registres. 

Vert : Valeurs dynamiques. 

Jaune : Flags (CC) actifs. 

8.3. DOCUMENTATION TECHNIQUE INTERNE 

L'architecture respecte le patron MVC. Le package com.sim6809.model contient la logique pure. 

8.3.1. Le Processeur (Cpu6809) 

Registres : Modélisés par des int pour éviter les problèmes de signe du byte Java. 

Cycle (step) : Reproduction du cycle Fetch-Decode-Execute. 

Interruptions : 

Gestion de priorité stricte : NMI > FIRQ > IRQ. 

Mécanisme d'acquittement : Les signaux (lineIRQ) sont remis à false dès leur traitement pour éviter les boucles infinies. 

Sauvegarde : pushAll pour IRQ/NMI (Bit E=1), sauvegarde partielle pour FIRQ (Bit E=0). 

8.3.2. La Mémoire (Bus): 

Stockage : Tableau int[65536] couvrant tout l'espace d'adressage. 

Sécurité : Application systématique de masques (addr & 0xFFFF, data & 0xFF) pour simuler les contraintes physiques 8/16 bits. 

Réactivité : Implémentation du pattern Observer (MemoryListener) pour notifier l'interface graphique uniquement lors des écritures mémoire. 

8.4 TABLEAU DE CORRESPONDANCE : DU MATÉRIEL AU LOGICIEL 

Ce tableau résume les choix d'implémentation pour traduire les composants électroniques en objets Java. 

Composant Matériel (6809) 

Traduction Java (Code) 

Justification Technique 

Registres 8 bits (A, B, DP, CC) 

public int 

Le type int est plus rapide que byte et évite les problèmes de signe (valeurs négatives) grâce au masquage & 0xFF. 

Registres 16 bits (X, Y, S, U, PC) 

public int 

Permet de stocker des adresses jusqu'à 65535 (0xFFFF) sans gérer le signe. 

Mémoire RAM (64 Ko) 

int[65536] 

Un tableau simple offre un accès direct en temps constant O(1) pour la lecture/écriture. 

Bus de Données (8 bits) 

Méthodes read() / write() 

Les méthodes appliquent systématiquement un masque & 0xFF pour tronquer les entiers Java et simuler la largeur du bus. 

Signaux de Contrôle (IRQ, HALT) 

Variables boolean 

true signifie qu'une tension est présente sur la broche (signal actif). 

Horloge (Quartz) 

AnimationTimer (JavaFX) 

La boucle graphique appelle la méthode step() plusieurs fois par image pour simuler la fréquence. 

 

8.5 JEU D'INSTRUCTIONS SUPPORTÉ   

Liste non exhaustive des instructions implémentées dans le moteur Asm.java et Cpu6809.java.  

  

Le simulateur supporte les catégories d'instructions suivantes :  

Chargement & Stockage (Load/Store) : LDA, LDB (8 bits), LDX, LDY, LDU, LDS (16 bits), STA, STB...  

Arithmétique & Logique : ADDA, ADDB (Addition), SUBA, SUBB (Soustraction), CMPA, CMPB (Comparaison). INCA, INCB, DECA, DECB (Incrément/Décrément). ABX (Ajout de B à X, spécifique 6809).  

Branchements (Sauts) : JMP (Saut inconditionnel étendu). BRA (Saut relatif court). BEQ (Branch if Equal / Z=1), BNE (Branch if Not Equal / Z=0).  

Manipulation de Piles : PSHS, PULS (Pile Système). PSHU, PULU (Pile Utilisateur) - Implémentation complète avec masques binaires.  

Contrôle Système : NOP (No Operation), RTS (Retour sous-programme), RTI (Retour Interruption). ANDCC, ORCC (Manipulation directe des drapeaux CC).  

Transfert de Registres : TFR (Transfert universel, ex: TFR A,B ou TFR X,S). 

 

9. CONCLUSION ET PERSPECTIVES 

Le projet Sim6809 Studio démontre la capacité à modéliser une architecture matérielle complexe via une approche logicielle rigoureuse. L'utilisation conjointe de Java pour la logique métier et de JavaFX pour la visualisation a permis de créer un outil pédagogique robuste, interactif et esthétique. 

Nous avons réussi à : 

Créer un cycle CPU fidèle. 

Implémenter un assembleur fonctionnel. 

Visualiser les concepts abstraits (Flags, Piles) de manière graphique. 

Perspectives d'évolution : 

Pour aller plus loin, le simulateur pourrait intégrer : 

Périphériques E/S : Simuler un PIA (Peripheral Interface Adapter) 6821 pour gérer un clavier matriciel. 

Écran Graphique : Mapper une zone mémoire (ex: $0400-$0600) vers un canvas JavaFX pour permettre le développement de petits jeux graphiques. 

Step-Back : Enregistrement des états précédents pour permettre de revenir en arrière dans l'exécution ("Reverse Debugging"). 

Ce projet constitue une base solide pour l'enseignement de l'architecture des ordinateurs et de la programmation système. 

 

Fin du Rapport. 
