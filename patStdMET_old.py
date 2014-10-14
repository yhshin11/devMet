import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patTemplate_cfg import *

process.load("PhysicsTools.PatAlgos.patSequences_cff")

### =========== Global configuration ==========================

## MET flavor configuration -> may be time consuming
## NoPu and MVA met need to be generated with some refeernce objects (e;g. leptons)
## look for the corresponding area in the config file to set your own definition


### ===========================================================
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
# "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValProdTTbar/AODSIM/START72_V1-v1/00000/84686BF3-AC30-E411-B9A8-00261894391C.root"
#  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValZMM_13/GEN-SIM-RECO/PU50ns_POSTLS172_V4-v1/00000/1823742B-8730-E411-9EAB-0025905A60DA.root"
#  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre6/RelValZMM_13/GEN-SIM-RECO/PRE_LS172_V11-v1/00000/7E674AE9-933F-E411-9C63-0026189438B1.root"
 "file:/afs/cern.ch/user/y/yoshin/work/public/relval/7E674AE9-933F-E411-9C63-0026189438B1.root"
 ),
    skipEvents = cms.untracked.uint32(0)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
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
process.options.wantSummary = False

#
# Configure PAT : remove MC matching
#
#from PhysicsTools.PatAlgos.tools.coreTools import *
#removeMCMatching(process, ['All'])

###
### PAT Jet switch
###
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *

switchJetCollection(process, 
                    jetSource = cms.InputTag('ak4PFJets'),
                    # jetSource = cms.InputTag('ak4PFJets'),
                    jetCorrections = ('AK4PF',['L1FastJet','L2Relative', 'L3Absolute'] ,''), #,'Uncertainty'
                    )

##
## Tune for MET correction : data needs residual corrections
##
process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")   
process.patPFJetMETtype1p2Corr.jetCorrLabel = cms.string("L3Absolute")


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
    fileName = cms.untracked.string('outStd.root')
)

##-------------------- Turn-on the FastJet density calculation -----------------------
#from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#process.kt6PFJets = kt4PFJets.clone()
#process.kt6PFJets.rParam = cms.double(0.6)
#process.kt6PFJets.doRhoFastjet = True

process.patJetCorrFactors.useRho = cms.bool(True)
process.patJetCorrFactors.rho = cms.InputTag("fixedGridRhoFastjetAll") #PAT
process.patJetCorrFactors.useNPV = cms.bool(False)


process.load("JetMETCorrections.Type1MET.correctedMet_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")


# Add tracer
# process.Tracer = cms.Service("Tracer")

#
# PATH definition , define which filter and sequence will be used before the NtupleMaker
# not needed for now

process.pat_sequence =  cms.Sequence(
    # PAT
    process.patDefaultSequence
)
  
process.p = cms.Path(
	 # pat sequence
  # process.pat_sequence*
	 process.correctionTermsPfMetType1Type2*
	 process.pfMetT1
)


# storage
process.outpath = cms.EndPath(process.out) #dummy

  
