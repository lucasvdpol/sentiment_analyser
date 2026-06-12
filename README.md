YouTube Sentiment & Analytics Pipeline
Projectoverzicht

Dit project omvatte de ontwikkeling van een geautomatiseerde datapipeline, ontworpen om YouTube-videodata binnen te halen, te verwerken en te analyseren. Het systeem is gebouwd om autonoom te draaien op een vast schema, waardoor er een longitudinale database wordt opgebouwd met prestatiegegevens en het publieke sentiment over tijd.
Doelstelling

Het doel was om te komen van ruwe datainjestie naar bruikbare inzichten door een robuuste ETL-pipeline (Extract, Transform, Load) te bouwen. Deze pipeline biedt dagelijks een overzicht van de prestaties van video's en het bijbehorende sentiment van kijkers.
De Workflow van de Pipeline

Het project werd uitgevoerd in vier verschillende fasen:
-Datainjestie: Ontwikkeling van een service die communiceert met de YouTube API. Deze component haalt metadata op (views, likes, reacties, etc.) voor specifieke video's en slaat deze op in een relationele database.
-Transcriptie: Integratie van OpenAI Whisper om automatisch spraak-naar-tekst-conversie uit te voeren op de videocontent.
-Sentimentanalyse: Ontwikkeling en training van een classificatiemodel om de transcripten te analyseren en het sentiment van de videocontent te bepalen.
-Automatisering & Integratie: Het inkapselen van de volledige pipeline in Docker-containers. Het systeem is geconfigureerd om als een nachtelijke taak te draaien, waardoor de database een accuraat historisch overzicht van de dagelijkse metrieken behoudt.

Architectuur

Het systeem is gebouwd om schaalbaar en onderhoudbaar te zijn:
-Database: PostgreSQL (gebruikt voor het opslaan van historische metadata en analytische resultaten).
-Processing: Op Python gebaseerde ETL-scripts voor datatransformatie.
-Infrastructuur: Docker & Docker Compose voor container-gebaseerde deployment.
-Automatisering: Georkestreerd via cron om dagelijkse uitvoering te garanderen.
-Visualisatie: Alle verwerkte data werd samengevoegd en gevisualiseerd via een dedicated dashboard, wat duidelijke inzichten geeft in sentimenttrends over tijd.

Status

Let op: Dit project is ontwikkeld als onderdeel van een onderwijscurriculum. Hoewel de productieomgeving op de schoolserver momenteel niet actief is, is het architecturale ontwerp modulair en direct inzetbaar op cloud-infrastructuur (zoals AWS, GCP of Azure).
