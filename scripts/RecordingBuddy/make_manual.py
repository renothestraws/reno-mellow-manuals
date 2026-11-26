# Generates the Recording Buddy user manual, French and English
# (scripts/RecordingBuddy/RecordingBuddy_manuel_FR.pdf and RecordingBuddy_manual_EN.pdf).
# Usage: python3 make_manual.py [output folder]
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Polygon, Circle, Line
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, ListFlowable, ListItem, Image)
from reportlab.platypus.tableofcontents import TableOfContents

VERSION = "1.2"
NAME = "ReNo Mellow - Recording Buddy"
FOLDER = "RecordingBuddy"
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/RecordingBuddy/"
URL_FR = BASE + "RecordingBuddy_manuel_FR.pdf"
URL_EN = BASE + "RecordingBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Recording_Buddy.ReaperPkg"
URL_REPO = "https://github.com/renothestraws/reno-mellow-script"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT_DIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", FONT_DIR + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

ACCENT = colors.HexColor("#2F7D4F")
DARK = colors.HexColor("#2B2D31")
GREY = colors.HexColor("#6B6F76")
LIGHT = colors.HexColor("#EEF3EF")

S = {
    "title": ParagraphStyle("title", fontName="DVB", fontSize=26, leading=32, alignment=TA_CENTER, textColor=DARK),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=13, leading=18, alignment=TA_CENTER, textColor=GREY),
    "center": ParagraphStyle("center", fontName="DV", fontSize=10, leading=14, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=15, leading=19, spaceBefore=10, spaceAfter=6, textColor=ACCENT,
                         keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, spaceBefore=7, spaceAfter=3, textColor=DARK,
                         keepWithNext=1),
    "p": ParagraphStyle("p", fontName="DV", fontSize=10, leading=13.4, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=9, leading=12),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=9, leading=12),
    "cap": ParagraphStyle("cap", fontName="DVI", fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=GREY,
                          spaceAfter=6),
    "toc1": ParagraphStyle("toc1", fontName="DV", fontSize=10.5, leading=16, leftIndent=8),
}

# ------------------------------------------------------------------ texts
T = {}
T["fr"] = {
    "file": "RecordingBuddy_manuel_FR.pdf",
    "sub": "Répéter puis enregistrer une boucle en plusieurs passes",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "RecordingBuddy_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié",
    "head2": ("Élément", "Effet"),
    "head_g": ("Geste", "Effet"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "Recording Buddy joue une même boucle plusieurs fois de suite. Chaque passage, appelé <b>passe</b>, a "
              "ses propres réglages : une boucle (celle de l'arrangement ou une autre), un pré-roll, une vitesse de "
              "lecture qui ne change pas la hauteur, un mode (écouter, jouer par-dessus, enregistrer ou avancer dans "
              "le morceau) et une pause."),
        ("p", "Exemple : on écoute la boucle à 100 %, on la joue à 90 % puis à 95 % pendant que l'ancienne prise "
              "est muette, et la dernière passe enregistre à 100 %. Tout s'enchaîne sans toucher à la souris."),
        ("draw", "timeline"),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « Recording Buddy », clic droit &gt; "
                "Install, puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Pas de mise à jour automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Copier le dossier <b>RecordingBuddy</b> dans le dossier Scripts de REAPER, puis charger et lancer "
              "<b>ReNo Mellow - Recording Buddy.lua</b> : il ajoute lui-même les autres actions."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Faire une <b>time selection</b> (ou une boucle) sur la partie à travailler.",
                "<b>Armer</b> la piste à enregistrer.",
                "Lancer l'action <b>ReNo Mellow - Recording Buddy</b>.",
                "Cliquer sur le gros bouton <b>Play</b> : la séquence <b>Default</b> joue ses 4 passes (Listen 100 %, "
                "Play 90 %, Play 95 %, Record 100 %).",
                "À tout moment, <b>STOP</b> arrête la séquence et sauvegarde la prise en cours."]),
        ("h1", "4. Onglet Rec Buddy"),
        ("draw", "recbuddy"),
        ("table2", [
            ("Bouton Play", "Lance la séquence. Contour vert au repos, vert en lecture, rouge en enregistrement, "
                            "orange avec le temps restant pendant une pause. Affiche la vitesse en cours."),
            ("Jauge Pass", "Passe en cours (ex. « Pass 2 / 4   90 %   PLAY ») et progression dans la boucle ; "
                           "bleue pendant le pré-roll."),
            ("Range", "Positions de la boucle en cours."),
            ("STOP", "Stop forcé : arrête la séquence, sauvegarde la prise, remet les réglages de REAPER. "
                     "Un stop dans le transport de REAPER arrête aussi la séquence."),
        ]),
        ("h1", "5. Onglet Set up"),
        ("p", "Une ligne = une passe. Les passes sont jouées de haut en bas."),
        ("draw", "setup"),
        ("table2", [
            ("On", "Décocher pour sauter la passe sans la supprimer."),
            ("Loop", "<b>def</b> = la boucle de l'arrangement (déplacée par les Move on au-dessus). "
                     "<b>[</b> et <b>]</b> = début et fin de la boucle propre à la passe, au curseur d'édition "
                     "(gardés en position musicale). Bouton <b>def</b> ou clic droit = revenir à def."),
            ("Pre-roll", "Durée jouée avant la boucle, en mesures ou en ms, 2 décimales (Ctrl+clic pour taper)."),
            ("C", "Pré-roll = du curseur d'édition jusqu'au début de la boucle de la passe."),
            ("Unit", "bars (mesures) ou ms."),
            ("Rate", "Vitesse de lecture de 25 à 200 %, au dixième. La hauteur est conservée."),
            ("Mode", "Listen, Play, Record ou Move on (voir section 6)."),
            ("Pause", "Temps d'attente après la passe (au moins 0,5 s pour Move on)."),
            ("Flèches, X", "Monter, descendre, supprimer la passe."),
            ("Add pass", "Ajoute une passe (copie de la dernière)."),
            ("All pre-rolls from edit cursor", "Comme C, pour toutes les passes."),
            ("Tailles", "Text size, Play button size, Display text size ; Show / Hide Display ; Dock the Display in a REAPER docker (range le Display dans un docker de REAPER, décocher pour le libérer)."),
        ]),
        ("p", "Sous le tableau : un avertissement si une passe enregistre à une autre vitesse que 100 %, et la durée "
              "totale estimée de la séquence."),
        ("h1", "6. Les modes de passe"),
        ("table2", [
            ("Listen", "Lecture simple : on écoute."),
            ("Play", "On joue par-dessus : les items des pistes armées sont muets sous la boucle. Le pré-roll et le "
                     "monitoring restent audibles. Les items qui débordent dans le pré-roll sont coupés le temps de "
                     "la passe puis remis tels quels."),
            ("Record", "Enregistrement en time selection auto punch sur la boucle de la passe."),
            ("Move on", "Arrêt, puis la boucle de l'arrangement avance de sa propre longueur ; le script attend la "
                        "pause. Pas de pré-roll ni de vitesse. Les passes avec leur propre boucle ne bougent pas."),
        ]),
        ("h1", "7. Séquences"),
        ("p", "Les réglages des passes s'enregistrent en séquences nommées. Une étoile (*) signale des modifications "
              "non sauvegardées."),
        ("table2", [
            ("Sequence", "Liste pour charger une séquence."),
            ("Save / Save as...", "Enregistre dans la séquence en cours / sous un nouveau nom."),
            ("Delete", "Supprime la séquence (les passes affichées restent)."),
            ("Examples", "Remet les trois exemples : Default, 4 takes, Practice."),
        ]),
        ("p", "<b>Default</b> : Listen 100 %, Play 90 %, Play 95 %, Record 100 %. <b>4 takes</b> : 4 passes Record "
              "à 100 %. <b>Practice</b> : Listen 90 %, puis Play 90, 90, 95, 95, 100 et 100 %. Les exemples "
              "utilisent toujours la boucle de l'arrangement (def), avec 2 mesures de pré-roll."),
        ("h1", "8. Le Display"),
        ("p", "Petite fenêtre sans barre de titre qui montre l'état de la séquence, pour travailler sans la grande "
              "fenêtre."),
        ("draw", "display"),
        ("table_g", [
            ("Double-clic", "Démarrer la séquence."),
            ("Ctrl+Alt+double-clic", "Stop forcé."),
            ("Clic droit", "Ouvrir la fenêtre principale sur l'onglet Set up."),
            ("Glisser", "Déplacer le Display."),
            ("Relancer l'action Display", "Fermer le Display."),
        ]),
        ("p", "Un Display ouvert se rouvre à sa place au démarrage de REAPER (un petit bloc est ajouté à "
              "Scripts/__startup.lua)."),
        ("h1", "9. Les actions"),
        ("table2", [
            ("ReNo Mellow - Recording Buddy", "Fenêtre principale (relancer = fermer)."),
            ("... - Display", "Ouvre ou ferme le Display."),
            ("... - Start-Stop", "Lance la séquence sans fenêtre ; relancer = arrêter."),
            ("... - Stop", "Stop forcé."),
        ]),
        ("p", "Ces actions s'associent à un raccourci clavier ou à une commande MIDI (une pédale par exemple) dans "
              "la liste d'actions. Les raccourcis sont à choisir librement."),
        ("p", "<b>Icône de barre d'outils :</b> <b>ReNo_RecordingBuddy</b> (100, 150 et 200 %) est installée avec le "
              "script. Dans Customize toolbars, l'associer à l'action de la fenêtre principale : elle est verte tant que "
              "la fenêtre est ouverte."),
        ("h1", "10. Ce que le script règle pendant une séquence"),
        ("ul", ["Conservation de la hauteur quand la vitesse change.",
                "Mode d'enregistrement time selection auto punch ; la time selection est placée sur la boucle de "
                "chaque passe.",
                "Repeat, pré-roll et count-in de REAPER coupés.",
                "Chaque stop sauvegarde les prises (Stop, save all recorded media).",
                "À la fin, la vitesse, les options et la time selection sont remises comme avant. Après un Move on, "
                "la time selection reste à sa nouvelle place."]),
        ("h1", "11. Questions fréquentes"),
        ("qa", [
            ("Le bouton Play ne démarre rien.",
             "Il faut une time selection ou une boucle, sauf si toutes les passes ont leur propre boucle. Le message "
             "rouge sous la jauge indique ce qui manque."),
            ("Rien n'est enregistré.", "Aucune piste n'est armée : un message le signale au début de la passe Record."),
            ("L'ancienne prise s'entend pendant une passe Play.",
             "Seules les pistes armées sont rendues muettes. Armer la piste qui contient l'ancienne prise."),
            ("Puis-je fermer la grande fenêtre pendant une séquence ?",
             "Oui si le Display est ouvert ou si la séquence a été lancée par Start-Stop. Sinon la séquence s'arrête."),
            ("REAPER a planté pendant une passe Play.",
             "Les items rendus muets ou coupés pour la passe peuvent le rester : les remettre à la main."),
        ]),
    ],
}

T["en"] = {
    "file": "RecordingBuddy_manual_EN.pdf",
    "sub": "Rehearse and record a loop in several passes",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "RecordingBuddy_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing",
    "head2": ("Item", "Effect"),
    "head_g": ("Gesture", "Effect"),
    "body": [
        ("h1", "1. What it does"),
        ("p", "Recording Buddy plays the same loop several times in a row. Each run, called a <b>pass</b>, has its "
              "own settings: a loop (the arrangement loop or another one), a pre-roll, a playback rate that keeps "
              "the pitch, a mode (listen, play along, record or move on in the song) and a pause."),
        ("p", "Example: listen to the loop at 100 %, play it at 90 % then 95 % while the old take is silent, and the "
              "last pass records at 100 %. Everything runs on its own, hands off the mouse."),
        ("draw", "timeline"),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « Recording Buddy », right-click &gt; "
                "Install, then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drop it into REAPER. No automatic updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Copy the <b>RecordingBuddy</b> folder into the REAPER Scripts folder, then load and run "
              "<b>ReNo Mellow - Recording Buddy.lua</b>: it adds the other actions itself."),
        ("h1", "3. First steps"),
        ("ol", ["Make a <b>time selection</b> (or a loop) over the part to work on.",
                "<b>Arm</b> the track to record.",
                "Run the action <b>ReNo Mellow - Recording Buddy</b>.",
                "Click the big <b>Play</b> button: the <b>Default</b> sequence plays its 4 passes (Listen 100 %, "
                "Play 90 %, Play 95 %, Record 100 %).",
                "At any time, <b>STOP</b> ends the sequence and saves the take being recorded."]),
        ("h1", "4. Rec Buddy tab"),
        ("draw", "recbuddy"),
        ("table2", [
            ("Play button", "Starts the sequence. Green outline when idle, green while playing, red while "
                            "recording, orange with the time left during a pause. Shows the current rate."),
            ("Pass gauge", "Current pass (e.g. « Pass 2 / 4   90 %   PLAY ») and progress through the loop; "
                           "blue during the pre-roll."),
            ("Range", "Position of the current loop."),
            ("STOP", "Forced stop: ends the sequence, saves the take, puts REAPER's settings back. A stop from "
                     "REAPER's transport also ends the sequence."),
        ]),
        ("h1", "5. Set up tab"),
        ("p", "One row = one pass. Passes run from top to bottom."),
        ("draw", "setup"),
        ("table2", [
            ("On", "Untick to skip the pass without deleting it."),
            ("Loop", "<b>def</b> = the arrangement loop (moved by the Move on passes above). <b>[</b> and <b>]</b> = "
                     "start and end of the pass's own loop, at the edit cursor (kept as musical positions). "
                     "<b>def</b> button or right-click = back to def."),
            ("Pre-roll", "Length played before the loop, in bars or ms, 2 decimals (Ctrl+click to type)."),
            ("C", "Pre-roll = from the edit cursor to the loop start of the pass."),
            ("Unit", "bars or ms."),
            ("Rate", "Playback rate from 25 to 200 %, in steps of 0.1. The pitch is kept."),
            ("Mode", "Listen, Play, Record or Move on (see section 6)."),
            ("Pause", "Waiting time after the pass (at least 0.5 s for Move on)."),
            ("Arrows, X", "Move the pass up, down, delete it."),
            ("Add pass", "Adds a pass (copy of the last one)."),
            ("All pre-rolls from edit cursor", "Same as C, for every pass."),
            ("Sizes", "Text size, Play button size, Display text size; Show / Hide Display; Dock the Display in a REAPER docker (puts the Display in a REAPER docker, untick to float it again)."),
        ]),
        ("p", "Under the table: a warning when a pass records at a rate other than 100 %, and the estimated total "
              "length of the sequence."),
        ("h1", "6. Pass modes"),
        ("table2", [
            ("Listen", "Plain playback: just listen."),
            ("Play", "Play along: the items of the armed tracks are silent under the loop. The pre-roll and the "
                     "input monitoring stay audible. Items reaching into the pre-roll are split for the pass, then "
                     "put back as they were."),
            ("Record", "Time selection auto punch recording on the loop of the pass."),
            ("Move on", "Stop, then the arrangement loop moves forward by its own length; the script waits the "
                        "pause. No pre-roll or rate. Passes with their own loop do not move."),
        ]),
        ("h1", "7. Sequences"),
        ("p", "Pass settings are saved as named sequences. A star (*) shows unsaved changes."),
        ("table2", [
            ("Sequence", "List to load a sequence."),
            ("Save / Save as...", "Saves into the current sequence / under a new name."),
            ("Delete", "Deletes the sequence (the passes shown stay)."),
            ("Examples", "Puts back the three examples: Default, 4 takes, Practice."),
        ]),
        ("p", "<b>Default</b>: Listen 100 %, Play 90 %, Play 95 %, Record 100 %. <b>4 takes</b>: 4 Record passes at "
              "100 %. <b>Practice</b>: Listen 90 %, then Play 90, 90, 95, 95, 100 and 100 %. The examples always "
              "use the arrangement loop (def), with a 2-bar pre-roll."),
        ("h1", "8. The Display"),
        ("p", "Small window without a title bar showing the state of the sequence, to work without the main window."),
        ("draw", "display"),
        ("table_g", [
            ("Double-click", "Start the sequence."),
            ("Ctrl+Alt+double-click", "Forced stop."),
            ("Right-click", "Open the main window on the Set up tab."),
            ("Drag", "Move the Display."),
            ("Run the Display action again", "Close the Display."),
        ]),
        ("p", "An open Display reopens at the same place when REAPER starts (a small block is added to "
              "Scripts/__startup.lua)."),
        ("h1", "9. Actions"),
        ("table2", [
            ("ReNo Mellow - Recording Buddy", "Main window (run again = close)."),
            ("... - Display", "Opens or closes the Display."),
            ("... - Start-Stop", "Starts the sequence without any window; run again = stop."),
            ("... - Stop", "Forced stop."),
        ]),
        ("p", "Assign these actions to a keyboard shortcut or a MIDI control (a footswitch, for example) in the "
              "action list. Pick any shortcuts you like."),
        ("p", "<b>Toolbar icon:</b> <b>ReNo_RecordingBuddy</b> (100, 150 and 200 %) is installed with the script. In "
              "Customize toolbars, give it to the main window action: it turns green while the window is open."),
        ("h1", "10. What the script sets during a sequence"),
        ("ul", ["Pitch is preserved when the rate changes.",
                "Time selection auto punch record mode; the time selection is placed on the loop of each pass.",
                "REAPER's repeat, pre-roll and count-in are switched off.",
                "Every stop saves the takes (Stop, save all recorded media).",
                "At the end, the rate, the options and the time selection are put back. After a Move on, the time "
                "selection stays at its new place."]),
        ("h1", "11. FAQ"),
        ("qa", [
            ("The Play button does not start anything.",
             "A time selection or a loop is needed, unless every pass has its own loop. The red message under the "
             "gauge says what is missing."),
            ("Nothing gets recorded.", "No track is armed: a message says so at the start of the Record pass."),
            ("I still hear the old take during a Play pass.",
             "Only the armed tracks are made silent. Arm the track holding the old take."),
            ("Can I close the main window during a sequence?",
             "Yes if the Display is open or the sequence was started with Start-Stop. Otherwise the sequence stops."),
            ("REAPER crashed during a Play pass.",
             "The items silenced or split for the pass may stay that way: put them back by hand."),
        ]),
    ],
}

# ------------------------------------------------------------------ drawings (simplified, not screenshots)
def d_recbuddy():
    d = Drawing(170 * mm, 62 * mm)
    W = 170 * mm
    d.add(Rect(0, 0, W, 62 * mm, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    d.add(String(8, 62 * mm - 14, "Rec Buddy   Set up", fontName="DVB", fontSize=8, fillColor=colors.white))
    bx, by, bw, bh = W / 2 - 30 * mm, 26 * mm, 60 * mm, 28 * mm
    d.add(Rect(bx, by, bw, bh, rx=8, ry=8, fillColor=ACCENT, strokeColor=None))
    cx, cy, s = bx + bw / 2, by + bh * 0.62, 6 * mm
    d.add(Polygon([cx - s * 0.8, cy - s, cx - s * 0.8, cy + s, cx + s, cy], fillColor=colors.white, strokeColor=None))
    d.add(String(cx, by + 4 * mm, "90 %", fontName="DVB", fontSize=13, fillColor=colors.white, textAnchor="middle"))
    d.add(Rect(8, 16 * mm, W - 16, 7 * mm, rx=3, ry=3, fillColor=colors.HexColor("#24272B"), strokeColor=None))
    d.add(Rect(8, 16 * mm, (W - 16) * 0.45, 7 * mm, rx=3, ry=3, fillColor=ACCENT, strokeColor=None))
    d.add(String(12, 18.3 * mm, "Pass 2 / 4   90 %   PLAY", fontName="DV", fontSize=8, fillColor=colors.white))
    d.add(String(W - 12, 18.3 * mm, "Playing", fontName="DV", fontSize=8, fillColor=colors.white, textAnchor="end"))
    d.add(String(8, 11 * mm, "Range: 17.1.00  ->  25.1.00", fontName="DV", fontSize=7, fillColor=colors.HexColor("#9A9A9A")))
    d.add(Rect(8, 3 * mm, W - 16, 6 * mm, rx=3, ry=3, fillColor=colors.HexColor("#8E2A22"), strokeColor=None))
    d.add(String(W / 2, 4.6 * mm, "STOP", fontName="DVB", fontSize=9, fillColor=colors.white, textAnchor="middle"))
    return d


def d_setup():
    cols = [("#", 7), ("On", 8), ("Loop", 40), ("Pre-roll", 20), ("C", 6), ("Unit", 12), ("Rate", 16),
            ("Mode", 18), ("Pause", 14), ("", 18)]
    rows = [("1", "x", "def  17.1 - 25.1", "2.00 bars", "C", "bars", "100.0 %", "Listen", "3.0 s", "^ v X"),
            ("2", "x", "def  17.1 - 25.1", "2.00 bars", "C", "bars", "90.0 %", "Play", "3.0 s", "^ v X"),
            ("3", "x", "[ ]  33.1 - 37.1  def", "1.50 bars", "C", "bars", "95.0 %", "Play", "3.0 s", "^ v X"),
            ("4", "x", "moves to 25.1", "-", "", "", "-", "Move on", "3.0 s", "^ v X"),
            ("5", "x", "def  25.1 - 33.1", "2.00 bars", "C", "bars", "100.0 %", "Record", "0.0 s", "^ v X")]
    mode_col = {"Listen": "#24456E", "Record": "#6E2620", "Move on": "#5E4C1C"}
    W = sum(c[1] for c in cols) * mm
    rh = 6 * mm
    H = rh * (len(rows) + 2) + 4
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=5, ry=5, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    y = H - rh - 2
    x = 0
    d.add(String(4, y + 2 * mm, "Sequence  [ Default  v ]   Save   Save as...   Delete   Examples",
                 fontName="DV", fontSize=7, fillColor=colors.white))
    y -= rh
    for name, w in cols:
        d.add(String(x + 3, y + 2 * mm, name, fontName="DVB", fontSize=7, fillColor=colors.HexColor("#CFCFCF")))
        x += w * mm
    for i, r in enumerate(rows):
        y -= rh
        if i % 2 == 0:
            d.add(Rect(0, y, W, rh, fillColor=colors.HexColor("#26292D"), strokeColor=None))
        x = 0
        for k, (name, w) in enumerate(cols):
            v = r[k]
            if name == "Mode" and v in mode_col:
                d.add(Rect(x + 1, y + 1, w * mm - 2, rh - 2, rx=2, ry=2,
                           fillColor=colors.HexColor(mode_col[v]), strokeColor=None))
            col = colors.HexColor("#9A9A9A") if (name == "Loop" and (v.startswith("def") or v.startswith("moves"))) \
                else colors.white
            d.add(String(x + 3, y + 2 * mm, v, fontName="DV", fontSize=7, fillColor=col))
            x += w * mm
    return d


def d_display():
    d = Drawing(80 * mm, 18 * mm)
    d.add(Rect(0, 0, 80 * mm, 18 * mm, rx=6, ry=6, fillColor=DARK, strokeColor=None))
    d.add(Circle(9 * mm, 9 * mm, 4 * mm, fillColor=colors.HexColor("#E04A3E"), strokeColor=None))
    d.add(String(17 * mm, 12 * mm, "Pass 4/4  100 %  REC", fontName="DVB", fontSize=8,
                 fillColor=colors.HexColor("#E04A3E")))
    d.add(Rect(17 * mm, 7.5 * mm, 58 * mm, 2.5 * mm, rx=1, ry=1, fillColor=colors.HexColor("#1E2023"), strokeColor=None))
    d.add(Rect(17 * mm, 7.5 * mm, 30 * mm, 2.5 * mm, rx=1, ry=1, fillColor=colors.HexColor("#E04A3E"), strokeColor=None))
    d.add(String(17 * mm, 2.5 * mm, "Recording", fontName="DV", fontSize=7, fillColor=colors.HexColor("#E8E8E8")))
    return d


def d_timeline(lang):
    lab = {"fr": ("pré-roll", "boucle", "pause", "temps"), "en": ("pre-roll", "loop", "pause", "time")}[lang]
    passes = [("Listen 100 %", "#4A6FA5", "#3FBF6F"), ("Play 90 %", "#4A6FA5", "#3FBF6F"),
              ("Play 95 %", "#4A6FA5", "#3FBF6F"), ("Record 100 %", "#4A6FA5", "#E04A3E")]
    W = 170 * mm
    d = Drawing(W, 30 * mm)
    seg = (W - 20) / 4
    y = 14 * mm
    for i, (name, cpre, cloop) in enumerate(passes):
        x0 = 10 + i * seg
        pre_w, loop_w, pause_w = seg * 0.22, seg * 0.55, seg * 0.15 if i < 3 else 0
        d.add(Rect(x0, y, pre_w, 7 * mm, fillColor=colors.HexColor(cpre), strokeColor=None))
        d.add(Rect(x0 + pre_w, y, loop_w, 7 * mm, fillColor=colors.HexColor(cloop), strokeColor=None))
        if pause_w:
            d.add(Rect(x0 + pre_w + loop_w, y, pause_w, 7 * mm, fillColor=colors.HexColor("#E0A030"),
                       strokeColor=None))
        d.add(String(x0, y + 9 * mm, name, fontName="DVB", fontSize=8, fillColor=DARK))
    d.add(Line(10, y - 3, W - 10, y - 3, strokeColor=GREY, strokeWidth=0.6))
    d.add(String(W - 10, y - 10, lab[3] + " ->", fontName="DV", fontSize=7, fillColor=GREY, textAnchor="end"))
    lx = 10
    for txt, c in ((lab[0], "#4A6FA5"), (lab[1], "#3FBF6F"), (lab[2], "#E0A030")):
        d.add(Rect(lx, 2 * mm, 4 * mm, 3 * mm, fillColor=colors.HexColor(c), strokeColor=None))
        d.add(String(lx + 5 * mm, 2.4 * mm, txt, fontName="DV", fontSize=7, fillColor=DARK))
        lx += 28 * mm
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
    story += [Spacer(1, 45 * mm), Paragraph(NAME, S["title"]), Spacer(1, 6 * mm), Paragraph(t["sub"], S["sub"]),
              Spacer(1, 4 * mm), Paragraph("%s — version %s" % (t["manual"], VERSION), S["sub"]),
              Spacer(1, 10 * mm),
              Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon_200.png"), width=60 * mm, height=20 * mm),
              Spacer(1, 18 * mm), Paragraph(t["other"], S["center"]), Spacer(1, 3 * mm),
              Paragraph('<link href="%s" color="blue">%s</link>' % (URL_REPO, URL_REPO), S["center"]),
              Spacer(1, 16 * mm), Paragraph(t["toc"], S["h2"])]
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"]]
    story += [toc, PageBreak()]

    body = t["body"]
    i = 0
    while i < len(body):
        item = body[i]
        if item[0] in ("h1", "h2"):
            head = Paragraph(item[1], S[item[0]])
            # a heading never ends a page: keep it with a drawing or the first paragraph after it
            if i + 1 < len(body) and body[i + 1][0] in ("draw", "p"):
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
        out = []
        for q, a in val:
            out.append(KeepTogether([Paragraph("<b>%s</b>" % q, S["p"]), Paragraph(a, S["p"])]))
        return out
    if kind == "draw":
        dr = {"recbuddy": d_recbuddy, "setup": d_setup, "display": d_display}.get(val)
        dw = dr() if dr else d_timeline(lang)
        return [KeepTogether([dw, Paragraph(t["cap"], S["cap"])])]
    return []


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
