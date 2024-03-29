import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patTemplate_cfg import *

process.load("PhysicsTools.PatAlgos.patSequences_cff")


### =========== Global configuration ==========================

## MET flavor configuration -> may be time consuming
## NoPu and MVA met need to be generated with some refeernce objects (e;g. leptons)
## look for the corresponding area in the config file to set your own definition
produceStdPFMET=False
produceMVAPFMET=True
produceNoPUPFMET=True
produceCaloMET=False
#with jet smearing ?
smearing=['NoSmear']#,'Smeared']

### ===========================================================
process.GlobalTag.globaltag ="POSTLS171_V2::All"

from CondCore.DBCommon.CondDBSetup_cfi import *
process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                           connect = cms.string('sqlite_file:CSA14_V2_MC.db'),
                           toGet =  cms.VPSet(
        #	cms.PSet(record = cms.string("JetCorrectionsRecord"),
        #                 tag = cms.string("JetCorrectorParametersCollection_CSA14_AK4Calo"),
        #                 label= cms.untracked.string("AK4Calo")),
	cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_CSA14_V1_MC_AK4PF"),
                 label= cms.untracked.string("AK4PF"))
        )
                           )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
     #  "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValProdTTbar/GEN-SIM-RECO/START72_V1-v1/00000/D0A3C700-AD30-E411-BE6C-003048FFCBFC.root"
"root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValProdTTbar/AODSIM/START72_V1-v1/00000/94E91206-AD30-E411-BAAE-0025905A6126.root"
       # "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre5/RelValProdTTbar/AODSIM/START72_V1-v1/00000/84686BF3-AC30-E411-B9A8-00261894391C.root"
  #      "root://eoscms//eos/cms/store/relval/CMSSW_7_2_0_pre4/RelValZMM_13/GEN-SIM-RECO/PU25ns_POSTLS172_V3-v3/00000/221E98F3-C627-E411-B9FD-0025905B8572.root"
        ),
                            skipEvents = cms.untracked.uint32(0)
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
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
                    jetCorrections     =  ('AK4PF',['L1FastJet','L2Relative', 'L3Absolute'] ,''), #,'Uncertainty'
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
    outputCommands = cms.untracked.vstring('keep *_*_*_*'),
    fileName = cms.untracked.string('out3.root')
)


### ==================   NoPU and MVA MET ==================##
## standard lepton configuration for mva/noPU MET

#electron
Ele_ACCEPTANCE = '(pt >= 19 && abs(eta)<2.5)'
Ele_Id = 'abs(deltaPhiSuperClusterTrackAtVtx)<0.06 && abs(deltaEtaSuperClusterTrackAtVtx)<0.007 && scSigmaIEtaIEta<0.03 && hadronicOverEm<0.12' 
Ele_Iso = '(chargedHadronIso + max(neutralHadronIso + photonIso - 0.5*puChargedHadronIso, 0.))/pt < 0.2'
process.selectedPatElectrons.cut = Ele_ACCEPTANCE+"&&"+Ele_Id+"&&"+Ele_Iso

process.selectedPatMuons.cut = cms.string("(abs(eta)<2.4 && pt>=15)&&isGlobalMuon && isTrackerMuon && globalTrack.normalizedChi2 < 10 && muonID(\'TrackerMuonArbitrated\') && globalTrack.hitPattern.numberOfValidMuonHits > 0 && trackIso/pt < 0.3")

    

if produceNoPUPFMET :
### No Pu MET
    process.load('RecoMET.METPUSubtraction.pfNoPUMET_cff')
    process.calibratedAK4PFJetsForPFNoPUMEt.correctors = cms.vstring('ak4PFL1FastL2L3')
    process.pfNoPUMEt.srcLeptons = cms.VInputTag(["selectedPatMuons","selectedPatElectrons"])

if produceMVAPFMET :
### MVA MET
    process.load('RecoMET.METPUSubtraction.mvaPFMET_cff')
    process.calibratedAK4PFJetsForPFMVAMEt.correctors = cms.vstring('ak4PFL1FastL2L3')
    process.pfMVAMEt.srcLeptons = cms.VInputTag( ["selectedPatMuons","selectedPatElectrons"])

### ==================   NoPU and MVA MET ==================##


##
## PAT processes 
##

# apply type I/type I + II PFMEt corrections to pat::MET object
# and estimate systematic uncertainties on MET
from PhysicsTools.PatUtils.tools.runType1PFMEtUncertainties import runType1PFMEtUncertainties
from PhysicsTools.PatUtils.tools.runType1CaloMEtUncertainties import runType1CaloMEtUncertainties
from PhysicsTools.PatUtils.tools.runMVAMEtUncertainties import runMVAMEtUncertainties
from PhysicsTools.PatUtils.tools.runNoPileUpMEtUncertainties import runNoPileUpMEtUncertainties

sfNoPUjetOffsetEnCorr = 0.2
doApplyUnclEnergyResidualCorr=False

if produceStdPFMET:
    for i in smearing:
        isSmear=False
        if i == "Smeared":
            isSmear=True
        runType1PFMEtUncertainties(
        process,
        electronCollection = cms.InputTag('selectedPatElectrons'),
        photonCollection = '',
        muonCollection = cms.InputTag('selectedPatMuons'),
        tauCollection = '',
        jetCollection = cms.InputTag('patJets'),        
        makeType1corrPFMEt = True,
        makeType1p2corrPFMEt = True,
        doApplyType0corr = True,
        doSmearJets =isSmear,
        postfix = i
        )

if produceMVAPFMET:
     for i in smearing:
        isSmear=False
        if i == "Smeared":
            isSmear=True
        runMVAMEtUncertainties(
            process,
            electronCollection = cms.InputTag('selectedPatElectrons'),
            photonCollection = '',
            muonCollection = '',#cms.InputTag('selectedPatMuons'),
            tauCollection = '',
            jetCollection = cms.InputTag('patJets'),    
            doSmearJets =isSmear,
            addToPatDefaultSequence = False,
            postfix = i
            )

if produceNoPUPFMET:
     for i in smearing:
        isSmear=False
        if i == "Smeared":
            isSmear=True
        runNoPileUpMEtUncertainties(
            process,
            electronCollection = cms.InputTag('selectedPatElectrons'),
            photonCollection = '',
            muonCollection = cms.InputTag('selectedPatMuons'),
            tauCollection = '',
            jetCollection = cms.InputTag('patJets'),    
            doSmearJets = isSmear,
            addToPatDefaultSequence = False,
            doApplyChargedHadronSubtraction = False,
            doApplyUnclEnergyCalibration = (doApplyUnclEnergyResidualCorr and not isData),
            sfNoPUjetOffsetEnCorr = sfNoPUjetOffsetEnCorr,
            postfix = i
            )

if produceCaloMET:
    runType1CaloMEtUncertainties(
        process,
        caloTowerCollection = cms.InputTag(''),
        addToPatDefaultSequence = False,
        postfix = ""
        )


##-------------------- Turn-on the FastJet density calculation -----------------------
#from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#process.kt6PFJets = kt4PFJets.clone()
#process.kt6PFJets.rParam = cms.double(0.6)
#process.kt6PFJets.doRhoFastjet = True

process.patJetCorrFactors.useRho = cms.bool(True)
process.patJetCorrFactors.rho = cms.InputTag("kt6PFJets:rho") #PAT
process.patJetCorrFactors.useNPV = cms.bool(False)


#
# PATH definition , define which filter and sequence will be used before the NtupleMaker
#

process.prepat_sequence = cms.Sequence(
    process.kt6PFJets
    )
 
process.pat_sequence =  cms.Sequence(
    # PAT
    process.patDefaultSequence
    )
    
if produceMVAPFMET :
    for i in smearing:
        process.pat_sequence += getattr(process, "pfMVAMEtUncertaintySequence" + i)

if produceNoPUPFMET :
    for i in smearing:
        process.pat_sequence +=  getattr(process, "pfNoPUMEtUncertaintySequence" + i)
        
if produceCaloMET :
    process.pat_sequence += process.caloType1MEtUncertaintySequence


#process.load("RecoMET.METPUSubtraction.pfNoPUMET_cff")
process.p = cms.Path(
    #prepat sequence
    process.prepat_sequence*
    #pat sequence
    process.pat_sequence
#    process.pfNoPUMEtSequence
)




# dummy solution for dummy developers, make nothing but needed 
process.outpath = cms.EndPath(process.out) #dummy
