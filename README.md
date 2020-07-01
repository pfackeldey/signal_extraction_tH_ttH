# signal_extraction_tH_ttH

Repository to keep all the scripts that make signal extraction and interpretation on ttH/tH multilepton analysis based on .txt combine-like datacards.

The different scripts need different setups to be loaded.
In the beggining of each script there is a note for which setup (type-1, type-2 or type-3) should be loaded.

* type-1) CMSSW_10X, to contain all the python packages -- nothing else needs to be installed on top.

* type-2) CMSSW with [Combine](https://github.com/cms-analysis/higgsanalysis-combinedlimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
) (at least v7.0.12)

```
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.12
scramv1 b clean; scramv1 b # always make a clean build
```

* type-3) CMSSW with Combine and CombineHavester

On top of the setup for type-2 scripts install CombineHavester:

```
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b
```

In case of KBFI use [this one](https://github.com/HEP-KBFI/CombineHarvester) instead.

## For standalone run of one combined datacard

See the README inside `test/`

## For kt-kv parameter scan (and eventually CP-angle scan)

See the README inside `test/kt_kv_scan/`


## NLO scans

### law

law is a tool, which lets you setup workflows: https://github.com/riga/law.

The setup is defined in `setup.sh` and `setup_cmssw.sh`. Before starting you need to set the proper path for data storage in `setup.sh`. Please change the "export DHA_DATA" environment variable to your specific computing setup: e.g. your local nfs.

Now we can start!

1. Setup law together with CMSSW 10_2_X:
```bash
source setup.sh
```

2. Let law index your tasks and their parameters (for autocompletion)
```bash
law index --verbose
```
You should see:
```bash
indexing tasks in 2 module(s)
loading module 'tasks.base', done
loading module 'tasks.inference', done

module 'tasks.base', 1 task(s):
    - dha.CHBase

module 'tasks.inference', 4 task(s):
    - dha.CombDatacards
    - dha.NLOT2W
    - dha.NLOLimit
    - dha.NLOScan1D

written 5 task(s) to index file 'example/path/.law/index'
```

3. Now we can check the status of our tasks:
```bash
law run dha.NLOScan1D --local-scheduler --version dev --print-status 2 --dha.CombDatacards-input-cards datacard1.txt,datacard2.txt
```  

IMPORTANT NOTE: you need to specify `--dha.CombDatacards-input-cards datacard1.txt,datacard2.txt`, where `datacard1.txt,datacard2.txt` are the comma seperated paths to your input datacards, which you want to combine.  

You should see, where `your/path` is set in setup.sh with `DHA_STORE`:
```bash
print task status with max_depth 2 and target_depth 0

> check status of dha.NLOScan1D(version=dev, channels=ee,emu,mumu, mass=125, POI=kl)
|  - LocalFileTarget(path=your/path/NLOScan1D/dev/higgsCombineTest.MultiDimFit.mH125.root)
|    absent
|
|  > check status of dha.NLOT2W(version=dev, channels=ee,emu,mumu, mass=125)
|  |  - LocalFileTarget(path=your/path/NLOT2W/dev/workspace.root)
|  |    absent
|  |
|  |  > check status of dha.CombDatacards(version=dev, channels=ee,emu,mumu, mass=125, input_cards=datacard1.txt,datacard2.txt)
|  |  |  - LocalFileTarget(path=your/path/CombDatacards/dev/datacard.txt)
|  |  |    absent
```
You see that the output of all tasks are "absent", which is obviously, because we have not run them yet!

4. Run the tasks! (Simply remove the `--print-status 2` cli argument; `2` denotes the tasks depth)

For doing the kappa lambda scan:
```bash
law run dha.NLOScan1D --local-scheduler --version dev --dha.CombDatacards-input-cards datacard1.txt,datacard2.txt --POI kl
```

For doing the C2V scan:
```bash
law run dha.NLOScan1D --local-scheduler --version dev --dha.CombDatacards-input-cards datacard1.txt,datacard2.txt --POI C2V
```

#### Additional information

You can clear the target outputs interactively by adding the `--remove-output` cli argument. It takes again a task depth as argument in the same way as `--print-status`. E.g. remove the output of the current task by adding `--remove-output`.
