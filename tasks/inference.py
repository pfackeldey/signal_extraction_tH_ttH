# coding: utf-8

import law
import luigi
from tasks.base import CHBase


class CombDatacards(CHBase):

    input_cards = law.CSVParameter(
        default="/net/scratch/cms/dihiggs/store/bbww_dl/Run2_pp_13TeV_2017/DatacardProducer/dev1/jet1_pt/ee/datacard.txt,/net/scratch/cms/dihiggs/store/bbww_dl/Run2_pp_13TeV_2017/DatacardProducer/dev1/jet1_pt/mumu/datacard.txt",
        description="Path to input datacards, comma seperated:"
        "e.g.: '/path/to/card1.txt,/path/to/card2.txt,...'",
    )

    def output(self):
        return self.local_target("datacard.txt")

    @property
    def cmd(self):
        return "combineCards.py {datacards} > {out}".format(
            datacards=" ".join(self.input_cards), out=self.output().path,
        )


class NLOT2W(CHBase):
    def requires(self):
        return CombDatacards.req(self, channels=self.channels, mass=self.mass)

    def output(self):
        return self.local_target("workspace.root")

    @property
    def cmd(self):
        return "PYTHONPATH=$DHA_BASE/utils:$PYTHONPATH text2workspace.py {datacard} -o {workspace} -m {mass} -P models:HHdefault".format(
            datacard=self.input().path, workspace=self.output().path, mass=self.mass,
        )


class NLOLimit(CHBase):

    coupling_modifier = law.CSVParameter(
        default=("r_gghh=1", "r_qqhh=1", "kt=1", "kl=1", "CV=1", "C2V=3")
    )

    def requires(self):
        return NLOT2W.req(self)

    def output(self):
        return self.local_target(
            "limit_{}.json".format("_".join(self.coupling_modifier))
        )

    @property
    def cmd(self):
        return (
            "combine -M AsymptoticLimits -v 1 {workspace} -m {mass} --run expected --noFitAsimov {stable_options} --redefineSignalPOIs r --setParameters {coupling_modifier} "
            "&& combineTool.py -M CollectLimits higgsCombineTest.AsymptoticLimits.mH125.root -o {limit}".format(
                workspace=self.input().path,
                mass=self.mass,
                limit=self.output().path,
                stable_options=self.stable_options,
                coupling_modifier=",".join(self.coupling_modifier),
            )
        )


class NLOScan1D(CHBase):

    POI = luigi.Parameter(default="kl")

    def __init__(self, *args, **kwargs):
        super(NLOScan1D, self).__init__(*args, **kwargs)
        self.params = "r,r_qqhh,r_gghh,CV,C2V,kl,kt"
        assert self.POI in self.params.split(",")
        self.freeze_params = ",".join(
            [p for p in self.params.split(",") if p != self.POI]
        )
        self.set_params = ",".join([p + "=1" for p in self.freeze_params.split(",")])

    def requires(self):
        return NLOT2W.req(self)

    def output(self):
        return self.local_target(
            "higgsCombineTest.MultiDimFit.mH{}.root".format(self.mass)
        )

    @property
    def cmd(self):
        return "combine -M MultiDimFit -t -1 {workspace} -m {mass} {stable_options} --redefineSignalPOIs {POI} --setParameters {set_params} --freezeParameters {freeze_params} --algo grid".format(
            workspace=self.input().path,
            mass=self.mass,
            stable_options=self.stable_options,
            POI=self.POI,
            set_params=self.set_params,
            freeze_params=self.freeze_params,
        )
