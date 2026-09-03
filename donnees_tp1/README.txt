================================================================================
INF8770 - Technologies Multimédias - Automne 2026
Archive de Données pour le Travail Pratique #1 : Compression sans perte : textes
================================================================================

Cette archive contient les fichiers de données textuelles à analyser et compresser.
Les fichiers sont courts, légers et représentatifs afin de permettre des calculs
et exécutions rapides sur vos machines.

Conformément à l'énoncé du TP1 (page 2) :
"Les données contiennent des fichiers textes de différentes natures (prose littéraire,
données structurées de type CSV, code source). Choisissez trois fichiers (un de chaque nature)
sur lesquels baser votre expérimentation."

Vous devez donc choisir EXACTEMENT UN fichier dans chacune des 3 catégories ci-dessous :

--------------------------------------------------------------------------------
DÉTAIL DES FICHIERS DE DONNÉES DISPONIBLES :
--------------------------------------------------------------------------------

1. CATÉGORIE PROSE LITTÉRAIRE (Langue naturelle continue, sans répétition artificielle) :
   - litteraire_fr.txt :
     * Taille : 5 092 octets (~5.0 Ko)
     * Format : Fichier texte brut (.txt), encodage UTF-8
     * Contenu : Extrait continu du roman Notre-Dame de Paris (Victor Hugo)
     * Caractéristiques : Texte français riche en accents (é, è, ê, à, ç), redondance
       naturelle de la langue.
   
   - litteraire_en.txt :
     * Taille : 4 142 octets (~4.0 Ko)
     * Format : Fichier texte brut (.txt), encodage UTF-8
     * Contenu : Extrait continu des aventures de Sherlock Holmes (Arthur Conan Doyle)
     * Caractéristiques : Prose anglaise victorienne fluide, alphabet sans accents.

2. CATÉGORIE DONNÉES STRUCTURÉES (Fichiers tabulaires délimités) :
   - structure_meteo.csv :
     * Taille : 26 515 octets (~25.9 Ko)
     * Format : Fichier CSV (.csv) délimité par des virgules avec ligne d'en-tête, encodage UTF-8
     * Contenu : Relevés météorologiques horaires à Montréal (température, humidité, pression, vent)
     * Caractéristiques : Séries temporelles régulières, délimiteurs récurrents.
   
   - structure_transactions.csv :
     * Taille : 27 421 octets (~26.8 Ko)
     * Format : Fichier CSV (.csv) avec ligne d'en-tête, encodage UTF-8
     * Contenu : Historique de transactions d'achats (identifiants, catégories, montants)
     * Caractéristiques : Délimiteurs périodiques et répétitions de catégories.

3. CATÉGORIE CODE SOURCE (Programmes réels sans aucun algorithme de compression) :
   - code_source_python.py :
     * Taille : 3 844 octets (~3.8 Ko)
     * Format : Script Python (.py), encodage UTF-8
     * Contenu : Implémentations d'arbres binaires, parcours de graphes et algorithmes de tri
     * Caractéristiques : Forte redondance d'indentation (blocs de 4 espaces répétés)
       et mots-clés syntaxiques fréquents (def, return, class, self).
   
   - code_source_c.c :
     * Taille : 2 200 octets (~2.2 Ko)
     * Format : Fichier source C (.c), norme C99, encodage UTF-8
     * Contenu : Fonctions de calcul matriciel et opérations sur vecteurs
     * Caractéristiques : Répétitions d'accolades, de points-virgules, de types (double, size_t)
       et d'opérateurs mathématiques.

--------------------------------------------------------------------------------
RECOMMANDATIONS POUR LES ÉTUDIANTS :
--------------------------------------------------------------------------------
- Tous les fichiers (qu'ils soient en .txt, .csv, .py ou .c) doivent être traités
  comme des flux d'octets bruts (mode binaire : open(f, 'rb')) lors de vos tests
  de compression et décompression.
- Vérifiez toujours la réversibilité stricte : donnees_decompressees == donnees_originales.

Bon succès dans votre TP1 !
L'équipe enseignante d'INF8770
