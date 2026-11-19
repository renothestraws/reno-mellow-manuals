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

VERSION = "1.0"
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
    "sub": "La grille de l'arrangement et de l'éditeur MIDI : fixe ou adaptative au zoom",
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
        ("p", "Grid Buddy rassemble tout ce qui touche à la grille de REAPER, dans l'arrangement et dans l'éditeur "
              "MIDI : le <b>type</b> (straight, triplet, quintolet, septolet, pointé, swing), la <b>taille fixe</b> "
              "(1/128 à 4) et la <b>grille adaptative</b>, qui change de taille toute seule quand on zoome pour garder "
              "un écart confortable entre les lignes."),
        ("p", "Il comprend une fenêtre à deux onglets (Grid et Set up), un petit <b>Display</b> à placer près du "
              "transport, un <b>service</b> de fond pour la grille adaptative et des <b>actions isolées</b> à associer "
              "à des raccourcis. Il reprend les idées d'Adaptive Grid et de Gridbox de FeedTheCat."),
        ("draw", "zoom"),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER. <b>js_ReaScriptAPI</b> est "
              "conseillée pour la grille adaptative de l'éditeur MIDI."),
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
              "<b>ReNo Mellow - Grid Buddy.lua</b> : il ajoute lui-même le Display, le service et toutes les actions "
              "(sections Main et MIDI Editor)."),
        ("p", "Les réglages d'Adaptive Grid sont repris au premier lancement. Ne pas faire tourner Adaptive Grid ou "
              "Gridbox en même temps que Grid Buddy."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Lancer l'action <b>ReNo Mellow - Grid Buddy</b> (icône de barre d'outils <b>ReNo_GridBuddy</b>, "
                "allumée tant que la fenêtre est ouverte).",
                "Dans l'onglet <b>Grid</b>, section Arrange view, cliquer <b>1/16</b> : la grille est fixe à la double croche.",
                "Cliquer <b>Triplet</b> : la grille devient 1/16T, à la même taille.",
                "Cliquer <b>Medium</b> sur la ligne Adaptive, puis zoomer : la grille suit le zoom.",
                "Recliquer <b>Medium</b> (ou <b>Off</b>) pour revenir à une grille fixe.",
                "Dans l'onglet Set up, <b>Show Display</b> ouvre le petit Display."]),
        ("h1", "4. Onglet Grid"),
        ("p", "Deux sections identiques : <b>Arrange view</b> et <b>MIDI editor</b>. La grille en cours est écrite en "
              "grand (ex. 1/16T), avec « ADAPTIVE Medium » quand la grille suit le zoom."),
        ("draw", "grid"),
        ("table2", [
            ("Type", "Straight, Triplet, Quintuplet et Septuplet (si affichés), Dotted, Swing. La taille reste la "
                     "même : 1/8 devient 1/8T, 1/8D..."),
            ("Swing", "Curseur de -100 à 100 % quand le swing est actif (arrangement). Dans l'éditeur MIDI, la "
                      "quantité se règle dans les réglages de grille de REAPER."),
            ("Fixed", "Frame et Measure (si affichés), puis 1/128 à 4. Le type en cours est gardé. Choisir une taille "
                      "fixe coupe la grille adaptative."),
            ("- / +", "Grille plus étroite / plus large : divisée ou multipliée par le diviseur, ou taille adaptative "
                      "voisine quand la grille est adaptative."),
            ("Adaptive", "Off (grille fixe), Narrowest, Narrow, Medium, Wide, Widest ou Custom (écart en pixels "
                         "choisi dans Set up). Recliquer le mode actif revient à Off. Réglable même sans éditeur MIDI ouvert."),
            ("Snap", "Snap on/off ; dans l'arrangement aussi Relative (snap relatif) et Snap/grid settings..."),
        ]),
        ("p", "Si l'option de REAPER « Use the same grid division in arrange view and MIDI editor » est active, un "
              "message le rappelle : l'éditeur MIDI suit alors la grille de l'arrangement."),
        ("h1", "5. Onglet Set up"),
        ("p", "Les réglages de la grille, du service et du Display."),
        ("table2", [
            ("Custom size (px)", "Pour le mode Custom : écart minimum entre deux lignes de grille, en pixels."),
            ("Grid divisor", "Pas des boutons - / +, de la molette et de la grille adaptative. 2 par défaut "
                             "(1/8 -&gt; 1/16) ; 3 donne 1/4 -&gt; 1/12..."),
            ("Min size / Max size", "Limites de la grille : 1/128, 1/8T, 1D, 2... Vide = pas de limite. "
                                    "Valables pour la molette et la grille adaptative."),
            ("Preserve grid type per size", "Le projet retient le type (triplet, swing...) utilisé pour chaque taille."),
            ("Show", "Boutons et entrées de menu Quintuplet, Septuplet, Frame, Measure."),
            ("Reverse mouse wheel", "Inverse le sens de la molette (Display et actions mousewheel)."),
            ("Adaptive service", "État du service. « Keep the adaptive mode when REAPER restarts » le relance avec "
                                 "REAPER ; sinon les grilles repassent en fixe au démarrage."),
            ("Display", "Show / Hide Display, taille du texte, Snap button, Swing bar, MIDI editor grid, Visible grid."),
            ("Window", "Taille du texte de la fenêtre."),
        ]),
        ("p", "Ces réglages existent deux fois, pour l'arrangement et pour l'éditeur MIDI. Une valeur refusée est "
              "signalée en rouge sous les champs."),
        ("h1", "6. La grille adaptative"),
        ("p", "La grille adaptative choisit la taille la plus fine dont les lignes restent à un écart minimum. Cet "
              "écart part du réglage de REAPER « minimum grid line spacing » (8 px par défaut) : Narrowest l'utilise "
              "tel quel, Narrow le double, Medium le triple, Wide le quadruple, Widest le multiplie par 6 ; Custom "
              "utilise la valeur de Set up. Dans l'éditeur MIDI, l'écart de base est de 15 px."),
        ("p", "Un petit <b>service</b> de fond (action <b>... - Service</b>, allumée tant qu'il tourne) surveille le "
              "zoom. Il démarre tout seul quand un mode adaptatif est choisi et s'arrête quand les deux grilles sont "
              "fixes. Relancer l'action Service repasse les deux grilles en fixe."),
        ("h1", "7. Le Display"),
        ("p", "Petite fenêtre sans barre de titre, à placer où l'on veut (par exemple à côté du transport). Elle "
              "montre l'aimant du snap, la grille de l'arrangement (« A » en vert quand elle est adaptative, barre "
              "bleue pour le swing) et, quand un éditeur MIDI est ouvert, une deuxième ligne MIDI."),
        ("draw", "display"),
        ("table_g", [
            ("Clic sur la grille", "Menu : type, swing, tailles fixes, modes adaptatifs, sous-menu MIDI editor, "
                                  "Open Grid Buddy, Set up."),
            ("Molette", "Taille suivante (adaptative ou fixe). Molette vers le haut = plus fin."),
            ("Alt+clic", "Swing on/off."),
            ("Alt+molette", "Quantité de swing par pas de 3 % (Ctrl+Alt : 1 %). Tenir Alt affiche le swing."),
            ("Clic sur l'aimant", "Snap on/off. Alt+clic : snap relatif. Clic droit : réglages snap/grille."),
            ("Clic droit sur la grille", "Ouvre la fenêtre Grid Buddy."),
            ("Glisser", "Déplacer le Display."),
            ("Relancer l'action Display", "Fermer le Display."),
        ]),
        ("p", "Un Display ouvert se rouvre à sa place au démarrage de REAPER (un petit bloc est ajouté à "
              "Scripts/__startup.lua). L'option Visible grid affiche la grille que REAPER dessine vraiment à ce zoom "
              "(tailles straight seulement)."),
        ("h1", "8. Les actions"),
        ("p", "Toutes les actions existent dans la section <b>Main</b> (« ReNo Mellow - Grid Buddy - ... ») et dans "
              "la section <b>MIDI Editor</b> (« ReNo Mellow - Grid Buddy MIDI - ... »)."),
        ("table2", [
            ("ReNo Mellow - Grid Buddy", "Fenêtre principale (relancer = fermer)."),
            ("... - Display / ... - Service", "Ouvre ou ferme le Display / le service adaptatif."),
            ("Adaptive off (fixed)", "Grille fixe."),
            ("Adaptive narrowest ... widest, custom", "Choisit le mode ; relancer le mode actif = grille fixe. "
                                                       "L'icône reste allumée sur le mode actif."),
            ("Adjust grid (mousewheel)", "À associer à une molette : taille adaptative si la grille est adaptative, "
                                         "sinon taille fixe."),
            ("Adjust fixed grid (mousewheel)", "À associer à une molette : taille fixe (coupe le mode adaptatif)."),
            ("Wider grid / Narrower grid", "Grille plus large / plus étroite d'un pas."),
            ("Adapt grid to zoom", "Adapte une fois la grille au zoom (taille Medium si la grille est fixe)."),
            ("Toggle swing", "Swing on/off."),
        ]),
        ("p", "Ces actions s'associent à un raccourci clavier, une molette (ex. Ctrl+molette) ou une commande MIDI dans "
              "la liste d'actions. Les raccourcis sont à choisir librement : ceux de ce manuel sont des exemples."),
        ("h1", "9. Questions fréquentes"),
        ("qa", [
            ("La grille ne suit pas le zoom.",
             "Vérifier qu'un mode adaptatif est choisi, que les lignes de grille sont visibles et que la grille "
             "n'est pas sur Frame ou Measure. L'onglet Set up indique si le service tourne."),
            ("La grille adaptative de l'éditeur MIDI réagit avec un peu de retard.",
             "C'est voulu sous Windows : le service attend que la souris s'arrête pour ne pas bloquer les infobulles "
             "et la liste des canaux. Installer js_ReaScriptAPI améliore ce comportement."),
            ("Les boutons Type de l'éditeur MIDI sont grisés.", "Aucun éditeur MIDI n'est ouvert."),
            ("Après un redémarrage, la grille est revenue en fixe.",
             "Cocher « Keep the adaptive mode when REAPER restarts » dans Set up."),
            ("J'utilisais Adaptive Grid / Gridbox.",
             "Les réglages sont repris. Retirer leurs actions des raccourcis et ne plus les lancer en même temps."),
        ]),
    ],
}

T["en"] = {
    "file": "GridBuddy_manual_EN.pdf",
    "sub": "The grid of the arrange view and the MIDI editor: fixed or adaptive to the zoom",
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
        ("p", "Grid Buddy gathers everything about the REAPER grid, in the arrange view and in the MIDI editor: the "
              "<b>type</b> (straight, triplet, quintuplet, septuplet, dotted, swing), the <b>fixed size</b> (1/128 to "
              "4) and the <b>adaptive grid</b>, which changes size on its own when you zoom, to keep a comfortable "
              "distance between the lines."),
        ("p", "It has a window with two tabs (Grid and Set up), a small <b>Display</b> to place next to the transport, "
              "a background <b>service</b> for the adaptive grid and <b>isolated actions</b> for your shortcuts. It is "
              "based on the ideas of Adaptive Grid and Gridbox by FeedTheCat."),
        ("draw", "zoom"),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER. <b>js_ReaScriptAPI</b> is "
              "recommended for the adaptive grid of the MIDI editor."),
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
              "<b>ReNo Mellow - Grid Buddy.lua</b>: it adds the Display, the service and every action itself "
              "(Main and MIDI Editor sections)."),
        ("p", "The settings of Adaptive Grid are imported the first time. Do not run Adaptive Grid or Gridbox at the "
              "same time as Grid Buddy."),
        ("h1", "3. First steps"),
        ("ol", ["Run the action <b>ReNo Mellow - Grid Buddy</b> (toolbar icon <b>ReNo_GridBuddy</b>, lit while the "
                "window is open).",
                "In the <b>Grid</b> tab, Arrange view section, click <b>1/16</b>: the grid is fixed to sixteenth notes.",
                "Click <b>Triplet</b>: the grid becomes 1/16T, same size.",
                "Click <b>Medium</b> on the Adaptive row, then zoom: the grid follows the zoom.",
                "Click <b>Medium</b> again (or <b>Off</b>) to go back to a fixed grid.",
                "In the Set up tab, <b>Show Display</b> opens the small Display."]),
        ("h1", "4. Grid tab"),
        ("p", "Two identical sections: <b>Arrange view</b> and <b>MIDI editor</b>. The current grid is written in large "
              "letters (e.g. 1/16T), with « ADAPTIVE Medium » when the grid follows the zoom."),
        ("draw", "grid"),
        ("table2", [
            ("Type", "Straight, Triplet, Quintuplet and Septuplet (if shown), Dotted, Swing. The size stays the same: "
                     "1/8 becomes 1/8T, 1/8D..."),
            ("Swing", "Slider from -100 to 100 % when swing is on (arrange view). In the MIDI editor, set the amount "
                      "in REAPER's grid settings."),
            ("Fixed", "Frame and Measure (if shown), then 1/128 to 4. The current type is kept. Choosing a fixed size "
                      "switches the adaptive grid off."),
            ("- / +", "Narrower / wider grid: divided or multiplied by the grid divisor, or the next adaptive size "
                      "when the grid is adaptive."),
            ("Adaptive", "Off (fixed grid), Narrowest, Narrow, Medium, Wide, Widest or Custom (spacing in pixels set "
                         "in Set up). Clicking the active mode again goes back to Off. Works even with no MIDI editor open."),
            ("Snap", "Snap on/off; in the arrange view also Relative (relative grid snap) and Snap/grid settings..."),
        ]),
        ("p", "When REAPER's option « Use the same grid division in arrange view and MIDI editor » is on, a message "
              "says so: the MIDI editor then follows the arrange grid."),
        ("h1", "5. Set up tab"),
        ("p", "Settings of the grid, the service and the Display."),
        ("table2", [
            ("Custom size (px)", "For the Custom mode: smallest distance between two grid lines, in pixels."),
            ("Grid divisor", "Step of the - / + buttons, the mouse wheel and the adaptive grid. 2 by default "
                             "(1/8 -&gt; 1/16); 3 gives 1/4 -&gt; 1/12..."),
            ("Min size / Max size", "Grid limits: 1/128, 1/8T, 1D, 2... Empty = no limit. Used by the mouse wheel "
                                    "and the adaptive grid."),
            ("Preserve grid type per size", "The project remembers the type (triplet, swing...) used for each size."),
            ("Show", "Quintuplet, Septuplet, Frame, Measure buttons and menu entries."),
            ("Reverse mouse wheel", "Reverses the wheel (Display and mousewheel actions)."),
            ("Adaptive service", "Service state. « Keep the adaptive mode when REAPER restarts » starts it with "
                                 "REAPER; otherwise the grids go back to fixed at start-up."),
            ("Display", "Show / Hide Display, text size, Snap button, Swing bar, MIDI editor grid, Visible grid."),
            ("Window", "Text size of the window."),
        ]),
        ("p", "These settings exist twice, for the arrange view and the MIDI editor. A refused value is shown in red "
              "under the fields."),
        ("h1", "6. The adaptive grid"),
        ("p", "The adaptive grid picks the finest size whose lines stay at a minimum distance. That distance starts "
              "from REAPER's « minimum grid line spacing » (8 px by default): Narrowest uses it as it is, Narrow "
              "doubles it, Medium triples it, Wide multiplies it by 4, Widest by 6; Custom uses the Set up value. In "
              "the MIDI editor the base distance is 15 px."),
        ("p", "A small background <b>service</b> (action <b>... - Service</b>, lit while it runs) watches the zoom. "
              "It starts on its own when an adaptive mode is chosen and stops when both grids are fixed. Running the "
              "Service action again sets both grids to fixed."),
        ("h1", "7. The Display"),
        ("p", "Small window without a title bar, to place anywhere (next to the transport, for example). It shows the "
              "snap magnet, the arrange grid (green « A » when adaptive, blue bar for the swing) and, when a MIDI "
              "editor is open, a second MIDI line."),
        ("draw", "display"),
        ("table_g", [
            ("Click on the grid", "Menu: type, swing, fixed sizes, adaptive modes, MIDI editor submenu, Open Grid "
                                  "Buddy, Set up."),
            ("Wheel", "Next size (adaptive or fixed). Wheel up = finer."),
            ("Alt+click", "Swing on/off."),
            ("Alt+wheel", "Swing amount in steps of 3 % (Ctrl+Alt: 1 %). Holding Alt shows the swing."),
            ("Click on the magnet", "Snap on/off. Alt+click: relative snap. Right-click: snap/grid settings."),
            ("Right-click on the grid", "Opens the Grid Buddy window."),
            ("Drag", "Move the Display."),
            ("Run the Display action again", "Close the Display."),
        ]),
        ("p", "An open Display reopens at the same place when REAPER starts (a small block is added to "
              "Scripts/__startup.lua). The Visible grid option shows the grid REAPER really draws at this zoom "
              "(straight sizes only)."),
        ("h1", "8. Actions"),
        ("p", "Every action exists in the <b>Main</b> section (« ReNo Mellow - Grid Buddy - ... ») and in the "
              "<b>MIDI Editor</b> section (« ReNo Mellow - Grid Buddy MIDI - ... »)."),
        ("table2", [
            ("ReNo Mellow - Grid Buddy", "Main window (run again = close)."),
            ("... - Display / ... - Service", "Opens or closes the Display / the adaptive service."),
            ("Adaptive off (fixed)", "Fixed grid."),
            ("Adaptive narrowest ... widest, custom", "Chooses the mode; running the active mode again = fixed grid. "
                                                       "The icon stays lit on the active mode."),
            ("Adjust grid (mousewheel)", "Bind it to a wheel: adaptive size when the grid is adaptive, otherwise "
                                         "fixed size."),
            ("Adjust fixed grid (mousewheel)", "Bind it to a wheel: fixed size (switches the adaptive mode off)."),
            ("Wider grid / Narrower grid", "Wider / narrower grid by one step."),
            ("Adapt grid to zoom", "Adapts the grid to the zoom once (Medium size when the grid is fixed)."),
            ("Toggle swing", "Swing on/off."),
        ]),
        ("p", "Assign these actions to a keyboard shortcut, a mouse wheel (e.g. Ctrl+wheel) or a MIDI control in the "
              "action list. Pick any shortcuts you like: the ones in this manual are examples."),
        ("h1", "9. FAQ"),
        ("qa", [
            ("The grid does not follow the zoom.",
             "Check that an adaptive mode is chosen, that the grid lines are visible and that the grid is not set "
             "to Frame or Measure. The Set up tab shows whether the service is running."),
            ("The adaptive grid of the MIDI editor reacts a bit late.",
             "This is on purpose on Windows: the service waits for the mouse to stop so that tooltips and the channel "
             "list keep working. Installing js_ReaScriptAPI improves it."),
            ("The Type buttons of the MIDI editor are greyed out.", "No MIDI editor is open."),
            ("After a restart, the grid is fixed again.",
             "Tick « Keep the adaptive mode when REAPER restarts » in Set up."),
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
    W, H = 174 * mm, 53 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.HexColor("#1F2124"), strokeColor=None))
    d.add(String(8, H - 12, "Grid   Set up", fontName="DVB", fontSize=8, fillColor=colors.white))
    d.add(String(8, H - 24, "Arrange view", fontName="DV", fontSize=7, fillColor=MUT))
    d.add(Line(8 + 50, H - 22, W - 8, H - 22, strokeColor=colors.HexColor("#45474C"), strokeWidth=0.6))
    d.add(String(8, H - 42, "1/16T", fontName="DVB", fontSize=17, fillColor=TXT))
    d.add(String(32 * mm, H - 40, "ADAPTIVE  Medium", fontName="DV", fontSize=7.5, fillColor=GREEN))
    rows = [("Type", ["Straight", "Triplet", "Dotted", "Swing"], ["Triplet"]),
            ("Fixed", ["1/128", "1/64", "1/32", "1/16", "1/8", "1/4", "1/2", "1", "2", "4", "-", "+"], []),
            ("Adaptive", ["Off", "Narrowest", "Narrow", "Medium", "Wide", "Widest", "Custom"], ["Medium"]),
            ("Snap", ["Snap", "Relative", "Snap/grid settings..."], ["Snap"])]
    y = H - 62
    for lab, items, on in rows:
        d.add(String(8, y + 4, lab, fontName="DV", fontSize=7, fillColor=MUT))
        buttons(d, 26 * mm, y + 1, items, on)
        y -= 7.2 * mm
    d.add(String(8, 4, "MIDI editor   (same rows)", fontName="DV", fontSize=7, fillColor=MUT))
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
    W, H = 62 * mm, 17 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=5, ry=5, fillColor=DARK, strokeColor=None))
    magnet(d, 2 * mm, 2.5 * mm, 12 * mm, colors.HexColor("#4FA3E8"))
    d.add(Line(16 * mm, 3 * mm, 16 * mm, H - 3 * mm, strokeColor=colors.HexColor("#45474C"), strokeWidth=0.8))
    d.add(String(22 * mm, 9.5 * mm, "A", fontName="DVB", fontSize=10, fillColor=GREEN))
    d.add(String(27 * mm, 9.5 * mm, "1/16", fontName="DVB", fontSize=10, fillColor=TXT))
    d.add(Rect(39 * mm, 8.3 * mm, 8 * mm, 0.9 * mm, fillColor=colors.HexColor("#4FA3E8"), strokeColor=None))
    d.add(String(22 * mm, 3 * mm, "MIDI  1/32T", fontName="DV", fontSize=8, fillColor=MUT))
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
