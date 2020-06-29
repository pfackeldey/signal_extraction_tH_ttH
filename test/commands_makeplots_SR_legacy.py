#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE


# python test/commands_makeplots_SR_legacy.py --cards_dir /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_22June20_unblinded/ --odir /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_22June20_unblinded/postfit_plots --fitDiagnosis /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_22June20_unblinded/results/fitDiagnosticsrobusthesse.root --unblided --doPostFit
from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--odir",
    type="string",
    dest="odir",
    help="Full path of where to put the plots",
    default="none"
    )
parser.add_option(
    "--cards_dir",
    type="string",
    dest="cards_dir",
    help="Full path of where the original datacards.txt/root are (to take templates)"
    )
parser.add_option(
    "--fitDiagnosis",
    type="string",
    dest="fitDiagnosis",
    help="Full path of fitDiagnosis.root"
    )
parser.add_option(
    "--fitDiagnosis_ITC",
    type="string",
    dest="fitDiagnosis_ITC",
    help="Full path of fitDiagnosis_ITC.root",
    default="none"
    )
parser.add_option(
    "--do_channel",
    type="string",
    dest="do_channel",
    help="FDo only this channel",
    default="none"
    )
parser.add_option(
    "--unblided",
    action="store_true",
    dest="unblided",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--doPostFit",
    action="store_true",
    dest="doPostFit",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--doITC",
    action="store_true",
    dest="doITC",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--fromHavester",
    action="store_true",
    dest="fromHavester",
    help="Self explanatory",
    default=False
    )

(options, args) = parser.parse_args()

print ()

def run_cmd(command):
  print ("executing command = '%s'" % command)
  p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
  stdout, stderr = p.communicate()
  return stdout

odir         = options.odir
fitDiagnosis = options.fitDiagnosis
cards_dir    = options.cards_dir
doPostFit    = options.doPostFit
unblided     = options.unblided
fromHavester = options.fromHavester
doITC        = options.doITC
do_channel   = options.do_channel
fitDiagnosis_ITC = options.fitDiagnosis_ITC

if odir == "none" :
    odir = cards_dir + "/plots"
run_cmd("mkdir %s"  % (odir))

eras = [  2018] # 0 , 2016, 2017,

cards_to_do = {
        "ttH_0l_2tau_ERA"         : {
            "original"          : "ttH_0l_2tau_ERA", # name of the datacard(.txt/.root) to take binX templates
            "binToReadOriginal" : "ttH_0l_2tau",               # if the datacard(.txt/.root) has a subfolder this is the name of the subfolder
            "IHEP"              : False ,                      # True if the datacard(.txt/.root) has no subfolder
            "channel"           : "0l_2tau",                   # to take the plot options of the options_plot_ranges function on configs/plot_options.py
            "binToRead"         : "ttH_0l_2tau_ERA",           # bin inside the fitDiagnosis, assumes that you use test/combine_cards_legacy_CR.py to merge cards before doing it
            "nameLabel"         : "none",                      # if you want to overwrite the option on plot options of the options_plot_ranges function on configs/plot_options.py
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_1l_1tau_ERA"         : {
            "original"          : "ttH_1l_1tau_ERA",
            "binToReadOriginal" : "ttH_1l_1tau",
            "IHEP"              : False ,
            "channel"           : "1l_1tau",
            "binToRead"         : "ttH_1l_1tau_ERA",
            "nameLabel"         : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_1l_2tau_ERA"         : {
            "original"          : "ttH_1l_2tau_ERA",
            "binToReadOriginal" : "ttH_1l_2tau",
            "IHEP"              : False ,
            "channel"           : "1l_2tau",
            "binToRead"         : "ttH_1l_2tau_ERA",
            "nameLabel"         : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_2los_1tau_ERA"         : {
            "original"          : "ttH_2los_1tau_ERA",
            "binToReadOriginal" : "ttH_2los_1tau",
            "IHEP"              : False ,
            "channel"           : "2los_1tau",
            "binToRead"         : "ttH_2los_1tau_ERA",
            "nameLabel"         : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "tH_2l_2tau_ERA"           : {
            "original"  : "none" ,
            "channel"   : "2l_2tau",
            "IHEP"      : False ,
            "binToRead" : "ttH_2l_2tau_ERA",
            "nameLabel" : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_3l_1tau_ERA"          : {
            "original"  : "none" ,
            "channel"   : "3l_1tau",
            "IHEP"      : False ,
            "binToRead" : "ttH_3l_1tau_ERA",
            "nameLabel" : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_4l_ERA"          : {
            "original"  : "none" ,
            "channel"   : "4l_0tau",
            "IHEP"      : False ,
            "binToRead" : "ttH_4l_ERA",
            "nameLabel" : "none",
            "fitDiagnosis_ITC"  : "none"
        },
        "ttH_cr_3l_ERA_cr"   : {
            #"cards_to_merge"      : ["ttH_cr_3l_ERA_eee_cr", "ttH_cr_3l_ERA_eem_cr", "ttH_cr_3l_ERA_emm_cr", "ttH_cr_3l_ERA_mmm_cr"],
            "channel"             : "3lctrl",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none",
            "fitDiagnosis_ITC"    : "none"
        },
        "ttH_cr_4l_ERA"   : {
            #"cards_to_merge"      : ["ttH_cr_3l_ERA_eee_cr", "ttH_cr_3l_ERA_eem_cr", "ttH_cr_3l_ERA_emm_cr", "ttH_cr_3l_ERA_mmm_cr"],
            "channel"             : "4lctrl",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_2lss_1tau_ERA"      : {
            #"cards_to_merge"      : ["ttH_2lss_1tau_rest_ERA", "ttH_2lss_1tau_tH_ERA", "ttH_2lss_1tau_ttH_ERA"],
            "channel"             : "2lss_1tau",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_2lss_0tau_rest_ERA" : {
            #"cards_to_merge"      : ["ttH_2lss_0tau_ee_Restnode_ERA", "ttH_2lss_0tau_em_Restnode_ERA", "ttH_2lss_0tau_mm_Restnode_ERA" ],
            "channel"             : "2lss_0tau_rest",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_2lss_0tau_tH_ERA"   : {
            #"cards_to_merge"      : ["ttH_2lss_0tau_ee_tHQnode_ERA", "ttH_2lss_0tau_em_tHQnode_ERA", "ttH_2lss_0tau_mm_tHQnode_ERA"],
            "channel"             : "2lss_0tau_tH",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_2lss_0tau_ttH_ERA"  : {
            #"cards_to_merge"      : ["ttH_2lss_0tau_ee_ttHnode_ERA", "ttH_2lss_0tau_em_ttHnode_ERA", "ttH_2lss_0tau_mm_ttHnode_ERA"],
            "channel"             : "2lss_0tau_ttH",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_2lss_0tau_ttW_ERA"  : {
            #"cards_to_merge"      : ["ttH_2lss_0tau_ee_ttWnode_ERA", "ttH_2lss_0tau_em_ttWnode_ERA", "ttH_2lss_0tau_mm_ttWnode_ERA" ],
            "channel"             : "2lss_0tau_ttW",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_3l_0tau_rest_ERA"   : {
            #"cards_to_merge"      : ["ttH_3l_0tau_rest_eee_ERA", "ttH_3l_0tau_rest_eem_bl_ERA", "ttH_3l_0tau_rest_eem_bt_ERA", "ttH_3l_0tau_rest_emm_bl_ERA", "ttH_3l_0tau_rest_emm_bt_ERA", "ttH_3l_0tau_rest_mmm_bl_ERA", "ttH_3l_0tau_rest_mmm_bt_ERA"],
            "channel"             : "3l_0tau_rest",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_3l_0tau_tH_ERA"     : {
            #"cards_to_merge"      : ["ttH_3l_0tau_tH_bl_ERA", "ttH_3l_0tau_tH_bt_ERA"],
            "channel"             : "3l_0tau_tH",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_3l_0tau_ttH_ERA"    : {
            #"cards_to_merge"      : ["ttH_3l_0tau_ttH_bl_ERA", "ttH_3l_0tau_ttH_bt_ERA"],
            "channel"             : "3l_0tau_ttH",
            "original"            : "none" ,
            "IHEP"                : False ,
            "binToRead"           : "none",
            "nameLabel"           : "none"
        },
        "ttH_1l_1tau_ERA"         : {
            "original"          : "ttH_1l_1tau_ERA",
            "binToReadOriginal" : "ttH_1l_1tau",
            "IHEP"              : False ,
            "channel"           : "1l_1tau",
            "binToRead"         : "ttH_1l_1tau_ERA",
            "nameLabel"         : "none"
        },
        "ttH_1l_2tau_ERA"         : {
            "original"          : "ttH_1l_2tau_ERA",
            "binToReadOriginal" : "ttH_1l_2tau",
            "IHEP"              : False ,
            "channel"           : "1l_2tau",
            "binToRead"         : "ttH_1l_2tau_ERA",
            "nameLabel"         : "none"
        },

}

for era in eras :
    for key in cards_to_do :
        if doITC and not ( "3l_0tau" in key or "2lss_0tau" in key or "2lss_1tau" in key) :
            continue
        if not do_channel == "none" and not do_channel in key :
            continue
        print (key, era)
        eraDraw = str(era)
        if era == 0 :
            eraDraw = "2018"
        cmd = "python test/makePlots.py "
        cmd += "--input %s " % fitDiagnosis
        cmd += "--odir %s " % odir
        if not cards_to_do[key]["original"] == "none" :
            cmd += "--original  %s/%s.root " % (cards_dir, cards_to_do[key]["original"].replace("ERA", eraDraw) )
            if cards_to_do[key]["IHEP"] :
                cmd += "--IHEP "
            else :
                cmd += "--binToReadOriginal %s " % cards_to_do[key]["binToReadOriginal"].replace("ERA", eraDraw)
        cmd += "--era %s " % str(era)
        cmd += "--nameOut %s " % key.replace("ERA", str(era))
        cmd += "--do_bottom "
        cmd += "--channel %s " % cards_to_do[key]["channel"].replace("ERA", eraDraw)
        if doPostFit :
            cmd += "--doPostFit "
        if not cards_to_do[key]["binToRead"] == "none" :
            cmd += "--binToRead %s " % cards_to_do[key]["binToRead"].replace("ERA", eraDraw)
        if unblided :
            cmd += "--unblind "
        if not cards_to_do[key]["nameLabel"] == "none" :
            cmd += "--nameLabel \"%s\" " % cards_to_do[key]["nameLabel"]
        if fromHavester :
            cmd += "--fromHavester "
        # # --tH_separate --input_ITC fitDiagnosis_ITC
        if not fitDiagnosis_ITC == "none" :
            cmd += " --tH_separate --input_ITC %s " % fitDiagnosis_ITC
        #print (cmd)
        output = run_cmd(cmd)
        ff = open("%s/%s.log" % (odir, key.replace("ERA", str(era))) ,"w+")
        ff.write(output)
        ff.close()
