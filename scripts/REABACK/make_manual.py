# Generates the REABACK user manual, French and English
# (scripts/REABACK/REABACK_manuel_FR.pdf and REABACK_manual_EN.pdf).
# Usage: python3 make_manual.py [output folder]
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, ListFlowable, ListItem, Image)
from reportlab.platypus.tableofcontents import TableOfContents

VERSION = "1.3"
NAME = "REABACK"
FOLDER = "REABACK"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/REABACK/"
URL_FR = BASE + "REABACK_manuel_FR.pdf"
URL_EN = BASE + "REABACK_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/REABACK.ReaperPkg"
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
    "title": ParagraphStyle("title", fontName="DVB", fontSize=30, leading=36, alignment=TA_CENTER, textColor=DARK),
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
    "file": "REABACK_manuel_FR.pdf",
    "sub": "Lancer ses backing tracks sur scène : une chanson = une région mère",
    "manual": "Manuel d'utilisation",
    "other": 'English version: <link href="%s" color="blue">%s</link>' % (URL_EN, "REABACK_manual_EN.pdf"),
    "toc": "Sommaire",
    "footer": "manuel",
    "page": "page",
    "cap": "Schéma simplifié",
    "head2": ("Élément", "Effet"),
    "head_g": ("Geste", "Effet"),
    "head_b": ("Bouton", "Effet"),
    "body": [
        ("h1", "1. Principe"),
        ("p", "REABACK transforme un projet REAPER en <b>setlist de scène</b>. Chaque chanson est une <b>région "
              "mère</b> placée sur la timeline ; REABACK les liste dans l'ordre du concert, leur donne les numéros "
              "1, 2, 3..., et permet de lancer un playback, de passer au suivant ou de revenir au précédent."),
        ("p", "L'ensemble comprend : la <b>fenêtre REABACK</b> (liste des régions et transport), des <b>actions "
              "isolées</b> pour un pédalier ou un clavier MIDI, une <b>page de télécommande</b> pour smartphone, un "
              "<b>prompteur</b> de paroles et d'accords pour tablette, la fenêtre <b>Reaback Set up</b> (préparation "
              "de la session), un <b>project template</b> et des <b>icônes</b> de barre d'outils."),
        ("h1", "2. Installation"),
        ("p", "<b>Prérequis :</b> REAPER et l'extension <b>ReaImGui</b> (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, dans ReaTeam Extensions), puis redémarrer REAPER. L'extension <b>SWS</b> est "
              "conseillée (Count-in, navigation de secours) ; <b>js_ReaScriptAPI</b> est optionnelle (fenêtre « Save "
              "as » de l'export .txt)."),
        ("h2", "Avec ReaPack (recommandé, mises à jour automatiques)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, puis coller l'adresse :<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, chercher « REABACK », clic droit &gt; Install, puis Apply.",
                "Les mises à jour : Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("p", "ReaPack installe les scripts (et les ajoute à la liste d'actions), les pages web dans "
              "<b>reaper_www_root</b>, le template <b>ReaBack</b> dans ProjectTemplates et les icônes de barre d'outils."),
        ("h2", "Avec le paquet .ReaperPkg (REAPER 7.86 et plus)"),
        ("p", "Télécharger le paquet :<br/><font size=8>%s</font><br/>puis le glisser dans REAPER. Pas de mise à jour "
              "automatique." % URL_PKG),
        ("h2", "Installation manuelle"),
        ("p", "Télécharger le dossier <b>REABACK</b> du dépôt, puis charger et lancer <b>REABACK_Install.lua</b> dans "
              "la liste d'actions (Actions &gt; Show action list &gt; New action &gt; Load ReaScript). Il copie les "
              "scripts, les pages web, le template et les icônes."),
        ("h1", "3. Préparer le projet"),
        ("p", "Pour commencer une session : <b>File &gt; Project templates &gt; ReaBack</b>. Le template contient les "
              "pistes <b>Video</b> et <b>Image</b>, <b>Lyrics</b>, <b>Chords</b>, <b>Comment</b>, <b>Timecode</b>, "
              "<b>Click</b>, <b>Cues</b>, 16 pistes <b>Stems</b> et 4 pistes <b>MIDI</b>, ainsi que deux lignes de "
              "règle de régions : <b>Song</b> (les chansons) et <b>Structure</b> (les parties)."),
        ("p", "Placer une <b>région par chanson</b>, couvrant tout le morceau : c'est elle que REABACK lance. "
              "Laisser un peu d'espace entre deux chansons."),
        ("draw", "nested"),
        ("p", "Pour repérer les parties d'un morceau (couplet, refrain, solo), créer des régions <b>à l'intérieur</b> "
              "de la région mère : elles sont <b>imbriquées</b> (régions filles). Elles appartiennent à la chanson et "
              "ne comptent pas dans la setlist. Une région fille doit être strictement contenue dans sa mère ; un seul "
              "niveau d'imbrication est géré."),
        ("h1", "4. La fenêtre REABACK"),
        ("p", "Lancer l'action <b>REABACK</b> (icône de barre d'outils, allumée tant que la fenêtre est ouverte)."),
        ("draw", "window"),
        ("table_b", [
            ("Previous / Next", "Chanson précédente / suivante (les chansons désactivées sont ignorées)."),
            ("Play/Stop", "Lance la lecture ; en lecture, voir section 8."),
            ("Stop", "En lecture : arrêt. Sans lecture : le curseur revient au début de la sélection temporelle."),
            ("Metronome", "Active ou coupe le métronome de REAPER."),
            ("Count-in", "Active ou coupe le compte avant la lecture (action SWS)."),
            ("Auto stop", "Arrête la lecture à la fin de la sélection si la boucle est coupée."),
            ("Smooth seek", "Les changements de chanson attendent la fin de la mesure au lieu de couper net."),
            ("Live loop", "Boucle la partie en cours (section 9)."),
            ("Zoom all", "Affiche tout le projet dans l'arrangement."),
            ("Apply IDs / Reset order / Export .txt", "Renumérote les régions, annule l'ordre non appliqué, exporte la liste."),
        ]),
        ("p", "Les boutons Metronome, Count-in, Auto stop, Smooth seek et Live loop passent en vert clair quand ils "
              "sont actifs."),
        ("h1", "5. La liste des régions"),
        ("p", "Une ligne par chanson. Colonnes : <b>ID</b> (numéro actuel), <b>Name</b>, <b>Comment</b> (note libre à "
              "taper dans la case), <b>Duration</b> (le total, hors chansons désactivées, est affiché en bas) et "
              "<b>New ID</b> (numéro qui sera donné par Apply IDs, en orange quand il change)."),
        ("h2", "Couleurs"),
        ("table2", [
            ("Nom jaune, plus grand", "La chanson en cours de lecture."),
            ("Vert, italique", "Chanson couverte par la sélection temporelle (prête à jouer)."),
            ("Rouge, barré, « OFF »", "Chanson désactivée."),
            ("Bleu, « (n nested) »", "Région mère qui contient n régions imbriquées."),
        ]),
        ("h2", "Gestes à la souris"),
        ("table_g", [
            ("Clic", "Sélectionne la chanson et place la sélection temporelle dessus (seek fluide si la lecture tourne)."),
            ("Double-clic", "Lance la lecture de la chanson."),
            ("Shift+clic", "Renomme la chanson."),
            ("Ctrl+clic", "Zoom horizontal sur la chanson."),
            ("Alt+clic", "Désactive la chanson ; un nouvel Alt+clic la réactive."),
            ("Glisser-déposer", "Change l'ordre de la setlist (les régions filles suivent leur mère)."),
        ]),
        ("h1", "6. Construire la setlist"),
        ("p", "L'ordre de la liste devient l'ordre des ID quand on clique sur <b>Apply IDs</b>. Exemple : on glisse "
              "« Nuit blanche » en tête, la colonne New ID passe en orange, puis Apply IDs réécrit les numéros des "
              "régions dans REAPER. <b>Reset order</b> annule les déplacements non appliqués."),
        ("p", "<b>Régions filles :</b> leur ID est celui de la mère multiplié par 100, plus leur rang. Si la chanson 2 "
              "contient Couplet, Refrain et Solo, ils reçoivent 201, 202 et 203 ; si la chanson passe en position 1, "
              "ils deviennent 101, 102 et 103."),
        ("p", "<b>Limite :</b> les ID calculés doivent rester inférieurs à 10000. Au-delà, un avertissement rouge "
              "s'affiche et Apply IDs refuse de s'exécuter."),
        ("h1", "7. Désactiver, renommer, commenter"),
        ("p", "<b>Alt+clic</b> retire une chanson du set de ce soir sans la supprimer : elle devient rouge barrée, "
              "reçoit un ID à partir de 10000 (affiché « OFF »), sort des numéros et des durées, et ne peut plus être "
              "sélectionnée ni lancée (elle reste déplaçable). Penser à Apply IDs pour renuméroter les autres. "
              "<b>Shift+clic</b> ouvre « Rename region » (OK / Cancel, Entrée / Échap). La colonne <b>Comment</b> garde "
              "une note par chanson (« capo 3 », « départ batterie seule »), enregistrée dans le projet."),
        ("h2", "Sets de régions"),
        ("p", "Un <b>set</b> mémorise toute la configuration (ordre, noms, régions actives ou non, commentaires) sous "
              "un nom : « Concert complet », « Festival 40 min »... Saisir un nom puis <b>Save set</b> ; choisir un set "
              "dans la liste, puis <b>Load</b> ou <b>Delete set</b>. La case « Apply IDs immediately when loading a "
              "set » renumérote dès le chargement. Les régions sont mémorisées en entier : une chanson supprimée entre "
              "temps est recréée au chargement. Les sets sont dans le fichier du projet : l'enregistrer."),
        ("h1", "8. Le transport sur scène"),
        ("table_b", [
            ("Play/Stop", "Sans lecture : lance. En lecture avec boucle : coupe la boucle et place la sélection "
                          "temporelle sur la chanson mère en cours (elle se joue jusqu'à sa fin). En lecture sans "
                          "boucle : arrête."),
            ("Stop", "En lecture : arrêt (action 40328). Sans lecture : retour au début de la sélection temporelle."),
            ("Previous / Next", "Chanson précédente / suivante, avec Smooth seek si activé."),
        ]),
        ("p", "<b>Scénario type :</b> activer Auto stop et Smooth seek (et Count-in si le batteur démarre sur le clic) ; "
              "cliquer sur la chanson, Play/Stop ; à la fin, Auto stop arrête ; Next puis Play/Stop pour la suivante. "
              "Si le chanteur veut prolonger un refrain, laisser la boucle active, puis Play/Stop quand il est prêt."),
        ("h1", "9. Live loop"),
        ("p", "<b>Live loop</b> boucle la partie en cours. Boucle coupée : le clic active la boucle et place la "
              "sélection temporelle sur la <b>région fille</b> à la position courante (la région mère s'il n'y en a "
              "pas). Boucle active : le clic coupe la boucle et remet la sélection sur la région mère. La position "
              "est celle de la lecture, ou du curseur d'édition à l'arrêt. Hors d'une chanson, rien ne se passe."),
        ("h1", "10. Actions isolées et raccourcis"),
        ("p", "Cinq scripts indépendants de la fenêtre, à associer à un raccourci clavier ou MIDI (pédalier) dans la "
              "liste d'actions ; ils ignorent les chansons désactivées. Les raccourcis sont à choisir librement : "
              "ceux de ce manuel sont des exemples."),
        ("table2", [
            ("REABACK_PlayStop", "Équivalent de Play/Stop (allumé pendant la lecture)."),
            ("REABACK_Stop", "Équivalent de Stop."),
            ("REABACK_Previous / REABACK_Next", "Chanson précédente / suivante."),
            ("REABACK_LiveLoop", "Équivalent de Live loop (allumé quand la boucle est active)."),
        ]),
        ("p", "Exemple : un pédalier à 4 pédales sur le canal 1 : pédale 1 Previous, 2 Play/Stop, 3 Next, 4 Stop."),
        ("h1", "11. Télécommande par smartphone"),
        ("p", "La page <b>REABACK.html</b> affiche la setlist sur un téléphone relié au même réseau que "
              "l'ordinateur de scène, via l'interface web de REAPER."),
        ("ol", ["Preferences &gt; Control/OSC/web &gt; Add &gt; Web browser interface ; noter le port.",
                "Laisser la fenêtre REABACK ouverte dans REAPER (elle publie la liste).",
                "Sur le téléphone, ouvrir <font size=8>http://&lt;adresse IP de l'ordinateur&gt;:&lt;port&gt;/REABACK.html</font>."]),
        ("p", "En mode normal : état (« Playing / loop »), Previous, Play/Stop, Stop, Next, Metronome, Count-in, "
              "Auto stop, Smooth seek, Follow et Live loop ; toucher = sélectionner, double-toucher = lancer. Le bouton "
              "<b>Edit</b> ajoute : flèches ▲/▼ pour déplacer, Rename, Disable/Enable, Comment, Apply IDs, Reset "
              "order, Export .txt et les sets. Le laisser fermé pendant le concert. Si le script REABACK n'est pas "
              "lancé, la page le signale ; le transport de base fonctionne quand même."),
        ("h1", "12. Le prompteur (tablette)"),
        ("p", "Le prompteur affiche en temps réel les <b>notes d'items</b> de trois pistes : celle dont le nom contient "
              "<b>Lyrics</b> (en <b>jaune</b>), <b>Chords</b> (en <b>rouge</b>) et <b>Comment</b> (en <b>blanc "
              "italique</b>), pendant la durée de chaque item. Il affiche aussi, en haut, le nom de la <b>région "
              "mère</b> en cours et, dessous, celui de la <b>région fille</b>."),
        ("draw", "prompter"),
        ("ol", ["Copier <b>Reaback-prompter.html</b> dans reaper_www_root (ReaPack le fait) et activer l'interface web.",
                "Lancer l'action <b>Reaback-prompter</b> (en arrière-plan, sans fenêtre ; la relancer l'arrête).",
                "Sur la tablette : <font size=8>http://&lt;adresse IP&gt;:&lt;port&gt;/Reaback-prompter.html</font>."]),
        ("p", "En bas : boutons <b>Lyrics</b>, <b>Chords</b>, <b>Comment</b> pour choisir ce qui reste à l'écran, "
              "<b>Next</b> (aperçu en pâle de l'item suivant), <b>A-</b> / <b>A+</b> (taille du texte) et plein écran ; "
              "un toucher sur le texte masque ou réaffiche la barre. Deux voyants en haut à droite : <b>PLAY</b> "
              "(vert), <b>PAUSE</b> (orange), <b>REC</b> (rouge) ou <b>STOP</b>, et <b>LOOP</b> (bleu) quand la boucle "
              "est active. À l'arrêt, le prompteur suit le curseur d'édition."),
        ("h1", "13. Reaback Set up"),
        ("p", "Fenêtre de raccourcis pour préparer la session. Chaque bouton cherche son action par son nom, puis par "
              "son numéro ; survoler un bouton montre l'action utilisée, et la ligne du bas indique ce qui a été "
              "exécuté."),
        ("h2", "Configuration"),
        ("p", "Audio device settings, MIDI devices (entrées, sorties : même page de REAPER), Web control surface, "
              "Project settings, Metronome settings, Routing matrix, Video window, External synchronization settings."),
        ("h2", "Session Built"),
        ("table2", [
            ("Project templates / Open project / Save project as...", "Fenêtres de REAPER correspondantes."),
            ("Media explorer", "Ouvre ou ferme le Media explorer."),
            ("Normalize", "Normalise les items sélectionnés."),
            ("Insert tempo change marker", "Marqueur de tempo au curseur d'édition."),
            ("Time selection to selected items", "Sélection temporelle sur les items sélectionnés."),
            ("Region from time selection", "Crée une région sur la sélection temporelle."),
            ("Lyrics / Chords / Comment item + notes", "Crée un item vide sur la sélection temporelle, sur la piste "
                          "dont le nom contient Lyrics / Chords / Comment, ouvre ses notes, puis décale la sélection "
                          "temporelle vers la droite de sa longueur : on enchaîne les lignes."),
            ("MIDI item + MIDI editor", "Item MIDI vide sur la sélection, sur la piste sélectionnée, ouvert dans "
                          "l'éditeur MIDI (docké, synchronisé à l'arrangement si l'action existe)."),
            ("Timecode track", "Piste dont le nom contient Timecode : vidée, sans envoi au master, timecode generator "
                          "sur tout le projet, propriétés de la source ouvertes."),
            ("Lock / Unlock items of the region", "Verrouille ou déverrouille les items de la région la plus large "
                          "sous le curseur d'édition."),
            ("Windows set manager", "Fenêtre des window sets (screensets) de REAPER."),
        ]),
        ("h1", "14. Icônes et questions fréquentes"),
        ("p", "Huit icônes (trois états : normal, survol, actif) sont installées dans Data/toolbar_icons : clic droit "
              "sur une barre d'outils &gt; Customize toolbar &gt; Choose icon, puis l'icône du même nom. Redémarrer "
              "REAPER si elles n'apparaissent pas. Les icônes s'allument selon l'état : fenêtres REABACK, Set up et "
              "prompteur tant qu'ils tournent, Play/Stop en lecture, Live loop quand la boucle est active."),
        ("qa", [
            ("La fenêtre ne s'ouvre pas.", "ReaImGui n'est pas installé : l'installer via ReaPack et redémarrer REAPER."),
            ("Le bouton Count-in ne fait rien.", "SWS n'est pas installé ou l'action n'existe pas dans votre version."),
            ("Apply IDs refuse.", "Un ID calculé dépasse 9999 (avertissement rouge) : réduire les chansons ou les imbrications."),
            ("Une partie est traitée comme une chanson.", "Elle dépasse de sa mère ou partage ses bornes : la rentrer strictement dedans."),
            ("Next ne trouve plus une chanson.", "Elle est désactivée (rouge barré) : Alt+clic pour la réactiver."),
            ("La page smartphone / le prompteur n'affichent rien.", "Le script REABACK / Reaback-prompter n'est pas lancé dans REAPER."),
            ("Les retours à la ligne des notes s'affichent mal.", "Mettre à jour vers la version 1.3 (le prompteur y décode correctement le texte)."),
        ]),
    ],
}

T["en"] = {
    "file": "REABACK_manual_EN.pdf",
    "sub": "Launch your backing tracks on stage: one song = one parent region",
    "manual": "User manual",
    "other": 'Version française : <link href="%s" color="blue">%s</link>' % (URL_FR, "REABACK_manuel_FR.pdf"),
    "toc": "Contents",
    "footer": "manual",
    "page": "page",
    "cap": "Simplified drawing",
    "head2": ("Item", "Effect"),
    "head_g": ("Gesture", "Effect"),
    "head_b": ("Button", "Effect"),
    "body": [
        ("h1", "1. Concept"),
        ("p", "REABACK turns a REAPER project into a <b>stage setlist</b>. Each song is a <b>parent region</b> on the "
              "timeline; REABACK lists them in concert order, numbers them 1, 2, 3..., and lets you start a backing "
              "track, jump to the next one or go back to the previous one."),
        ("p", "The package includes: the <b>REABACK window</b> (region list and transport), <b>stand-alone actions</b> "
              "for a MIDI footswitch or keyboard, a <b>remote-control page</b> for smartphones, a lyrics and chords "
              "<b>prompter</b> for tablets, the <b>Reaback Set up</b> window (session preparation), a <b>project "
              "template</b> and toolbar <b>icons</b>."),
        ("h1", "2. Installation"),
        ("p", "<b>Requirements:</b> REAPER and the <b>ReaImGui</b> extension (Extensions &gt; ReaPack &gt; Browse "
              "packages &gt; ReaImGui, in ReaTeam Extensions), then restart REAPER. The <b>SWS</b> extension is "
              "recommended (Count-in, fallback navigation); <b>js_ReaScriptAPI</b> is optional (« Save as » window of "
              "the .txt export)."),
        ("h2", "With ReaPack (recommended, automatic updates)"),
        ("ol", ["Extensions &gt; ReaPack &gt; Import repositories, then paste the address:<br/>"
                "<font size=8>%s</font>" % URL_INDEX,
                "Extensions &gt; ReaPack &gt; Browse packages, search « REABACK », right-click &gt; Install, then Apply.",
                "Updates: Extensions &gt; ReaPack &gt; Synchronize packages."]),
        ("p", "ReaPack installs the scripts (and adds them to the action list), the web pages in "
              "<b>reaper_www_root</b>, the <b>ReaBack</b> template in ProjectTemplates and the toolbar icons."),
        ("h2", "With the .ReaperPkg package (REAPER 7.86 and later)"),
        ("p", "Download the package:<br/><font size=8>%s</font><br/>then drag it into REAPER. No automatic "
              "updates." % URL_PKG),
        ("h2", "Manual installation"),
        ("p", "Download the <b>REABACK</b> folder of the repository, then load and run <b>REABACK_Install.lua</b> in the "
              "action list (Actions &gt; Show action list &gt; New action &gt; Load ReaScript). It copies the scripts, "
              "the web pages, the template and the icons."),
        ("h1", "3. Preparing the project"),
        ("p", "To start a session: <b>File &gt; Project templates &gt; ReaBack</b>. The template contains the "
              "<b>Video</b> and <b>Image</b>, <b>Lyrics</b>, <b>Chords</b>, <b>Comment</b>, <b>Timecode</b>, "
              "<b>Click</b> and <b>Cues</b> tracks, 16 <b>Stems</b> tracks and 4 <b>MIDI</b> tracks, plus two region "
              "ruler lanes: <b>Song</b> (the songs) and <b>Structure</b> (the parts)."),
        ("p", "Put <b>one region per song</b>, covering the whole track: this is what REABACK launches. Leave a little "
              "space between two songs."),
        ("draw", "nested"),
        ("p", "To mark the parts of a song (verse, chorus, solo), create regions <b>inside</b> the parent region: they "
              "are <b>nested</b> (child regions). They belong to the song and do not count in the setlist. A child "
              "region must be strictly inside its parent; only one nesting level is handled."),
        ("h1", "4. The REABACK window"),
        ("p", "Run the <b>REABACK</b> action (toolbar icon, lit while the window is open)."),
        ("draw", "window"),
        ("table_b", [
            ("Previous / Next", "Previous / next song (disabled songs are skipped)."),
            ("Play/Stop", "Starts playback; during playback, see section 8."),
            ("Stop", "While playing: stop. When stopped: the cursor returns to the start of the time selection."),
            ("Metronome", "Turns REAPER's metronome on or off."),
            ("Count-in", "Turns the count-in before playback on or off (SWS action)."),
            ("Auto stop", "Stops playback at the end of the selection when repeat is off."),
            ("Smooth seek", "Song changes wait for the end of the measure instead of cutting."),
            ("Live loop", "Loops the current part (section 9)."),
            ("Zoom all", "Shows the whole project in the arrange view."),
            ("Apply IDs / Reset order / Export .txt", "Renumber the regions, cancel the pending order, export the list."),
        ]),
        ("p", "Metronome, Count-in, Auto stop, Smooth seek and Live loop turn light green when active."),
        ("h1", "5. The region list"),
        ("p", "One row per song. Columns: <b>ID</b> (current number), <b>Name</b>, <b>Comment</b> (free note, type in "
              "the box), <b>Duration</b> (the total, without disabled songs, is shown at the bottom) and "
              "<b>New ID</b> (number Apply IDs will give, orange when it changes)."),
        ("h2", "Colours"),
        ("table2", [
            ("Yellow, larger name", "The song being played."),
            ("Green, italic", "Song covered by the time selection (ready to play)."),
            ("Red, struck through, « OFF »", "Disabled song."),
            ("Blue, « (n nested) »", "Parent region containing n nested regions."),
        ]),
        ("h2", "Mouse gestures"),
        ("table_g", [
            ("Click", "Selects the song and puts the time selection on it (smooth seek while playing)."),
            ("Double-click", "Plays the song."),
            ("Shift+click", "Renames the song."),
            ("Ctrl+click", "Horizontal zoom on the song."),
            ("Alt+click", "Disables the song; another Alt+click enables it again."),
            ("Drag and drop", "Changes the setlist order (child regions follow their parent)."),
        ]),
        ("h1", "6. Building the setlist"),
        ("p", "The order of the list becomes the order of the IDs when you click <b>Apply IDs</b>. Example: drag "
              "« Nuit blanche » to the top, the New ID column turns orange, then Apply IDs rewrites the region numbers "
              "in REAPER. <b>Reset order</b> cancels the moves not yet applied."),
        ("p", "<b>Child regions:</b> their ID is the parent's ID times 100, plus their rank. If song 2 contains Verse, "
              "Chorus and Solo, they get 201, 202 and 203; if the song moves to position 1, they become 101, 102 and "
              "103."),
        ("p", "<b>Limit:</b> computed IDs must stay below 10000. Beyond that, a red warning appears and Apply IDs "
              "refuses to run."),
        ("h1", "7. Disabling, renaming, comments"),
        ("p", "<b>Alt+click</b> removes a song from tonight's set without deleting it: it turns red and struck "
              "through, gets an ID from 10000 (shown « OFF »), leaves the numbering and the durations, and can no "
              "longer be selected or played (it can still be dragged). Remember to Apply IDs to renumber the others. "
              "<b>Shift+click</b> opens « Rename region » (OK / Cancel, Enter / Esc). The <b>Comment</b> column keeps a "
              "note per song (« capo 3 », « drums alone intro »), saved in the project."),
        ("h2", "Region sets"),
        ("p", "A <b>set</b> remembers the whole configuration (order, names, enabled or disabled regions, comments) "
              "under a name: « Full show », « Festival 40 min »... Type a name then <b>Save set</b>; choose a set in "
              "the list, then <b>Load</b> or <b>Delete set</b>. The « Apply IDs immediately when loading a set » box "
              "renumbers on load. Regions are stored completely: a song deleted in the meantime is recreated on load. "
              "Sets live in the project file: save it."),
        ("h1", "8. Transport on stage"),
        ("table_b", [
            ("Play/Stop", "Stopped: starts. Playing with repeat on: turns repeat off and puts the time selection on "
                          "the current parent song (it plays to its end). Playing with repeat off: stops."),
            ("Stop", "Playing: stop (action 40328). Stopped: back to the start of the time selection."),
            ("Previous / Next", "Previous / next song, with Smooth seek if enabled."),
        ]),
        ("p", "<b>Typical scenario:</b> enable Auto stop and Smooth seek (and Count-in if the drummer starts on the "
              "click); click the song, Play/Stop; at the end Auto stop stops; Next then Play/Stop for the following "
              "song. If the singer wants to extend a chorus, leave repeat on, then Play/Stop when ready."),
        ("h1", "9. Live loop"),
        ("p", "<b>Live loop</b> loops the current part. Repeat off: the click turns repeat on and puts the time "
              "selection on the <b>child region</b> at the current position (the parent region if there is none). "
              "Repeat on: the click turns repeat off and puts the selection back on the parent region. The position "
              "is the play position, or the edit cursor when stopped. Outside a song, nothing happens."),
        ("h1", "10. Stand-alone actions and shortcuts"),
        ("p", "Five scripts that do not need the window, to bind to a keyboard or MIDI shortcut (footswitch) in the "
              "action list; they skip disabled songs. Pick any shortcuts you like: the ones in this manual are examples."),
        ("table2", [
            ("REABACK_PlayStop", "Same as Play/Stop (lit while playing)."),
            ("REABACK_Stop", "Same as Stop."),
            ("REABACK_Previous / REABACK_Next", "Previous / next song."),
            ("REABACK_LiveLoop", "Same as Live loop (lit when repeat is on)."),
        ]),
        ("p", "Example: a 4-pedal controller on channel 1: pedal 1 Previous, 2 Play/Stop, 3 Next, 4 Stop."),
        ("h1", "11. Smartphone remote control"),
        ("p", "The <b>REABACK.html</b> page shows the setlist on a phone connected to the same network as the stage "
              "computer, through REAPER's web interface."),
        ("ol", ["Preferences &gt; Control/OSC/web &gt; Add &gt; Web browser interface; note the port.",
                "Keep the REABACK window open in REAPER (it publishes the list).",
                "On the phone, open <font size=8>http://&lt;computer IP address&gt;:&lt;port&gt;/REABACK.html</font>."]),
        ("p", "Normal mode: state (« Playing / loop »), Previous, Play/Stop, Stop, Next, Metronome, Count-in, Auto "
              "stop, Smooth seek, Follow and Live loop; tap = select, double-tap = play. The <b>Edit</b> button adds: "
              "▲/▼ arrows to move, Rename, Disable/Enable, Comment, Apply IDs, Reset order, Export .txt and the sets. "
              "Keep it closed during the show. If the REABACK script is not running, the page says so; basic "
              "transport still works."),
        ("h1", "12. The prompter (tablet)"),
        ("p", "The prompter shows the <b>item notes</b> of three tracks in real time: the one whose name contains "
              "<b>Lyrics</b> (in <b>yellow</b>), <b>Chords</b> (in <b>red</b>) and <b>Comment</b> (in <b>white "
              "italic</b>), for the length of each item. At the top it also shows the name of the current <b>parent "
              "region</b> and, below, the <b>child region</b>."),
        ("draw", "prompter"),
        ("ol", ["Copy <b>Reaback-prompter.html</b> to reaper_www_root (ReaPack does it) and enable the web interface.",
                "Run the <b>Reaback-prompter</b> action (background, no window; run it again to stop it).",
                "On the tablet: <font size=8>http://&lt;IP address&gt;:&lt;port&gt;/Reaback-prompter.html</font>."]),
        ("p", "At the bottom: <b>Lyrics</b>, <b>Chords</b>, <b>Comment</b> buttons to choose what stays on screen, "
              "<b>Next</b> (pale preview of the next item), <b>A-</b> / <b>A+</b> (text size) and full screen; a tap on "
              "the text hides or shows the bar. Two indicators at the top right: <b>PLAY</b> (green), <b>PAUSE</b> "
              "(orange), <b>REC</b> (red) or <b>STOP</b>, and <b>LOOP</b> (blue) when repeat is on. When stopped, the "
              "prompter follows the edit cursor."),
        ("h1", "13. Reaback Set up"),
        ("p", "Shortcut window to prepare the session. Each button looks for its action by name, then by ID; hovering "
              "a button shows the action used, and the bottom line tells what was run."),
        ("h2", "Configuration"),
        ("p", "Audio device settings, MIDI devices (inputs, outputs: the same REAPER page), Web control surface, "
              "Project settings, Metronome settings, Routing matrix, Video window, External synchronization settings."),
        ("h2", "Session Built"),
        ("table2", [
            ("Project templates / Open project / Save project as...", "The matching REAPER windows."),
            ("Media explorer", "Opens or closes the Media explorer."),
            ("Normalize", "Normalizes the selected items."),
            ("Insert tempo change marker", "Tempo marker at the edit cursor."),
            ("Time selection to selected items", "Time selection on the selected items."),
            ("Region from time selection", "Creates a region over the time selection."),
            ("Lyrics / Chords / Comment item + notes", "Creates an empty item over the time selection, on the track "
                          "whose name contains Lyrics / Chords / Comment, opens its notes, then shifts the time "
                          "selection right by its length: you chain the lines."),
            ("MIDI item + MIDI editor", "Empty MIDI item over the selection, on the selected track, opened in the "
                          "MIDI editor (docked, synced to the arrange view if the action exists)."),
            ("Timecode track", "Track whose name contains Timecode: cleared, no master send, timecode generator over "
                          "the whole project, source properties opened."),
            ("Lock / Unlock items of the region", "Locks or unlocks the items of the widest region under the edit "
                          "cursor."),
            ("Windows set manager", "REAPER's window sets (screensets) window."),
        ]),
        ("h1", "14. Icons and FAQ"),
        ("p", "Eight icons (three states: normal, hover, active) are installed in Data/toolbar_icons: right-click a "
              "toolbar &gt; Customize toolbar &gt; Choose icon, then the icon with the same name. Restart REAPER if "
              "they do not show up. Icons light up with the state: REABACK, Set up and prompter windows while they run, "
              "Play/Stop while playing, Live loop when repeat is on."),
        ("qa", [
            ("The window does not open.", "ReaImGui is not installed: install it via ReaPack and restart REAPER."),
            ("The Count-in button does nothing.", "SWS is not installed or the action does not exist in your version."),
            ("Apply IDs refuses.", "A computed ID exceeds 9999 (red warning): reduce songs or nesting."),
            ("A part is treated as a song.", "It goes beyond its parent or shares its edges: put it strictly inside."),
            ("Next no longer finds a song.", "It is disabled (red, struck through): Alt+click to enable it again."),
            ("The phone page / the prompter show nothing.", "The REABACK / Reaback-prompter script is not running in REAPER."),
            ("Line breaks of the notes look wrong.", "Update to version 1.3 (the prompter decodes the text correctly there)."),
        ]),
    ],
}

# ------------------------------------------------------------------ drawings (simplified, not screenshots)
BG = colors.HexColor("#1F2124")
BTN = colors.HexColor("#3A3D42")
ON = colors.HexColor("#3F7FC9")
TXT = colors.HexColor("#E8E8E8")
MUT = colors.HexColor("#9A9A9A")
YEL = colors.HexColor("#FFE600")
RED = colors.HexColor("#FF3B30")
LBLUE = colors.HexColor("#8EC5FF")
GREEN = colors.HexColor("#7CF0A6")


def d_nested():
    W, H = 174 * mm, 36 * mm
    d = Drawing(W, H)
    songs = [("1  Nuit blanche", 0.0, 0.40, True), ("2  Sous le soleil", 0.43, 0.99, True)]
    d.add(Rect(0, 0, W, H, rx=5, ry=5, fillColor=colors.HexColor("#F4F6F8"), strokeColor=colors.HexColor("#C9CED4")))
    for lab, a, b, kids in songs:
        x0, x1 = 6 * mm + a * 160 * mm, 6 * mm + b * 160 * mm
        d.add(Rect(x0, 15 * mm, x1 - x0 - 2, 12 * mm, fillColor=colors.HexColor("#DCE8F6"), strokeColor=ACCENT))
        d.add(String(x0 + 3, 21 * mm, lab, fontName="DVB", fontSize=8, fillColor=DARK))
    sub = [("101", 0.02, 0.16), ("102", 0.17, 0.30), ("201", 0.46, 0.62), ("202", 0.63, 0.78), ("203", 0.79, 0.97)]
    for lab, a, b in sub:
        x0, x1 = 6 * mm + a * 160 * mm, 6 * mm + b * 160 * mm
        d.add(Rect(x0, 5 * mm, x1 - x0, 8 * mm, fillColor=colors.HexColor("#FFF1C2"), strokeColor=colors.HexColor("#C9A227")))
        d.add(String((x0 + x1) / 2, 7.3 * mm, lab, fontName="DV", fontSize=8, fillColor=DARK, textAnchor="middle"))
    d.add(String(6 * mm, H - 4 * mm, "Song", fontName="DVI", fontSize=7, fillColor=GREY))
    return d


def buttons(d, x, y, labels, on=(), h=5 * mm, fs=6.5):
    for lab in labels:
        w = max(8 * mm, len(lab) * fs * 0.62 + 4 * mm)
        d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=ON if lab in on else BTN, strokeColor=None))
        d.add(String(x + w / 2, y + h / 2 - fs * 0.35, lab, fontName="DV", fontSize=fs, fillColor=TXT,
                     textAnchor="middle"))
        x += w + 1.2 * mm
    return x


def d_window():
    W, H = 174 * mm, 56 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=BG, strokeColor=None))
    buttons(d, 6 * mm, H - 11 * mm, ["Previous", "Play/Stop", "Stop", "Next"], h=7 * mm, fs=8)
    buttons(d, 6 * mm, H - 18 * mm, ["Metronome", "Count-in", "Auto stop", "Smooth seek", "Live loop", "Zoom all"],
            on=("Auto stop", "Live loop"))
    cols = [("ID", 6), ("Name", 22), ("Comment", 70), ("Duration", 128), ("New ID", 152)]
    y = H - 27 * mm
    for lab, x in cols:
        d.add(String(x * mm, y, lab, fontName="DVB", fontSize=7, fillColor=MUT))
    d.add(Line(6 * mm, y - 2, W - 6 * mm, y - 2, strokeColor=colors.HexColor("#45474C"), strokeWidth=0.6))
    rows = [("1", "Nuit blanche", "start on click", "03:42", "1", TXT, "DV"),
            ("2", "Sous le soleil  (3 nested)", "capo 3", "04:05", "2", LBLUE, "DV"),
            ("3", "Dernière danse", "", "03:18", "3", YEL, "DVB"),
            ("OFF", "Interlude", "", "—", "", RED, "DVI"),
            ("4", "Rappel", "", "03:55", "4", GREEN, "DVI")]
    for k, (i, n, c, du, nw, col, f) in enumerate(rows):
        yy = y - 11 - k * 9
        d.add(String(6 * mm, yy, i, fontName="DV", fontSize=7.5, fillColor=MUT))
        d.add(String(22 * mm, yy, n, fontName=f, fontSize=8 if col != YEL else 9, fillColor=col))
        d.add(String(70 * mm, yy, c, fontName="DV", fontSize=7.5, fillColor=MUT))
        d.add(String(128 * mm, yy, du, fontName="DV", fontSize=7.5, fillColor=TXT))
        d.add(String(152 * mm, yy, nw, fontName="DV", fontSize=7.5, fillColor=colors.HexColor("#FF9F0A") if nw == "3" else TXT))
        if col == RED:
            d.add(Line(22 * mm, yy + 2.5, 40 * mm, yy + 2.5, strokeColor=RED, strokeWidth=0.8))
    buttons(d, 6 * mm, 3 * mm, ["Apply IDs", "Reset order", "Export .txt", "Save set", "Load", "Delete set"], h=5 * mm)
    return d


def d_prompter():
    W, H = 120 * mm, 62 * mm
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=colors.black, strokeColor=colors.HexColor("#45474C")))
    d.add(String(W / 2, H - 9 * mm, "Sous le soleil", fontName="DVB", fontSize=8, fillColor=colors.white, textAnchor="middle"))
    d.add(String(W / 2, H - 14 * mm, "Refrain", fontName="DV", fontSize=6.5, fillColor=LBLUE, textAnchor="middle"))
    d.add(String(W / 2, H - 22 * mm, "Am        F        C        G", fontName="DVB", fontSize=9, fillColor=RED, textAnchor="middle"))
    d.add(String(W / 2, H - 32 * mm, "Dansons sous le soleil", fontName="DVB", fontSize=13, fillColor=YEL, textAnchor="middle"))
    d.add(String(W / 2, H - 40 * mm, "jusqu'au bout de la nuit", fontName="DVB", fontSize=13, fillColor=YEL, textAnchor="middle"))
    d.add(String(W / 2, H - 49 * mm, "stop net sur le dernier accord", fontName="DVI", fontSize=7.5, fillColor=colors.white, textAnchor="middle"))
    d.add(Rect(W - 30 * mm, H - 6 * mm, 11 * mm, 4 * mm, rx=2, ry=2, fillColor=colors.HexColor("#34C759"), strokeColor=None))
    d.add(String(W - 24.5 * mm, H - 5 * mm, "PLAY", fontName="DVB", fontSize=5.5, fillColor=colors.black, textAnchor="middle"))
    d.add(Rect(W - 17 * mm, H - 6 * mm, 11 * mm, 4 * mm, rx=2, ry=2, fillColor=colors.HexColor("#5AC8FA"), strokeColor=None))
    d.add(String(W - 11.5 * mm, H - 5 * mm, "LOOP", fontName="DVB", fontSize=5.5, fillColor=colors.black, textAnchor="middle"))
    buttons(d, 6 * mm, 2 * mm, ["Lyrics", "Chords", "Comment", "Next", "A-", "A+"], on=("Lyrics", "Chords", "Comment"), h=4.5 * mm, fs=6)
    return d


DRAW = {"nested": d_nested, "window": d_window, "prompter": d_prompter}


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
        return [table(val, t["head2"], 58), Spacer(1, 4)]
    if kind == "table_g":
        return [table(val, t["head_g"]), Spacer(1, 4)]
    if kind == "table_b":
        return [table(val, t["head_b"], 52), Spacer(1, 4)]
    if kind == "qa":
        return [KeepTogether([Paragraph("<b>%s</b>" % q, S["p"]), Paragraph(a, S["p"])]) for q, a in val]
    if kind == "draw":
        return [KeepTogether([DRAW[val](), Paragraph(t["cap"], S["cap"])])]
    return []


def build(lang, out):
    t = T[lang]
    doc = Doc(os.path.join(out, t["file"]), lang)
    story = [Spacer(1, 40 * mm), Paragraph(NAME, S["title"]), Spacer(1, 6 * mm), Paragraph(t["sub"], S["sub"]),
             Spacer(1, 4 * mm), Paragraph("%s — version %s" % (t["manual"], VERSION), S["sub"]),
             Spacer(1, 8 * mm), Image(os.path.join(HERE, "REABACK_icon.png"), width=22 * mm, height=22 * mm),
             Spacer(1, 8 * mm), Paragraph(t["other"], S["center"]), Spacer(1, 3 * mm),
             Paragraph('<link href="%s" color="blue">%s</link>' % (URL_REPO, URL_REPO), S["center"]),
             Spacer(1, 14 * mm), Paragraph(t["toc"], S["h2"])]
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"]]
    story += [toc, PageBreak()]
    body = t["body"]
    i = 0
    while i < len(body):
        item = body[i]
        if item[0] in ("h1", "h2"):
            head = Paragraph(item[1], S[item[0]])
            if i + 1 < len(body) and body[i + 1][0] in ("draw", "p", "table_b", "table2", "table_g"):
                story.append(KeepTogether([head] + render(body[i + 1], lang)))
                i += 2
                continue
            story.append(head)
        else:
            story += render(item, lang)
        i += 1
    doc.multiBuild(story)
    return os.path.join(out, t["file"])


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for lg in ("fr", "en"):
        print(build(lg, out))
