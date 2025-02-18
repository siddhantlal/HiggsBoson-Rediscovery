import ROOT
import glob
import itertools

# File pattern and TChain setup
file_pattern = "/home/siddhant/ATLAS_HIGGS_DATA/15005/4lep/*.root"
file_list = glob.glob(file_pattern)
chain = ROOT.TChain("mini")  # Ensure this is the correct tree name
for f in file_list:
    chain.Add(f)

scale = 0.001  # Conversion factor from MeV to GeV
lep_mass_assumption = 0.105  # Assume muon mass (you may treat electrons similarly if needed)

# Z mass window settings
mZ = 91.1876
Z_window_low = 66
Z_window_high = 116

# Histogram for the refined Higgs candidate invariant mass
h_mass = ROOT.TH1F("h_mass", "Invariant Mass of Higgs Candidates;Mass [GeV];Events", 100, 0, 1000)
higgs_candidates = []

for event in chain:
    # Get lepton arrays
    pts   = event.lep_pt
    etas  = event.lep_eta
    phis  = event.lep_phi
    charges = event.lep_charge  # Verify that this branch exists
    nlep = len(pts)
    
    if nlep < 4:
        continue

    # Build TLorentzVectors for leptons (with conversion)
    leptons = []
    for i in range(nlep):
        if abs(etas[i]) < 2.5:  # Basic acceptance
            vec = ROOT.TLorentzVector()
            vec.SetPtEtaPhiM(pts[i] * scale, etas[i], phis[i], lep_mass_assumption)
            leptons.append((vec, charges[i]))
    
    if len(leptons) < 4:
        continue

    # Try all combinations of 4 leptons
    best_pairing = None
    best_diff = 1e9  # To choose the pairing with the first Z candidate closest to mZ
    for combo in itertools.combinations(range(len(leptons)), 4):
        indices = list(combo)
        # Try all possible ways to partition these 4 leptons into two pairs
        for pair1 in itertools.combinations(indices, 2):
            pair2 = [idx for idx in indices if idx not in pair1]
            # Retrieve vectors and charges for both pairs
            vec1, q1 = leptons[pair1[0]]
            vec2, q2 = leptons[pair1[1]]
            vec3, q3 = leptons[pair2[0]]
            vec4, q4 = leptons[pair2[1]]
            
            # Require opposite-sign for both pairs
            if q1 * q2 >= 0 or q3 * q4 >= 0:
                continue

            Z1 = vec1 + vec2
            Z2 = vec3 + vec4

            # Check if both Z candidates are within the Z mass window
            if (Z_window_low < Z1.M() < Z_window_high) and (Z_window_low < Z2.M() < Z_window_high):
                diff = abs(Z1.M() - mZ)
                if diff < best_diff:
                    best_diff = diff
                    best_pairing = (Z1, Z2)
    
    if best_pairing is not None:
        Z1, Z2 = best_pairing
        higgs_candidate = Z1 + Z2
        candidate_mass = higgs_candidate.M()
        h_mass.Fill(candidate_mass)
        # Optionally, select candidate if within a Higgs window (e.g., 115-135 GeV)
        if 115 < candidate_mass < 135:
            higgs_candidates.append(candidate_mass)

# Output results
print("Number of refined Higgs candidates (115-135 GeV):", len(higgs_candidates))
c1 = ROOT.TCanvas()
h_mass.Draw()
c1.SaveAs("refined_mass_distribution.png")
