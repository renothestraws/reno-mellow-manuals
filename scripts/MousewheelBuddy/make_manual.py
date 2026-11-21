# Generates the Mousewheel Buddy user manual, French and English
# (scripts/MousewheelBuddy/GridBuddy_manuel_FR.pdf and GridBuddy_manual_EN.pdf).
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
NAME = "ReNo Mellow - Mousewheel Buddy"
FOLDER = "MousewheelBuddy"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/MousewheelBuddy/"
URL_FR = BASE + "MousewheelBuddy_manuel_FR.pdf"
URL_EN = BASE + "MousewheelBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Mousewheel_Buddy.ReaperPkg"
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
MODS = ["Wheel", "Ctrl+Wheel", "Shift+Wheel", "Alt+Wheel", "Ctrl+Shift+Wheel", "Ctrl+Alt+Wheel",
        "Shift+Alt+Wheel", "Ctrl+Shift+Alt+Wheel"]
FILES = ["", " (Ctrl)", " (Shift)", " (Alt)", " (Ctrl+Shift)", " (Ctrl+Alt)", " (Shift+Alt)", " (Ctrl+Shift+Alt)"]

T = {}
T["fr"] = {
    "file": "MousewheelBuddy_manuel_FR.pdf",
    "sub": "Une molette qui sait où elle est",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "MousewheelBuddy_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié (pas une capture d'écran)",
    "head2": ("Élément", "Effet"),
    "head_a": ("Action (liste d'actions)", "Touches à tenir en l'assignant"),
    "head_z": ("Zone", "Molette vers le haut / vers le bas (actions de base)"),
    "head_m": ("Page", "Actions de base"),
    "zones_title": ("Arrange", "MIDI Editor"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "Dans REAPER, la molette de la souris fait toujours la même chose, où que soit la souris. "
              "<b>Mousewheel Buddy</b> lui donne de l'intelligence : l'action lancée dépend de la <b>zone survolée</b> "
              "(la règle, un item, une enveloppe, le mixer, le transport ; dans l'éditeur MIDI, la règle, les notes, "
              "les lignes de contrôleurs) et des <b>touches tenues</b> (aucune, Ctrl, Shift, Alt et leurs combinaisons)."),
        ("p", "Par exemple : la molette sur la règle zoome horizontalement, sur les pistes elle fait défiler la vue, "
              "et Ctrl + molette zoome verticalement. Tout se règle zone par zone, pour la molette vers le haut et vers "
              "le bas, dans une fenêtre de réglage."),
        ("p", "Le script fournit 8 actions molette pour l'arrangement (section Main de la liste d'actions) et 8 pour "
              "l'éditeur MIDI (section MIDI Editor), une par combinaison de touches, plus la fenêtre de réglage."),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER, l'extension <b>SWS</b> (sws-extension.org), qui permet de savoir ce qui se "
              "trouve sous la souris, et l'extension <b>ReaImGui</b> pour la fenêtre de réglage (Extensions &gt; "
              "ReaPack &gt; Browse packages &gt; ReaImGui, dans ReaTeam Extensions). Redémarrer REAPER après "
              "l'installation d'une extension."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « Mousewheel Buddy », clic droit &gt; "
                "Install, puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Les 8 actions "
              "de l'éditeur MIDI sont ajoutées au premier lancement de la fenêtre <b>ReNo Mellow - Mousewheel "
              "Buddy</b>. Pas de mise à jour automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Copier le dossier <b>MousewheelBuddy</b> dans le dossier Scripts de REAPER, charger "
              "<b>ReNo Mellow - Mousewheel Buddy.lua</b> et les actions <b>ReNo Mellow - Mousewheel Buddy - "
              "Wheel….lua</b> voulues dans la section Main, puis lancer la fenêtre : elle ajoute les actions MIDI."),
        ("h1", "3. Premiers pas"),
        ("ol", ["Ouvrir la liste d'actions (Actions &gt; Show action list), section <b>Main</b>.",
                "Sélectionner <b>ReNo Mellow - Mousewheel Buddy - Wheel</b>, cliquer <b>Add…</b> puis tourner la "
                "molette, sans toucher au clavier. La molette est maintenant gérée par Mousewheel Buddy.",
                "Tourner la molette au-dessus de la règle : la vue zoome horizontalement, autour de la souris. "
                "Au-dessus des pistes : la vue défile.",
                "Lancer <b>ReNo Mellow - Mousewheel Buddy</b> pour ouvrir la fenêtre de réglage et changer les "
                "actions de chaque zone.",
                "Faire de même, si on le souhaite, avec les autres combinaisons (Ctrl, Shift, Alt…) et avec les "
                "actions de la section <b>MIDI Editor</b>."]),
        ("p", "Les raccourcis montrés dans ce manuel sont des exemples : chacun choisit les combinaisons qu'il "
              "assigne. Une combinaison qui n'est pas assignée garde le comportement normal de REAPER."),
        ("h1", "4. Les actions molette"),
        ("p", "Chaque action porte dans son nom les touches à tenir en tournant la molette au moment de "
              "l'assigner (bouton Add… de la liste d'actions). Les noms des actions MIDI sont les mêmes avec "
              "« MIDI » : <b>ReNo Mellow - Mousewheel Buddy MIDI - Wheel (Ctrl)</b>…"),
        ("table_a", None),
        ("p", "<b>Sur Mac</b>, REAPER appelle Ctrl « Cmd » et Alt « Opt » : l'action « Wheel (Ctrl) » s'assigne à "
              "Cmd + molette, « Wheel (Alt) » à Opt + molette. La fenêtre de réglage affiche Cmd et Opt."),
        ("p", "Lancée sans la molette (bouton Run, menu, touche), une action molette ne fait rien."),
        ("h1", "5. La fenêtre de réglage"),
        ("draw", "setup"),
        ("p", "L'action <b>ReNo Mellow - Mousewheel Buddy</b> ouvre la fenêtre ; son bouton de barre d'outils est "
              "allumé tant qu'elle est ouverte, et la relancer la ferme. Trois onglets : <b>Arrange</b>, <b>MIDI "
              "Editor</b> et <b>Options</b>."),
        ("table2", [
            ("Invert wheel direction", "Inverse le sens de la molette pour tout l'onglet (toutes les pages)."),
            ("Reset this page", "Remet les actions de base de la page affichée (voir section 7)."),
            ("Horizontal / Vertical zoom center", "Centre des zooms lancés par la molette, prioritaire sur les "
                                                  "préférences (voir section 8)."),
            ("Last wheel event", "Ligne grise : la dernière molette reçue (touches, zone vue par SWS, action "
                                 "lancée). Utile pour régler et pour comprendre un problème."),
            ("Wheel, Ctrl+Wheel, Shift+Wheel…", "Une page par combinaison de touches. En tournant la molette, la "
                                                "page suit les touches tenues."),
            ("Mouse over", "Les zones. La zone survolée par la dernière molette est en vert."),
            ("Wheel up / Wheel down", "L'action de la zone, molette vers le haut et vers le bas : taper son ID "
                                      "(40138, _SWS_…, _RS…) ou cliquer <b>Pick…</b> pour la choisir dans la liste "
                                      "d'actions (puis Select). <b>x</b> = ne rien faire. Le nom de l'action "
                                      "s'affiche dessous ; « Unknown action » signale un ID inconnu."),
            ("Options", "Taille du texte, présence de SWS, actions MIDI enregistrées, rappel du mode d'emploi."),
        ]),
        ("h1", "6. Les zones"),
        ("draw", "zones"),
        ("p", "Mousewheel Buddy demande à SWS ce qui se trouve sous la souris au moment où la molette tourne."),
        ("table_z", [
            ("Arrange", None),
            ("Ruler / timeline", "Zoom horizontal avant / arrière"),
            ("Item", "Défilement vers le haut / vers le bas"),
            ("Envelope lane", "Défilement vers le haut / vers le bas"),
            ("Track lane (no item)", "Défilement vers le haut / vers le bas"),
            ("Empty area below tracks", "Défilement vers le haut / vers le bas"),
            ("Mixer (MCP)", "Rien"),
            ("Transport", "Défilement gauche / droite de 10 % (SWS)"),
            ("Other (scrollbars…)", "Zoom vertical avant / arrière"),
            ("MIDI Editor", None),
            ("Ruler / timeline", "Zoom horizontal avant / arrière"),
            ("Notes area", "Défilement vers le haut / vers le bas"),
            ("CC lanes", "Défilement gauche / droite"),
            ("Other (scrollbars…)", "Rien"),
        ]),
        ("p", "Le <b>panneau des pistes (TCP)</b> et le <b>clavier du piano roll</b> ne sont pas dans la liste : "
              "REAPER y gère la molette lui-même et ne lance pas les actions assignées à la molette."),
        ("h1", "7. Les combinaisons de touches"),
        ("p", "Chaque page a ses propres actions. Au départ, elles reprennent les habitudes de REAPER :"),
        ("table_m", [
            ("Wheel", "Les actions de base de la section 6."),
            ("Ctrl+Wheel (Cmd)", "Zoom vertical avant / arrière, dans toutes les zones."),
            ("Alt+Wheel (Opt)", "Défilement gauche / droite, dans toutes les zones."),
            ("Ctrl+Alt+Wheel", "Défilement vers le haut / vers le bas, dans toutes les zones."),
            ("Shift, Ctrl+Shift, Shift+Alt, Ctrl+Shift+Alt", "Vides : à remplir selon ses besoins."),
        ]),
        ("h1", "8. Le centre du zoom"),
        ("p", "Dans Préférences &gt; Zoom/Scroll/Offset, REAPER règle autour de quoi il zoome (curseur d'édition, "
              "centre de la vue, souris…). Mousewheel Buddy a son propre réglage, par onglet : pendant qu'une "
              "action molette s'exécute, il remplace celui des préférences, puis le rétablit aussitôt. Les "
              "raccourcis clavier et les menus gardent donc le réglage des préférences."),
        ("table2", [
            ("Horizontal zoom center", "Preferences (garder le réglage des préférences), Edit or play cursor, "
                                       "Edit cursor, Center of view, <b>Mouse cursor</b> (par défaut)."),
            ("Vertical zoom center", "Preferences, Track at view center, Top visible track, Last selected track, "
                                     "<b>Track under mouse</b> (par défaut)."),
        ]),
        ("h1", "9. Questions fréquentes"),
        ("qa", [
            ("Il ne se passe rien quand je tourne la molette.",
             "Vérifier que l'action est assignée à la molette dans la bonne section (Main pour l'arrangement, MIDI "
             "Editor pour l'éditeur MIDI) et avec les bonnes touches. Ouvrir la fenêtre de réglage : si la ligne "
             "« Last wheel event » ne bouge pas, l'action n'est pas lancée."),
            ("La molette ne fait rien sur le TCP ou sur le clavier du piano roll.",
             "C'est normal : REAPER gère la molette lui-même à ces endroits."),
            ("Une case affiche « Unknown action ».",
             "L'ID ne correspond à aucune action de cette section : extension manquante (SWS…), script supprimé ou "
             "ID d'une autre section. Le choisir avec Pick…"),
            ("Les actions MIDI n'apparaissent pas dans la section MIDI Editor.",
             "Après une installation par .ReaperPkg, lancer une fois la fenêtre de réglage : elle les ajoute. "
             "Sinon, onglet MIDI Editor, bouton <b>Add them</b>."),
            ("Un message demande d'installer SWS.",
             "Mousewheel Buddy a besoin de SWS pour savoir ce qui est sous la souris. L'installer puis redémarrer "
             "REAPER."),
        ]),
    ],
}

T["en"] = {
    "file": "MousewheelBuddy_manual_EN.pdf",
    "sub": "A mouse wheel that knows where it is",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "MousewheelBuddy_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing (not a screenshot)",
    "head2": ("Item", "Effect"),
    "head_a": ("Action (Action List)", "Keys to hold when binding it"),
    "head_z": ("Zone", "Wheel up / wheel down (default actions)"),
    "head_m": ("Page", "Default actions"),
    "zones_title": ("Arrange", "MIDI Editor"),
    "body": [
        ("h1", "1. What it does"),
        ("p", "In REAPER, the mouse wheel always does the same thing wherever the mouse is. <b>Mousewheel Buddy</b> "
              "makes it smarter: the action it runs depends on the <b>zone under the mouse</b> (the ruler, an item, "
              "an envelope, the mixer, the transport; in the MIDI editor, the ruler, the notes, the CC lanes) and on "
              "the <b>keys you hold</b> (none, Ctrl, Shift, Alt and their combinations)."),
        ("p", "For example: the wheel over the ruler zooms horizontally, over the tracks it scrolls the view, and "
              "Ctrl + wheel zooms vertically. Everything is set zone by zone, for wheel up and wheel down, in a "
              "setup window."),
        ("p", "The script provides 8 wheel actions for the arrange view (Main section of the Action List) and 8 for "
              "the MIDI editor (MIDI Editor section), one per key combination, plus the setup window."),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER, the <b>SWS</b> extension (sws-extension.org), which tells what is under "
              "the mouse, and the <b>ReaImGui</b> extension for the setup window (Extensions &gt; ReaPack &gt; "
              "Browse packages &gt; ReaImGui, in ReaTeam Extensions). Restart REAPER after installing an extension."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « Mousewheel Buddy », right-click &gt; "
                "Install, then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drag it into REAPER. The 8 MIDI editor "
              "actions are added the first time you open the <b>ReNo Mellow - Mousewheel Buddy</b> window. No "
              "automatic updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Copy the <b>MousewheelBuddy</b> folder into REAPER's Scripts folder, load <b>ReNo Mellow - "
              "Mousewheel Buddy.lua</b> and the <b>ReNo Mellow - Mousewheel Buddy - Wheel….lua</b> actions you "
              "want in the Main section, then open the window: it adds the MIDI actions."),
        ("h1", "3. Getting started"),
        ("ol", ["Open the Action List (Actions &gt; Show action list), <b>Main</b> section.",
                "Select <b>ReNo Mellow - Mousewheel Buddy - Wheel</b>, click <b>Add…</b> and turn the mouse wheel, "
                "without touching the keyboard. The wheel is now handled by Mousewheel Buddy.",
                "Turn the wheel over the ruler: the view zooms horizontally around the mouse. Over the tracks: the "
                "view scrolls.",
                "Run <b>ReNo Mellow - Mousewheel Buddy</b> to open the setup window and change the action of each "
                "zone.",
                "Do the same, if you like, with the other combinations (Ctrl, Shift, Alt…) and with the actions of "
                "the <b>MIDI Editor</b> section."]),
        ("p", "The shortcuts shown in this manual are examples: you choose the combinations you bind. A combination "
              "that is not bound keeps REAPER's normal behaviour."),
        ("h1", "4. The wheel actions"),
        ("p", "Each action has in its name the keys to hold while turning the wheel when you bind it (Add… button "
              "of the Action List). The MIDI action names are the same with « MIDI »: <b>ReNo Mellow - Mousewheel "
              "Buddy MIDI - Wheel (Ctrl)</b>…"),
        ("table_a", None),
        ("p", "<b>On macOS</b>, REAPER calls Ctrl « Cmd » and Alt « Opt »: « Wheel (Ctrl) » is bound to Cmd + wheel, "
              "« Wheel (Alt) » to Opt + wheel. The setup window shows Cmd and Opt."),
        ("p", "Run without the wheel (Run button, menu, key), a wheel action does nothing."),
        ("h1", "5. The setup window"),
        ("draw", "setup"),
        ("p", "The <b>ReNo Mellow - Mousewheel Buddy</b> action opens the window; its toolbar button is lit while it "
              "is open, and running it again closes it. Three tabs: <b>Arrange</b>, <b>MIDI Editor</b> and "
              "<b>Options</b>."),
        ("table2", [
            ("Invert wheel direction", "Reverses the wheel for the whole tab (all pages)."),
            ("Reset this page", "Restores the default actions of the page shown (see section 7)."),
            ("Horizontal / Vertical zoom center", "Center of the zooms run by the wheel, over the Preferences "
                                                  "(see section 8)."),
            ("Last wheel event", "Grey line: the last wheel turn received (keys, zone seen by SWS, action run). "
                                 "Handy to set things up and to understand a problem."),
            ("Wheel, Ctrl+Wheel, Shift+Wheel…", "One page per key combination. When you turn the wheel, the page "
                                                "follows the keys you hold."),
            ("Mouse over", "The zones. The zone under the last wheel turn is shown in green."),
            ("Wheel up / Wheel down", "The action of the zone, wheel up and wheel down: type its ID (40138, _SWS_…, "
                                      "_RS…) or click <b>Pick…</b> to choose it in the Action List (then Select). "
                                      "<b>x</b> = do nothing. The action name is shown below; « Unknown action » "
                                      "means the ID is not found."),
            ("Options", "Text size, SWS found or not, registered MIDI actions, short how-to."),
        ]),
        ("h1", "6. The zones"),
        ("draw", "zones"),
        ("p", "Mousewheel Buddy asks SWS what is under the mouse when the wheel turns."),
        ("table_z", [
            ("Arrange", None),
            ("Ruler / timeline", "Zoom in / out horizontally"),
            ("Item", "Scroll up / down"),
            ("Envelope lane", "Scroll up / down"),
            ("Track lane (no item)", "Scroll up / down"),
            ("Empty area below tracks", "Scroll up / down"),
            ("Mixer (MCP)", "Nothing"),
            ("Transport", "Scroll left / right by 10 % (SWS)"),
            ("Other (scrollbars…)", "Zoom in / out vertically"),
            ("MIDI Editor", None),
            ("Ruler / timeline", "Zoom in / out horizontally"),
            ("Notes area", "Scroll up / down"),
            ("CC lanes", "Scroll left / right"),
            ("Other (scrollbars…)", "Nothing"),
        ]),
        ("p", "The <b>track panel (TCP)</b> and the <b>piano roll keyboard</b> are not listed: REAPER handles the "
              "wheel there itself and does not run the actions bound to the wheel."),
        ("h1", "7. Key combinations"),
        ("p", "Each page has its own actions. By default they follow REAPER's habits:"),
        ("table_m", [
            ("Wheel", "The default actions of section 6."),
            ("Ctrl+Wheel (Cmd)", "Zoom in / out vertically, in every zone."),
            ("Alt+Wheel (Opt)", "Scroll left / right, in every zone."),
            ("Ctrl+Alt+Wheel", "Scroll up / down, in every zone."),
            ("Shift, Ctrl+Shift, Shift+Alt, Ctrl+Shift+Alt", "Empty: fill them as you need."),
        ]),
        ("h1", "8. Zoom center"),
        ("p", "In Preferences &gt; Zoom/Scroll/Offset, REAPER sets what it zooms around (edit cursor, center of view, "
              "mouse…). Mousewheel Buddy has its own setting, per tab: while a wheel action runs it replaces the "
              "preference, then restores it right away. Keyboard shortcuts and menus keep the preference."),
        ("table2", [
            ("Horizontal zoom center", "Preferences (keep the preference), Edit or play cursor, Edit cursor, "
                                       "Center of view, <b>Mouse cursor</b> (default)."),
            ("Vertical zoom center", "Preferences, Track at view center, Top visible track, Last selected track, "
                                     "<b>Track under mouse</b> (default)."),
        ]),
        ("h1", "9. FAQ"),
        ("qa", [
            ("Nothing happens when I turn the wheel.",
             "Check that the action is bound to the wheel in the right section (Main for the arrange view, MIDI "
             "Editor for the MIDI editor) and with the right keys. Open the setup window: if the « Last wheel "
             "event » line does not change, the action is not run."),
            ("The wheel does nothing special over the TCP or the piano roll keyboard.",
             "That is normal: REAPER handles the wheel there itself."),
            ("A field shows « Unknown action ».",
             "The ID matches no action of this section: missing extension (SWS…), deleted script or ID of another "
             "section. Choose it with Pick…"),
            ("The MIDI actions are not in the MIDI Editor section.",
             "After a .ReaperPkg installation, open the setup window once: it adds them. Otherwise, MIDI Editor tab, "
             "<b>Add them</b> button."),
            ("A message asks to install SWS.",
             "Mousewheel Buddy needs SWS to know what is under the mouse. Install it, then restart REAPER."),
        ]),
    ],
}


# ------------------------------------------------------------------ drawings (simplified, not screenshots)
BTN = colors.HexColor("#3A3D42")
ON = colors.HexColor("#2F7D4F")
TXT = colors.HexColor("#E8E8E8")
MUT = colors.HexColor("#9A9A9A")
GREEN = colors.HexColor("#7CF0A6")
BG = colors.HexColor("#1F2124")


def buttons(d, x, y, labels, on=(), h=5 * mm, fs=6.3):
    for lab in labels:
        w = max(8 * mm, len(lab) * fs * 0.6 + 3.5 * mm)
        d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=ON if lab in on else BTN, strokeColor=None))
        d.add(String(x + w / 2, y + h / 2 - fs * 0.35, lab, fontName="DV", fontSize=fs, fillColor=TXT,
                     textAnchor="middle"))
        x += w + 1.1 * mm
    return x


def d_setup(lang):
    W, H = 164 * mm, 62 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=BG, strokeColor=None))
    buttons(d, 6, H - 16, ["Arrange", "MIDI Editor", "Options"], on=("Arrange",))
    buttons(d, 6, H - 30, ["[ ] Invert wheel direction", "Reset this page"])
    buttons(d, 6, H - 44, ["Mouse cursor  v", "Horizontal zoom center", "Track under mouse  v", "Vertical zoom center"])
    d.add(String(6, H - 55, "Last wheel event: main wheel | val 15 ... | ruler / timeline / | ran 1012",
                 fontName="DV", fontSize=6.3, fillColor=MUT))
    buttons(d, 6, H - 72, ["Wheel", "Ctrl+Wheel", "Shift+Wheel", "Alt+Wheel", "Ctrl+Shift+Wheel", "Ctrl+Alt+Wheel",
                           "Shift+Alt+Wheel", "Ctrl+Shift+Alt+Wheel"], on=("Wheel",), fs=5.4)
    # table
    y0 = H - 84
    cols = (6, 44 * mm, 110 * mm)
    for i, txt in enumerate(("Mouse over", "Wheel up", "Wheel down")):
        d.add(String(cols[i] + 2, y0 - 3, txt, fontName="DVB", fontSize=6.5, fillColor=TXT))
    rows = [("Ruler / timeline", "1012", "View: Zoom in horizontal", "1011", "View: Zoom out horizontal", True),
            ("Item", "40138", "View: Scroll view up", "40139", "View: Scroll view down", False),
            ("Envelope lane", "40138", "View: Scroll view up", "40139", "View: Scroll view down", False)]
    y = y0 - 14
    for lab, a, an, b, bn, here in rows:
        if here:
            d.add(Rect(3, y - 11, W - 6, 19, fillColor=colors.HexColor("#24402F"), strokeColor=None))
        d.add(String(cols[0] + 2, y, lab, fontName="DV", fontSize=6.5, fillColor=GREEN if here else TXT))
        for x, idt, nm in ((cols[1], a, an), (cols[2], b, bn)):
            d.add(Rect(x, y - 2, 18 * mm, 4.4 * mm, fillColor=colors.HexColor("#2B3A55"), strokeColor=None))
            d.add(String(x + 2, y, idt, fontName="DV", fontSize=6.3, fillColor=TXT))
            buttons(d, x + 19.5 * mm, y - 2, ["Pick...", "x"], h=4.4 * mm, fs=5.6)
            d.add(String(x + 2, y - 8.5, nm, fontName="DV", fontSize=5.4, fillColor=MUT))
        y -= 24
    return d


def d_zones(lang):
    W, H = 164 * mm, 50 * mm
    d = Drawing(W, H)
    t1, t2 = T[lang]["zones_title"]
    # arrange
    x0, w = 0, 104 * mm
    d.add(String(x0, H - 6, t1, fontName="DVB", fontSize=8, fillColor=DARK))
    d.add(Rect(x0, H - 16, w, 6 * mm, fillColor=colors.HexColor("#DCE6F2"), strokeColor=GREY, strokeWidth=0.4))
    d.add(String(x0 + 30 * mm, H - 13, "Ruler / timeline", fontName="DV", fontSize=6.5, fillColor=DARK))
    d.add(Rect(x0, 10 * mm, 22 * mm, H - 26 - 10 * mm, fillColor=colors.HexColor("#E3E3E3"), strokeColor=GREY,
               strokeWidth=0.4))
    d.add(String(x0 + 11 * mm, 24 * mm, "TCP", fontName="DVB", fontSize=7, fillColor=GREY, textAnchor="middle"))
    d.add(String(x0 + 11 * mm, 20 * mm, "(REAPER)", fontName="DV", fontSize=5.5, fillColor=GREY, textAnchor="middle"))
    lanes = [("Track lane", None), ("Item", (30, 30)), ("Envelope lane", None)]
    yy = H - 24
    for lab, item in lanes:
        d.add(Rect(x0 + 22 * mm, yy - 8 * mm, w - 22 * mm, 8 * mm, fillColor=colors.white, strokeColor=GREY,
                   strokeWidth=0.4))
        if item:
            d.add(Rect(x0 + 40 * mm, yy - 7 * mm, 30 * mm, 6 * mm, fillColor=colors.HexColor("#9DB7D8"),
                       strokeColor=None))
        d.add(String(x0 + 24 * mm, yy - 5 * mm, lab, fontName="DV", fontSize=6.3, fillColor=DARK))
        yy -= 8 * mm
    d.add(String(x0 + 24 * mm, 12 * mm, "Empty area below tracks", fontName="DV", fontSize=6.3, fillColor=GREY))
    d.add(Rect(x0, 0, w, 6 * mm, fillColor=colors.HexColor("#DCE6F2"), strokeColor=GREY, strokeWidth=0.4))
    d.add(String(x0 + w / 2, 2 * mm, "Transport", fontName="DV", fontSize=6.5, fillColor=DARK, textAnchor="middle"))
    # midi
    x0, w = 106 * mm, 58 * mm
    d.add(String(x0, H - 6, t2, fontName="DVB", fontSize=8, fillColor=DARK))
    d.add(Rect(x0, H - 16, w, 6 * mm, fillColor=colors.HexColor("#DCE6F2"), strokeColor=GREY, strokeWidth=0.4))
    d.add(String(x0 + 14 * mm, H - 13, "Ruler / timeline", fontName="DV", fontSize=6.5, fillColor=DARK))
    d.add(Rect(x0, 16 * mm, 10 * mm, H - 16 - 16 * mm, fillColor=colors.HexColor("#E3E3E3"), strokeColor=GREY,
               strokeWidth=0.4))
    d.add(String(x0 + 5 * mm, 22 * mm, "keys", fontName="DV", fontSize=5.5, fillColor=GREY, textAnchor="middle"))
    d.add(Rect(x0 + 10 * mm, 16 * mm, w - 10 * mm, H - 16 - 16 * mm, fillColor=colors.white, strokeColor=GREY,
               strokeWidth=0.4))
    for k in range(4):
        d.add(Rect(x0 + (16 + k * 10) * mm, (20 + (k % 3) * 4) * mm, 7 * mm, 2.2 * mm,
                   fillColor=colors.HexColor("#9DB7D8"), strokeColor=None))
    d.add(String(x0 + 30 * mm, 33 * mm, "Notes area", fontName="DV", fontSize=6.3, fillColor=DARK))
    d.add(Rect(x0, 2 * mm, w, 13 * mm, fillColor=colors.HexColor("#F4F6F8"), strokeColor=GREY, strokeWidth=0.4))
    for k in range(10):
        d.add(Line(x0 + (14 + k * 4.5) * mm, 3 * mm, x0 + (14 + k * 4.5) * mm, (4 + (k * 7 % 9)) * mm,
                   strokeColor=ACCENT, strokeWidth=1.2))
    d.add(String(x0 + 2 * mm, 11 * mm, "CC lanes", fontName="DV", fontSize=6.3, fillColor=DARK))
    return d


def table_n(rows, head, w1=60):
    data = [[Paragraph(head[0], S["cellb"]), Paragraph(head[1], S["cellb"])]]
    style = [("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
             ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#D5D9DD")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for a, b in rows:
        if b is None:
            data.append([Paragraph("<font color='#2F6FB5'>%s</font>" % a, S["cellb"]), ""])
            style.append(("SPAN", (0, len(data) - 1), (1, len(data) - 1)))
        else:
            data.append([Paragraph(a, S["cellb"]), Paragraph(b, S["cell"])])
    t = Table(data, colWidths=[w1 * mm, (169 - w1) * mm], repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def actions_rows(lang):
    rows = []
    for m, f in zip(MODS, FILES):
        keys = m.replace("+Wheel", "").replace("Wheel", "")
        if lang == "fr":
            keys = (keys.replace("+", " + ") + " + molette") if keys else "molette seule"
        else:
            keys = (keys.replace("+", " + ") + " + wheel") if keys else "wheel only"
        rows.append(("ReNo Mellow - Mousewheel Buddy - Wheel" + f, keys))
    return rows

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
    t = Table(data, colWidths=[w1 * mm, (169 - w1) * mm], repeatRows=1)
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
                nxt = render(body[i + 1], lang)
                flat = []
                for f in nxt:  # a KeepTogether inside a KeepTogether always moves to the next page
                    flat += f._content if isinstance(f, KeepTogether) else [f]
                story.append(KeepTogether([head] + flat))
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
    if kind == "table_a":
        return [table_n(actions_rows(lang), t["head_a"], 92), Spacer(1, 4)]
    if kind == "table_z":
        return [table_n(val, t["head_z"], 50), Spacer(1, 4)]
    if kind == "table_m":
        return [table_n(val, t["head_m"], 62), Spacer(1, 4)]
    if kind == "qa":
        out = []
        for q, a in val:
            out.append(KeepTogether([Paragraph("<b>%s</b>" % q, S["p"]), Paragraph(a, S["p"])]))
        return out
    if kind == "draw":
        dw = {"setup": d_setup, "zones": d_zones}[val](lang)
        return [KeepTogether([dw, Paragraph(t["cap"], S["cap"])])]
    return []


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
