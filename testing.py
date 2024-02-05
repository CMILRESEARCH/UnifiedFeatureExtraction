from modules.ftu import FTU
from modules.pipelines import SayatPipeline, NaglahPipeline


ftu1 = FTU({'name': 'ftu1'})
ftu2 = FTU({'name': 'ftu2'})
ftu3 = FTU({'name': 'ftu3'})
ftu4 = FTU({'name': 'ftu4'})

ftus = [ftu1, ftu2, ftu3, ftu4]

pipeline1 = SayatPipeline({"name": "experiment 1"})
pipeline2 = NaglahPipeline({"name": "experiment 2"})

pipeline1.run(ftus)
pipeline2.run(ftus)
