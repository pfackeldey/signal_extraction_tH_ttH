# coding: utf-8

import law
import luigi
from tasks.base import CHBase, AnalysisTask


class CombDatacards(CHBase):

    input_cards = law.CSVParameter(
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
        return CombDatacards.req(self, mass=self.mass)

    def output(self):
        return self.local_target("workspace.root")

    @property
    def cmd(self):
        return "PYTHONPATH=$DHA_BASE/utils:$PYTHONPATH text2workspace.py {datacard} -o {workspace} -m {mass} -P models:HHdefault".format(
            datacard=self.input().path, workspace=self.output().path, mass=self.mass,
        )


class NLO(object):

    POI = luigi.Parameter(default="kl=1")

    def __init__(self, *args, **kwargs):
        super(NLO, self).__init__(*args, **kwargs)
        self.name, self.val = self.POI.split("=")
        self.params = "r,r_qqhh,r_gghh,CV,C2V,kl,kt"
        assert self.name in ("C2V", "kl")  # we only scan those 2
        self.freeze_params = ",".join([p for p in self.params.split(",") if p != self.name])
        self.set_params = ",".join([p + "=1" for p in self.freeze_params.split(",")])


class NLOLimit(NLO, CHBase):
    def requires(self):
        return NLOT2W.req(self)

    def output(self):
        return self.local_target("limit_{}.json".format(self.POI))

    @property
    def cmd(self):
        return (
            "combine -M AsymptoticLimits -v 1 {workspace} -m {mass} --run expected --noFitAsimov {stable_options} --redefineSignalPOIs r --setParameters {params} "
            "&& combineTool.py -M CollectLimits higgsCombineTest.AsymptoticLimits.mH{mass}.root -o {limit}".format(
                workspace=self.input().path,
                mass=self.mass,
                limit=self.output().path,
                stable_options=self.stable_options,
                params=",".join([self.set_params, self.POI]),
            )
        )


class NLOklLimits(AnalysisTask, law.WrapperTask):
    def requires(self):
        return [NLOLimit.req(self, POI="kl={}".format(v)) for v in range(-20, 21)]


class PlotklLimits(AnalysisTask):
    def requires(self):
        return {v: NLOLimit.req(self, POI="kl={}".format(v)) for v in range(-20, 21)}

    def output(self):
        return self.local_target("scan.pdf")

    def run(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import mplhep as hep

        self.output().parent.touch()

        data = [
            [kl] + [data[i] for i in range(-2, 3)]
            for kl, data in (
                (key, {int(k[3:]): v for k, v in inp.load()["125.0"].items()})
                for key, inp in sorted(self.input().items(), key=lambda x: x[0])
            )
        ]
        arr = np.array(data)
        plt.figure()
        hep.cms.cmslabel(loc=0)
        plt.plot(
            arr[:, 0], arr[:, 3], label="expected limit", color="black", linestyle="dashed",
        )
        plt.fill_between(
            arr[:, 0],
            arr[:, 5],
            arr[:, 1],
            color="yellow",
            label=r"2$\sigma$ expected",
            interpolate=True,
        )
        plt.fill_between(
            arr[:, 0],
            arr[:, 4],
            arr[:, 2],
            color="limegreen",
            label=r"1$\sigma$ expected",
            interpolate=True,
        )
        plt.legend(loc="upper left")
        plt.xlabel(r"$\kappa_\lambda$")
        plt.ylabel(r"95% CL on $\frac{\sigma}{\sigma_{SM}}$")
        plt.yscale("log")
        plt.grid()
        plt.savefig(self.output().path)
        plt.close()


class NLOC2VLimits(AnalysisTask, law.WrapperTask):
    def requires(self):
        return [NLOLimit.req(self, POI="C2V={}".format(v)) for v in range(-10, 11)]


class PlotC2VLimits(AnalysisTask):
    def requires(self):
        return {v: NLOLimit.req(self, POI="C2V={}".format(v)) for v in range(-10, 11)}

    def output(self):
        return self.local_target("scan.pdf")

    def run(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import mplhep as hep

        self.output().parent.touch()

        data = [
            [kl] + [data[i] for i in range(-2, 3)]
            for kl, data in (
                (key, {int(k[3:]): v for k, v in inp.load()["125.0"].items()})
                for key, inp in sorted(self.input().items(), key=lambda x: x[0])
            )
        ]
        arr = np.array(data)
        plt.figure()
        hep.cms.cmslabel(loc=0)
        plt.plot(
            arr[:, 0], arr[:, 3], label="expected limit", color="black", linestyle="dashed",
        )
        plt.fill_between(
            arr[:, 0],
            arr[:, 5],
            arr[:, 1],
            color="yellow",
            label=r"2$\sigma$ expected",
            interpolate=True,
        )
        plt.fill_between(
            arr[:, 0],
            arr[:, 4],
            arr[:, 2],
            color="limegreen",
            label=r"1$\sigma$ expected",
            interpolate=True,
        )
        plt.legend(loc="upper left")
        plt.xlabel(r"C2V")
        plt.ylabel(r"95% CL on $\frac{\sigma}{\sigma_{SM}}$")
        plt.yscale("log")
        plt.grid()
        plt.savefig(self.output().path)
        plt.close()


class NLOScan1D(NLO, CHBase):
    def requires(self):
        return NLOT2W.req(self)

    def output(self):
        return self.local_target("higgsCombineTest.MultiDimFit.mH{}.root".format(self.mass))

    @property
    def cmd(self):
        return "combine -M MultiDimFit -t -1 {workspace} -m {mass} {stable_options} --redefineSignalPOIs {POI} --setParameters {set_params} --freezeParameters {freeze_params} --algo grid".format(
            workspace=self.input().path,
            mass=self.mass,
            stable_options=self.stable_options,
            POI=self.name,
            set_params=self.set_params,
            freeze_params=self.freeze_params,
        )


class NLOScan2D(CHBase):
    def requires(self):
        return NLOT2W.req(self)

    def output(self):
        return self.local_target("higgsCombineTest.MultiDimFit.mH{}.root".format(self.mass))

    @property
    def cmd(self):
        return "combine -M MultiDimFit -t -1 {workspace} -m {mass} {stable_options} --redefineSignalPOIs CV,C2V --setParameters r=1,kl=1 --freezeParameters r,kl --algo grid".format(
            workspace=self.input().path, mass=self.mass, stable_options=self.stable_options,
        )
