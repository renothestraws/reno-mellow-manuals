# Manuel RM1982Verb (FR / EN) - reportlab + DejaVu
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
ACC = colors.HexColor('#6cd9c7'); DARK = colors.HexColor('#1d1f23'); GREY = colors.HexColor('#5b5f66')
VERSION = '1.2'
BASE = 'https://github.com/renothestraws/reno-mellow-manuals/raw/main/plugins/RM1982Verb/'
IMG = '/home/claude/irbuddy/verb_face.png'

FR = dict(
 file='RM1982Verb_manuel_FR.pdf', other=('English version', BASE + 'RM1982Verb_manual_EN.pdf'),
 sub="Réverbération à convolution pour REAPER, série 1982",
 foot='ReNo Mellow - RM1982Verb %s - manuel' % VERSION,
 cap="Aperçu de la façade (rendu par le code du plug-in, couleur verte).",
 hd=('Réglage', 'Plage', 'Effet'), hd2=('Geste', 'Effet'),
 S=[
  ('1. Présentation', [
   "<b>RM1982Verb</b> est une réverbération à <b>convolution</b> : elle rejoue sur votre son l'empreinte d'un espace ou d'une "
   "réverbe, appelée <b>réponse impulsionnelle</b> (IR). Elle est livrée avec 100 IR d'usine et avec le script <b>IR Buddy</b>, "
   "qui capture l'IR de vos propres réverbes plug-ins (manuel IR Buddy séparé).",
   "IMAGE",
   "Chaîne du traitement : entrée → PREDELAY → convolution → MOD → WIDTH → PAN → EQ → DUCKER → mélange sec / traité (MIX) → VOLUME.",
  ]),
  ('2. Installation', [
   "<b>ReaPack</b> : dépôt ReNo Mellow (<i>https://raw.githubusercontent.com/renothestraws/reno-mellow/main/index.xml</i>), "
   "catégorie Reverb, paquet RM1982Verb. <b>Sans ReaPack</b> : glissez <b>RM1982Verb.ReaperPkg</b> dans la fenêtre de REAPER (7.86+).",
   "Sont installés : le plug-in (navigateur d'effets, chercher « RM1982Verb »), les 100 IR dans <b>REAPER/Data/RM IR</b> et les "
   "quatre actions d'IR Buddy. Avec ReaPack, lancez une fois l'action <b>ReNo Mellow - IR Buddy - Rescan RM IR</b> pour remplir le navigateur d'IR.",
  ]),
  ('3. Charger une IR', [
   "BUL:<b>Navigateur</b> : cliquez sur le nom de l'IR. Dossiers à gauche, IR à droite ; molette pour défiler, clic pour charger. "
   "La fenêtre reste ouverte pour comparer ; × ou un nouveau clic sur le nom la ferme.",
   "BUL:<b>Flèches &lt; &gt;</b> : IR précédente / suivante du même dossier.",
   "BUL:<b>Liste « IR file »</b> au-dessus de la façade (liste de REAPER) : tous les fichiers de REAPER/Data/RM IR.",
   "BUL:<b>Glisser-déposer</b> d'un fichier .wav n'importe où sur la fenêtre du plug-in (le chemin est gardé avec le projet).",
   "BUL:<b>Bouton dossier</b> : rappelle comment ajouter votre propre dossier d'IR (action IR Buddy « Add IR folder »).",
   "WAV mono ou stéréo, 10 s maximum ; rééchantillonnage automatique si la fréquence diffère du projet. Chaque IR est ramenée "
   "à la même énergie (réverbe à environ -3 dB sous l'entrée) et sa fin silencieuse est coupée.",
  ]),
  ('4. Réglages', ['TABLE']),
  ('5. Latence : ECO ou ZERO', [
   "<b>ECO</b> (par défaut) : 1024 échantillons de latence (21 ms à 48 kHz), compensés automatiquement par REAPER ; moins de processeur. "
   "<b>ZERO</b> : aucune latence (utile en direct ou en enregistrement), un peu plus de processeur. Le son est identique dans les deux modes.",
  ]),
  ('6. Souris et clavier', ['TABLE2']),
  ('7. Les IR d\'usine', [
   "100 IR en 8 dossiers : <b>Ambience</b> (9), <b>Chamber</b> (10), <b>Hall</b> (17), <b>Microphone</b> (21, empreintes de micros "
   "à utiliser avec MIX à 100 %), <b>NonLin</b> (7), <b>Plate</b> (13), <b>Room</b> (13), <b>Spaces</b> (10). Le premier mot du nom "
   "indique le caractère : Modern, Classic, Vintage, Digital, Eighties, Sim, Steel, Soft.",
  ]),
  ('8. Questions fréquentes', [
   "QA:« Cannot open the file » dans le navigateur|L'index ne correspond plus aux fichiers : lancez <b>IR Buddy - Rescan RM IR</b>.",
   "QA:Le navigateur dit « No IR index yet »|IR Buddy n'a pas encore écrit l'index : lancez <b>Rescan RM IR</b>. La liste « IR file » marche sans index.",
   "QA:Une nouvelle IR n'apparaît pas dans la liste « IR file »|Rouvrez la fenêtre du plug-in.",
   "QA:Sur une piste de retour (send)|Mettez MIX à 100 % : seule la réverbe sort, le son sec passe par la piste d'origine.",
  ]),
 ],
 rows=[('ATTACK', '0 – 500 ms', "Fondu d'entrée sur le début de l'IR : adoucit les premières réflexions."),
       ('PREDELAY', '0 – 250 ms', "Retard avant la réverbe : laisse le son direct respirer devant."),
       ('DECAY', '10 – 100 %', "Raccourcit la queue (100 % = IR d'origine)."),
       ('MOD', 'OFF – 100 %', "Léger chorus sur la queue, pour l'animer."),
       ('WIDTH', '0 – 200 %', "Largeur stéréo de la réverbe : 0 = mono, 100 = d'origine, 200 = très large."),
       ('PAN', 'L100 – C – R100', "Place la réverbe à gauche ou à droite (traité seulement, puissance constante)."),
       ('DUCKER', 'OFF, -60 – 0 dB', "Seuil d'un compresseur piloté par le son sec (ratio 3:1, genou souple, attaque 1 ms, release automatique) : la réverbe s'efface pendant le jeu et revient entre les notes. GR = atténuation en cours."),
       ('HPF / LPF', 'OFF – 1 kHz / 1 kHz – OFF', "Filtres coupe-bas et coupe-haut sur la réverbe (12 dB/octave)."),
       ('LOW / MID / HIGH', '±12 dB', "Plateau 250 Hz, cloche 1,2 kHz, plateau 6 kHz, sur la réverbe seulement."),
       ('VOLUME', '-24 – +12 dB', "Niveau de sortie (sec + réverbe)."),
       ('MIX', '0 – 100 %', "Dosage sec / réverbe (30 % par défaut)."),
       ('LATENCY', 'ZERO / ECO', "Voir section 5.")],
 rows2=[('Glisser un potard (vertical)', 'Régler ; Shift = réglage fin ; molette aussi.'),
        ('Ctrl-clic (Cmd-clic) sur un potard', 'Valeur par défaut.'),
        ('Clic sur une valeur / double-clic sur un potard', 'Saisie au clavier : 25, 1.2s, 4.5k, off, L30, R25, C ; Entrée = valider, Échap = annuler.'),
        ('Clic sur le nom de l\'IR', 'Ouvre / ferme le navigateur d\'IR.'),
        ('Double-clic sur « RM1982Verb »', 'Couleur verte / orange.'),
        ('Boutons SIZE', 'Taille de la fenêtre : 75 à 200 %.'),
        ('Clic sur les crête-mètres', 'Remise à zéro.')],
)
EN = dict(
 file='RM1982Verb_manual_EN.pdf', other=('Version française', BASE + 'RM1982Verb_manuel_FR.pdf'),
 sub='Convolution reverb for REAPER, 1982 series',
 foot='ReNo Mellow - RM1982Verb %s - manual' % VERSION,
 cap="Panel preview (drawn by the plug-in's own code, green colour).",
 hd=('Control', 'Range', 'What it does'), hd2=('Gesture', 'What it does'),
 S=[
  ('1. Overview', [
   "<b>RM1982Verb</b> is a <b>convolution</b> reverb: it plays back on your sound the fingerprint of a space or of a reverb, "
   "called an <b>impulse response</b> (IR). It comes with 100 factory IRs and with the <b>IR Buddy</b> script, which captures the IR "
   "of your own reverb plug-ins (separate IR Buddy manual).",
   "IMAGE",
   "Signal flow: input → PREDELAY → convolution → MOD → WIDTH → PAN → EQ → DUCKER → dry / wet blend (MIX) → VOLUME.",
  ]),
  ('2. Installation', [
   "<b>ReaPack</b>: ReNo Mellow repository (<i>https://raw.githubusercontent.com/renothestraws/reno-mellow/main/index.xml</i>), "
   "Reverb category, RM1982Verb package. <b>Without ReaPack</b>: drag <b>RM1982Verb.ReaperPkg</b> into the REAPER window (7.86+).",
   "Installed: the plug-in (FX browser, search \"RM1982Verb\"), the 100 IRs in <b>REAPER/Data/RM IR</b> and the four IR Buddy actions. "
   "With ReaPack, run the <b>ReNo Mellow - IR Buddy - Rescan RM IR</b> action once to fill the IR browser.",
  ]),
  ('3. Load an IR', [
   "BUL:<b>Browser</b>: click the IR name. Folders on the left, IRs on the right; wheel to scroll, click to load. "
   "It stays open so you can compare; × or another click on the name closes it.",
   "BUL:<b>&lt; &gt; arrows</b>: previous / next IR of the same folder.",
   "BUL:<b>\"IR file\" list</b> above the panel (REAPER's list): every file in REAPER/Data/RM IR.",
   "BUL:<b>Drag and drop</b> a .wav file anywhere on the plug-in window (the path is saved with the project).",
   "BUL:<b>Folder button</b>: reminds you how to add your own IR folder (IR Buddy action \"Add IR folder\").",
   "Formats: mono or stereo WAV, up to 10 s (longer: cut, shown as \"cut at 10 s\"). An IR at another sample rate than the project is "
   "resampled automatically (shown on the status line). Every IR is brought to the same energy and its silent end is trimmed: "
   "the reverb comes out about 3 dB below the input, whatever the IR.",
  ]),
  ('4. Controls', ['TABLE']),
  ('5. Latency: ECO or ZERO', [
   "<b>ECO</b> (default): 1024 samples of latency (21 ms at 48 kHz), compensated automatically by REAPER; less CPU. "
   "<b>ZERO</b>: no latency at all (live playing, recording), a little more CPU. The sound is the same in both modes.",
  ]),
  ('6. Mouse and keyboard', ['TABLE2']),
  ('7. Factory IRs', [
   "100 IRs in 8 folders: <b>Ambience</b> (9), <b>Chamber</b> (10), <b>Hall</b> (17), <b>Microphone</b> (21, microphone fingerprints, "
   "use them with MIX at 100 %), <b>NonLin</b> (7), <b>Plate</b> (13), <b>Room</b> (13), <b>Spaces</b> (10). The first word of the name "
   "gives the character: Modern, Classic, Vintage, Digital, Eighties, Sim, Steel, Soft.",
  ]),
  ('8. FAQ', [
   "QA:\"Cannot open the file\" in the browser|The index no longer matches the files: run <b>IR Buddy - Rescan RM IR</b>.",
   "QA:The browser says \"No IR index yet\"|IR Buddy has not written the index yet: run <b>Rescan RM IR</b>. The \"IR file\" list works without it.",
   "QA:A new IR does not show in the \"IR file\" list|Close and reopen the plug-in window: REAPER reads the folder again.",
   "QA:On a return (send) track|Set MIX to 100 %: only the reverb comes out, the dry sound goes through the original track.",
  ]),
 ],
 rows=[('ATTACK', '0 – 500 ms', 'Fade-in on the start of the IR: softens the early reflections.'),
       ('PREDELAY', '0 – 250 ms', 'Delay before the reverb: lets the direct sound breathe in front.'),
       ('DECAY', '10 – 100 %', 'Shortens the tail (100 % = original IR).'),
       ('MOD', 'OFF – 100 %', 'Light chorus on the tail, to make it move.'),
       ('WIDTH', '0 – 200 %', 'Stereo width of the reverb: 0 = mono, 100 = original, 200 = extra wide.'),
       ('PAN', 'L100 – C – R100', 'Moves the reverb left or right (wet only, equal power).'),
       ('DUCKER', 'OFF, -60 – 0 dB', 'Threshold of a compressor driven by the dry sound (3:1, soft knee, 1 ms attack, automatic release): the reverb steps back while you play and blooms between the notes. GR = current reduction.'),
       ('HPF / LPF', 'OFF – 1 kHz / 1 kHz – OFF', 'Low-cut and high-cut filters on the reverb (12 dB/octave).'),
       ('LOW / MID / HIGH', '±12 dB', '250 Hz shelf, 1.2 kHz bell, 6 kHz shelf, on the reverb only.'),
       ('VOLUME', '-24 – +12 dB', 'Output level (dry + reverb).'),
       ('MIX', '0 – 100 %', 'Dry / reverb blend (30 % by default).'),
       ('LATENCY', 'ZERO / ECO', 'See section 5.')],
 rows2=[('Drag a knob (vertical)', 'Adjust; Shift = fine; mouse wheel too.'),
        ('Ctrl-click (Cmd-click) a knob', 'Default value.'),
        ('Click a value / double-click a knob', 'Type it: 25, 1.2s, 4.5k, off, L30, R25, C; Enter = OK, Esc = cancel.'),
        ('Click the IR name', 'Opens / closes the IR browser.'),
        ('Double-click "RM1982Verb"', 'Green / orange colour.'),
        ('SIZE buttons', 'Window size: 75 to 200 %.'),
        ('Click the peak meters', 'Reset.')],
)

st_body = ParagraphStyle('b', fontName='DV', fontSize=8.8, leading=12, spaceAfter=3, textColor=DARK)
st_h = ParagraphStyle('h', fontName='DVB', fontSize=13, leading=17, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#2a9d8f'), keepWithNext=1)
st_bul = ParagraphStyle('u', parent=st_body, leftIndent=14, bulletIndent=4, spaceAfter=2)
st_cell = ParagraphStyle('c', fontName='DV', fontSize=8.5, leading=11, textColor=DARK)
st_cellb = ParagraphStyle('cb', fontName='DVB', fontSize=8.5, leading=11, textColor=DARK)
st_q = ParagraphStyle('q', fontName='DVB', fontSize=9.5, leading=13, spaceBefore=3, textColor=DARK, keepWithNext=1)
st_cap = ParagraphStyle('cap', fontName='DV', fontSize=7.5, textColor=GREY, spaceAfter=6)

def tbl(head, rows, widths):
    data = [[Paragraph(h, st_cellb) for h in head]] + [[Paragraph(c, st_cellb if i == 0 else st_cell) for i, c in enumerate(r)] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), ACC), ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c9ccd1')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f4f6')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t

def build(L):
    def deco(c, d):
        c.saveState(); c.setFillColor(ACC); c.rect(0, A4[1] - 6*mm, A4[0], 6*mm, fill=1, stroke=0)
        c.setFont('DV', 8); c.setFillColor(GREY); c.drawString(18*mm, 10*mm, L['foot'])
        c.drawRightString(A4[0] - 18*mm, 10*mm, str(d.page)); c.restoreState()
    doc = BaseDocTemplate(L['file'], pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=16*mm,
                          title='RM1982Verb', author='ReNo Mellow')
    W = A4[0] - 36*mm
    doc.addPageTemplates([PageTemplate(frames=[Frame(18*mm, 16*mm, W, A4[1] - 31*mm, id='f')], onPage=deco)])
    s = [Paragraph('ReNo Mellow', ParagraphStyle('k', fontName='DVB', fontSize=10, textColor=GREY)),
         Paragraph('RM1982Verb', ParagraphStyle('t', fontName='DVB', fontSize=24, leading=28, textColor=DARK)),
         Paragraph(L['sub'], ParagraphStyle('s', fontName='DV', fontSize=12, leading=16, textColor=GREY, spaceAfter=4)),
         Paragraph('Version %s &nbsp;·&nbsp; <link href="%s" color="#2a9d8f">%s</link>' % (VERSION, L['other'][1], L['other'][0]),
                   ParagraphStyle('v', fontName='DV', fontSize=9, textColor=GREY, spaceAfter=6))]
    for title, paras in L['S']:
        s.append(Paragraph(title, st_h if paras[0] != 'TABLE' else ParagraphStyle('h2', parent=st_h, keepWithNext=0)))
        for p in paras:
            if p == 'IMAGE':
                s.append(Image(IMG, width=W*0.8, height=W*0.8*470/1220)); s.append(Paragraph(L['cap'], st_cap))
            elif p == 'TABLE': s.append(tbl(L['hd'], L['rows'], [30*mm, 34*mm, W - 64*mm])); s.append(Spacer(1, 4))
            elif p == 'TABLE2': s.append(tbl(L['hd2'], L['rows2'], [62*mm, W - 62*mm])); s.append(Spacer(1, 4))
            elif p.startswith('BUL:'): s.append(Paragraph(p[4:], st_bul, bulletText='•'))
            elif p.startswith('QA:'):
                q, a = p[3:].split('|', 1); s.append(Paragraph(q, st_q)); s.append(Paragraph(a, st_body))
            else: s.append(Paragraph(p, st_body))
    doc.build(s)

for L in (FR, EN): build(L)
