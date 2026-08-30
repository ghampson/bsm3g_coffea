# From  2018_nanov9.yaml
sigma_inclusive_50 = 6025.6   

# Sum of all M-50 HT-binned sigmas
sigma_ht_bins = {
    "HT-70to100":    140.0,
    "HT-100to200":   160.7,
    "HT-200to400":    48.63,
    "HT-400to600":     6.993,
    "HT-600to800":     1.761,
    "HT-800to1200":    0.8021,
    "HT-1200to2500":   0.1937,
    "HT-2500toInf":    0.003514,
}
total_ht_binned = sum(sigma_ht_bins.values())
print(f"Sum of HT-binned sigmas: {total_ht_binned:.2f} pb")

# What fraction of the inclusive does this represent?
fraction_ht_above70 = total_ht_binned / sigma_inclusive_50
print(f"Fraction of inclusive above HT=70: {fraction_ht_above70*100:.1f}%")

