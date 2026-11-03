# Changelog / Journal des versions

Newest version first. Each version is in English, then in French.
La version la plus récente en premier. Chaque version est en anglais, puis en français.

## 1.32.0

### English

**The desperation moves under the name, and the wins of two humans** (test 1, The King of Fighters '98, Seb's mockups)
- Under the name of each human player, a panel, as in the mockup Seb chose. A badge says the stocks (1 STOCK, 2 STOCKS), EXTRA, or MAX in gold. The power gauge is drawn as the game draws it, the bar and a green square per stock, 3 squares for the first fighter of a team and one more for each teammate beaten.
- When the gauge allows a desperation move (a stock or MAX in Advanced, the full gauge or the health in the red in Extra), the commands of the fighter's ones show in the panel, their arrows facing the other fighter (player 2 on the right faces left). The arrows light up as the stick does them. When a button ends an attempt that missed a step or so, the steps missed are crossed in red and RATÉ shows. DM ! shows once the game took its stock (its full gauge in Extra), SDM ! in MAX (A+B+C took a stock before), and the row stays lit while it shows. A special move (236 and a punch) gives no RATÉ, and neither does a stock taken by a guard cancel. A command done in full that the game did not take stays lit a moment, without a word, and goes to the log (to find the stocks if their address is not the right one).
- The buttons are drawn in the colours of the Neo Geo (A red, B yellow, C green, D blue) with the names of the game file (`"buttons"`, LP LK HP HK).
- The team moves to the name's line, small, the beaten ones struck.
- When two humans play a game of teams, a VICTOIRES pill under the credits counts the matches each one won, P1 on the left and P2 on the right. One more comes when VICTOIRE shows. ArcadeDMD counts them itself, and puts them back to 0 once one of the two left 20 s ago. Against the computer it does not show.
- New values in The King of Fighters '98, all to confirm in game, their changes written in the log. The stick and buttons of each player (BIOS_P1CURRENT 0x10FD96 and BIOS_P2CURRENT 0x10FD9C, read the other way round if up and down show together), the power gauge (0x1081E8, RetroAchievements code notes, 0xA0 full), the stocks (0x1082E3, the MAME cheat Infinite Power), the mode Advanced or Extra (0x10A84C, next to the team), a byte that may be the MAX timer (0x1081EA), and player 2's in his own block.
- The commands of the 84 desperation moves of the 38 fighters, 3 at most each (`"moves"` in the game file, numpad notation for a fighter facing right, P for a punch and K for a kick). They come from the MAME command.dat (Progetto-SNAPS, the entry of the original game), checked against the Korean Enha wiki. A shorter form of a command that the game takes too still gives DM ! when the game took its stock.

**The inputs pressed, and Extra's MAX** (test 3, Seb's first fights)
- When no desperation move can come out, the panel shows the inputs pressed, as training mode does. Each direction the stick takes and the buttons pressed with it, the newest on the right and lit, the older ones fading, all gone 3 s after the last one. The commands of the desperation moves take their place as soon as one can come out.
- In Extra, the gauge full is MAX until its bar is empty or a desperation move takes it at once. The commands showed only while the gauge was exactly full, and went away as soon as the bar of MAX began to drain. DM ! (SDM ! with the health in the red) when the gauge falls at once. The gauge full, empty, or taken at once go to the log.

**When a super can come out in Extra** (test 4, Seb never plays Extra)
- The badge says why a desperation move can come out. MAX in gold, VIE ROUGE in red when the life is nearly empty (a quarter of the bar, to confirm in game, the game raises it for a team that lost a fighter), MAX + VIE ROUGE for an SDM. The panel's edge takes the same colour.
- While none can come out in Extra, the bar is longer, with how full it is (62 %) and the rule beside it, SUPER À 100 %.

**The stage darker under the fights** (test 5, Seb)
- The backdrop of the fighting games is darker, 50 % instead of 30 %, the names, health bars and buttons stood out too little over it. `"dim_fight"` in the `preview` section sets it, from 0 to 80, the other scenes keep `"dim"`.

**ROUND 1 once, at the fight** (test 6, Seb's video of The King of Fighters '98)
- Between the select screens and the fight the game shows other screens, HOW TO PLAY, THE NEXT COMPETITOR, the order select, BATTLE IN CHINA. Only the character select and the order select were told, and each of the others started a fight on the HD screen, ROUND 1 with the sweep of the stage changing, then the last match's timer. Every screen but the fight's (0xE8BE, RetroAchievements code notes) is now a select screen, VS in the middle and no event of a fight, and ROUND 1 comes once, when the fight's screen appears. The sweep of the next stage comes on BATTLE IN, where the game shows it.
- A screen, of the select or of the fight, counts once it lasted 0.4 s. A screen of a moment neither starts nor ends a fight.
- VS no longer shows for a moment just after FIGHT !, the timer having stood still for 6 s during the entrances of the fighters. FIGHT ! counts as the timer moving.
- The last match's timer (44) no longer shows at the start of the next one, until the game sets its own or GO comes.
- The winner of the match (VICTOIRE, the team eliminated) stays its 5.5 s over the screen of his quotes, which now is a select screen.

**MAX over in Advanced** (test 7, Seb's photo, MAX lit while the game was out of it)
- The game neither fills its gauge nor gives a stock during MAX. A stock gained, or the gauge filling again, now ends MAX on the HD screen. It could stay lit up to 15 s after the game's.
- A+B+C, the start of MAX with the gauge, and MAX once a second go to the log, to set its end on a cabinet.

**ROUND and FIGHT ! when the game shows them** (test 8, Seb's second video, all of it late in test 7)
- The fight's screen (0xE8BE) only comes once GO is over, not during the entrances of the fighters. Test 6 waited for it, ROUND n came at GO and FIGHT ! 1.5 s after. ROUND n now comes when the game starts its round (the state of the fight at 0x01, RetroAchievements code notes of '97), at once, and FIGHT ! 1.15 s after READY (0x18), as before test 6.
- The select screens are the character select, the order select, and any screen where the game has no fight going (its state at 0). HOW TO PLAY, THE NEXT COMPETITOR and BATTLE IN still start nothing. A state at 0 for less than 0.4 s between two rounds ends nothing, and the round starting ends the select screen at once.
- The next fighter's band (ENTRE EN SCÈNE) comes 1.4 s after ROUND n, when the game shows him, no longer just after the K.O. The beaten one's name stays until then.
- The changes of the state of the fight still go to the log (`Combat, état 0x..`), to check them on a cabinet.

**MAX as the game says it** (test 8, Seb's photo and video, MAX lit with no stock)
- The badge says MAX when every square of the gauge is lit, as the game does. MAX ACTIVÉ is the MAX of A+B+C, in gold.
- MAX ACTIVÉ now waits for the byte of MAX (0x1081EA) to move within 0.6 s of A+B+C taking a stock. A stock taken by a desperation move just after A+B+C pressed by chance lit MAX. If the byte does not move, the log says `pas de MAX`, and the commands keep the stocks left.

**No shop signs under the fights** (test 8, Seb)
- The shop signs of the city backdrop that lit up at the level of the names (the white rectangles) no longer show under the fights and select screens. The other scenes keep them.

**Read at every frame**
- A value marked `"fast"` is read at every frame, the stick and buttons here. The MAME plugin reads it at each frame. The RetroArch reader asks for it at each frame between its other reads, and asks for all those at once (RetroArch answers them at the same frame, one block of memory at a time took a frame each). Each change of the stick and buttons keeps the time it was read.
- When RetroArch closes during a game whose stick is read, the HD screen leaves the game as fast as before (test 2). The values asked together were asked again one by one when no answer came, 3 s or more each time.

**Version**
- 1.32.0 in `dmd/app.py` and the MAME plugin.

### Français

**Les coups désespérés sous le nom, et les victoires de deux humains** (test 1, The King of Fighters '98, les maquettes de Seb)
- Sous le nom de chaque joueur humain, un panneau, comme sur la maquette que Seb a choisie. Une pastille dit les stocks (1 STOCK, 2 STOCKS), EXTRA, ou MAX en doré. La jauge est dessinée comme dans le jeu, la barre et un carré vert par stock, 3 carrés pour le premier combattant d'une équipe et un de plus pour chaque équipier battu.
- Quand la jauge permet un coup désespéré (un stock ou le MAX en Advanced, la jauge pleine ou la vie dans le rouge en Extra), les commandes de ceux du combattant s'affichent dans le panneau, leurs flèches tournées vers l'autre combattant (le joueur 2 à droite regarde à gauche). Les flèches s'allument quand le stick les fait. Quand un bouton finit une tentative à qui il manque une étape ou deux, les étapes manquées sont barrées en rouge et RATÉ s'affiche. DM ! s'affiche quand le jeu a pris son stock (sa jauge pleine en Extra), SDM ! en MAX (A+B+C a pris un stock avant), et la ligne reste allumée pendant ce temps. Un coup spécial (236 et un poing) ne donne pas de RATÉ, un stock pris par une garde annulée non plus. Une commande faite en entier que le jeu n'a pas prise reste allumée un moment, sans mot, et va dans le journal (pour trouver les stocks si leur adresse n'est pas la bonne).
- Les boutons ont les couleurs de la Neo Geo (A rouge, B jaune, C vert, D bleu) et les noms du fichier du jeu (`"buttons"`, LP LK HP HK).
- L'équipe monte sur la ligne du nom, en petit, les battus barrés.
- Quand deux humains jouent à un jeu d'équipes, une pastille VICTOIRES sous les crédits compte les matchs gagnés par chacun, P1 à gauche et P2 à droite. Il en vient un de plus quand VICTOIRE s'affiche. ArcadeDMD les compte lui-même, et les remet à 0 quand l'un des deux est parti depuis 20 s. Contre l'ordinateur elle ne s'affiche pas.
- De nouvelles valeurs dans The King of Fighters '98, toutes à confirmer en jeu, leurs changements écrits dans le journal. Le stick et les boutons de chaque joueur (BIOS_P1CURRENT 0x10FD96 et BIOS_P2CURRENT 0x10FD9C, lus à l'envers si haut et bas viennent ensemble), la jauge (0x1081E8, notes de code de RetroAchievements, 0xA0 pleine), les stocks (0x1082E3, le code MAME Infinite Power), le mode Advanced ou Extra (0x10A84C, à côté de l'équipe), un octet qui pourrait être le chrono du MAX (0x1081EA), et ceux du joueur 2 dans son propre bloc.
- Les commandes des 84 coups désespérés des 38 combattants, 3 au plus chacun (`"moves"` dans le fichier du jeu, en notation du pavé numérique pour un combattant tourné vers la droite, P pour un poing et K pour un pied). Elles viennent du command.dat de MAME (Progetto-SNAPS, l'entrée du jeu d'origine), vérifiées avec le wiki coréen Enha. Une forme plus courte d'une commande que le jeu prend aussi donne quand même DM ! quand le jeu a pris son stock.

**Les touches appuyées, et le MAX d'Extra** (test 3, les premiers combats de Seb)
- Quand aucun coup désespéré ne peut sortir, le panneau montre les touches appuyées, comme le mode entraînement. Chaque direction du stick et les boutons appuyés avec, la plus récente à droite et éclairée, les plus anciennes plus pâles, le tout parti 3 s après la dernière. Les commandes des coups désespérés prennent leur place dès que l'un d'eux peut sortir.
- En Extra, la jauge pleine est le MAX jusqu'à ce que sa barre soit vide ou qu'un coup désespéré la prenne d'un coup. Les commandes ne s'affichaient que tant que la jauge était pile pleine, et partaient dès que la barre du MAX commençait à se vider. DM ! (SDM ! avec la vie dans le rouge) quand la jauge tombe d'un coup. La jauge pleine, vide, ou prise d'un coup vont dans le journal.

**Quand un super peut sortir en Extra** (test 4, Seb ne joue jamais en Extra)
- La pastille dit pourquoi un coup désespéré peut sortir. MAX en doré, VIE ROUGE en rouge quand la vie est presque vide (un quart de la barre, à confirmer en jeu, le jeu le monte pour une équipe qui a perdu un combattant), MAX + VIE ROUGE pour un SDM. Le bord du panneau prend la même couleur.
- Tant qu'aucun ne peut sortir en Extra, la barre est plus longue, avec son remplissage (62 %) et la règle à côté, SUPER À 100 %.

**Le décor plus sombre sous les combats** (test 5, Seb)
- Le décor des jeux de combat est plus sombre, 50 % au lieu de 30 %, les noms, barres de vie et boutons ne ressortaient pas assez dessus. `"dim_fight"` dans la section `preview` le règle, de 0 à 80, les autres scènes gardent `"dim"`.

**ROUND 1 une seule fois, au combat** (test 6, la vidéo de Seb sur The King of Fighters '98)
- Entre les écrans de sélection et le combat, le jeu montre d'autres écrans, HOW TO PLAY, THE NEXT COMPETITOR, la sélection de l'ordre, BATTLE IN CHINA. Seules la sélection des personnages et celle de l'ordre étaient dites, et chacun des autres lançait un combat sur l'écran HD, ROUND 1 avec le balayage du décor qui change, puis le chrono du match d'avant. Tout écran autre que celui du combat (0xE8BE, notes de code de RetroAchievements) est maintenant un écran de sélection, VS au milieu et aucun événement de combat, et ROUND 1 vient une fois, quand l'écran du combat apparaît. Le balayage du décor suivant vient sur BATTLE IN, là où le jeu le montre.
- Un écran, de sélection ou de combat, compte une fois qu'il a duré 0,4 s. Un écran d'un instant ne lance ni ne finit un combat.
- VS ne s'affiche plus un instant juste après FIGHT !, le chrono étant immobile depuis 6 s pendant l'entrée des combattants. FIGHT ! compte comme un chrono qui bouge.
- Le chrono du match d'avant (44) ne s'affiche plus au début du suivant, tant que le jeu n'a pas mis le sien ou que GO n'est pas venu.
- Le vainqueur du match (VICTOIRE, l'équipe éliminée) reste ses 5,5 s par-dessus l'écran de ses répliques, qui est maintenant un écran de sélection.

**La fin du MAX en Advanced** (test 7, la photo de Seb, MAX allumé alors que le jeu n'y était plus)
- Le jeu ne remplit pas sa jauge et ne donne pas de stock pendant le MAX. Un stock gagné, ou la jauge qui se remplit à nouveau, finit maintenant le MAX sur l'écran HD. Il pouvait rester allumé jusqu'à 15 s après celui du jeu.
- A+B+C, le début du MAX avec la jauge, et le MAX une fois par seconde vont dans le journal, pour régler sa fin sur une borne.

**ROUND et FIGHT ! quand le jeu les montre** (test 8, la deuxième vidéo de Seb, tout était en retard dans le test 7)
- L'écran du combat (0xE8BE) ne vient qu'une fois GO fini, pas pendant l'entrée des combattants. Le test 6 l'attendait, ROUND n venait à GO et FIGHT ! 1,5 s après. ROUND n vient maintenant quand le jeu commence son round (l'état du combat à 0x01, notes de code de RetroAchievements de '97), tout de suite, et FIGHT ! 1,15 s après READY (0x18), comme avant le test 6.
- Les écrans de sélection sont la sélection des personnages, celle de l'ordre, et tout écran où le jeu n'a pas de combat en cours (son état à 0). HOW TO PLAY, THE NEXT COMPETITOR et BATTLE IN ne lancent toujours rien. Un état à 0 pendant moins de 0,4 s entre deux rounds ne finit rien, et le round qui commence finit l'écran de sélection tout de suite.
- Le bandeau du combattant suivant (ENTRE EN SCÈNE) vient 1,4 s après ROUND n, quand le jeu le montre, et plus juste après le K.O. Le nom du battu reste jusque-là.
- Les changements d'état du combat vont toujours dans le journal (`Combat, état 0x..`), pour les vérifier sur une borne.

**Le MAX comme le dit le jeu** (test 8, la photo et la vidéo de Seb, MAX allumé sans stock)
- La pastille dit MAX quand tous les carrés de la jauge sont allumés, comme le jeu. MAX ACTIVÉ est le MAX de A+B+C, en doré.
- MAX ACTIVÉ attend maintenant que l'octet du MAX (0x1081EA) bouge dans les 0,6 s après que A+B+C a pris un stock. Un stock pris par un coup désespéré juste après un A+B+C appuyé par hasard allumait le MAX. Si l'octet ne bouge pas, le journal dit `pas de MAX`, et les commandes suivent les stocks qui restent.

**Plus d'enseignes sous les combats** (test 8, Seb)
- Les enseignes du décor de la ville qui s'allumaient à hauteur des noms (les rectangles blancs) ne s'affichent plus sous les combats et les écrans de sélection. Les autres scènes les gardent.

**Lu à chaque image**
- Une valeur marquée `"fast"` est lue à chaque image, ici le stick et les boutons. Le plugin MAME la lit à chaque image. La lecture RetroArch la demande à chaque image entre ses autres lectures, et demande alors toutes celles-ci d'un coup (RetroArch y répond à la même image, un bloc de mémoire à la fois prenait une image chacun). Chaque changement du stick et des boutons garde le moment où il a été lu.
- Quand RetroArch se ferme pendant un jeu dont le stick est lu, l'écran HD sort du jeu aussi vite qu'avant (test 2). Les valeurs demandées ensemble étaient redemandées une par une faute de réponse, 3 s ou plus à chaque fois.

**Version**
- 1.32.0 dans `dmd/app.py` et le plugin MAME.

## 1.31.1

### English

**The K.O. of the fighting games**

An audit of every game file with a health bar, 115 games, after The King of Fighters '98 showed no K.O. on Seb's cabinet. RetroAchievements' code notes (downloaded with `tools/ra_notes.py`) and the cheat databases of FinalBurn Neo and MAME were read game by game. Everything below is still to be confirmed in game.
- A health bar that goes below zero at a K.O. reads empty, not full. In many SNK games the health is a word that a K.O. takes below zero, its byte read 0xFF (the notes say ff = K.O. in Real Bout Fatal Fury 2, SNK vs. Capcom, World Heroes Perfect and 2 Jet, 0xFB in King of the Monsters), which reads far above full and showed a full bar, so no K.O., no WIN and no round was ever seen. 40 Neo Geo fighting games get the rule the Capcom games already had (`"zero_from"`, halfway between full and the top of the byte or word): Art of Fighting 1 to 3, Aggressors of Dark Kombat, Breakers and Breakers Revenge, Fatal Fury 1 to 3 and Special, Fight Fever, Garou, Voltage Fighter Gowcaizer, Kabuki Klash, Kizuna Encounter, King of Fighters '94 and '95, King of the Monsters 1 and 2, The Last Blade 1 and 2, Legend of Success Joe, Matrimelee, Ninja Master's, Real Bout Fatal Fury 1, 2 and Special, Samurai Shodown 1 to 5 and 5 Special, Sengoku 3, SNK vs. Capcom, World Heroes 1, 2, 2 Jet and Perfect. The shared scene of the Neo Geo fighting games keeps the same values for their sets.
- Rage of the Dragons and Ragnagard read their health as a signed 16-bit word, below zero is empty there (their notes and cheats write it as a word).
- Six games are left as they are, their full health being 0xFF or a counter of the damage (Galaxy Fight, Karnov's Revenge, Waku Waku 7, Double Dragon, and the Capcom wrestling games whose cheat fills the bar with 0xFF).
- The computer's health where the game keeps it. Fatal Fury, King of the Monsters and Legend of Success Joe keep the computer's fighter in a block of its own, player 2's block only moves when a human plays there. Against the computer the right bar never moved. It now shows the computer's (`_cpu_hp`), player 2's when he plays (a `"tag"` on `p2_mode`).
- Rounds won read in 13 more games, gold stars under the bars and the winner of each round: Samurai Shodown III, IV, V and V Special, SNK vs. Capcom, Garou, Real Bout Fatal Fury 1, 2 and Special, Art of Fighting 1 and 2, Kabuki Klash.
- The round of the match, ROUND n in big letters when a fight begins as in The King of Fighters: Fatal Fury 2 and Special, Real Bout Fatal Fury Special, World Heroes 2 Jet and Perfect (`round`, from 1 in these games, `"add": -1`).
- The select screens the game tells (The King of Fighters '94, '96, '98, '99 and 2002, Real Bout Fatal Fury Special, a value `select`). There the HD screen shows VS and no event of a fight, the bars the game fills or empties for the next match give neither K.O. nor ROUND, and the fight begins with its ROUND as the screen ends. The panels show VS too.
- RetroAchievements' notes number the bytes of the Neo Geo's RAM in the other order of each pair, the 68000's byte is the next one (0x8238 in the notes is 0x108239). Every value taken from them follows that rule, checked on the King of Fighters' values learned on a cabinet.

**FIGHT ! with the game's GO, and the fighters a team has lost** (test 2, Seb's video of The King of Fighters '98)
- FIGHT ! comes with the game's own FIGHT or GO, when the round's timer starts counting down. Its fraction of a second (`_time_sub`, RetroAchievements code notes, read in The King of Fighters '96, '97, '98 and 2003, Real Bout Fatal Fury and Special, Fatal Fury 1, 2 and Special, Samurai Shodown III, IV and V Special) moves at every frame once it runs, other games wait for their first second counted down. FIGHT ! came 1.35 s after ROUND, with the names of the fighters, 5 s before READY and GO. A timer set to infinite gives it 20 s after the bars filled (12 s without the fraction, the entrances of the fighters before a first round wait for GO too), a game that reads no timer shows it at once as before. The shock wave of FIGHT ! comes with it.
- While a round waits for its GO, the HD screen keeps its timer. VS showed during READY and GO, the timer having stood still for 6 s.
- The King of Fighters counts a K.O. a moment before the bar of the beaten fighter reads empty. A team out is now told by the fighters it had lost when the fight began (GO). The count read with the bar still up already had this K.O., and a team was eliminated after its second fighter (CPU WINS, P1 TEAM ELIMINATED in the middle of a match).
- For the same reason the band of the next fighter came before the K.O. and over it, and his name and his team replaced the beaten fighter's at once. Both wait for the K.O. and the WIN now, 3 s at most (a round lost on time).
- The last fighter of a team lost on time ends the match too, TIME UP, the WIN, then the winner in big letters.
- Samurai Shodown V Special read the frames of its timer's second as its timer. It reads its seconds (BCD at 0x10836A, RetroAchievements code notes).

**A fighter at 0 still stands, the end of a match, FIGHT ! with GO** (test 3, Seb's second match of The King of Fighters '98)
- In The King of Fighters '96 to 2002 a fighter at 0 still fights, only a bar below zero is a K.O. (RetroAchievements code notes of '98, 0x0000 = lowest possible health while alive, underflows when dead). 0 reads 1 (`"add": 1`). It gave a K.O. and the WIN in the middle of a fight (Andy at 0 after a blow blocked), and a fighter at 0 made the K.O. of the other one look like the end of a round already over, so the match was not ended.
- The end of a match stays 5.5 s (3.2 s before). A team is out also when its count says its three fighters are beaten, read a moment before the K.O.
- The King of Fighters '97 and '98 read the state of the fight (`_fight_state` at 0x10A786, RetroAchievements code notes of '97, the MAME cheat Hide Background of '98). FIGHT ! comes 1.15 s after READY (0x18), with GO. With the timer it came 0.65 s after GO, a second late with the reading. The changes of this state, FIGHT ! and the start of the timer go to the log, to set this delay on a cabinet.

**Version**
- 1.31.1 in `dmd/app.py` and the MAME plugin.

### Français

**Le K.O. des jeux de combat**

Un audit de chaque fichier de jeu qui a une barre de vie, 115 jeux, après que The King of Fighters '98 n'a montré aucun K.O. sur la borne de Seb. Les notes de code de RetroAchievements (téléchargées avec `tools/ra_notes.py`) et les bases de triche de FinalBurn Neo et de MAME ont été lues jeu par jeu. Tout ce qui suit reste à confirmer en jeu.
- Une barre de vie qui passe sous zéro au K.O. se lit vide, et plus pleine. Dans beaucoup de jeux SNK la vie est un mot qu'un K.O. fait passer sous zéro, son octet lu 0xFF (les notes disent ff = K.O. dans Real Bout Fatal Fury 2, SNK vs. Capcom, World Heroes Perfect et 2 Jet, 0xFB dans King of the Monsters), ce qui se lit bien au-dessus du plein et affichait une barre pleine, si bien qu'aucun K.O., aucun WIN et aucun round n'était vu. 40 jeux de combat Neo Geo prennent la règle qu'avaient déjà les jeux Capcom (`"zero_from"`, à mi-chemin entre le plein et le haut de l'octet ou du mot), Art of Fighting 1 à 3, Aggressors of Dark Kombat, Breakers et Breakers Revenge, Fatal Fury 1 à 3 et Special, Fight Fever, Garou, Voltage Fighter Gowcaizer, Kabuki Klash, Kizuna Encounter, King of Fighters '94 et '95, King of the Monsters 1 et 2, The Last Blade 1 et 2, Legend of Success Joe, Matrimelee, Ninja Master's, Real Bout Fatal Fury 1, 2 et Special, Samurai Shodown 1 à 5 et 5 Special, Sengoku 3, SNK vs. Capcom, World Heroes 1, 2, 2 Jet et Perfect. La scène commune des jeux de combat Neo Geo garde les mêmes valeurs pour leurs sets.
- Rage of the Dragons et Ragnagard lisent leur vie en mot signé de 16 bits, sous zéro c'est vide (leurs notes et leurs codes l'écrivent en mot).
- Six jeux restent tels quels, leur vie pleine valant 0xFF ou comptant les dégâts (Galaxy Fight, Karnov's Revenge, Waku Waku 7, Double Dragon, et les jeux de catch Capcom dont le code remplit la barre avec 0xFF).
- La vie de l'ordinateur là où le jeu la garde. Fatal Fury, King of the Monsters et Legend of Success Joe gardent le combattant de l'ordinateur dans un bloc à lui, celui du joueur 2 ne bouge que quand un humain y joue. Contre l'ordinateur, la barre de droite ne bougeait jamais. Elle montre maintenant celle de l'ordinateur (`_cpu_hp`), et celle du joueur 2 quand il joue (un `"tag"` sur `p2_mode`).
- Les rounds gagnés lus dans 13 jeux de plus, étoiles dorées sous les barres et vainqueur de chaque round, Samurai Shodown III, IV, V et V Special, SNK vs. Capcom, Garou, Real Bout Fatal Fury 1, 2 et Special, Art of Fighting 1 et 2, Kabuki Klash.
- Le round du match, ROUND n en grand quand un combat commence comme dans The King of Fighters, Fatal Fury 2 et Special, Real Bout Fatal Fury Special, World Heroes 2 Jet et Perfect (`round`, à partir de 1 dans ces jeux, `"add": -1`).
- Les écrans de sélection que dit le jeu (The King of Fighters '94, '96, '98, '99 et 2002, Real Bout Fatal Fury Special, une valeur `select`). L'écran HD y affiche VS et aucun événement de combat, les barres que le jeu remplit ou vide pour le match suivant ne donnent ni K.O. ni ROUND, et le combat commence avec son ROUND quand l'écran se termine. Les dalles affichent VS aussi.
- Les notes de RetroAchievements numérotent les octets de la RAM de la Neo Geo dans l'autre ordre de chaque paire, l'octet du 68000 est le voisin (0x8238 dans les notes, c'est 0x108239). Chaque valeur qui en vient suit cette règle, vérifiée sur les valeurs des King of Fighters apprises sur une borne.

**FIGHT ! avec le GO du jeu, et les combattants qu'une équipe a perdus** (test 2, la vidéo de Seb sur The King of Fighters '98)
- FIGHT ! vient avec le FIGHT ou le GO du jeu, quand le chrono du round se met à décompter. Sa fraction de seconde (`_time_sub`, notes de code de RetroAchievements, lue dans The King of Fighters '96, '97, '98 et 2003, Real Bout Fatal Fury et Special, Fatal Fury 1, 2 et Special, Samurai Shodown III, IV et V Special) bouge à chaque image dès qu'il tourne, les autres jeux attendent leur première seconde décomptée. FIGHT ! venait 1,35 s après ROUND, avec les noms des combattants, 5 s avant READY et GO. Un chrono réglé sur l'infini le donne 20 s après que les barres se sont remplies (12 s sans la fraction, les entrées des combattants avant un premier round attendent aussi le GO), un jeu qui ne lit pas de chrono le montre tout de suite comme avant. L'onde de choc de FIGHT ! vient avec lui.
- Tant qu'un round attend son GO, l'écran HD garde son chrono. VS s'affichait pendant READY et GO, le chrono étant immobile depuis 6 s.
- The King of Fighters compte un K.O. juste avant que la barre du combattant battu se lise vide. Une équipe éliminée se dit maintenant d'après les combattants qu'elle avait perdus au début du combat (GO). Le compte lu barre encore levée avait déjà ce K.O., et une équipe était éliminée après son deuxième combattant (VICTOIRE CPU, ÉQUIPE P1 ÉLIMINÉE en plein match).
- Pour la même raison, le bandeau du combattant suivant venait avant le K.O. et par-dessus, et son nom et son équipe remplaçaient tout de suite ceux du battu. Les deux attendent maintenant le K.O. et le WIN, 3 s au plus (un round perdu au temps).
- Le dernier combattant d'une équipe perdu au temps finit aussi le match, TIME UP, le WIN, puis le vainqueur en grand.
- Samurai Shodown V Special lisait les images de la seconde de son chrono comme son chrono. Il lit ses secondes (en BCD à 0x10836A, notes de code de RetroAchievements).

**Un combattant à 0 est encore debout, la fin d'un match, FIGHT ! avec GO** (test 3, le deuxième match de Seb sur The King of Fighters '98)
- Dans The King of Fighters '96 à 2002, un combattant à 0 se bat encore, seule une barre passée sous zéro est un K.O. (notes de code de RetroAchievements du '98, 0x0000 = la vie la plus basse encore en vie, sous zéro à la mort). 0 se lit 1 (`"add": 1`). Il donnait un K.O. et le WIN en plein combat (Andy à 0 après un coup gardé), et un combattant à 0 faisait prendre le K.O. de l'autre pour la fin d'un round déjà fini, si bien que le match ne finissait pas.
- La fin d'un match reste 5,5 s (3,2 s avant). Une équipe est éliminée aussi quand son compte dit que ses trois combattants sont battus, lu juste avant le K.O.
- The King of Fighters '97 et '98 lisent l'état du combat (`_fight_state` à 0x10A786, notes de code de RetroAchievements du '97, le code MAME Hide Background du '98). FIGHT ! vient 1,15 s après READY (0x18), avec GO. Avec le chrono, il venait 0,65 s après GO, une seconde de retard avec la lecture. Les changements de cet état, FIGHT ! et le départ du chrono vont dans le journal, pour régler ce délai sur une borne.

**Version**
- 1.31.1 dans `dmd/app.py` et le plugin MAME.

## 1.31.0

### English

**The Cave games**
- Every Cave game of FinalBurn Neo is recognized, with MAME as with RetroArch. That makes 37 games and their 158 sets. The games of the Cave board (DonPachi, DoDonPachi, ESP Ra.De., Dangun Feveron, Guwange, Puzzle Uo Poko), those Cave made for the IGS PGM (DoDonPachi Dai-Ou-Jou and its Black Label, Ketsui, Espgaluda, and DoDonPachi II that IGS made under Cave's licence), the games of Cave's own CV1000 board (Mushihime-sama, its Futari, Black Label and Matsuri, Espgaluda II, Ibara, Ibara Kuro Black Label, Pink Sweets, Muchi Muchi Pork!, Deathsmiles and its MegaBlack Label, DoDonPachi Dai-Fukkatsu and its Black Label, DoDonPachi SaiDaiOuJou, Akai Katana, Puzzle! Mushihime-Tama), and the games other companies made on the Cave board (Power Instinct 2, Gogetsuji Legends, Sailor Moon, Air Gallet, Hotdog Storm, Mazinger Z, Gaia Crusaders, Thunder Heroes, Metamoqester, Koro Koro Quest, Crusher Makochan). A version, a bootleg or a hack takes the file of its original game. The files are made by `tools/cave_games.py` from the list and the cheat database of FinalBurn Neo, completed by MAME's (the cheat collection of mamecheat.co.uk), which knows more for many games.
- What is read (cheat databases of FinalBurn Neo and MAME). The credits, the lives, the bombs and in DoDonPachi and Dai-Ou-Jou their slots (three at the start, one more for each ship lost, six at most), the shot level, the combo gauge that drains, the ship chosen (TYPE-A, TYPE-B, TYPE-C), the stage or the round, the loop of DonPachi and DoDonPachi, the hero of Guwange and his energy, the multiplier of ESP Ra.De., the spirit stones of Espgaluda, the energy of Deathsmiles. The CV1000 games read their credits, lives and bombs from MAME's cheats. The score and the hit counter are not in the cheat databases, learn them with `learn.bat` (`score=`, `hits=`, `stage=`).
- DoDonPachi learned on a cabinet. The score of each player as the game shows it, its tens with the continues used as the last digit, the hit counter of each player as it stays on screen after a chain, the credits.
- A value can be made from others while the game runs, the `"tag"` of a game file with `"sum"` (DoDonPachi's score from its tens and its continues).
- A version whose own cheats put its values elsewhere reads them there, each value where the same cheat of that version writes (Dai-Ou-Jou V100 and its Black Label, Guwange Special, the first versions of DoDonPachi II, the world version of Dai-Ou-Jou with MAME's cheats). A value its cheats do not give is left to learn rather than read at a wrong place.
- RetroArch, FinalBurn Neo core. The 64 KB of the 68000's work RAM of the Cave board (from 0x100000, 0x200000 in Guwange, 0x300000 in Hotdog Storm and Koro Koro Quest, 0x400000 in Power Instinct 2), the 128 KB of the PGM from 0x800000, and the CV1000's RAM from 0xC000000, as far as the values of the game go (2 MB for most of them, up to 6 MB). Metamoqester keeps its values out of this RAM and is read with MAME only.
- A game whose credits are not read counts them from the coin buttons (`coin_buttons.bat`).

**The Capcom games**
- MAME's cheats complete FinalBurn Neo's for the Capcom games too (`tools/cps_games.py`). Street Fighter Zero (CPS Changer) gets all its values, the health, the timer, the rounds won, the super gauge, the characters and the backdrop. Final Fight and Varth read their credits instead of counting the coin buttons. JoJo's Venture names its characters.

**The Neo Geo games**
- Checked against MAME's cheat collection. 286 of their values were already the same, none learned on a cabinet is replaced. MAME adds the super gauge of 14 fighting games, shown under the fighters on the HD screen (Art of Fighting 1 and 2, Garou, King of Fighters '96, Ninja Master's, Real Bout Fatal Fury 1, 2 and Special, Rage of the Dragons, Samurai Shodown III, IV, V and V Special, World Heroes Perfect), the characters of Fatal Fury 2, the timer of Karnov's Revenge, Football Frenzy and The Irritating Maze, the lives and bombs of player 2 in Zed Blade.
- Puzzle Bobble. Player 2's score shows at the top right of the HD screen, the scene had never drawn it (its address, from RetroAchievements, is the one learned on a cabinet).
- Puzzle Bobble in a VS game between two players. The game mode and the matches won by each player are read, these where the game keeps the ones it shows (learned on a cabinet, 0-0, 0-2 then 1-2). The game sets them back to 0-0 when a human then beats the computer, the HD screen follows it. VS takes the place of ROUND between the boards, the wins of each player in big on each side, and a match won shows P1 WINS! or P2 WINS! with the score of the wins, gold sparks over the winner and new boards. On the panel, 2 VS 3 takes the place of ROUND.
- Puzzle Bobble. The arrow of the HD screen turns as the game's does and the bubble leaves in the same direction. The game keeps its arrow in 256 steps per turn, 60 steps (84 degrees) to the left or to the right at most, learned on a cabinet with seven captures each matched to its photo. Player 2's arrow is read 0x9C further, like the scores (it moved in VS captures, to confirm). Read a few times a second, the arrow glides to it, and the next bubble moved a little aside so the arrow aimed far left no longer covers it.
- Strikers 1945 Plus. The SUPER SHOT box of the HD screen fills as the bar of the game does, segment by segment, and glows when it is full. The super shots in stock show beside it (x2), the number jumps when one is earned. What the gauge showed until now is that stock (the cheats say so), it does not move while the bar goes up. The bar is read as one 16-bit number (RetroAchievements code notes, FinalBurn Neo's cheat) and its full value is learned in game, the log notes its first fills. The panel shows SUPER SHOT for each one fired.
- Strikers 1945 Plus. The score of both players is read. It was learned on a cabinet where RetroAchievements' code notes put it, a binary number and not BCD as first read there.
- Strikers 1945 Plus. Each plane of the HD screen has the colours of its sprite in the game, read on photos of the plane select screen. The white P-38 with its blue engines, the blue F5U with its red tail, the Spitfire with green wings and a blue body, the lime Ta-152, the emerald Zero with its yellow leading edges, the red Fiat with its yellow nose, and the light brown XP-55 Ascender with its pale fins, seen in game behind the "?". Player 2's plane is no longer tinted blue, the plane in the side panel keeps its colours, and when both players fly the same plane a small 1P or 2P tab tells them apart.
- The King of Fighters '98 on the HD screen, after Seb's games against the computer in 3 on 3. The value read as the match number in the run ("Select Current Round") is the round of the match, one more at each K.O., and showed STAGE 2, STAGE 3... at every K.O., up to STAGE 6 at the end of the match. It is now `round`, in the King of Fighters '96, '97, '99 and 2000 as well, which keep it at the same kind of place. At a K.O., K.O. in big red letters on the loser's side and WIN in gold on the winner's, with its confetti, and PERFECT after them when the winner took no blow. When the next fight begins, ROUND 2, ROUND 3... in big letters, then FIGHT !, and a new match shows its place under its ROUND 1 (the backdrops of '98, JAPAN, CHINA, KOREA...). The next fighter of a team comes once the K.O. is over, when the game counts one more of its fighters beaten. When a team loses its third fighter, the winner in big letters (P1 WINS) and the team eliminated under it (CPU TEAM ELIMINATED), with confetti across the whole screen.
- The King of Fighters '96 to 2002. A K.O. takes the fighter's health below zero, its word read 0xFF... (RetroAchievements code notes, lose = ff), and the byte read showed a full bar. No K.O. was ever seen, so no K.O. nor WIN, no end of the match, and ROUND came only when the game emptied a bar for its own reasons (Seb). A bar from 0x80 now reads empty (`"zero_from"`), as in Street Fighter II.
- Fighting games. TIME UP only shows when the timer has counted down to 0, a second after another. At the start of a round King of Fighters puts its timer back to 0 before its 60 or 90 seconds, which showed TIME UP (Seb). WIN after a TIME UP comes once it is over. On the select screen of the next match the timer of the last fight stayed (7 in '98). Both health bars empty without a K.O. now give VS at once, as does a timer that has not moved for 6 seconds, on the HD screen as on the panel, and a timer put back to 0 at the start of a round is not shown. Rage of the Dragons keeps its STAGE, its value is the stage of the run ("Select Stage").

**RetroAchievements**
- The public RetroAchievements scripts on GitHub (RATools, 38 scripts for 35 of our arcade games) were compared with the game files. None of them puts one of our values elsewhere, and more than sixty of our values are confirmed, the health bars and the timers of the fighting games, the score of King of Fighters '97, 2001 and 2002, the lives, the score and the weapon of Metal Slug 3, the lives of Ninja Combat, Prehistoric Isle 2 and The Punisher...
- They give the score of 15 games that did not read it. Fatal Fury 3, Galaxy Fight, Karnov's Revenge, King of Fighters 2003, The Last Blade 1 and 2, Real Bout Fatal Fury Special, Prehistoric Isle 2, Night Warriors, Street Fighter Alpha (both players), Street Fighter Alpha 3, Street Fighter III 3rd Strike, The Punisher, Quiz & Dragons (both players) and Puzzle! Mushihime-Tama. And the rounds won of Fatal Fury 3, Karnov's Revenge, Marvel Super Heroes, Street Fighter Alpha 3 and X-Men vs. Street Fighter, gold stars under the health bars on the HD screen. To be checked in game.
- `tools/ra_notes.py` downloads what RetroAchievements knows of the arcade games ArcadeDMD knows into `ra_notes.json`, the code notes, and with an account the achievements, the leaderboards and the rich presence.
- What it downloaded from a RetroAchievements account (293 of our games, 12,000 code notes, 9,500 achievements, 1,000 leaderboards, 176 rich presences) checked against the game files. Its addresses agree with ours on every board, the Neo Geo, the CPS1, CPS2 and CPS3, the Cave board, the PGM and the CV1000, and it confirms the scores taken from the scripts on GitHub. Read in its leaderboards, its rich presence and its code notes, it gives the score of 74 more games. To be checked in game.
  - Neo Geo. Aero Fighters 2 and 3, Art of Fighting, Bang Bead, Blazing Star, Blue's Journey, Burning Fight, Cyber-Lip, Double Dragon, Eight Man, Fatal Fury 1, 2 and Special, Garou, Ghost Pilots, King of Fighters '94, King of the Monsters, Last Resort, Legend of Success Joe, Magical Drop II and III, Magician Lord, Metal Slug 2, X and 5, Money Puzzle Exchanger, Mutation Nation, Puzzle Bobble, Pulstar, Rage of the Dragons, Real Bout Fatal Fury, Samurai Shodown, Sengoku 3, Shock Troopers and its 2nd Squad, Spin Master, Viewpoint, Waku Waku 7, Zupapa!
  - Capcom. 1941, 19XX, Three Wonders, Armored Warriors, Battle Circuit, Cadillacs and Dinosaurs, Capcom Sports Club, Captain Commando, Eco Fighters, Final Fight, JoJo's Bizarre Adventure, Knights of the Round, Mega Man 1 and 2, Mighty! Pang, Pang! 3, Progear, Street Fighter II' Hyper Fighting, Strider, Super Gem Fighter, Super Puzzle Fighter II Turbo, U.N. Squadron, Warriors of Fate.
  - Cave. Akai Katana, Deathsmiles and its MegaBlack Label, DonPachi, ESP Ra.De. (its stage too), Dangun Feveron (the sum of the scores of its stages), Gaia Crusaders, Gogetsuji Legends, Ketsui (two words that the ARM of its protection keeps), Power Instinct 2, Puzzle Uo Poko, Sailor Moon.

**The credits on the HD screen**
- Every scene has the credits as in Metal Slug during a game. The coin struck with the symbol of `config.json` and CRÉDITS 07 in their gold-edged pill, a coin falling onto it for each credit put in and +1 CRÉDIT rising. At the bottom in the middle, or beside it when the game already has something there, the batter of baseball, the hand of mahjong, the answers of the quizzes, the quotas of Magical Drop, the clock of Street Hoop, the shogi board, our soldier in NAM-1975, our fists in The Super Spy, the power gauge of the golf games.
- The fights, the Capcom panels and the Capcom shoot'em ups show them that way too, in place of their CRÉDITS 07 text. The labels that were at the bottom in the middle move up above them (the plane in 19XX and Strikers 1945 Plus, the pilot in Giga Wing, the hero in Dimahoo, the missiles in Varth, LEVEL in Zed Blade, Gururin and Puzzle De Pon!, the stage in Pulstar, ROUND in Blazing Star and Puzzle Bobble).
- Metal Slug. A grenade that blows up, player 1's or player 2's, shakes the whole screen hard and lights it up orange. One right after another shakes less.

**Metal Slug**
- The grenade of the HD screen bounces once and blows up as it lands again, about a second after the throw, as the game's does. In the first Metal Slug, whose grenades on screen are read (RetroAchievements code notes), it blows up at the very moment the game's own does, at once on an enemy hit on the way. Player 2's are read 0xA0 further, to confirm in game.
- At launch the HD screen could show MISSION 183 before MISSION 1, the game's RAM not set yet. A value of a game file can now say which values the game really has (`valid`), another one is set aside. The missions of the Metal Slug go from 1 to 6, 1 to 5 in Metal Slug 3 and 5.

**DoDonPachi on the HD screen**
- Seen from the sky like the other vertical shoot'em ups, the ship flies to the right over the stage and the enemies answer the way Cave's games do. Rings and spirals of pink and blue bullets from the gunships, fans of needles from the helicopters, aimed bullets from the little fighters, big slow orbs from the tanks on the roads.
- The three ships read in the game. The red fighter of the focused stream, the helicopter whose guns follow its turns and whose pods turn around it, the blue fighter of the spread. Player 2 has other colours, as in the game. Each one fires its laser when the fire is held, a thick blue beam that bites the enemy in front, the pods gathered before it.
- An enemy blows up each time the game counts one destroyed, told by its hit counter that climbs, three at most at once, and its points rise where it was. A burst of hits, the laser on a big one, makes it spark, and every 50 hits the chain glows. The points that come without a hit (a medal, a boss, the bonus of the stage) blow up an enemy or count as a bonus, and a big gain (a boss, a big machine) turns all its bullets into gold stars that fly to the ship.
- A bomb turns the screen white and shakes it hard, three rings sweep it from the ship, five waves of blasts burn everything in front, every bullet is wiped away and the enemy fire stops a moment. A ship lost blows up, the bullets vanish for a moment, and the new bomb slot it gives glints.
- The HUD as in the game. 1P and the score with the ships left, the hit counter with its gauge that drains and the best chain (MAX HIT), the bombs at the bottom with the empty slots still to come and MAX when they are all full, the ship chosen, 2P on the right.
- The credits as in Metal Slug, at the bottom in the middle. The coin with the symbol of `config.json` in its gold-edged pill, a coin falling onto it for each credit put in during a game and +1 CRÉDIT rising. The other Cave shoot'em ups have it too.
- The credits go down at START. learn.bat had kept the coins put in (0x100F83), which go up with the credits but never go down, and ArcadeDMD put that address back at each start. It is now set aside, the credits are read where the game counts them, one less for each START and each continue.
- The level of the shot beside the ships left, POWER and a case per level lit up to the level read in the game, MAX at the top. A P taken shows POWER UP over the ship with the level reached under it, POWER MAX at the top. The level is read in the first byte of its cheat, which keeps it while the ship blows up and comes back. The other Cave shoot'em ups have it too, 8 levels in Dai-Ou-Jou, Ketsui and Espgaluda, a bar and 12/14 in Guwange and Air Gallet.
- Its six stages after the maps of the game's stages (sent and numbered by Seb). The dark forest crossed by giant branches, the tanks driving on the long one. The base on a red planet with its hangars, its runway and its great gate, then the cratered ground, its landing pads and its sunken dock. The blue rocky peaks and their valleys of sand. The base and its elevated highway, then the ruined city and the skeletons of its buildings. The great grey machine and its green channels. The orange hive with its honeycomb grates and its cells lit in red, then its lilac half and its purple pipes, where the last stage of the second loop takes place too. Each one goes by in the game's order, from the bottom of its map to its top: the craters before the base and its gate, the ruins before the highway and the base, the lilac part of the hive before the orange one. A new stage changes the backdrop under a STAGE banner. The second loop is announced, and its stages recall it under their banner. The same places, colours and mood, everything drawn by the program, no image comes from the game.
- A boss of our own for each stage, in the dominant colour of the game's (pictures sent by Seb). Only the kind of machine and the colour are kept, the shapes are ours. A green flying wing, a huge khaki tank, a great sand-coloured saucer, a purple gunship, a light blue flying battleship, a deep blue hexagonal fortress, and for the last one a golden crescent, its core glowing in the middle. DoDonPachi II and the other Cave games keep their big machine.
- The ships left as the game shows them, 2 at the start. The game counts the ship in play too, one less is read. The panel shows them the same way.
- Who plays is read in the game, no longer guessed from what moves. The game keeps a state that says player 1 alone, player 2 alone, both, a continue or the ship select (RetroAchievements code notes and rich presence, checked in captures taken on a cabinet), and the ships each player has. Player 2 who presses START at the ship select comes in at once (nobody has ships there yet, the players' flags of the game say who came in), a player whose game is over leaves the HD screen and his side invites to START as in the game, a new game alone does not bring back player 2's plane, and the coin screen no longer comes back when nothing moves for a while. The other Cave games still guess it.
- The boss of each stage, at the WARNING of the game itself. The routine the stage runs is read (0x1013FC), the one of the WARNING found in captures taken on a cabinet at the first three bosses, so the carrier that drops the ship at the start of stage 1 no longer brings a WARNING. In the Japanese and Arrange versions, whose program keeps its routines elsewhere, a little before the stage stops scrolling where its boss comes (RetroAchievements code notes), 14 steps, once the stage was seen scrolling toward it. The log says how long before the stop it came. WARNING and the red alarm, then its name, SUZAKU, SENKOU, KAKOU, RAIKOU, RANKOU, RYUUKOU, and HIBACHI at the end of the second loop. A big machine of our own comes in from the right and holds there, firing thick rings, twin spirals and fans. Our shots and the chain hit it, a bomb shakes it. It falls when the results of the stage show, or on its big score, blasts all over it and its bullets turned into gold stars. The panel shows WARNING! then its name.
- The information in big, the action behind it. Each player has a glass panel, its score as big as it fits, the ships left and the level of the shot, the hit counter with its gauge, the bombs and their slots, the ship chosen. The action goes on behind under a dark veil, darker at the sides, as an animated background. Between the panels the stage, and during a fight the boss's name over a long gauge of its life. The boss comes to the middle, between the panels. The other Cave games keep their HUD for now.
- The boss's life read in the game, a signed 32-bit number at 0x100198, learned on a cabinet with twelve captures of the fight against the boss of stage 1 (86016 when it is entirely on the screen, down to 369 just before it blows up, -33 after). It is where the cheat that kills it in one hit writes, whose 16-bit word alone made the gauge jump when the life went under 65536. Stage 6 keeps its boss's 0x40 before (MAME cheat database), to confirm in game. The gauge is full at the highest life seen, glows at each blow, and the boss blows up when its life reaches 0 or less, as in the game, without waiting for the results. After a continue in the middle of a fight the game keeps the boss's damage, and so does the gauge: the full life of each stage's boss is remembered until it falls or the stage changes, on the HD screen as on the panel. A life under 200 is not a boss's and never makes it fall. A bomb in the middle of the fight brings a lot of points at once, which made our boss fall while the game's was still fighting (Seb). With its life read, only its life says when it falls, and if anything takes it off the screen while the game still fights it, it comes back with its damage.

**The other Cave games on the HD screen**
- Each one has its own scene, built on DoDonPachi's. DonPachi with thinner bullets, Dai-Ou-Jou with the thickest rain of the series, Dai-Fukkatsu and SaiDaiOuJou in brighter colours, DoDonPachi II over the sea. Young psychics of our own over the Tokyo of the future by night (ESP Ra.De., its multiplier beside the gauge). A wanderer of old Japan who walks the village at dusk while his guardian spirit flies around him (Guwange, the hero and his energy read in the game). A night of fever on a floor of neon (Dangun Feveron, the fighter and the round read in the game). Two attack helicopters and their lock-on over the city (Ketsui). Winged heroes and the awakening that slows the bullets down, turns them gold and the screen violet when the spirit stones drain (Espgaluda, Espgaluda II). A great horned beetle over the forest of the insects (Mushihime-sama and its sequels). Fighters high in the sky (Ibara, Pink Sweets), flying pigs (Muchi Muchi Pork!), a gothic flyer over the graveyards, seen from the side (Deathsmiles), fighters of the age of steam, seen from the side (Akai Katana). Hotdog Storm, Mazinger Z (its energy) and Air Gallet with our jet fighters. Uo Poko and Mushihime-Tama with the bubbles of the puzzle games.
- The fighting games (Power Instinct 2, Gogetsuji Legends, Metamoqester) get the fight scene of the fighting games.

**The panel**
- The Cave shoot'em ups have a panel of their own in the spirit of DoDonPachi. Pink and blue bullets drift by, 1P and the score at the top with the ships left, the hit counter in the middle (the ship chosen when there is no chain), the bombs and their empty slots at the bottom with MAX when they are full, and the combo gauge that drains.
- A panel scene can show the empty slots up to a value (`"slots"` of an `icons` layer) and test a value against another one (`"ge_var"` in a `"when"`).
- DoDonPachi's panel shows the boss's life during a fight, a thin bar above the bombs, full at the highest life seen. A gauge of a panel scene can take its top from the highest value seen while it shows (`"max": "peak"`), kept while it hides for at most `"peak_hold"` seconds (half a second by default, a minute for the boss, the time of a continue).

**The shoot'em ups**
- Every shoot'em up whose power is read shows POWER UP over the ship with the level reached under it, a case per level as on its HUD, and POWER MAX at the top (Blazing Star, the Aero Fighters, Strikers 1945 Plus, Last Resort, the Capcom and Cave shoot'em ups...). Andro Dunos shows the level of each of its four weapons, Zed Blade its LEVEL.

**learn.bat**
- Under RetroArch a big RAM is read by windows of requests. The 2 MB of a CV1000 took a minute, it now takes seconds. A small RAM is read as before.
- Credits that only went up between the captures. The coins put in go up with them, so learn.bat says so, asks for one capture after START (one credit less) and saves nothing by itself, unless its first choice is the address the game file already has.
- A name that neither the game file nor the scenes know is reported with the closest one (scroe2, did you mean score2?) and nothing is captured. The same line typed again keeps it. An s too many (scores2) or a 2 stuck to the name (wins2, victoires2) is understood, and a value already learned under such a name moves to the right one at start.

**Demo**
- `demo_cave.bat` shows the Cave games without playing. Pick the game in the list, or give it directly, `demo_cave.bat ddonpach` for example.

**Updating from 1.30.1**
Unzip the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Les jeux Cave**
- Tous les jeux Cave de FinalBurn Neo sont reconnus, avec MAME comme avec RetroArch. Cela fait 37 jeux et leurs 158 sets. Les jeux de la carte Cave (DonPachi, DoDonPachi, ESP Ra.De., Dangun Feveron, Guwange, Puzzle Uo Poko), ceux que Cave a faits pour le PGM d'IGS (DoDonPachi Dai-Ou-Jou et son Black Label, Ketsui, Espgaluda, et DoDonPachi II qu'IGS a fait sous licence Cave), les jeux de la carte CV1000 de Cave (Mushihime-sama, son Futari, son Black Label et son Matsuri, Espgaluda II, Ibara, Ibara Kuro Black Label, Pink Sweets, Muchi Muchi Pork!, Deathsmiles et son MegaBlack Label, DoDonPachi Dai-Fukkatsu et son Black Label, DoDonPachi SaiDaiOuJou, Akai Katana, Puzzle! Mushihime-Tama), et les jeux que d'autres ont faits sur la carte Cave (Power Instinct 2, Gogetsuji Legends, Sailor Moon, Air Gallet, Hotdog Storm, Mazinger Z, Gaia Crusaders, Thunder Heroes, Metamoqester, Koro Koro Quest, Crusher Makochan). Une version, un bootleg ou un hack prend le fichier de son jeu d'origine. Les fichiers sont faits par `tools/cave_games.py` d'après la liste et la base de triche de FinalBurn Neo, complétée par celle de MAME (la collection de mamecheat.co.uk), qui en sait plus pour beaucoup de jeux.
- Ce qui est lu (bases de triche de FinalBurn Neo et de MAME). Les crédits, les vies, les bombes et dans DoDonPachi et Dai-Ou-Jou leurs places (trois au départ, une de plus par vaisseau perdu, six au plus), le niveau du tir, la jauge de combo qui se vide, le vaisseau choisi (TYPE-A, TYPE-B, TYPE-C), le niveau ou le round, la boucle de DonPachi et DoDonPachi, le héros de Guwange et son énergie, le multiplicateur d'ESP Ra.De., les pierres d'esprit d'Espgaluda, l'énergie de Deathsmiles. Les jeux du CV1000 lisent leurs crédits, leurs vies et leurs bombes dans les codes de MAME. Le score et le compteur de coups ne sont pas dans les bases de triche, apprends-les avec `learn.bat` (`score=`, `hits=`, `stage=`).
- DoDonPachi appris sur une borne. Le score de chaque joueur comme le jeu l'affiche, ses dizaines avec le nombre de continues en dernier chiffre, le compteur de coups de chaque joueur tel qu'il reste à l'écran après une chaîne, les crédits.
- Une valeur peut être faite d'autres pendant le jeu, le `"tag"` d'un fichier de jeu avec `"sum"` (le score de DoDonPachi d'après ses dizaines et ses continues).
- Une version dont les propres codes de triche mettent ses valeurs ailleurs les lit là, chaque valeur là où écrit le même code de cette version (Dai-Ou-Jou V100 et son Black Label, Guwange Special, les premières versions de DoDonPachi II, la version mondiale de Dai-Ou-Jou avec les codes de MAME). Une valeur que ses codes ne donnent pas reste à apprendre plutôt que lue au mauvais endroit.
- RetroArch, cœur FinalBurn Neo. Les 64 Ko de la RAM de travail du 68000 de la carte Cave (à partir de 0x100000, 0x200000 dans Guwange, 0x300000 dans Hotdog Storm et Koro Koro Quest, 0x400000 dans Power Instinct 2), les 128 Ko du PGM à partir de 0x800000, et la RAM du CV1000 à partir de 0xC000000, aussi loin que vont les valeurs du jeu (2 Mo pour la plupart, jusqu'à 6 Mo). Metamoqester garde ses valeurs hors de cette RAM et se lit avec MAME seulement.
- Un jeu dont les crédits ne sont pas lus les compte d'après les boutons des pièces (`coin_buttons.bat`).

**Les jeux Capcom**
- Les codes de MAME complètent ceux de FinalBurn Neo pour les jeux Capcom aussi (`tools/cps_games.py`). Street Fighter Zero (CPS Changer) a toutes ses valeurs, la vie, le chrono, les rounds gagnés, la jauge de super, les personnages et le décor. Final Fight et Varth lisent leurs crédits au lieu de compter les boutons des pièces. JoJo's Venture nomme ses personnages.

**Les jeux Neo Geo**
- Vérifiés avec la collection de codes de MAME. 286 de leurs valeurs étaient déjà les mêmes, aucune de celles apprises sur une borne n'est remplacée. MAME ajoute la jauge de super de 14 jeux de combat, affichée sous les combattants sur l'écran HD (Art of Fighting 1 et 2, Garou, King of Fighters '96, Ninja Master's, Real Bout Fatal Fury 1, 2 et Special, Rage of the Dragons, Samurai Shodown III, IV, V et V Special, World Heroes Perfect), les personnages de Fatal Fury 2, le chrono de Karnov's Revenge, Football Frenzy et The Irritating Maze, les vies et les bombes du joueur 2 dans Zed Blade.
- Puzzle Bobble. Le score du joueur 2 s'affiche en haut à droite de l'écran HD, la scène ne le dessinait jamais (son adresse, venue de RetroAchievements, est celle apprise sur une borne).
- Puzzle Bobble en partie VS à deux. Le mode de jeu et les matchs gagnés par chaque joueur sont lus, ceux-ci là où le jeu garde ceux qu'il affiche (appris sur une borne, 0-0, 0-2 puis 1-2). Le jeu les remet à 0-0 quand un humain bat ensuite l'ordinateur, l'écran HD le suit. VS remplace le ROUND entre les plateaux, avec les victoires de chaque joueur en gros de chaque côté, et un match gagné affiche J1 GAGNE ! ou J2 GAGNE ! avec le score des victoires, des étincelles dorées sur le gagnant et de nouveaux plateaux. Sur la dalle, 2 VS 3 remplace le ROUND.
- Puzzle Bobble. La flèche de l'écran HD tourne comme celle du jeu et la bulle part dans la même direction. Le jeu garde sa flèche en 256 pas par tour, 60 pas (84 degrés) à gauche ou à droite au plus, appris sur une borne avec sept captures chacune avec sa photo. La flèche du joueur 2 est lue 0x9C plus loin, comme les scores (elle bougeait dans des captures du VS, à confirmer). Lue quelques fois par seconde, la flèche y glisse, et la bulle suivante s'est un peu écartée pour que la flèche tout à gauche ne la cache plus.
- Strikers 1945 Plus. La case SUPER SHOT de l'écran HD se remplit comme la barre du jeu, segment par segment, et brille quand elle est pleine. Les super tirs en réserve s'affichent à côté (x2), le nombre saute quand on en gagne un. Ce que la jauge montrait jusqu'ici, c'est cette réserve (les codes de triche le disent), elle ne bouge pas quand la barre monte. La barre est lue comme un nombre de 16 bits (notes de code de RetroAchievements, code de triche de FinalBurn Neo) et sa valeur pleine est apprise en jeu, le journal note ses premiers remplissages. La dalle affiche SUPER SHOT à chaque super tir parti.
- Strikers 1945 Plus. Le score des deux joueurs se lit. Il a été appris sur une borne là où le mettent les notes de RetroAchievements, un nombre binaire et pas du BCD comme on l'y avait d'abord lu.
- Strikers 1945 Plus. Chaque avion de l'écran HD a les couleurs de son sprite dans le jeu, lues sur des photos de l'écran de choix des avions. Le P-38 blanc aux moteurs bleus, le F5U bleu à la queue rouge, le Spitfire aux ailes vertes et au corps bleu, le Ta-152 vert anis, le Zero émeraude aux bords d'attaque jaunes, le Fiat rouge au nez jaune, et l'Ascender marron clair aux dérives pâles, vu en jeu derrière le « ? ». L'avion du joueur 2 n'est plus teinté de bleu, celui du panneau de côté garde ses couleurs, et quand les deux joueurs volent sur le même avion un petit onglet 1P ou 2P les distingue.
- The King of Fighters '98 sur l'écran HD, d'après les parties de Seb contre l'ordinateur en 3 contre 3. La valeur lue comme le numéro du match dans la partie (« Select Current Round ») est le round du match, un de plus à chaque K.O., et affichait STAGE 2, STAGE 3... à chaque K.O., jusqu'à STAGE 6 à la fin du match. C'est maintenant `round`, dans les King of Fighters '96, '97, '99 et 2000 aussi, qui la gardent au même genre d'endroit. À un K.O., K.O. en grosses lettres rouges du côté du perdant et WIN doré du côté du gagnant, avec ses confettis, et PERFECT après eux quand le gagnant n'a pris aucun coup. Quand le combat suivant commence, ROUND 2, ROUND 3... en grand, puis FIGHT !, et un nouveau match affiche son lieu sous son ROUND 1 (les décors du '98, JAPON, CHINE, CORÉE...). Le combattant suivant d'une équipe entre une fois le K.O. passé, quand le jeu compte un de ses combattants battu de plus. Quand une équipe perd son troisième combattant, le vainqueur en grand (VICTOIRE P1) et l'équipe éliminée dessous (ÉQUIPE CPU ÉLIMINÉE), avec des confettis sur tout l'écran.
- The King of Fighters '96 à 2002. Un K.O. fait passer la vie du combattant sous zéro, son mot lu 0xFF... (notes de code de RetroAchievements, lose = ff), et l'octet lu affichait une barre pleine. Aucun K.O. n'était vu, donc ni K.O. ni WIN, pas de fin de match, et ROUND ne venait que quand le jeu vidait une barre pour ses propres raisons (Seb). Une barre à partir de 0x80 se lit maintenant vide (`"zero_from"`), comme dans Street Fighter II.
- Jeux de combat. TIME UP ne s'affiche que quand le chrono a décompté jusqu'à 0, une seconde après l'autre. Au début d'un round, King of Fighters remet son chrono à 0 avant ses 60 ou 90 secondes, ce qui affichait TIME UP (Seb). Le WIN après un TIME UP vient une fois celui-ci passé. À l'écran de sélection du match suivant, le chrono du combat d'avant restait (7 dans le '98). Les deux barres de vie vides sans K.O. donnent maintenant VS tout de suite, comme un chrono qui n'a pas bougé depuis 6 secondes, sur l'écran HD comme sur la dalle, et un chrono remis à 0 au début d'un round ne s'affiche pas. Rage of the Dragons garde son STAGE, sa valeur est le niveau de la partie (« Select Stage »).

**RetroAchievements**
- Les scripts RetroAchievements publics sur GitHub (RATools, 38 scripts pour 35 de nos jeux d'arcade) ont été comparés aux fichiers de jeu. Aucun ne met une de nos valeurs ailleurs, et plus de soixante de nos valeurs sont confirmées, les barres de vie et les chronos des jeux de combat, le score de King of Fighters '97, 2001 et 2002, les vies, le score et l'arme de Metal Slug 3, les vies de Ninja Combat, Prehistoric Isle 2 et The Punisher...
- Ils donnent le score de 15 jeux qui ne le lisaient pas. Fatal Fury 3, Galaxy Fight, Karnov's Revenge, King of Fighters 2003, The Last Blade 1 et 2, Real Bout Fatal Fury Special, Prehistoric Isle 2, Night Warriors, Street Fighter Alpha (les deux joueurs), Street Fighter Alpha 3, Street Fighter III 3rd Strike, The Punisher, Quiz & Dragons (les deux joueurs) et Puzzle! Mushihime-Tama. Et les rounds gagnés de Fatal Fury 3, Karnov's Revenge, Marvel Super Heroes, Street Fighter Alpha 3 et X-Men vs. Street Fighter, des étoiles dorées sous les barres de vie sur l'écran HD. À vérifier en jeu.
- `tools/ra_notes.py` télécharge ce que RetroAchievements sait des jeux d'arcade qu'ArcadeDMD connaît dans `ra_notes.json`, les notes de code, et avec un compte les succès, les classements et la présence.
- Ce qu'il a téléchargé avec un compte RetroAchievements (293 de nos jeux, 12 000 notes de code, 9 500 succès, 1 000 classements, 176 présences) comparé aux fichiers de jeu. Ses adresses collent avec les nôtres sur toutes les cartes, la Neo Geo, les CPS1, CPS2 et CPS3, la carte Cave, le PGM et le CV1000, et il confirme les scores pris dans les scripts de GitHub. Lu dans ses classements, sa présence et ses notes de code, il donne le score de 74 jeux de plus. À vérifier en jeu.
  - Neo Geo. Aero Fighters 2 et 3, Art of Fighting, Bang Bead, Blazing Star, Blue's Journey, Burning Fight, Cyber-Lip, Double Dragon, Eight Man, Fatal Fury 1, 2 et Special, Garou, Ghost Pilots, King of Fighters '94, King of the Monsters, Last Resort, Legend of Success Joe, Magical Drop II et III, Magician Lord, Metal Slug 2, X et 5, Money Puzzle Exchanger, Mutation Nation, Puzzle Bobble, Pulstar, Rage of the Dragons, Real Bout Fatal Fury, Samurai Shodown, Sengoku 3, Shock Troopers et son 2nd Squad, Spin Master, Viewpoint, Waku Waku 7, Zupapa!
  - Capcom. 1941, 19XX, Three Wonders, Armored Warriors, Battle Circuit, Cadillacs and Dinosaurs, Capcom Sports Club, Captain Commando, Eco Fighters, Final Fight, JoJo's Bizarre Adventure, Knights of the Round, Mega Man 1 et 2, Mighty! Pang, Pang! 3, Progear, Street Fighter II' Hyper Fighting, Strider, Super Gem Fighter, Super Puzzle Fighter II Turbo, U.N. Squadron, Warriors of Fate.
  - Cave. Akai Katana, Deathsmiles et son MegaBlack Label, DonPachi, ESP Ra.De. (son niveau aussi), Dangun Feveron (la somme des scores de ses niveaux), Gaia Crusaders, Gogetsuji Legends, Ketsui (deux mots que garde l'ARM de sa protection), Power Instinct 2, Puzzle Uo Poko, Sailor Moon.

**Les crédits sur l'écran HD**
- Toutes les scènes ont les crédits comme dans Metal Slug pendant une partie. La pièce frappée du symbole de `config.json` et CRÉDITS 07 dans leur pastille au bord doré, une pièce qui tombe dessus pour chaque crédit mis et +1 CRÉDIT qui monte. En bas au milieu, ou à côté quand le jeu y a déjà quelque chose, le frappeur du baseball, la main du mahjong, les réponses des quiz, les quotas de Magical Drop, le chrono de Street Hoop, le plateau de shogi, notre soldat dans NAM-1975, nos poings dans The Super Spy, la jauge de puissance des jeux de golf.
- Les combats, les panneaux Capcom et les shoot'em ups Capcom les montrent ainsi aussi, à la place de leur texte CRÉDITS 07. Ce qui était en bas au milieu remonte au-dessus (l'avion dans 19XX et Strikers 1945 Plus, le pilote dans Giga Wing, le héros dans Dimahoo, les missiles dans Varth, LEVEL dans Zed Blade, Gururin et Puzzle De Pon!, le stage dans Pulstar, ROUND dans Blazing Star et Puzzle Bobble).
- Metal Slug. Une grenade qui explose, celle du joueur 1 ou du joueur 2, fait trembler fort tout l'écran et l'éclaire d'orange. Celle qui suit de près une autre tremble moins.

**Metal Slug**
- La grenade de l'écran HD rebondit une fois et explose en retombant, une seconde environ après le lancer, comme celle du jeu. Dans le premier Metal Slug, dont les grenades à l'écran se lisent (notes de code de RetroAchievements), elle explose au moment même où celle du jeu explose, tout de suite sur un ennemi touché en chemin. Celles du joueur 2 se lisent 0xA0 plus loin, à vérifier en jeu.
- Au lancement, l'écran HD pouvait afficher MISSION 183 avant MISSION 1, la RAM du jeu pas encore prête. Une valeur d'un fichier de jeu peut maintenant dire les valeurs que le jeu a vraiment (`valid`), une autre est écartée. Les missions des Metal Slug vont de 1 à 6, de 1 à 5 dans Metal Slug 3 et 5.

**DoDonPachi sur l'écran HD**
- Vu du ciel comme les autres shoot'em ups verticaux, le vaisseau vole vers la droite au-dessus du niveau et les ennemis répondent comme dans les jeux Cave. Des anneaux et des spirales de boulettes roses et bleues des canonnières, des éventails d'aiguilles des hélicoptères, des balles visées des petits chasseurs, de grosses sphères lentes des chars sur les routes.
- Les trois vaisseaux lus dans le jeu. Le chasseur rouge du tir serré, l'hélicoptère dont les canons suivent les virages et dont les nacelles tournent autour de lui, le chasseur bleu de l'éventail. Le joueur 2 a d'autres couleurs, comme dans le jeu. Chacun tire son laser quand le tir est maintenu, un épais rayon bleu qui mord l'ennemi devant lui, les nacelles réunies devant.
- Un ennemi explose chaque fois que le jeu en compte un de détruit, d'après son compteur de coups qui monte, trois au plus d'un coup, et ses points montent là où il était. Une rafale de coups, le laser sur un gros, le fait étinceler, et tous les 50 coups la chaîne brille. Les points qui viennent sans coup (une médaille, un boss, le bonus du niveau) font exploser un ennemi ou se comptent en bonus, et un gros gain (un boss, une grosse machine) change toutes ses boulettes en étoiles d'or qui filent vers le vaisseau.
- Une bombe fait blanchir l'écran et le secoue fort, trois anneaux le balaient depuis le vaisseau, cinq vagues d'explosions brûlent tout devant, toutes les boulettes disparaissent et le tir ennemi s'arrête un moment. Un vaisseau perdu explose, les boulettes disparaissent un moment, et la place de bombe qu'il donne en plus brille.
- Le HUD comme dans le jeu. 1P et le score avec les vaisseaux restants, le compteur de coups avec sa jauge qui se vide et la meilleure chaîne (MAX HIT), les bombes en bas avec les places vides des bombes à venir et MAX quand tout est plein, le vaisseau choisi, 2P à droite.
- Les crédits comme dans Metal Slug, en bas au milieu. La pièce au symbole de `config.json` dans sa pastille au bord doré, une pièce qui tombe dessus pour chaque crédit mis pendant une partie et +1 CRÉDIT qui monte. Les autres shoot'em ups Cave l'ont aussi.
- Les crédits baissent au START. learn.bat avait gardé les pièces mises (0x100F83), qui montent avec les crédits mais ne descendent jamais, et ArcadeDMD remettait cette adresse à chaque démarrage. Elle est maintenant écartée, les crédits se lisent là où le jeu les compte, un de moins à chaque START et à chaque continue.
- Le niveau du tir à côté des vaisseaux restants, POWER et une case par niveau allumées jusqu'au niveau lu dans le jeu, MAX en haut. Un P ramassé affiche POWER UP au-dessus du vaisseau avec le niveau atteint dessous, POWER MAX au plus haut. Le niveau se lit dans le premier octet de son code, qui le garde pendant que le vaisseau explose et revient. Les autres shoot'em ups Cave l'ont aussi, 8 niveaux dans Dai-Ou-Jou, Ketsui et Espgaluda, une barre et 12/14 dans Guwange et Air Gallet.
- Ses six niveaux d'après les cartes des niveaux du jeu (envoyées et numérotées par Seb). La forêt sombre traversée de branches géantes, les chars roulant sur la longue. La base sur une planète rouge avec ses hangars, sa piste et son grand portail, puis le sol et ses cratères, ses pistes rondes et son bassin. Les pics rocheux bleus et leurs vallées de sable. La base et son autoroute surélevée, puis la ville en ruines et les squelettes de ses immeubles. La grande machine grise et ses canaux verts. La ruche orange avec ses grilles en alvéoles et ses cellules allumées en rouge, puis sa moitié lilas et ses tuyaux violets, où se passe aussi le dernier niveau de la deuxième boucle. Chacun défile dans l'ordre du jeu, du bas de sa carte à son haut, les cratères avant la base et son portail, les ruines avant l'autoroute et la base, la partie lilas de la ruche avant l'orange. Un nouveau niveau change le décor sous un bandeau STAGE. La deuxième boucle s'annonce, et ses niveaux la rappellent sous leur bandeau. Les mêmes lieux, couleurs et ambiance, tout dessiné par le programme, aucune image ne vient du jeu.
- Un boss à nous pour chaque niveau, dans la couleur dominante de celui du jeu (images envoyées par Seb). Seuls le genre d'engin et la couleur sont gardés, les formes sont à nous. Une aile volante verte, un énorme char kaki, une grande soucoupe couleur sable, une canonnière violette, un cuirassé volant bleu clair, une forteresse hexagonale bleu profond, et pour le dernier un croissant doré, son cœur qui luit au milieu. DoDonPachi II et les autres jeux Cave gardent leur grosse machine.
- Les vaisseaux qui restent comme le jeu les montre, 2 au départ. Le jeu compte aussi le vaisseau en jeu, un de moins est lu. La dalle les montre de même.
- Qui joue se lit dans le jeu, il n'est plus deviné d'après ce qui bouge. Le jeu garde un état qui dit le joueur 1 seul, le joueur 2 seul, les deux, une continue ou le choix du vaisseau (notes de code et présence de RetroAchievements, vérifiées dans des captures prises sur une borne), et les vaisseaux de chaque joueur. Le joueur 2 qui fait START au choix du vaisseau arrive tout de suite (personne n'y a encore de vaisseaux, les drapeaux des joueurs du jeu disent qui est arrivé), un joueur dont la partie est finie quitte l'écran HD et son côté invite à faire START comme dans le jeu, une nouvelle partie seul ne ramène pas l'avion du joueur 2, et l'écran à pièces ne revient plus quand rien ne bouge un moment. Les autres jeux Cave le devinent toujours.
- Le boss de chaque niveau, au WARNING du jeu lui-même. La routine que suit le niveau est lue (0x1013FC), celle du WARNING trouvée dans des captures prises sur une borne aux trois premiers boss, si bien que le porte-avions qui largue le vaisseau au début du niveau 1 ne donne plus de WARNING. Dans les versions japonaise et Arrange, dont le programme garde ses routines ailleurs, un peu avant que le niveau s'arrête de défiler là où son boss arrive (notes de code de RetroAchievements), 14 pas, une fois le niveau vu défiler vers lui. Le journal dit combien de temps avant l'arrêt il est venu. WARNING et l'alarme rouge, puis son nom, SUZAKU, SENKOU, KAKOU, RAIKOU, RANKOU, RYUUKOU, et HIBACHI au bout du second tour. Une grosse machine à nous entre par la droite et tient sa place en tirant des anneaux serrés, des spirales jumelles et des éventails. Nos tirs et la chaîne la touchent, une bombe la secoue. Elle tombe quand les résultats du niveau s'affichent, ou sur son gros score, des explosions partout sur elle et ses boulettes changées en étoiles d'or. La dalle affiche WARNING! puis son nom.
- Les informations en grand, l'action derrière. Chaque joueur a son panneau de verre, son score aussi grand que possible, les vaisseaux restants et le niveau du tir, le compteur de coups avec sa jauge, les bombes et leurs places, le vaisseau choisi. L'action continue derrière sous un voile sombre, plus sombre sur les côtés, comme une animation de fond. Entre les panneaux le niveau, et pendant un combat le nom du boss au-dessus d'une longue jauge de sa vie. Le boss vient au milieu, entre les panneaux. Les autres jeux Cave gardent leur HUD pour l'instant.
- La vie du boss lue dans le jeu, un nombre signé de 32 bits à 0x100198, appris sur une borne avec douze captures du combat contre le boss du niveau 1 (86016 quand il est entièrement à l'écran, jusqu'à 369 juste avant qu'il explose, -33 après). C'est là où écrit le code de triche qui le tue d'un coup, dont le mot de 16 bits seul faisait sauter la jauge quand la vie passait sous 65536. Le niveau 6 garde celle de son boss 0x40 avant (base de triche de MAME), à confirmer en jeu. La jauge est pleine à la plus haute vie vue, s'éclaire à chaque coup, et le boss explose quand sa vie arrive à 0 ou moins, comme dans le jeu, sans attendre les résultats. Après une continue en plein combat, le jeu garde les dégâts du boss et la jauge aussi, la vie pleine du boss de chaque niveau étant retenue jusqu'à ce qu'il tombe ou que le niveau change, sur l'écran HD comme sur la dalle. Une vie sous 200 n'est pas celle d'un boss et ne le fait jamais tomber. Une bombe en plein combat rapporte beaucoup de points d'un coup, ce qui faisait tomber notre boss alors que celui du jeu se battait encore (Seb). Sa vie lue dit seule quand il tombe, et si quoi que ce soit le fait quitter l'écran pendant que le jeu se bat encore contre lui, il revient avec ses dégâts.

**Les autres jeux Cave sur l'écran HD**
- Chacun a sa scène, bâtie sur celle de DoDonPachi. DonPachi avec moins de boulettes, Dai-Ou-Jou avec la pluie la plus épaisse de la série, Dai-Fukkatsu et SaiDaiOuJou en couleurs plus vives, DoDonPachi II au-dessus de la mer. De jeunes médiums à nous au-dessus du Tokyo du futur la nuit (ESP Ra.De., son multiplicateur à côté de la jauge). Un voyageur du Japon d'autrefois qui marche dans le village au crépuscule pendant que son esprit gardien vole autour de lui (Guwange, le héros et son énergie lus dans le jeu). Une nuit de fièvre sur une piste au néon (Dangun Feveron, le chasseur et le round lus dans le jeu). Deux hélicoptères d'attaque et leur verrouillage au-dessus de la ville (Ketsui). Des héros ailés et l'éveil qui ralentit les boulettes, les rend dorées et fait virer l'écran au violet quand les pierres d'esprit fondent (Espgaluda, Espgaluda II). Un grand scarabée à corne au-dessus de la forêt des insectes (Mushihime-sama et ses suites). Des chasseurs haut dans le ciel (Ibara, Pink Sweets), des cochons volants (Muchi Muchi Pork!), une silhouette gothique au-dessus des cimetières, de profil (Deathsmiles), des chasseurs de l'âge de la vapeur, de profil (Akai Katana). Hotdog Storm, Mazinger Z (son énergie) et Air Gallet avec nos chasseurs à réaction. Uo Poko et Mushihime-Tama avec les bulles des jeux de réflexion.
- Les jeux de combat (Power Instinct 2, Gogetsuji Legends, Metamoqester) ont la scène des jeux de combat.

**La dalle**
- Les shoot'em ups Cave ont leur dalle dans l'esprit de DoDonPachi. Des boulettes roses et bleues passent, 1P et le score en haut avec les vaisseaux restants, le compteur de coups au milieu (le vaisseau choisi quand il n'y a pas de chaîne), les bombes et leurs places vides en bas avec MAX quand tout est plein, et la jauge de combo qui se vide.
- Une scène de la dalle peut montrer les places vides jusqu'à une valeur (`"slots"` d'une couche `icons`) et comparer une valeur à une autre (`"ge_var"` dans un `"when"`).
- La dalle de DoDonPachi montre la vie du boss pendant un combat, une barre fine au-dessus des bombes, pleine à la plus haute vie vue. Une jauge d'une scène de la dalle peut prendre son maximum de la plus haute valeur vue pendant qu'elle s'affiche (`"max": "peak"`), gardé tant qu'elle reste cachée au plus `"peak_hold"` secondes (une demi-seconde par défaut, une minute pour le boss, le temps d'une continue).

**Les shoot'em ups**
- Chaque shoot'em up dont la puissance est lue affiche POWER UP au-dessus du vaisseau avec le niveau atteint dessous, une case par niveau comme sur son HUD, et POWER MAX au plus haut (Blazing Star, les Aero Fighters, Strikers 1945 Plus, Last Resort, les shoot'em ups Capcom et Cave...). Andro Dunos montre le niveau de chacune de ses quatre armes, Zed Blade son LEVEL.

**learn.bat**
- Sous RetroArch, une grande RAM se lit par fenêtres de demandes. Les 2 Mo d'un CV1000 prenaient une minute, quelques secondes maintenant. Une petite RAM se lit comme avant.
- Des crédits qui n'ont fait que monter entre les captures. Les pièces mises montent avec eux, alors learn.bat le dit, demande une capture après START (un crédit en moins) et n'enregistre rien d'office, sauf si son premier choix est l'adresse que le fichier du jeu a déjà.
- Un nom que ni le fichier du jeu ni les scènes ne connaissent est signalé avec le plus proche (scroe2, tu voulais dire score2 ?) et rien n'est capturé. La même ligne retapée le garde. Un s en trop (scores2) ou un 2 collé au nom (wins2, victoires2) est compris, et une valeur déjà apprise sous un tel nom passe sous le bon au démarrage.

**Démo**
- `demo_cave.bat` montre les jeux Cave sans jouer. Choisis le jeu dans la liste, ou donne-le directement, `demo_cave.bat ddonpach` par exemple.

**Mettre à jour depuis la 1.30.1**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.30.1

### English

**The START buttons**
- `coin_buttons.bat` now also asks for the START button of each player. In a game that does not give its credits (most Capcom games under RetroArch, Mercs, Final Fight, Street Fighter II', the Alpha series...), a player who presses START with a credit begins at once. The game shows from the select screen or the intro on, PRESS START no longer waits until the player has control. Player 2 who presses START takes his credit too, a challenger in a fighting game included. Nothing is counted for START pressed without a credit, during a game or in RetroArch's menu.
- The coin buttons count fast presses, one coin each, like RetroArch. A press less than 0.15 s after the previous one was taken for a bounce, and the credits of a Neo Geo fell behind the game's. A bounce is now a contact shorter than 30 ms right after the button was let go.

**Capcom games**
- Player 2 of the fighting games. PRESS START and CPU stayed on his side even when a second player came in. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 and JoJo's Bizarre Adventure read who controls each fighter, a human or the computer (cheat database), and so do Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter and X-Men: Children of the Atom (found in captures made on a cabinet). In the other fighting games, player 2 is seen as he comes in, his score going up once it is learned, his START with a credit, or a credit spent during a fight (a challenger). He leaves when nobody plays any more, or two minutes after his score stopped moving.
- Player 2 who plays alone against the computer. Player 1 shows as CPU, with PRESS START or INSERT COIN above him, and his score is no longer the computer's. The games above read it, the others see it from player 2's START followed by a credit the game spends. Player 1 who comes in afterwards plays again.
- In the Marvel games (X-Men: Children of the Atom, Marvel Super Heroes and the three "vs.") the computer scores too. A score going up no longer makes player 2 a human there.
- Hyper Street Fighter II, Marvel vs. Capcom, X-Men: Children of the Atom, Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter read the score of each player, learned on a cabinet.
- The super gauge of Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter and X-Men: Children of the Atom works like the game's. The bar of the current level, with POWER 1, 2 or 3 beside it, and POWER MAX at the top level. It showed the level as a third of the bar, X-Men's stayed empty at Level 1.
- Marvel vs. Capcom reads its credits, learned on a cabinet. Two coins for a credit is counted right.
- Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter give each player two fighters who take turns. The health and the name shown are those of the fighter on screen, and a partner who comes in is no longer a K.O. Two empty bars and a DOUBLE K.O. came in the middle of a fight.
- A game that clears both fighters (the select screen after START, the end of a game) no longer shows a DOUBLE K.O., nor KO in the middle of the HD screen and on the panel, in every fighting game. X-Men: Children of the Atom showed one at each START.
- The empty part of the health bars on the HD screen is dark grey instead of dark red, in every fighting game. A nearly empty bar looked full and red on the cabinet (X-Men: Children of the Atom).
- X-Men: Children of the Atom reads the rounds won by each player, the S under the portraits of the game (found in captures made on a cabinet). The winner of a round shows even when a bar is not quite empty.
- Night Warriors reads the rounds won by each player (cheat database). Gold stars under the bars on the HD screen, gold squares next to the timer on the panel, and the winner of each round from them.
- The health of Magic Sword, Willow and Tenchi wo Kurau II reads empty when it goes below zero, like in the other Capcom games since 1.30.0.
- A version whose own cheats put its values elsewhere reads them there. The second revision of JoJo's Venture (all its values), Quiz & Dragons' Japanese resale (the lives) and the US Eco Fighters (the credits) read their parent's addresses until now.

**Neo Geo**
- Metal Slug shows its tank on the HD screen. In the tank, the tank takes the place of the weapon, with its energy in hits (three, like in the game) and its cannon shells. A hit makes the lost case blink, a shell flies to the backdrop, BAIL OUT! blinks when it has no energy left, and a destroyed tank blows up. The demo gets in the tank too, and your own drawing of the tank can take the place of ArcadeDMD's (`sprites\mslug_tank_hd.png`). A plain background around it is made transparent, its empty margins are cut, it sits in the middle of the card's frame and the shells leave from its cannon. Whether the player is in it was found in RAM captures made on a cabinet. The tank's energy and shells are its own (cheat database), right as soon as the player gets in.
- The rescued prisoners of the first Metal Slug (found in RAM captures made on a cabinet), of Metal Slug X, of player 2 in Metal Slug 3 and of Metal Slug 5 (cheat database). They are counted under each soldier on the HD screen, with +1 PRISONER for each one freed. The demos free prisoners too.
- The score of each soldier sits in the middle of its band on the Metal Slug HD screen, it touched the line under J1 or J2.
- The credits on the Metal Slug HD screen are bigger and brighter, in a dark pill with a gold edge, beside a coin struck with the symbol of `config.json` (€, $, £ or a plain coin) instead of a star. A coin put in falls onto it, and two coins at once give one +2 CREDITS.
- On the HD screens, a number that grows for a moment (Metal Slug's score and ammo, a timer under 10 seconds) keeps its digits together. They moved apart.
- Player 2 of the first Metal Slug shows his weapon, his ammo and his bombs (cheat database), and his score, learned on a cabinet. The score of each player is read where the game keeps it, one digit per byte. The place found by `learn.bat` until now holds the score of the last player who scored, so player 1's changed whenever player 2 scored.
- Metal Slug X, 3, 4 and 5 read their mission, Metal Slug X its timer too (cheat database). Their backdrops change with the missions, with MISSION COMPLETE in between, like in the first two.
- An address learned with `learn.bat` that the game's file rules out is removed from `learned` when ArcadeDMD starts, and `learn.bat` leaves it aside (Metal Slug's score).
- Twinkle Star Sprites shows the right hearts. They are the energy of the game, eight for a heart (cheat database, checked in captures made on a cabinet), the value read until now stayed at 3. It also reads the score of both players, the stage against the computer and the chain of each player (the N HIT of the game), learned on a cabinet.
- `learn.bat` finds a stage, a mission or a round that the game keeps from 0 (0 for stage 1), and saves it with +1. A chain (`hits=4`) is looked for as a short counter, no longer as a hiscore. Something on or off typed 1 or 0 (`perfect=1`) is also found when the game keeps a timer there instead of a 1, and read 0 or 1. In Twinkle Star Sprites it found four BCD bytes, wrong from 10 HIT on, and that address is removed from `learned` when ArcadeDMD starts.
- A new HD scene for Twinkle Star Sprites, livelier and readable from afar. The character's name in big letters on a plate in its colours, the score, five big hearts with the half ones, POW 1 2 MAX in three blocks and the bombs. The box of the column shows VERSUS and VS between two players, and STAGE with its number against the computer, whose side shows its character, its hearts and its bombs, with PRESS START in place of its score. Big moments for what the game does. The chain the game counts (N HIT), the fireballs of an attack cross the column and land with LV1 or LV2 ATTACK, a charged shot leaves as a beam of light (LV 1, LV 2, MAX !), a bomb rumbles the whole screen three times, flashes it white then gold, turns giant rays of light over it, sends three shockwaves across both fields and the column and a shower of stars over them, with BOMB ! bouncing in, a boss attack darkens the other field under BOSS ATTACK !, a heart breaks or fills up, and the last one gives K.O. and WIN ! with fireworks. The game's PERFECT, a formation of puffballs cleared in one chain, shows PERFECT ! in big letters on that side, for player 1 as for player 2 or the computer (learned on a cabinet).
- The credits of a Neo Geo under RetroArch, guessed from its BIOS, start from those left the last time the game was quit. FinalBurn Neo keeps them in the game's backup memory and gives them back, ArcadeDMD guessed only one. Metal Slug showed one credit less than the game on a cabinet. The guess is no longer lost either when the game comes back after RetroArch's menu was open a while.

**Documentation**
- The README opens on The King of Fighters '98, Twinkle Star Sprites and Metal Slug on the HD screen, and its tables say what each Metal Slug and Twinkle Star Sprites read under RetroArch.

**Updating from 1.30.0**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept). Then run `coin_buttons.bat` once more and press the left coin button, the right one, then START for player 1 and START for player 2.

### Français

**Les boutons START**
- `coin_buttons.bat` demande maintenant aussi le bouton START de chaque joueur. Dans un jeu qui ne donne pas ses crédits (la plupart des jeux Capcom sous RetroArch, Mercs, Final Fight, Street Fighter II', les Alpha...), un joueur qui appuie sur START avec un crédit commence tout de suite. Le jeu s'affiche dès l'écran de sélection ou l'intro, PRESS START n'attend plus que le joueur ait le contrôle. Le joueur 2 qui appuie sur START prend aussi son crédit, un challenger dans un jeu de combat compris. Rien n'est compté pour un START appuyé sans crédit, en pleine partie ou dans le menu de RetroArch.
- Les boutons des pièces comptent les appuis rapides, une pièce chacun, comme RetroArch. Un appui moins de 0,15 s après le précédent était pris pour un rebond, et les crédits d'une Neo Geo prenaient du retard sur ceux du jeu. Un rebond est maintenant un contact de moins de 30 ms juste après avoir lâché le bouton.

**Jeux Capcom**
- Le joueur 2 des jeux de combat. PRESS START et CPU restaient affichés de son côté même quand un deuxième joueur arrivait. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 et JoJo's Bizarre Adventure lisent qui dirige chaque combattant, un humain ou l'ordinateur (base de triche), Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter et X-Men: Children of the Atom aussi (trouvé dans des captures faites sur une borne). Dans les autres jeux de combat, le joueur 2 est vu quand il arrive, son score qui monte une fois appris, son START avec un crédit, ou un crédit dépensé en plein combat (un challenger). Il repart quand plus personne ne joue, ou deux minutes après que son score a cessé de bouger.
- Le joueur 2 qui joue seul contre l'ordinateur. Le joueur 1 s'affiche CPU, avec PRESS START ou INSERT COIN au-dessus, et son score n'est plus celui de l'ordinateur. Les jeux ci-dessus le lisent, les autres le voient au START du joueur 2 suivi d'un crédit que le jeu dépense. Le joueur 1 qui arrive ensuite rejoue.
- Dans les jeux Marvel (X-Men: Children of the Atom, Marvel Super Heroes et les trois « vs. ») l'ordinateur marque aussi des points. Un score qui monte ne fait plus du joueur 2 un humain dans ces jeux.
- Hyper Street Fighter II, Marvel vs. Capcom, X-Men: Children of the Atom, Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter lisent le score de chaque joueur, appris sur une borne.
- La jauge de super de Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter et X-Men: Children of the Atom marche comme celle du jeu. La barre du niveau en cours, avec POWER 1, 2 ou 3 à côté, et POWER MAX au niveau le plus haut. Elle montrait le niveau en tiers de barre, et celle de X-Men restait vide au Level 1.
- Marvel vs. Capcom lit ses crédits, appris sur une borne. Deux pièces pour un crédit sont bien comptées.
- Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter donnent à chaque joueur deux combattants qui se relaient. La vie et le nom affichés sont ceux du combattant à l'écran, et un partenaire qui prend la suite n'est plus un K.O. Deux barres vides et un DOUBLE K.O. arrivaient en plein combat.
- Un jeu qui vide ses deux combattants (l'écran de sélection après START, la fin d'une partie) n'affiche plus de DOUBLE K.O., ni KO au milieu de l'écran HD et sur la dalle, dans tous les jeux de combat. X-Men: Children of the Atom en montrait un à chaque START.
- La partie vide des barres de vie sur l'écran HD est gris foncé au lieu de rouge foncé, dans tous les jeux de combat. Une barre presque vide paraissait pleine et rouge sur la borne (X-Men: Children of the Atom).
- X-Men: Children of the Atom lit les rounds gagnés par chaque joueur, les S sous les portraits du jeu (trouvé dans des captures faites sur une borne). Le gagnant d'un round s'affiche même quand une barre n'est pas tout à fait vide.
- Night Warriors lit les rounds gagnés par chaque joueur (base de triche). Des étoiles dorées sous les barres sur l'écran HD, des carrés dorés à côté du chrono sur la dalle, et le vainqueur de chaque round d'après eux.
- La vie de Magic Sword, Willow et Tenchi wo Kurau II se lit vide quand elle passe sous zéro, comme dans les autres jeux Capcom depuis la 1.30.0.
- Une version dont les propres codes de triche mettent ses valeurs ailleurs les lit là. La deuxième révision de JoJo's Venture (toutes ses valeurs), la réédition japonaise de Quiz & Dragons (les vies) et Eco Fighters américain (les crédits) lisaient jusqu'ici les adresses de leur jeu d'origine.

**Neo Geo**
- Metal Slug montre son char sur l'écran HD. Dans le char, il prend la place de l'arme, avec son énergie en coups (trois, comme dans le jeu) et ses obus. Un coup reçu fait clignoter la case perdue, un obus part vers le décor, ÉJECTE-TOI ! clignote quand il n'a plus d'énergie, et le char détruit explose. La démo monte aussi dans le char, et ton propre dessin du char peut prendre la place de celui d'ArcadeDMD (`sprites\mslug_tank_hd.png`). Un fond uni autour de lui devient transparent, ses marges vides sont coupées, il se place au milieu du cadre de la carte et les obus partent de son canon. Savoir si le joueur est dedans a été trouvé dans des captures faites sur une borne. L'énergie et les obus sont ceux du char lui-même (base de triche), justes dès que le joueur monte dedans.
- Les prisonniers libérés du premier Metal Slug (trouvés dans des captures faites sur une borne), de Metal Slug X, du joueur 2 dans Metal Slug 3 et de Metal Slug 5 (base de triche). Ils sont comptés sous chaque soldat sur l'écran HD, avec +1 PRISONNIER à chaque libération. Les démos en libèrent aussi.
- Le score de chaque soldat est au milieu de sa bande sur l'écran HD de Metal Slug, il touchait le trait sous J1 ou J2.
- Les crédits sur l'écran HD de Metal Slug sont plus gros et plus clairs, dans une pastille sombre au bord doré, à côté d'une pièce frappée du symbole de `config.json` (€, $, £ ou une pièce unie) au lieu d'une étoile. Une pièce mise tombe dessus, et deux pièces d'un coup donnent un seul +2 CRÉDITS.
- Sur les écrans HD, un nombre qui grossit un instant (le score et les munitions de Metal Slug, un chrono sous 10 secondes) garde ses chiffres serrés. Ils s'écartaient.
- Le joueur 2 du premier Metal Slug montre son arme, ses munitions et ses bombes (base de triche), et son score, appris sur une borne. Le score de chaque joueur se lit là où le jeu le garde, un chiffre par octet. La place trouvée jusqu'ici par `learn.bat` garde le score du dernier joueur qui a marqué, celui du joueur 1 changeait donc dès que le joueur 2 marquait.
- Metal Slug X, 3, 4 et 5 lisent leur mission, Metal Slug X son chrono aussi (base de triche). Leurs décors changent avec les missions, avec MISSION COMPLETE entre les deux, comme dans les deux premiers.
- Une adresse apprise avec `learn.bat` que le fichier du jeu écarte est retirée de `learned` au démarrage d'ArcadeDMD, et `learn.bat` la laisse de côté (le score de Metal Slug).
- Twinkle Star Sprites montre les bons cœurs. Ce sont l'énergie du jeu, huit pour un cœur (base de triche, vérifié dans des captures faites sur une borne), la valeur lue jusqu'ici restait à 3. Il lit aussi le score des deux joueurs, l'étape contre l'ordinateur et la chaîne de chaque joueur (le N HIT du jeu), appris sur une borne.
- `learn.bat` trouve une étape, une mission ou un round que le jeu garde à partir de 0 (0 pour l'étape 1), et l'enregistre avec +1. Une chaîne (`hits=4`) est cherchée comme un petit compteur, plus comme un hiscore. Ce qui est allumé ou éteint, tapé 1 ou 0 (`perfect=1`), est aussi trouvé quand le jeu y garde un compte à rebours au lieu d'un 1, et lu 0 ou 1. Dans Twinkle Star Sprites il trouvait quatre octets BCD, faux dès 10 HIT, et cette adresse est retirée de `learned` au démarrage d'ArcadeDMD.
- Une nouvelle scène HD pour Twinkle Star Sprites, plus vivante et lisible de loin. Le nom du personnage en grand sur une plaque à ses couleurs, le score, cinq gros cœurs avec les demi-cœurs, POW 1 2 MAX en trois blocs et les bombes. Le cadre de la colonne affiche VERSUS et VS à deux, et STAGE avec son numéro contre l'ordinateur, dont le côté montre son personnage, ses cœurs et ses bombes, avec PRESS START à la place de son score. De grands moments pour ce que fait le jeu. La chaîne que compte le jeu (N HIT), les boules de feu d'une attaque traversent la colonne et arrivent avec LV1 ou LV2 ATTACK, un tir chargé part en rayon de lumière (LV 1, LV 2, MAX !), une bombe fait gronder tout l'écran trois fois, le fait flasher en blanc puis en or, fait tourner de grands rayons de lumière dessus, envoie trois ondes de choc à travers les deux terrains et la colonne et une pluie d'étoiles dessus, avec BOMB ! qui rebondit, une attaque de boss assombrit l'autre terrain sous BOSS ATTACK !, un cœur éclate ou se remplit, et le dernier donne K.O. et WIN ! avec un feu d'artifice. Le PERFECT du jeu, un groupe de boules balayé d'une seule chaîne, affiche PERFECT ! en grand de ce côté, pour le joueur 1 comme pour le joueur 2 ou l'ordinateur (appris sur une borne).
- Les crédits d'une Neo Geo sous RetroArch, devinés d'après son BIOS, repartent de ceux qui restaient la dernière fois qu'on a quitté le jeu. FinalBurn Neo les garde dans la mémoire de sauvegarde du jeu et les rend, ArcadeDMD n'en devinait qu'un. Metal Slug affichait un crédit de moins que le jeu sur une borne. La devinette n'est plus perdue non plus quand le jeu revient après un moment dans le menu de RetroArch.

**Documentation**
- Le README s'ouvre sur The King of Fighters '98, Twinkle Star Sprites et Metal Slug sur l'écran HD, et ses tableaux disent ce que lisent chaque Metal Slug et Twinkle Star Sprites sous RetroArch.

**Mettre à jour depuis la 1.30.0**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés). Relance ensuite une fois `coin_buttons.bat` et appuie sur le bouton des pièces de gauche, celui de droite, puis sur START du joueur 1 et START du joueur 2.

## 1.30.0

### English

**Every Capcom CPS1, CPS2 and CPS3 game**
- Every Capcom CPS1, CPS2 and CPS3 game of FinalBurn Neo is recognized, with MAME as with RetroArch. That makes 88 games and their 942 sets. A version, a bootleg or a hack takes the file of its original game, with its own name when it has one.
- The values of the cheat database of FinalBurn Neo are read, each player's health, the timer, the lives, the bombs, the super gauge, the characters and their names, the stage, and the credits when the game keeps them. The timer shows when the cheat gives all of it. In 23 games it only gives a part (one digit, the seconds of a clock, a counter that is not the timer seen in the game), ArcadeDMD then reads it only to see that the game runs. The RAM of the CPS3, whose bytes are reversed in 32-bit words, is put back in order.
- The Capcom games have no BIOS that tells who plays. ArcadeDMD watches the timer, the score once it is learned, and the health in the fighting games. As long as they move, player 1 plays, and after 10 seconds without any change the coin screen comes back. Without them, the game stays on its game scene. When the game's credits are read, a credit spent is a start, player 1 plays from the select screen on.
- `demo_capcom.bat` plays the demo of a Capcom game, most of them with the coin screen first.

**The Capcom fighting games**
- 22 fighting games read their stage. The HD screen shows it, with the place under the stage banner (CHINA, INDIA, FEAST OF THE DAMNED...).
- Eight new fight stages drawn by the program. A castle roof in Japan at night, a Chinese street market, a steel factory, a gothic manor under the moon, an Indian palace at sunset, a golden temple on its river, a laboratory and an air base at dusk.
- The super gauges, on the bottom line of the panel and under the fighters on the HD screen. Blue as they fill up, gold with MAX when they are full.
- Street Fighter III: New Generation names its fighters.
- Street Fighter II, Champion Edition, Hyper Fighting, Super Street Fighter II and Street Fighter Alpha read the rounds won by each player. Gold stars under the bars on the HD screen, gold squares next to the timer on the panel, and the winner of each round from them. In Street Fighter II the health goes below zero at a K.O. and read full, the K.O. was missed and the WIN went to the wrong fighter. A bar below zero now reads empty, in every Capcom game. Street Fighter II also reads its credits and the score, learned on a cabinet. A credit spent switches to the game at the character select, PRESS START no longer stays on.

**The Capcom games done one by one**
- Fifty Capcom games get a panel scene and an animated HD scene of their own, drawn by the program.
- The 23 games with characters show like Metal Slug on the HD screen, with no character drawn by the program. The beat'em ups (Final Fight, Captain Commando, Cadillacs and Dinosaurs, The Punisher, The King of Dragons, Knights of the Round, Warriors of Fate, the two Dungeons & Dragons, Alien vs. Predator, Armored Warriors, Battle Circuit), the action games and platformers (Ghouls'n Ghosts, Strider, Mega Twins, Magic Sword, Willow, Nemo, Three Wonders, Dynasty Wars), the two Pang and Mercs. The place of the game stays behind, calm and darker, each player has a panel with what is read in the game (gauge, lives, score, bombs, weapon, level), and the middle shows the logo, the timer when it is read whole, and the credits. The game's events show between the panels. Points are a punch, a shot, a slash, a thrown weapon, a spell or a balloon that bursts, a bomb or a special leaves the panel and the middle blows up, a life lost turns the panel red. Player 2's panel lights up when his values move.
- The shoot'em ups (1944, 19XX, 1941, Varth, U.N. Squadron, Carrier Air Wing, Forgotten Worlds, Giga Wing, Progear, Mars Matrix, Dimahoo, Eco Fighters, Mercs). Once the score is learned, the enemies blow up when the game scores points, a bomb sweeps the screen, the weapon picked up and the plane chosen are named, and on the panel the plane of the game flies and fires.
- The puzzle games and quizzes (Super Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons, Adventure Quiz Capcom World 2) play by themselves with our own gems, balls, questions and players.
- Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou, Gulun.Pa!, Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin and Ganbare! Marine Kun get theirs too.
- Final Fight Anniversary Edition, Final Fight EX and Tenchi wo Kurau II CPS Changer take the scene of their game.

**Credits and coins**
- Under RetroArch most Capcom games do not give their credits. With the coin buttons shown by `coin_buttons.bat`, ArcadeDMD counts them. A coin gives a credit and a player who begins takes one, at the start, at a continue (lives back from 0, or the energy in Mercs) and when player 2 joins in (his values start moving). For an exact count, `learn.bat` can find where the game keeps them.
- 1944 and Dimahoo keep all their values outside of the memory RetroArch shares. The log says so, launch them with MAME to see everything.
- Super Puzzle Fighter II Turbo no longer draws two little fighters, the counter gems fly across to the other well and the names read in the game show in the middle.
- 1944 on the HD screen takes the icons of the game. The bombs as B medals, the side fighters in stock in their frame with their number, the gold crystals picked up, POW in yellow. The side fighters fly at our plane's sides, a bomb is a salvo of missiles, and a big WARNING announces the boss once its address is found.
- The MAME plugin no longer opens an error window (CPU not found) when MAME starts on its own game list, and no longer sends a game start for it.

**HD screen**
- The animated backdrops are a little darker so that the information stands out (`"dim"` in the `preview` section, 30 percent by default, 0 to 80).
- The credits of the fighting games are bigger, on a dark pill.

**Also**
- Player 2 shows in the Capcom shoot'em ups when his values move, his score that goes up, a life or a bomb spent, a hit taken. He stayed on PRESS START, these games have no BIOS that tells who plays. Giga Wing also reads the bombs and the power of player 2, and its score and credits learned on a cabinet. The credits show under the logo during a game.
- Mercs reads its timer whole, three digits where only the last one was read (TIME 7), the score of both players learned on a cabinet, the mega crashes of player 2, which leave his panel too, and the weapon of each player, named next to his badge with its power-ups (assault rifle, flamethrower, shotgun, grenade launcher), and the mission, MISSION 1 COMPLETE! when the next one starts. FinalBurn Neo sets it for three players, the README tells how to set it for two (DIP switches).
- The HD screen gave the Metal Slug scene to Marvel Super Heroes and Magic Sword, their names start like Metal Slug's. Only the Metal Slug games get it now.

**Updating from 1.29.3**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Tous les jeux Capcom CPS1, CPS2 et CPS3**
- Chaque jeu Capcom CPS1, CPS2 et CPS3 de FinalBurn Neo est reconnu, avec MAME comme avec RetroArch. Ça fait 88 jeux et leurs 942 sets. Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, avec son propre nom quand il en a un.
- Ce qu'écrit la base de codes de triche de FinalBurn Neo est lu. La vie de chaque joueur, le chrono, les vies, les bombes, la jauge de super, les personnages et leur nom, le décor, et les crédits quand le jeu les garde. Le chrono s'affiche quand la triche le donne en entier. Dans 23 jeux elle n'en donne qu'une partie (un chiffre, les secondes d'une horloge, un compteur qui n'est pas le chrono vu dans le jeu), ArcadeDMD ne le lit alors que pour voir que le jeu tourne. La RAM du CPS3, dont les octets sont inversés par mots de 32 bits, est remise dans l'ordre.
- Les jeux Capcom n'ont pas de BIOS qui dit qui joue. ArcadeDMD surveille le chrono, le score une fois appris, et la vie dans les jeux de combat. Tant qu'ils bougent, le joueur 1 joue, et au bout de 10 secondes sans le moindre changement l'écran des pièces revient. Sans eux, le jeu reste sur sa scène de jeu. Quand les crédits du jeu sont lus, un crédit dépensé est un départ, le joueur 1 joue dès l'écran de sélection.
- `demo_capcom.bat` lance la démo d'un jeu Capcom, la plupart avec l'écran des pièces d'abord.

**Les jeux de combat Capcom**
- 22 jeux de combat lisent leur décor. L'écran HD le montre, avec le lieu sous le bandeau du décor (CHINE, INDE, FEAST OF THE DAMNED...).
- Huit nouveaux décors de combat dessinés par le programme. Un toit de château au Japon la nuit, un marché chinois, une aciérie, un manoir gothique sous la lune, un palais indien au couchant, un temple d'or au bord de son fleuve, un laboratoire et une base aérienne au crépuscule.
- Les jauges de super, sur la ligne du bas de la dalle et sous les combattants sur l'écran HD. Bleues quand elles se remplissent, dorées avec MAX quand elles sont pleines.
- Street Fighter III: New Generation donne le nom de ses combattants.
- Street Fighter II, Champion Edition, Hyper Fighting, Super Street Fighter II et Street Fighter Alpha lisent les rounds gagnés par chaque joueur. Des étoiles dorées sous les barres sur l'écran HD, des carrés dorés à côté du chrono sur la dalle, et le vainqueur de chaque round d'après eux. Dans Street Fighter II la vie passe sous zéro au K.O. et se lisait pleine, le K.O. était raté et le WIN allait au mauvais combattant. Une barre sous zéro se lit maintenant vide, dans tous les jeux Capcom. Street Fighter II lit aussi ses crédits et le score, appris sur une borne. Un crédit dépensé passe au jeu dès la sélection des personnages, PRESS START ne reste plus affiché.

**Les jeux Capcom faits un par un**
- Cinquante jeux Capcom ont une scène de dalle et une scène HD animée à leur image, dessinées par le programme.
- Les 23 jeux à personnages s'affichent façon Metal Slug sur l'écran HD, sans personnage dessiné par le programme. Les beat'em up (Final Fight, Captain Commando, Cadillacs and Dinosaurs, The Punisher, The King of Dragons, Knights of the Round, Warriors of Fate, les deux Dungeons & Dragons, Alien vs. Predator, Armored Warriors, Battle Circuit), les jeux d'action et de plateformes (Ghouls'n Ghosts, Strider, Mega Twins, Magic Sword, Willow, Nemo, Three Wonders, Dynasty Wars), les deux Pang et Mercs. Le décor du jeu reste derrière, calme et plus sombre, chaque joueur a un panneau avec ce qui est lu dans le jeu (jauge, vies, score, bombes, arme, niveau), et le milieu montre le logo, le chrono quand il est lu en entier, et les crédits. Les événements du jeu se voient entre les panneaux. Des points font un coup de poing, un tir, une entaille, une arme lancée, un sort ou un ballon qui éclate, une bombe ou un coup spécial part du panneau et le milieu explose, une vie perdue fait rougir le panneau. Le panneau du joueur 2 s'allume quand ses valeurs bougent.
- Les shoot'em up (1944, 19XX, 1941, Varth, U.N. Squadron, Carrier Air Wing, Forgotten Worlds, Giga Wing, Progear, Mars Matrix, Dimahoo, Eco Fighters, Mercs). Une fois le score appris, les ennemis explosent quand le jeu marque des points, une bombe balaie l'écran, l'arme ramassée et l'avion choisi sont nommés, et sur la dalle l'avion du jeu vole et tire.
- Les jeux de réflexion et les quiz (Super Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons, Adventure Quiz Capcom World 2) jouent tout seuls avec nos propres gemmes, billes, questions et joueurs.
- Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou, Gulun.Pa!, Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin et Ganbare! Marine Kun ont aussi les leurs.
- Final Fight Anniversary Edition, Final Fight EX et Tenchi wo Kurau II CPS Changer prennent la scène de leur jeu.

**Crédits et pièces**
- Sous RetroArch la plupart des jeux Capcom ne donnent pas leurs crédits. Avec les boutons des pièces montrés par `coin_buttons.bat`, ArcadeDMD les compte. Une pièce donne un crédit et un joueur qui commence en prend un, au départ, à un continue (les vies qui reviennent de 0, ou l'énergie dans Mercs) et quand le joueur 2 arrive (ses valeurs se mettent à bouger). Pour un compte exact, `learn.bat` peut trouver où le jeu les garde.
- 1944 et Dimahoo gardent toutes leurs valeurs hors de la mémoire que RetroArch partage. Le journal le dit, lance-les avec MAME pour tout voir.
- Super Puzzle Fighter II Turbo ne dessine plus deux petits combattants, les gemmes à compteur volent vers l'autre puits et les noms lus dans le jeu s'affichent au milieu.
- 1944 prend les icônes du jeu sur l'écran HD. Les bombes en médailles B, l'escorte en réserve dans son cadre avec son nombre, les cristaux d'or ramassés, POW en jaune. Les chasseurs d'escorte volent à côté de notre avion, une bombe est une salve de missiles, et un grand WARNING annonce le boss une fois son adresse trouvée.
- Le plugin MAME n'ouvre plus de fenêtre d'erreur (CPU introuvable) quand MAME démarre sur sa liste de jeux, et n'envoie plus de départ de partie pour elle.

**Écran HD**
- Les décors animés sont un peu assombris pour que les infos ressortent (`"dim"` dans la section `preview`, 30 % par défaut, de 0 à 80).
- Les crédits des jeux de combat sont plus gros, sur une pastille sombre.

**Aussi**
- Le joueur 2 apparaît dans les shoot'em up Capcom quand ses valeurs bougent, son score qui monte, une vie ou une bombe en moins, un coup reçu. Il restait sur PRESS START, ces jeux n'ont pas de BIOS qui dit qui joue. Giga Wing lit aussi les bombes et la puissance du joueur 2, et son score et ses crédits appris sur une borne. Les crédits s'affichent sous le logo pendant la partie.
- Mercs lit son chrono en entier, trois chiffres dont seul le dernier était lu (TIME 7), le score des deux joueurs appris sur une borne, les méga attaques du joueur 2, qui partent aussi de son panneau, et l'arme de chaque joueur, nommée à côté de son badge avec ses POW (fusil d'assaut, lance-flammes, fusil à pompe, lance-grenades), et la mission, MISSION 1 ACCOMPLIE ! quand la suivante commence. FinalBurn Neo le règle pour trois joueurs, le README dit comment le régler pour deux (DIP switches).
- L'écran HD donnait la scène de Metal Slug à Marvel Super Heroes et à Magic Sword, leur nom commence comme celui de Metal Slug. Seuls les Metal Slug l'ont maintenant.

**Mettre à jour depuis la 1.29.3**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.3

### English

**Every Neo Geo game with RetroArch**
- Every Neo Geo set of FinalBurn Neo is recognized (693 of them). A version, a bootleg or a hack takes the file of its original game, as with MAME. Metal Slug 3 Fully Decrypted plays like Metal Slug 3, and KOF 2002 Magic Plus like KOF 2002 with its own name at the top. A homebrew game gets the scene of its genre, and so does Treasure of the Caribbean, the last official game that was missing. Only the BIOS and the test programs are left out.
- `test_retroarch.bat` tells which game a version takes the file of.
- On the HD screen, each coin door says what a coin gives. On a Neo Geo MVS, the right one says 2 CREDITS, like the machine.

**Updating from 1.29.2**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Tous les jeux Neo Geo avec RetroArch**
- Chaque set Neo Geo de FinalBurn Neo est reconnu (693 en tout). Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, comme avec MAME. Metal Slug 3 Fully Decrypted se joue comme Metal Slug 3, et KOF 2002 Magic Plus comme KOF 2002 avec son propre nom en haut. Un jeu amateur (homebrew) a la scène de son genre, tout comme Treasure of the Caribbean, le dernier jeu officiel qui manquait. Seuls le BIOS et les programmes de test sont laissés de côté.
- `test_retroarch.bat` dit de quel jeu une version prend le fichier.
- Sur l'écran HD, chaque monnayeur dit ce que donne une pièce. Sur une Neo Geo MVS, celui de droite affiche 2 CRÉDITS, comme la machine.

**Mettre à jour depuis la 1.29.2**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.2

### English

**Every coin and its side, with RetroArch**
- `coin_buttons.bat` shows ArcadeDMD your two coin buttons, on the controllers or the keyboard. ArcadeDMD then reads them itself, at the same time as RetroArch and without taking them from it. Every coin is seen with its side, during a game too, and on the HD screen the coin drops in the slot on the side where you put it. Windows only.
- An MVS gives 2 credits for a coin in its second slot when its settings were not changed. ArcadeDMD counts the same way (`"mvs_credits": [1, 2]` in the `coin_buttons` section of `config.json`).
- Without the buttons, the BIOS now also shows the first coin put in during a game.
- `test_coins.bat` also writes down each press on the coin buttons.

**Updating from 1.29.1**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept). Then run `coin_buttons.bat` once.

### Français

**Chaque pièce et son côté, avec RetroArch**
- `coin_buttons.bat` montre à ArcadeDMD tes deux boutons de pièce, sur les manettes ou le clavier. ArcadeDMD les lit alors lui-même, en même temps que RetroArch et sans les lui prendre. Chaque pièce est vue avec son côté, même en pleine partie, et sur l'écran HD la pièce tombe dans le monnayeur du côté où tu l'as mise. Seulement sous Windows.
- Une MVS donne 2 crédits pour une pièce dans son deuxième monnayeur quand ses réglages n'ont pas été changés. ArcadeDMD compte pareil (`"mvs_credits": [1, 2]` dans la rubrique `coin_buttons` de `config.json`).
- Sans les boutons, le BIOS montre maintenant aussi la première pièce mise en pleine partie.
- `test_coins.bat` note aussi chaque appui sur les boutons des pièces.

**Mettre à jour depuis la 1.29.1**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés). Lance ensuite une fois `coin_buttons.bat`.

## 1.29.1

### English

**Fixes from the cabinet**
- Fighting games. The timer sits right between its two lines, with the same gap on each side. The line on the left touched the digits.
- Only the name of the game on the panel, without the maker (SNK, VIDEO SYSTEM...), on the coin screen and at the top during a game. A title that fits stays still instead of scrolling.
- With RetroArch, the HD screen no longer drops the coins once on the right, once on the left. RetroArch does not tell which coin slot a coin came through, so the coin drops in player 1's slot when nobody plays, in the slot of the player who comes in during a game, and in the slot of the player at the CONTINUE.
- `test_coins.bat` writes down what the Neo Geo BIOS does when a coin goes in with RetroArch, to find out on a real cabinet how to see every coin and its side. The result goes to `runtime\test_coins.txt`.

**Updating from 1.29**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Corrections vues sur la borne**
- Jeux de combat. Le chrono est pile entre ses deux traits, avec le même espace de chaque côté. Le trait de gauche touchait les chiffres.
- Seulement le nom du jeu sur la dalle, sans le fabricant (SNK, VIDEO SYSTEM...), sur l'écran des pièces et en haut pendant la partie. Un titre qui tient reste fixe au lieu de défiler.
- Avec RetroArch, l'écran HD ne fait plus tomber les pièces une fois à droite, une fois à gauche. RetroArch ne dit pas par quel monnayeur une pièce est passée, alors la pièce tombe dans le monnayeur du joueur 1 quand personne ne joue, dans celui du joueur qui arrive pendant une partie, et dans celui du joueur au CONTINUE.
- `test_coins.bat` note ce que fait le BIOS de la Neo Geo quand une pièce entre avec RetroArch, pour trouver sur une vraie borne comment voir chaque pièce et son côté. Le résultat va dans `runtime\test_coins.txt`.

**Mettre à jour depuis la 1.29**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.0

### English

**A simpler panel for the shoot'em ups**
- During a game, the panel of the fifteen Neo Geo shoot'em ups only shows the score in big digits in the middle (or the title of the game as long as the score has not been learned), your lives at the bottom left (a plane and x2) and your bombs at the bottom right. The title no longer scrolls during a game, the credits and INSERT COIN are gone, as are the power gauge and the scenery.
- Between them flies your ship. It follows your stick and fires while you hold the fire button, read in the Neo Geo BIOS with MAME as with RetroArch, and flies by itself until you touch them. With two players, both ships face to face.
- Everything else takes the panel for a moment, one thing at a time, as on a pinball. BOMB! and its explosions, POWER UP then MAX POWER, the plane that blows up and the lives left, LAST LIFE, 1UP, ROUND 2 or STAGE 2, SPEED UP, the SUPER SHOT of Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 and PLAYER 2, and CREDIT 1 when a coin goes in during a game. A more important event replaces the one playing (GAME OVER over a life lost), a less important one waits its turn.
- Each enemy destroyed in the game blows up ahead of your ship, a big one for a big enemy. As long as the score has not been learned, an enemy blows up ahead of it now and then while it fires, as on the HD screen. Your own animations in the `artwork` folder still come first, and `artwork\ship.gif` (or `artwork\<game>\ship.gif`) replaces the ship.
- A value that the game has not set yet (the lives during the choice of the plane) is not shown.
- Three new panel layers, `events` (short events, one at a time), `counter` (a small drawing followed by a number) and `ship` (the ship that follows the stick).

**The panel looks like the preview**
- LEDs light up in proportion to the value they get, so the dark grays of the scenes glowed on the Pixelcade and made them look busy. ArcadeDMD now corrects the colors it sends to the Pixelcade (`"gamma": 2.2` in the `pixelcade` section, `1.0` sends them as they are).

**The coin drops with RetroArch too**
- The FinalBurn Neo core of RetroArch does not share the memory where an MVS keeps its credits, so the coin never dropped. ArcadeDMD now guesses the credits from the Neo Geo BIOS. A coin put in while nobody plays drops on the panel and the HD screen, PRESS START follows, and each player who starts takes a credit. A coin put in during a game is not seen. FinalBurn Neo must be in MVS mode, and `runtime\arcadedmd.log` tells what the BIOS did. With MAME, the real credits are still read.

**Fixes**
- In the Neo Geo games whose score has not been learned, the title that scrolls at the top no longer runs into INSERT COIN.

**Updating from 1.28**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Une dalle plus simple pour les shoot'em up**
- Pendant la partie, la dalle des quinze shoot'em up Neo Geo ne montre plus que le score en gros au milieu (ou le titre du jeu tant que le score n'est pas appris), tes vies en bas à gauche (un avion et x2) et tes bombes en bas à droite. Le titre ne défile plus pendant la partie, les crédits et INSERT COIN disparaissent, comme la jauge de puissance et le décor.
- Entre les deux vole ton vaisseau. Il suit ton stick et tire tant que tu tiens le bouton de tir, lus dans le BIOS de la Neo Geo avec MAME comme avec RetroArch, et vole tout seul tant que tu n'y as pas touché. À deux, les deux vaisseaux face à face.
- Tout le reste prend la dalle un instant, une chose à la fois, comme sur un flipper. BOMBE! et ses explosions, POWER UP puis MAX POWER, l'avion qui explose et les vies qui restent, LAST LIFE, 1UP, ROUND 2 ou STAGE 2, SPEED UP, le SUPER SHOT de Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 et PLAYER 2, et CRÉDIT 1 quand une pièce entre en pleine partie. Un événement plus important remplace celui en cours (GAME OVER par-dessus une vie perdue), un moins important attend son tour.
- Chaque ennemi détruit dans le jeu explose devant ton vaisseau, une grosse explosion pour un gros ennemi. Tant que le score n'est pas appris, un ennemi explose devant lui de temps en temps pendant qu'il tire, comme sur l'écran HD. Tes propres animations du dossier `artwork` passent toujours en premier, et `artwork\ship.gif` (ou `artwork\<jeu>\ship.gif`) remplace le vaisseau.
- Une valeur que le jeu n'a pas encore posée (les vies pendant le choix de l'avion) ne s'affiche pas.
- Trois nouvelles couches de dalle, `events` (des événements courts, un à la fois), `counter` (un petit dessin suivi d'un nombre) et `ship` (le vaisseau qui suit le stick).

**La dalle ressemble à l'aperçu**
- Les LED éclairent en proportion de la valeur reçue, donc les gris sombres des scènes brillaient sur la Pixelcade et les rendaient chargées. ArcadeDMD corrige maintenant les couleurs qu'il envoie à la Pixelcade (`"gamma": 2.2` dans la section `pixelcade`, `1.0` les envoie telles quelles).

**La pièce tombe aussi avec RetroArch**
- Le cœur FinalBurn Neo de RetroArch ne partage pas la mémoire où la MVS range ses crédits, donc la pièce ne tombait jamais. ArcadeDMD devine maintenant les crédits d'après le BIOS de la Neo Geo. Une pièce mise quand personne ne joue tombe sur la dalle et sur l'écran HD, PRESS START suit, et chaque joueur qui commence prend un crédit. Une pièce mise en pleine partie ne se voit pas. FinalBurn Neo doit être en mode MVS, et `runtime\arcadedmd.log` dit ce que le BIOS a fait. Avec MAME, les vrais crédits sont toujours lus.

**Corrections**
- Dans les jeux Neo Geo dont le score n'est pas appris, le titre qui défile en haut ne chevauche plus INSERT COIN.

**Mettre à jour depuis la 1.28**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.28.0

### English

**The shoot'em ups follow the game more closely**
- In the fifteen Neo Geo shoot'em ups done one by one, once the score is read, the enemies of the HD screen only blow up when the game scores points. The enemy our shots are hitting goes first and its points show above it. The bigger the gain next to the usual ones, the bigger the blast, and the screen shakes for a big enemy. Our shots still hit the enemies, they flash.
- The bombs, the super shot of Strikers 1945 Plus and the charged shot of Pulstar stay weapons of the game, they destroy what they hit. The unit of Last Resort hits the enemies too, and the points decide which one blows up.
- A bonus that the game counts at the end of a stage shows as one BONUS counter instead of blowing up dozens of enemies.
- On the panel, real explosions drawn pixel by pixel. One goes off ahead of the ship at each point scored, the size and pace of the DOFLinx ones, a big fireball (or a blue plasma blast in space) for a big gain, and a row of explosions with a shock wave when a bomb goes off. The super shot of Strikers 1945 Plus and the charged shot of Pulstar have theirs too. The ship fires at each point, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger and Last Hope included.
- Your own animations (the GIFs of DOFLinx or of the Pixelcade, for example) can replace ours. They go in an `artwork` folder next to `arcadedmd.py`, which is never published and which an update never touches (`artwork\boom.gif`, `boom_big.gif`, `bomb.gif`, `shock.gif`, `super.gif`, `charge.gif`, or `artwork\<game>\` for one game). A 128 x 32 GIF plays over the whole panel, or at the place of the action when its drawing fits in the middle, like the explosions of DOFLinx.
- A new panel layer, `anim`, plays an animation once when a value of the game changes.
- The score of these games is in no database. Until it is learned with `learn.bat`, the scenes play by themselves as before.

**Updating from 1.27**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Les shoot'em up suivent mieux le jeu**
- Dans les quinze shoot'em up Neo Geo faits un par un, dès que le score est lu, les ennemis de l'écran HD n'explosent que quand le jeu marque des points. L'ennemi que nos tirs touchent part d'abord et ses points s'affichent au-dessus. Plus le gain est gros à côté des gains habituels, plus l'explosion est forte, et l'écran tremble pour un gros ennemi. Nos tirs touchent toujours les ennemis, ils clignotent.
- Les bombes, le super tir de Strikers 1945 Plus et le tir chargé de Pulstar restent des armes du jeu, ils détruisent ce qu'ils touchent. L'unité de Last Resort touche aussi les ennemis, et les points décident lequel explose.
- Un bonus compté par le jeu en fin de niveau s'affiche en un seul compteur BONUS au lieu de faire exploser des dizaines d'ennemis.
- Sur la dalle, de vraies explosions dessinées pixel par pixel. Une part devant le vaisseau à chaque point marqué, de la taille et au rythme de celles de DOFLinx, une grosse boule de feu (ou une explosion de plasma bleu dans l'espace) pour un gros gain, et une rangée d'explosions avec une onde de choc quand une bombe part. Le super tir de Strikers 1945 Plus et le tir chargé de Pulstar ont aussi la leur. Le vaisseau tire à chaque point, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger et Last Hope compris.
- Tes propres animations (les GIF de DOFLinx ou de la Pixelcade par exemple) peuvent remplacer les nôtres. Elles vont dans un dossier `artwork` à côté d'`arcadedmd.py`, jamais publié et jamais touché par une mise à jour (`artwork\boom.gif`, `boom_big.gif`, `bomb.gif`, `shock.gif`, `super.gif`, `charge.gif`, ou `artwork\<jeu>\` pour un seul jeu). Un GIF de 128 x 32 se joue sur toute la dalle, ou à l'endroit de l'action quand son dessin tient au milieu, comme les explosions de DOFLinx.
- Une nouvelle couche de dalle, `anim`, joue une animation une fois quand une valeur du jeu change.
- Le score de ces jeux n'est dans aucune base. Tant qu'il n'est pas appris avec `learn.bat`, les scènes jouent toutes seules comme avant.

**Mettre à jour depuis la 1.27**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.27.0

### English

**Neo Geo games done one by one, eleventh and last batch**
- Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 and Shougi no Tatsujin now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes ninety-seven games done one by one, every game of `PROGRESS.md`.
- Nightmare in the Dark and The Super Spy. The graveyard under a huge full moon where the monsters burn, the corridor of the building where a masked fighter faces our fists.
- The four quizzes. Their sets as in the games, the question panel and its four answers, a big circle for a right answer and a big cross for a wrong one, read from the score and the lives. The questions are our own.
- The five mahjong games and Shougi no Tatsujin. Each felt and its tile backs, our hand of thirteen tiles, RON and TSUMO, the HP of Janshin Densetsu, the die of Minasan no Okagesamadesu!, then the wooden board by the sea where each piece taken goes onto a stand.
- Fixed. A round dot of a panel scene that follows no value is now drawn (the full moon of Nightmare in the Dark, the centre circle of Battle Flip Shot around the time).
- The score of Nightmare in the Dark, The Super Spy and the four quizzes is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the ninety-seven games.

**Updating from 1.26**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, onzième et dernier lot**
- Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 et Shougi no Tatsujin ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quatre-vingt-dix-sept jeux faits un par un, tous les jeux de `PROGRESS.md`.
- Nightmare in the Dark et The Super Spy. Le cimetière sous une énorme pleine lune où les monstres brûlent, le couloir de l'immeuble où un combattant masqué fait face à nos poings.
- Les quatre quiz. Leurs décors comme dans les jeux, le panneau de la question et ses quatre réponses, un grand rond pour une bonne réponse et une grande croix pour une mauvaise, lus dans le score et les vies. Les questions sont à nous.
- Les cinq jeux de mahjong et Shougi no Tatsujin. Chaque tapis et ses dos de tuiles, notre main de treize tuiles, RON et TSUMO, les HP de Janshin Densetsu, le dé de Minasan no Okagesamadesu!, puis le plateau de bois au bord de la mer où chaque pièce prise va sur un support.
- Corrigé. Un disque d'une scène de dalle qui ne suit aucune valeur est maintenant dessiné (la pleine lune de Nightmare in the Dark, le cercle central de Battle Flip Shot autour du temps).
- Le score de Nightmare in the Dark, The Super Spy et des quatre quiz n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quatre-vingt-dix-sept jeux.

**Mettre à jour depuis la 1.26**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.26.0

### English

**Neo Geo games done one by one, tenth batch**
- Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords and Eight Man now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes eighty-five games done one by one. `PROGRESS.md` shows what comes next.
- Zintrick, Digger Man and The Irritating Maze. Jewels shaped like drops thrown up their columns, a mine where our little digger digs to each jewel while the rocks fall, a corridor of the maze where a life lost in the game is an electric shock.
- Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger and Last Hope. Space over a planet with the four weapons in their colours, the forest and its steam train seen from the sky, the sea at dusk and its iron warships, deep space and its nebulas.
- Bang Bang Busters, Crossed Swords and Eight Man. The ice world where the enemies are trapped in bubbles, a duel of knights in the forest at night with the gold and the magic read in the game, the ruined city at sunset where our fast cyborg leaves a trail of copies.
- The score of these games except The Irritating Maze is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the eighty-five games.

**Updating from 1.25**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, dixième lot**
- Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords et Eight Man ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quatre-vingt-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Zintrick, Digger Man et The Irritating Maze. Des joyaux en gouttes lancés dans leurs colonnes, une mine où notre petit mineur creuse jusqu'à chaque joyau pendant que les rochers tombent, un couloir du labyrinthe où une vie perdue dans le jeu est une décharge électrique.
- Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger et Last Hope. L'espace au-dessus d'une planète avec les quatre armes dans leurs couleurs, la forêt et son train à vapeur vus du ciel, la mer au crépuscule et ses cuirassés, l'espace profond et ses nébuleuses.
- Bang Bang Busters, Crossed Swords et Eight Man. Le monde de glace où les ennemis sont pris dans des bulles, un duel de chevaliers dans la forêt la nuit avec l'or et la magie lus dans le jeu, la ville en ruine au coucher du soleil où notre cyborg rapide laisse une traînée de copies.
- Le score de ces jeux, sauf The Irritating Maze, n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quatre-vingt-cinq jeux.

**Mettre à jour depuis la 1.25**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.25.0

### English

**Neo Geo games done one by one, ninth batch**
- Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa and Puzzled now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes seventy-five games done one by one. `PROGRESS.md` shows what comes next.
- Bang Bead and Battle Flip Shot. Two players face to face on a court seen from above, the street with its parked cars, the arena of teal metal and its targets. A 'Miracle' power spent is a shot on fire, a target hit in the game cracks.
- Over Top. The stages seen from the sky, the pine forest and the grey road, the map in its little television, the time, RANK, the speedometer and the lap time.
- Stakes Winner, Stakes Winner 2 and Jockey Grand Prix. Horse races seen from the side, a Japanese racecourse, Longchamp and its windmill, a dirt track with its odds board. The horse's qualities and POWER read in the game.
- Gururin, Ghostlop, Pochi and Nyaa and Puzzled. A board that turns a quarter, little ghosts shot up in a street at night, soft blocks with faces of cats and dogs, brick towers whose full lines leave until the balloon floats away. The next pieces read in the game where they are known.
- The score of Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa and Puzzled is in no database. Learn it with `learn.bat`. No value of Jockey Grand Prix is known yet, its races run by themselves.
- A new panel sprite, a galloping horse and its jockey.
- `demo_neogeo.bat` now offers the seventy-five games.

**Updating from 1.24**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, neuvième lot**
- Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa et Puzzled ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait soixante-quinze jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Bang Bead et Battle Flip Shot. Deux joueurs face à face sur un terrain vu du dessus, la rue et ses voitures garées, l'arène de métal bleu-vert et ses cibles. Un pouvoir 'Miracle' dépensé est un tir en feu, une cible touchée dans le jeu se fissure.
- Over Top. Les étapes vues du ciel, la forêt de pins et la route grise, la carte dans sa petite télévision, le temps, RANK, le compteur et le temps du tour.
- Stakes Winner, Stakes Winner 2 et Jockey Grand Prix. Des courses de chevaux vues de côté, un hippodrome japonais, Longchamp et son moulin, une piste en terre et son tableau des cotes. Les qualités du cheval et POWER lus dans le jeu.
- Gururin, Ghostlop, Pochi and Nyaa et Puzzled. Un plateau qui tourne d'un quart, de petits fantômes tirés dans une rue la nuit, des blocs tout doux aux têtes de chats et de chiens, des tours de briques dont les lignes pleines partent jusqu'à ce que le ballon s'envole. Les pièces suivantes lues dans le jeu quand elles sont connues.
- Le score de Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa et Puzzled n'est dans aucune base. Apprends-le avec `learn.bat`. Aucune valeur de Jockey Grand Prix n'est encore connue, ses courses vont toutes seules.
- Un nouveau sprite pour la dalle, un cheval au galop et son jockey.
- `demo_neogeo.bat` propose maintenant les soixante-quinze jeux.

**Mettre à jour depuis la 1.24**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.24.0

### English

**Neo Geo games done one by one, eighth batch**
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf and Power Spikes II now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes sixty-five games done one by one. `PROGRESS.md` shows what comes next.
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98 and Pleasure Goal. The match in the stadium with the scoreboard of each game, the round clock, the yellow numbers and the moon, the blue band, the faces of futsal. The goals and the time read in the game.
- Soccer Brawl. Football of the future at night, the players in armour, the POWER METER of each team.
- Football Frenzy. The field seen from above, two teams line up, the runner breaks through until he is tackled, the points read in the game are touchdowns.
- Baseball Stars Professional and 2020 Super Baseball. The field seen from behind home plate, the count B S O in lights, the box of the inning, the outs counted in the game.
- Top Player's Golf and Power Spikes II. The course where the ball flies to the flag at each stroke, the indoor arena where three players on each side jump and spike, a super shot is a spike on fire.
- Nothing to learn in these ten games. No value of Tecmo World Soccer '96 is known yet, its match plays by itself.
- `demo_neogeo.bat` now offers the sixty-five games.

**Updating from 1.23**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, huitième lot**
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf et Power Spikes II ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait soixante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98 et Pleasure Goal. Le match dans le stade avec le tableau de score de chaque jeu, l'horloge ronde, les chiffres jaunes et la lune, le bandeau bleu, les visages du futsal. Les buts et le temps lus dans le jeu.
- Soccer Brawl. Le football du futur la nuit, les joueurs en armure, le POWER METER de chaque équipe.
- Football Frenzy. Le terrain vu de haut, deux équipes s'alignent, le porteur file jusqu'au plaquage, les points lus dans le jeu sont des touchdowns.
- Baseball Stars Professional et 2020 Super Baseball. Le terrain vu de derrière le marbre, le compte B S O en voyants, la boîte de la manche, les retraits comptés dans le jeu.
- Top Player's Golf et Power Spikes II. Le parcours où la balle vole vers le drapeau à chaque coup, la salle où trois joueurs de chaque côté sautent et smashent, un super coup est un smash en feu.
- Rien à apprendre dans ces dix jeux. Aucune valeur de Tecmo World Soccer '96 n'est encore connue, son match se joue tout seul.
- `demo_neogeo.bat` propose maintenant les soixante-cinq jeux.

**Mettre à jour depuis la 1.23**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.23.0

### English

**Neo Geo games done one by one, seventh batch**
- Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks and Super Sidekicks 2 now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes fifty-five games done one by one. `PROGRESS.md` shows what comes next.
- Puzzle De Pon! R!. The boards and the star dial of Puzzle De Pon!, under a pink sky.
- Panic Bomber, Pop 'n Bounce and Super Bubble Pop. Fields of their own, little heads that fall and stack with bombs that blow up in a cross, soft creatures that a bouncing ball bursts, a white board seen at an angle where a little robot shoots its bubbles. The points and the power read in the game set things off.
- Spin Master and Ganryu. The desert of the pyramids where our hero throws his yo-yo, a street of old Japan at night where our swordsman fights the ninjas. The counters where each game puts them.
- Zupapa! and Neo Mr. Do!. The blue cave and its striped platforms where our little round hero boots the monsters, the field of coloured tiles where our little digger digs his tunnels and picks the cherries, EXTRA lit letter by letter.
- Super Sidekicks and Super Sidekicks 2. The match with the scoreboard of each game, the goals and the time read in the game.
- The score of Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa! and Neo Mr. Do! is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the fifty-five games.

**Updating from 1.22**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, septième lot**
- Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks et Super Sidekicks 2 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait cinquante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Puzzle De Pon! R!. Les plateaux et le cadran étoilé de Puzzle De Pon!, sous un ciel rose.
- Panic Bomber, Pop 'n Bounce et Super Bubble Pop. Des champs à eux, de petites têtes qui tombent et s'empilent avec des bombes qui sautent en croix, des créatures molles qu'une balle qui rebondit fait éclater, un plateau blanc vu de biais où un petit robot tire ses bulles. Les points et la puissance lus dans le jeu déclenchent tout ça.
- Spin Master et Ganryu. Le désert des pyramides où notre héros lance son yo-yo, une rue du vieux Japon la nuit où notre sabreur combat les ninjas. Les compteurs là où chaque jeu les met.
- Zupapa! et Neo Mr. Do!. La grotte bleue et ses plateformes rayées où notre petit héros rond chasse les monstres, le champ de cases colorées où notre petit mineur creuse ses tunnels et ramasse les cerises, EXTRA qui s'allume lettre par lettre.
- Super Sidekicks et Super Sidekicks 2. Le match avec le tableau de score de chaque jeu, les buts et le temps lus dans le jeu.
- Le score de Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa! et Neo Mr. Do! n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les cinquante-cinq jeux.

**Mettre à jour depuis la 1.22**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.22.0

### English

**Neo Geo games done one by one, sixth batch**
- Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger and Puzzle De Pon! now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes forty-five games done one by one. `PROGRESS.md` shows what comes next.
- Mutation Nation, Sengoku, Sengoku 2 and Ninja Combat. Beat'em ups seen from the side, a ruined city, a red sunset with a castle floating in the sky, a great wooden bridge at dusk, a park at night. Fighters of our own, a swordsman whose blade leaves a trail of light, mutants, armoured ghost warriors and ninjas. The points are blows that land, the health that goes down a blow taken, the sphere or the attack item read in the game is shown. The counters where each game puts them.
- Ninja Commando. The jungle seen from above, our blue ninja runs up the path and throws fire dragons at the enemy ninjas. LIFE and TIME at the bottom as in the game.
- Blue's Journey. The land of giant plants, our little hero of our own throws leaves at the snails and the bees. 1P=, TIME=, the hearts and the flowers as in the game.
- Puzzle Bobble 2 and Puzzle De Pon!. The beach, then a sky full of stars, the boards in their frames of metal or bricks, the star dial of Puzzle De Pon! whose hand turns with the time left. The bubbles of Puzzle De Pon! come from the game.
- Magical Drop II and Money Puzzle Exchanger. The orange brick wall and its marble columns, the pastel diamonds and the coins of 10 to 500 with a little piggy bank of our own. The quota, the level and the chains read in the game pop the drops and the coins.
- The score of these ten games is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the forty-five games.

**Updating from 1.21**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, sixième lot**
- Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger et Puzzle De Pon! ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quarante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Mutation Nation, Sengoku, Sengoku 2 et Ninja Combat. Des beat'em up de profil, une ville en ruine, un coucher de soleil rouge et un château flottant, un grand pont de bois au crépuscule, un parc la nuit. Des combattants à nous, un sabreur dont la lame laisse une traînée de lumière, des mutants, des guerriers fantômes en armure et des ninjas. Les points sont des coups portés, la vie qui baisse un coup reçu, la sphère ou l'objet d'attaque lu dans le jeu s'affiche. Les compteurs là où chaque jeu les met.
- Ninja Commando. La jungle vue du dessus, notre ninja bleu remonte le chemin et lance des dragons de feu sur les ninjas ennemis. LIFE et TIME en bas comme dans le jeu.
- Blue's Journey. Le pays des plantes géantes, notre petit héros à nous lance des feuilles aux escargots et aux abeilles. 1P=, TIME=, les cœurs et les fleurs comme dans le jeu.
- Puzzle Bobble 2 et Puzzle De Pon!. La plage, puis un ciel plein d'étoiles, les plateaux dans leurs cadres de métal ou de briques, le cadran étoilé de Puzzle De Pon! dont l'aiguille tourne avec le temps qui reste. Les bulles de Puzzle De Pon! viennent du jeu.
- Magical Drop II et Money Puzzle Exchanger. Le mur de briques orange et ses colonnes de marbre, les losanges pastel et les pièces de 10 à 500 avec une petite tirelire à nous. Le quota, le niveau et les chaînes lus dans le jeu font éclater les gouttes et les pièces.
- Le score de ces dix jeux n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quarante-cinq jeux.

**Mettre à jour depuis la 1.21**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.21.0

### English

**Neo Geo games done one by one, fifth batch**
- NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army and Burning Fight now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes thirty-five games done one by one. `PROGRESS.md` shows what comes next.
- NAM-1975. Our soldier seen from behind shoots into the burning city, then the jungle. The bullets, the grenades and the weapon read in the game are shown, a grenade blows up where the crosshair is.
- Cyber-Lip. Our hero runs down the city at night and shoots the walking robots and the drones. The weapon whose ammo goes down in the game is the one he fires. TIME in blue, the weapon in the blue bar at the bottom.
- Ghost Pilots and Alpha Mission II. Seen from the sky, the earth and the sea, then a fortress in space. A fighter with a big radial engine, a space fighter, enemy planes, bombers and saucers. The planes left, the bombs, the stars, the gold and the power where each game puts them.
- Viewpoint. The floor of tiles seen at an angle, our hover-ship and its shadow. The bomb carried in the game sweeps the screen in its colour when it is spent.
- Zed Blade and Prehistoric Isle 2. Seen from the side, a valley at dawn with its helicopters, the sea by the island with its flying reptiles. A bomb spent blows up the screen.
- Shock Troopers 2nd Squad. The city street seen from above, our commando goes up the road and shoots the soldiers, the jeeps and the tanks. The weapon read in the game is the one he fires, a grenade spent is thrown. TIME in big yellow numbers, the weapon box and LV as in the game.
- Robo Army and Burning Fight. Beat'em ups seen from the side, the edge of a town at dusk, a street of small shops at night. A cyborg and a street fighter of our own face the robots and the thugs that come from both sides. The points are blows that land, the health that goes down a blow taken.
- The score of these ten games is in no database. Learn it with `learn.bat`.
- New panel sprite `sprites/runner.png`, a small running fighter.
- `demo_neogeo.bat` now lists the thirty-five games.
- Demo mode. A game that drives the ammo of its weapon itself keeps it when the weapon changes.

**Updating from 1.20**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, cinquième lot**
- NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army et Burning Fight ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait trente-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- NAM-1975. Notre soldat vu de dos tire dans la ville en feu, puis la jungle. Les balles, les grenades et l'arme lues dans le jeu s'affichent, une grenade saute là où est le viseur.
- Cyber-Lip. Notre héros parcourt la ville la nuit et tire sur les robots marcheurs et les drones. L'arme dont les munitions baissent dans le jeu est celle qu'il tire. TIME en bleu, l'arme dans la barre bleue en bas.
- Ghost Pilots et Alpha Mission II. Vus du ciel, la terre et la mer, puis une forteresse dans l'espace. Un chasseur à gros moteur en étoile, un chasseur spatial, des avions ennemis, des bombardiers et des soucoupes. Les avions qui restent, les bombes, les étoiles, l'or et la puissance là où chaque jeu les met.
- Viewpoint. Le sol de dalles vu de biais, notre vaisseau et son ombre. La bombe portée dans le jeu balaie l'écran dans sa couleur quand elle part.
- Zed Blade et Prehistoric Isle 2. De profil, une vallée à l'aube et ses hélicoptères, la mer au bord de l'île et ses reptiles volants. Une bombe dépensée fait sauter l'écran.
- Shock Troopers 2nd Squad. La rue de la ville vue du dessus, notre commando remonte la route et tire sur les soldats, les jeeps et les chars. L'arme lue dans le jeu est celle qu'il tire, une grenade dépensée est lancée. TIME en gros chiffres jaunes, le cadre de l'arme et LV comme dans le jeu.
- Robo Army et Burning Fight. Des beat'em up de profil, le bord d'une ville au soir, une rue de petites boutiques la nuit. Un cyborg et un combattant à nous affrontent les robots et les voyous qui arrivent des deux côtés. Les points sont des coups portés, la vie qui baisse un coup reçu.
- Le score de ces dix jeux n'est dans aucune base. Apprends-le avec `learn.bat`.
- Nouveau sprite de dalle `sprites/runner.png`, un petit combattant qui court.
- `demo_neogeo.bat` propose maintenant les trente-cinq jeux.
- Mode démo. Un jeu qui gère lui-même les munitions de son arme les garde quand l'arme change.

**Mettre à jour depuis la 1.20**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.20.0

### English

**Neo Geo games done one by one, fourth batch**
- Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally and Magician Lord now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes twenty-five games done one by one. `PROGRESS.md` shows what comes next.
- Strikers 1945 Plus. On the HD screen, the game's two side panels (SCORE, the planes left, BOMB, the SUPER SHOT gauge) around war-torn ground seen from the sky, villages with broken tiled roofs, a railway and its train, a river and its bridges. The plane chosen by the player, drawn after the real one (P-38, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55). The full gauge that empties is the super shot, a bomb brings a formation of bombers.
- Street Hoop. A half court in a park, three against three. The points read in the game are shots from far, jump shots or dunks, the full SUPER SHOT gauge that empties is a shot on fire. The points in big red and blue letters at the top, the clock in its orange box at the bottom.
- Super Dodge Ball. A cobbled lot, two teams of three players of our own. A player whose health goes down takes the ball full in the face, at zero he is out, the full POW gauge that empties is a power shot on fire. The health bars of both teams with the names, TIME in the middle.
- Neo Bomberman. The maze seen from above, one look per world, little miner robots of our own. The bombs dropped in the game are dropped here and blow up in a cross, blocks break and come back.
- Twinkle Star Sprites. Two fields side by side and the ornate column between them, a forest that scrolls down, little witches of our own. The attacks read in the game cross over to the other field, a heart lost makes the witch spin, a bomb clears her field. Pow 1 2 Max and the bombs at the bottom.
- League Bowling. The alley seen from behind the bowler. Each time the game's shot clock starts again, the bowler throws, the ball hooks down the lane and the pins fly, STRIKE! or SPARE! now and then.
- Neo Drift Out and Thrash Rally. The rally stages seen from the sky, dirt, tarmac or snow, the car drifts in the bends, a checkpoint arch goes by when time is added. TIME as in each game, and the speed in Thrash Rally.
- Riding Hero. The road seen from behind the bike rushes to the horizon, the rider leans into the bends, the others are passed or come back, a turbo spent is a burst of speed. SPEED, TIME, TURBO and RANK where the game puts them.
- Magician Lord. The villages in the giant trees, then a temple. A hero of our own throws his magic at the undead and takes the shape read in the game. HP and POW at the bottom.
- The score of Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling and Magician Lord is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the planes of Strikers 1945 Plus and the witches of Twinkle Star Sprites follow them.
- New panel sprite `sprites/car.png`, a rally car seen from above.
- `demo_neogeo.bat` now lists the twenty-five games.

**Updating from 1.19**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, quatrième lot**
- Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally et Magician Lord ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait vingt-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Strikers 1945 Plus. Sur l'écran HD, les deux panneaux de côté du jeu (SCORE, les avions qui restent, BOMB, la jauge SUPER SHOT) autour d'un sol ravagé vu du ciel, des villages aux toits de tuiles crevés, une voie ferrée et son train, une rivière et ses ponts. L'avion choisi par le joueur, dessiné d'après le vrai (P-38, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55). La jauge pleine qui se vide est le super tir, une bombe amène une formation de bombardiers.
- Street Hoop. Un demi-terrain dans un parc, trois contre trois. Les points lus dans le jeu sont des tirs de loin, des tirs en suspension ou des smashs, la jauge SUPER SHOT pleine qui se vide donne un tir enflammé. Les points en grosses lettres rouges et bleues en haut, l'horloge dans son cadre orange en bas.
- Super Dodge Ball. Un terrain vague pavé, deux équipes de trois joueurs à nous. Un joueur dont la vie baisse prend la balle en pleine figure, à zéro il est éliminé, la jauge POW pleine qui se vide donne un tir enflammé. Les barres de vie des deux équipes avec les noms, TIME au milieu.
- Neo Bomberman. Le labyrinthe vu de haut, un style par monde, de petits robots mineurs à nous. Les bombes posées dans le jeu sont posées ici et sautent en croix, les blocs cassent et reviennent.
- Twinkle Star Sprites. Deux terrains côte à côte et la colonne ornée entre les deux, une forêt qui défile vers le bas, de petites sorcières à nous. Les attaques lues dans le jeu passent de l'autre côté, un cœur perdu fait tourner la sorcière, une bombe nettoie son terrain. Pow 1 2 Max et les bombes en bas.
- League Bowling. La salle vue de derrière le joueur. Chaque fois que le chrono du jeu repart, le joueur lance, la boule file en courbe et les quilles volent, STRIKE ! ou SPARE ! de temps en temps.
- Neo Drift Out et Thrash Rally. Les spéciales vues du ciel, terre, goudron ou neige, la voiture dérape dans les virages, une arche de contrôle passe quand du temps s'ajoute. TIME comme dans chaque jeu, et la vitesse dans Thrash Rally.
- Riding Hero. La route vue de derrière la moto file vers l'horizon, le pilote se penche dans les virages, les autres sont dépassés ou reviennent, un turbo dépensé donne un coup d'accélérateur. SPEED, TIME, TURBO et RANK là où le jeu les met.
- Magician Lord. Les villages dans les arbres géants, puis un temple. Un héros à nous lance sa magie sur les morts-vivants et prend la forme lue dans le jeu. HP et POW en bas.
- Le score de Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling et Magician Lord n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), les avions de Strikers 1945 Plus et les sorcières de Twinkle Star Sprites les suivent.
- Nouveau sprite de dalle `sprites/car.png`, une voiture de rallye vue du dessus.
- `demo_neogeo.bat` propose maintenant les vingt-cinq jeux.

**Mettre à jour depuis la 1.19**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.19.0

### English

**Neo Geo games done one by one, third batch**
- Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 and Aero Fighters 3 now have a file of their own, with a panel scene and an animated HD scene made for each game. That makes fifteen games done one by one. `PROGRESS.md` shows what comes next.
- Top Hunter. On the panel, the lives as small hunters, the timer and the power gauge. On the HD screen, hunters as big as in the game on four planets (forest, ice, wind, fire) with their two lanes, and as in the game leaves, ice or rock across the top of the screen. Robots and walking machines with turbines come on both lanes, the hunter jumps from one lane to the other and punches, throws or shoots them when the score goes up, and the full power gauge that empties is a special move. When the timer starts again for a new stage, the hunters move on to the next planet. At the top, as in the game, the hunter's head with 1UP= and the lives, the score and the power, and TIME next to the logo.
- Baseball Stars 2. On the panel, the runs of both teams with RUN! when one comes in, the balls, strikes and outs lights, and the POW gauges. On the HD screen, the field as in the game's batting view, bright green grass seen from behind home plate, the batter big in front and the pitcher on the mound. Each ball, strike and out read in the game becomes a pitch, called in big rainbow letters as in the game. The batter hits and a fielder catches the ball, and the runs send the ball far and the runners home, with fireworks when it goes over the wall. After the third out, the other team comes to bat. The count is shown in coloured dots, as in the game.
- Last Resort. On the panel, the lives, the power and the speed over a city at night. On the HD screen, the city at night of the game's first stage, giant towers lit with orange windows, purple buildings, the highway with its street lamps and its cars. The unit turns around the ship on the side away from where it goes and fires with it, and now and then it flies straight ahead and comes back. At the top 1P= and the score with the lives, POW at the bottom, as in the game.
- Aero Fighters 2 and 3. On the panel, the lives, the bombs and the power, with the pilot's name in Aero Fighters 3. On the HD screen, seen from the sky as in the games, a city in daylight with its avenues, car parks and parks in Aero Fighters 2, a city by a river at nightfall in Aero Fighters 3. Jets drawn after real fighters, helicopters and tanks in Aero Fighters 2, propeller planes and big bombers in Aero Fighters 3. The planes fly with their shadows below, the enemies blow up when the score goes up, and a bomb clears the screen. The bombs are shown in their frames, as in the games. In Aero Fighters 3, the plane is the one of the pilot chosen by player 1, among twelve.
- The score of Top Hunter, Last Resort and the two Aero Fighters is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the hunters of Top Hunter (up and down change lanes), the ships of Last Resort (button B launches the unit) and the planes of the Aero Fighters follow them.
- `demo_neogeo.bat` now lists the fifteen games.

**HD screen**
- A background prepared while a game runs now appears without a jolt, its layers are made ready a little at each image.

**Updating from 1.18**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, troisième lot**
- Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 et Aero Fighters 3 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ça fait quinze jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Top Hunter. Sur la dalle, les vies en petits chasseurs, le chrono et la jauge de puissance. Sur l'écran HD, des chasseurs aussi grands que dans le jeu sur quatre planètes (forêt, glace, vent, feu) avec leurs deux voies, et comme dans le jeu du feuillage, de la glace ou de la roche en haut de l'écran. Des robots et des machines à turbines arrivent sur les deux voies, le chasseur saute d'une voie à l'autre et les frappe, les jette ou leur tire dessus quand le score monte, et la jauge de puissance pleine qui se vide donne un coup spécial. Quand le chrono repart pour un nouveau stage, les chasseurs passent à la planète suivante. En haut, comme dans le jeu, la tête du chasseur avec 1UP= et les vies, le score et la puissance, et TIME à côté du logo.
- Baseball Stars 2. Sur la dalle, les points des deux équipes avec RUN! quand il y en a un, les lampes des balles, des prises et des retraits, et les jauges POW. Sur l'écran HD, le terrain comme dans la vue de frappe du jeu, une herbe vert vif vue de derrière le marbre, le frappeur en grand devant et le lanceur sur le monticule. Chaque balle, prise et retrait lu dans le jeu devient un lancer, annoncé en grosses lettres arc-en-ciel comme dans le jeu. Le frappeur frappe et un joueur attrape la balle, et les points envoient la balle loin et les coureurs au marbre, avec un feu d'artifice quand elle passe le mur. Après le troisième retrait, l'autre équipe passe à la batte. Le compte s'affiche en pastilles de couleur, comme dans le jeu.
- Last Resort. Sur la dalle, les vies, la puissance et la vitesse au-dessus d'une ville la nuit. Sur l'écran HD, la ville la nuit du premier stage du jeu, des tours géantes aux fenêtres orange, des immeubles violets, l'autoroute avec ses réverbères et ses voitures. L'unité tourne autour du vaisseau, du côté opposé à sa route, et tire avec lui, et de temps en temps elle part droit devant puis revient. En haut 1P= et le score avec les vies, POW en bas, comme dans le jeu.
- Aero Fighters 2 et 3. Sur la dalle, les vies, les bombes et la puissance, avec le nom du pilote dans Aero Fighters 3. Sur l'écran HD, vues du ciel comme dans les jeux, une ville en plein jour avec ses avenues, ses parkings et ses parcs dans Aero Fighters 2, une ville au bord d'un fleuve à la tombée de la nuit dans Aero Fighters 3. Des avions de chasse dessinés d'après de vrais avions, des hélicoptères et des chars dans Aero Fighters 2, des avions à hélice et de gros bombardiers dans Aero Fighters 3. Les avions volent avec leur ombre dessous, les ennemis explosent quand le score monte, et une bombe nettoie l'écran. Les bombes s'affichent dans leur cadre, comme dans les jeux. Dans Aero Fighters 3, l'avion est celui du pilote choisi par le joueur 1, parmi douze.
- Le score de Top Hunter, Last Resort et des deux Aero Fighters n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), les chasseurs de Top Hunter (haut et bas changent de voie), les vaisseaux de Last Resort (le bouton B lance l'unité) et les avions des Aero Fighters les suivent.
- `demo_neogeo.bat` propose maintenant les quinze jeux.

**Écran HD**
- Un décor préparé pendant qu'un jeu tourne s'affiche maintenant sans à-coup, ses couches sont prêtes un peu à chaque image.

**Mettre à jour depuis la 1.18**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.18.0

### English

**Neo Geo games done one by one, second batch**
- Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 and Sengoku 3 now have a file of their own, with a panel scene and an animated HD scene made for each game. That makes ten games done one by one. `PROGRESS.md` shows what comes next.
- Pulstar. On the panel, the lives as small ships, the stage and the charge gauge. On the HD screen, one world per stage (Earth, water vein, fire, space station, forest, nebula). The charge glows on the nose of the ship and leaves as a big beam, the pods and the front shield follow the ship, and STAGE comes with the name of the stage.
- Magical Drop III. On the panel, both players' tarot cards, the quota and the level. On the HD screen, two fields of drops under a tarot sky. When the quota goes down, the jester throws a drop and as many pop, a big group makes a chain, the level pushes a row down, and the card flips when the character changes.
- Super Sidekicks 3 and The Ultimate 11. On the panel, the goals of both teams and GOAL! when one goes in, with the power gauges in The Ultimate 11. On the HD screen, the match seen by the TV camera, by day, or at night under the floodlights. When the goals go up, the ball ends in the net, GOAL!, confetti, and the crowd jumps. In The Ultimate 11, a full power gauge that empties fires a super shot on fire.
- Sengoku 3. On the panel, the health and the magic of both players, the timer, the fighter, the throwing weapon and how many are left. On the HD screen, a temple under the moon and shadow warriors. The throwing weapons fly when their count goes down, a warrior falls under the sword when the score goes up, the magic sweeps the screen, and the panel shakes when hit.
- The score of Pulstar, Magical Drop III and Sengoku 3 is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the ship of Pulstar and the jester of Magical Drop III follow them, and button A strikes in Sengoku 3.
- `demo_neogeo.bat` now lists the ten games.

**HD screen**
- A banner can have a line under it, such as the name of the stage in Pulstar.
- Preparing a background while a game runs no longer freezes the display for a moment.

**Updating from 1.17**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, deuxième lot**
- Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 et Sengoku 3 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ça fait dix jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Pulstar. Sur la dalle, les vies en petits vaisseaux, le stage et la jauge de charge. Sur l'écran HD, un monde par stage (la Terre, la veine d'eau, le feu, la station spatiale, la forêt, la nébuleuse). La charge brille au nez du vaisseau et part en gros rayon, les modules et le bouclier avant suivent le vaisseau, et STAGE arrive avec le nom du stage.
- Magical Drop III. Sur la dalle, les cartes de tarot des deux joueurs, le quota et le niveau. Sur l'écran HD, deux champs de gouttes sous un ciel de tarot. Quand le quota baisse, le fou lance une goutte et autant de gouttes éclatent, un gros groupe fait une chaîne, le niveau fait descendre une rangée, et la carte se retourne quand le personnage change.
- Super Sidekicks 3 et The Ultimate 11. Sur la dalle, les buts des deux équipes et BUT ! quand il y en a un, avec les jauges de puissance dans The Ultimate 11. Sur l'écran HD, le match vu par la caméra de télé, de jour, ou de nuit sous les projecteurs. Quand les buts montent, le ballon finit au fond du filet, BUT !, des confettis, et le public saute. Dans The Ultimate 11, une jauge de puissance pleine qui se vide lance un super tir en feu.
- Sengoku 3. Sur la dalle, la vie et la magie des deux joueurs, le chrono, le combattant, l'arme de jet et ce qu'il en reste. Sur l'écran HD, un temple sous la lune et des guerriers de l'ombre. Les armes de jet partent quand leur nombre baisse, un guerrier tombe sous le sabre quand le score monte, la magie balaie l'écran, et le panneau tremble quand on est touché.
- Le score de Pulstar, Magical Drop III et Sengoku 3 n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), le vaisseau de Pulstar et le fou de Magical Drop III les suivent, et le bouton A frappe dans Sengoku 3.
- `demo_neogeo.bat` propose maintenant les dix jeux.

**Écran HD**
- Un bandeau peut avoir une ligne dessous, comme le nom du stage dans Pulstar.
- Préparer un décor pendant qu'un jeu tourne ne fige plus l'affichage un instant.

**Mettre à jour depuis la 1.17**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.17.0

### English

**Neo Geo games done one by one**
- Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers and Neo Turf Masters now have a file of their own, with a panel scene and an animated HD scene made for each game. They are the first five, the best-known first. `PROGRESS.md` shows what comes next.
- Blazing Star. On the panel, the lives as small ships, ROUND and the shot power. On the HD screen, the ship flies above a big planet and fires, an enemy blows up when the score goes up, POWER UP, and ROUND with a burst of speed.
- Puzzle Bobble. On the panel, the bubble in the launcher and the next one, in their colors. On the HD screen, each bubble shot in the game leaves the launcher and sticks to a little board, and three of a color pop.
- Windjammers. On the panel, the points of the set with the timer in between, the court and the opponent's country. On the HD screen, the court of the game and the scoreboard. The disc flies into the goal with +3 or +5, or drops on the other side with +2.
- Shock Troopers. Energy, gun and ammo, special weapon. On the HD screen, a jungle at war with the shots and the grenades blowing up.
- Neo Turf Masters. Club and distance, stroke, power and wind. On the HD screen, a golf course where the wind pushes the clouds and the flag, and the ball flies to the green at each stroke.
- The score of Blazing Star, Puzzle Bobble and Shock Troopers is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the ship and the launcher follow them. Until the player touches them, the scene plays by itself.
- With nobody playing, the coin screen, as for the fighting games. GAME OVER when the game ends, CONTINUE ? during the countdown.
- `demo_neogeo.bat` shows these games with simulated values.

**HD screen**
- The animated backgrounds are 2 to 8 times faster to draw, for Metal Slug and the fighting games too.

**Game files**
- New panel elements, `icons` (a small drawing repeated for a value, such as lives), `dot` (a disk colored by a value, such as a bubble) and `arrow` (an arrow that turns with a value, such as the wind). See README section 8.
- `"names"` in `"derived"` can hold one list per language.
- The `"demo"` section can move the game's own values (`"sim"`), and `"attract": true` starts any game on the coin screen.

**Updating from 1.16**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un**
- Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers et Neo Turf Masters ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ce sont les cinq premiers, les plus connus d'abord. `PROGRESS.md` montre ce qui vient ensuite.
- Blazing Star. Sur la dalle, les vies en petits vaisseaux, ROUND et la puissance du tir. Sur l'écran HD, le vaisseau vole au-dessus d'une grosse planète et tire, un ennemi explose quand le score monte, POWER UP, et ROUND avec une pointe de vitesse.
- Puzzle Bobble. Sur la dalle, la bulle dans le lanceur et la suivante, à leurs couleurs. Sur l'écran HD, chaque bulle tirée dans le jeu part du lanceur et colle à un petit plateau, et trois de la même couleur éclatent.
- Windjammers. Sur la dalle, les points du set avec le chrono entre les deux, le terrain et le pays de l'adversaire. Sur l'écran HD, le terrain du jeu et le tableau des scores. Le palet file dans le but avec +3 ou +5, ou tombe de l'autre côté avec +2.
- Shock Troopers. L'énergie, l'arme et ses munitions, l'arme spéciale. Sur l'écran HD, une jungle en guerre avec les tirs et les grenades qui explosent.
- Neo Turf Masters. Le club et sa distance, le coup, la puissance et le vent. Sur l'écran HD, un parcours de golf où le vent pousse les nuages et le drapeau, et la balle part vers le green à chaque coup.
- Le score de Blazing Star, Puzzle Bobble et Shock Troopers n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), le vaisseau et le lanceur les suivent. Tant que le joueur n'y touche pas, la scène joue toute seule.
- Quand personne ne joue, l'écran des pièces, comme pour les jeux de combat. GAME OVER quand la partie finit, CONTINUE ? pendant le compte à rebours.
- `demo_neogeo.bat` montre ces jeux avec des valeurs simulées.

**Écran HD**
- Les décors animés se dessinent 2 à 8 fois plus vite, pour les Metal Slug et les jeux de combat aussi.

**Fichiers de jeu**
- Nouveaux éléments de dalle, `icons` (un petit dessin répété selon une valeur, comme les vies), `dot` (un disque coloré selon une valeur, comme une bulle) et `arrow` (une flèche qui tourne selon une valeur, comme le vent). Voir la section 8 du README.
- `"names"` dans `"derived"` peut avoir une liste par langue.
- La section `"demo"` peut faire bouger les valeurs propres au jeu (`"sim"`), et `"attract": true` fait commencer n'importe quel jeu sur l'écran des pièces.

**Mettre à jour depuis la 1.16**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.16.0

### English

**Game logo when a game starts**
- When a game starts, its LaunchBox Clear Logo comes first. On the HD screen it arrives big with a flash and a light sweep, then glides to its place in the scene. On the Pixelcade and ZeDMD panels it zooms in on the LEDs. The Pixelcade shows it as soon as pixelweb has handed the panel over.
- New `"intro"` section in `config.json` (`"logo"`, `"seconds"`, `"launchbox"`), see README section 3.

**Coin screen for the fighting games**
- With nobody playing, the Neo Geo fighting games wait for a coin. On the panel, a € coin floats above a slot and drops into it when a coin is inserted, with +1 and the credit counter rolling, then PRESS START with a button.
- On the HD screen, two coin doors with a coin spinning above each one. An inserted coin drops into its slot with sparks, +1 and the counter rolling, then come the 1P and 2P START buttons.
- A coin only drops when the credits really go up. The game's own demo fights no longer set off sparks or K.O. on the HD screen.
- `"coin_symbol"` sets the symbol on the coins (€, $, £ or none). `sprites\insert_coin.gif` replaces the panel's coin screen with your own animation. `"coins": false` in the `preview` section brings back the plain INSERT COIN on the HD screen. See README section 7.

**Fighting scene on the panel**
- The top row is one pixel lower, so the accents stay visible.
- On the computer's side, the credits and PRESS START take turns.
- The timer sits in a frame, and the fighters' names are white.

**Other changes**
- `demo_fight.bat` starts on the coin screen. Two coins go in, then the fight begins (`"demo": {"attract": false}` in a game file skips it).
- HD screen, the arena backdrop no longer has bright dots on its spotlights.

**Updating from 1.15**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Logo du jeu au lancement**
- Quand un jeu démarre, son Clear Logo LaunchBox arrive d'abord. Sur l'écran HD, il entre en grand avec un éclair et un reflet, puis glisse à sa place dans la scène. Sur la Pixelcade et les dalles ZeDMD, il grandit sur les LED. La Pixelcade l'affiche dès que pixelweb lui a laissé la dalle.
- Nouvelle section `"intro"` dans `config.json` (`"logo"`, `"seconds"`, `"launchbox"`), voir la section 3 du README.

**Écran des pièces des jeux de combat**
- Quand personne ne joue, les jeux de combat Neo Geo attendent une pièce. Sur la dalle, une pièce € flotte au-dessus d'une fente et tombe dedans quand une pièce est mise, avec +1 et le compteur de crédits qui roule, puis PRESS START avec un bouton.
- Sur l'écran HD, deux monnayeurs avec une pièce qui tourne au-dessus de chacun. Une pièce mise tombe dans sa fente avec des étincelles, +1 et le compteur qui roule, puis arrivent les boutons START 1P et 2P.
- Une pièce ne tombe que quand les crédits montent vraiment. Les combats de démonstration du jeu ne déclenchent plus d'étincelles ni de K.O. sur l'écran HD.
- `"coin_symbol"` règle le symbole des pièces (€, $, £ ou aucun). `sprites\insert_coin.gif` remplace l'écran des pièces de la dalle par ta propre animation. `"coins": false` dans la section `preview` remet le simple INSERT COIN sur l'écran HD. Voir la section 7 du README.

**Scène de combat sur la dalle**
- La ligne du haut est un pixel plus bas, les accents restent visibles.
- Du côté de l'ordinateur, les crédits et PRESS START s'affichent tour à tour.
- Le chrono est dans un cadre, et les noms des combattants sont en blanc.

**Autres changements**
- `demo_fight.bat` commence sur l'écran des pièces. Deux pièces entrent, puis le combat commence (`"demo": {"attract": false}` dans un fichier de jeu le saute).
- Écran HD, le décor de l'arène n'a plus de points lumineux sur ses projecteurs.

**Mettre à jour depuis la 1.15**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.15.0

### English

**English and French**
- Everything is now in English, and switches to French by itself when Windows is in French. This covers the messages, `install.bat`, the learning tool, the test tools, the MAME plugin (messages and Tab menu), the words on the LED panel and the HD screen.
- To force a language, add `"language": "en"` or `"fr"` at the top of `config.json`. `"auto"` (the default) follows Windows.
- The texts of the scenes in `games\*.json` are now written in English and translated to French when drawn. Files written in French still work in both languages.

**New file names**
- `run.bat` (was `lancer.bat`), `learn.bat` (`apprendre.bat`), `install.bat` (`installer.bat`), `screen_setup.bat` (`ecran_dmd.bat`), `test_panel.bat` (`test_dalle.bat`), `demo_fight.bat` (`demo_combat.bat`).
- `config.default.json` (was `config.defaut.json`). Your `config.json` is kept.
- `learned\` (was `appris\`). The folder is moved by itself the first time ArcadeDMD starts.
- `README.md` in English and `README.fr.md` in French (was `LISEZMOI.md`).
- `install.bat` removes the old French-named files.

**HD screen (LCD marquee)**
- New Metal Slug scene. One soldier panel per player, shots in the style of each weapon, bombs that explode in the backdrop, a crate when a weapon is picked up, the helmet falling when a life is lost, LAST LIFE, rescued prisoners, coins, player 2 joining, CONTINUE and GAME OVER.
- Each Metal Slug mission has its own animated backdrop (jungle, desert, snowy mountain, city at war, harbor, enemy base), with MISSION COMPLETE and fireworks in between, and a slideshow of the backdrops when nobody plays.
- New fighting game effects. Sparks, combo counter, FIRST ATTACK, super moves, red heartbeat when health is low, exploding K.O., DOUBLE K.O., TIME UP, PERFECT, confetti for the winner, next King of Fighters fighter, FIGHT !
- Eight animated fighting backgrounds with a crowd (city at night, temple, harbor, ruins, arena, desert, snowy mountain, jungle).
- The background follows the game's stage. Addresses from the cheat databases for The King of Fighters '96 to 2000 and 2002, Garou, Fatal Fury 2 and Special, Real Bout Fatal Fury 2 and Special, Samurai Shodown II to IV, World Heroes and World Heroes Perfect, Rage of the Dragons, SNK vs. Capcom (JAMMA PCB), and the mission number of Metal Slug 1 and 2. They still have to be confirmed in game.
- Each game file chooses the background of each of its stages (`"hd": {"stages": [...]}`), see README section 3.
- Metal Slug games read the Neo Geo BIOS stick and buttons, so handgun shots and the backdrop scrolling follow the player. To be confirmed in game.

**Other changes**
- `demo_fight.bat` changes the stage every two K.O. The Metal Slug demo moves to the next mission every 25 seconds.
- `test_retroarch.bat` shows the stage, backdrop and mission values.
- The project is on GitHub. Each version comes with its zip on the Releases page.

**Updating from 1.14**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once. It updates the MAME plugin and removes the old files.

### Français

**Anglais et français**
- Tout est maintenant en anglais, et passe tout seul en français quand Windows est en français. C'est le cas des messages, de `install.bat`, de l'outil d'apprentissage, des outils de test, du plugin MAME (messages et menu Tab), des mots de la dalle LED et de l'écran HD.
- Pour forcer une langue, ajoute `"language": "en"` ou `"fr"` en haut de `config.json`. `"auto"` (par défaut) suit Windows.
- Les textes des scènes dans `games\*.json` sont maintenant écrits en anglais et traduits en français à l'affichage. Les fichiers écrits en français marchent toujours dans les deux langues.

**Nouveaux noms de fichiers**
- `run.bat` (ex `lancer.bat`), `learn.bat` (`apprendre.bat`), `install.bat` (`installer.bat`), `screen_setup.bat` (`ecran_dmd.bat`), `test_panel.bat` (`test_dalle.bat`), `demo_fight.bat` (`demo_combat.bat`).
- `config.default.json` (ex `config.defaut.json`). Ton `config.json` est gardé.
- `learned\` (ex `appris\`). Le dossier est déplacé tout seul au premier démarrage d'ArcadeDMD.
- `README.md` en anglais et `README.fr.md` en français (ex `LISEZMOI.md`).
- `install.bat` supprime les anciens fichiers aux noms français.

**Écran HD (marquee LCD)**
- Nouvelle scène Metal Slug. Un panneau de soldat par joueur, des tirs dans le style de chaque arme, des bombes qui explosent dans le décor, une caisse quand on ramasse une arme, le casque qui tombe quand on perd une vie, DERNIÈRE VIE, prisonniers libérés, pièces, arrivée du joueur 2, CONTINUE et GAME OVER.
- Chaque mission des Metal Slug a son décor animé (jungle, désert, montagne enneigée, ville en guerre, port, base ennemie), avec MISSION COMPLETE et un feu d'artifice entre les deux, et un diaporama des décors quand personne ne joue.
- Nouveaux effets des jeux de combat. Étincelles, compteur de combo, PREMIER COUP, super coups, battement de cœur rouge quand la vie est basse, K.O. qui explose, DOUBLE K.O., TIME UP, PERFECT, confettis pour le vainqueur, combattant suivant des King of Fighters, FIGHT !
- Huit décors de combat animés avec du public (ville la nuit, temple, port, ruines, arène, désert, montagne enneigée, jungle).
- Le décor suit le stage du jeu. Adresses tirées des bases de triche pour The King of Fighters '96 à 2000 et 2002, Garou, Fatal Fury 2 et Special, Real Bout Fatal Fury 2 et Special, Samurai Shodown II à IV, World Heroes et World Heroes Perfect, Rage of the Dragons, SNK vs. Capcom (JAMMA PCB), et le numéro de mission de Metal Slug 1 et 2. Elles restent à confirmer en jeu.
- Chaque fichier de jeu choisit le décor de chacun de ses stages (`"hd": {"stages": [...]}`), voir la section 3 du README.
- Les Metal Slug lisent le stick et les boutons par le BIOS Neo Geo, les tirs au pistolet et le défilement du décor suivent donc le joueur. À confirmer en jeu.

**Autres changements**
- `demo_fight.bat` change de stage tous les deux K.O. La démo Metal Slug passe à la mission suivante toutes les 25 secondes.
- `test_retroarch.bat` affiche les valeurs du stage, du décor et de la mission.
- Le projet est sur GitHub. Chaque version a son zip sur la page Releases.

**Mise à jour depuis la 1.14**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois. Il met à jour le plugin MAME et supprime les anciens fichiers.

## 1.14.0 and earlier / et avant

Versions released before the project moved to GitHub. Each one is a commit named after its version (ArcadeDMD 1.2 to ArcadeDMD 1.14.0) in the history of the main branch.

Versions publiées avant l'arrivée du projet sur GitHub. Chacune est un commit qui porte son numéro (ArcadeDMD 1.2 à ArcadeDMD 1.14.0) dans l'historique de la branche main.
