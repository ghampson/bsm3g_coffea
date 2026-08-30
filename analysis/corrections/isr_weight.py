import copy
import correctionlib
import awkward as ak
from pathlib import Path


def add_isr_weight(events, weights, year, variation, dataset, workflow, fit, one_dim):
    if dataset.startswith("DYJetsToLL"):
        # get dilepton pt - branch on workflow since the field name differs
        if workflow == "ztomumu":
            dilepton_pt = ak.firsts(events.selected_dimuons.pt)
        elif workflow == "ztoee":
            dilepton_pt = ak.firsts(events.selected_dielectrons.pt)
        else:
            raise ValueError(f"add_isr_weight: unsupported workflow '{workflow}'")

        njet = ak.num(events.selected_jets)
        if one_dim:
            in_binning = (dilepton_pt > 0.0) & (dilepton_pt < 1000.0)
        else:
            in_binning = (dilepton_pt > 0.0) & (dilepton_pt < 1000.0) & (njet > 0) & (njet < 5)

        selected_dilepton_pt = dilepton_pt.mask[in_binning]
        selected_njet = njet.mask[in_binning]
        selected_dilepton_pt = ak.fill_none(selected_dilepton_pt, 500.0)
        selected_njet = ak.fill_none(selected_njet, 2.0)

        # load correction set
        if one_dim:
            fname = f"{Path.cwd()}/analysis/data/{year}_{workflow}_isr_weight_1d"
        else:
            fname = f"{Path.cwd()}/analysis/data/{year}_{workflow}_isr_weight"
            if fit:
                fname += "_fit"
        fname += ".json.gz"
        cset = correctionlib.CorrectionSet.from_file(fname)

        # compute weight
        if one_dim:
            sf = cset["isr_weight"].evaluate(selected_dilepton_pt)
        else:
            sf = cset["isr_weight"].evaluate(selected_dilepton_pt, selected_njet)
        weight = ak.where(in_binning, sf, ak.ones_like(sf))
        weights.add(
            name="isr_weight",
            weight=weight,
        )