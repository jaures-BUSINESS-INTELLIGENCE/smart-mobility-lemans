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
