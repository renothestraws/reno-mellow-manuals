# -*- coding: utf-8 -*-
"""Manuel ReNo Mellow - Strip Buddy (FR + EN).
Usage : python3 make_manual.py   -> StripBuddy_manuel_FR.pdf + StripBuddy_manual_EN.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, Image, Flowable)

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.19"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DV", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DVB", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DVI", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DVM", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

ACCENT = colors.HexColor("#C0392B")
DARK = colors.HexColor("#222222")
GREY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F2F2F2")

BASE = "https://github.com/renothestraws/reno-mellow-manuals/raw/main/scripts/StripBuddy/"
URL_FR = BASE + "StripBuddy_manuel_FR.pdf"
URL_EN = BASE + "StripBuddy_manual_EN.pdf"
URL_INDEX = "https://raw.githubusercontent.com/renothestraws/reno-mellow-script/main/index.xml"
URL_PKG = "https://github.com/renothestraws/reno-mellow-script/raw/main/packages/ReNo_Mellow_Strip_Buddy.ReaperPkg"
URL_REPO = "https://github.com/renothestraws/reno-mellow-script"

ST = {
    "title": ParagraphStyle("title", fontName="DVB", fontSize=26, leading=32, textColor=DARK, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=14, leading=19, textColor=GREY, alignment=TA_CENTER),
    "center": ParagraphStyle("center", fontName="DV", fontSize=10, leading=14, alignment=TA_CENTER, textColor=DARK),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, textColor=ACCENT, spaceBefore=10, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=12, leading=15, textColor=DARK, spaceBefore=8, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.5, leading=13.5, textColor=DARK, spaceAfter=5),
    "li": ParagraphStyle("li", fontName="DV", fontSize=9.5, leading=13.5, textColor=DARK, leftIndent=12,
                         bulletIndent=2, spaceAfter=2),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.6, leading=11.5, textColor=DARK),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.6, leading=11.5, textColor=DARK),
    "head": ParagraphStyle("head", fontName="DVB", fontSize=8.8, leading=11.5, textColor=colors.white),
    "note": ParagraphStyle("note", fontName="DVI", fontSize=8.5, leading=11.5, textColor=GREY, spaceAfter=6),
    "toc": ParagraphStyle("toc", fontName="DV", fontSize=11, leading=17, textColor=DARK, leftIndent=40),
}

# ----------------------------------------------------------------------------------------------
# Texts
# ----------------------------------------------------------------------------------------------
T = {}
T["fr"] = dict(
    file="StripBuddy_manuel_FR.pdf",
    subtitle="Presets de pistes en un clic pour REAPER",
    manual="Manuel d'utilisation",
    other='English version : <link href="%s" color="#C0392B">StripBuddy_manual_EN.pdf</link>' % URL_EN,
    footer="ReNo Mellow – Strip Buddy %s – manuel d'utilisation" % VERSION,
    page="page",
    toc_title="Sommaire",
    toc=["1. Principe", "2. Installation", "3. Premiers pas", "4. L'onglet Strips", "5. L'onglet Setup",
         "6. Fonctions avancées", "7. Le Display des tags", "8. Fichiers, actions et raccourcis", "9. Questions fréquentes"],
    s1="1. Principe",
    s1p=[
        "Strip Buddy (anciennement Custom Strips) enregistre des <b>presets de pistes</b>, appelés <i>strips</i>. Un strip réunit tout ce qu'on règle "
        "d'habitude à la main en préparant une session : nom, tag, couleur, icône, layouts, entrée d'enregistrement, mode de "
        "panoramique, type de mètre, chaîne d'effets, enveloppes visibles, noms des items, normalisation et groupe.",
        "Un clic sur un strip l'applique à <b>toutes les pistes sélectionnées</b>, en une seule étape d'annulation. "
        "Dans un strip, seul le nom est obligatoire : une case vide ne modifie rien sur la piste.",
        "La fenêtre a deux onglets : <b>Strips</b>, la palette de boutons de tous les jours, rangée en dossiers ; "
        "<b>Setup</b>, le tableau où l'on règle chaque strip. Le script est livré avec 165 strips de base en 15 dossiers.",
    ],
    s2="2. Installation",
    s2a="Avec ReaPack (recommandé, mises à jour automatiques)",
    s2a_steps=[
        "Extensions > ReaPack > <b>Import repositories…</b>, coller l'adresse ci-dessous, OK.",
        "Extensions > ReaPack > <b>Browse packages</b>, chercher « Strip Buddy », clic droit > Install, puis Apply.",
        "Installer aussi <b>ReaImGui</b> (même fenêtre) s'il manque, puis redémarrer REAPER.",
        "Mises à jour : Extensions > ReaPack > <b>Synchronize packages</b>.",
    ],
    s2b="Avec le paquet .ReaperPkg (REAPER 7.86 ou plus récent)",
    s2b_steps=[
        "Télécharger le fichier <b>ReNo_Mellow_Strip_Buddy.ReaperPkg</b> (lien ci-dessous).",
        "Le glisser dans la fenêtre de REAPER : le script, son icône et les icônes de pistes sont installés.",
        "Pas de mise à jour automatique : reprendre le nouveau paquet à chaque version.",
    ],
    s2c="Prérequis et barre d'outils",
    s2c_p=[
        "<b>ReaImGui</b> est obligatoire. Sans lui, le script prévient et ouvre la bonne page de ReaPack. "
        "<b>js_ReaScriptAPI</b> est facultatif : avec lui, les fenêtres de choix de fichiers filtrent les bons types de fichiers.",
        "Pour un bouton : clic droit sur une barre d'outils > Customize toolbar > Add, action « ReNo Mellow - Strip Buddy », "
        "icône <b>ReNo_StripBuddy</b>. Le bouton reste allumé tant que la fenêtre est ouverte.",
    ],
    links_head=["Lien", "Adresse"],
    links=[("Index ReaPack", URL_INDEX), ("Paquet .ReaperPkg", URL_PKG), ("Dépôt GitHub", URL_REPO)],
    s3="3. Premiers pas",
    s3_steps=[
        "Lancer l'action <b>ReNo Mellow - Strip Buddy</b> (liste d'actions ou bouton de barre d'outils).",
        "Au premier lancement, les 165 strips de base sont créés dans 15 dossiers (Drums, Bass, Vocals…).",
        "Sélectionner une ou plusieurs pistes dans REAPER.",
        "Dans l'onglet Strips, cliquer sur un strip, par exemple « Kick in » : la piste est renommée, taguée et reçoit son icône.",
        "Une erreur ? Ctrl+Z annule tout le strip d'un coup.",
    ],
    schema_note="Schéma simplifié de la fenêtre, pas une capture d'écran.",
    s4="4. L'onglet Strips",
    s4p="La colonne de gauche liste les dossiers, avec le nombre de strips de chacun. "
        "« All strips » montre tout, « No folder » montre les strips pas encore rangés. "
        "À droite, un bouton par strip, à la couleur du strip ; le survoler affiche tout ce qu'il règle.",
    s4_head=["Geste", "Effet"],
    s4_rows=[
        ("Clic sur un strip", "Applique le strip aux pistes sélectionnées (une étape d'annulation)."),
        ("Glisser un strip sur un autre", "Change l'ordre des strips."),
        ("Glisser un strip sur un dossier", "Range le strip dans ce dossier (« No folder » = le sortir)."),
        ("Clic droit sur un strip", "Apply, Rename, Edit in Setup, Duplicate, Delete."),
        ("Clic sur un dossier", "Affiche ses strips. Le dernier dossier ouvert est retenu."),
        ("+ New folder", "Crée un dossier (un seul niveau). Un strip créé ensuite y va directement."),
        ("Clic droit sur un dossier", "Rename ou Delete. Ses strips sont gardés et repassent dans « No folder »."),
        ("Glisser un dossier sur un autre", "Change l'ordre des dossiers."),
    ],
    s5="5. L'onglet Setup",
    s5p="Une ligne par strip, une colonne par réglage. <b>Une case vide est ignorée</b> quand le strip est appliqué. "
        "En haut : + Add strip, Load default strips, Export…, Import…, Clear all strips. "
        "À droite de chaque ligne : flèches pour déplacer, Dup pour dupliquer, Del pour supprimer.",
    s5_head=["Colonne", "Ce que le strip fait à la piste"],
    s5_rows=[
        ("#", "Numéro du strip ; clic pour le sélectionner (voir multisélection)."),
        ("Strip name", "Nom du bouton. Seule case obligatoire."),
        ("Track name", "Renomme la piste. Plusieurs pistes sélectionnées : Tom 1, Tom 2, Tom 3…"),
        ("Tag", "Ajoute un tag de 1 à 3 caractères en fin de nom : « Kick in [KIK] ». Un tag existant est remplacé."),
        ("Colour", "Couleur de la piste. Set pour en choisir une, x pour l'enlever."),
        ("Icon", "Icône de piste. Browse ouvre Data/track_icons (62 icônes cs_tags_XXX fournies)."),
        ("Layout", "Layouts TCP et MCP du thème actif, ou layout par défaut du thème."),
        ("Record input", "Entrée mono, stéréo ou MIDI ; ou Record output stereo / mono / MIDI."),
        ("Pan mode", "Project default, Stereo balance / mono pan, Stereo pan, Dual pan, Balance (classic 3.x)."),
        ("Metering", "Stereo peaks, Multichannel peaks, Stereo RMS, Combined RMS, LUFS-M, LUFS-S, Meter disabled."),
        ("FX chain", "Fichier .RfxChain ajouté après les effets déjà présents. Browse ouvre FXChains."),
        ("Envelopes", "Enveloppes rendues visibles : Volume, Pan, Width, Mute, Trim volume."),
        ("Item name", "Renomme tous les items de la piste, numérotés par position s'il y en a plusieurs."),
        ("Normalize", "LUFS-I, RMS, Peak ou True peak, cible en dB, chaque item ou tous ensemble. "
                      "Désactivée par défaut (case non cochée) ; en la cochant, -15 dBFS Peak, ensemble est proposé."),
        ("Group", "Groupe de piste (1 à 64 ou 128), nom du groupe et flags lead / follow."),
    ],
    s5_rec="Choisir une entrée remet la piste en enregistrement de l'entrée si elle enregistrait sa sortie ; "
           "les modes MIDI (overdub…) ne sont pas touchés.",
    s5_norm="« Tous ensemble » applique un gain commun et garde l'équilibre entre les items : en Peak, l'item le plus fort "
            "atteint la cible ; en LUFS ou RMS, la mesure combine tous les items, pondérés par leur durée (approximation).",
    s6="6. Fonctions avancées",
    s6_items=[
        ("Multisélection", "Clic sur le numéro (#) d'une ligne : sélection. Ctrl+clic : ajouter ou retirer. "
                           "Shift+clic : toute une plage. Une modification faite dans une ligne sélectionnée est copiée dans "
                           "toutes les lignes sélectionnées, sauf le nom du strip. Seul le réglage modifié est copié."),
        ("Héritage par tag", "Le premier strip d'un tag dans un dossier (ex. Cymbals pour [CYM]) transmet sa couleur et son "
                             "icône aux autres strips du même tag de ce dossier qui n'en ont pas, ou qui avaient hérité la même valeur."),
        ("Load default strips", "Ajoute les strips de base qui manquent (nom de piste, tag, icône ; sans normalisation). "
                                "Ne modifie jamais les strips existants ; peut être relancé sans créer de doublons."),
        ("Export… / Import…", "Export : tous les strips, un dossier ou les strips sans dossier, dans un fichier .rnstrips "
                              "(par défaut Data/ReNo_StripBuddy/Exports). Import : en ajout (dossiers de même nom fusionnés, "
                              "doublons ignorés) ou en remplacement complet."),
        ("Clear all strips", "Efface tous les strips, et les dossiers si la case est cochée. Pas d'annulation : "
                             "faire un Export avant."),
    ],
    sd="7. Le Display des tags",
    sdp=["Le Display est une petite barre flottante, sans titre, à placer où l'on veut. Le bouton <b>Strip Buddy</b>, à l'image de "
         "l'icône de barre d'outils, ouvre ou ferme la fenêtre principale ; il est allumé quand elle est ouverte. Ensuite, quatre options "
         "à allumer (une ou plusieurs) : <b>Zoom</b>, <b>View</b>, <b>Scroll</b>, <b>Select</b>. À droite, la liste "
         "déroulante des tags du projet (les [ABC] en fin de nom de piste), précédée de <b>All</b>. Choisir un tag "
         "applique d'un coup toutes les options allumées, dans l'ordre View, Select, Zoom, Scroll (une étape d'annulation).",
         "Ouvrir : action « ReNo Mellow - Strip Buddy - Display », ou bouton « Open / close the Display » de l'onglet "
         "Display. Relancer l'action ferme le Display."],
    sd_head=["Option", "Avec un tag", "Avec All"],
    sd_rows=[
        ("View", "N'affiche que les pistes du tag ; leurs dossiers parents restent visibles.", "Réaffiche toutes les pistes."),
        ("Zoom", "Agrandit les pistes du tag pour remplir la hauteur de l'arrangement.", "Remet les hauteurs par défaut."),
        ("Scroll", "Amène la première piste du tag en haut (TCP) ou à gauche (mixer).", "Revient à la première piste."),
        ("Select", "Sélectionne les pistes du tag (prêtes pour un strip).", "Sélectionne toutes les pistes."),
    ],
    sd_more=["<b>Molette</b> au-dessus de la liste : tag suivant / précédent, appliqué aussitôt. Chaque tag est affiché "
             "avec la couleur de sa première piste. <b>Clic droit</b> sur la barre : taille du texte, réouverture au démarrage, Open / Close Strip Buddy, Close.",
             "Onglet <b>Display</b> de la fenêtre principale : <b>Display View</b> (TCP, MCP ou Both : où View cache les pistes), "
             "<b>Display Scroll</b> (TCP, MCP ou Both : où Scroll fait défiler), et « Reopen the Display when REAPER starts ».",
             "Zoom et Scroll précis utilisent js_ReaScriptAPI ; sans elle, le Zoom passe par SWS s'il est installé et le Scroll "
             "par l'action native « Vertical scroll selected tracks into view »."],
    callout_disp="Exemple : View et Scroll allumés, tag KIK choisi dans la liste.",
    s7="8. Fichiers, actions et raccourcis",
    s7_rows=[
        ("Actions", "« ReNo Mellow - Strip Buddy » (ouvre / ferme la fenêtre) et « ReNo Mellow - Strip Buddy - Display » (ouvre / ferme le Display)."),
        ("Raccourci", "Aucun imposé : chacun choisit le sien dans la liste d'actions (ex. Ctrl+Shift+C, simple exemple)."),
        ("Données", "Data/ReNo_StripBuddy/strips.lua, enregistré automatiquement à chaque modification."),
        ("Exports", "Data/ReNo_StripBuddy/Exports/*.rnstrips"),
        ("Icônes", "Data/track_icons/cs_tags_XXX.png (pistes), Data/toolbar_icons/ReNo_StripBuddy.png (barre d'outils)."),
    ],
    s7_head=["Élément", "Détail"],
    s8="9. Questions fréquentes",
    faq=[
        ("J'utilisais Custom Strips.", "Dans ReaPack, désinstaller d'abord Custom Strips, puis installer Strip Buddy. "
                                       "Au premier lancement, vos strips, dossiers, exports et réglages sont repris automatiquement. "
                                       "Remplacer l'ancien bouton de barre d'outils par l'action « ReNo Mellow - Strip Buddy »."),
        ("Le script dit qu'il manque ReaImGui.", "Installer ReaImGui avec ReaPack (Browse packages), puis redémarrer REAPER."),
        ("Rien ne se passe au clic.", "Aucune piste n'est sélectionnée : le message « Select one or more tracks first. » "
                                      "s'affiche en bas de la fenêtre."),
        ("ReaPack ne voit pas la nouvelle version.", "Le serveur de GitHub peut garder l'ancien index environ 5 minutes : "
                                                     "attendre puis refaire Synchronize packages."),
        ("Mes strips n'ont pas les nouveautés des strips de base.", "Load default strips n'ajoute que les strips manquants. "
                                                                   "Utiliser la multisélection pour régler plusieurs strips d'un coup."),
        ("Un nom de strip est coupé sur son bouton.", "Les boutons ont une largeur fixe : choisir un nom plus court, "
                                                      "le nom de piste peut rester long."),
    ],
    sch_strips="Onglet Strips", sch_setup="Onglet Setup",
)

T["en"] = dict(
    file="StripBuddy_manual_EN.pdf",
    subtitle="One-click track presets for REAPER",
    manual="User manual",
    other='Version française : <link href="%s" color="#C0392B">StripBuddy_manuel_FR.pdf</link>' % URL_FR,
    footer="ReNo Mellow – Strip Buddy %s – user manual" % VERSION,
    page="page",
    toc_title="Contents",
    toc=["1. Overview", "2. Installation", "3. Getting started", "4. The Strips tab", "5. The Setup tab",
         "6. Advanced features", "7. The tag Display", "8. Files, actions and shortcuts", "9. FAQ"],
    s1="1. Overview",
    s1p=[
        "Strip Buddy (formerly Custom Strips) stores <b>track presets</b>, called <i>strips</i>. A strip gathers everything you usually set by hand "
        "when preparing a session: name, tag, colour, icon, layouts, record input, pan mode, meter type, FX chain, visible "
        "envelopes, item names, normalization and group.",
        "One click on a strip applies it to <b>all selected tracks</b>, as a single undo step. "
        "Only the strip name is required: an empty cell leaves the track unchanged.",
        "The window has two tabs: <b>Strips</b>, your everyday palette of buttons, sorted in folders; "
        "<b>Setup</b>, the table where each strip is set. The script ships with 165 default strips in 15 folders.",
    ],
    s2="2. Installation",
    s2a="With ReaPack (recommended, automatic updates)",
    s2a_steps=[
        "Extensions > ReaPack > <b>Import repositories…</b>, paste the address below, OK.",
        "Extensions > ReaPack > <b>Browse packages</b>, search for “Strip Buddy”, right-click > Install, then Apply.",
        "Also install <b>ReaImGui</b> (same window) if it is missing, then restart REAPER.",
        "Updates: Extensions > ReaPack > <b>Synchronize packages</b>.",
    ],
    s2b="With the .ReaperPkg package (REAPER 7.86 or newer)",
    s2b_steps=[
        "Download <b>ReNo_Mellow_Strip_Buddy.ReaperPkg</b> (link below).",
        "Drag it into the REAPER window: the script, its toolbar icon and the track icons are installed.",
        "No automatic updates: download the new package for each version.",
    ],
    s2c="Requirements and toolbar",
    s2c_p=[
        "<b>ReaImGui</b> is required. Without it, the script warns you and opens the right ReaPack page. "
        "<b>js_ReaScriptAPI</b> is optional: with it, file dialogs only show the right file types.",
        "For a button: right-click a toolbar > Customize toolbar > Add, action “ReNo Mellow - Strip Buddy”, "
        "icon <b>ReNo_StripBuddy</b>. The button stays lit while the window is open.",
    ],
    links_head=["Link", "Address"],
    links=[("ReaPack index", URL_INDEX), (".ReaperPkg package", URL_PKG), ("GitHub repository", URL_REPO)],
    s3="3. Getting started",
    s3_steps=[
        "Run the action <b>ReNo Mellow - Strip Buddy</b> (action list or toolbar button).",
        "On first run, the 165 default strips are created in 15 folders (Drums, Bass, Vocals…).",
        "Select one or more tracks in REAPER.",
        "In the Strips tab, click a strip, for example “Kick in”: the track is renamed, tagged and gets its icon.",
        "A mistake? Ctrl+Z undoes the whole strip at once.",
    ],
    schema_note="Simplified drawing of the window, not a screenshot.",
    s4="4. The Strips tab",
    s4p="The left column lists the folders, with the number of strips in each. "
        "“All strips” shows everything, “No folder” shows the strips not filed yet. "
        "On the right, one button per strip, in the strip's colour; hover it to see everything it sets.",
    s4_head=["Action", "Result"],
    s4_rows=[
        ("Click a strip", "Applies the strip to the selected tracks (one undo step)."),
        ("Drag a strip onto another", "Changes the order of the strips."),
        ("Drag a strip onto a folder", "Files the strip in that folder (“No folder” = take it out)."),
        ("Right-click a strip", "Apply, Rename, Edit in Setup, Duplicate, Delete."),
        ("Click a folder", "Shows its strips. The last folder opened is remembered."),
        ("+ New folder", "Creates a folder (one level). A strip created next goes straight into it."),
        ("Right-click a folder", "Rename or Delete. Its strips are kept and go back to “No folder”."),
        ("Drag a folder onto another", "Changes the order of the folders."),
    ],
    s5="5. The Setup tab",
    s5p="One row per strip, one column per setting. <b>An empty cell is ignored</b> when the strip is applied. "
        "At the top: + Add strip, Load default strips, Export…, Import…, Clear all strips. "
        "At the right of each row: arrows to move it, Dup to duplicate, Del to delete.",
    s5_head=["Column", "What the strip does to the track"],
    s5_rows=[
        ("#", "Strip number; click to select it (see multi-selection)."),
        ("Strip name", "Button name. The only required cell."),
        ("Track name", "Renames the track. Several selected tracks: Tom 1, Tom 2, Tom 3…"),
        ("Tag", "Adds a 1 to 3 character tag at the end of the name: “Kick in [KIK]”. An existing tag is replaced."),
        ("Colour", "Track colour. Set to choose one, x to remove it."),
        ("Icon", "Track icon. Browse opens Data/track_icons (62 cs_tags_XXX icons included)."),
        ("Layout", "TCP and MCP layouts of the current theme, or the theme default."),
        ("Record input", "Mono, stereo or MIDI input; or Record output stereo / mono / MIDI."),
        ("Pan mode", "Project default, Stereo balance / mono pan, Stereo pan, Dual pan, Balance (classic 3.x)."),
        ("Metering", "Stereo peaks, Multichannel peaks, Stereo RMS, Combined RMS, LUFS-M, LUFS-S, Meter disabled."),
        ("FX chain", ".RfxChain file added after the existing FX. Browse opens FXChains."),
        ("Envelopes", "Envelopes made visible: Volume, Pan, Width, Mute, Trim volume."),
        ("Item name", "Renames every item on the track, numbered by position when there are several."),
        ("Normalize", "LUFS-I, RMS, Peak or True peak, target in dB, each item or all together. "
                      "Off by default (box unticked); ticking it suggests -15 dBFS Peak, together."),
        ("Group", "Track group (1 to 64 or 128), group name and lead / follow flags."),
    ],
    s5_rec="Choosing an input switches the track back to recording its input if it was recording its output; "
           "MIDI modes (overdub…) are left alone.",
    s5_norm="“All together” applies one common gain and keeps the balance between items: in Peak, the loudest item reaches "
            "the target; in LUFS or RMS, the measure combines all items, weighted by their length (approximation).",
    s6="6. Advanced features",
    s6_items=[
        ("Multi-selection", "Click a row number (#): select it. Ctrl+click: add or remove. Shift+click: a whole range. "
                            "A change made in a selected row is copied to every selected row, except the strip name. "
                            "Only the changed setting is copied."),
        ("Tag inheritance", "The first strip of a tag in a folder (e.g. Cymbals for [CYM]) passes its colour and icon to the "
                            "other strips of the same tag in that folder that have none, or that had inherited the same value."),
        ("Load default strips", "Adds the missing default strips (track name, tag, icon; no normalization). "
                                "Never changes existing strips; can be run again without creating duplicates."),
        ("Export… / Import…", "Export: all strips, one folder or the strips without folder, to a .rnstrips file "
                              "(default Data/ReNo_StripBuddy/Exports). Import: added to your strips (folders with the same "
                              "name merged, duplicates skipped) or replacing everything."),
        ("Clear all strips", "Deletes every strip, and the folders if the box is ticked. Cannot be undone: "
                             "Export first."),
    ],
    sd="7. The tag Display",
    sdp=["The Display is a small floating bar without a title, to place wherever you like. The <b>Strip Buddy</b> button, drawn like "
         "the toolbar icon, opens or closes the main window; it is lit while the window is open. Then four options "
         "to turn on (one or more): <b>Zoom</b>, <b>View</b>, <b>Scroll</b>, <b>Select</b>. On the right, the drop-down "
         "list of the project's tags (the [ABC] at the end of track names), with <b>All</b> first. Picking a tag applies "
         "every option that is on, in the order View, Select, Zoom, Scroll (one undo step).",
         "Open it with the action “ReNo Mellow - Strip Buddy - Display”, or the “Open / close the Display” button of "
         "the Display tab. Running the action again closes the Display."],
    sd_head=["Option", "With a tag", "With All"],
    sd_rows=[
        ("View", "Shows only the tracks of the tag; their folder parents stay visible.", "Shows every track again."),
        ("Zoom", "Enlarges the tag's tracks to fill the arrange height.", "Resets the track heights."),
        ("Scroll", "Brings the tag's first track to the top (TCP) or to the left (mixer).", "Goes back to the first track."),
        ("Select", "Selects the tag's tracks (ready for a strip).", "Selects every track."),
    ],
    sd_more=["<b>Mouse wheel</b> over the list: next / previous tag, applied at once. Each tag shows the colour of its first "
             "track. <b>Right-click</b> the bar: text size, reopen at startup, Open / Close Strip Buddy, Close.",
             "<b>Display</b> tab of the main window: <b>Display View</b> (TCP, MCP or Both: where View hides tracks), "
             "<b>Display Scroll</b> (TCP, MCP or Both: where Scroll scrolls), and “Reopen the Display when REAPER starts”.",
             "Precise Zoom and Scroll use js_ReaScriptAPI; without it, Zoom goes through SWS if installed and Scroll through "
             "the native action “Vertical scroll selected tracks into view”."],
    callout_disp="Example: View and Scroll on, tag KIK picked in the list.",
    s7="8. Files, actions and shortcuts",
    s7_rows=[
        ("Actions", "“ReNo Mellow - Strip Buddy” (opens / closes the window) and “ReNo Mellow - Strip Buddy - Display” (opens / closes the Display)."),
        ("Shortcut", "None imposed: choose your own in the action list (e.g. Ctrl+Shift+C, just an example)."),
        ("Data", "Data/ReNo_StripBuddy/strips.lua, saved automatically after each change."),
        ("Exports", "Data/ReNo_StripBuddy/Exports/*.rnstrips"),
        ("Icons", "Data/track_icons/cs_tags_XXX.png (tracks), Data/toolbar_icons/ReNo_StripBuddy.png (toolbar)."),
    ],
    s7_head=["Item", "Detail"],
    s8="9. FAQ",
    faq=[
        ("I was using Custom Strips.", "In ReaPack, first uninstall Custom Strips, then install Strip Buddy. "
                                       "On first run, your strips, folders, exports and settings are brought over automatically. "
                                       "Replace the old toolbar button with the action “ReNo Mellow - Strip Buddy”."),
        ("The script says ReaImGui is missing.", "Install ReaImGui with ReaPack (Browse packages), then restart REAPER."),
        ("Nothing happens when I click.", "No track is selected: the message “Select one or more tracks first.” "
                                          "appears at the bottom of the window."),
        ("ReaPack does not see the new version.", "GitHub may serve the old index for about 5 minutes: "
                                                  "wait, then Synchronize packages again."),
        ("My strips don't have the new default settings.", "Load default strips only adds missing strips. "
                                                          "Use multi-selection to set several strips at once."),
        ("A strip name is cut on its button.", "Buttons have a fixed width: use a shorter strip name; "
                                               "the track name can stay long."),
    ],
    sch_strips="Strips tab", sch_setup="Setup tab",
)

# ----------------------------------------------------------------------------------------------
# Drawn schemas (simplified, clearly not screenshots)
# ----------------------------------------------------------------------------------------------
STRIP_COLS = ["#E74C3C", "#E74C3C", "#E74C3C", "#E74C3C", "#F39C12", "#F39C12", "#26BAAA", "#3B82F6"]


class StripsSchema(Flowable):
    def __init__(self, t, w=170 * mm, h=62 * mm):
        super().__init__(); self.t, self.width, self.height = t, w, h

    def draw(self):
        c, W, H = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#2B2B2B")); c.roundRect(0, 0, W, H, 4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#3A3A3A")); c.rect(0, H - 9 * mm, W, 9 * mm, fill=1, stroke=0)
        c.setFont("DVB", 8); c.setFillColor(colors.white)
        c.drawString(4 * mm, H - 6 * mm, "ReNo Mellow - Strip Buddy " + VERSION)
        # tabs
        c.setFillColor(colors.HexColor("#555555")); c.rect(4 * mm, H - 16 * mm, 20 * mm, 6 * mm, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#333333")); c.rect(25 * mm, H - 16 * mm, 18 * mm, 6 * mm, fill=1, stroke=0)
        c.setFont("DV", 7); c.setFillColor(colors.white)
        c.drawString(6 * mm, H - 14 * mm, "Strips"); c.drawString(27 * mm, H - 14 * mm, "Setup")
        # folder list
        c.setStrokeColor(colors.HexColor("#666666")); c.setFillColor(colors.HexColor("#252525"))
        c.rect(4 * mm, 4 * mm, 40 * mm, H - 22 * mm, fill=1, stroke=1)
        names = ["All strips  (164)", "Drums  (39)", "Drum pad  (8)", "Percussion  (21)", "…", "No folder  (0)"]
        y = H - 24 * mm
        for i, n in enumerate(names):
            if i == 1:
                c.setFillColor(colors.HexColor("#3A6EA5")); c.rect(5 * mm, y - 1.2 * mm, 38 * mm, 4.4 * mm, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("DV", 6.5); c.drawString(6.5 * mm, y, n); y -= 5 * mm
        c.setFillColor(colors.HexColor("#444444")); c.rect(5 * mm, 5.5 * mm, 38 * mm, 5 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.drawCentredString(24 * mm, 7.2 * mm, "+ New folder")
        # strip buttons
        labels = ["Drums", "Kick", "Kick in", "Kick out", "Snare", "Snare top", "Cymbals", "Room"]
        x0, y0 = 49 * mm, H - 30 * mm
        for i, lab in enumerate(labels):
            col, row = i % 4, i // 4
            x, yy = x0 + col * 29 * mm, y0 - row * 14 * mm
            c.setFillColor(colors.HexColor(STRIP_COLS[i])); c.roundRect(x, yy, 26 * mm, 10 * mm, 2, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("DVB", 8); c.drawCentredString(x + 13 * mm, yy + 3.6 * mm, lab)
        # callouts
        c.setFillColor(colors.HexColor("#BBBBBB")); c.setFont("DVI", 6.5)
        c.drawString(49 * mm, 8 * mm, self.t["callout_strips"])


class SetupSchema(Flowable):
    def __init__(self, t, w=170 * mm, h=40 * mm):
        super().__init__(); self.t, self.width, self.height = t, w, h

    def draw(self):
        c, W, H = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#2B2B2B")); c.roundRect(0, 0, W, H, 4, fill=1, stroke=0)
        btns = ["+ Add strip", "Load default strips", "Export...", "Import...", "Clear all strips"]
        x = 4 * mm
        c.setFont("DV", 6.5)
        for b in btns:
            w = c.stringWidth(b, "DV", 6.5) + 4 * mm
            c.setFillColor(colors.HexColor("#444444")); c.rect(x, H - 9 * mm, w, 5 * mm, fill=1, stroke=0)
            c.setFillColor(colors.white); c.drawString(x + 2 * mm, H - 7.3 * mm, b); x += w + 2 * mm
        cols = ["#", "Strip name", "Track name", "Tag", "Colour", "Icon", "…", "Normalize", "Group"]
        widths = [7, 24, 24, 11, 14, 24, 10, 30, 18]
        ys = [H - 15 * mm, H - 21 * mm, H - 27 * mm, H - 33 * mm]
        rows = [cols, ["1", "Drums", "Drums", "DRM", "", "cs_tags_DRM", "", "-", "-"],
                ["2", "Kick", "Kick", "KIK", "", "cs_tags_KIK", "", "-", "-"],
                ["3", "Kick in", "Kick in", "KIK", "", "cs_tags_KIK", "", "-", "-"]]
        for r, (yy, row) in enumerate(zip(ys, rows)):
            x = 4 * mm
            if r == 0:
                c.setFillColor(colors.HexColor("#3A3A3A")); c.rect(4 * mm, yy - 1.5 * mm, sum(widths) * mm, 5 * mm, fill=1, stroke=0)
            elif r in (2, 3):
                c.setFillColor(colors.HexColor("#4A7FC0")); c.rect(4 * mm, yy - 1.5 * mm, sum(widths) * mm, 5 * mm, fill=1, stroke=0)
            for k, (val, w) in enumerate(zip(row, widths)):
                if r > 0 and k == 4:
                    c.setFillColor(colors.HexColor("#E74C3C")); c.rect(x + 2 * mm, yy - 0.5 * mm, 4 * mm, 3 * mm, fill=1, stroke=0)
                c.setFillColor(colors.white); c.setFont("DVB" if r == 0 else "DV", 6.3)
                c.drawString(x + 1 * mm, yy, val); x += w * mm
        c.setFillColor(colors.HexColor("#BBBBBB")); c.setFont("DVI", 6.5)
        c.drawString(4 * mm, 3 * mm, self.t["callout_setup"])


class DisplaySchema(Flowable):
    def __init__(self, t, w=170 * mm, h=36 * mm):
        super().__init__(); self.t, self.width, self.height = t, w, h

    def draw(self):
        c, W, H = self.canv, self.width, self.height
        bx, by, bw, bh = 4 * mm, H - 16 * mm, 130 * mm, 12 * mm
        c.setFillColor(colors.HexColor("#2B2B2B")); c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=0)
        x = bx + 2.5 * mm
        w0 = 9 * mm
        c.drawImage(os.path.join(HERE, "icon_on.png"), x, by + 1.5 * mm, w0, w0, mask="auto")
        x += w0 + 1.5 * mm
        c.setFillColor(colors.HexColor("#888888")); c.drawString(x + 0.5 * mm, by + 5 * mm, "|"); x += 4 * mm
        for name, on in (("Zoom", False), ("View", True), ("Scroll", True), ("Select", False)):
            w = c.stringWidth(name, "DV", 8) + 5 * mm
            c.setFillColor(colors.HexColor("#2E7D32" if on else "#4A4A4A")); c.roundRect(x, by + 2.5 * mm, w, 7 * mm, 2, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("DV", 8); c.drawCentredString(x + w / 2, by + 5 * mm, name); x += w + 1.5 * mm
        c.setFillColor(colors.HexColor("#888888")); c.drawString(x + 1 * mm, by + 5 * mm, "|"); x += 5 * mm
        c.setFillColor(colors.HexColor("#E74C3C")); c.rect(x, by + 3.5 * mm, 5 * mm, 5 * mm, fill=1, stroke=0); x += 6.5 * mm
        c.setFillColor(colors.HexColor("#4A4A4A")); c.roundRect(x, by + 2.5 * mm, 26 * mm, 7 * mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.white); c.drawString(x + 2 * mm, by + 5 * mm, "KIK   v")
        # open list
        lx, ly = x, by - 18 * mm
        c.setFillColor(colors.HexColor("#333333")); c.rect(lx, ly, 26 * mm, 17.5 * mm, fill=1, stroke=0)
        for k, (n, col) in enumerate((("All", None), ("KIK", "#E74C3C"), ("SNR", "#E74C3C"), ("BSS", "#26BAAA"))):
            yy = ly + 13.5 * mm - k * 4.2 * mm
            if n == "KIK":
                c.setFillColor(colors.HexColor("#3A6EA5")); c.rect(lx + 0.5 * mm, yy - 1 * mm, 25 * mm, 4 * mm, fill=1, stroke=0)
            if col:
                c.setFillColor(colors.HexColor(col)); c.rect(lx + 1.5 * mm, yy - 0.3 * mm, 2.6 * mm, 2.6 * mm, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("DV", 7); c.drawString(lx + 5.5 * mm, yy, n)
        c.setFillColor(GREY); c.setFont("DVI", 7.5)
        words, line, lines = self.t["callout_disp"].split(), "", []
        for wd in words:
            if c.stringWidth(line + " " + wd, "DVI", 7.5) > 40 * mm and line:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        for k, ln in enumerate(lines):
            c.drawString(lx + 32 * mm, by - 6 * mm - k * 3.8 * mm, ln)


T["fr"]["callout_strips"] = "Clic = appliquer · glisser = réordonner ou ranger · clic droit = menu"
T["fr"]["callout_setup"] = "Lignes 2 et 3 sélectionnées (en bleu) : une modification dans l'une est copiée dans l'autre."
T["en"]["callout_strips"] = "Click = apply · drag = reorder or file · right-click = menu"
T["en"]["callout_setup"] = "Rows 2 and 3 selected (blue): a change in one is copied to the other."


# ----------------------------------------------------------------------------------------------
def table(head, rows, widths, first_bold=True):
    data = [[Paragraph(h, ST["head"]) for h in head]]
    for r in rows:
        data.append([Paragraph(r[0], ST["cellb"] if first_bold else ST["cell"]), Paragraph(r[1], ST["cell"])])
    tb = Table(data, colWidths=widths, repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return tb


def numbered(items):
    return [Paragraph(s, ST["li"], bulletText="%d." % (i + 1)) for i, s in enumerate(items)]


def build(lang):
    t = T[lang]
    out = os.path.join(HERE, t["file"])

    def on_page(c, doc):
        if doc.page == 1:
            return
        c.saveState(); c.setFont("DV", 7.5); c.setFillColor(GREY)
        c.drawString(18 * mm, 10 * mm, t["footer"])
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, "%s %d" % (t["page"], doc.page))
        c.setStrokeColor(colors.HexColor("#DDDDDD")); c.line(18 * mm, 13 * mm, A4[0] - 18 * mm, 13 * mm)
        c.restoreState()

    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                          bottomMargin=18 * mm, title="ReNo Mellow - Strip Buddy " + VERSION, author="ReNo Mellow")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    W = doc.width
    s = []

    # cover
    s.append(Spacer(1, 45 * mm))
    s.append(Image(os.path.join(HERE, "icon_200.png"), width=60 * mm, height=20 * mm))
    s.append(Spacer(1, 12 * mm))
    s.append(Paragraph("ReNo Mellow – Strip Buddy", ST["title"]))
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph(t["subtitle"], ST["sub"]))
    s.append(Spacer(1, 3 * mm))
    s.append(Paragraph("%s · version %s" % (t["manual"], VERSION), ST["sub"]))
    s.append(Spacer(1, 18 * mm))
    s.append(Paragraph(t["toc_title"], ParagraphStyle("tt", parent=ST["h1"], alignment=TA_CENTER)))
    for line in t["toc"]:
        s.append(Paragraph(line, ST["toc"]))
    s.append(Spacer(1, 16 * mm))
    s.append(Paragraph(t["other"], ST["center"]))
    s.append(PageBreak())

    # 1
    s.append(Paragraph(t["s1"], ST["h1"]))
    for p in t["s1p"]:
        s.append(Paragraph(p, ST["p"]))
    # 2
    s.append(Paragraph(t["s2"], ST["h1"]))
    s.append(KeepTogether([Paragraph(t["s2a"], ST["h2"])] + numbered(t["s2a_steps"])))
    s.append(KeepTogether([Paragraph(t["s2b"], ST["h2"])] + numbered(t["s2b_steps"])))
    s.append(KeepTogether([Paragraph(t["s2c"], ST["h2"])] + [Paragraph(p, ST["p"]) for p in t["s2c_p"]]))
    links = [(a, '<font name="DVM" size="7.2">%s</font>' % b) for a, b in t["links"]]
    s.append(Spacer(1, 2 * mm))
    s.append(table(t["links_head"], links, [34 * mm, W - 34 * mm]))
    # 3
    s.append(KeepTogether([Paragraph(t["s3"], ST["h1"])] + numbered(t["s3_steps"])))
    # 4
    s.append(KeepTogether([Paragraph(t["s4"], ST["h1"]), Paragraph(t["s4p"], ST["p"]), StripsSchema(t),
                           Paragraph(t["schema_note"], ST["note"])]))
    s.append(table(t["s4_head"], t["s4_rows"], [50 * mm, W - 50 * mm]))
    # 5
    s.append(KeepTogether([Paragraph(t["s5"], ST["h1"]), Paragraph(t["s5p"], ST["p"]), SetupSchema(t),
                           Paragraph(t["schema_note"], ST["note"])]))
    s.append(table(t["s5_head"], t["s5_rows"], [28 * mm, W - 28 * mm]))
    s.append(Spacer(1, 3 * mm))
    s.append(Paragraph(t["s5_rec"], ST["p"]))
    s.append(Paragraph(t["s5_norm"], ST["p"]))
    # 6
    s.append(Paragraph(t["s6"], ST["h1"]))
    for head, body in t["s6_items"]:
        s.append(KeepTogether([Paragraph(head, ST["h2"]), Paragraph(body, ST["p"])]))
    # 7 Display
    s.append(KeepTogether([Paragraph(t["sd"], ST["h1"])] + [Paragraph(p, ST["p"]) for p in t["sdp"]] +
                          [DisplaySchema(t), Paragraph(t["schema_note"], ST["note"])]))
    data = [[Paragraph(h, ST["head"]) for h in t["sd_head"]]]
    for a, b, c2 in t["sd_rows"]:
        data.append([Paragraph(a, ST["cellb"]), Paragraph(b, ST["cell"]), Paragraph(c2, ST["cell"])])
    tb = Table(data, colWidths=[22 * mm, W - 72 * mm, 50 * mm], repeatRows=1)
    tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACCENT), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
                            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s.append(tb); s.append(Spacer(1, 3 * mm))
    for p in t["sd_more"]:
        s.append(Paragraph(p, ST["p"]))
    # 8
    s.append(KeepTogether([Paragraph(t["s7"], ST["h1"]), table(t["s7_head"], t["s7_rows"], [28 * mm, W - 28 * mm])]))
    # 8
    s.append(Paragraph(t["s8"], ST["h1"]))
    for q, a in t["faq"]:
        s.append(KeepTogether([Paragraph("<b>%s</b>" % q, ST["p"]), Paragraph(a, ST["li"])]))
    doc.build(s)
    return out


if __name__ == "__main__":
    for lg in ("fr", "en"):
        print(build(lg))
