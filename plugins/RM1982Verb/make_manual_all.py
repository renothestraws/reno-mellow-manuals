# Manuel unique RM1982Verb + IR Buddy (FR / EN) : reprend les textes de make_manual_verb.py et make_manual.py
import re, sys
sys.path.insert(0, '/home/claude/irbuddy')
ns_v, ns_i = {}, {}
src_v = open('/home/claude/irbuddy/make_manual_verb.py').read().replace("for L in (FR, EN): build(L)", "")
src_i = open('/home/claude/irbuddy/make_manual.py').read().replace("for lg in ('fr', 'en'): build(lg)", "")
exec(src_v, ns_v); exec(src_i, ns_i)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, PageBreak

V = ns_v; I = ns_i
BASE = V['BASE']
PART = {'fr': ("Partie 2 — IR Buddy : créer vos propres IR",
               "IR Buddy est un paquet séparé, commun avec RMampsim (voir Installation). Ses actions se trouvent dans la liste d'actions (<b>Actions &gt; Show action list</b>) ; "
               "donnez-leur un raccourci ou placez-les dans une barre d'outils si vous le souhaitez."),
        'en': ("Part 2 — IR Buddy: make your own IRs",
               "IR Buddy is a separate package, shared with RMampsim (see Installation). Its actions are in the action list (<b>Actions &gt; Show action list</b>); "
               "give them a shortcut or put them on a toolbar if you like.")}
PART1 = {'fr': "Partie 1 — RM1982Verb", 'en': "Part 1 — RM1982Verb"}
SUB = {'fr': "Réverbération à convolution pour REAPER, série 1982, et son script IR Buddy",
       'en': "Convolution reverb for REAPER, 1982 series, and its IR Buddy script"}
FOOT = {'fr': "ReNo Mellow - RM1982Verb %s + IR Buddy - manuel" % V['VERSION'], 'en': "ReNo Mellow - RM1982Verb %s + IR Buddy - manual" % V['VERSION']}
FILES = {'fr': ('RM1982Verb_manuel_FR.pdf', ('English version', BASE + 'RM1982Verb_manual_EN.pdf')),
         'en': ('RM1982Verb_manual_EN.pdf', ('Version française', BASE + 'RM1982Verb_manuel_FR.pdf'))}
st_part = ParagraphStyle('part', fontName='DVB', fontSize=17, leading=22, spaceBefore=6, spaceAfter=4, textColor=colors.HexColor('#1d1f23'), keepWithNext=1)

from reportlab.platypus import Table, TableStyle
CALL = {'fr': ("<b>À NE PAS OUBLIER : « ReNo Mellow - IR Buddy - Rescan RM IR »</b>",
               "Cette action met à jour la liste du navigateur d'IR de RM1982Verb. Lancez-la : "
               "<b>1.</b> une fois après l'installation par ReaPack ; "
               "<b>2.</b> chaque fois que vous copiez, renommez ou supprimez des IR à la main dans REAPER/Data/RM IR ; "
               "<b>3.</b> si le navigateur affiche « No IR index yet » ou « Cannot open the file ». "
               "Une capture et l'action Add IR folder la lancent automatiquement."),
        'en': ("<b>DON'T FORGET: \"ReNo Mellow - IR Buddy - Rescan RM IR\"</b>",
               "This action updates the list of the RM1982Verb IR browser. Run it: "
               "<b>1.</b> once after installing through ReaPack; "
               "<b>2.</b> every time you copy, rename or delete IRs by hand in REAPER/Data/RM IR; "
               "<b>3.</b> when the browser shows \"No IR index yet\" or \"Cannot open the file\". "
               "A capture and the Add IR folder action run it automatically.")}
def callout(lg):
    W = A4[0] - 36*mm
    t = Table([[Paragraph(CALL[lg][0], ParagraphStyle('ct', fontName='DVB', fontSize=10.5, leading=14, textColor=V['DARK']))],
               [Paragraph(CALL[lg][1], ParagraphStyle('cb', fontName='DV', fontSize=9, leading=12.5, textColor=V['DARK']))]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dff7f3')), ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2a9d8f')),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    return [Spacer(1, 4), t, Spacer(1, 6)]
LG = ['fr']
def body(L, sections, kind, start, tblf, Lfull=None):
    out = []; n = start
    for title, paras in sections:
        t = re.sub(r'^\d+\.\s*', '', title)
        if kind == 'i' and t in ('Installation',):
            continue
        out.append(Paragraph('%d. %s' % (n, t), V['st_h'] if not (paras and paras[0] == 'TABLE') else ParagraphStyle('h2', parent=V['st_h'], keepWithNext=0)))
        n += 1
        for p in paras:
            if kind == 'v':
                p = p.replace("(manuel IR Buddy séparé)", "(voir la partie 2)").replace("(separate IR Buddy manual)", "(see part 2)")
            if p == 'IMAGE':
                W = A4[0] - 36*mm
                out.append(Image(V['IMG'], width=W*0.8, height=W*0.8*470/1220)); out.append(Paragraph(L['cap'], V['st_cap']))
            elif p == 'TABLE': out.append(V['tbl'](L['hd'], L['rows'], [30*mm, 34*mm, A4[0] - 36*mm - 64*mm]))
            elif p == 'TABLE2': out.append(V['tbl'](L['hd2'], L['rows2'], [62*mm, A4[0] - 36*mm - 62*mm]))
            elif p == 'DIAGRAM': out.append(I['Diagram'](Lfull['diag'])); out.append(Spacer(1, 4))
            elif p == 'TABLE_ACTIONS': out.append(I['tbl'](Lfull['actions'], ('Action', ''), [70*mm, A4[0] - 36*mm - 70*mm]))
            elif p == 'TABLE_FIELDS': out.append(I['tbl'](Lfull['fields'], Lfull['fields_head'], [50*mm, A4[0] - 36*mm - 50*mm]))
            elif p.startswith('BUL:'): out.append(Paragraph(p[4:], V['st_bul'], bulletText='•'))
            elif p.startswith('QA:') and kind == 'v' and ('Cannot open the file' in p or 'No IR index yet' in p): continue
            elif p.startswith('QA:'):
                q, a = p[3:].split('|', 1); out.append(Paragraph(q, V['st_q'])); out.append(Paragraph(a, V['st_body']))
            else: out.append(Paragraph(p, V['st_body']))
            if p.startswith('TABLE'): out.append(Spacer(1, 4))
        if kind == 'v' and t == 'Installation': out += callout(LG[0])
    return out, n

def build(lg):
    LV = V['FR'] if lg == 'fr' else V['EN']; LI = I['T'][lg]
    LG[0] = lg
    fn, other = FILES[lg]
    def deco(c, d):
        c.saveState(); c.setFillColor(V['ACC']); c.rect(0, A4[1] - 6*mm, A4[0], 6*mm, fill=1, stroke=0)
        c.setFont('DV', 8); c.setFillColor(V['GREY']); c.drawString(18*mm, 10*mm, FOOT[lg])
        c.drawRightString(A4[0] - 18*mm, 10*mm, str(d.page)); c.restoreState()
    doc = BaseDocTemplate(fn, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=16*mm,
                          title='RM1982Verb + IR Buddy', author='ReNo Mellow')
    doc.addPageTemplates([PageTemplate(frames=[Frame(18*mm, 16*mm, A4[0] - 36*mm, A4[1] - 31*mm, id='f')], onPage=deco)])
    s = [Paragraph('ReNo Mellow', ParagraphStyle('k', fontName='DVB', fontSize=10, textColor=V['GREY'])),
         Paragraph('RM1982Verb + IR Buddy', ParagraphStyle('t', fontName='DVB', fontSize=24, leading=28, textColor=V['DARK'])),
         Paragraph(SUB[lg], ParagraphStyle('s', fontName='DV', fontSize=12, leading=16, textColor=V['GREY'], spaceAfter=4)),
         Paragraph('Version %s &nbsp;·&nbsp; <link href="%s" color="#2a9d8f">%s</link>' % (V['VERSION'], other[1], other[0]),
                   ParagraphStyle('v', fontName='DV', fontSize=9, textColor=V['GREY'], spaceAfter=6)),
         Paragraph(PART1[lg], st_part)]
    part1, n = body(LV, LV['S'], 'v', 1, None)
    s += part1
    s.append(PageBreak())
    s.append(Paragraph(PART[lg][0], st_part)); s.append(Paragraph(PART[lg][1], V['st_body']))
    s.append(I['tbl'](LI['actions'], ('Action', ''), [70*mm, A4[0] - 36*mm - 70*mm])); s.append(Spacer(1, 4))
    s += callout(lg)
    part2, _ = body(LV, LI['sections'], 'i', n, None, LI)
    s += part2
    doc.build(s)

for lg in ('fr', 'en'): build(lg)
