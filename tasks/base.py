# coding: utf-8

from __future__ import absolute_import

__all__ = ["BaseTask", "AnalysisTask", "CMSSWSandboxTask", "CHBase"]


import os

import luigi
import six
import law
from law.util import make_list

law.contrib.load("numpy", "tasks", "root")


class BaseTask(law.Task):
    version = luigi.Parameter(description="task version")

    output_collection_cls = law.SiblingFileCollection

    def local_path(self, *path):
        parts = [str(p) for p in self.store_parts() + path]
        return os.path.join(os.environ["DHA_STORE"], *parts)

    def local_target(self, *args):
        cls = law.LocalFileTarget if args else law.LocalDirectoryTarget
        return cls(self.local_path(*args))

    def local_directory_target(self, *args):
        return law.LocalDirectoryTarget(self.local_path(*args))


class AnalysisTask(BaseTask):

    task_namespace = "dha"

    def __init__(self, *args, **kwargs):
        super(AnalysisTask, self).__init__(*args, **kwargs)

    def store_parts(self):
        return (self.__class__.__name__, self.version)

    @classmethod
    def modify_param_values(cls, params):
        return params


class CMSSWSandboxTask(law.SandboxTask):
    @property
    def sandbox(self):
        return "bash::setup_cmssw.sh"


class CHBase(AnalysisTask, CMSSWSandboxTask):

    mass = luigi.Parameter(default="125")

    stable_options = r"--cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0"

    def store_parts(self):
        return super(CHBase, self).store_parts() + (self.mass,)

    @property
    def cmd(self):
        raise NotImplementedError

    def run(self):
        self.output().parent.touch()
        with self.publish_step(law.util.colored("{}:".format(self.cmd), color="light_cyan")):
            for line in law.util.readable_popen(
                self.cmd, shell=True, executable="/bin/bash", cwd=self.output().parent.path,
            ):
                if isinstance(line, str):
                    print(line)
                else:
                    process = line
                    if process.returncode != 0:
                        raise Exception("{} failed".format(self.cmd))
