## Reflection 1: easy vs. hard questions
I think the guided build will already answer "where is the service thin
compared to the population" well, because it uses a fixed schedule. It will
not answer "when are there repeated delays" or "what can we predict" well,
because that needs weeks of real-time data that does not exist yet.
<!-- Je pense que la construction guidée répondra déjà bien à « où le service
est-il faible par rapport à la population », car elle utilise un horaire fixe.
Elle ne répondra pas bien à « quand y a-t-il des retards répétés » ni à
« que peut-on prévoir », car il faut des semaines de données en temps réel
qui n'existent pas encore. -->
## Reflection 2: why the static feed is not refreshed every 15 minutes
The schedule only changes when SETRAM publishes a new feed, a few times a
year. Downloading and processing it every 15 minutes would give the same
result almost every time, so it would waste resources and fill the Git
history with useless commits.
<!-- L'horaire ne change que quand SETRAM publie un nouveau fichier, quelques
fois par an. Le télécharger et le traiter toutes les 15 minutes donnerait
presque toujours le même résultat : ce serait un gaspillage de ressources et
cela remplirait l'historique Git de commits inutiles. -->

## Reflection 3: auto-typed IDs and joins
If one file reads stop_id as numbers and another reads it as text (because of
values like "FLEX-381"), the join compares the number 1001 with the text
"1001". They do not match, so rows are lost or the merge fails, and nothing
looks obviously broken. Reading every column as text (dtype=str) makes all
files use the same type, so the join works.
<!-- Si un fichier lit stop_id comme des nombres et un autre comme du texte
(à cause de valeurs comme « FLEX-381 »), la jointure compare le nombre 1001 avec
le texte « 1001 ». Ils ne correspondent pas, donc des lignes sont perdues ou la
fusion échoue, sans que rien ne paraisse cassé. Lire chaque colonne comme du
texte (dtype=str) donne le même type à tous les fichiers, donc la jointure
fonctionne. -->
## Reflection 4: per-route vs. per-stop logging
A 12-week semester has 4 x 24 x 7 x 12 = 8,064 snapshots. Logging every
stop update (about 5,000 per snapshot) would give about 40 million rows.
Logging one row per route (about 30 routes) gives about 240,000 rows, which
is roughly 170 times smaller and fine for Git. But with one row per route, it
is harder to answer "which specific stops are delayed again and again?", or
"do delays build up along a line?", because the stop-level detail is lost.
<!-- Un semestre de 12 semaines compte 4 x 24 x 7 x 12 = 8 064 instantanés.
Enregistrer chaque mise à jour d'arrêt (environ 5 000 par instantané) donnerait
environ 40 millions de lignes. Enregistrer une ligne par ligne de bus (environ
30 lignes) donne environ 240 000 lignes, soit environ 170 fois moins, ce qui
convient à Git. Mais avec une ligne par ligne de bus, il est plus difficile de
répondre à « quels arrêts précis sont en retard de façon répétée ? » ou
« les retards s'accumulent-ils le long d'une ligne ? », car le détail par arrêt
est perdu. -->
## Reflection 5: color encoding of delays
The current rule shows a very early bus as green, but a bus that leaves early
can strand a waiting passenger just like a late bus. I would use a scale
centered on zero: green for roughly on time (for example from -60 s to
+180 s), orange or red for late, and purple or blue for very early, with the
strongest color at both extremes. With this rule, a route with a large
negative delay would be flagged as a problem, whereas the current chart shows
it as the best route.
<!-- La règle actuelle affiche un bus très en avance en vert, mais un bus qui
part trop tôt peut laisser un passager à quai, comme un bus en retard.
J'utiliserais une échelle centrée sur zéro : vert pour à peu près à l'heure
(par exemple de -60 s à +180 s), orange ou rouge pour en retard, violet ou bleu
pour très en avance, avec la couleur la plus forte aux deux extrêmes. Avec
cette règle, une ligne avec un grand retard négatif serait signalée comme un
problème, alors que le graphique actuel la montre comme la meilleure ligne. -->
## Reflection 6: static vs. real-time schedule
A 15-minute schedule for the static reference would be wasteful: the data is
the same, so we would download and process the same file again and again,
create useless commits, and put load on the data provider for no new
information. A monthly schedule for the real-time delays would make the
real-time picture useless: delays last minutes or hours, so one snapshot per
month would show one random moment and no pattern. The mismatch goes both
ways: the schedule must follow how fast the source changes.
<!-- Un calendrier de 15 minutes pour la référence statique serait un
gaspillage : les données sont les mêmes, donc on téléchargerait et traiterait
le même fichier encore et encore, avec des commits inutiles et de la charge
pour le fournisseur, sans information nouvelle. Un calendrier mensuel pour les
retards en temps réel rendrait l'image temps réel inutile : les retards durent
des minutes ou des heures, donc un instantané par mois montrerait un moment au
hasard et aucun motif. L'erreur existe dans les deux sens : le calendrier doit
suivre la vitesse à laquelle la source change. -->
## Reflection 7: sanity check against reality
I looked at the route with the largest average delay on the dashboard: line T1
at about 311 seconds. Only one trip was observed for this line, so the average
is based on a single bus. It was late in the evening, with only 7 routes
reporting. In my history file, T1 has exactly the same values in two snapshots
taken about 38 minutes apart (1 trip, 24 updates, 17 skipped stops, 311.1 s
average delay, 450 s maximum). A real bus in service would not give identical
numbers, so the data looks frozen. I looked for information about a disruption
on line T1 that evening and found none (I could not read SETRAM's live traffic
page, and search results only showed older articles). My best guess is that
this is a data artifact (a frozen trip or a stuck bus in the feed) based on a
very small sample, not a real network problem.
<!-- J'ai regardé la ligne avec le plus grand retard moyen sur le tableau de bord :
la ligne T1, environ 311 secondes. Un seul trajet a été observé pour cette
ligne, donc la moyenne repose sur un seul bus. C'était tard le soir, avec
seulement 7 lignes qui remontent des données. Dans mon fichier d'historique,
T1 a exactement les mêmes valeurs dans deux instantanés pris à environ 38
minutes d'écart (1 trajet, 24 mises à jour, 17 arrêts supprimés, 311,1 s de
retard moyen, 450 s au maximum). Un vrai bus en service ne donnerait pas des
chiffres identiques, donc les données semblent figées. J'ai cherché une
information sur une perturbation de la ligne T1 ce soir-là et je n'en ai pas
trouvé (je n'ai pas pu lire la page d'info trafic de SETRAM en direct, et les
résultats de recherche ne montraient que d'anciens articles). Ma meilleure
hypothèse est qu'il s'agit d'un artefact de données (un trajet figé ou un bus
bloqué dans le flux) reposant sur un très petit échantillon, pas d'un vrai
problème du réseau. -->
## Reflection 8: where population misleads as a demand proxy
A small commune can have a low population but high transport demand if it
hosts a big employer, a hospital, a school or a shopping area: many people
come from outside every day. For example, a commune with a large business
park has few residents but many workers who use the bus. The reverse also
happens: a commune with many residents who all have a car, or many elderly
people who travel little, can have a high population but low demand.
<!-- Une petite commune peut avoir peu d'habitants mais une forte demande de
transport si elle accueille un gros employeur, un hôpital, une école ou une zone
commerciale : beaucoup de gens viennent de l'extérieur chaque jour. Par exemple,
une commune avec un grand parc d'activités a peu de résidents mais beaucoup de
salariés qui prennent le bus. L'inverse existe aussi : une commune avec beaucoup
d'habitants qui ont tous une voiture, ou beaucoup de personnes âgées qui se
déplacent peu, peut avoir une forte population mais une faible demande. -->
## Reflection 9: supply metric and a commune where it misleads
My metric is: scheduled stop-visits per weekday per 1,000 residents (the sum
of daily trips over all stops of a commune, divided by its population, times
1,000). In my real output, La-Chapelle-Saint-Aubin is first with about 1,010
visits per 1,000 residents, with 53 stops for only 2,319 residents, while Le
Mans (148,876 residents) is in the middle with about 154. This looks wrong. I
checked the stop names in stops_frequency.csv: many of the 53 stops have names
like "Zone Industrielle Nord", "Université", "Citroën", "Panhard" or "Louis
Delage", which look like places in Le Mans, and only "Église St-Aubin" clearly
belongs to the commune. The reason is that each stop is assigned to the commune
with the nearest center, not to the commune where it really is, so stops from
the north of Le Mans are counted in small neighbouring communes. The ranking
mostly measures this assignment method, not real accessibility for residents.
<!-- Ma mesure est : passages prévus un jour de semaine pour 1 000 habitants (la
somme des trajets quotidiens sur tous les arrêts d'une commune, divisée par sa
population, fois 1 000). Dans mes vrais résultats, La-Chapelle-Saint-Aubin est
première avec environ 1 010 passages pour 1 000 habitants, avec 53 arrêts pour
seulement 2 319 habitants, alors que Le Mans (148 876 habitants) est au milieu
avec environ 154. Cela semble faux. J'ai vérifié les noms d'arrêts dans
stops_frequency.csv : beaucoup des 53 arrêts ont des noms comme « Zone
Industrielle Nord », « Université », « Citroën », « Panhard » ou « Louis
Delage », qui ressemblent à des lieux du Mans, et seul « Église St-Aubin »
appartient clairement à la commune. La raison est que chaque arrêt est rattaché
à la commune dont le centre est le plus proche, pas à la commune où il se
trouve vraiment, donc des arrêts du nord du Mans sont comptés dans de petites
communes voisines. Le classement mesure surtout cette méthode de rattachement,
pas l'accessibilité réelle pour les habitants. -->
## Reflection 10: aggregating stop-level delays without a huge file
I would not keep every stop update. Instead I would keep one row per stop and
per day, with the number of observations, the average delay, the 90th
percentile of the delay, and the share of observations more than 5 minutes
late. With about 800 stops, this gives about 800 rows per day, so roughly
70,000 rows for a 12-week semester instead of 40 million. This is small
enough for Git and still answers "which stops are repeatedly delayed?". I
could also keep the raw detail only for the few stops that cross a delay
threshold.
<!-- Je ne garderais pas chaque mise à jour d'arrêt. Je garderais plutôt une
ligne par arrêt et par jour, avec le nombre d'observations, le retard moyen, le
90e percentile du retard et la part des observations en retard de plus de 5
minutes. Avec environ 800 arrêts, cela donne environ 800 lignes par jour, donc
environ 70 000 lignes pour un semestre de 12 semaines au lieu de 40 millions.
C'est assez petit pour Git et cela répond encore à « quels arrêts sont en retard
de façon répétée ? ». Je pourrais aussi garder le détail brut seulement pour les
quelques arrêts qui dépassent un seuil de retard. -->
## Reflection 11 (closing): back to Reflection 1
In Reflection 1 I guessed that "where is the service thin compared to the
population" would be easy and that delays and predictions would be hard. This
was partly right. The supply-vs-population question was answerable today, but
it needed real judgment: my first result was misleading because of how stops
are assigned to communes, and population is only a proxy for demand. The
question about recurring delays needs weeks of history: after a few hours I
have only two snapshots, and some routes (like T1, with one bus) are based on
a very small sample. Predicting delays needs even more history and a clear
definition of what is predicted.
<!-- Dans la réflexion 1, j'avais deviné que « où le service est-il faible par
rapport à la population » serait facile et que les retards et les prévisions
seraient difficiles. C'était en partie juste. La question offre/population
était réalisable aujourd'hui, mais elle a demandé un vrai jugement : mon premier
résultat était trompeur à cause de la façon dont les arrêts sont rattachés aux
communes, et la population n'est qu'un substitut de la demande. La question sur
les retards récurrents demande des semaines d'historique : après quelques
heures, je n'ai que deux instantanés, et certaines lignes (comme T1, avec un
seul bus) reposent sur un très petit échantillon. Prévoir les retards demande
encore plus d'historique et une définition claire de ce qu'on prévoit. -->

