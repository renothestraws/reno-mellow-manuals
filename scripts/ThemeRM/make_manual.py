"""User manual (PDF, FR or EN) - Default 7.0 RM Orange / RM Teal themes + toolbar icons.

python3 make_manual.py <fr|en> <output.pdf> <icons_rmo_dir_200> <icons_rmt_dir_200>
"""
import sys, os
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

LANG, OUT, RMO, RMT = sys.argv[1:5]
VERSION = "1.0"
FR = LANG == "fr"
def L(fr, en): return fr if FR else en

REPO = "github.com/renothestraws/reno-mellow-script"
RAW = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/"
MANUALS = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/ThemeRM/"
OTHER_URL = MANUALS + ("ThemeRM_manual_EN.pdf" if FR else "ThemeRM_manuel_FR.pdf")
INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
for b in (0, 1):
    for i in (0, 1):
        addMapping("DV", b, i, "DVB" if b else "DV")

ORANGE = colors.HexColor("#FF941F")
TEAL = colors.HexColor("#6CD9C7")
ACC = colors.HexColor("#E07A10")
DARK = colors.HexColor("#1D1F21")
GREY = colors.HexColor("#6B6F76")
LIGHT = colors.HexColor("#F2F3F5")
LINE = colors.HexColor("#D9DBDF")

st = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.5, spaceAfter=5),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, textColor=DARK, spaceBefore=4, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=ACC, spaceBefore=8, spaceAfter=4),
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
def link(url, text=None): return f'<link href="{url}" color="#E07A10"><u>{text or url}</u></link>'

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
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF4E8")),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.5, ORANGE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t

# ---------------------------------------------------------------- real icon crops
TMP = OUT + "_tmp"
os.makedirs(TMP, exist_ok=True)
def states(folder, name, tag):
    """Return 3 png paths (rest, hover, on) cut from a real toolbar icon."""
    im = PILImage.open(os.path.join(folder, f"toolbar_icons_{tag}_{name}.png")).convert("RGBA")
    w, h = im.size; s = w // 3; out = []
    for k in range(3):
        p = os.path.join(TMP, f"{tag}_{name}_{k}.png")
        im.crop((k * s, 0, (k + 1) * s, h)).save(p); out.append(p)
    return out

SAMPLE = ["play", "record", "loop", "metronome", "gridbuddy", "split"]
def existing(folder, tag):
    return [n for n in SAMPLE if os.path.exists(os.path.join(folder, f"toolbar_icons_{tag}_{n}.png"))]

class IconRow(Flowable):
    def __init__(self, folder, tag, label):
        super().__init__(); self.folder, self.tag, self.label = folder, tag, label
        self.names = existing(folder, tag)
        self.width, self.height = 170 * mm, 17 * mm
    def draw(self):
        c = self.canv
        c.setFillColor(DARK); c.roundRect(0, 0, self.width, self.height, 4, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("DVB", 8.5); c.drawString(6, self.height - 11, self.label)
        x = 6
        for n in self.names:
            for p in states(self.folder, n, self.tag):
                c.drawImage(p, x, 4, 26, 26, mask="auto"); x += 28
            x += 8

# ---------------------------------------------------------------- drawings
class Palette(Flowable):
    def __init__(self):
        super().__init__(); self.width, self.height = 170 * mm, 30 * mm
    def draw(self):
        c = self.canv
        sw = [("#FF941F", "RM Orange"), ("#FFB359", "Orange " + L("texte", "text")),
              ("#6CD9C7", "RM Teal"), ("#99EBDB", "Teal " + L("texte", "text")),
              ("#1D1F21", L("Fond TCP/MCP", "TCP/MCP bg")), ("#292A2E", L("Boutons", "Buttons")),
              ("#2B2B2B", L("Éléments vides", "Empty slots"))]
        w = self.width / len(sw)
        for k, (hx, name) in enumerate(sw):
            c.setFillColor(colors.HexColor(hx)); c.setStrokeColor(LINE)
            c.roundRect(k * w + 2, 10, w - 4, self.height - 12, 3, stroke=1, fill=1)
            c.setFillColor(DARK); c.setFont("DV", 6.8); c.drawCentredString(k * w + w / 2, 2, name)
            c.setFillColor(colors.white if hx in ("#1D1F21", "#292A2E", "#2B2B2B") else DARK)
            c.setFont("DVM", 6.5); c.drawCentredString(k * w + w / 2, 14, hx)

class Meter(Flowable):
    """Horizontal sketch of the meter gradient (-62 .. +6 dB)."""
    STOPS = [(-62, (60, 170, 90)), (-24, (77, 209, 107)), (-18, (250, 214, 56)),
             (-9, (255, 160, 40)), (-3, (255, 56, 46)), (6, (255, 56, 46))]
    def __init__(self):
        super().__init__(); self.width, self.height = 170 * mm, 24 * mm
    def col(self, db):
        S = self.STOPS
        for (d0, c0), (d1, c1) in zip(S, S[1:]):
            if d0 <= db <= d1:
                t = (db - d0) / (d1 - d0)
                return colors.Color(*[(a + (b - a) * t) / 255 for a, b in zip(c0, c1)])
        return colors.Color(*[v / 255 for v in S[-1][1]])
    def draw(self):
        c = self.canv; W = self.width; x0, y0, h = 4, 12, 9
        n = 300
        for i in range(n):
            db = -62 + 68 * i / n
            c.setFillColor(self.col(db)); c.rect(x0 + (W - 8) * i / n, y0, (W - 8) / n + 0.5, h, stroke=0, fill=1)
        c.setFillColor(DARK); c.setFont("DV", 7)
        for db in (-60, -48, -36, -24, -18, -12, -6, 0, 6):
            x = x0 + (W - 8) * (db + 62) / 68
            c.setStrokeColor(GREY); c.line(x, y0 - 2, x, y0)
            c.drawCentredString(x, y0 - 9, f"{db:+d}" if db else "0")
        c.setFont("DV", 7.5); c.setFillColor(GREY)
        c.drawString(x0, y0 + h + 4, L("dBFS (gauche = bas du mètre, droite = haut)", "dBFS (left = bottom of the meter, right = top)"))

# ---------------------------------------------------------------- document
TITLE = L("Manuel d'utilisation", "User manual")
NAME = "Default 7.0 RM Orange / RM Teal"

class Doc(BaseDocTemplate):
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name == "h1":
            self.notify("TOCEntry", (0, f.getPlainText(), self.page))

def on_page(c, d):
    c.saveState()
    c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    c.setFont("DV", 7.5); c.setFillColor(GREY)
    c.drawString(20 * mm, 10 * mm, f"ReNo Mellow - {NAME} {VERSION} - {TITLE}")
    c.drawRightString(190 * mm, 10 * mm, str(d.page))
    c.restoreState()

COVER_ICONS = [states(RMO, "record", "rmo")[2] if os.path.exists(os.path.join(RMO, "toolbar_icons_rmo_record.png")) else None,
               states(RMT, "record", "rmt")[2] if os.path.exists(os.path.join(RMT, "toolbar_icons_rmt_record.png")) else None]

def cover(c, d):
    c.saveState()
    W, H = A4
    c.setFillColor(DARK); c.rect(0, H - 120 * mm, W, 120 * mm, stroke=0, fill=1)
    # two accent bands
    c.setFillColor(ORANGE); c.rect(0, H - 120 * mm, W / 2, 3 * mm, stroke=0, fill=1)
    c.setFillColor(TEAL); c.rect(W / 2, H - 120 * mm, W / 2, 3 * mm, stroke=0, fill=1)
    x = 20 * mm
    for p in COVER_ICONS:
        if p: c.drawImage(p, x, H - 62 * mm, 28 * mm, 28 * mm, mask="auto"); x += 32 * mm
    c.setFillColor(colors.white); c.setFont("DVB", 24); c.drawString(20 * mm, H - 80 * mm, "Default 7.0 RM")
    c.setFillColor(ORANGE); c.drawString(20 * mm + c.stringWidth("Default 7.0 RM ", "DVB", 24), H - 80 * mm, "Orange")
    w2 = c.stringWidth("Default 7.0 RM Orange ", "DVB", 24)
    c.setFillColor(colors.white); c.drawString(20 * mm + w2, H - 80 * mm, "/")
    c.setFillColor(TEAL); c.drawString(20 * mm + w2 + c.stringWidth("/ ", "DVB", 24), H - 80 * mm, "Teal")
    c.setFont("DV", 12.5); c.setFillColor(colors.HexColor("#C9CCD1"))
    c.drawString(20 * mm, H - 90 * mm, L("Thèmes REAPER, Theme Adjusters et icônes de barre d'outils",
                                         "REAPER themes, Theme Adjusters and toolbar icons"))
    c.setFillColor(ORANGE); c.setFont("DVB", 11)
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
          title=f"ReNo Mellow - {NAME} - {TITLE}", author="ReNo Mellow", subject=f"{NAME} {VERSION} for REAPER")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, A4[1] - 140 * mm, id="c")
doc.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=cover),
                      PageTemplate("normal", [frame], onPage=on_page)])

S = [NextPageTemplate("normal")]
S.append(P(L("Deux thèmes pour REAPER dans l'esprit des plug-ins RM : le thème <b>Default 7.0</b> de Cockos, "
             "redessiné avec des gris doux et un accent <b>orange</b> (RM Orange) ou <b>vert d'eau</b> (RM Teal). "
             "Chaque thème a son <b>Theme Adjuster</b> recoloré, et un jeu complet d'<b>icônes de barre d'outils</b> "
             "existe dans chaque couleur.",
             "Two REAPER themes in the spirit of the RM plug-ins: Cockos' <b>Default 7.0</b> theme, "
             "redrawn with soft greys and an <b>orange</b> (RM Orange) or <b>teal</b> (RM Teal) accent. "
             "Each theme has its own recoloured <b>Theme Adjuster</b>, and a full set of <b>toolbar icons</b> "
             "exists in each colour.")))
S.append(P(L(f'{link(OTHER_URL, "English version of this manual")}',
             f'{link(OTHER_URL, "Version française de ce manuel")}'), "small"))
S.append(Spacer(1, 4))
toc = TableOfContents(); toc.levelStyles = [st["toc1"]]
S.append(P(L("<b>Sommaire</b>", "<b>Contents</b>")))
S.append(toc)
S.append(PageBreak())

# 1 -----------------------------------------------------------------
S.append(P(L("1. Principe", "1. What it is"), "h1"))
S.append(P(L("Les thèmes RM gardent <b>toute la mise en page et tous les réglages</b> du Default 7.0 : mêmes layouts de "
             "pistes (TCP), de mixer (MCP) et de transport, mêmes options dans le Theme Adjuster. Seul l'habillage change : "
             "couleurs, boutons, faders, potards et vu-mètres. Vous retrouvez donc vos repères, avec un look plus calme "
             "et moins fatigant pour les yeux lors des longues séances.",
             "The RM themes keep <b>all the layouts and settings</b> of Default 7.0: same track (TCP), mixer (MCP) and "
             "transport layouts, same options in the Theme Adjuster. Only the skin changes: colours, buttons, faders, "
             "knobs and meters. You keep your bearings, with a calmer look that is easier on the eyes during long sessions.")))
S.append(KeepTogether([P(L("Palette", "Palette"), "h2"), Palette(), Spacer(1, 4)]))
S.append(table([[L("Élément", "Element"), L("Ce qui change", "What changes")],
                [L("Boutons", "Buttons"), L("Boutons d'origine recolorés ; l'accent (orange ou teal) marque l'état allumé.",
                                            "Original buttons recoloured; the accent (orange or teal) marks the lit state.")],
                [L("Armement d'enregistrement", "Record arm"), L("Bouton rond, rouge quand la piste est armée.",
                                                               "Round button, red when the track is armed.")],
                [L("Faders et potards", "Faders and knobs"), L("Touche « hardware » : capuchons en relief ; fader du TCP plus large.",
                                                              "A “hardware” touch: raised caps; wider TCP fader.")],
                [L("Vu-mètres", "Meters"), L("Dégradé vert → jaune → rouge, bascule autour de -18 dBFS (voir chapitre 4).",
                                             "Green → yellow → red gradient, switching around -18 dBFS (see chapter 4).")],
                [L("Zones vides", "Empty slots"), L("Emplacements vides du TCP et du MCP en gris doux (43, 43, 43) au lieu de noir.",
                                                   "Empty TCP and MCP slots in soft grey (43, 43, 43) instead of black.")],
                [L("Textes", "Text"), L("Police Arial grasse, plus lisible sur fond sombre.", "Bold Arial font, easier to read on dark backgrounds.")]],
               [42 * mm, 128 * mm]))

# 2 -----------------------------------------------------------------
S.append(P(L("2. Installation", "2. Installation"), "h1"))
S.append(P(L("Trois façons de faire, au choix. Les fichiers sont les mêmes ; seule la mise à jour change.",
             "Three ways, your choice. The files are the same; only updating differs.")))
S.append(P(L("Avec ReaPack (recommandé)", "With ReaPack (recommended)"), "h2"))
S.extend(N([L(f"Extensions > ReaPack > Import repositories, collez l'adresse : {code(INDEX)} (inutile si le dépôt ReNo Mellow Scripts est déjà importé).",
              f"Extensions > ReaPack > Import repositories, paste the address: {code(INDEX)} (not needed if the ReNo Mellow Scripts repository is already imported)."),
            L("Extensions > ReaPack > Browse packages, cherchez <b>Default 7.0 RM</b> et installez la version Orange, Teal, ou les deux. "
              "Le paquet contient le thème <b>et</b> son Theme Adjuster.",
              "Extensions > ReaPack > Browse packages, search for <b>Default 7.0 RM</b> and install the Orange version, the Teal one, or both. "
              "The package contains the theme <b>and</b> its Theme Adjuster."),
            L("Pour les icônes, cherchez <b>Toolbar icons RM</b> et installez RM Orange et/ou RM Teal.",
              "For the icons, search for <b>Toolbar icons RM</b> and install RM Orange and/or RM Teal."),
            L("Activez le thème : Options > Themes, puis choisissez Default_7.0_RM_Orange ou Default_7.0_RM_Teal.",
              "Activate the theme: Options > Themes, then pick Default_7.0_RM_Orange or Default_7.0_RM_Teal.")]))
S.append(P(L("Sans ReaPack (téléchargement direct)", "Without ReaPack (direct download)"), "h2"))
S.append(table([[L("Fichier", "File"), L("Que faire", "What to do")],
                [link(RAW + "Default_7.0_RM_Orange.ReaperThemeZip", "Default_7.0_RM_Orange.ReaperThemeZip") + "<br/>" +
                 link(RAW + "Default_7.0_RM_Teal.ReaperThemeZip", "Default_7.0_RM_Teal.ReaperThemeZip"),
                 L("Glissez-le dans la fenêtre de REAPER (ou double-cliquez) : le thème s'installe et s'active.",
                   "Drag it into the REAPER window (or double-click it): the theme installs and activates.")],
                [link(RAW + "Default_7.0_RM_Orange_Theme_Adjuster.ReaperPkg", "Default_7.0_RM_Orange_Theme_Adjuster.ReaperPkg") + "<br/>" +
                 link(RAW + "Default_7.0_RM_Teal_Theme_Adjuster.ReaperPkg", "Default_7.0_RM_Teal_Theme_Adjuster.ReaperPkg"),
                 L("Glissez-le dans REAPER (version 7.86 ou plus) : le Theme Adjuster est installé et ajouté à la liste d'actions.",
                   "Drag it into REAPER (version 7.86 or later): the Theme Adjuster is installed and added to the action list.")],
                [link(RAW + "ReNo_Mellow_Toolbar_Icons_RM_Orange.ReaperPkg", "ReNo_Mellow_Toolbar_Icons_RM_Orange.ReaperPkg") + "<br/>" +
                 link(RAW + "ReNo_Mellow_Toolbar_Icons_RM_Teal.ReaperPkg", "ReNo_Mellow_Toolbar_Icons_RM_Teal.ReaperPkg"),
                 L("Glissez-le dans REAPER : les icônes vont dans Data/toolbar_icons (100, 150 et 200 %).",
                   "Drag it into REAPER: the icons go to Data/toolbar_icons (100, 150 and 200 %).")]],
               [88 * mm, 82 * mm]))
S.append(Spacer(1, 4))
S.append(note(L("Un paquet .ReaperPkg ne peut pas installer de thème : c'est pourquoi le thème lui-même est fourni en "
                ".ReaperThemeZip. Les paquets .ReaperPkg ne se mettent pas à jour seuls ; avec ReaPack, pensez à "
                "Extensions > ReaPack > Synchronize packages.",
                "A .ReaperPkg package cannot install a theme: that is why the theme itself comes as a .ReaperThemeZip. "
                ".ReaperPkg packages do not update themselves; with ReaPack, use Extensions > ReaPack > Synchronize packages.")))

# 3 -----------------------------------------------------------------
S.append(P(L("3. Theme Adjuster", "3. Theme Adjuster"), "h1"))
S.append(P(L("Le Theme Adjuster RM est le Default 7.0 Theme Adjuster de Cockos, avec les couleurs du thème. Il règle "
             "exactement les mêmes choses : layouts des pistes et du mixer, éléments visibles, tailles, couleurs des pistes, "
             "options du transport.",
             "The RM Theme Adjuster is Cockos' Default 7.0 Theme Adjuster, in the theme's colours. It sets exactly "
             "the same things: track and mixer layouts, visible elements, sizes, track colours, transport options.")))
S.append(table([[L("Thème actif", "Active theme"), L("Action à lancer (Actions > Show action list)", "Action to run (Actions > Show action list)")],
                ["Default_7.0_RM_Orange", code("Default_7.0_RM_Orange_theme_adjuster.lua")],
                ["Default_7.0_RM_Teal", code("Default_7.0_RM_Teal_theme_adjuster.lua")]],
               [50 * mm, 120 * mm]))
S.append(Spacer(1, 4))
S.extend(B([L("L'adjuster ne fonctionne qu'avec un thème dont le nom commence par <b>Default_7.0</b> : c'est le cas des thèmes RM. "
              "Ne renommez pas le fichier du thème.",
              "The adjuster only works with a theme whose name starts with <b>Default_7.0</b>: the RM themes do. "
              "Do not rename the theme file."),
            L("Vos réglages sont enregistrés dans le thème actif, comme avec le Default 7.0.",
              "Your settings are stored in the active theme, as with Default 7.0."),
            L("Astuce : placez l'action sur une barre d'outils avec une icône RM (chapitre 5).",
              "Tip: put the action on a toolbar with an RM icon (chapter 5).")]))

# 4 -----------------------------------------------------------------
S.append(KeepTogether([
    P(L("4. Vu-mètres", "4. Meters"), "h1"),
    P(L("Les crête-mètres des pistes et du mixer passent du vert au rouge selon le niveau, comme sur une console. "
        "Le vert couvre la zone de travail confortable ; le passage au jaune se fait vers <b>-18 dBFS</b>, l'orange vers "
        "-9 dBFS et le rouge à partir de -3 dBFS.",
        "Track and mixer peak meters go from green to red with the level, like on a console. "
        "Green covers the comfortable working range; the change to yellow happens around <b>-18 dBFS</b>, orange around "
        "-9 dBFS, and red from -3 dBFS.")),
    Meter(), Spacer(1, 4)]))
S.append(note(L("Le dégradé suppose l'échelle par défaut de REAPER (environ -62 à +6 dB). Si vous changez la plage des "
                "mètres dans Preferences > Appearance > VU meters, les couleurs restent à la même place sur le mètre et "
                "ne correspondent plus exactement à ces valeurs.",
                "The gradient assumes REAPER's default scale (about -62 to +6 dB). If you change the meter range in "
                "Preferences > Appearance > VU meters, the colours stay at the same place on the meter and no longer match "
                "these values exactly.")))

# 5 -----------------------------------------------------------------
S.append(P(L("5. Icônes de barre d'outils RM", "5. RM toolbar icons"), "h1"))
S.append(P(L("Toutes les icônes personnalisées ReNo Mellow (actions natives, éditeur MIDI, et les icônes des scripts "
             "Grid Buddy, Strip Buddy, Recording Buddy et Tool Buddy) sont redessinées dans chaque couleur : 147 icônes, "
             "en 100, 150 et 200 %. Chaque icône a trois états : repos, survol et allumé (couleur d'accent).",
             "All the ReNo Mellow custom icons (native actions, MIDI editor, and the Grid Buddy, Strip Buddy, Recording Buddy "
             "and Tool Buddy script icons) are redrawn in each colour: 147 icons, at 100, 150 and 200 %. Each icon has three "
             "states: rest, hover and lit (accent colour).")))
S.append(KeepTogether([IconRow(RMO, "rmo", L("RM Orange  (repos · survol · allumé)", "RM Orange  (rest · hover · lit)")), Spacer(1, 4),
                       IconRow(RMT, "rmt", L("RM Teal  (repos · survol · allumé)", "RM Teal  (rest · hover · lit)")), Spacer(1, 6)]))
S.append(table([[L("Jeu", "Set"), L("Nom des fichiers", "File names")],
                ["RM Orange", code("toolbar_icons_rmo_&lt;name&gt;.png")],
                ["RM Teal", code("toolbar_icons_rmt_&lt;name&gt;.png")]], [40 * mm, 130 * mm]))
S.append(Spacer(1, 4))
S.extend(N([L("Clic droit sur une barre d'outils > Customize toolbar.", "Right-click a toolbar > Customize toolbar."),
            L("Choisissez un bouton puis Icon. Tapez <b>rmo</b> ou <b>rmt</b> dans le filtre pour ne voir que les icônes RM.",
              "Pick a button, then Icon. Type <b>rmo</b> or <b>rmt</b> in the filter to see only the RM icons."),
            L("REAPER choisit seul la taille 150 ou 200 % selon l'échelle de l'écran.",
              "REAPER picks the 150 or 200 % size on its own according to the screen scaling.")]))

# 6 -----------------------------------------------------------------
S.append(KeepTogether([P(L("6. Questions fréquentes", "6. FAQ"), "h1"),
    table([[L("Question", "Question"), L("Réponse", "Answer")],
           [L("Le Theme Adjuster dit que le thème n'est pas compatible.", "The Theme Adjuster says the theme is not compatible."),
            L("Vérifiez que le thème actif est bien Default_7.0_RM_Orange (ou Teal) et que son fichier n'a pas été renommé.",
              "Check that the active theme is Default_7.0_RM_Orange (or Teal) and that its file was not renamed.")],
           [L("Puis-je installer Orange et Teal ensemble ?", "Can I install Orange and Teal together?"),
            L("Oui. Ce sont deux thèmes distincts avec chacun leur adjuster ; passez de l'un à l'autre dans Options > Themes.",
              "Yes. They are two separate themes, each with its own adjuster; switch between them in Options > Themes.")],
           [L("Mes anciennes icônes ReNo Mellow restent-elles ?", "Do my old ReNo Mellow icons stay?"),
            L("Oui. Les jeux RM portent d'autres noms (rmo, rmt) et n'écrasent rien ; vos barres d'outils ne changent pas tant que vous ne choisissez pas les nouvelles icônes.",
              "Yes. The RM sets have different names (rmo, rmt) and overwrite nothing; your toolbars do not change until you pick the new icons.")],
           [L("Les couleurs des mètres ne tombent pas à -18 dB.", "The meter colours do not fall at -18 dB."),
            L("Voir chapitre 4 : le dégradé suit l'échelle par défaut des mètres.", "See chapter 4: the gradient follows the default meter scale.")],
           [L("Comment revenir au thème d'origine ?", "How do I go back to the original theme?"),
            L("Options > Themes > Default_7.0. Rien n'est modifié dans le thème de Cockos.",
              "Options > Themes > Default_7.0. Nothing is changed in the Cockos theme.")]],
          [62 * mm, 108 * mm])]))
S.append(Spacer(1, 8))
S.append(P(L("Les thèmes RM sont dérivés du thème Default 7.0 de Cockos ; les Theme Adjusters RM sont des versions "
             "modifiées du Default 7.0 Theme Adjuster de Cockos (licence LGPL v2 ou ultérieure).",
             "The RM themes are derived from Cockos' Default 7.0 theme; the RM Theme Adjusters are modified versions "
             "of Cockos' Default 7.0 Theme Adjuster (LGPL v2 or later)."), "small"))

doc.multiBuild(S)
import shutil; shutil.rmtree(TMP, ignore_errors=True)
print("ok", OUT)
