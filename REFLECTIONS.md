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
