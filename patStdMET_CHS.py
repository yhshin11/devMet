import FWCore.ParameterSet.Config as cms

process = cms.Process('MET')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')



### =========== Global configuration ==========================

## MET flavor configuration -> may be time consuming
## NoPu and MVA met need to be generated with some refeernce objects (e;g. leptons)
## look for the corresponding area in the config file to set your own definition


### ===========================================================
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValProdTTbar/AODSIM/START72_V1-v1/00000/84686BF3-AC30-E411-B9A8-00261894391C.root"
"root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValZMM_13/GEN-SIM-RECO/PU50ns_POSTLS172_V4-v1/00000/1823742B-8730-E411-9EAB-0025905A60DA.root"
#  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre6/RelValZMM_13/GEN-SIM-RECO/PRE_LS172_V11-v1/00000/7E674AE9-933F-E411-9C63-0026189438B1.root"
#  "file:/afs/cern.ch/user/y/yoshin/work/public/relval/7E674AE9-933F-E411-9C63-0026189438B1.root"
#  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre6/RelValZMM_13/GEN-SIM-RECO/PU50ns_PRE_LS172_V12-v1/00000/025E473F-6442-E411-BDFE-0025905A60BC.root"
 ),
    skipEvents = cms.untracked.uint32(0)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

##
## To remove the "begin job processing line " from printing
##
#process.MessageLogger = cms.Service("MessageLogger",
#   destinations = cms.untracked.vstring('cout',),
#   cout         = cms.untracked.PSet(threshold = cms.untracked.string('ERROR'))
#)
process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.MessageLogger.cerr.default.limit = 10
#process.options.wantSummary = False


#
# for debugging
# Needed by PAT which want an output module
process.dummy = cms.EDAnalyzer("Dummy")

#
# out module for tests
#
process.out = cms.OutputModule(
    "PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = cms.untracked.vstring('keep *_*_*_*',),
    fileName = cms.untracked.string('output/outStdMET_CHS.root')
)


process.load("JetMETCorrections.Type1MET.correctedMet_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")



process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")
process.ak4PFCHSL1Fastjet.algorithm = cms.string('AK4PFchs')
process.ak4PFCHSL2Relative.algorithm = cms.string('AK4PFchs')
process.ak4PFCHSL3Absolute.algorithm = cms.string('AK4PFchs')
process.corrPfMetType1.src = cms.InputTag('ak4PFJetsCHS')
process.corrPfMetType1.offsetCorrLabel = cms.string("ak4PFCHSL1Fastjet")
process.corrPfMetType1.jetCorrLabel = cms.string("ak4PFCHSL1FastL2L3")

#
# PATH definition , define which filter and sequence will be used before the NtupleMaker
#

process.p = cms.Path(
    process.correctionTermsPfMetType1Type2*
    process.pfMetT1
   #pat sequence
#   process.pat_sequence
)


# storage
process.outpath = cms.EndPath(process.out) #dummy

  
