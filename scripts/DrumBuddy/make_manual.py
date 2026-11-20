# Generates the Drum Buddy user manual, French and English
# (scripts/DrumBuddy/DrumBuddy_manuel_FR.pdf and DrumBuddy_manual_EN.pdf).
# Usage: python3 make_manual.py [output folder]
import math
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Wedge, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, ListFlowable, ListItem, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents

VERSION = "1.2"
NAME = "ReNo Mellow - Drum Buddy"
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/DrumBuddy/"
URL_FR = BASE + "DrumBuddy_manuel_FR.pdf"
URL_EN = BASE + "DrumBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Drum_Buddy.ReaperPkg"
URL_REPO = "https://github.com/renothestraws/reno-mellow-script"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT_DIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", FONT_DIR + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

ACCENT = colors.HexColor("#5A4FCF")
DARK = colors.HexColor("#2B2D31")
GREY = colors.HexColor("#6B6F76")
LIGHT = colors.HexColor("#EDF2F8")

S = {
    "title": ParagraphStyle("title", fontName="DVB", fontSize=26, leading=32, alignment=TA_CENTER, textColor=DARK),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=13, leading=18, alignment=TA_CENTER, textColor=GREY),
    "center": ParagraphStyle("center", fontName="DV", fontSize=10, leading=14, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=15, leading=19, spaceBefore=10, spaceAfter=6, textColor=ACCENT,
                         keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, spaceBefore=7, spaceAfter=3, textColor=DARK,
                         keepWithNext=1),
    "p": ParagraphStyle("p", fontName="DV", fontSize=10, leading=14, spaceAfter=5),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=9, leading=12),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=9, leading=12),
    "cap": ParagraphStyle("cap", fontName="DVI", fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=GREY,
                          spaceAfter=6),
    "toc1": ParagraphStyle("toc1", fontName="DV", fontSize=10.5, leading=16, leftIndent=8),
}
# headings already kept together with what follows: no keepWithNext (it chained whole sections together)
S["h1k"] = ParagraphStyle("h1", parent=S["h1"], keepWithNext=0)
S["h2k"] = ParagraphStyle("h2k", parent=S["h2"], keepWithNext=0)


# ------------------------------------------------------------------ texts
T = {}
T["fr"] = {
    "file": "DrumBuddy_manuel_FR.pdf",
    "sub": "Des fills de batterie dans l'éditeur MIDI, pensés comme un batteur",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "DrumBuddy_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié",
    "head2": ("Élément", "Effet"),
    "head_g": ("Geste", "Effet"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "Drum Buddy écrit des <b>fills de batterie</b> dans l'éditeur MIDI. Tout part d'un <b>batteur</b> : "
              "chaque projet a le sien, avec sa drum map (les notes de son instrument), sa façon de jouer "
              "(vélocités, flas, drags, humanize, Rush / Laid back) et ses <b>16 chops</b> préférés, rangés sur des pads."),
        ("p", "Un chop ne contient que des <b>groupes de coups</b> et leur <b>sticking</b> (main droite, main gauche, "
              "kick, fla, drag, accents et ghost notes) avec l'élément de batterie de chaque coup. Il ne contient pas "
              "de rythme : à l'insertion, <b>un coup dure un pas de la grille</b> de l'éditeur MIDI. Le même chop "
              "joue donc en doubles croches avec une grille 1/16, en triples avec 1/32, en triolets avec 1/16T."),
        ("p", "Un clic sur un pad pose le chop au <b>curseur d'édition</b> et place le curseur à la fin. "
              "<b>Again</b>, <b>Vary</b> et <b>Random</b> donnent des variantes en un clic, et un petit <b>Display</b> "
              "flottant garde les chops à portée de main."),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « Drum Buddy », clic droit &gt; Install, "
                "puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Les deux actions "
              "(fenêtre et Display) sont ajoutées à la liste d'actions. Pas de mise à jour automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Copier le dossier <b>DrumBuddy</b> dans le dossier Scripts de REAPER, puis charger "
              "<b>ReNo Mellow - Drum Buddy.lua</b> et <b>ReNo Mellow - Drum Buddy - Display.lua</b> dans la liste "
              "d'actions (Actions &gt; Show action list &gt; New action &gt; Load ReaScript). Les deux fichiers "
              "doivent rester dans le même dossier."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Ouvrir un item MIDI de batterie dans l'éditeur MIDI et placer le curseur d'édition où le fill commence.",
                "Régler la grille de l'éditeur MIDI, par exemple <b>1/16</b>.",
                "Lancer l'action <b>ReNo Mellow - Drum Buddy</b> (relancer l'action = fermer la fenêtre). Trois "
                "batteurs sont fournis, avec une drum map General MIDI et 16 chops chacun : <b>Charlie</b> (rock-pop), "
                "<b>Mike</b> (metal) et <b>Buddie</b> (jazz et gospel). Un nouveau projet commence avec Charlie.",
                "Onglet <b>Kit</b> : vérifier que les notes correspondent à l'instrument (bouton <b>Detect from note "
                "names</b> ou <b>Learn</b>, voir section 7).",
                "Onglet <b>Drummer</b> : cliquer un pad. Le chop est inséré au curseur, qui passe à la fin du fill."]),
        ("h1", "4. Le batteur du projet"),
        ("p", "Le batteur choisi est <b>enregistré dans le projet</b> : à l'ouverture de la session, ou en passant "
              "d'un onglet de projet à l'autre, Drum Buddy recharge son batteur. Un nouveau projet reprend le dernier "
              "batteur utilisé. Le texte sous la liste indique « Drummer of this project » ou propose "
              "<b>Use in this project</b>."),
        ("p", "Chaque batteur est un petit fichier texte dans le dossier ressources de REAPER : "
              "<b>Data/ReNo_DrumBuddy/drummers</b>. On peut le sauvegarder, le copier sur une autre machine ou le partager."),
        ("table2", [
            ("Charlie (rock-pop)", "Jeu droit, fills simples et passe-partout : caisse claire, toms, 3+3+2, flam fill, et "
                                   "des chops tout au charley (Full HH accents, Full HH kick, HH open lift). Crash à la fin."),
            ("Mike (metal)", "Vélocités hautes, humanize serré : SSKK x4 (SSKKSSKKSSKKSSKK), SSSSKK (SSSSKKSSSSKKSSSS), "
                             "blast, double pédale (K / K2), RLK et doubles sur 4 toms, gallop. China à la fin."),
            ("Buddie (jazz-gospel)", "Laid back, ghost notes douces : swing triplets, comping, ride and snare, gospel RLK "
                                     "et RLLK, ratamacue, pataflafla, drags. Grille en triolets (1/8T) pour le swing."),
        ]),
        ("table_g", [
            ("Liste du batteur", "Choisir le batteur de ce projet."),
            ("New", "Nouveau batteur : drum map General MIDI, réglages par défaut, pads vides."),
            ("Duplicate", "Copie du batteur actuel (drum map, réglages et chops) sous un autre nom."),
            ("Delete", "Supprime le batteur et ses 16 chops, après confirmation."),
            ("Export", "Enregistre le batteur dans un fichier (nom, drum map, profil, 16 chops), pour le sauvegarder "
                       "ou le partager. Sans l'extension js_ReaScriptAPI, le fichier va dans Data/ReNo_DrumBuddy/exports."),
            ("Import", "Charge un batteur depuis un fichier et l'utilise dans ce projet (un numéro est ajouté si le "
                       "nom existe déjà)."),
        ]),
        ("h1", "5. Onglet Drummer : les 16 pads"),
        ("table_g", [
            ("Clic sur un pad", "Insère le chop au curseur d'édition, sur le canal actif de l'éditeur MIDI, puis place "
                                "le curseur à la fin. L'item est allongé si besoin. Une seule annulation."),
            ("Clic sur un pad vide", "Enregistre le fill de l'onglet Editor dans ce pad, avec un nom."),
            ("Clic droit sur un pad", "Edit in the Editor, Replace with the fill of the Editor, Rename, Clear the pad."),
            ("Survol d'un pad", "Sticking du chop, nombre de coups et durée avec la grille actuelle."),
            ("Again", "Réinsère le dernier fill. L'humanize est tiré à nouveau : chaque fois une variante."),
            ("Vary", "Réinsère le dernier fill avec une nouvelle orchestration (un élément par groupe), même sticking."),
            ("Random", "Insère un fill nouveau dans le style du batteur (rudiment ou découpage au hasard, densité du "
                       "profil). <b>Random length</b> : 1 temps, 2 temps, 1 mesure ou 2 mesures."),
        ]),
        ("draw", "pads"),
        ("p", "Exemple de durée : un chop de 8 coups dure 2 temps avec une grille 1/16, 1 temps avec 1/32, et "
              "8 croches de triolet avec 1/8T."),
        ("h1", "6. Onglet Editor : construire un chop"),
        ("p", "Un fill est une suite de <b>groupes</b>, comme un batteur pense son sticking (par 2, 3, 4, 6...). "
              "On part d'un <b>preset</b> : rudiments (Rolls, Diddles, Flams, Drags) ou découpages (Groupings : "
              "4+4+4+4, 3+3+2, 3+3+3+3+4, 5+5+6, 6+6+4, 2+2+3, et <b>Custom</b> où l'on tape par exemple 3+3+2)."),
        ("draw", "grid"),
        ("p", "Chaque groupe est un bloc : <b>en-tête</b> (taille du groupe), <b>sticking</b>, <b>orchestration</b> et "
              "<b>pastille</b> de l'élément du groupe. Les temps sont repérés par une case plus claire."),
        ("table_g", [
            ("Clic sur l'en-tête", "Sticking suivant de la bibliothèque pour un groupe de cette taille."),
            ("Clic droit sur l'en-tête", "Liste des stickings, ajouter / retirer un coup, couper en deux, fusionner "
                                         "avec le suivant, copier sur le suivant, inverser R / L, supprimer."),
            ("Clic sur un coup", "Mode suivant : normal &gt; accent &gt; ghost &gt; kick (K) &gt; fla (Fl) &gt; normal. "
                                 "Accent = trait au-dessus, ghost = trait en dessous. K et Fl n'ont ni accent ni ghost."),
            ("Clic droit sur un coup", "Main R ou L, et tous les modes, y compris le drag (Dr)."),
            ("Molette sur l'orchestration", "Élément suivant ou précédent pour ce coup, ou « - » = coup silencieux. "
                                            "Un coup K ne prend que Kick ou Kick 2."),
            ("Clic droit sur l'orchestration", "Menu des éléments par famille (Snare, Toms, Hi-hat, Ride, Crash, Perc)."),
            ("Pastille du groupe", "Clic ou molette : élément de tout le groupe ; clic droit : menu."),
        ]),
        ("h2", "Outils Sticking"),
        ("table2", [
            ("Random", "Un sticking au hasard pour chaque groupe."),
            ("Accent first", "Accent sur le premier coup de chaque groupe."),
            ("Accent odd / even", "Accents sur les coups 1, 3, 5... ou 2, 4, 6... du fill."),
            ("Accent beat", "Accents seulement sur les temps (noires)."),
            ("Ghost odd / even / offbeat", "Ghost notes sur les coups impairs, pairs, ou hors des temps. Les accents restent."),
        ]),
        ("h2", "Outils Orchestration"),
        ("table2", [
            ("All snare / All HH", "Tous les coups R et L sur la caisse claire, ou sur le charley fermé (ouvert sur les accents)."),
            ("Toms down / Toms up", "Un tom par groupe, du plus aigu au plus grave ou l'inverse."),
            ("R ride / L HH", "Main droite sur la ride, main gauche sur le charley fermé."),
            ("MP", "Snare, snare, kick, kick en boucle sur tout le fill."),
            ("Shuffle", "HH, SN, HH, HH, SN, HH en boucle sur tout le fill."),
        ]),
        ("h2", "Fill"),
        ("table2", [
            ("Repeat", "Joue tout le fill deux fois."),
            ("Reset", "Revient au preset tel qu'il est écrit."),
            ("Insert at edit cursor", "Insère le fill de l'Editor au curseur."),
            ("Save to a pad...", "Nom du chop, puis choix d'un des 16 pads (un pad occupé est remplacé)."),
        ]),
        ("h1", "7. Onglet Kit : la drum map"),
        ("p", "La drum map appartient au batteur : 29 éléments (caisse claire et ses articulations, 6 toms, charley "
              "fermé, mi-ouvert, ouvert, pied, ride, crashes, china, splash, stack, percussions, 2 grosses caisses). "
              "Une note -1 signifie « non mappé » : l'élément est ignoré à l'insertion et apparaît en orange."),
        ("table2", [
            ("Detect from note names", "Lit les noms de notes chargés dans l'éditeur MIDI pour la piste éditée "
                                       "(File &gt; Note names) et reconnaît les éléments par mots-clés. Les éléments "
                                       "sans nom reconnu gardent leur note."),
            ("Load GM", "Charge la drum map General MIDI."),
            ("Learn", "Cliquer Learn, puis : la touche de l'élément sur le clavier du piano roll, une note de cet "
                      "élément dans l'éditeur, ou le pad d'un contrôleur MIDI."),
            ("Note", "Saisie directe du numéro de note (-1 à 127)."),
        ]),
        ("h1", "8. Onglet Profile : la façon de jouer"),
        ("table2", [
            ("Name", "Nom du batteur."),
            ("Velocity", "Vélocités Accent, Normal et Ghost (les notes de grâce des flas et drags utilisent Ghost)."),
            ("Grace notes", "Avance de la note de grâce du fla (ms) et espacement des deux notes du drag (ms)."),
            ("Feel", "Humanize de la vélocité (%) et du timing (ms), et Rush (en avance) / Laid back (en retard)."),
            ("Style", "Density : peu de ghost notes et de kicks (fills propres) ou beaucoup (fills chargés), pour "
                      "Random et Vary. Option cymbales dans Random et Vary."),
            ("End of the fill", "Kick + un élément (crash, china, splash, ride...) juste après le fill, ou rien."),
            ("Options", "Replace the notes under the fill (pour tous les batteurs) ; Open the Display when REAPER "
                        "starts ; taille du texte et opacité du Display."),
        ]),
        ("h1", "9. Le Display"),
        ("p", "Petite barre sans titre (action « ReNo Mellow - Drum Buddy - Display »), cachée quand aucun éditeur MIDI "
              "n'est ouvert. Elle affiche le batteur du projet et un de ses chops."),
        ("draw", "display"),
        ("table_g", [
            ("Clic sur le chop", "Insère le chop au curseur d'édition."),
            ("Molette ou flèches", "Chop précédent ou suivant (pads remplis seulement)."),
            ("Clic droit sur le chop", "Les 16 pads : un clic insère."),
            ("Again / Vary / Random", "Comme dans l'onglet Drummer. Clic droit sur Random : longueur."),
            ("Open", "Ouvre ou ferme Drum Buddy."),
            ("Clic droit sur Open", "Taille du texte (10 à 28), opacité du fond (15 à 100 %), Open with REAPER "
                                    "(ouverture au démarrage de REAPER), fermer le Display."),
            ("Relancer l'action Display", "Fermer le Display."),
        ]),
        ("h1", "10. Les actions"),
        ("table2", [
            ("ReNo Mellow - Drum Buddy", "Fenêtre principale (relancer = fermer). Icône de barre d'outils allumée "
                                         "tant qu'elle est ouverte."),
            ("ReNo Mellow - Drum Buddy - Display", "Ouvre ou ferme le Display."),
        ]),
        ("p", "Les deux actions sont dans la section Main et s'associent au raccourci ou au bouton de barre d'outils de "
              "votre choix."),
        ("h1", "11. Questions fréquentes"),
        ("p", "Les cas les plus courants."),
        ("qa", [
            ("Rien ne se passe quand je clique un pad.",
             "Un item MIDI doit être ouvert dans l'éditeur MIDI : le message apparaît en bas de la fenêtre."),
            ("Certaines notes manquent dans le fill.",
             "Ces éléments ne sont pas dans la drum map (note -1) : le message en bas de la fenêtre les cite. "
             "Les régler dans l'onglet Kit."),
            ("Le fill est trop long ou trop court.",
             "La durée suit la grille de l'éditeur MIDI : changer la grille (1/16, 1/32, 1/16T...) change la vitesse du fill."),
            ("Learn ne réagit pas.",
             "Cliquer une autre touche ou une autre note que celle déjà active, ou vérifier que le contrôleur MIDI est "
             "activé en entrée dans les préférences de REAPER."),
            ("J'ai changé de projet et le batteur a changé.",
             "C'est voulu : chaque projet garde son batteur. Choisir un autre batteur l'enregistre dans le projet en cours."),
        ]),
    ],
}

T["en"] = {
    "file": "DrumBuddy_manual_EN.pdf",
    "sub": "Drum fills in the MIDI editor, the way a drummer thinks",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "DrumBuddy_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing",
    "head2": ("Item", "Effect"),
    "head_g": ("Gesture", "Effect"),
    "body": [
        ("h1", "1. What it does"),
        ("p", "Drum Buddy writes <b>drum fills</b> in the MIDI editor. Everything starts from a <b>drummer</b>: each "
              "project has its own, with his drum map (the notes of his instrument), his way of playing (velocities, "
              "flams, drags, humanize, Rush / Laid back) and his <b>16 favorite chops</b>, stored on pads."),
        ("p", "A chop holds only <b>groups of strokes</b> and their <b>sticking</b> (right hand, left hand, kick, "
              "flam, drag, accents and ghost notes) with the drum piece of each stroke. It holds no rhythm: when it is "
              "inserted, <b>one stroke lasts one grid step</b> of the MIDI editor. The same chop plays 16th notes with a "
              "1/16 grid, 32nd notes with 1/32, triplets with 1/16T."),
        ("p", "Clicking a pad puts the chop at the <b>edit cursor</b> and moves the cursor to its end. <b>Again</b>, "
              "<b>Vary</b> and <b>Random</b> give variations in one click, and a small floating <b>Display</b> keeps the "
              "chops at hand."),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « Drum Buddy », right-click &gt; Install, then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drop it into REAPER. Both actions (window "
              "and Display) are added to the action list. No automatic updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Copy the <b>DrumBuddy</b> folder into the REAPER Scripts folder, then load "
              "<b>ReNo Mellow - Drum Buddy.lua</b> and <b>ReNo Mellow - Drum Buddy - Display.lua</b> in the action list "
              "(Actions &gt; Show action list &gt; New action &gt; Load ReaScript). Both files must stay in the same folder."),
        ("h1", "3. First steps"),
        ("ol", ["Open a drum MIDI item in the MIDI editor and put the edit cursor where the fill starts.",
                "Set the MIDI editor grid, for example <b>1/16</b>.",
                "Run the action <b>ReNo Mellow - Drum Buddy</b> (run it again = close the window). Three drummers "
                "come with it, each with a General MIDI drum map and 16 chops: <b>Charlie</b> (rock-pop), <b>Mike</b> "
                "(metal) and <b>Buddie</b> (jazz and gospel). A new project starts with Charlie.",
                "<b>Kit</b> tab: check that the notes match the instrument (<b>Detect from note names</b> or "
                "<b>Learn</b>, see section 7).",
                "<b>Drummer</b> tab: click a pad. The chop is inserted at the cursor, which moves to the end of the fill."]),
        ("h1", "4. The drummer of the project"),
        ("p", "The chosen drummer is <b>saved in the project</b>: when the session is opened, or when switching project "
              "tabs, Drum Buddy loads its drummer. A new project takes the last drummer used. The text under the list "
              "shows « Drummer of this project » or offers <b>Use in this project</b>."),
        ("p", "Each drummer is a small text file in the REAPER resource folder: <b>Data/ReNo_DrumBuddy/drummers</b>. "
              "It can be backed up, copied to another computer or shared."),
        ("table2", [
            ("Charlie (rock-pop)", "Straight playing, simple all-purpose fills: snare, toms, 3+3+2, flam fill, and "
                                   "all-hi-hat chops (Full HH accents, Full HH kick, HH open lift). Crash at the end."),
            ("Mike (metal)", "High velocities, tight humanize: SSKK x4 (SSKKSSKKSSKKSSKK), SSSSKK (SSSSKKSSSSKKSSSS), "
                             "blast, double kick (K / K2), RLK and doubles on 4 toms, gallop. China at the end."),
            ("Buddie (jazz-gospel)", "Laid back, soft ghost notes: swing triplets, comping, ride and snare, gospel RLK and "
                                     "RLLK, ratamacue, pataflafla, drags. Triplet grid (1/8T) for the swing."),
        ]),
        ("table_g", [
            ("Drummer list", "Choose the drummer of this project."),
            ("New", "New drummer: General MIDI drum map, default settings, empty pads."),
            ("Duplicate", "Copy of the current drummer (drum map, settings and chops) under another name."),
            ("Delete", "Deletes the drummer and his 16 chops, after confirmation."),
            ("Export", "Saves the drummer in a file (name, drum map, profile, 16 chops), to back it up or share it. "
                       "Without the js_ReaScriptAPI extension, the file goes to Data/ReNo_DrumBuddy/exports."),
            ("Import", "Loads a drummer from a file and uses it in this project (a number is added if the name is "
                       "already taken)."),
        ]),
        ("h1", "5. Drummer tab: the 16 pads"),
        ("table_g", [
            ("Click on a pad", "Inserts the chop at the edit cursor, on the active channel of the MIDI editor, then "
                               "moves the cursor to the end. The item is extended if needed. One undo step."),
            ("Click on an empty pad", "Saves the fill of the Editor tab in this pad, with a name."),
            ("Right-click on a pad", "Edit in the Editor, Replace with the fill of the Editor, Rename, Clear the pad."),
            ("Hover a pad", "Sticking of the chop, number of strokes and length with the current grid."),
            ("Again", "Inserts the last fill again. Humanize is drawn again: a slightly different take each time."),
            ("Vary", "Inserts the last fill with a new orchestration (one piece per group), same sticking."),
            ("Random", "Inserts a new fill in the style of the drummer (random rudiment or grouping, density of the "
                       "profile). <b>Random length</b>: 1 beat, 2 beats, 1 bar or 2 bars."),
        ]),
        ("draw", "pads"),
        ("p", "Length example: an 8-stroke chop lasts 2 beats with a 1/16 grid, 1 beat with 1/32, and 8 triplet "
              "eighths with 1/8T."),
        ("h1", "6. Editor tab: building a chop"),
        ("p", "A fill is a series of <b>groups</b>, the way a drummer thinks his sticking (in 2, 3, 4, 6...). Start "
              "from a <b>preset</b>: rudiments (Rolls, Diddles, Flams, Drags) or groupings (4+4+4+4, 3+3+2, 3+3+3+3+4, "
              "5+5+6, 6+6+4, 2+2+3, and <b>Custom</b> where you type for example 3+3+2)."),
        ("draw", "grid"),
        ("p", "Each group is a block: <b>header</b> (size of the group), <b>sticking</b>, <b>orchestration</b> and the "
              "<b>chip</b> of the group piece. Beats are marked by a lighter cell."),
        ("table_g", [
            ("Click on the header", "Next sticking of the library for a group of this size."),
            ("Right-click on the header", "List of stickings, add / remove a stroke, split in two, merge with next, "
                                          "copy to next, invert R / L, delete."),
            ("Click on a stroke", "Next mode: normal &gt; accent &gt; ghost &gt; kick (K) &gt; flam (Fl) &gt; normal. "
                                  "Accent = line above, ghost = line below. K and Fl have no accent or ghost."),
            ("Right-click on a stroke", "Hand R or L, and every mode, drag (Dr) included."),
            ("Wheel on the orchestration", "Next or previous piece for this stroke, or « - » = silent stroke. A K stroke "
                                           "takes Kick or Kick 2 only."),
            ("Right-click on the orchestration", "Menu of the pieces by family (Snare, Toms, Hi-hat, Ride, Crash, Perc)."),
            ("Group chip", "Click or wheel: piece of the whole group; right-click: menu."),
        ]),
        ("h2", "Sticking tools"),
        ("table2", [
            ("Random", "A random sticking for each group."),
            ("Accent first", "Accent on the first stroke of each group."),
            ("Accent odd / even", "Accents on strokes 1, 3, 5... or 2, 4, 6... of the fill."),
            ("Accent beat", "Accents only on the beats (quarter notes)."),
            ("Ghost odd / even / offbeat", "Ghost notes on odd strokes, even strokes, or off the beats. Accents stay."),
        ]),
        ("h2", "Orchestration tools"),
        ("table2", [
            ("All snare / All HH", "Every R and L stroke on the snare, or on the closed hi-hat (open on accents)."),
            ("Toms down / Toms up", "One tom per group, high to low or low to high."),
            ("R ride / L HH", "Right hand on the ride, left hand on the closed hi-hat."),
            ("MP", "Snare, snare, kick, kick in a loop over the whole fill."),
            ("Shuffle", "HH, SN, HH, HH, SN, HH in a loop over the whole fill."),
        ]),
        ("h2", "Fill"),
        ("table2", [
            ("Repeat", "Plays the whole fill twice."),
            ("Reset", "Back to the preset as written."),
            ("Insert at edit cursor", "Inserts the fill of the Editor at the cursor."),
            ("Save to a pad...", "Name of the chop, then one of the 16 pads (a used pad is replaced)."),
        ]),
        ("h1", "7. Kit tab: the drum map"),
        ("p", "The drum map belongs to the drummer: 29 pieces (snare and its articulations, 6 toms, closed, half-open, "
              "open and pedal hi-hat, ride, crashes, china, splash, stack, percussion, 2 kicks). Note -1 means "
              "« not mapped »: the piece is skipped when inserting and shown in orange."),
        ("table2", [
            ("Detect from note names", "Reads the note names loaded in the MIDI editor for the edited track (File &gt; "
                                       "Note names) and recognizes the pieces by keywords. Pieces with no matching name "
                                       "keep their note."),
            ("Load GM", "Loads the General MIDI drum map."),
            ("Learn", "Click Learn, then: the key of the piece on the piano roll keyboard, a note of that piece in the "
                      "editor, or the pad of a MIDI controller."),
            ("Note", "Type the note number directly (-1 to 127)."),
        ]),
        ("h1", "8. Profile tab: how the drummer plays"),
        ("table2", [
            ("Name", "Name of the drummer."),
            ("Velocity", "Accent, Normal and Ghost velocities (grace notes of flams and drags use Ghost)."),
            ("Grace notes", "Lead of the flam grace note (ms) and spacing of the two drag notes (ms)."),
            ("Feel", "Humanize of velocity (%) and timing (ms), and Rush (ahead) / Laid back (behind)."),
            ("Style", "Density: few ghost notes and kicks (clean fills) or many (busy fills), for Random and Vary. "
                      "Cymbals option in Random and Vary."),
            ("End of the fill", "Kick + a piece (crash, china, splash, ride...) right after the fill, or nothing."),
            ("Options", "Replace the notes under the fill (all drummers); Open the Display when REAPER starts; "
                        "text size and opacity of the Display."),
        ]),
        ("h1", "9. The Display"),
        ("p", "Small bar without a title (action « ReNo Mellow - Drum Buddy - Display »), hidden when no MIDI editor is "
              "open. It shows the drummer of the project and one of his chops."),
        ("draw", "display"),
        ("table_g", [
            ("Click on the chop", "Inserts the chop at the edit cursor."),
            ("Wheel or arrows", "Previous or next chop (filled pads only)."),
            ("Right-click on the chop", "The 16 pads: a click inserts."),
            ("Again / Vary / Random", "As in the Drummer tab. Right-click on Random: length."),
            ("Open", "Opens or closes Drum Buddy."),
            ("Right-click on Open", "Text size (10 to 28), background opacity (15 to 100 %), Open with REAPER "
                                    "(opens when REAPER starts), close the Display."),
            ("Run the Display action again", "Close the Display."),
        ]),
        ("h1", "10. Actions"),
        ("table2", [
            ("ReNo Mellow - Drum Buddy", "Main window (run again = close). Toolbar icon lit while it is open."),
            ("ReNo Mellow - Drum Buddy - Display", "Opens or closes the Display."),
        ]),
        ("p", "Both actions are in the Main section; assign them to any shortcut or toolbar button you like."),
        ("h1", "11. FAQ"),
        ("p", "The most common cases."),
        ("qa", [
            ("Nothing happens when I click a pad.",
             "A MIDI item must be open in the MIDI editor: the message is shown at the bottom of the window."),
            ("Some notes are missing in the fill.",
             "Those pieces are not in the drum map (note -1): the message at the bottom of the window lists them. Set "
             "them in the Kit tab."),
            ("The fill is too long or too short.",
             "The length follows the MIDI editor grid: changing the grid (1/16, 1/32, 1/16T...) changes the speed of the fill."),
            ("Learn does not react.",
             "Click another key or another note than the one already active, or check that the MIDI controller is "
             "enabled for input in the REAPER preferences."),
            ("I changed project and the drummer changed.",
             "That is intended: each project keeps its drummer. Choosing another drummer saves it in the current project."),
        ]),
    ],
}

# ------------------------------------------------------------------ drawings (simplified, not screenshots)
BTN = colors.HexColor("#3A3D42")
ON = colors.HexColor("#5A4FCF")
PAD = colors.HexColor("#3B3560")
PAD_E = colors.HexColor("#26262C")
TXT = colors.HexColor("#E8E8E8")
MUT = colors.HexColor("#9A9A9A")
CELL = colors.HexColor("#34343C")
CELL_B = colors.HexColor("#4C4C62")
ORCH = colors.HexColor("#3B3560")
KICK = colors.HexColor("#2A2A2E")
HEAD = colors.HexColor("#2C2C34")
DEMO = ["Snare 8", "Snare to toms", "Full HH accents", "Full HH kick", "Fours down", "Triplets around",
        "Flam fill", "RLRLKK", "Snare build", "Paradiddle toms", "Doubles", "Ride bell lift",
        "3+3+2 toms", "HH open lift", "RLKK", None]


def buttons(d, x, y, labels, on=(), h=5 * mm, fs=6.5):
    for lab in labels:
        w = max(8 * mm, len(lab) * fs * 0.62 + 4 * mm)
        d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=ON if lab in on else BTN, strokeColor=None))
        d.add(String(x + w / 2, y + h / 2 - fs * 0.35, lab, fontName="DV", fontSize=fs, fillColor=TXT,
                     textAnchor="middle"))
        x += w + 1.2 * mm
    return x


def d_pads(height=None):
    W, H = 174 * mm, 74 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    d.add(String(8, H - 6 * mm, "Charlie", fontName="DVB", fontSize=9, fillColor=colors.white))
    buttons(d, 40 * mm, H - 8 * mm, ["New", "Duplicate", "Delete", "Export", "Import"])
    pw, ph, gap = 38 * mm, 10 * mm, 2.5 * mm
    x0, y0 = (W - (4 * pw + 3 * gap)) / 2, H - 14 * mm - ph
    for i in range(16):
        r, c = divmod(i, 4)
        x, y = x0 + c * (pw + gap), y0 - r * (ph + gap)
        name = DEMO[i]
        d.add(Rect(x, y, pw, ph, rx=3, ry=3, fillColor=PAD if name else PAD_E, strokeColor=None))
        d.add(String(x + pw / 2, y + ph - 3.8 * mm, str(i + 1), fontName="DV", fontSize=7, fillColor=MUT, textAnchor="middle"))
        d.add(String(x + pw / 2, y + 1.8 * mm, name or "+", fontName="DVB", fontSize=7, fillColor=TXT, textAnchor="middle"))
    bw = (4 * pw + 3 * gap - 2 * gap) / 3
    yb = 4 * mm
    for k, lab in enumerate(["Again", "Vary", "Random"]):
        x = x0 + k * (bw + gap)
        d.add(Rect(x, yb, bw, 7 * mm, rx=3, ry=3, fillColor=BTN, strokeColor=None))
        d.add(String(x + bw / 2, yb + 2.4 * mm, lab, fontName="DVB", fontSize=8, fillColor=TXT, textAnchor="middle"))
    return d


def d_grid():
    # 3+3+2 : R L L | R L L | R L, accents on the first stroke, toms
    W, H = 174 * mm, 40 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    groups = [(["R", "L", "L"], ["S", "S", "S"], "S"), (["R", "L", "K"], ["T1", "T1", "K"], "T1"), (["Fl", "L"], ["T3", "T3"], "T3")]
    cw, gap, ggap = 11 * mm, 0.8 * mm, 5 * mm
    total = sum(len(g[0]) for g in groups) * (cw + gap) + (len(groups) - 1) * ggap
    x = (W - total) / 2
    idx = 0
    for sticks, orch, gp in groups:
        n = len(sticks)
        gw = n * (cw + gap) - gap
        d.add(Rect(x, H - 9 * mm, gw, 5 * mm, rx=2, ry=2, fillColor=HEAD, strokeColor=None))
        d.add(String(x + gw / 2, H - 7.6 * mm, str(n), fontName="DV", fontSize=7, fillColor=MUT, textAnchor="middle"))
        for k in range(n):
            cx = x + k * (cw + gap)
            beat = idx % 4 == 0
            ys = H - 19 * mm
            d.add(Rect(cx, ys, cw, 6.5 * mm, rx=2, ry=2, fillColor=CELL_B if beat else CELL, strokeColor=None))
            d.add(String(cx + cw / 2, ys + 2.1 * mm, sticks[k], fontName="DVB", fontSize=8, fillColor=TXT, textAnchor="middle"))
            if k == 0 and sticks[k] not in ("K", "Fl"):
                d.add(Rect(cx + 1.5 * mm, ys + 7.3 * mm, cw - 3 * mm, 0.6 * mm, fillColor=colors.white, strokeColor=None))
            if sticks[k] == "L" and k == 2:
                d.add(Rect(cx + 1.5 * mm, ys - 1.4 * mm, cw - 3 * mm, 0.6 * mm, fillColor=colors.white, strokeColor=None))
            yo = ys - 9 * mm
            d.add(Rect(cx, yo, cw, 6.5 * mm, rx=2, ry=2, fillColor=KICK if orch[k] == "K" else ORCH, strokeColor=None))
            d.add(String(cx + cw / 2, yo + 2.1 * mm, orch[k], fontName="DV", fontSize=7.5,
                         fillColor=MUT if orch[k] == "K" else TXT, textAnchor="middle"))
            idx += 1
        yp = H - 35 * mm
        d.add(Rect(x, yp, gw, 4.5 * mm, rx=2, ry=2, fillColor=ON, strokeColor=None))
        d.add(String(x + gw / 2, yp + 1.3 * mm, gp, fontName="DVB", fontSize=7, fillColor=TXT, textAnchor="middle"))
        x += gw + ggap
    return d


def d_display():
    W, H = 174 * mm, 14 * mm
    d = Drawing(W, H)
    w0 = 150 * mm
    x0 = (W - w0) / 2
    d.add(Rect(x0, 0, w0, H, rx=5, ry=5, fillColor=colors.HexColor("#2B2D31"), strokeColor=None))
    d.add(String(x0 + 4 * mm, 5 * mm, "Charlie", fontName="DV", fontSize=7, fillColor=MUT))
    x = buttons(d, x0 + 22 * mm, 4.5 * mm, ["<", "13. 3+3+2 toms", ">"], fs=7)
    buttons(d, x + 2 * mm, 4.5 * mm, ["Again", "Vary", "Random", "Open"], fs=7)
    return d


# ------------------------------------------------------------------ document
class Doc(BaseDocTemplate):
    def __init__(self, fn, lang):
        super().__init__(fn, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                         bottomMargin=18 * mm, title=NAME + " " + VERSION, author="ReNo Mellow")
        self.lang = lang
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self.footer)])

    def footer(self, c, doc):
        if doc.page == 1:
            return
        t = T[self.lang]
        c.saveState()
        c.setFont("DV", 8)
        c.setFillColor(GREY)
        c.drawString(18 * mm, 10 * mm, "%s %s — %s" % (NAME, VERSION, t["footer"]))
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, "%s %d" % (t["page"], doc.page))
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name == "h1":
            self.notify("TOCEntry", (0, f.getPlainText(), self.page))


def table(rows, head, w1=48):
    data = [[Paragraph(head[0], S["cellb"]), Paragraph(head[1], S["cellb"])]]
    for a, b in rows:
        data.append([Paragraph(a, S["cellb"]), Paragraph(b, S["cell"])])
    t = Table(data, colWidths=[w1 * mm, (174 - w1) * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#D5D9DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def build(lang, out):
    t = T[lang]
    doc = Doc(os.path.join(out, t["file"]), lang)
    story = []
    story += [Spacer(1, 22 * mm), Paragraph(NAME, S["title"]), Spacer(1, 6 * mm), Paragraph(t["sub"], S["sub"]),
              Spacer(1, 4 * mm), Paragraph("%s — version %s" % (t["manual"], VERSION), S["sub"]),
              Spacer(1, 6 * mm), d_grid(),
              Spacer(1, 6 * mm), Paragraph(t["other"], S["center"]), Spacer(1, 3 * mm),
              Paragraph('<link href="%s" color="blue">%s</link>' % (URL_REPO, URL_REPO), S["center"]),
              Spacer(1, 10 * mm), Paragraph(t["toc"], S["h2"])]
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"]]
    story += [toc, PageBreak()]

    body = t["body"]
    i = 0
    while i < len(body):
        item = body[i]
        if item[0] in ("h1", "h2"):
            head = Paragraph(item[1], S[item[0] + "k"])
            # a heading never ends a page: room for the heading and the start of what follows
            nxt = body[i + 1] if i + 1 < len(body) else None
            if nxt and nxt[0] == "draw":
                dw = {"pads": d_pads, "grid": d_grid, "display": d_display}[nxt[1]]()
                story.append(KeepTogether([head, dw, Paragraph(t["cap"], S["cap"])]))
                i += 2
                continue
            story.append(CondPageBreak(32 * mm))
            story.append(head)
        else:
            story += render(item, lang)
        i += 1
    doc.multiBuild(story)
    return os.path.join(out, t["file"])


def render(item, lang):
    t = T[lang]
    kind, val = item
    if kind == "p":
        return [Paragraph(val, S["p"])]
    if kind in ("ol", "ul"):
        items = [ListItem(Paragraph(x, S["p"]), leftIndent=14) for x in val]
        return [ListFlowable(items, bulletType="1" if kind == "ol" else "bullet", start="1" if kind == "ol" else None,
                             bulletFontName="DV", bulletFontSize=9, leftIndent=14)]
    if kind == "table2":
        return [table(val, t["head2"]), Spacer(1, 4)]
    if kind == "table_g":
        return [table(val, t["head_g"]), Spacer(1, 4)]
    if kind == "qa":
        return [KeepTogether([Paragraph("<b>%s</b>" % q, S["p"]), Paragraph(a, S["p"])]) for q, a in val]
    if kind == "draw":
        dw = {"pads": d_pads, "grid": d_grid, "display": d_display}[val]()
        return [KeepTogether([dw, Paragraph(t["cap"], S["cap"])])]
    return []


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
