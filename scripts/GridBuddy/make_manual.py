# Generates the Grid Buddy user manual, French and English
# (scripts/GridBuddy/GridBuddy_manuel_FR.pdf and GridBuddy_manual_EN.pdf).
# Usage: python3 make_manual.py [output folder]
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, ListFlowable, ListItem, Image)
from reportlab.platypus.tableofcontents import TableOfContents

VERSION = "1.5"
NAME = "ReNo Mellow - Grid Buddy"
FOLDER = "GridBuddy"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/GridBuddy/"
URL_FR = BASE + "GridBuddy_manuel_FR.pdf"
URL_EN = BASE + "GridBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Grid_Buddy.ReaperPkg"
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

ACTIONS = ["Adaptive off (fixed)", "Adaptive narrowest", "Adaptive narrow", "Adaptive medium", "Adaptive wide",
           "Adaptive widest", "Adaptive custom", "Adjust grid (mousewheel)", "Adjust fixed grid (mousewheel)",
           "Wider grid", "Narrower grid", "Adapt grid to zoom", "Toggle swing"]

# ------------------------------------------------------------------ texts
T = {}
T["fr"] = {
    "file": "GridBuddy_manuel_FR.pdf",
    "sub": "La grille de l'arrangement et de l'éditeur MIDI, en un coup d'œil",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "GridBuddy_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié",
    "head2": ("Élément", "Effet"),
    "head_g": ("Geste", "Effet"),
    "zoom": ("zoom arrière : grille plus large", "zoom avant : grille plus fine"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "Grid Buddy rassemble les réglages de la grille de REAPER, dans l'arrangement et dans l'éditeur MIDI : "
              "le <b>type</b> (straight, triplet, quintolet, septolet, pointé, swing), la <b>taille</b> (1/128 à 4), "
              "le snap et le <b>lien</b> entre la grille de l'arrangement et celle de l'éditeur MIDI."),
        ("p", "Il comprend une fenêtre à deux onglets (Grid et Set up), deux petits <b>Displays</b> indépendants "
              "(arrangement et éditeur MIDI) où la molette change la taille de la grille, et des <b>actions isolées</b> à associer à des "
              "raccourcis. Il reprend les idées de Gridbox de FeedTheCat."),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « Grid Buddy », clic droit &gt; Install, "
                "puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Les actions de "
              "l'éditeur MIDI sont ajoutées au premier lancement de Grid Buddy. Pas de mise à jour automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Copier le dossier <b>GridBuddy</b> dans le dossier Scripts de REAPER, puis charger et lancer "
              "<b>ReNo Mellow - Grid Buddy.lua</b> : il ajoute lui-même les deux Displays et toutes les actions "
              "(sections Main et MIDI Editor)."),
        ("p", "Les réglages d'Adaptive Grid / Gridbox sont repris au premier lancement. Ne pas les faire tourner "
              "en même temps que Grid Buddy."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Lancer l'action <b>ReNo Mellow - Grid Buddy</b> (icône de barre d'outils <b>ReNo_GridBuddy</b>, "
                "allumée tant que la fenêtre est ouverte).",
                "Dans l'onglet <b>Grid</b>, section Arrange view, cliquer <b>1/16</b> : la grille passe à la double croche.",
                "Cliquer <b>Triplet</b> : la grille devient 1/16T, à la même taille.",
                "Dans la section MIDI editor, cocher <b>Link MIDI editor to the arrange grid</b> : l'éditeur MIDI "
                "suit la grille de l'arrangement.",
                "Dans l'onglet Set up, <b>Show</b> ouvre le Display de l'arrangement ou le Display MIDI ; la molette "
                "dessus change la taille."]),
        ("h1", "4. Onglet Grid"),
        ("draw", "grid"),
        ("p", "Deux sections : <b>Arrange view</b> et <b>MIDI editor</b>. La grille en cours est écrite en grand "
              "(ex. 1/16T)."),
        ("table2", [
            ("Type", "Straight, Triplet, Quintuplet et Septuplet (si affichés), Dotted, Swing. La taille reste la "
                     "même : 1/8 devient 1/8T, 1/8D..."),
            ("Swing", "Curseur de -100 à 100 % quand le swing est actif (arrangement). Dans l'éditeur MIDI, la "
                      "quantité se règle dans les réglages de grille de REAPER."),
            ("Size", "Frame et Measure (si affichés), puis 1/128 à 4. Le type en cours est gardé."),
            ("- / +", "Grille plus étroite / plus large : divisée ou multipliée par le diviseur."),
            ("Snap", "Snap on/off ; dans l'arrangement aussi Relative (snap relatif) et Snap/grid settings..."),
            ("Link MIDI editor to the arrange grid", "Section MIDI editor : active ou coupe l'option de REAPER "
                     "« Use the same grid division in arrange view and MIDI editor » (voir section 6)."),
        ]),
        ("h1", "5. Onglet Set up"),
        ("p", "Les réglages de la grille et du Display."),
        ("table2", [
            ("Grid divisor", "Pas des boutons - / +, de la molette et des actions Wider / Narrower. 2 par défaut "
                             "(1/8 -&gt; 1/16) ; 3 donne 1/4 -&gt; 1/12..."),
            ("Min size / Max size", "Limites de - / + ; pour la molette : tailles straight la plus fine et la plus large "
                                    "avant les triolets / pointées (vide = 1/128 et 4). Ex. 1/128, 1/8T, 1D, 2."),
            ("Preserve grid type per size", "Le projet retient le type (triplet, swing...) utilisé pour chaque taille."),
            ("Show", "Boutons et entrées de menu Quintuplet, Septuplet ; boutons Frame, Measure."),
            ("Reverse mouse wheel", "Inverse le sens de la molette (Displays et action mousewheel)."),
            ("Wheel sensitivity", "Displays : crans de molette par changement de taille, de 1 à 4 (1,5 par défaut = "
                                  "2 pas pour 3 crans). Plus haut = plus lent."),
            ("Displays", "Une ligne par Display (Arrange, MIDI) : Show / Hide, taille du texte, Snap button ; pour "
                         "l'arrangement aussi Swing bar et Visible grid."),
            ("Window", "Taille du texte de la fenêtre."),
        ]),
        ("p", "Le diviseur et les limites existent deux fois, pour l'arrangement et pour l'éditeur MIDI. Une valeur "
              "refusée est signalée en rouge sous les champs."),
        ("h1", "6. Lier l'éditeur MIDI"),
        ("p", "<b>Lié</b> : l'éditeur MIDI utilise la grille de l'arrangement. La section MIDI editor est grisée avec "
              "« LINKED to the arrange grid », le Display MIDI affiche « MIDI = » en vert et les actions « Grid "
              "Buddy MIDI » changent la grille de l'arrangement."),
        ("p", "<b>Non lié</b> : l'éditeur MIDI a sa propre grille, réglée dans la section MIDI editor, avec le "
              "Display MIDI ou avec les actions « Grid Buddy MIDI »."),
        ("p", "Le lien se change dans la fenêtre (case Link MIDI editor) ou dans le menu des Displays. C'est l'option "
              "de REAPER elle-même : elle reste active même quand Grid Buddy est fermé."),
        ("h1", "7. Les Displays"),
        ("p", "Deux petites fenêtres sans barre de titre, indépendantes, à placer où l'on veut : le <b>Display</b> "
              "de l'arrangement (action Main) et le <b>Display MIDI</b> (action « Grid Buddy MIDI - Display », "
              "visible seulement quand un éditeur MIDI est ouvert). Chacun montre l'aimant du snap et la grille "
              "(barre bleue pour le swing dans l'arrangement)."),
        ("draw", "display"),
        ("table_g", [
            ("Molette", "Taille suivante (vers le haut = plus fin). Après la plus fine viennent 1/8T, 1/16T, "
                        "1/32T ; après la plus large 1/2D, 1/4D, 1/8D, 1/16D, 1/32D (voir ci-dessous)."),
            ("Clic sur la grille", "Menu : Straight, Triplet, Quintuplet / Septuplet (si affichés), Dotted, Swing, "
                                  "puis Frame et Measure (arrangement), Hide grid (cache les lignes de grille), "
                                  "Link MIDI editor ; Display MIDI : aussi Sync to arrange view (action 40640)."),
            ("Alt+clic", "Swing on/off (arrangement)."),
            ("Alt+molette", "Quantité de swing par pas de 3 % (Ctrl+Alt : 1 %), arrangement."),
            ("Clic sur l'aimant", "Snap on/off. Alt+clic : snap relatif (arrangement). Clic droit : réglages snap/grille."),
            ("Clic droit sur la grille", "Ouvre la fenêtre Grid Buddy."),
            ("Glisser", "Déplacer le Display."),
            ("Relancer l'action Display", "Fermer ce Display."),
        ]),
        ("p", "<b>Échelle de la molette</b> (Displays et action Adjust grid) : 1/32T · 1/16T · 1/8T · 1/128 · 1/64 · "
              "1/32 · 1/16 · 1/8 · 1/4 · 1/2 · 1 · 2 · 4 · 1/2D · 1/4D · 1/8D · 1/16D · 1/32D. Elle s'arrête aux "
              "deux bouts. Une grille hors de l'échelle (1/4T, quintolet...) revient d'abord à sa taille straight. "
              "Le swing est gardé sur les tailles straight."),
        ("p", "Grille cachée : le Display affiche « Hidden » ; la molette ou un type la réaffiche. Un Display ouvert "
              "se rouvre à sa place au démarrage de REAPER (un petit bloc est ajouté à "
              "Scripts/__startup.lua). L'option Visible grid affiche la grille que REAPER dessine vraiment à ce zoom "
              "(tailles straight seulement)."),
        ("h1", "8. Les actions"),
        ("p", "Toutes les actions existent dans la section <b>Main</b> (« ReNo Mellow - Grid Buddy - ... ») et dans "
              "la section <b>MIDI Editor</b> (« ReNo Mellow - Grid Buddy MIDI - ... »)."),
        ("table2", [
            ("ReNo Mellow - Grid Buddy", "Fenêtre principale (relancer = fermer)."),
            ("... - Display / ... MIDI - Display", "Ouvre ou ferme le Display de l'arrangement / de l'éditeur MIDI."),
            ("Adjust grid (mousewheel)", "À associer à une molette : même échelle que les Displays."),
            ("Wider grid / Narrower grid", "Grille plus large / plus étroite d'un pas (diviseur)."),
            ("Toggle swing", "Swing on/off."),
        ]),
        ("p", "Ces actions s'associent à un raccourci clavier, une molette (ex. Ctrl+molette) ou une commande MIDI dans "
              "la liste d'actions. Les raccourcis sont à choisir librement : ceux de ce manuel sont des exemples."),
        ("h1", "9. Questions fréquentes"),
        ("p", "Les cas les plus courants."),
        ("qa", [
            ("La section MIDI editor est grisée.",
             "Soit aucun éditeur MIDI n'est ouvert, soit l'éditeur MIDI est lié à l'arrangement (case Link MIDI editor)."),
            ("La molette ne va pas plus loin.", "Elle est au bout de l'échelle : 1/32T d'un côté, 1/32D de l'autre."),
            ("Où est la grille adaptative de la version 1.0 ?",
             "Elle a été retirée en 1.1 pour garder un outil simple : la molette du Display change la taille."),
            ("J'utilisais Adaptive Grid / Gridbox.",
             "Les réglages sont repris. Retirer leurs actions des raccourcis et ne plus les lancer en même temps."),
        ]),
    ],
}

T["en"] = {
    "file": "GridBuddy_manual_EN.pdf",
    "sub": "The grid of the arrange view and the MIDI editor, at a glance",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "GridBuddy_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing",
    "head2": ("Item", "Effect"),
    "head_g": ("Gesture", "Effect"),
    "zoom": ("zoom out: wider grid", "zoom in: finer grid"),
    "body": [
        ("h1", "1. What it does"),
        ("p", "Grid Buddy gathers the settings of the REAPER grid, in the arrange view and in the MIDI editor: the "
              "<b>type</b> (straight, triplet, quintuplet, septuplet, dotted, swing), the <b>size</b> (1/128 to 4), "
              "snap and the <b>link</b> between the arrange grid and the MIDI editor grid."),
        ("p", "It has a window with two tabs (Grid and Set up), two small independent <b>Displays</b> "
              "(arrange view and MIDI editor) where the mouse wheel changes the grid size, and <b>isolated actions</b> for your shortcuts. It is "
              "based on the ideas of Gridbox by FeedTheCat."),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « Grid Buddy », right-click &gt; Install, "
                "then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drop it into REAPER. The MIDI editor actions "
              "are added the first time Grid Buddy runs. No automatic updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Copy the <b>GridBuddy</b> folder into the REAPER Scripts folder, then load and run "
              "<b>ReNo Mellow - Grid Buddy.lua</b>: it adds both Displays and every action itself "
              "(Main and MIDI Editor sections)."),
        ("p", "The settings of Adaptive Grid / Gridbox are imported the first time. Do not run them at the same "
              "time as Grid Buddy."),
        ("h1", "3. First steps"),
        ("ol", ["Run the action <b>ReNo Mellow - Grid Buddy</b> (toolbar icon <b>ReNo_GridBuddy</b>, lit while the "
                "window is open).",
                "In the <b>Grid</b> tab, Arrange view section, click <b>1/16</b>: the grid goes to sixteenth notes.",
                "Click <b>Triplet</b>: the grid becomes 1/16T, same size.",
                "In the MIDI editor section, tick <b>Link MIDI editor to the arrange grid</b>: the MIDI editor "
                "follows the arrange grid.",
                "In the Set up tab, <b>Show</b> opens the arrange Display or the MIDI Display; the mouse wheel over it "
                "changes the size."]),
        ("h1", "4. Grid tab"),
        ("draw", "grid"),
        ("p", "Two sections: <b>Arrange view</b> and <b>MIDI editor</b>. The current grid is written in large letters "
              "(e.g. 1/16T)."),
        ("table2", [
            ("Type", "Straight, Triplet, Quintuplet and Septuplet (if shown), Dotted, Swing. The size stays the same: "
                     "1/8 becomes 1/8T, 1/8D..."),
            ("Swing", "Slider from -100 to 100 % when swing is on (arrange view). In the MIDI editor, set the amount "
                      "in REAPER's grid settings."),
            ("Size", "Frame and Measure (if shown), then 1/128 to 4. The current type is kept."),
            ("- / +", "Narrower / wider grid: divided or multiplied by the grid divisor."),
            ("Snap", "Snap on/off; in the arrange view also Relative (relative grid snap) and Snap/grid settings..."),
            ("Link MIDI editor to the arrange grid", "MIDI editor section: turns REAPER's option « Use the same grid "
                     "division in arrange view and MIDI editor » on or off (see section 6)."),
        ]),
        ("h1", "5. Set up tab"),
        ("p", "Settings of the grid and the Display."),
        ("table2", [
            ("Grid divisor", "Step of the - / + buttons, the mouse wheel and the Wider / Narrower actions. 2 by "
                             "default (1/8 -&gt; 1/16); 3 gives 1/4 -&gt; 1/12..."),
            ("Min size / Max size", "Limits of - / +; for the mouse wheel: finest and widest straight sizes before the "
                                    "triplets / dotted sizes (empty = 1/128 and 4). E.g. 1/128, 1/8T, 1D, 2."),
            ("Preserve grid type per size", "The project remembers the type (triplet, swing...) used for each size."),
            ("Show", "Quintuplet, Septuplet buttons and menu entries; Frame, Measure buttons."),
            ("Reverse mouse wheel", "Reverses the wheel (Displays and mousewheel action)."),
            ("Wheel sensitivity", "Displays: wheel notches per size change, 1 to 4 (1.5 by default = 2 steps for 3 "
                                  "notches). Higher = slower."),
            ("Displays", "One row per Display (Arrange, MIDI): Show / Hide, text size, Snap button; for the arrange "
                         "view also Swing bar and Visible grid."),
            ("Window", "Text size of the window."),
        ]),
        ("p", "The divisor and the limits exist twice, for the arrange view and the MIDI editor. A refused value is "
              "shown in red under the fields."),
        ("h1", "6. Linking the MIDI editor"),
        ("p", "<b>Linked</b>: the MIDI editor uses the arrange grid. The MIDI editor section is greyed out with "
              "« LINKED to the arrange grid », the MIDI Display shows « MIDI = » in green and the « Grid Buddy MIDI » "
              "actions change the arrange grid."),
        ("p", "<b>Not linked</b>: the MIDI editor has its own grid, set in the MIDI editor section, with the MIDI "
              "Display or with the « Grid Buddy MIDI » actions."),
        ("p", "Change the link in the window (Link MIDI editor box) or in the Displays' menu. It is REAPER's own option: "
              "it stays on even when Grid Buddy is closed."),
        ("h1", "7. The Displays"),
        ("p", "Two small independent windows without a title bar, to place anywhere: the arrange <b>Display</b> "
              "(Main action) and the <b>MIDI Display</b> (action « Grid Buddy MIDI - Display », shown only while a "
              "MIDI editor is open). Each shows the snap magnet and the grid (blue bar for the swing in the arrange "
              "view)."),
        ("draw", "display"),
        ("table_g", [
            ("Wheel", "Next size (up = finer). Past the finest come 1/8T, 1/16T, 1/32T; past the widest "
                      "1/2D, 1/4D, 1/8D, 1/16D, 1/32D (see below)."),
            ("Click on the grid", "Menu: Straight, Triplet, Quintuplet / Septuplet (if shown), Dotted, Swing, then "
                                  "Frame and Measure (arrange view), Hide grid (hides the grid lines), Link MIDI "
                                  "editor; MIDI Display: also Sync to arrange view (action 40640)."),
            ("Alt+click", "Swing on/off (arrange view)."),
            ("Alt+wheel", "Swing amount in steps of 3 % (Ctrl+Alt: 1 %), arrange view."),
            ("Click on the magnet", "Snap on/off. Alt+click: relative snap (arrange view). Right-click: snap/grid settings."),
            ("Right-click on the grid", "Opens the Grid Buddy window."),
            ("Drag", "Move the Display."),
            ("Run the Display action again", "Close that Display."),
        ]),
        ("p", "<b>Wheel ladder</b> (Displays and Adjust grid action): 1/32T · 1/16T · 1/8T · 1/128 · 1/64 · 1/32 · "
              "1/16 · 1/8 · 1/4 · 1/2 · 1 · 2 · 4 · 1/2D · 1/4D · 1/8D · 1/16D · 1/32D. It stops at both ends. A "
              "grid off the ladder (1/4T, quintuplet...) first goes back to its straight size. Swing is kept on "
              "straight sizes."),
        ("p", "Hidden grid: the Display shows « Hidden »; the wheel or a type shows it again. An open Display reopens at the same place when REAPER starts (a small block is added to "
              "Scripts/__startup.lua). The Visible grid option shows the grid REAPER really draws at this zoom "
              "(straight sizes only)."),
        ("h1", "8. Actions"),
        ("p", "Every action exists in the <b>Main</b> section (« ReNo Mellow - Grid Buddy - ... ») and in the "
              "<b>MIDI Editor</b> section (« ReNo Mellow - Grid Buddy MIDI - ... »)."),
        ("table2", [
            ("ReNo Mellow - Grid Buddy", "Main window (run again = close)."),
            ("... - Display / ... MIDI - Display", "Opens or closes the arrange / MIDI editor Display."),
            ("Adjust grid (mousewheel)", "Bind it to a wheel: same ladder as the Displays."),
            ("Wider grid / Narrower grid", "Wider / narrower grid by one step (divisor)."),
            ("Toggle swing", "Swing on/off."),
        ]),
        ("p", "Assign these actions to a keyboard shortcut, a mouse wheel (e.g. Ctrl+wheel) or a MIDI control in the "
              "action list. Pick any shortcuts you like: the ones in this manual are examples."),
        ("h1", "9. FAQ"),
        ("p", "The most common cases."),
        ("qa", [
            ("The MIDI editor section is greyed out.",
             "Either no MIDI editor is open, or the MIDI editor is linked to the arrange view (Link MIDI editor box)."),
            ("The mouse wheel stops.", "It is at an end of the ladder: 1/32T on one side, 1/32D on the other."),
            ("Where is the adaptive grid of version 1.0?",
             "It was removed in 1.1 to keep the tool simple: the Display's mouse wheel changes the size."),
            ("I used Adaptive Grid / Gridbox.",
             "Their settings are imported. Remove their actions from your shortcuts and do not run them at the same time."),
        ]),
    ],
}

# ------------------------------------------------------------------ drawings (simplified, not screenshots)
BTN = colors.HexColor("#3A3D42")
ON = colors.HexColor("#3F7FC9")
TXT = colors.HexColor("#E8E8E8")
MUT = colors.HexColor("#9A9A9A")
GREEN = colors.HexColor("#7CF0A6")


def buttons(d, x, y, labels, on=(), h=5 * mm, fs=6.5):
    for lab in labels:
        w = max(8 * mm, len(lab) * fs * 0.62 + 4 * mm)
        d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=ON if lab in on else BTN, strokeColor=None))
        d.add(String(x + w / 2, y + h / 2 - fs * 0.35, lab, fontName="DV", fontSize=fs, fillColor=TXT,
                     textAnchor="middle"))
        x += w + 1.2 * mm
    return x


def d_grid():
    W, H = 174 * mm, 46 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    d.add(String(8, H - 12, "Grid   Set up", fontName="DVB", fontSize=8, fillColor=colors.white))
    d.add(String(8, H - 24, "Arrange view", fontName="DV", fontSize=7, fillColor=MUT))
    d.add(Line(8 + 50, H - 22, W - 8, H - 22, strokeColor=colors.HexColor("#45474C"), strokeWidth=0.6))
    d.add(String(8, H - 42, "1/16T", fontName="DVB", fontSize=17, fillColor=TXT))
    rows = [("Type", ["Straight", "Triplet", "Dotted", "Swing"], ["Triplet"]),
            ("Size", ["1/128", "1/64", "1/32", "1/16", "1/8", "1/4", "1/2", "1", "2", "4", "-", "+"], ["1/16"]),
            ("Snap", ["Snap", "Relative", "Snap/grid settings..."], ["Snap"])]
    y = H - 62
    for lab, items, on in rows:
        d.add(String(8, y + 4, lab, fontName="DV", fontSize=7, fillColor=MUT))
        buttons(d, 26 * mm, y + 1, items, on)
        y -= 7.2 * mm
    d.add(String(8, 4, "MIDI editor   [x] Link MIDI editor to the arrange grid   (same rows)", fontName="DV", fontSize=7, fillColor=MUT))
    return d


def magnet(d, x, y, s, col):
    from reportlab.graphics.shapes import ArcPath
    cx, cy, r = x + s * 0.45, y + s / 2, s * 0.26
    p = ArcPath(strokeColor=col, strokeWidth=s * 0.13, fillColor=None)
    p.addArc(cx, cy, r, 90, 270)
    d.add(p)
    d.add(Line(cx, cy + r, cx + s * 0.38, cy + r, strokeColor=col, strokeWidth=s * 0.13))
    d.add(Line(cx, cy - r, cx + s * 0.38, cy - r, strokeColor=col, strokeWidth=s * 0.13))


def d_display():
    W, H = 150 * mm, 14 * mm
    d = Drawing(W, H)
    for k, (txt, pre) in enumerate((("1/16T", ""), ("1/32", "MIDI "))):
        x0 = k * 78 * mm
        w = 56 * mm
        d.add(Rect(x0, 0, w, H, rx=5, ry=5, fillColor=DARK, strokeColor=None))
        magnet(d, x0 + 2 * mm, 1.5 * mm, 11 * mm, colors.HexColor("#4FA3E8"))
        d.add(Line(x0 + 15 * mm, 2.5 * mm, x0 + 15 * mm, H - 2.5 * mm, strokeColor=colors.HexColor("#45474C"),
                   strokeWidth=0.8))
        if pre:
            d.add(String(x0 + 21 * mm, 5.2 * mm, pre, fontName="DV", fontSize=9, fillColor=MUT))
        d.add(String(x0 + (32 if pre else 24) * mm, 5.2 * mm, txt, fontName="DVB", fontSize=10, fillColor=TXT))
        if not pre:
            d.add(Rect(x0 + 37 * mm, 3.8 * mm, 8 * mm, 0.9 * mm, fillColor=colors.HexColor("#4FA3E8"), strokeColor=None))
    return d


def d_zoom(lang):
    lab = T[lang]["zoom"]
    W, H = 170 * mm, 30 * mm
    d = Drawing(W, H)
    for k, (n, txt) in enumerate(((4, lab[0]), (16, lab[1]))):
        x0 = 6 * mm + k * 88 * mm
        w = 76 * mm
        d.add(Rect(x0, 8 * mm, w, 16 * mm, fillColor=colors.HexColor("#F4F6F8"), strokeColor=colors.HexColor("#C9CED4")))
        for i in range(n + 1):
            x = x0 + w * i / n
            d.add(Line(x, 8 * mm, x, 24 * mm, strokeColor=ACCENT if i % (n // 4 or 1) == 0 else colors.HexColor("#9DB7D8"),
                       strokeWidth=1.2 if i % (n // 4 or 1) == 0 else 0.6))
        d.add(String(x0 + w / 2, 3 * mm, txt, fontName="DV", fontSize=8, fillColor=DARK, textAnchor="middle"))
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
              Spacer(1, 8 * mm), Image(os.path.join(HERE, "ReNo_GridBuddy.png"), width=54 * mm, height=18 * mm),
              Spacer(1, 8 * mm), Paragraph(t["other"], S["center"]), Spacer(1, 3 * mm),
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
        dr = {"grid": d_grid, "display": d_display}.get(val)
        dw = dr() if dr else d_zoom(lang)
        return [KeepTogether([dw, Paragraph(t["cap"], S["cap"])])]
    return []


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
