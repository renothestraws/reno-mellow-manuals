"""User manual (PDF, FR or EN) - ReNo Mellow Tool Buddy.

python3 make_manual.py <fr|en> <output.pdf> <ReNo_ToolBuddy.png>
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, Flowable, NextPageTemplate, PageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage

LANG, OUT, ICON = sys.argv[1], sys.argv[2], sys.argv[3]
VERSION = "1.11"
FR = LANG == "fr"
def L(fr, en): return fr if FR else en

REPO = "github.com/renothestraws/reno-mellow-script"
MANUALS = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/ToolBuddy/"
OTHER_URL = MANUALS + ("ToolBuddy_manual_EN.pdf" if FR else "ToolBuddy_manuel_FR.pdf")
PKG = "github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Tool_Buddy.ReaperPkg"
INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
for b in (0, 1):
    for i in (0, 1):
        addMapping("DV", b, i, "DVB" if b else "DV")

RED = colors.HexColor("#D63031")
DARK = colors.HexColor("#2B2D31")
GREY = colors.HexColor("#6B6F76")
LIGHT = colors.HexColor("#F2F3F5")
LINE = colors.HexColor("#D9DBDF")

st = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.5, spaceAfter=5),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, textColor=DARK, spaceBefore=4, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=RED, spaceBefore=8, spaceAfter=4),
    "bul": ParagraphStyle("bul", fontName="DV", fontSize=9.5, leading=13.5, leftIndent=12, bulletIndent=2, spaceAfter=2),
    "num": ParagraphStyle("num", fontName="DV", fontSize=9.5, leading=13.5, leftIndent=14, bulletIndent=0, spaceAfter=2),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.6, leading=11.5),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.6, leading=11.5),
    "note": ParagraphStyle("note", fontName="DV", fontSize=9, leading=12.5, textColor=DARK),
    "small": ParagraphStyle("small", fontName="DV", fontSize=8, leading=10.5, textColor=GREY),
    "toc1": ParagraphStyle("toc1", fontName="DV", fontSize=10, leading=16),
}

def P(t, s="body"): return Paragraph(t, st[s])
def B(items): return [Paragraph(i, st["bul"], bulletText="•") for i in items]
def N(items): return [Paragraph(i, st["num"], bulletText=f"{k}.") for k, i in enumerate(items, 1)]
def code(t): return f'<font name="DVM" size="8.6">{t}</font>'

def table(rows, widths, header=True):
    data = [[Paragraph(c, st["cellb"] if (header and r == 0) else st["cell"]) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header: style.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(style))
    return t

def note(text):
    t = Table([[Paragraph(text, st["note"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDF1F1")),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.5, RED),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t

# ---------------------------------------------------------------- icon (first state)
im = PILImage.open(ICON).convert("RGBA")
w, h = im.size
ICON_PNG = OUT + ".icon.png"
im.crop((0, 0, w // 3, h)).resize((120, 120), PILImage.LANCZOS).save(ICON_PNG)

# ---------------------------------------------------------------- drawings
class ToolboxMock(Flowable):
    def __init__(self, width=170 * mm, height=48 * mm):
        super().__init__(); self.width, self.height = width, height
    def draw(self):
        c = self.canv; W, H = self.width, self.height
        c.setFillColor(colors.HexColor("#1E1F22")); c.roundRect(0, 0, W, H, 4, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#2E4A7A")); c.rect(0, H - 14, W, 14, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("DVB", 8); c.drawString(8, H - 10, "Tool Buddy")
        c.setFillColor(colors.HexColor("#3B6FB6")); c.roundRect(8, H - 32, 34, 13, 2, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#3A3F45")); c.roundRect(45, H - 32, 36, 13, 2, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("DV", 7.5); c.drawString(14, H - 28, "Tools"); c.drawString(51, H - 28, "Setup")
        names = ["Split", "Nudge", "Glue", "Fade in", "Quantize", "Trim", "Reverse", "Normalize"]
        bw, bh, gap = (W - 16 - 3 * 6) / 4, 22, 6
        for k, n in enumerate(names):
            col, row = k % 4, k // 4
            x = 8 + col * (bw + gap); y = H - 62 - row * (bh + gap)
            fill = {"Split": "#2F7D4F", "Glue": "#B03A2E"}.get(n, "#3C4148")
            c.setFillColor(colors.HexColor(fill)); c.roundRect(x, y, bw, bh, 3, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont("DV", 8); c.drawCentredString(x + bw / 2, y + 8, n)
        c.setFillColor(colors.HexColor("#C9CCD1")); c.setFont("DV", 7.2)
        c.drawString(8, 22, "Current tool: Split")
        c.setFillColor(colors.HexColor("#9A9A9A"))
        c.drawString(8, 12, "Main: Split items at edit cursor    Alt: ... at time selection    Alt 2: ... at grid")
        c.setFillColor(colors.HexColor("#E05555")); c.drawString(8, 3, "ARMED: Glue (Main)   [Disarm]")

class BubbleMock(Flowable):
    def __init__(self, label="Split", midi=False):
        super().__init__(); self.label, self.midi = label, midi
        self.width, self.height = 62 * mm, 13 * mm
    def draw(self):
        c = self.canv; W, H = self.width, self.height
        c.setFillColor(DARK); c.roundRect(0, 0, W, H, 7, stroke=0, fill=1)
        c.drawImage(ICON_PNG, 6, (H - 26) / 2, 26, 26, mask="auto")
        x = 38
        if self.midi:
            c.setFillColor(colors.HexColor("#9A9A9A")); c.setFont("DV", 9); c.drawString(x, H / 2 - 3, "MIDI"); x += 30
        c.setStrokeColor(colors.HexColor("#55585E")); c.setLineWidth(1.2); c.line(x, 7, x, H - 7)
        c.setFillColor(colors.HexColor("#7CF0A6")); c.setFont("DVB", 12); c.drawString(x + 9, H / 2 - 4, self.label)

# ---------------------------------------------------------------- document
TITLE = L("Manuel d'utilisation", "User manual")

class Doc(BaseDocTemplate):
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name == "h1":
            self.notify("TOCEntry", (0, f.getPlainText(), self.page))

def on_page(c, d):
    c.saveState()
    c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    c.setFont("DV", 7.5); c.setFillColor(GREY)
    c.drawString(20 * mm, 10 * mm, f"ReNo Mellow - Tool Buddy {VERSION} - {TITLE}")
    c.drawRightString(190 * mm, 10 * mm, str(d.page))
    c.restoreState()

def cover(c, d):
    c.saveState()
    W, H = A4
    c.setFillColor(DARK); c.rect(0, H - 120 * mm, W, 120 * mm, stroke=0, fill=1)
    c.drawImage(ICON_PNG, 20 * mm, H - 62 * mm, 30 * mm, 30 * mm, mask="auto")
    c.setFillColor(colors.white); c.setFont("DVB", 26); c.drawString(20 * mm, H - 80 * mm, "Tool Buddy")
    c.setFont("DV", 13); c.setFillColor(colors.HexColor("#C9CCD1"))
    c.drawString(20 * mm, H - 90 * mm, L("Un même raccourci, plusieurs outils - pour REAPER",
                                         "One shortcut, many tools - for REAPER"))
    c.setFillColor(colors.HexColor("#7CF0A6")); c.setFont("DVB", 11)
    c.drawString(20 * mm, H - 104 * mm, f"{TITLE}  ·  version {VERSION}")
    c.setFillColor(colors.HexColor("#C9CCD1")); c.setFont("DV", 8.5)
    other = L("English version ›", "Version française ›")
    c.drawRightString(W - 20 * mm, H - 104 * mm, other)
    tw = c.stringWidth(other, "DV", 8.5)
    c.linkURL(OTHER_URL, (W - 20 * mm - tw, H - 106 * mm, W - 20 * mm, H - 100 * mm), relative=0)
    c.setFillColor(GREY); c.setFont("DV", 9)
    c.drawString(20 * mm, 20 * mm, "ReNo Mellow  ·  " + REPO + "  ·  " + L("novembre 2026", "November 2026"))
    c.restoreState()

doc = Doc(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=22 * mm,
          title=f"ReNo Mellow - Tool Buddy - {TITLE}", author="ReNo Mellow",
          subject=f"Tool Buddy {VERSION} for REAPER")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, A4[1] - 140 * mm, id="c")
doc.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=cover),
                      PageTemplate("normal", [frame], onPage=on_page)])

S = [NextPageTemplate("normal")]
S.append(P(L("Le Tool Buddy remplace les montages à base de cycle actions et d'exclusive toggles SWS : "
             "vous choisissez un <b>outil</b>, et les mêmes raccourcis clavier lancent l'action de cet outil. "
             "Changez d'outil, et le même raccourci fait autre chose.",
             "The Tool Buddy replaces setups built from SWS cycle actions and exclusive toggles: "
             "you pick a <b>tool</b>, and the same keyboard shortcuts run that tool's actions. "
             "Switch tools, and the same shortcut does something else.")))
S.append(P(L("<i>Tool Buddy s'appelait auparavant <b>Swiss Army Knife</b> : vos outils et réglages sont repris automatiquement "
             "au premier lancement. Réassignez simplement vos raccourcis aux nouvelles actions « Tool Buddy ».</i>",
             "<i>Tool Buddy was formerly called <b>Swiss Army Knife</b>: your tools and settings are carried over automatically "
             "on first launch. Just reassign your shortcuts to the new “Tool Buddy” actions.</i>"), "small"))
S.append(P(L(f'<link href="{OTHER_URL}" color="#D63031"><u>English version of this manual</u></link>',
             f'<link href="{OTHER_URL}" color="#D63031"><u>Version française de ce manuel</u></link>'), "small"))
S.append(Spacer(1, 4))
toc = TableOfContents(); toc.levelStyles = [st["toc1"]]
S.append(P(L("<b>Sommaire</b>", "<b>Contents</b>")))
S.append(toc)
S.append(PageBreak())

# 1 -----------------------------------------------------------------
S.append(P(L("1. Principe", "1. How it works"), "h1"))
S.append(P(L("Chaque <b>outil</b> porte un nom et jusqu'à trois actions REAPER : une action <b>principale</b>, une "
             "action <b>alt</b> et une action <b>alt 2</b>. Trois scripts, chacun sur le raccourci de votre choix, lancent "
             "l'action correspondante de l'outil actif (W, Shift+W et Ctrl+W ne sont que des exemples) :",
             "Each <b>tool</b> has a name and up to three REAPER actions: a <b>main</b> action, an <b>alt</b> action "
             "and an <b>alt 2</b> action. Three scripts, each on a shortcut of your choice, run the matching action "
             "of the active tool (W, Shift+W and Ctrl+W are only examples):")))
S.append(table([[L("Raccourci (exemple)", "Shortcut (example)"), "Script", L("Lance", "Runs")],
                ["W", "ReNo Mellow - Tool Buddy", L("l'action principale de l'outil actif", "the active tool's main action")],
                ["Shift+W", "ReNo Mellow - Tool Buddy (alt)", L("son action alt", "its alt action")],
                ["Ctrl+W", "ReNo Mellow - Tool Buddy (alt2)", L("son action alt 2", "its alt 2 action")]],
               [32 * mm, 72 * mm, 66 * mm]))
S.append(Spacer(1, 6))
S.append(P(L("Une action peut être une action native de REAPER, une action SWS, un script ou une custom action. "
             "Pour enchaîner plusieurs actions, créez une custom action dans l'Action List et affectez-la à l'outil.",
             "An action can be a native REAPER action, an SWS action, a script or a custom action. "
             "To chain several actions, create a custom action in the Action List and assign it to the tool.")))
S.append(P(L("Il existe <b>deux versions séparées</b>, avec chacune ses 24 outils, son outil actif et ses fenêtres :",
             "There are <b>two separate versions</b>, each with its own 24 tools, active tool and windows:")))
S += B([L("<b>Arrange</b> : pour la fenêtre d'arrangement, dans la section <b>Main</b> de l'Action List ;",
          "<b>Arrange</b>: for the arrange view, in the <b>Main</b> section of the Action List;"),
        L("<b>MIDI</b> : pour l'éditeur MIDI, dans la section <b>MIDI Editor</b> de l'Action List (scripts suffixés « MIDI »).",
          "<b>MIDI</b>: for the MIDI editor, in the <b>MIDI Editor</b> section of the Action List (scripts named “MIDI”).")])
S.append(P(L("Deux fenêtres servent à piloter le tout : la <b>Toolbox</b> (choisir et configurer les outils) et la "
             "<b>bulle Display</b> (voir l'outil actif et en changer, à placer où vous voulez).",
             "Two windows drive everything: the <b>Toolbox</b> (choose and set up tools) and the "
             "<b>Display bubble</b> (see and change the active tool, placed wherever you like).")))

# 2 -----------------------------------------------------------------
S.append(P("2. Installation", "h1"))
S.append(P(L("Prérequis", "Requirements"), "h2"))
S += B([L("REAPER 7 (7.86 ou plus pour l'installation par glisser-déposer, 7.03 ou plus pour les infobulles) ;",
          "REAPER 7 (7.86 or later for drag-and-drop install, 7.03 or later for tooltips);"),
        L("l'extension <b>ReaImGui</b>, obligatoire (Extensions > ReaPack > Browse packages > « ReaImGui », dépôt ReaTeam Extensions) ;",
          "the <b>ReaImGui</b> extension, required (Extensions > ReaPack > Browse packages > “ReaImGui”, ReaTeam Extensions repository);"),
        L("l'extension <b>SWS</b>, conseillée.", "the <b>SWS</b> extension, recommended.")])
S.append(P(L("Méthode 1 - ReaPack (mises à jour automatiques)", "Method 1 - ReaPack (automatic updates)"), "h2"))
S += N([L("Extensions > ReaPack > Import repositories, puis collez l'adresse : ", "Extensions > ReaPack > Import repositories, then paste: ")
        + code(INDEX) + L(" ;", ";"),
        L("Extensions > ReaPack > Browse packages, cherchez « Tool Buddy » et installez-le ;",
          "Extensions > ReaPack > Browse packages, search for “Tool Buddy” and install it;"),
        L("les scripts Arrange arrivent dans la section Main, les scripts MIDI dans la section MIDI Editor.",
          "Arrange scripts go to the Main section, MIDI scripts to the MIDI Editor section.")])
S.append(P(L("Méthode 2 - Paquet à glisser (REAPER 7.86+)", "Method 2 - Drag-and-drop package (REAPER 7.86+)"), "h2"))
S += N([L("téléchargez ", "download ") + code("ReNo_Mellow_Tool_Buddy.ReaperPkg") + " : " + code(PKG) + L(" ;", ";"),
        L("glissez le fichier dans la fenêtre de REAPER et confirmez ;", "drag the file onto the REAPER window and confirm;"),
        L("lancez une fois la Toolbox : elle ajoute la version MIDI à la section MIDI Editor.",
          "run the Toolbox once: it adds the MIDI version to the MIDI Editor section.")])
S.append(note(L("Avec le paquet .ReaperPkg, il n'y a pas de mise à jour automatique : téléchargez et glissez la nouvelle "
                "version quand elle sort. Avec ReaPack, faites simplement Extensions > ReaPack > Synchronize packages.",
                "The .ReaperPkg package does not update itself: download and drop the new version when it comes out. "
                "With ReaPack, simply use Extensions > ReaPack > Synchronize packages.")))

# 3 -----------------------------------------------------------------
S.append(P(L("3. Premiers pas", "3. Getting started"), "h1"))
S += N([L("Ouvrez l'Action List (touche ?) et lancez <b>ReNo Mellow - Tool Buddy - Toolbox</b>. "
          "Au premier lancement, elle crée un outil d'exemple, <b>Split</b>, et enregistre tous les scripts.",
          "Open the Action List (? key) and run <b>ReNo Mellow - Tool Buddy - Toolbox</b>. "
          "The first time, it creates a sample tool, <b>Split</b>, and registers all the scripts."),
        L("Toujours dans l'Action List, section <b>Main</b>, assignez un raccourci de votre choix à chacun des "
          "trois scripts. Dans ce manuel, nous utilisons <b>à titre d'exemple</b> W pour le script principal, "
          "Shift+W pour « (alt) » et Ctrl+W pour « (alt2) » : n'importe quelle touche ou combinaison convient.",
          "Still in the Action List, <b>Main</b> section, assign a shortcut of your choice to each of the three "
          "scripts. This manual uses W for the main script, Shift+W for “(alt)” and Ctrl+W for “(alt2)” "
          "<b>as examples only</b>: any key or combination works."),
        L("Sélectionnez un item et appuyez sur votre raccourci principal : l'item est coupé au curseur d'édition. "
          "Le raccourci alt coupe à la sélection temporelle, le raccourci alt 2 coupe sur la grille.",
          "Select an item and press your main shortcut: the item is split at the edit cursor. "
          "The alt shortcut splits at the time selection, the alt 2 shortcut splits at the grid."),
        L("Lancez <b>ReNo Mellow - Tool Buddy - Display</b> et placez la bulle près de votre transport.",
          "Run <b>ReNo Mellow - Tool Buddy - Display</b> and place the bubble near your transport.")])
S.append(Spacer(1, 4))
S.append(table([[L("Outil d'exemple", "Sample tool"), "Main", "Alt", "Alt 2"],
                ["Split (Arrange)", L("40012 - coupe au curseur d'édition", "40012 - split at edit cursor"),
                 L("40061 - coupe à la sélection temporelle", "40061 - split at time selection"),
                 L("40932 - coupe sur la grille", "40932 - split at grid")],
                ["Split (MIDI)", L("40046 - coupe les notes au curseur", "40046 - split notes at edit cursor"),
                 L("40052 - coupe sous la souris", "40052 - split notes at mouse cursor"),
                 L("40641 - coupe sur la grille", "40641 - split notes at grid")]],
               [30 * mm, 47 * mm, 47 * mm, 46 * mm]))

# 4 -----------------------------------------------------------------
S.append(KeepTogether([P(L("4. La Toolbox - onglet Tools", "4. The Toolbox - Tools tab"), "h1"),
    P(L("L'onglet Tools montre vos outils sous forme de grille. L'outil actif est en <b>vert</b>.",
        "The Tools tab shows your tools as a grid. The active tool is <b>green</b>.")), ToolboxMock()]))
S.append(Spacer(1, 6))
S.append(table([[L("Geste", "Gesture"), L("Effet", "Effect")],
                [L("Clic", "Click"), L("choisit l'outil actif", "selects the active tool")],
                [L("Clic droit", "Right-click"), L("<b>arme</b> l'action principale de l'outil (bouton rouge)",
                                                   "<b>arms</b> the tool's main action (red button)")],
                [L("Shift + clic droit", "Shift + right-click"), L("arme l'action alt (bouton orange)", "arms the alt action (orange button)")],
                [L("Ctrl + clic droit", "Ctrl + right-click"), L("arme l'action alt 2 (bouton violet)", "arms the alt 2 action (purple button)")],
                [L("Clic droit sur un outil armé", "Right-click on an armed tool"),
                 L("désarme (aussi : bouton Disarm sous la grille)", "disarms (also: Disarm button under the grid)")],
                [L("Survol d'un outil", "Hover over a tool"), L("affiche l'emplacement et les trois actions", "shows the slot and its three actions")]],
               [50 * mm, 120 * mm]))
S.append(Spacer(1, 5))
S.append(P(L("Armer une action fonctionne comme le clic droit sur un bouton de barre d'outils de REAPER : "
             "l'action reste armée et s'exécute à chaque clic dans l'arrangement (ou dans l'éditeur MIDI pour la "
             "version MIDI), jusqu'à ce que vous la désarmiez.",
             "Arming works like right-clicking a REAPER toolbar button: the action stays armed and runs on each "
             "click in the arrange view (or in the MIDI editor for the MIDI version) until you disarm it.")))
S.append(P(L("Sous la grille sont rappelés l'outil actif, ses trois actions et, en rouge, l'action armée.",
             "Under the grid you see the active tool, its three actions and, in red, the armed action.")))
S.append(note(L("Option : <b>Setup > Settings > Close the window after choosing a tool</b> ferme la Toolbox dès que "
                "vous cliquez sur un outil. Le clic droit (armement) ne la ferme pas.",
                "Option: <b>Setup > Settings > Close the window after choosing a tool</b> closes the Toolbox as soon "
                "as you click a tool. Right-click (arming) does not close it.")))

# 5 -----------------------------------------------------------------
S.append(P(L("5. La Toolbox - onglet Setup", "5. The Toolbox - Setup tab"), "h1"))
S.append(P(L("À gauche, la liste des 24 emplacements (l'outil actif est en vert). À droite, l'édition de "
             "l'emplacement sélectionné.",
             "On the left, the list of the 24 slots (the active tool is green). On the right, the editor of the "
             "selected slot.")))
S.append(P(L("Créer ou modifier un outil", "Create or edit a tool"), "h2"))
S += N([L("cliquez sur un emplacement vide (« - ») ;", "click an empty slot (“-”);"),
        L("tapez un <b>nom</b> : c'est lui qui apparaît dans la grille et dans la bulle ;",
          "type a <b>name</b>: it is shown in the grid and in the bubble;"),
        L("pour chaque action (<b>Main</b>, <b>Alt</b>, <b>Alt 2</b>), cliquez sur <b>Pick...</b> et choisissez "
          "l'action dans l'Action List, ou tapez son identifiant (",
          "for each action (<b>Main</b>, <b>Alt</b>, <b>Alt 2</b>), click <b>Pick...</b> and choose the action in "
          "the Action List, or type its ID (")
        + code("40012") + ", " + code("_SWS_...") + ", " + code("_RS...")
        + L(" pour un script, l'identifiant d'une custom action) ;", " for a script, a custom action's ID);"),
        L("le nom de l'action s'affiche en gris sous le champ ; « Action not found » en rouge signale un identifiant inconnu.",
          "the action name appears in grey under the field; a red “Action not found” means an unknown ID.")])
S.append(P(L("Une action laissée vide ne fait rien : par exemple, si un outil n'a pas d'action alt 2, le raccourci alt 2 est ignoré.",
             "An empty action does nothing: for example, if a tool has no alt 2 action, the alt 2 shortcut is ignored.")))
S.append(KeepTogether([P(L("Boutons de l'emplacement", "Slot buttons"), "h2"), table([
    [L("Bouton", "Button"), L("Effet", "Effect")],
    [L("Clear (à côté d'une action)", "Clear (next to an action)"), L("vide cette action", "clears that action")],
    ["Move up / Move down", L("déplace l'outil dans la liste (et dans la grille)", "moves the tool in the list (and in the grid)")],
    ["Duplicate", L("copie l'outil dans le premier emplacement libre", "copies the tool to the first free slot")],
    ["Clear slot", L("vide tout l'emplacement (avec confirmation)", "clears the whole slot (asks first)")]],
    [50 * mm, 120 * mm])]))
S.append(KeepTogether([P("Settings", "h2"), table([
    [L("Réglage", "Setting"), L("Effet", "Effect")],
    ["Tooltip when the tool changes", L("infobulle près de la souris quand l'outil change (Next / Previous tool)",
                                        "tooltip near the mouse when the tool changes (Next / Previous tool)")],
    ["Tooltip when a tool action is run", L("infobulle « Tool Buddy: nom de l'outil » à chaque utilisation d'un des trois raccourcis",
                                            "“Tool Buddy: tool name” tooltip each time one of the three shortcuts is used")],
    ["Tooltip duration", L("durée des infobulles (0,3 à 3 s)", "tooltip duration (0.3 to 3 s)")],
    ["Window text size", L("taille du texte de la fenêtre (10 à 20)", "window text size (10 to 20)")],
    ["Tool text size", L("taille du texte des boutons d'outils (10 à 28)", "tool button text size (10 to 28)")],
    ["Tool button height / min. width", L("hauteur et largeur minimale des boutons d'outils", "height and minimum width of tool buttons")],
    ["Default sizes", L("remet les tailles d'origine", "restores the original sizes")],
    ["Close the window after choosing a tool", L("ferme la Toolbox après le choix d'un outil", "closes the Toolbox after choosing a tool")]],
    [62 * mm, 108 * mm])]))
S.append(P(L("Les tailles et la fermeture automatique se règlent séparément pour la Toolbox Arrange et la Toolbox MIDI.",
             "Sizes and auto-close are set separately for the Arrange Toolbox and the MIDI Toolbox."), "small"))
S.append(P("Presets", "h2"))
S += B([L("<b>Export...</b> : enregistre les 24 outils dans un fichier texte (pratique pour sauvegarder ou partager) ;",
          "<b>Export...</b>: saves the 24 tools to a text file (handy to back up or share);"),
        L("<b>Import...</b> : remplace les 24 outils par ceux d'un fichier exporté ;",
          "<b>Import...</b>: replaces the 24 tools with those of an exported file;"),
        L("<b>Reset to defaults</b> : revient au seul outil Split d'exemple.",
          "<b>Reset to defaults</b>: goes back to the single sample Split tool.")])
S.append(P("Scripts", "h2"))
S.append(P(L("Indique combien de scripts sont présents dans l'Action List. <b>Register scripts again</b> les "
             "réenregistre si vous en avez retiré par erreur ou déplacé le dossier.",
             "Shows how many scripts are in the Action List. <b>Register scripts again</b> registers them again "
             "if you removed some by mistake or moved the folder.")))

# 6 -----------------------------------------------------------------
S.append(KeepTogether([P(L("6. La bulle Display", "6. The Display bubble"), "h1"),
    P(L("Une petite fenêtre sans barre de titre qui affiche l'outil actif. Placez-la où vous voulez, par "
        "exemple près des boutons de transport.",
        "A small window without a title bar that shows the active tool. Place it wherever you like, for "
        "example next to the transport buttons.")),
    BubbleMock("Split"), Spacer(1, 4), BubbleMock("Quantize", midi=True), Spacer(1, 6),
    table([[L("Geste", "Gesture"), L("Effet", "Effect")],
           [L("Glisser", "Drag"), L("déplace la bulle", "moves the bubble")],
           [L("Molette", "Mouse wheel"), L("outil précédent / suivant", "previous / next tool")],
           [L("Double-clic", "Double-click"), L("ouvre la Toolbox correspondante", "opens the matching Toolbox")],
           [L("Survol du nom de l'outil", "Hover over the tool name"), L("bulle avec les trois actions de l'outil (main, alt, alt2)", "tooltip with the tool's three actions (main, alt, alt2)")],
           [L("Survol du reste", "Hover elsewhere"), L("bulle d'aide avec ces gestes", "help tooltip listing these gestures")],
           [L("Clic droit", "Right-click"), L("menu : Open Toolbox, Next tool, Previous tool, Text size, Close",
                                              "menu: Open Toolbox, Next tool, Previous tool, Text size, Close")]],
          [40 * mm, 130 * mm])]))
S.append(Spacer(1, 5))
S += B([L("La bulle <b>retient sa place</b> et, si elle était ouverte à la fermeture de REAPER, <b>se rouvre "
          "toute seule</b> au démarrage suivant.",
          "The bubble <b>remembers its position</b> and, if it was open when REAPER was closed, <b>reopens by "
          "itself</b> at the next start."),
        L("Pour la fermer pour de bon : clic droit > <b>Close</b>, ou relancez son script (son bouton de barre "
          "d'outils fonctionne comme un interrupteur et reste allumé tant que la bulle est ouverte).",
          "To close it for good: right-click > <b>Close</b>, or run its script again (its toolbar button works "
          "as a switch and stays lit while the bubble is open)."),
        L("La bulle MIDI (« MIDI » à côté du couteau) n'apparaît que lorsqu'un éditeur MIDI est ouvert, et revient à "
          "sa place dès que vous en ouvrez un.",
          "The MIDI bubble (“MIDI” next to the knife) only shows while a MIDI editor is open, and comes back to its "
          "place as soon as you open one."),
        L("La bulle ne peut pas être dockée.", "The bubble cannot be docked.")])
S.append(note(L("Pour se rouvrir au démarrage, la bulle ajoute une fois un petit bloc balisé « ReNo Mellow Tool "
                "Buddy » au fichier <b>Scripts/__startup.lua</b> de REAPER. Le reste du fichier n'est pas modifié. "
                "Si vous désinstallez Tool Buddy, ce bloc ne fait plus rien ; vous pouvez aussi le supprimer à la main.",
                "To reopen at startup, the bubble adds, once, a small block marked “ReNo Mellow Tool Buddy” to "
                "REAPER's <b>Scripts/__startup.lua</b> file. The rest of the file is left untouched. If you uninstall "
                "the Tool Buddy, the block does nothing; you can also delete it by hand.")))

# 7 -----------------------------------------------------------------
S.append(P(L("7. Changer d'outil au clavier", "7. Changing tools from the keyboard"), "h1"))
S.append(P(L("Les scripts <b>Next tool</b> et <b>Previous tool</b> passent à l'outil suivant ou précédent (les "
             "emplacements vides sont sautés, la liste boucle). Assignez-les aux touches de votre choix ou à "
             "un contrôleur MIDI. Une infobulle indique le nouvel outil si l'option est activée.",
             "The <b>Next tool</b> and <b>Previous tool</b> scripts move to the next or previous tool (empty slots "
             "are skipped, the list wraps around). Assign them to keys of your choice or to a MIDI controller. "
             "A tooltip shows the new tool if the option is on.")))

# 8 -----------------------------------------------------------------
S.append(P(L("8. La version éditeur MIDI", "8. The MIDI editor version"), "h1"))
S.append(P(L("Elle fonctionne exactement comme la version Arrange, mais avec ses propres outils, son propre outil "
             "actif et ses propres fenêtres :",
             "It works exactly like the Arrange version, but with its own tools, active tool and windows:")))
S += N([L("dans l'éditeur MIDI, ouvrez l'Action List : la section <b>MIDI Editor</b> est sélectionnée ;",
          "in the MIDI editor, open the Action List: the <b>MIDI Editor</b> section is selected;"),
        L("lancez <b>ReNo Mellow - Tool Buddy MIDI - Toolbox</b> et créez vos outils MIDI (Pick... ouvre "
          "directement la section MIDI Editor) ;",
          "run <b>ReNo Mellow - Tool Buddy MIDI - Toolbox</b> and create your MIDI tools (Pick... opens "
          "the MIDI Editor section directly);"),
        L("assignez les raccourcis de votre choix (par exemple W, Shift+W et Ctrl+W) aux scripts "
          "<b>Tool Buddy MIDI</b>, <b>(alt)</b> et <b>(alt2)</b> ;",
          "assign shortcuts of your choice (for example W, Shift+W and Ctrl+W) to the "
          "<b>Tool Buddy MIDI</b>, <b>(alt)</b> and <b>(alt2)</b> scripts;"),
        L("lancez <b>Tool Buddy MIDI - Display</b> pour la bulle MIDI.",
          "run <b>Tool Buddy MIDI - Display</b> for the MIDI bubble.")])
S.append(P(L("Les raccourcis de la section MIDI Editor n'interfèrent pas avec ceux de la section Main : un même "
             "raccourci (W dans nos exemples) peut couper des items dans l'arrangement et des notes dans l'éditeur MIDI.",
             "MIDI Editor shortcuts do not clash with Main section shortcuts: the same shortcut (W in our examples) "
             "can split items in the arrange view and notes in the MIDI editor.")))

# 9 -----------------------------------------------------------------
S.append(KeepTogether([P(L("9. Liste des scripts", "9. Script list"), "h1"), table([["Script", "Section", L("Rôle", "Role")],
                ["Tool Buddy - Toolbox", "Main", L("choisir et configurer les outils Arrange", "choose and set up Arrange tools")],
                ["Tool Buddy - Display", "Main", L("bulle de l'outil actif Arrange", "Arrange active-tool bubble")],
                ["Tool Buddy / (alt) / (alt2)", "Main", L("lancer l'action principale / alt / alt 2", "run the main / alt / alt 2 action")],
                ["Tool Buddy - Next tool / Previous tool", "Main", L("outil suivant / précédent", "next / previous tool")],
                ["Tool Buddy MIDI - Toolbox", "MIDI Editor", L("choisir et configurer les outils MIDI", "choose and set up MIDI tools")],
                ["Tool Buddy MIDI - Display", "MIDI Editor", L("bulle de l'outil actif MIDI", "MIDI active-tool bubble")],
                ["Tool Buddy MIDI / (alt) / (alt2)", "MIDI Editor", L("lancer l'action principale / alt / alt 2", "run the main / alt / alt 2 action")],
                ["Tool Buddy MIDI - Next tool / Previous tool", "MIDI Editor", L("outil suivant / précédent", "next / previous tool")]],
               [78 * mm, 26 * mm, 66 * mm])]))
S.append(P(L("Tous les noms commencent par « ReNo Mellow - ». Les fichiers TB_lib, TB_toolbox, TB_display et "
             "TB_startup sont des bibliothèques internes, pas des actions.",
             "All names start with “ReNo Mellow - ”. The TB_lib, TB_toolbox, TB_display and TB_startup files "
             "are internal libraries, not actions."), "small"))

# 10 ----------------------------------------------------------------
faq = [
    [L("Le raccourci principal ne fait rien", "The main shortcut does nothing"),
     L("L'outil actif n'a pas d'action principale, ou son identifiant est inconnu (vérifiez dans Setup : "
       "« Action not found »). Une infobulle « action not found » s'affiche si les infobulles sont activées.",
       "The active tool has no main action, or its ID is unknown (check in Setup: “Action not found”). "
       "An “action not found” tooltip shows if tooltips are on.")],
    [L("Les raccourcis MIDI ne font rien", "MIDI shortcuts do nothing"),
     L("Ils doivent être assignés dans la section <b>MIDI Editor</b> de l'Action List, et un éditeur MIDI doit être "
       "ouvert (« open a MIDI editor first »).",
       "They must be assigned in the <b>MIDI Editor</b> section of the Action List, and a MIDI editor must be open "
       "(“open a MIDI editor first”).")],
    [L("« This script needs ReaImGui »", "“This script needs ReaImGui”"),
     L("Installez ReaImGui avec ReaPack (ReaTeam Extensions), puis redémarrez REAPER.",
       "Install ReaImGui with ReaPack (ReaTeam Extensions), then restart REAPER.")],
    [L("Pas d'infobulles", "No tooltips"),
     L("Elles demandent REAPER 7.03 ou plus et peuvent être désactivées dans Setup > Settings.",
       "They need REAPER 7.03 or later and can be turned off in Setup > Settings.")],
    [L("La bulle ne montre pas le couteau", "The bubble shows no knife"),
     L("L'icône ", "The ") + code("Data/toolbar_icons/ReNo_ToolBuddy.png")
     + L(" est absente : la bulle affiche « TB » à la place. Réinstallez ou synchronisez le paquet.",
         " icon is missing: the bubble shows “TB” instead. Reinstall or synchronize the package.")],
    [L("La bulle MIDI a disparu", "The MIDI bubble is gone"),
     L("Normal si aucun éditeur MIDI n'est ouvert : elle revient dès qu'un éditeur s'ouvre.",
       "Normal when no MIDI editor is open: it comes back as soon as one opens.")],
    [L("Un script manque dans l'Action List", "A script is missing from the Action List"),
     "Toolbox > Setup > Scripts > <b>Register scripts again</b>."],
    [L("Où sont enregistrés mes outils ?", "Where are my tools saved?"),
     L("Dans les réglages de REAPER (", "In REAPER's settings (") + code("reaper-extstate.ini")
     + L(", section ReNoMellow_ToolBuddy), pour toutes les sessions. Pensez à <b>Export...</b> pour en garder une copie.",
         ", section ReNoMellow_ToolBuddy), for all projects. Use <b>Export...</b> to keep a copy.")],
]
S.append(KeepTogether([P(L("10. Questions fréquentes", "10. FAQ"), "h1"),
                       table([["Situation", "Solution"]] + faq, [52 * mm, 118 * mm])]))

doc.multiBuild(S)
print("ok", LANG)
