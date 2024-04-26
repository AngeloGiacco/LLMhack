import requests

tools = [
    {
        "type": "function",
        "function": {
            "name": "tool_query_gnomad_by_rsid",
            "description": "Queries the gnomad API for detailed information about a variant based on its rsid.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rsid": {
                        "type": "string",
                        "description": "The rsid of the variant"
                    }
                },
                "required": ["rsid"]
            },
            "return": {
                "type": "object",
                "description": "Data dictionary from the API response, potentially containing a wide array of variant details."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_query_single_nucleotide_polymorphisms_db_by_rsid",
            "description": "Queries the Single Nucleotide Polymorphisms Database (dbSNP) using an rsid. (Note: The function is missing the URL of the API endpoint).",
            "parameters": {
                "type": "object",
                "properties": {
                    "rsid": {
                        "type": "string",
                        "description": "The rsid of the variant"
                    }
                },
                "required": ["rsid"]
            },
            "return": {
                "type": "object",
                "description": """The total number of results on the server, which can be more than the number of results returned. This reported total number of results may also be significantly less than the actual number of results and is limited to 10,000, which may significantly improve the service response time.
    An array of codes for the returned items. (This is the field specified with the cf query parameter above.)
    A hash of the "extra" data requested via the "ef" query parameter above. The keys on the hash are the fields (or their requested aliases) named in the "ef" parameter, and the value for a field is an array of that field's values in the same order as the returned codes.
    An array, with one element for each returned code, where each element is an array of the display strings specified with the "df" query parameter.
    An array, with one element for each returned code, where each element is the "code system" for the returned code. Note that only code-system aware APIs will return this array."""
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_variant_consequences_by_id",
            "description": "Fetches variant consequences from Ensembl VEP based on a dbSNP, COSMIC, or HGMD identifier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "dbSNP, COSMIC, or HGMD identifier"
                    }
                },
                "required": ["id"]
            },
            "return": {
                "type": "object",
                "description": "Data dictionary with variant consequences."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_variant_consequences_by_hgvs",
            "description": "Fetches variant consequences from Ensembl VEP based on an HGVS code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hgvs_code": {
                        "type": "string",
                        "description": "The HGVS code"
                    }
                },
                "required": ["hgvs_code"]
            },
            "return": {
                "type": "object",
                "description": "Data dictionary with variant consequences."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_variant_consequences_by_region_and_allele",
            "description": "Fetches variant consequences from Ensembl VEP based on a genomic region and allele.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "The genomic region"
                    },
                    "allele": {
                        "type": "string",
                        "description": "The allele"
                    }
                },
                "required": ["region", "allele"]
            },
            "return": {
                "type": "object",
                "description": "Data dictionary with variant consequences."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_mutation_tester_result",
            "description": "Fetches results from the MutationTaster API, providing predictions on a variant's potential impact.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chromosome_coordinate": {
                        "type": "string",
                        "description": "Likely a variant identifier"
                    },
                    "original_reference_allele": {
                        "type": "string",
                        "description": "original reference allele of the nucleotide substitution in capital, for example, C"
                    },
                    "new_allele": {
                        "type": "string",
                        "description": "new allele after the nucleotide substitution, for example C"
                    }
                },
                "required": ["chromosome_coordinate", "original_reference_allele", "new_allele"]
            },
            "return": {
                "type": "string",
                "description": "JSON data containing parsed results from MutationTaster, including prediction, model, potential disease links, etc."
            } 
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_clinvar_data_by_rcv_code",
            "description": "Uses the clinvar library to retrieve and analyze data from ClinVar based on an RCV accession code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rcv": {
                        "type": "string",
                        "description": "A ClinVar RCV accession code",
                        "example":"RCV000009910"
                    }
                },
                "required": ["rcv"]
            },
            "return": {
                "type": "object",
                "description": "Analyzed ClinVar data"
            }
        }
    }
]

def tool_query_gnomad_by_rsid(rsid):
    """calls the gnomad api and filters by rsid of the variant, returning all fields possible"""
    query_for_variants = """
        {
            variant(rsid: "%s", dataset: gnomad_r2_1) {
            variantId
            reference_genome
            chrom
            pos
            ref
            alt
            colocatedVariants
            multiNucleotideVariants {
            combined_variant_id
            changes_amino_acids
            n_individuals
            other_constituent_snvs
            }
            exome {
            ac
            an
            ac_hemi
            ac_hom
            faf95 {
                popmax
                popmax_population
            }
            filters
            populations {
                id
                ac
                an
                ac_hemi
                ac_hom
            }
            age_distribution {
                het {
                bin_edges
                bin_freq
                n_smaller
                n_larger
                }
                hom {
                bin_edges
                bin_freq
                n_smaller
                n_larger
                }
            }
            qualityMetrics {
                alleleBalance {
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
                genotypeDepth {
                all {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
                genotypeQuality {
                all {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
            }
            }
            genome {
            ac
            an
            ac_hemi
            ac_hom
            faf95 {
                popmax
                popmax_population
            }
            filters
            populations {
                id
                ac
                an
                ac_hemi
                ac_hom
            }
            age_distribution {
                het {
                bin_edges
                bin_freq
                n_smaller
                n_larger
                }
                hom {
                bin_edges
                bin_freq
                n_smaller
                n_larger
                }
            }
            qualityMetrics {
                alleleBalance {
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
                genotypeDepth {
                all {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
                genotypeQuality {
                all {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                alt {
                    bin_edges
                    bin_freq
                    n_smaller
                    n_larger
                }
                }
            }
            }
            flags
            rsid
            sortedTranscriptConsequences {
            canonical
            gene_id
            gene_version
            gene_symbol
            hgvs
            hgvsc
            hgvsp
            lof
            lof_flags
            lof_filter
            major_consequence
            polyphen_prediction
            sift_prediction
            transcript_id
            transcript_version
            }
        }
        
        }
    """
    query = query_for_variants % (rsid.lower())
    end_point = "https://gnomad.broadinstitute.org/api/"

    response = requests.post(end_point, data={'query': query}, timeout=1000)

    if response.status_code == 200:
        data_dict = response.json()
        return data_dict
    else:
        print("API request failed. Status code:", response.status_code)
        return None

def tool_query_single_nucleotide_polymorphisms_db_by_rsid(rsid):
    response = requests.get(end_point)
    if response.status_code == 200:
        data_dict = response.json()
        return data_dict #figure out how to use output explanation
    else:
        print("API request failed. Status code:", response.status_code)
        return None
    
    Query 

def tool_get_variant_consequences_by_id(id):
    """id supports dbSNP, COSMIC and HGMD identifiers"""
    server = "https://rest.ensembl.org"
    ext = f"/vep/human/id/{id}?Geno2MP=1"
    
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if response.status_code == 200:  # Check for successful response
        data_dict = response.json()
        return data_dict
    else:
        print("API request failed. Status code:", response.status_code)
        return None 
    
def tool_get_variant_consequences_by_hgvs(hgvs_code):
    #ensembl Fetch variant consequences based on a HGVS notation

    server = "https://rest.ensembl.org"
    ext = f"/vep/human/hgvs/{hgvs_code}?Geno2MP=1"
    
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if response.status_code == 200:  # Check for successful response
        data_dict = response.json()
        return data_dict
    else:
        print("API request failed. Status code:", response.status_code)
        return None
    
def tool_get_variant_consequences_by_region_and_allele(region,allele):
    #ensembl Fetch variant consequences based on a specific region and allele
    server = "https://rest.ensembl.org"
    ext = f"/vep/human/region/{region}/{allele}?Geno2MP=1"
    
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if response.status_code == 200:  # Check for successful response
        data_dict = response.json()
        return data_dict
    else:
        print("API request failed. Status code:", response.status_code)
        return None
    
def tool_get_mutation_tester_result(chromosome_coordinate, original_reference_allele, new_allele):
    def parse_line(line):
        fields = line.decode('utf-8').strip().split('\t')
        while len(fields) < 15:
            fields.append('')
        return {
            'id': fields[0],
            'chr': fields[1],
            'pos': fields[2],
            'ref': fields[3],
            'alt': fields[4],
            'transcript_stable': fields[5],
            'NCBI_geneid': fields[6],
            'prediction': fields[7],
            'model': fields[8],
            'tree_vote': fields[9].split('|'),  # Handle multiple values
            'note': fields[10],
            'splicesite': fields[11],
            'distance_from_splicesite': fields[12],
            'disease_mutation': fields[13],
            'polymorphism': fields[14]
        }
    #exapmle target url with two variants 
    #target_url = "https://www.genecascade.org/MT2021/MT_API102.cgi?variants=21:33039603A>C,2:233391374T>C"
    #example with one variant
    target_url = f"https://www.genecascade.org/MT2021/MT_API102.cgi?variants={chromosome_coordinate}{original_reference_allele}>{new_allele}"

    response = requests.get(target_url)
    if response.status_code == 200:  # Check for successful response
        lines = response.content.splitlines()[1:] 
        data = [parse_line(line) for line in lines]
        json_data = json.dumps(data, indent=2)
        return json_data
    else:
        print("API request failed. Status code:", response.status_code)
        return None
    
from clinvar import clinvar_rcv_analyser
from clinvar import clinvar_rcv_retriever

def tool_get_clinvar_data_by_rcv_code(rcv):
    response = clinvar_rcv_retriever(rcv)
    if response:
        return clinvar_rcv_analyser(response)