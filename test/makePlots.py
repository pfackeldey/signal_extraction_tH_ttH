#!/usr/bin/env python
import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict

sys.stdout.flush()
sys.stdout.flush()

from ROOT import gROOT
#gROOT.SetBatch(1)

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--nameOut", type="string",
    dest="nameOut",
    help="To appear on the name of the file with the final plot",
    default="test"
    )
parser.add_option(
    "--input", type="string", dest="input",
    help="A valid file with the shapes as output of combine FitDiagnostics"#,
    #default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/ttH_fitDiagnostics.Test_shapes.root"
    )
parser.add_option(
    "--input_ITC", type="string", dest="input_ITC",
    help="A valid file with the shapes as output of combine FitDiagnostics",
    default="none"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output plots",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/"
    )
parser.add_option(
    "--original", type="string", dest="original",
    help="The original datacard: used only to rebin (the datacard.root)",
    default="none"
    )
parser.add_option(
    "--channel", type="string", dest="channel",
    help="Name of the category as it is appear on the input file",
    default="ttH_1l_2tau_OS"
    )
parser.add_option(
    "--typeCat", type="string", dest="typeCat",
    help="Name of the category as it is appear on the input file",
    default="none"
    )
parser.add_option(
    "--labelX", type="string", dest="labelX",
    help="To appear on final plot",
    default="none"
    )
parser.add_option(
    "--nameLabel", type="string", dest="nameLabel",
    help="To appear on final plot",
    default="none"
    )
parser.add_option(
    "--useLogPlot", action="store_true", dest="useLogPlot",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--divideByBinWidth", action="store_true", dest="divideByBinWidth",
    help="If final plot shall be done dividing bin content by bin width ",
    default=False
    )
parser.add_option(
    "--unblind", action="store_true", dest="unblind",
    help="Do subcategories from multilepton cards ",
    default=False
    )
parser.add_option(
    "--doPostFit", action="store_true", dest="doPostFit",
    help="Do the postfit instead of prefit ",
    default=False
    )
parser.add_option(
    "--minY", type="float", dest="minY",
    help="For the final plot",
    default=0.
    )
parser.add_option(
    "--maxY", type="float", dest="maxY",
    help="For the final plot",
    default=1.
    )
parser.add_option(
    "--fromHavester", action="store_true", dest="fromHavester",
    help="The input file is from CombineHavester. In this case you do not need to enter 'original' if you called the PostFitShapesFromWorkspace with the -d option",
    default=False
    )
parser.add_option(
    "--do_bottom", action="store_true", dest="do_bottom",
    help="If do bottom pad",
    default=False
    )
parser.add_option(
    "--IHEP", action="store_true", dest="IHEP",
    help="IHEP cards do not have directories",
    default=False
    )
parser.add_option(
    "--HH", action="store_true", dest="HH",
    help="is HH",
    default=False
    )
parser.add_option(
    "--tH_separated", action="store_true", dest="tH_separated",
    help="Draw tH not on the stack",
    default=False
    )
parser.add_option(
    "--era", type="int",
    dest="era",
    help="To appear on the name of the file with the final plot. If era == 0 it assumes you gave the path for the 2018 era and it will use the same naming convention to look for the 2017/2016.",
    default=2017
    )
parser.add_option(
    "--binToRead", type="string", dest="binToRead",
    help="Folder to read on the input root file -- if none it will try yo read all and put side by side.",
    default="none"
    )
parser.add_option(
    "--binToReadOriginal", type="string", dest="binToReadOriginal",
    help="Folder to read on the input root file -- if none it will try yo read all and put side by side.",
    default="none"
    )
(options, args) = parser.parse_args()

divideByBinWidth = options.divideByBinWidth
category         = options.channel
if options.typeCat == "none" :
    typeCat          = category
else :
    typeCat          = options.typeCat
print ("category", category, typeCat)
do_bottom = options.do_bottom
shapes_input = options.input
shapes_input_ITC = options.input_ITC
HH           = options.HH
tH_separated = options.tH_separated
input_ITC    = options.input_ITC

binToRead = options.binToRead
if binToRead == "none" :
    binToRead = "ttH_" +  category
print ("binToRead", binToRead)

binToReadOriginal = options.binToReadOriginal
if binToReadOriginal == "none" :
    binToReadOriginal = "ttH_" + category
print ("binToReadOriginal", binToReadOriginal)

print ("nameOut", options.nameOut)

labelY = "Events"
if divideByBinWidth : labelY = "Events / bin width"

if options.doPostFit :
    if not options.fromHavester :
        folder = "shapes_fit_s"
        folder_data = "shapes_fit_s" # it is a TGraphAsymmErrors, not histogram
        typeFit = "postfit"
    else :
        folder = binToRead + "_postfit"
        folder_data = binToRead + "_postfit" # it is a histogram
        typeFit = "postfit"
else :
    if not options.fromHavester :
        folder = "shapes_prefit"
        folder_data = "shapes_prefit" # it is a TGraphAsymmErrors, not histogram
        typeFit = "prefit"
    else :
        folder = binToRead + "_prefit"
        folder_data = binToRead + "_prefit" # it is a histogram
        typeFit = "prefit"
print ("folder", folder)

if not options.fromHavester : name_total = "total" # "total_background" # "total_covar" #
#elif not options.doPostFit : name_total = "TotalBkg"
else : name_total = "TotalProcs"

execfile("python/data_manager_makePostFitPlots.py")
ROOT.gStyle.SetOptStat(0)
###ROOT.gROOT.SetBatch(0) ---> it still does not solve in batch if 1, and break in iterative if 0

flips       = "data_flips"
conversions = "Convs"
fakes       = "data_fakes"

info_file = os.environ["CMSSW_BASE"] + "/src/signal_extraction_tH_ttH/configs/plot_options.py"
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)
procs  = list_channels_draw("ttH")[category]
print procs
leading_minor_H = list_channels_draw("ttH")[category]["leading_minor_H"]
print ("leading_minor_H", leading_minor_H)
if not HH :
    dprocs = options_plot ("ttH", category, procs["bkg_proc_from_data"] + procs['bkg_procs_from_MC'] + procs["signal"], leading_minor_H, False) # tH_separated
else :
    dprocs = options_plot ("ttH", category, procs["bkg_proc_from_data"] + procs['bkg_procs_from_MC'], leading_minor_H, False) # tH_separated
    dprocsHH = options_plot ("ttH", category,  procs["signal_HH"], "HH", tH_separated)

label_head = options_plot_ranges("ttH")[typeCat]["label"]
print (options_plot_ranges("ttH")[typeCat])
if options.doPostFit :
    list_cats = options_plot_ranges("ttH")[typeCat]["list_cats"]
else :
    list_cats = options_plot_ranges("ttH")[typeCat]["list_cats_original"]

if not options.nameLabel == "none" :
    label_head += options.nameLabel

if typeFit == "prefit" :
    label_head = label_head+", \n"+typeFit
else :
    label_head = label_head+", #mu(t#bar{t}H)=#hat{#mu}"

if not options.labelX == "none" :
    labelX = options.labelX
elif typeCat in options_plot_ranges("ttH").keys() :
    labelX = options_plot_ranges("ttH")[typeCat]["labelX"]
else : labelX = "BDT"

print ("will draw processes", list(dprocs.keys()))

if not options.original == "none" :
    fileOrig = options.original
else :
    fileOrig = shapes_input
print ("template on ", fileOrig)

era = options.era

minY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() : minY = options_plot_ranges("ttH")[typeCat]["minY"]
else : minY = options.minY

maxY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() :
        maxY = options_plot_ranges("ttH")[typeCat]["maxY"]
else : maxY = options.maxY
if options.era == 0 :
    maxY = 2 * maxY

print("reading shapes from: ", shapes_input)
fin = [ROOT.TFile(shapes_input, "READ")]
if options.era == 0 :
    fin = fin + [ROOT.TFile(shapes_input.replace("2018", "2017"), "READ")]
    fin = fin + [ROOT.TFile(shapes_input.replace("2018", "2016"), "READ")]
    print ("will sum up " + str(len(fin)) + " eras")
    print (shapes_input.replace("2018", "2017"))
    print (shapes_input.replace("2018", "2016"))

if not options.original == "none" :
    if not binToRead == "none" :
        catcats =  [binToRead]
    else :
        catcats = getCats(folder, fin[0], options.fromHavester)
    if options.IHEP :
        readFrom = ""
    elif not binToReadOriginal == "none" :
        readFrom =  binToReadOriginal + "/"
    else :
        readFrom =  "ttH_" + category + "/"
    print ("original readFrom ", readFrom)
    fileorriginal = ROOT.TFile(fileOrig, "READ")
    if options.IHEP :
        histRead = "x_TTZ"
    elif HH :
        histRead = "TTH"
    else :
        histRead = "TTW" #"ttH_htt"
    template = fileorriginal.Get(readFrom + histRead )
    template.GetYaxis().SetTitle(labelY)
    template.SetTitle(" ")
    nbinscatlist = [template.GetNbinsX()]
    datahist = fileorriginal.Get(readFrom + "data_obs")
else :
    if not binToRead == "none" :
        if len(list_cats) == 1 :
            catcats = [binToRead] #[folder]
        else :
            if not options.era == 0 :
                catcats = [ cat.replace("2018", str(era)) for cat in list_cats]
            else :
                catcats = [ cat for cat in list_cats]
    else :
        if len(list_cats) == 0 :
            catcats = getCats(folder, fin[0], options.fromHavester)
        else :
            if options.era == 0 :
                catcats = list_cats
            else :
                catcats = [ cat.replace("2018", str(era)) for cat in list_cats]
    #catcats = [binToRead]
    print("Drawing: ", catcats)
    nbinstotal = 0
    nbinscatlist = []
    for catcat in catcats :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        hist = fin[0].Get(readFrom + "/" + name_total )
        print ("reading shapes", readFrom + "/" + name_total)
        print (hist.Integral())
        nbinscat =  GetNonZeroBins(hist)
        nbinscatlist += [nbinscat]
        print (readFrom, nbinscat)
        nbinstotal += nbinscat
        datahist = fin[0].Get(readFrom + "/data")
    template = ROOT.TH1F("my_hist", "", nbinstotal, 0 - 0.5 , nbinstotal - 0.5)
    template.GetYaxis().SetTitle(labelY)
    print (nbinscatlist)

legend_y0 = 0.645
legend1 = ROOT.TLegend(0.2400, legend_y0, 0.9450, 0.910)
legend1.SetNColumns(3)
legend1.SetFillStyle(0)
legend1.SetBorderSize(0)
legend1.SetFillColor(10)
legend1.SetTextSize(0.040)
print label_head
legend1.SetHeader(label_head)
header = legend1.GetListOfPrimitives().First()
header.SetTextSize(.05)
header.SetTextColor(1)
header.SetTextFont(62)

if options.unblind :
    dataTGraph1 = "NoneType"
    if not options.fromHavester :
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        dataTGraph1.Set(template.GetXaxis().GetNbins())
    else :
        dataTGraph1 = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        print( " histtotal ", readFrom + "/" + name_total )
        histtotal = fin[0].Get(readFrom + "/" + name_total )
        lastbin += rebin_data(
            template,
            dataTGraph1,
            readFrom,
            fin,
            options.fromHavester,
            lastbin,
            histtotal,
            nbinscatlist[cc]
            )
    dataTGraph1.Draw()
    legend1.AddEntry(dataTGraph1, "Data", "p")
hist_total = template.Clone()

lastbin = 0
for cc, catcat in enumerate(catcats) :
    if not options.fromHavester :
        readFrom = folder + "/" + catcat
    else :
        readFrom = catcat
        readFrom += "_prefit"
    print ("read the hist with total uncertainties", readFrom, catcat)
    lastbin += rebin_total(
        hist_total,
        readFrom,
        fin,
        divideByBinWidth,
        name_total,
        lastbin,
        do_bottom,
        labelX,
        nbinscatlist[cc]
        )

if do_bottom :
    canvas = ROOT.TCanvas("canvas", "canvas", 600, 1500)
else :
    canvas = ROOT.TCanvas("canvas", "canvas", 900, 900)
canvas.SetFillColor(10)
canvas.SetBorderSize(2)
dumb = canvas.Draw()
del dumb

if do_bottom :
    topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.34, 1.00, 0.995)
    topPad.SetFillColor(10)
    topPad.SetTopMargin(0.075)
    topPad.SetLeftMargin(0.20)
    topPad.SetBottomMargin(0.053)
    topPad.SetRightMargin(0.04)
    if options.useLogPlot or options_plot_ranges("ttH")[typeCat]["useLogPlot"]:
        topPad.SetLogy()

    bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.05, 1.00, 0.34)
    bottomPad.SetFillColor(10)
    bottomPad.SetTopMargin(0.036)
    bottomPad.SetLeftMargin(0.20)
    bottomPad.SetBottomMargin(0.35)
    bottomPad.SetRightMargin(0.04)
else :
    topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.05, 1.00, 0.995)
    topPad.SetFillColor(10)
    topPad.SetTopMargin(0.075)
    topPad.SetLeftMargin(0.20)
    topPad.SetBottomMargin(0.1)
    topPad.SetRightMargin(0.04)
    if options.useLogPlot or options_plot_ranges("ttH")[typeCat]["useLogPlot"]:
        topPad.SetLogy()
####################################
canvas.cd()
dumb = topPad.Draw()
del dumb
topPad.cd()
del topPad
dumb = hist_total.Draw("axis")

del dumb
histogramStack_mc = ROOT.THStack()
print ("list of processes considered and their integrals")

linebin = []
linebinW = []
poslinebinW_X = []
pos_linebinW_Y = []
y0 = options_plot_ranges("ttH")[typeCat]["position_cats"]
if options.era == 0 :
    y0 = 2 * y0
for kk, key in  enumerate(dprocs.keys()) :
    hist_rebin = template.Clone()
    lastbin = 0
    addlegend = True
    print("Stacking ", key)
    for cc, catcat in enumerate(catcats) :
        if not cc == 0 : addlegend = False
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        info_hist = rebin_hist(
            hist_rebin,
            fin,
            readFrom,
            key,
            dprocs[key],
            divideByBinWidth,
            addlegend,
            lastbin,
            nbinscatlist[cc],
            options.original
            )
        print (info_hist["lastbin"] , lastbin, nbinscatlist[cc] )
        lastbin += info_hist["lastbin"]
        if kk == 0 :
            print (info_hist)
            print ("info_hist[binEdge]", info_hist["binEdge"])
            if info_hist["binEdge"] > 0 :
                linebin += [ROOT.TLine(info_hist["binEdge"], 0., info_hist["binEdge"], y0*1.1)] # (legend_y0 + 0.05)*maxY
            x0 = float(lastbin - info_hist["labelPos"] - 1)
            sum_inX = 0.1950
            if len(catcat) > 2 :
                if len(catcat) == 3 :
                    sum_inX = 5.85
                else :
                    sum_inX = 4.0
            if len(catcat) == 0 :
                poslinebinW_X += [x0 - sum_inX]
            else :
                poslinebinW_X += [options_plot_ranges("ttH")[typeCat]["catsX"][cc]]
            pos_linebinW_Y += [y0]
    if hist_rebin == 0 or not hist_rebin.Integral() > 0 or (info_hist["labelPos"] == 0 and not options.original == "none" )  : # : (info_hist["labelPos"] == 0 and not options.original == "none" )
        continue
    print (key,  0 if hist_rebin == 0 else hist_rebin.Integral() )
    ####
    """
    CX_ITC_o_SM_tHq = 0.7927/0.07096
    CX_ITC_o_SM_tHW = 0.1472/0.01561
    ####
    #hist_rebin.Scale(1.18)
    if "tHq" in key :
        hist_rebin.Scale(CX_ITC_o_SM_tHq)
    if "tHW" in key :
        hist_rebin.Scale(CX_ITC_o_SM_tHW)
    """
    dumb = histogramStack_mc.Add(hist_rebin)
    del dumb

if HH :
    #"""
    histHH = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        print ("read the hist with total uncertainties", readFrom, catcat)
        lastbin += rebin_total(
            histHH,
            readFrom,
            fin,
            divideByBinWidth,
            #"signal_ggf_nonresonant_hh_bbvvSM",
            "signal_ggf_nonresonant_hh_bbvv_slkl_1p00",
            #"signal_ggf_spin0_900_hh_bbvv_sl",
            lastbin,
            do_bottom,
            labelX,
            nbinscatlist[cc]
            )
    #fin[0].Get("shapes_prefit/HH_2l_0tau/signal_ggf_nonresonant_hh_bbvvSM")
    # "color" : 8, "fillStype" : 3315,
    histHH.SetMarkerSize(0)
    histHH.SetLineWidth(3)
    histHH.SetFillColor(1)
    histHH.SetLineColor(1)
    histHH.SetFillStyle(3315)
    #histHH.Scale(1.18)
    legend1.AddEntry(histHH, "HH SM bbvv sl", "f")
    print("HH SM bbvv sl", histHH.Integral())
    ###
    #histHH2 = fin[0].Get("shapes_prefit/HH_2l_0tau/signal_ggf_nonresonant_hh_bbttSM")
    histHH2 = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        print ("read the hist with total uncertainties", readFrom, catcat)
        lastbin += rebin_total(
            histHH2,
            readFrom,
            fin,
            divideByBinWidth,
            #"signal_ggf_nonresonant_hh_bbttSM",
            "signal_ggf_nonresonant_hh_bbttkl_1p00",
            #"signal_ggf_spin0_900_hh_bbtt",
            lastbin,
            do_bottom,
            labelX,
            nbinscatlist[cc]
            )
    # "color" : 8, "fillStype" : 3315,
    histHH2.SetMarkerSize(0)
    histHH2.SetLineWidth(3)
    histHH2.SetFillColor(4)
    histHH2.SetLineColor(4)
    histHH2.SetFillStyle(3351)
    #histHH2.Scale(1.18)
    legend1.AddEntry(histHH2, "HH SM bbtt", "f")
    print("HH SM bbtt", histHH2.Integral())
    ##
    histHH3 = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
            readFrom += "_prefit"
        print ("read the hist with total uncertainties", readFrom, catcat)
        lastbin += rebin_total(
            histHH3,
            readFrom,
            fin,
            divideByBinWidth,
            #"signal_ggf_nonresonant_hh_bbttSM",
            "signal_ggf_nonresonant_hh_bbvvkl_1p00",
            #"signal_ggf_spin0_900_hh_bbvv",
            lastbin,
            do_bottom,
            labelX,
            nbinscatlist[cc]
            )
    # "color" : 8, "fillStype" : 3315,
    histHH3.SetMarkerSize(0)
    histHH3.SetLineWidth(3)
    histHH3.SetFillColor(8)
    histHH3.SetLineColor(8)
    histHH3.SetFillStyle(3351)
    #histHH3.Scale(1.18)
    legend1.AddEntry(histHH3, "HH SM bbvv dl", "f")
    print("HH SM bbvv dl", histHH3.Integral())
    #"""

if tH_separated :
    histogramtH = [ROOT.TH1F(), ROOT.TH1F()]
    CX_ITC_o_SM_tHq = 0.7927/0.07096
    CX_ITC_o_SM_tHW = 0.1472/0.01561

    files_read = [ fin ]
    if not input_ITC == "none" :
        print ('getting ITC shape')
        fin_tH = [ROOT.TFile(shapes_input_ITC, "READ")]
        if options.era == 0 :
            fin_tH = fin_tH + [ROOT.TFile(shapes_input_ITC.replace("2018", "2017"), "READ")]
            fin_tH = fin_tH + [ROOT.TFile(shapes_input_ITC.replace("2018", "2016"), "READ")]
            print ("will sum up " + str(len(fin)) + " eras")
            print (shapes_input.replace("2018", "2017"))
            print (shapes_input.replace("2018", "2016"))
        files_read += [ fin_tH ]
    print (len (files_read))
    dprocs_tH = options_plot_tH ("ttH", category, procs["bkg_proc_from_data"] + procs['bkg_procs_from_MC'] + procs["signal"])
    for  mm, mmm in enumerate(files_read) : #
      #histogramStack_mc_tH = ROOT.THStack()
      hSumAll = ROOT.TH1F()
      for kk, key in enumerate( ["tHW_hzz", "tHW_htt", "tHW_hww", "tHq_hzz", "tHq_htt", "tHq_hww"] ) :
        hist_rebin2 = template.Clone()
        lastbin = 0
        for cc, catcat in enumerate(catcats) :
            if not options.fromHavester :
                readFrom = folder + "/" + catcat
            else :
                readFrom = catcat
                readFrom += "_prefit"
            if not cc == 0 :
                addlegend = False
            info_hist2 = rebin_hist(
                hist_rebin2,
                files_read[mm],
                readFrom,
                key,
                dprocs_tH[key],
                divideByBinWidth,
                addlegend,
                lastbin,
                nbinscatlist[cc],
                options.original
                )
            print("tH stack", key, hist_rebin2.Integral())
            print (info_hist2["lastbin"] , lastbin, nbinscatlist[cc] )
            lastbin += info_hist2["lastbin"]
            if kk == 0 :
                print (info_hist2)
                print ("info_hist[binEdge]", info_hist["binEdge"])
                if info_hist["binEdge"] > 0 :
                    linebin += [ROOT.TLine(info_hist2["binEdge"], 0., info_hist2["binEdge"], y0*1.1)] # (legend_y0 + 0.05)*maxY
                x0 = float(lastbin - info_hist2["labelPos"] - 1)
                sum_inX = 0.1950
                if len(catcat) > 2 :
                    if len(catcat) == 3 :
                        sum_inX = 5.85
                    else :
                        sum_inX = 4.0
                if len(catcat) == 0 :
                    poslinebinW_X += [x0 - sum_inX]
                else :
                    poslinebinW_X += [options_plot_ranges("ttH")[typeCat]["catsX"][cc]]
                pos_linebinW_Y += [y0]
        if hist_rebin2 == 0 or not hist_rebin2.Integral() > 0 or (info_hist2["labelPos"] == 0 and not options.original == "none" )  :
            continue
        print (key,  0 if hist_rebin2 == 0 else hist_rebin2.Integral() )
        if mm == 1 :
            if "tHq" in key : hist_rebin2.Scale(CX_ITC_o_SM_tHq)
            if "tHW" in key: hist_rebin2.Scale(CX_ITC_o_SM_tHW)
        if not hSumAll.Integral() > 0 :
            hist_rebin2.SetLineWidth(4)
            hSumAll = hist_rebin2.Clone()
        else :
            hSumAll.Add(hist_rebin2)
      histogramtH[mm] = hSumAll #.Clone()
      histogramtH[mm].SetFillStyle(3315)

    for  mm, mmm in enumerate(files_read) :
        print ('getting tH shape: ', files_read[mm], histogramtH[mm].Integral())
        if mm == 0 :
            #histogramtH[mm].SetLineColor(dprocs_tH[key]["color"])
            histogramtH[mm].SetLineColor(1)
            histogramtH[mm].SetFillColor(1)
            #histogramtH[mm].SetFillStyle(3315)
            #histogramtH[mm].SetLineStyle(9)
            #histogramtH[mm].Scale(10.)
            #legend1.AddEntry(histogramtH[mm], "tH (SM)*10", "f")
            legend1.AddEntry(histogramtH[mm], "tH (SM)", "f")
        if mm == 1 :
            histogramtH[mm].SetLineColor(8)
            histogramtH[mm].SetFillColor(8)
            #histogramtH[mm].Scale(20.)
            #histogramtH[mm].SetFillStyle(3315)
            #histogramtH[mm].Scale(100.)
            histogramtH[mm].SetLineStyle(9)
            #legend1.AddEntry(histogramtH[mm], "tH (ITC)*100", "f")
            legend1.AddEntry(histogramtH[mm], "tH (ITC)", "f")
    #"""


for line1 in linebin :
    line1.SetLineColor(1)
    line1.SetLineStyle(3)
    line1.Draw()

dumb = hist_total.Draw("axis,same")
dumb = histogramStack_mc.Draw("hist,same")
del dumb
dumb = hist_total.Draw("e2,same")
del dumb
if HH :
    #dumb = histogramStack_mcHH.Draw("hist,same")
    #del dumb
    dumb = histHH.Draw("hist,same")
    dumb = histHH2.Draw("hist,same")
    dumb = histHH3.Draw("hist,same")
    del dumb
if options.unblind :
    dumb = dataTGraph1.Draw("e1P,same")
    del dumb
dumb = hist_total.Draw("axis,same")
del dumb
if tH_separated  :
    for mm, mmm in enumerate(histogramtH) :
        print ("Drawing tH ", mm)
        mmm.Draw("hist,same")


dumb = legend1.Draw("same")
del dumb

labels = addLabel_CMS_preliminary(options.era)
for ll, label in enumerate(labels) :
    print ("printing label", ll)
    if ll == 0 :
        dumb = label.Draw("same")
        del dumb
    else :
        dumb = label.Draw()
        del dumb

for cc, cat in enumerate(options_plot_ranges("ttH")[typeCat]["cats"]) :
    print ("Draw label cat", cat, cc)
    sumBottom = 0
    for ccf, cf in enumerate(cat) :
        linebinW = ROOT.TLatex()
        linebinW.DrawLatex(poslinebinW_X[cc], pos_linebinW_Y[cc] + sumBottom, cf)
        linebinW.SetTextFont(50)
        linebinW.SetTextAlign(12)
        linebinW.SetTextSize(0.05)
        linebinW.SetTextColor(1)
        if era == 0 :
            sumBottom += -4.4
        else :
            sumBottom += -2.4

legend1.AddEntry(hist_total, "Uncertainty", "f")

#################################
if do_bottom :
    canvas.cd()
    dumb = bottomPad.Draw()
    del dumb
    bottomPad.cd()
    bottomPad.SetLogy(0)
    print ("doing bottom pad")
    hist_total_err = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            readFrom = catcat
        histtotal = hist_total
        lastbin += do_hist_total_err(
            hist_total_err,
            labelX, histtotal  ,
            options_plot_ranges("ttH")[typeCat]["minYerr"],
            options_plot_ranges("ttH")[typeCat]["maxYerr"],
            era
            )
        print (readFrom, lastbin)
    dumb = hist_total_err.Draw("e2")
    del dumb
    if options.unblind :
        if not options.fromHavester :
            dataTGraph2 = ROOT.TGraphAsymmErrors()
        else :
            dataTGraph2 = template.Clone()
        lastbin = 0
        for cc, catcat in enumerate(catcats) :
            if not options.fromHavester :
                readFrom = folder + "/" + catcat
            else :
                readFrom = catcat
            histtotal = fin[0].Get((readFrom + "/" + name_total).replace("2018", str(era)) )
            lastbin += err_data(
                dataTGraph2,
                hist_total,
                dataTGraph1,
                options.fromHavester,
                hist_total,
                readFrom,
                fin[0])
        dumb = dataTGraph2.Draw("e1P,same")
        del dumb
    line = ROOT.TF1("line", "0", hist_total_err.GetXaxis().GetXmin(), hist_total_err.GetXaxis().GetXmax())
    line.SetLineStyle(3)
    line.SetLineColor(ROOT.kBlack)
    dumb = line.Draw("same")
    del dumb
    print ("done bottom pad")
    del bottomPad
##################################
oplin = "linear"
if options.useLogPlot :
    oplin = "log"
    print ("made log")
optbin = "plain"
if divideByBinWidth :
    optbin = "divideByBinWidth"

savepdf = options.odir+category+"_"+typeFit+"_"+optbin+"_"+options.nameOut+"_unblind"+str(options.unblind)+"_"+oplin + "_" + options.typeCat
print ("saving...", savepdf )
dumb = canvas.SaveAs(savepdf + ".pdf")
print ("saved", savepdf + ".pdf")
del dumb
if not HH :
    dumb = canvas.Print(savepdf + ".root")
    print ("saved", savepdf + ".root")
    del dumb
canvas.IsA().Destructor(canvas)
#dumb = canvas.SaveAs(savepdf + ".png")
#print ("saved", savepdf + ".png")
#del dumb
#print ("saved", savepdf)
