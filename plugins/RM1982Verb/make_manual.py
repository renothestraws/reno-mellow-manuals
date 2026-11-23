# Manuel IR Buddy (FR / EN) - reportlab + DejaVu
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
ACC = colors.HexColor('#6cd9c7'); DARK = colors.HexColor('#1d1f23'); GREY = colors.HexColor('#5b5f66')
VERSION = '1.0'
BASE = 'https://github.com/renothestraws/reno-mellow-manuals/raw/main/plugins/RM1982Verb/'

T = {
 'fr': dict(
  file='IRBuddy_manuel_FR.pdf', other=('English version', BASE + 'IRBuddy_manual_EN.pdf'),
  sub="Capturer la réponse impulsionnelle d'une réverbe plug-in pour RM1982Verb",
  foot='ReNo Mellow - IR Buddy %s - manuel' % VERSION,
  sections=[
   ('1. Le principe', [
    "Une <b>réponse impulsionnelle</b> (IR, <i>impulse response</i>) est l'empreinte sonore d'une réverbe : ce qu'elle "
    "renvoie quand on lui envoie un seul clic très bref. Une réverbe à convolution comme <b>RM1982Verb</b> rejoue "
    "cette empreinte sur n'importe quel son.",
    "<b>IR Buddy</b> fabrique cette empreinte à partir des plug-ins d'une piste, en un clic. Il copie la chaîne d'effets "
    "sur une piste temporaire, y fait passer une impulsion (un échantillon à 0 dBFS), lit le résultat, coupe la fin "
    "silencieuse et enregistre un fichier WAV dans <b>REAPER/Data/RM IR</b>. La piste temporaire est ensuite supprimée : "
    "votre projet n'est pas modifié.",
    "DIAGRAM",
    "La méthode de l'impulsion est exacte pour les réverbes numériques. Ce qui varie dans le temps (modulation, chorus, "
    "« shimmer ») ou ce qui sature n'est pas capturé : l'IR garde une photo figée de la réverbe.",
   ]),
   ('2. Installation', [
    "IR Buddy est livré avec <b>RM1982Verb</b> (et ses 100 IR) : par <b>ReaPack</b> (dépôt ReNo Mellow, catégorie Reverb) ou "
    "en glissant <b>RM1982Verb.ReaperPkg</b> dans la fenêtre de REAPER (7.86+). Quatre actions apparaissent dans la liste d'actions "
    "(<b>Actions &gt; Show action list</b>) :",
    "TABLE_ACTIONS",
    "Donnez-leur un raccourci ou placez-les dans une barre d'outils si vous le souhaitez. Aucune extension n'est nécessaire.",
   ]),
   ('3. Préparer la réverbe', [
    "Créez une piste et insérez-y le plug-in de réverbe (vous pouvez ajouter d'autres effets après, un EQ par exemple : "
    "toute la chaîne est capturée). Réglez la réverbe ainsi :",
    "BUL:<b>100 % wet</b> (dry à zéro) : sinon le clic d'origine se retrouve au début de l'IR.",
    "BUL:<b>Modulation coupée ou faible</b> : elle ne se capture pas et peut rendre la queue granuleuse.",
    "BUL:<b>Pas de mode « freeze » ni « infinite »</b> : l'IR serait coupée à la longueur maximale.",
    "BUL:Le <b>predelay</b> de la réverbe est capturé. Vous pouvez aussi le mettre à zéro et le régler ensuite dans RM1982Verb.",
    "Les réglages de volume et de panoramique de la piste ne comptent pas : seuls les effets sont capturés. "
    "Le niveau n'a pas d'importance, RM1982Verb normalise chaque IR.",
   ]),
   ('4. Capturer', [
    "Sélectionnez la piste de la réverbe, puis lancez <b>ReNo Mellow - IR Buddy</b>. Une fenêtre de réglages s'ouvre ; "
    "ils sont mémorisés pour la fois suivante.",
    "TABLE_FIELDS",
    "Validez avec <b>OK</b>. Le calcul se fait hors temps réel, en une ou deux secondes. Un message indique le fichier créé, "
    "sa longueur, mono ou stéréo, et le délai avant le premier son. Si la queue était encore audible à la fin, "
    "il vous propose d'allonger la longueur maximale.",
    "Astuce : gardez la même piste et changez seulement le preset de la réverbe entre deux captures, avec un nouveau nom.",
   ]),
   ('5. Utiliser l\'IR dans RM1982Verb', [
    "Ouvrez RM1982Verb et <b>cliquez sur le nom de l'IR</b> : le <b>navigateur</b> s'ouvre, avec vos dossiers à gauche et "
    "leurs IR à droite (molette pour défiler, clic pour charger). Les flèches <b>&lt; &gt;</b> passent à l'IR précédente ou "
    "suivante du même dossier. Le navigateur lit un index qu'IR Buddy met à jour à chaque capture et à chaque ajout de dossier ; "
    "si vous copiez des fichiers à la main, lancez <b>Rescan RM IR</b>. La liste <b>IR file</b> au-dessus de la façade marche aussi. "
    "Vous pouvez aussi glisser le fichier WAV sur la fenêtre de RM1982Verb.",
    "Mettez <b>MIX</b> à 100 % si RM1982Verb est sur une piste de retour (send), et réglez ensuite ATTACK, DECAY, "
    "PREDELAY, WIDTH et l'EQ comme sur n'importe quelle réverbe.",
   ]),
   ('6. Ajouter votre propre dossier d\'IR', [
    "Vos IR sont déjà rangées ailleurs (un disque de sons, par exemple) ? Pas besoin de les copier. Lancez "
    "<b>ReNo Mellow - IR Buddy - Add IR folder</b>, choisissez le dossier, puis le nom qu'il aura dans la liste. "
    "IR Buddy crée dans REAPER/Data/RM IR un <b>lien</b> vers ce dossier (une jonction sous Windows, un lien symbolique "
    "sous macOS) : vos fichiers restent à leur place.",
    "Dans RM1982Verb, le bouton <b>dossier</b> au bout de la ligne de l'IR rappelle cette marche à suivre. "
    "Le dossier apparaît aussitôt dans le navigateur (clic sur le nom de l'IR).",
    "Pour le retirer, supprimez le raccourci dans REAPER/Data/RM IR (action <b>Open RM IR folder</b>) : seul le lien "
    "disparaît, vos fichiers ne sont pas touchés. Sous Windows, le lien ne fonctionne qu'avec un disque local, pas réseau. "
    "Avec l'extension js_ReaScriptAPI, vous choisissez directement le dossier ; sans elle, choisissez n'importe quel "
    ".wav à l'intérieur.",
   ]),
   ('7. Questions fréquentes', [
    "QA:« The FX chain returned silence »|La réverbe est sans doute contournée (bypass), hors ligne, ou son wet est à zéro. Avec un plug-in sur DSP externe (UAD…), le rendu hors temps réel donne du silence : IR Buddy propose alors de recommencer en temps réel (ou répondez Y à « Real time »).",
    "QA:L'IR commence par un clic sec|Le dry n'est pas à zéro : mettez la réverbe à 100 % wet et recommencez.",
    "QA:« both channels were identical »|La réverbe est mono : l'IR est enregistrée en mono, c'est normal.",
    "QA:Le premier son arrive tard|Predelay de la réverbe ou latence d'un plug-in : répondez Y à « Trim silence at start ».",
    "QA:Et une vraie pièce, ou une réverbe matérielle ?|IR Buddy capture les plug-ins. Pour une pièce ou un appareil "
    "analogique, on enregistre un balayage sinusoïdal puis on le convertit en IR (par exemple avec le logiciel gratuit "
    "REW, Room EQ Wizard) ; le WAV obtenu se range ensuite dans REAPER/Data/RM IR.",
   ]),
  ],
  actions=[('ReNo Mellow - IR Buddy', 'Capture les effets de la piste sélectionnée et enregistre l\'IR.'),
           ('ReNo Mellow - IR Buddy - Add IR folder', 'Ajoute un de vos dossiers d\'IR à la liste de RM1982Verb (par un lien).'),
           ('ReNo Mellow - IR Buddy - Rescan RM IR', 'Met à jour l\'index du navigateur de RM1982Verb (après un ajout de fichiers à la main).'),
           ('ReNo Mellow - IR Buddy - Open RM IR folder', 'Ouvre (et crée au besoin) le dossier REAPER/Data/RM IR.')],
  fields_head=('Réglage', 'Effet'),
  fields=[('IR name', "Nom du fichier. Proposé : le nom du premier effet actif."),
          ('Sub-folder of RM IR', "Sous-dossier de REAPER/Data/RM IR (par défaut « Plug-ins »). Vide = directement dans RM IR."),
          ('Max length (s)', "Longueur capturée, de 1 à 10 s. La fin silencieuse (-90 dB sous la crête) est coupée ensuite."),
          ('Output (S / M)', "S = stéréo (deux canaux), M = mono (somme des deux). Une réverbe mono donne toujours un fichier mono."),
          ('Trim silence at start (Y / N)', "Y retire le silence avant le premier son (predelay, latence). N garde le timing exact."),
          ('Real time (Y / N)', "Y = temps réel, pour les plug-ins sur DSP externe (UAD…) : l'impulsion passe par la piste de la réverbe et sa sortie est enregistrée (latence compensée, rien vers le master). N = hors temps réel, instantané.")],
  diag=('Piste de la réverbe', 'Piste temporaire', 'Data/RM IR/…/nom.wav', 'copie des effets', 'impulsion + rendu'),
 ),
 'en': dict(
  file='IRBuddy_manual_EN.pdf', other=('Version française', BASE + 'IRBuddy_manuel_FR.pdf'),
  sub='Capture the impulse response of a reverb plug-in for RM1982Verb',
  foot='ReNo Mellow - IR Buddy %s - manual' % VERSION,
  sections=[
   ('1. How it works', [
    "An <b>impulse response</b> (IR) is the sonic fingerprint of a reverb: what it sends back when you feed it one very "
    "short click. A convolution reverb such as <b>RM1982Verb</b> plays that fingerprint back on any sound.",
    "<b>IR Buddy</b> makes that fingerprint from the plug-ins of a track, in one click. It copies the FX chain to a "
    "temporary track, sends an impulse through it (one sample at 0 dBFS), reads the result, trims the silent end and "
    "saves a WAV file in <b>REAPER/Data/RM IR</b>. The temporary track is then deleted: your project is not changed.",
    "DIAGRAM",
    "The impulse method is exact for digital reverbs. Anything that moves over time (modulation, chorus, shimmer) or "
    "that saturates is not captured: the IR keeps a frozen snapshot of the reverb.",
   ]),
   ('2. Installation', [
    "IR Buddy comes with <b>RM1982Verb</b> (and its 100 IRs): through <b>ReaPack</b> (ReNo Mellow repository, Reverb category) or "
    "by dragging <b>RM1982Verb.ReaperPkg</b> into the REAPER window (7.86+). Four actions appear in the action list "
    "(<b>Actions &gt; Show action list</b>):",
    "TABLE_ACTIONS",
    "Give them a shortcut or put them on a toolbar if you like. No extension is required.",
   ]),
   ('3. Prepare the reverb', [
    "Create a track and insert the reverb plug-in (you may add other FX after it, an EQ for instance: the whole chain "
    "is captured). Set the reverb like this:",
    "BUL:<b>100 % wet</b> (dry off): otherwise the original click ends up at the start of the IR.",
    "BUL:<b>Modulation off or low</b>: it cannot be captured and can make the tail grainy.",
    "BUL:<b>No freeze or infinite mode</b>: the IR would be cut at the maximum length.",
    "BUL:The reverb's <b>predelay</b> is captured. You can also set it to zero and set it later in RM1982Verb.",
    "The track volume and pan do not matter: only the FX are captured. The level does not matter either, RM1982Verb "
    "normalizes every IR.",
   ]),
   ('4. Capture', [
    "Select the reverb track, then run <b>ReNo Mellow - IR Buddy</b>. A settings dialog opens; the settings are "
    "remembered for next time.",
    "TABLE_FIELDS",
    "Click <b>OK</b>. The render runs offline, in one or two seconds. A message shows the new file, its length, mono or "
    "stereo, and the delay before the first sound. If the tail was still audible at the end, it suggests a longer "
    "maximum length.",
    "Tip: to build a whole library, keep the same track and only change the reverb preset between captures "
    "(\"Large hall\", \"Bright plate\"…), with a new name each time.",
   ]),
   ('5. Use the IR in RM1982Verb', [
    "Open RM1982Verb and <b>click the IR name</b>: the <b>browser</b> opens, with your folders on the left and their IRs "
    "on the right (wheel to scroll, click to load). The <b>&lt; &gt;</b> arrows step to the previous or next IR of the same folder. "
    "The browser reads an index that IR Buddy updates after each capture and each added folder; if you copy files by hand, run "
    "<b>Rescan RM IR</b>. The <b>IR file</b> list above the panel works too. "
    "You can also drop the WAV file on the RM1982Verb window.",
    "Set <b>MIX</b> to 100 % when RM1982Verb sits on a return (send) track, then adjust ATTACK, DECAY, PREDELAY, WIDTH "
    "and the EQ as on any reverb.",
   ]),
   ('6. Add your own IR folder', [
    "Your IRs are already stored somewhere else (a sound drive, for instance)? No need to copy them. Run "
    "<b>ReNo Mellow - IR Buddy - Add IR folder</b>, choose the folder, then the name it will have in the list. "
    "IR Buddy creates in REAPER/Data/RM IR a <b>link</b> to that folder (a junction on Windows, a symbolic link on macOS): "
    "your files stay where they are.",
    "In RM1982Verb, the <b>folder</b> button at the end of the IR line reminds you of these steps. "
    "The folder shows right away in the browser (click the IR name).",
    "To remove it, delete the shortcut in REAPER/Data/RM IR (<b>Open RM IR folder</b> action): only the link goes away, "
    "your files are untouched. On Windows the link only works with a local drive, not a network drive. With the "
    "js_ReaScriptAPI extension you pick the folder directly; without it, pick any .wav inside it.",
   ]),
   ('7. FAQ', [
    "QA:\"The FX chain returned silence\"|The reverb is probably bypassed, offline, or its wet level is at zero. With a plug-in running on external DSP (UAD...), the offline render is silent: IR Buddy then offers to capture again in real time (or answer Y to \"Real time\").",
    "QA:The IR starts with a dry click|The dry signal is not off: set the reverb to 100 % wet and capture again.",
    "QA:\"both channels were identical\"|The reverb is mono: the IR is saved as mono, this is normal.",
    "QA:The first sound comes late|That is the reverb's predelay, or a plug-in latency. Answer Y to "
    "\"Trim silence at start\" to remove it.",
    "QA:What about a real room or a hardware reverb?|IR Buddy captures plug-ins. For a room or analog gear you record "
    "a sine sweep and convert it to an IR (for example with the free REW, Room EQ Wizard); then put the WAV in "
    "REAPER/Data/RM IR.",
   ]),
  ],
  actions=[('ReNo Mellow - IR Buddy', 'Captures the FX of the selected track and saves the IR.'),
           ('ReNo Mellow - IR Buddy - Add IR folder', 'Adds one of your IR folders to the RM1982Verb list (through a link).'),
           ('ReNo Mellow - IR Buddy - Rescan RM IR', 'Updates the index of the RM1982Verb browser (after adding files by hand).'),
           ('ReNo Mellow - IR Buddy - Open RM IR folder', 'Opens (and creates if needed) the REAPER/Data/RM IR folder.')],
  fields_head=('Setting', 'What it does'),
  fields=[('IR name', 'File name. Suggested: the name of the first active FX.'),
          ('Sub-folder of RM IR', 'Sub-folder of REAPER/Data/RM IR (default "Plug-ins"). Empty = straight into RM IR.'),
          ('Max length (s)', 'Captured length, 1 to 10 s. The silent end (-90 dB below the peak) is trimmed afterwards.'),
          ('Output (S / M)', 'S = stereo (two channels), M = mono (sum of both). A mono reverb always gives a mono file.'),
          ('Trim silence at start (Y / N)', 'Y removes the silence before the first sound (predelay, latency). N keeps the exact timing.'),
          ('Real time (Y / N)', 'Y = real-time capture, for plug-ins running on external DSP (UAD...) that return silence offline: the impulse plays on the reverb track itself (after the end of the project) and its output is recorded on a temporary track, latency compensated (nothing is sent to the master). N = offline render, instant.')],
  diag=('Reverb track', 'Temporary track', 'Data/RM IR/…/name.wav', 'FX copied', 'impulse + render'),
 ),
}

st_body = ParagraphStyle('b', fontName='DV', fontSize=8.8, leading=12, spaceAfter=4, textColor=DARK)
st_h = ParagraphStyle('h', fontName='DVB', fontSize=14, leading=18, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#2a9d8f'), keepWithNext=1)
st_bul = ParagraphStyle('u', parent=st_body, leftIndent=14, bulletIndent=4, spaceAfter=3)
st_cell = ParagraphStyle('c', fontName='DV', fontSize=9, leading=12, textColor=DARK)
st_cellb = ParagraphStyle('cb', fontName='DVB', fontSize=9, leading=12, textColor=DARK)
st_q = ParagraphStyle('q', fontName='DVB', fontSize=10, leading=14, spaceBefore=4, textColor=DARK, keepWithNext=1)

class Diagram(Flowable):
    def __init__(self, labels): super().__init__(); self.l = labels; self.width = 170*mm; self.height = 22*mm
    def draw(self):
        c = self.canv; w = 48*mm; h = 14*mm; y = 3*mm; xs = [0, 61*mm, 122*mm]
        for i, x in enumerate(xs):
            c.setFillColor(colors.HexColor('#24272c') if i < 2 else ACC); c.roundRect(x, y, w, h, 3*mm, fill=1, stroke=0)
            c.setFillColor(colors.white if i < 2 else DARK); c.setFont('DVB', 9); c.drawCentredString(x + w/2, y + h/2 - 3, self.l[i])
        c.setStrokeColor(GREY); c.setFillColor(GREY); c.setLineWidth(1.2)
        for i in range(2):
            x0 = xs[i] + w + 1.5*mm; x1 = xs[i+1] - 1.5*mm; yy = y + h/2
            c.line(x0, yy, x1 - 2*mm, yy)
            p = c.beginPath(); p.moveTo(x1, yy); p.lineTo(x1 - 2.5*mm, yy + 1.5*mm); p.lineTo(x1 - 2.5*mm, yy - 1.5*mm); p.close(); c.drawPath(p, fill=1, stroke=0)
            c.setFont('DV', 7.5); c.drawCentredString((x0 + x1)/2, y + h + 2.5*mm, self.l[3 + i])

def tbl(rows, head, widths):
    data = [[Paragraph(head[0], st_cellb), Paragraph(head[1], st_cellb)]] + [[Paragraph(a, st_cellb), Paragraph(b, st_cell)] for a, b in rows]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), ACC), ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c9ccd1')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f4f6')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    return t

def build(lang):
    L = T[lang]
    def deco(c, d):
        c.saveState(); c.setFillColor(ACC); c.rect(0, A4[1] - 6*mm, A4[0], 6*mm, fill=1, stroke=0)
        c.setFont('DV', 8); c.setFillColor(GREY); c.drawString(20*mm, 10*mm, L['foot'])
        c.drawRightString(A4[0] - 20*mm, 10*mm, str(d.page)); c.restoreState()
    doc = BaseDocTemplate(L['file'], pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=16*mm,
                          title='IR Buddy', author='ReNo Mellow')
    doc.addPageTemplates([PageTemplate(frames=[Frame(18*mm, 16*mm, A4[0] - 36*mm, A4[1] - 31*mm, id='f')], onPage=deco)])
    s = []
    s.append(Paragraph('ReNo Mellow', ParagraphStyle('k', fontName='DVB', fontSize=10, textColor=GREY)))
    s.append(Paragraph('IR Buddy', ParagraphStyle('t', fontName='DVB', fontSize=24, leading=28, textColor=DARK)))
    s.append(Paragraph(L['sub'], ParagraphStyle('s', fontName='DV', fontSize=12, leading=16, textColor=GREY, spaceAfter=4)))
    s.append(Paragraph('Version %s &nbsp;·&nbsp; <link href="%s" color="#2a9d8f">%s</link>' % (VERSION, L['other'][1], L['other'][0]),
                       ParagraphStyle('v', fontName='DV', fontSize=9, textColor=GREY, spaceAfter=8)))
    for title, paras in L['sections']:
        block = [Paragraph(title, st_h)]
        first = True
        for p in paras:
            if p == 'DIAGRAM': el = Diagram(L['diag'])
            elif p == 'TABLE_ACTIONS': el = tbl(L['actions'], ('Action', ''), [70*mm, 100*mm])
            elif p == 'TABLE_FIELDS': el = tbl(L['fields'], L['fields_head'], [50*mm, 120*mm])
            elif p.startswith('BUL:'): el = Paragraph(p[4:], st_bul, bulletText='•')
            elif p.startswith('QA:'):
                q, a = p[3:].split('|', 1); s.append(Paragraph(q, st_q)) if not first else block.append(Paragraph(q, st_q)); el = Paragraph(a, st_body)
            else: el = Paragraph(p, st_body)
            if first: block.append(el); s.extend(block); first = False
            else: s.append(el)
            if p.startswith('TABLE') or p == 'DIAGRAM': s.append(Spacer(1, 6))
    doc.build(s)

for lg in ('fr', 'en'): build(lg)
