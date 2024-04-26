import xml.etree.ElementTree as ET
import requests

def clinvar_rcv_retriever(rcv):
    """
    Collection of variant information through ClinVar API
    :param rcv: Variant Disease Record id
    :return: XML root (element tree format)
    """

    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" \
                      "db=clinvar&rettype=clinvarset&id={rcv}"

    response = requests.get(url)

    if response.status_code != 200:
        print("No response from clinvar!")
        return 0
    else:
        root = ET.fromstring(response.content)
        return root


def clinvar_rcv_analyser(root):
    """
    Python style storing of variant information from ClinVar XML
    :param root: XML root (element tree format)
    :return: Python dictionary having variant information
    """
    clinvar_info = {}

    for child in root:

        # Latest update time
        clinvar_info["last_update"] = child.find("ReferenceClinVarAssertion").attrib["DateLastUpdated"]

        # RCV accession to check with our RCVs
        clinvar_info["accession"] = child.find("ReferenceClinVarAssertion/ClinVarAccession").attrib["Acc"]

        # Clinical significance of the variant
        
        if clinvar_sig := child.find("ReferenceClinVarAssertion/ClinicalSignificance/Description") is not None:
          clinvar_info["clinvar_sig"] = clinvar_sig.text

        # The source of the significance and any annotations
        clinvar_info["source_type"] = child.find("ReferenceClinVarAssertion/ObservedIn/Method/MethodType").text

        # Functional and molecular consequences of the variants if any
        cons_node = child.find("ReferenceClinVarAssertion/MeasureSet/Measure").findall("AttributeSet")
        fcons_list, mcons_list = [], []
        for node in cons_node:
            # Functional Consequences
            cons_node2 = node.find("Attribute[@Type='FunctionalConsequence']")
            if cons_node2 is not None:
                fcons_list.append(cons_node2.text)
            else:
                continue

            # Molecular Consequences
            cons_node3 = node.find("Attribute[@Type='MolecularConsequence']")
            if cons_node3 is not None:
                mcons_list.apend(cons_node3.text)
            else:
                continue

        if not fcons_list:
            clinvar_info["functional_consq"] = "None"
        else:
            t = ",".join(fcons_list)
            if t[-1] == ",": t = t[:-1]
            clinvar_info["functional_consq"] = t

        if not mcons_list:
            clinvar_info["molecular_consq"] = "None"
        else:
            t = ",".join(mcons_list)
            if t[-1] == ",": t = t[:-1]
            clinvar_info["molecular_consq"] = t

        # Disease mechanism of the variants
        trait_node = child.find("ReferenceClinVarAssertion/TraitSet/Trait").findall("AttributeSet")
        trait_list = []

        for node in trait_node:
            # Disease mechanism
            trait_node2 = node.find("Attribute[@Type='disease mechanism']")
            if trait_node2 is not None:
                trait_list.append(trait_node2.text)
            else:
                continue

        if not trait_list:
            clinvar_info["disease_mech"] = "None"
        else:
            t = ",".join(trait_list)
            if t[-1] == ",": t = t[:-1]
            clinvar_info["disease_mech"] = t

    return clinvar_info