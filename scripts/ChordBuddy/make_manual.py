# Generates the Chord Buddy user manual, French and English
# (scripts/ChordBuddy/ChordBuddy_manuel_FR.pdf and ChordBuddy_manual_EN.pdf).
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
                                TableStyle, KeepTogether, PageBreak, ListFlowable, ListItem)
from reportlab.platypus.tableofcontents import TableOfContents

VERSION = "1.3"
NAME = "ReNo Mellow - Chord Buddy"
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/ChordBuddy/"
URL_FR = BASE + "ChordBuddy_manuel_FR.pdf"
URL_EN = BASE + "ChordBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Chord_Buddy.ReaperPkg"
URL_REPO = "https://github.com/renothestraws/reno-mellow-script"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT_DIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", FONT_DIR + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

ACCENT = colors.HexColor("#2F6FB5")
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

# ------------------------------------------------------------------ texts
T = {}
T["fr"] = {
    "file": "ChordBuddy_manuel_FR.pdf",
    "sub": "La roue des quintes pour écrire des accords dans l'éditeur MIDI",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "ChordBuddy_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié",
    "head2": ("Élément", "Effet"),
    "head_g": ("Geste", "Effet"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "Chord Buddy écrit des accords dans l'éditeur MIDI à partir d'une <b>roue des quintes</b>. Un clic sur un "
              "accord le pose au <b>curseur d'édition</b>, avec la longueur de la grille, puis le curseur passe à la fin "
              "de l'accord : il suffit de cliquer les accords les uns après les autres pour écrire une grille."),
        ("p", "La roue pivote : la tonalité placée en haut est la tonalité active et ses sept accords sont en couleur, "
              "avec leur degré. Chaque case a son réglage d'<b>inversion</b>, l'octave se choisit au centre, et des "
              "options règlent le type d'accord, le voicing, la basse, le strum et la vélocité."),
        ("p", "Un petit <b>Display</b> affiche le nom de l'accord sous le curseur et <b>exporte</b> les accords "
              "sélectionnés : item sur une piste « Chords », take marker, text event ou symbole d'accord de la vue notation."),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « Chord Buddy », clic droit &gt; Install, "
                "puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Les deux actions "
              "(fenêtre et Display) sont ajoutées à la liste d'actions. Pas de mise à jour automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Copier le dossier <b>ChordBuddy</b> dans le dossier Scripts de REAPER, puis charger "
              "<b>ReNo Mellow - Chord Buddy.lua</b> et <b>ReNo Mellow - Chord Buddy - Display.lua</b> dans la liste "
              "d'actions (Actions &gt; Show action list &gt; New action &gt; Load ReaScript). Les fichiers "
              "ChordBuddy_*.lua sont des bibliothèques : ne pas les charger."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Ouvrir un item MIDI dans l'éditeur MIDI et placer le curseur d'édition au début.",
                "Lancer l'action <b>ReNo Mellow - Chord Buddy</b> (relancer l'action = fermer la fenêtre).",
                "Choisir la grille de l'éditeur MIDI (par exemple 1/1 pour une ronde), ou <b>1 bar</b> dans la fenêtre.",
                "Cliquer <b>C</b>, puis <b>Am</b>, <b>F</b> et <b>G</b> : quatre accords se suivent, chacun à la fin du précédent.",
                "Activer <b>Auto</b> et recommencer : les inversions sont choisies pour que les accords restent proches."]),
        ("h1", "4. La roue"),
        ("draw", "wheel"),
        ("p", "Trois anneaux : accords <b>majeurs</b> à l'extérieur, <b>mineurs</b> relatifs au milieu, <b>diminués</b> "
              "à l'intérieur. La tonalité en haut est active : ses accords sont en couleur avec leur degré "
              "(I, ii, iii, IV, V, vi, vii° ; i, ii°, III... en mineur). Les noms des notes suivent la tonalité "
              "(F# en Sol, Gb en Réb) ; les cases hors tonalité gardent l'orthographe de leur propre tonalité. Chaque case majeure indique l'<b>armure</b> de sa tonalité (0 pour Do, 1# à 6#, 5b à 1b) ; le centre l'affiche à côté de la tonalité active (ex. « Eb major 3b »), la relative mineure ayant la même armure."),
        ("table_g", [
            ("Clic sur une case", "Insère l'accord au curseur d'édition, sur le canal actif de l'éditeur MIDI, puis "
                                  "place le curseur à la fin de l'accord. L'item est allongé si l'accord dépasse."),
            ("Glisser / molette sur la roue", "Fait tourner la roue d'une tonalité à la fois ; la tonalité en haut "
                                              "devient la tonalité active."),
            ("Boutons − / + d'une case", "Changent l'inversion de cette case d'un cran (voir section 6)."),
            ("Clic sur le chiffre (ou clic droit sur les boutons)", "Remet l'inversion de la case à 0."),
            ("Centre : flèches ou molette", "Octave de l'accord (octave de la fondamentale à inv 0). Le centre "
                                            "affiche la tonalité et le numéro de la note Do de cette octave."),
            ("Survol d'une case", "Bulle avec le nom, le degré et les notes ; le mini clavier montre les notes."),
        ]),
        ("h1", "5. Les réglages autour de la roue"),
        ("draw", "bar"),
        ("table2", [
            ("Major / Minor", "Degrés affichés vus depuis la tonalité majeure ou sa relative mineure (mêmes accords)."),
            ("Grid / Grid x2 / Grid x4 / 1 bar", "Longueur de l'accord : la grille de l'éditeur MIDI, deux ou quatre "
                                                 "fois la grille, ou une mesure."),
            ("Auto", "Inversion automatique : la plus proche de l'accord qui précède le curseur. Les cases affichent "
                     "« inv A »."),
            ("Bass", "Ajoute la fondamentale une octave plus bas, toujours sous la note la plus grave."),
            ("Close / Open / Drop 2", "Voicing : serré ; Open monte d'une octave la 2e note en partant du bas ; "
                                      "Drop 2 descend d'une octave la 2e note en partant du haut."),
            ("Triad, 7, maj7, 6, sus2, sus4, add9", "Type d'accord appliqué à toutes les cases : 7 ajoute la septième "
                     "mineure (C7, Dm7, Bm7b5), maj7 la septième majeure, 6 la sixte majeure (Bdim + 6 = Bdim7), "
                     "sus2 / sus4 remplacent la tierce, add9 ajoute la neuvième."),
            ("Strum ms", "Décalage entre les notes, de la plus grave à la plus aiguë (0 = plaqué)."),
            ("Humanize", "Variation aléatoire de la vélocité (+/-)."),
            ("Mini clavier", "Notes de l'accord survolé, avec inversion, voicing et basse."),
        ]),
        ("h1", "6. Les inversions"),
        ("p", "Chaque case a son propre réglage d'inversion, avec ses boutons − et +, de −3 à +3 (−4 à +4 pour les accords à quatre notes). "
              "Chaque cran vers le haut fait monter la note la plus grave d'une octave ; chaque cran vers le bas fait "
              "descendre la note la plus aiguë d'une octave. Exemple avec C (C E G) :"),
        ("table2", [
            ("0", "C E G (état fondamental)"),
            ("+1 / +2", "E G C (1er renversement) / G C E (2e renversement)"),
            ("+3", "C E G une octave plus haut"),
            ("−1 / −2 / −3", "G C E plus bas / E G C plus bas / C E G une octave plus bas"),
        ]),
        ("p", "Le réglage est mémorisé pour chaque case. Avec <b>Auto</b>, il est ignoré : le script compare les "
              "inversions possibles à l'accord précédent et garde la plus proche (de C vers F : C F A)."),
        ("h1", "7. Le Display"),
        ("p", "Petite barre sans titre, à placer où l'on veut (action « ReNo Mellow - Chord Buddy - Display »). Elle "
              "affiche en grand le nom de l'accord sous le <b>curseur d'édition</b> et suit le <b>curseur de lecture</b> "
              "pendant la lecture. Elle lit la prise de l'éditeur MIDI ou, sans éditeur ouvert, l'item MIDI "
              "sélectionné sous le curseur."),
        ("draw", "display"),
        ("table_g", [
            ("Open", "Ouvre la fenêtre Chord Buddy (rien ne se passe si elle est déjà ouverte)."),
            ("Export", "Exporte les accords sélectionnés avec les modes cochés dans Set up (section 8)."),
            ("Clic droit sur Export", "Menu : exporter avec un seul mode, cette fois seulement."),
            ("Clic droit sur une zone vide", "Menu : Open Chord Buddy, Dock in REAPER docker (range le Display dans un "
                                             "docker de REAPER, décocher pour le libérer), Close."),
            ("Relancer l'action Display", "Fermer le Display."),
        ]),
        ("p", "Noms reconnus : triades (majeur, mineur, dim, aug), sus2, sus4, 5, 6, m6, 7, maj7, m7, m7b5, dim7, mMaj7, "
              "7sus4, add9, madd9, avec la basse si elle n'est pas la fondamentale (C/E). « ? » = accord inconnu. Quand un "
              "même groupe de notes a deux noms possibles, la basse tranche (C E G A avec Do à la basse = C6, avec La = Am7)."),
        ("h1", "8. Les exports"),
        ("p", "Sélectionner les notes d'un ou de plusieurs accords, puis cliquer <b>Export</b> sur le Display. Les "
              "notes sont regroupées en accords : une note fait partie de l'accord si elle commence pendant que les "
              "notes déjà prises sonnent encore (les accords strummés restent entiers). Chaque accord est exporté "
              "à sa place, le tout en une seule annulation. Un export déjà présent au même endroit est remplacé."),
        ("table2", [
            ("Item on « Chords » track", "Item vide de la durée de l'accord, avec le nom en note d'item, sur la piste "
                                         "« Chords » (créée tout en haut du projet si elle n'existe pas ; nom réglable)."),
            ("Take marker", "Take marker au début de l'accord, sur l'item qui contient l'accord."),
            ("Text event", "Événement texte MIDI (type Text) au début de l'accord, dans la prise."),
            ("Notation event", "Symbole d'accord de la vue notation de l'éditeur MIDI, au-dessus de la portée."),
        ]),
        ("p", "Option <b>Color exported items and markers by degree</b> : items et take markers prennent la couleur "
              "du degré de l'accord dans la tonalité active (comme sur la roue)."),
        ("h1", "9. Onglet Set up"),
        ("table2", [
            ("Window", "Opacity (opacité du fond), Wheel size, Text size."),
            ("Insertion", "Velocity (100 par défaut), Replace existing notes (supprime les notes qui commencent dans "
                          "la zone de l'accord ; désactivé par défaut), Move edit cursor to the end of the chord."),
            ("Note names", "Spelling : Follow the key, Always sharps, Always flats. Octave naming : Like REAPER (lit le "
                           "réglage « MIDI octave name display offset ») ou Manual ; la ligne grise indique le nom "
                           "donné à la note 60."),
            ("Export (Display)", "Modes cochés pour le bouton Export, nom de la piste Chords, couleurs par degré."),
            ("Display", "Open / Close Display ; Open the Display when REAPER starts (ajoute un petit bloc à "
                        "Scripts/__startup.lua) ; taille du texte et opacité du Display."),
        ]),
        ("h1", "10. Les actions"),
        ("table2", [
            ("ReNo Mellow - Chord Buddy", "Fenêtre principale (relancer = fermer). Icône de barre d'outils allumée "
                                          "tant qu'elle est ouverte."),
            ("ReNo Mellow - Chord Buddy - Display", "Ouvre ou ferme le Display."),
        ]),
        ("p", "Les deux actions sont dans la section Main et s'associent à un raccourci ou à un bouton de barre "
              "d'outils, au choix."),
        ("h1", "11. Questions fréquentes"),
        ("p", "Les cas les plus courants."),
        ("qa", [
            ("Rien ne se passe quand je clique un accord.",
             "Un item MIDI doit être ouvert dans l'éditeur MIDI : le message apparaît sous la roue."),
            ("L'octave ne correspond pas à mon piano roll.",
             "Set up &gt; Octave naming : passer en Manual et régler l'offset (la ligne grise montre le nom de la note 60)."),
            ("Export dit « Select the notes of one or more chords first ».",
             "Sélectionner les notes des accords dans l'éditeur MIDI (ou sélectionner l'item dans l'arrangement)."),
            ("Le nom affiché est « ? ».",
             "Le groupe de notes ne correspond à aucun accord connu (par exemple deux notes seulement)."),
            ("Auto choisit une inversion inattendue.",
             "Auto se règle sur l'accord qui précède le curseur. Désactiver Auto pour reprendre les inversions réglées avec − / +."),
        ]),
    ],
}

T["en"] = {
    "file": "ChordBuddy_manual_EN.pdf",
    "sub": "The circle of fifths for writing chords in the MIDI editor",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "ChordBuddy_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing",
    "head2": ("Item", "Effect"),
    "head_g": ("Gesture", "Effect"),
    "body": [
        ("h1", "1. What it does"),
        ("p", "Chord Buddy writes chords in the MIDI editor from a <b>circle of fifths</b>. Clicking a chord puts it "
              "at the <b>edit cursor</b>, as long as the grid, then moves the cursor to the end of the chord: click "
              "chords one after the other to write a progression."),
        ("p", "The wheel turns: the key at the top is the active key and its seven chords are colored, with their "
              "degree. Each cell has its own <b>inversion</b> setting, the octave is chosen in the center, and options "
              "set the chord type, voicing, bass, strum and velocity."),
        ("p", "A small <b>Display</b> shows the name of the chord under the cursor and <b>exports</b> the selected "
              "chords: item on a « Chords » track, take marker, text event or chord symbol of the notation view."),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « Chord Buddy », right-click &gt; Install, "
                "then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drop it into REAPER. Both actions (window "
              "and Display) are added to the action list. No automatic updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Copy the <b>ChordBuddy</b> folder into the REAPER Scripts folder, then load "
              "<b>ReNo Mellow - Chord Buddy.lua</b> and <b>ReNo Mellow - Chord Buddy - Display.lua</b> in the action "
              "list (Actions &gt; Show action list &gt; New action &gt; Load ReaScript). The ChordBuddy_*.lua files are "
              "libraries: do not load them."),
        ("h1", "3. First steps"),
        ("ol", ["Open a MIDI item in the MIDI editor and put the edit cursor at its start.",
                "Run the action <b>ReNo Mellow - Chord Buddy</b> (run it again = close the window).",
                "Choose the MIDI editor grid (for example 1/1 for a whole note), or <b>1 bar</b> in the window.",
                "Click <b>C</b>, then <b>Am</b>, <b>F</b> and <b>G</b>: four chords follow each other, each at the end "
                "of the previous one.",
                "Turn <b>Auto</b> on and do it again: inversions are chosen so that the chords stay close."]),
        ("h1", "4. The wheel"),
        ("draw", "wheel"),
        ("p", "Three rings: <b>major</b> chords outside, relative <b>minor</b> chords in the middle, <b>diminished</b> "
              "chords inside. The key at the top is active: its chords are colored with their degree "
              "(I, ii, iii, IV, V, vi, vii°; i, ii°, III... in minor). Note names follow the key (F# in G, Gb in Db); "
              "cells outside the key keep the spelling of their own key. Each major cell shows the <b>key signature</b> of its "
              "key (0 for C, 1# to 6#, 5b to 1b); the center shows it next to the active key (e.g. « Eb major 3b »), "
              "the relative minor having the same signature."),
        ("table_g", [
            ("Click on a cell", "Inserts the chord at the edit cursor, on the active channel of the MIDI editor, then "
                                "moves the cursor to the end of the chord. The item is extended if needed."),
            ("Drag / wheel on the wheel", "Turns the wheel one key at a time; the key at the top becomes the active key."),
            ("− / + buttons of a cell", "Change the inversion of that cell by one step (see section 6)."),
            ("Click on the number (or right-click on the buttons)", "Resets the inversion of the cell to 0."),
            ("Center: arrows or wheel", "Octave of the chord (octave of the root at inv 0). The center shows the key "
                                        "and the number of the C note of that octave."),
            ("Hover a cell", "Tooltip with the name, degree and notes; the mini keyboard shows the notes."),
        ]),
        ("h1", "5. Settings around the wheel"),
        ("draw", "bar"),
        ("table2", [
            ("Major / Minor", "Degrees shown from the major key or its relative minor (same chords)."),
            ("Grid / Grid x2 / Grid x4 / 1 bar", "Chord length: the MIDI editor grid, two or four times the grid, or one bar."),
            ("Auto", "Automatic inversion: the closest to the chord before the cursor. Cells show « inv A »."),
            ("Bass", "Adds the root an octave lower, always under the lowest note."),
            ("Close / Open / Drop 2", "Voicing: close; Open raises the 2nd note from the bottom by an octave; "
                                      "Drop 2 lowers the 2nd note from the top by an octave."),
            ("Triad, 7, maj7, 6, sus2, sus4, add9", "Chord type applied to every cell: 7 adds the minor seventh (C7, Dm7, "
                     "Bm7b5), maj7 the major seventh, 6 the major sixth (Bdim + 6 = Bdim7), sus2 / sus4 replace the "
                     "third, add9 adds the ninth."),
            ("Strum ms", "Delay between the notes, from the lowest to the highest (0 = block chord)."),
            ("Humanize", "Random velocity variation (+/-)."),
            ("Mini keyboard", "Notes of the hovered chord, with inversion, voicing and bass."),
        ]),
        ("h1", "6. Inversions"),
        ("p", "Each cell has its own inversion setting, with its − and + buttons, from −3 to +3 (−4 to +4 for four-note chords). Each step up raises "
              "the lowest note by an octave; each step down lowers the highest note by an octave. Example with C (C E G):"),
        ("table2", [
            ("0", "C E G (root position)"),
            ("+1 / +2", "E G C (1st inversion) / G C E (2nd inversion)"),
            ("+3", "C E G one octave higher"),
            ("−1 / −2 / −3", "G C E lower / E G C lower / C E G one octave lower"),
        ]),
        ("p", "The setting is remembered for each cell. With <b>Auto</b> it is ignored: the script compares the possible "
              "inversions with the previous chord and keeps the closest one (from C to F: C F A)."),
        ("h1", "7. The Display"),
        ("p", "Small bar without a title, to place anywhere (action « ReNo Mellow - Chord Buddy - Display »). It shows in "
              "large letters the name of the chord under the <b>edit cursor</b> and follows the <b>play cursor</b> during "
              "playback. It reads the MIDI editor take or, with no editor open, the selected MIDI item under the cursor."),
        ("draw", "display"),
        ("table_g", [
            ("Open", "Opens the Chord Buddy window (nothing happens if it is already open)."),
            ("Export", "Exports the selected chords with the modes ticked in Set up (section 8)."),
            ("Right-click on Export", "Menu: export with one mode, this time only."),
            ("Right-click an empty spot", "Menu: Open Chord Buddy, Dock in REAPER docker (puts the Display in a REAPER "
                                          "docker, untick to float it again), Close."),
            ("Run the Display action again", "Close the Display."),
        ]),
        ("p", "Recognized names: triads (major, minor, dim, aug), sus2, sus4, 5, 6, m6, 7, maj7, m7, m7b5, dim7, mMaj7, "
              "7sus4, add9, madd9, with the bass when it is not the root (C/E). « ? » = unknown chord. When the same notes "
              "have two possible names, the bass decides (C E G A with C in the bass = C6, with A = Am7)."),
        ("h1", "8. Exports"),
        ("p", "Select the notes of one or more chords, then click <b>Export</b> on the Display. Notes are grouped into "
              "chords: a note belongs to the chord when it starts while the notes already taken are still sounding "
              "(strummed chords stay whole). Each chord is exported at its own place, all in a single undo. An export "
              "already at the same place is replaced."),
        ("table2", [
            ("Item on « Chords » track", "Empty item as long as the chord, with the name as item notes, on the « Chords » "
                                         "track (created at the top of the project if missing; name can be changed)."),
            ("Take marker", "Take marker at the start of the chord, on the item holding the chord."),
            ("Text event", "MIDI text event (Text type) at the start of the chord, in the take."),
            ("Notation event", "Chord symbol of the MIDI editor notation view, above the staff."),
        ]),
        ("p", "Option <b>Color exported items and markers by degree</b>: items and take markers get the color of the "
              "chord's degree in the active key (as on the wheel)."),
        ("h1", "9. Set up tab"),
        ("table2", [
            ("Window", "Opacity (background), Wheel size, Text size."),
            ("Insertion", "Velocity (100 by default), Replace existing notes (deletes notes starting inside the chord; "
                          "off by default), Move edit cursor to the end of the chord."),
            ("Note names", "Spelling: Follow the key, Always sharps, Always flats. Octave naming: Like REAPER (reads the "
                           "« MIDI octave name display offset » setting) or Manual; the grey line shows the name of note 60."),
            ("Export (Display)", "Modes ticked for the Export button, Chords track name, colors by degree."),
            ("Display", "Open / Close Display; Open the Display when REAPER starts (adds a small block to "
                        "Scripts/__startup.lua); text size and opacity of the Display."),
        ]),
        ("h1", "10. Actions"),
        ("table2", [
            ("ReNo Mellow - Chord Buddy", "Main window (run again = close). Toolbar icon lit while it is open."),
            ("ReNo Mellow - Chord Buddy - Display", "Opens or closes the Display."),
        ]),
        ("p", "Both actions are in the Main section; assign them to any shortcut or toolbar button you like."),
        ("h1", "11. FAQ"),
        ("p", "The most common cases."),
        ("qa", [
            ("Nothing happens when I click a chord.",
             "A MIDI item must be open in the MIDI editor: the message is shown under the wheel."),
            ("The octave does not match my piano roll.",
             "Set up &gt; Octave naming: choose Manual and set the offset (the grey line shows the name of note 60)."),
            ("Export says « Select the notes of one or more chords first ».",
             "Select the notes of the chords in the MIDI editor (or select the item in the arrange view)."),
            ("The name shown is « ? ».", "The notes do not match any known chord (for example only two notes)."),
            ("Auto picks an unexpected inversion.",
             "Auto follows the chord before the cursor. Turn Auto off to use the inversions set with − / + again."),
        ]),
    ],
}

# ------------------------------------------------------------------ drawings (simplified, not screenshots)
FIFTHS = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
MINORS = ["Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m", "Bbm", "Fm", "Cm", "Gm", "Dm"]
DIMS = ["Bdim", "F#dim", "C#dim", "G#dim", "D#dim", "A#dim", "E#dim", "Cdim", "Gdim", "Ddim", "Adim", "Edim"]
DEG = {(0, 1): ("I", "#9EE0CC"), (1, 1): ("V", "#AAD8E6"), (11, 1): ("IV", "#CCFFCC"),
       (0, 2): ("vi", "#FFD27F"), (1, 2): ("iii", "#FF9F7A"), (11, 2): ("ii", "#F7F7C0"),
       (0, 3): ("vii°", "#FFC0CB")}
BTN = colors.HexColor("#3A3D42")
ON = colors.HexColor("#3F7FC9")
TXT = colors.HexColor("#E8E8E8")
MUT = colors.HexColor("#9A9A9A")


def d_wheel(size=92 * mm):
    W = 174 * mm
    d = Drawing(W, size)
    cx, cy, R = W / 2, size / 2, size / 2 - 1
    rings = [(1, 0.76, 1.0, FIFTHS, 11), (2, 0.55, 0.76, MINORS, 8.5), (3, 0.34, 0.55, DIMS, 6)]
    for ring, r1, r2, names, fs in rings:
        for pos in range(12):
            mid = 90 - pos * 30                      # reportlab angles: counter-clockwise from the right
            deg = DEG.get((pos, ring))
            col = colors.HexColor(deg[1]) if deg else colors.HexColor("#BDBDBD")
            d.add(Wedge(cx, cy, R * r2, mid - 15, mid + 15, radius1=R * r1, fillColor=col,
                        strokeColor=colors.HexColor("#808080"), strokeWidth=0.8))
            rm = R * (r1 + r2) / 2
            x, y = cx + rm * math.cos(math.radians(mid)), cy + rm * math.sin(math.radians(mid))
            tc = colors.HexColor("#505050") if deg else colors.HexColor("#6E6E6E")
            d.add(String(x, y - fs * 0.15, names[pos], fontName="DVB", fontSize=fs, fillColor=tc, textAnchor="middle"))
            by = y - fs * 0.15 - 7.5
            for bx, t in ((x - 7.5, "-"), (x + 4.5, "+")):
                d.add(Rect(bx, by, 3.5, 3.6, rx=0.8, ry=0.8, fillColor=colors.HexColor("#F2F2F2"),
                           strokeColor=colors.HexColor("#9A9A9A"), strokeWidth=0.3))
                d.add(String(bx + 1.75, by + 0.8, t, fontName="DVB", fontSize=3.4, fillColor=DARK, textAnchor="middle"))
            d.add(String(x, by + 0.8, "0", fontName="DVB", fontSize=3.6, fillColor=tc, textAnchor="middle"))
            top = deg[0] if (deg and ring != 3) else None
            if ring == 1:
                sig = "0" if pos == 0 else ("%d#" % pos if pos <= 6 else "%db" % (12 - pos))
                top = (top + "  " + sig) if top else sig
            if top:
                d.add(String(x, y + fs * 0.75, top, fontName="DV", fontSize=5, fillColor=tc, textAnchor="middle"))
    d.add(Circle(cx, cy, R * 0.34, fillColor=colors.HexColor("#F0F0F0"), strokeColor=colors.HexColor("#808080"),
                 strokeWidth=0.8))
    d.add(String(cx, cy + R * 0.17, "C major  0", fontName="DVB", fontSize=7, fillColor=DARK, textAnchor="middle"))
    t = 3.2
    d.add(Polygon([cx, cy + R * 0.11 + t, cx - t, cy + R * 0.11 - t * 0.6, cx + t, cy + R * 0.11 - t * 0.6],
                  fillColor=GREY, strokeColor=None))
    d.add(String(cx, cy - 4, "Oct 4", fontName="DVB", fontSize=10, fillColor=DARK, textAnchor="middle"))
    d.add(Polygon([cx - t, cy - R * 0.12 + t * 0.6, cx + t, cy - R * 0.12 + t * 0.6, cx, cy - R * 0.12 - t],
                  fillColor=GREY, strokeColor=None))
    d.add(String(cx, cy - R * 0.24, "C4 = 60", fontName="DV", fontSize=5, fillColor=GREY, textAnchor="middle"))
    return d


def buttons(d, x, y, labels, on=(), h=5 * mm, fs=6.5):
    for lab in labels:
        w = max(8 * mm, len(lab) * fs * 0.62 + 4 * mm)
        d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=ON if lab in on else BTN, strokeColor=None))
        d.add(String(x + w / 2, y + h / 2 - fs * 0.35, lab, fontName="DV", fontSize=fs, fillColor=TXT,
                     textAnchor="middle"))
        x += w + 1.2 * mm
    return x


def d_bar(lang="fr"):
    W, H = 174 * mm, 40 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    d.add(String(8, H - 5 * mm, "Chord Buddy    Set up", fontName="DVB", fontSize=8, fillColor=colors.white))
    buttons(d, 8, H - 13 * mm, ["Major", "Minor", "Grid  v", "Auto", "Bass", "Close  v"], on=("Major", "Auto"))
    d.add(Circle(W / 2, H / 2 - 1 * mm, 6 * mm, fillColor=colors.HexColor("#BDBDBD"), strokeColor=None))
    d.add(Circle(W / 2, H / 2 - 1 * mm, 2.6 * mm, fillColor=colors.HexColor("#F0F0F0"), strokeColor=None))
    d.add(String(W / 2 + 9 * mm, H / 2 - 2 * mm, "la roue" if lang == "fr" else "the wheel", fontName="DVI",
                 fontSize=7, fillColor=MUT))
    buttons(d, 8, 8 * mm, ["Triad", "7", "maj7", "6", "sus2", "sus4", "add9"], on=("7",))
    d.add(String(8, 2.5 * mm, "Strum ms   |   Humanize   |   mini keyboard", fontName="DV", fontSize=6.5, fillColor=MUT))
    return d


def d_display():
    W, H = 174 * mm, 16 * mm
    d = Drawing(W, H)
    x0 = (W - 62 * mm) / 2
    d.add(Rect(x0, 0, 62 * mm, H, rx=5, ry=5, fillColor=DARK, strokeColor=None))
    d.add(String(x0 + 4 * mm, 4.8 * mm, "Dm7", fontName="DVB", fontSize=16, fillColor=TXT))
    buttons(d, x0 + 30 * mm, 5 * mm, ["Open", "Export"], fs=7)
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
              Spacer(1, 6 * mm), d_wheel(70 * mm),
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
            head = Paragraph(item[1], S[item[0]])
            # a heading never ends a page: keep it with what follows
            if i + 1 < len(body) and body[i + 1][0] in ("draw", "p", "table2", "ol"):
                story.append(KeepTogether([head] + render(body[i + 1], lang)))
                i += 2
                continue
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
        dw = d_bar(lang) if val == "bar" else {"wheel": d_wheel, "display": d_display}[val]()
        return [KeepTogether([dw, Paragraph(t["cap"], S["cap"])])]
    return []


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
