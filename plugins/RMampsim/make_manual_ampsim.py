# Manuel RMampsim (FR / EN) - reportlab + DejaVu
# python3 make_manual_ampsim.py  (dans ce dossier) -> RMampsim_manuel_FR.pdf, RMampsim_manual_EN.pdf
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image

pdfmetrics = __import__('reportlab.pdfbase.pdfmetrics', fromlist=['x'])
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
ACC = colors.HexColor('#6cd9c7'); DARK = colors.HexColor('#1d1f23'); GREY = colors.HexColor('#5b5f66'); TEAL = colors.HexColor('#2a9d8f')
VERSION = '1.0'
BASE = 'https://github.com/renothestraws/reno-mellow-manuals/raw/main/plugins/RMampsim/'
HERE = os.path.dirname(os.path.abspath(__file__))
IMG_FACE = os.path.join(HERE, 'ampsim_face.png')
IMG_BROWSER = os.path.join(HERE, 'ampsim_browser.png')
REPO = 'https://raw.githubusercontent.com/renothestraws/reno-mellow/main/index.xml'

FR = dict(
 file='RMampsim_manuel_FR.pdf', other=('English version', BASE + 'RMampsim_manual_EN.pdf'),
 sub="Lecteur de modèles Neural Amp Modeler (NAM) A2 et chargeur d'IR de baffle pour REAPER",
 foot='ReNo Mellow - RMampsim %s - manuel' % VERSION,
 cap_face="La façade (rendu par le code du plug-in, couleur verte).",
 cap_browser="Le navigateur de modèles : dossiers à gauche, modèles à droite.",
 call=("<b>À NE PAS OUBLIER : « ReNo Mellow - IR Buddy - Rescan RM IR »</b>",
       "RMampsim ne lit pas directement les fichiers .nam : cette action les <b>convertit</b> et met à jour la liste des modèles "
       "et des baffles. Lancez-la : <b>1.</b> une fois après l'installation ; <b>2.</b> chaque fois que vous ajoutez, renommez ou "
       "supprimez un .nam dans REAPER/Data/RM Amp ou une IR dans REAPER/Data/RM IR/Cab ; <b>3.</b> si le plug-in affiche « NO MODEL » "
       "ou si un modèle manque dans la liste."),
 hd=('Réglage', 'Plage', 'Effet'), hd2=('Geste', 'Effet'), hd3=('Champ', 'Effet'), hd4=('Dossier / fichier', 'Contenu'),
 S=[
  ('1. Présentation', [
   "<b>RMampsim</b> fait jouer des <b>modèles d'amplis NAM</b> (Neural Amp Modeler) : un réseau de neurones entraîné à reproduire "
   "un ampli réel ou un plug-in d'ampli, réglé d'une certaine façon. RMampsim lit le format récent <b>A2</b>, directement en JSFX "
   "et <b>sans latence</b>, puis fait passer le son dans une <b>IR de baffle</b>.",
   "IMAGE_FACE",
   "Chaîne : entrée (L+R)/2 → INPUT et IN CAL → modèle NAM A2 → normalisation → EQ (BASS, MID, TREBLE, PRESENCE) → "
   "baffle (IR) et MIC → LEVEL → écrêteur de sécurité à 0 dBFS. La sortie est en stéréo identique sur les deux canaux.",
   "RMampsim est livré avec <b>17 modèles A2</b> (7 têtes, 10 « full rigs ») et <b>10 IR de baffle</b>, tous faits par ReNo Mellow. "
   "Par défaut, une nouvelle instance charge <b>Hot Plexi Head</b> et le baffle <b>British Vintage 4x12</b>.",
  ]),
  ('2. Installation', [
   "RMampsim a besoin du paquet de scripts <b>IR Buddy</b> (commun avec RM1982Verb) : c'est lui qui convertit les modèles et "
   "prépare vos captures. Installez les deux :",
   "BUL:<b>ReaPack</b> : dépôt ReNo Mellow (<i>%s</i>), catégorie <b>Amp</b> → <b>RMampsim</b>, et catégorie <b>Scripts</b> → "
   "<b>ReNo Mellow - IR Buddy</b>." % REPO,
   "BUL:<b>Sans ReaPack</b> : glissez <b>RMampsim.ReaperPkg</b> puis <b>IR Buddy.ReaperPkg</b> dans la fenêtre de REAPER (7.86+).",
   "Ensuite, lancez une fois l'action <b>ReNo Mellow - IR Buddy - Rescan RM IR</b> (Actions &gt; Show action list).",
   "CALLOUT",
   "Sont installés : le plug-in (navigateur d'effets, chercher « RMampsim »), les fichiers suivants, et les actions d'IR Buddy.",
   "TABLE4",
   "<b>Fréquence d'échantillonnage</b> : les modèles NAM sont faits pour <b>48 kHz</b>. À une autre fréquence le plug-in fonctionne, "
   "mais le son s'écarte un peu de l'original : réglez le projet à 48 kHz (Project settings) pour le son exact.",
  ]),
  ('3. Choisir un modèle et un baffle', [
   "BUL:<b>Cliquez sur le nom du modèle</b> : le <b>navigateur</b> s'ouvre (dossiers à gauche, modèles à droite ; molette pour défiler, "
   "clic pour charger). La fenêtre reste ouverte pour comparer ; × ou un nouveau clic sur le nom la ferme.",
   "IMAGE_BROWSER",
   "BUL:<b>Flèches &lt; &gt;</b> : modèle précédent / suivant du même dossier.",
   "BUL:<b>LITE / FULL</b> : un fichier A2 contient deux tailles du même modèle. LITE est léger pour le processeur ; FULL est un peu "
   "plus fidèle mais plusieurs fois plus lourd. Commencez en LITE, passez en FULL pour le mixage final si votre ordinateur suit.",
   "BUL:<b>AMP</b> éteint : le modèle est contourné, RMampsim devient un simple <b>chargeur d'IR de baffle</b> (pour un ampli déjà "
   "simulé ailleurs, ou une prise de son DI passée dans un vrai préampli).",
   "BUL:<b>Baffle</b> : même principe, cliquez sur le nom de l'IR sous CABINET (seul le dossier REAPER/Data/RM IR/Cab est listé), "
   "ou <b>glissez un fichier .wav</b> n'importe où sur la fenêtre. <b>CAB</b> allume / éteint le baffle.",
   "<b>Têtes et full rigs.</b> Un modèle « <b>Head</b> » est un ampli seul : il lui faut un baffle. Un modèle « <b>Full Rig</b> » "
   "(ou « Amp + Cab ») contient déjà le baffle et le micro : quand vous le choisissez, RMampsim <b>coupe CAB automatiquement</b> "
   "et l'en-tête affiche « full rig (cab in model) ». En revenant à une tête, CAB se rallume. Vous pouvez toujours forcer CAB à la main.",
  ]),
  ('4. Réglages', ['TABLE']),
  ('5. Ajouter vos propres modèles NAM', [
   "Vous pouvez ajouter autant de modèles que vous voulez : les vôtres (voir section 6) ou ceux de la communauté.",
   "BUL:<b>Trouver des modèles A2</b> : sur <b>tone3000.com</b>, la page de chaque tone indique les modèles <b>A2-Full / A2-Lite</b>. "
   "Seuls les modèles <b>A2</b> sont lus ; les anciens modèles A1 (« Standard », « Lite », « Feather », « Nano ») sont ignorés "
   "et listés par le Rescan.",
   "BUL:<b>Les ranger</b> : copiez les fichiers <b>.nam</b> dans <b>REAPER/Data/RM Amp</b>. Les sous-dossiers sont permis et "
   "deviennent les dossiers du navigateur (par exemple RM Amp/Mes captures/Crunch). L'action <b>ReNo Mellow - IR Buddy - Open RM Amp folder</b> "
   "ouvre ce dossier.",
   "BUL:<b>Les convertir</b> : lancez <b>Rescan RM IR</b>. Chaque .nam est converti une fois (les suivants vont plus vite) et un message "
   "indique combien de modèles sont prêts, et lesquels ont été ignorés.",
   "BUL:<b>Full rig</b> : RMampsim reconnaît un modèle avec baffle grâce au type indiqué dans le fichier (TONE3000 « Amp + Cab ») ou "
   "à son nom ou à son dossier : « Full Rig », « Amp + Cab », « Amp Cab », « Combo ». Pour un full rig mal reconnu, ajoutez « Full Rig » "
   "au nom du fichier et relancez le Rescan.",
   "BUL:<b>IN CAL</b> : certains modèles indiquent le niveau d'entrée de la capture (en dBu) ; la zone MODEL affiche alors "
   "« captured at +xx dBu ». Réglez IN CAL au niveau de votre interface pour 0 dBFS (fiche technique de votre entrée instrument) : "
   "la guitare attaque le modèle comme le vrai ampli. Sans cette information, IN CAL est grisé (« not used by this model »).",
   "Les modèles que vous téléchargez restent la propriété de leurs auteurs : gardez-les pour votre usage, ne les redistribuez "
   "pas sans leur accord.",
  ]),
  ('6. Capturer votre propre ampli (Capture for NAM)', [
   "L'action <b>ReNo Mellow - IR Buddy - Capture for NAM</b> fait passer le <b>signal de capture officiel</b> de NAM "
   "(« T3K sweep v3 », 3 min 10 s, fourni dans REAPER/Data/RM Amp/Capture signal) dans votre plug-in d'ampli, et enregistre la sortie. "
   "L'entraînement se fait ensuite gratuitement sur <b>TONE3000</b>, qui vous rend un fichier .nam A2.",
   "<b>a. Préparer</b>",
   "BUL:Projet à <b>48 kHz</b>.",
   "BUL:Sur une piste : votre plug-in d'ampli réglé comme vous voulez le capturer, <b>sans noise gate</b>.",
   "BUL:<b>Ampli seul</b> (« Head ») : coupez le baffle / l'IR du plug-in. <b>Full rig</b> : laissez-le allumé "
   "(une IR de baffle classique, pas une réverbe de pièce longue).",
   "BUL:Sélectionnez la piste.",
   "<b>b. Lancer l'action</b> : une fenêtre demande trois réglages, mémorisés pour la fois suivante.",
   "TABLE3",
   "Le fichier <b>« nom - output.wav »</b> (WAV 24 bits mono, exactement la longueur du signal) est créé dans "
   "<b>REAPER/Data/RM Amp/Captures (to train)</b>. Si l'ampli dépasse 0 dBFS, son niveau est baissé et le message le signale : "
   "c'est sans conséquence pour NAM.",
   "<b>c. Entraîner sur TONE3000</b>",
   "BUL:Sur <b>tone3000.com</b>, créez une capture (compte gratuit), signal <b>« T3K sweep v3 »</b>, type <b>Amp Head</b> "
   "(ampli seul) ou <b>Amp + Cab</b> (full rig).",
   "BUL:Envoyez le fichier « … - output.wav » comme <b>sortie</b> (output). Vous n'avez pas à envoyer le signal d'entrée.",
   "BUL:<b>Advanced</b> : Max Epochs <b>400 – Max</b> pour la meilleure fidélité (plus long). <b>Calibration</b> (Send / Return Level) : "
   "laissez <b>vide</b> pour un plug-in ; pour un vrai ampli, indiquez les niveaux de votre interface (dBu pour 0 dBFS) : IN CAL pourra s'en servir.",
   "BUL:Pendant l'entraînement, l'<b>ESR</b> (écart entre le modèle et l'original) baisse : sous 0,01, la différence est quasi inaudible.",
   "<b>d. Utiliser le modèle</b> : téléchargez le .nam (A2) dans <b>REAPER/Data/RM Amp</b>, gardez « Full Rig » dans son nom si c'en est un, "
   "lancez <b>Rescan RM IR</b> : le modèle apparaît dans le navigateur de RMampsim.",
   "<b>Un vrai ampli ?</b> Insérez sur la piste le plug-in <b>ReaInsert</b> (sortie vers l'entrée de l'ampli par une re-amp box, retour "
   "du micro ou de la sortie ligne), réglez sa latence, et répondez <b>Y</b> à « Real time ». Le signal passe à pleine échelle : "
   "réglez le volume d'écoute avant de lancer.",
  ]),
  ('7. Vos propres baffles', [
   "Copiez vos IR de baffle (.wav, mono ou stéréo, 10 s max, rééchantillonnage automatique) dans <b>REAPER/Data/RM IR/Cab</b> "
   "(sous-dossiers permis), puis lancez <b>Rescan RM IR</b>. Pour un essai rapide, glissez simplement le fichier sur RMampsim.",
   "Pour capturer le baffle d'un plug-in de simulation : action <b>ReNo Mellow - IR Buddy</b> sur la piste du plug-in de baffle seul, "
   "sous-dossier <b>Cab</b>, sortie <b>M</b> (mono). <b>MIC</b> déplace ensuite le micro virtuel du centre (brillant) vers le bord (plus sombre).",
  ]),
  ('8. Souris et clavier', ['TABLE2']),
  ('9. Questions fréquentes', [
   "QA:« NO MODEL - click to browse » ou liste vide|L'index n'existe pas encore : lancez <b>Rescan RM IR</b> (IR Buddy doit être installé), "
   "puis rouvrez le navigateur. Le modèle par défaut se charge sur une nouvelle instance.",
   "QA:Mon modèle n'apparaît pas|C'est un modèle A1 (le Rescan le liste comme ignoré), ou le Rescan n'a pas été relancé après la copie.",
   "QA:Ça sature / c'est trop fort|Baissez INPUT ou LEVEL. Les modèles sont normalisés à partir de leur volume ; une guitare très chaude "
   "peut sortir plus fort. Un écrêteur de sécurité limite la sortie à 0 dBFS.",
   "QA:Le processeur est très chargé|Passez en <b>LITE</b>. Utilisez FULL au rendu, ou figez la piste (Freeze).",
   "QA:Le son est différent de l'original|Vérifiez le projet à 48 kHz, la normalisation (LEVEL), le baffle (un full rig n'en a pas besoin) "
   "et, pour un ampli calibré, IN CAL.",
   "QA:Le navigateur de baffles montre seulement « Cab »|C'est voulu : seules les IR de REAPER/Data/RM IR/Cab sont proposées, pas les "
   "IR de réverbe de RM1982Verb.",
  ]),
 ],
 rows=[('AMP', 'ON / OFF', "Allume le modèle. OFF = chargeur d'IR de baffle seul."),
       ('Modèle', 'navigateur, &lt; &gt;', "Choix du modèle NAM A2 (section 3)."),
       ('LITE / FULL', '', "Taille du modèle : léger ou plus fidèle."),
       ('INPUT', '-24 – +24 dB', "Gain avant le modèle : plus de saturation vers la droite."),
       ('BASS / MID / TREBLE', '±12 dB', "EQ après l'ampli : plateau 120 Hz, cloche 750 Hz, plateau 2,8 kHz."),
       ('PRESENCE', '±12 dB', "Cloche 5,5 kHz : mordant et brillance."),
       ('LEVEL', '-24 – +12 dB', "Volume de sortie. Les modèles sont normalisés (-24 dB de volume moyen)."),
       ('CAB', 'ON / OFF', "Allume le baffle. Coupé automatiquement pour un full rig."),
       ('Baffle', 'navigateur, &lt; &gt;', "IR de REAPER/Data/RM IR/Cab, ou .wav glissé sur la fenêtre."),
       ('MIC', '0 – 100 %', "Position du micro : centre (0, brillant) vers bord (100, plus sombre)."),
       ('IN CAL', 'OFF, 0 – 30 dBu', "Niveau de votre interface pour 0 dBFS. Utilisé si le modèle indique son niveau de capture."),
       ('Mètres IN / OUT', '', "Niveaux d'entrée et de sortie (dBFS).")],
 rows2=[('Glisser un potard (vertical)', 'Régler ; Shift = réglage fin ; molette aussi.'),
        ('Ctrl-clic (Cmd-clic) sur un potard', 'Valeur par défaut.'),
        ('Clic sur une valeur / double-clic sur un potard', 'Saisie au clavier : 3, -6, off ; Entrée = valider, Échap = annuler.'),
        ('Clic sur le nom du modèle / du baffle', 'Ouvre / ferme le navigateur.'),
        ('Glisser un .wav sur la fenêtre', 'Charge ce fichier comme baffle.'),
        ('Double-clic sur « RMampsim »', 'Couleur verte / orange.'),
        ('Boutons SIZE', 'Taille de la fenêtre : 75 à 200 %.')],
 rows3=[('Capture name', "Nom du fichier. Proposé : le nom du premier effet actif. Avec Cab = Y, « Full Rig » est ajouté au nom."),
        ('Cab in capture (Y / N)', "N = ampli seul (baffle du plug-in coupé). Y = full rig (baffle compris)."),
        ('Real time (Y / N)', "N = rendu hors temps réel, en quelques secondes. Y = temps réel (environ 3 min 15 s, le transport enregistre), "
         "pour les plug-ins sur DSP externe (UAD…) ou un vrai ampli par ReaInsert. Si le rendu hors ligne ne donne que du silence, "
         "l'action propose de recommencer en temps réel.")],
 rows4=[('REAPER/Data/RM Amp/ReNo Mellow', "Les 17 modèles d'usine (Heads, Full Rigs). Vos modèles vont dans REAPER/Data/RM Amp."),
        ('REAPER/Data/RM IR/Cab', "Les 10 IR de baffle d'usine ; vos IR de baffle vont ici."),
        ('REAPER/Data/RM Amp/Capture signal', "T3K-sweep-v3.wav, le signal de capture NAM (utilisé par Capture for NAM)."),
        ('REAPER/Data/RMIRIndex', "Index et modèles convertis, écrits par le Rescan (ne pas modifier).")],
)

EN = dict(
 file='RMampsim_manual_EN.pdf', other=('Version française', BASE + 'RMampsim_manuel_FR.pdf'),
 sub='Neural Amp Modeler (NAM) A2 player and cabinet IR loader for REAPER',
 foot='ReNo Mellow - RMampsim %s - manual' % VERSION,
 cap_face='The panel (rendered by the plug-in code, green colour).',
 cap_browser='The model browser: folders on the left, models on the right.',
 call=("<b>DON'T FORGET: \"ReNo Mellow - IR Buddy - Rescan RM IR\"</b>",
       "RMampsim does not read .nam files directly: this action <b>converts</b> them and updates the list of models and cabinets. "
       "Run it: <b>1.</b> once after installing; <b>2.</b> every time you add, rename or delete a .nam in REAPER/Data/RM Amp or an IR in "
       "REAPER/Data/RM IR/Cab; <b>3.</b> when the plug-in shows \"NO MODEL\" or a model is missing from the list."),
 hd=('Control', 'Range', 'What it does'), hd2=('Gesture', 'What it does'), hd3=('Field', 'What it does'), hd4=('Folder / file', 'Content'),
 S=[
  ('1. Overview', [
   "<b>RMampsim</b> plays <b>NAM amp models</b> (Neural Amp Modeler): a neural network trained to reproduce a real amp or an amp plug-in "
   "at given settings. RMampsim reads the recent <b>A2</b> format, natively in JSFX and with <b>zero latency</b>, then runs the sound "
   "through a <b>cabinet IR</b>.",
   "IMAGE_FACE",
   "Signal chain: input (L+R)/2 → INPUT and IN CAL → NAM A2 model → normalisation → EQ (BASS, MID, TREBLE, PRESENCE) → cabinet (IR) "
   "and MIC → LEVEL → safety clipper at 0 dBFS. The output is the same on both channels.",
   "RMampsim comes with <b>17 A2 models</b> (7 heads, 10 full rigs) and <b>10 cabinet IRs</b>, all made by ReNo Mellow. "
   "A new instance loads <b>Hot Plexi Head</b> and the <b>British Vintage 4x12</b> cabinet.",
  ]),
  ('2. Installation', [
   "RMampsim needs the <b>IR Buddy</b> script package (shared with RM1982Verb): it converts the models and prepares your captures. "
   "Install both:",
   "BUL:<b>ReaPack</b>: ReNo Mellow repository (<i>%s</i>), <b>Amp</b> category → <b>RMampsim</b>, and <b>Scripts</b> category → "
   "<b>ReNo Mellow - IR Buddy</b>." % REPO,
   "BUL:<b>Without ReaPack</b>: drag <b>RMampsim.ReaperPkg</b>, then <b>IR Buddy.ReaperPkg</b>, into the REAPER window (7.86+).",
   "Then run the <b>ReNo Mellow - IR Buddy - Rescan RM IR</b> action once (Actions &gt; Show action list).",
   "CALLOUT",
   "Installed: the plug-in (FX browser, search \"RMampsim\"), the following files, and the IR Buddy actions.",
   "TABLE4",
   "<b>Sample rate</b>: NAM models are made for <b>48 kHz</b>. At another rate the plug-in works, but the tone drifts a little from the "
   "original: set the project to 48 kHz (Project settings) for the exact tone.",
  ]),
  ('3. Pick a model and a cabinet', [
   "BUL:<b>Click the model name</b>: the <b>browser</b> opens (folders on the left, models on the right; wheel to scroll, click to load). "
   "It stays open so you can compare; × or another click on the name closes it.",
   "IMAGE_BROWSER",
   "BUL:<b>&lt; &gt; arrows</b>: previous / next model of the same folder.",
   "BUL:<b>LITE / FULL</b>: an A2 file holds two sizes of the same model. LITE is light on the CPU; FULL is a little more accurate but "
   "several times heavier. Start with LITE, switch to FULL for the final mix if your computer keeps up.",
   "BUL:<b>AMP</b> off: the model is bypassed and RMampsim becomes a plain <b>cabinet IR loader</b> (for an amp simulated elsewhere, or a "
   "DI recorded through a real preamp).",
   "BUL:<b>Cabinet</b>: same idea, click the IR name under CABINET (only REAPER/Data/RM IR/Cab is listed), or <b>drop a .wav file</b> "
   "anywhere on the window. <b>CAB</b> switches the cabinet on / off.",
   "<b>Heads and full rigs.</b> A \"<b>Head</b>\" model is the amp alone: it needs a cabinet. A \"<b>Full Rig</b>\" (or \"Amp + Cab\") model "
   "already holds the cabinet and the mic: when you pick one, RMampsim <b>switches CAB off automatically</b> and the header shows "
   "\"full rig (cab in model)\". Back to a head, CAB comes back on. You can always force CAB by hand.",
  ]),
  ('4. Controls', ['TABLE']),
  ('5. Add your own NAM models', [
   "Add as many models as you like: your own (see section 6) or community models.",
   "BUL:<b>Find A2 models</b>: on <b>tone3000.com</b>, each tone page lists its <b>A2-Full / A2-Lite</b> models. Only <b>A2</b> models are "
   "read; older A1 models (\"Standard\", \"Lite\", \"Feather\", \"Nano\") are skipped and listed by the Rescan.",
   "BUL:<b>Store them</b>: copy the <b>.nam</b> files into <b>REAPER/Data/RM Amp</b>. Sub-folders are allowed and become the browser "
   "folders (for instance RM Amp/My captures/Crunch). The <b>ReNo Mellow - IR Buddy - Open RM Amp folder</b> action opens that folder.",
   "BUL:<b>Convert them</b>: run <b>Rescan RM IR</b>. Each .nam is converted once (later rescans are faster) and a message tells how many "
   "models are ready and which ones were skipped.",
   "BUL:<b>Full rig</b>: RMampsim recognises a model with a cabinet from the gear type stored in the file (TONE3000 \"Amp + Cab\") or "
   "from its name or folder: \"Full Rig\", \"Amp + Cab\", \"Amp Cab\", \"Combo\". If a full rig is not recognised, add \"Full Rig\" to "
   "the file name and rescan.",
   "BUL:<b>IN CAL</b>: some models store the input level of the capture (dBu); the MODEL area then shows \"captured at +xx dBu\". Set IN CAL "
   "to the level of your interface for 0 dBFS (spec sheet of your instrument input): your guitar hits the model like the real amp. "
   "Without that information, IN CAL is greyed out (\"not used by this model\").",
   "Downloaded models belong to their authors: keep them for your own use, don't redistribute them without their consent.",
  ]),
  ('6. Capture your own amp (Capture for NAM)', [
   "The <b>ReNo Mellow - IR Buddy - Capture for NAM</b> action runs the <b>official NAM capture signal</b> (\"T3K sweep v3\", 3 min 10 s, "
   "provided in REAPER/Data/RM Amp/Capture signal) through your amp plug-in and records the output. Training then happens for free on "
   "<b>TONE3000</b>, which gives you back an A2 .nam file.",
   "<b>a. Prepare</b>",
   "BUL:Project at <b>48 kHz</b>.",
   "BUL:On a track: your amp plug-in set the way you want to capture it, <b>no noise gate</b>.",
   "BUL:<b>Amp only</b> (\"Head\"): switch the plug-in's cabinet / IR off. <b>Full rig</b>: leave it on (a regular cabinet IR, not a long room reverb).",
   "BUL:Select the track.",
   "<b>b. Run the action</b>: a dialog asks for three settings, remembered for next time.",
   "TABLE3",
   "The file <b>\"name - output.wav\"</b> (24-bit mono WAV, exactly the length of the signal) is written to "
   "<b>REAPER/Data/RM Amp/Captures (to train)</b>. If the amp goes above 0 dBFS its level is lowered and the message says so: "
   "this does no harm to NAM.",
   "<b>c. Train on TONE3000</b>",
   "BUL:On <b>tone3000.com</b>, create a capture (free account), signal <b>\"T3K sweep v3\"</b>, type <b>Amp Head</b> (amp only) or "
   "<b>Amp + Cab</b> (full rig).",
   "BUL:Upload the \"… - output.wav\" file as the <b>output</b>. You don't need to upload the input signal.",
   "BUL:<b>Advanced</b>: Max Epochs <b>400 – Max</b> for the best accuracy (takes longer). <b>Calibration</b> (Send / Return Level): leave "
   "<b>empty</b> for a plug-in; for a real amp, enter your interface levels (dBu for 0 dBFS): IN CAL can then use them.",
   "BUL:During training the <b>ESR</b> (error between the model and the original) goes down: below 0.01 the difference is barely audible.",
   "<b>d. Use the model</b>: download the .nam (A2) into <b>REAPER/Data/RM Amp</b>, keep \"Full Rig\" in its name if it is one, run "
   "<b>Rescan RM IR</b>: the model shows up in the RMampsim browser.",
   "<b>A real amp?</b> Insert the <b>ReaInsert</b> plug-in on the track (output to the amp input through a re-amp box, return from the "
   "mic or line out), set its latency, and answer <b>Y</b> to \"Real time\". The signal plays at full scale: set your monitoring level first.",
  ]),
  ('7. Your own cabinets', [
   "Copy your cabinet IRs (.wav, mono or stereo, up to 10 s, automatic resampling) into <b>REAPER/Data/RM IR/Cab</b> (sub-folders allowed), "
   "then run <b>Rescan RM IR</b>. For a quick try, just drop the file on RMampsim.",
   "To capture the cabinet of a simulation plug-in: run <b>ReNo Mellow - IR Buddy</b> on the track of the cabinet plug-in alone, "
   "sub-folder <b>Cab</b>, output <b>M</b> (mono). <b>MIC</b> then moves the virtual mic from the center (bright) to the edge (darker).",
  ]),
  ('8. Mouse and keyboard', ['TABLE2']),
  ('9. FAQ', [
   "QA:\"NO MODEL - click to browse\" or an empty list|The index does not exist yet: run <b>Rescan RM IR</b> (IR Buddy must be installed), "
   "then open the browser again. The default model loads on a new instance.",
   "QA:My model does not show up|It is an A1 model (the Rescan lists it as skipped), or the Rescan was not run after copying it.",
   "QA:It distorts / it is too loud|Lower INPUT or LEVEL. Models are normalised from their loudness; a very hot guitar can come out louder. "
   "A safety clipper limits the output at 0 dBFS.",
   "QA:The CPU load is high|Switch to <b>LITE</b>. Use FULL for the render, or freeze the track.",
   "QA:It sounds different from the original|Check the project is at 48 kHz, the normalisation (LEVEL), the cabinet (a full rig does not "
   "need one) and, for a calibrated amp, IN CAL.",
   "QA:The cabinet browser only shows \"Cab\"|That is on purpose: only the IRs of REAPER/Data/RM IR/Cab are offered, not the RM1982Verb "
   "reverb IRs.",
  ]),
 ],
 rows=[('AMP', 'ON / OFF', 'Switches the model on. OFF = cabinet IR loader only.'),
       ('Model', 'browser, &lt; &gt;', 'NAM A2 model (section 3).'),
       ('LITE / FULL', '', 'Model size: light or more accurate.'),
       ('INPUT', '-24 – +24 dB', 'Gain before the model: more drive to the right.'),
       ('BASS / MID / TREBLE', '±12 dB', 'EQ after the amp: 120 Hz shelf, 750 Hz bell, 2.8 kHz shelf.'),
       ('PRESENCE', '±12 dB', '5.5 kHz bell: bite and sparkle.'),
       ('LEVEL', '-24 – +12 dB', 'Output level. Models are normalised (-24 dB average loudness).'),
       ('CAB', 'ON / OFF', 'Switches the cabinet on. Switched off automatically for a full rig.'),
       ('Cabinet', 'browser, &lt; &gt;', 'IR from REAPER/Data/RM IR/Cab, or a .wav dropped on the window.'),
       ('MIC', '0 – 100 %', 'Mic position: center (0, bright) to edge (100, darker).'),
       ('IN CAL', 'OFF, 0 – 30 dBu', 'Level of your interface for 0 dBFS. Used when the model stores its capture level.'),
       ('IN / OUT meters', '', 'Input and output levels (dBFS).')],
 rows2=[('Drag a knob (vertical)', 'Adjust; Shift = fine; mouse wheel too.'),
        ('Ctrl-click (Cmd-click) a knob', 'Default value.'),
        ('Click a value / double-click a knob', 'Type it: 3, -6, off; Enter = OK, Esc = cancel.'),
        ('Click the model / cabinet name', 'Opens / closes the browser.'),
        ('Drop a .wav on the window', 'Loads that file as the cabinet.'),
        ('Double-click "RMampsim"', 'Green / orange colour.'),
        ('SIZE buttons', 'Window size: 75 to 200 %.')],
 rows3=[('Capture name', 'File name. Suggested: the name of the first active FX. With Cab = Y, "Full Rig" is added to the name.'),
        ('Cab in capture (Y / N)', 'N = amp only (plug-in cabinet off). Y = full rig (cabinet included).'),
        ('Real time (Y / N)', 'N = offline render, a few seconds. Y = real time (about 3 min 15 s, the transport records), for plug-ins '
         'running on external DSP (UAD...) or a real amp through ReaInsert. If the offline render is silent, the action offers to capture again in real time.')],
 rows4=[('REAPER/Data/RM Amp/ReNo Mellow', 'The 17 factory models (Heads, Full Rigs). Your own models go in REAPER/Data/RM Amp.'),
        ('REAPER/Data/RM IR/Cab', 'The 10 factory cabinet IRs; your cabinet IRs go here.'),
        ('REAPER/Data/RM Amp/Capture signal', 'T3K-sweep-v3.wav, the NAM capture signal (used by Capture for NAM).'),
        ('REAPER/Data/RMIRIndex', 'Index and converted models written by the Rescan (do not edit).')],
)

st_body = ParagraphStyle('b', fontName='DV', fontSize=8.8, leading=12, spaceAfter=3, textColor=DARK)
st_h = ParagraphStyle('h', fontName='DVB', fontSize=13, leading=17, spaceBefore=8, spaceAfter=4, textColor=TEAL, keepWithNext=1)
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

def callout(L, W):
    t = Table([[Paragraph(L['call'][0], ParagraphStyle('ct', fontName='DVB', fontSize=10.5, leading=14, textColor=DARK))],
               [Paragraph(L['call'][1], ParagraphStyle('cbx', fontName='DV', fontSize=9, leading=12.5, textColor=DARK))]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dff7f3')), ('BOX', (0, 0), (-1, -1), 2, TEAL),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    return [Spacer(1, 3), t, Spacer(1, 6)]

def build(L):
    def deco(c, d):
        c.saveState(); c.setFillColor(ACC); c.rect(0, A4[1] - 6*mm, A4[0], 6*mm, fill=1, stroke=0)
        c.setFont('DV', 8); c.setFillColor(GREY); c.drawString(18*mm, 10*mm, L['foot'])
        c.drawRightString(A4[0] - 18*mm, 10*mm, str(d.page)); c.restoreState()
    doc = BaseDocTemplate(os.path.join(HERE, L['file']), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm,
                          bottomMargin=16*mm, title='RMampsim', author='ReNo Mellow')
    W = A4[0] - 36*mm
    doc.addPageTemplates([PageTemplate(frames=[Frame(18*mm, 16*mm, W, A4[1] - 31*mm, id='f')], onPage=deco)])
    s = [Paragraph('ReNo Mellow', ParagraphStyle('k', fontName='DVB', fontSize=10, textColor=GREY)),
         Paragraph('RMampsim', ParagraphStyle('t', fontName='DVB', fontSize=24, leading=28, textColor=DARK)),
         Paragraph(L['sub'], ParagraphStyle('s', fontName='DV', fontSize=12, leading=16, textColor=GREY, spaceAfter=4)),
         Paragraph('Version %s &nbsp;·&nbsp; <link href="%s" color="#2a9d8f">%s</link>' % (VERSION, L['other'][1], L['other'][0]),
                   ParagraphStyle('v', fontName='DV', fontSize=9, textColor=GREY, spaceAfter=6))]
    for title, paras in L['S']:
        s.append(Paragraph(title, st_h if paras[0] != 'TABLE' else ParagraphStyle('h2', parent=st_h, keepWithNext=0)))
        for p in paras:
            if p == 'IMAGE_FACE':
                s.append(Image(IMG_FACE, width=W*0.85, height=W*0.85*470/1060)); s.append(Paragraph(L['cap_face'], st_cap))
            elif p == 'IMAGE_BROWSER':
                s.append(Image(IMG_BROWSER, width=W*0.7, height=W*0.7*470/1060)); s.append(Paragraph(L['cap_browser'], st_cap))
            elif p == 'CALLOUT': s.extend(callout(L, W))
            elif p == 'TABLE': s.append(tbl(L['hd'], L['rows'], [36*mm, 30*mm, W - 66*mm])); s.append(Spacer(1, 4))
            elif p == 'TABLE2': s.append(tbl(L['hd2'], L['rows2'], [62*mm, W - 62*mm])); s.append(Spacer(1, 4))
            elif p == 'TABLE3': s.append(tbl(L['hd3'], L['rows3'], [44*mm, W - 44*mm])); s.append(Spacer(1, 4))
            elif p == 'TABLE4': s.append(tbl(L['hd4'], L['rows4'], [58*mm, W - 58*mm])); s.append(Spacer(1, 4))
            elif p.startswith('BUL:'): s.append(Paragraph(p[4:], st_bul, bulletText='•'))
            elif p.startswith('QA:'):
                q, a = p[3:].split('|', 1); s.append(Paragraph(q, st_q)); s.append(Paragraph(a, st_body))
            elif p.startswith('<b>') and p.endswith('</b>'):
                s.append(Paragraph(p, ParagraphStyle('sub3', parent=st_body, fontName='DVB', fontSize=9.5, spaceBefore=4, keepWithNext=1)))
            else: s.append(Paragraph(p, st_body))
    doc.build(s)

if __name__ == '__main__':
    for L in (FR, EN): build(L)
