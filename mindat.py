import os
import json
import requests
import jinja2

DTYPES = [
    ["int", int, "xsd:integer"],
    ["float", float, "xsd:float"],
    ["bool", bool, "xsd:boolean"],
    ["str", str, "xsd:string"],
]

MINERAL_LIST = [
    "Aluminum",

]


def get_ima_minerals():
    """
    Retrieves a list of IMA approved minerals from the mindat.org API
    The list is saved in ima_minerals.json.
    """
    API_KEY = "e3cfd162955edf7815887621e7b318ca"
    # API_KEY = input('Enter your API key: ')
    MINDAT_API_URL = "https://api.mindat.org"
    headers = {"Authorization": "Token " + API_KEY}

    # read from cache if it exists
    if os.path.exists("ima_minerals.json"):
        with open("ima_minerals.json", "r") as f:
            return json.loads(f.read())['results']

    filter_dict = {
        "ima_status": [
            "APPROVED"
        ],
        "format": "json",
    }

    response = requests.get(
        MINDAT_API_URL + "/geomaterials/", params=filter_dict, headers=headers
    )

    result_data = response.json()["results"]
    json_data = {"results": result_data}

    while True:
        try:
            next_url = response.json()["next"]
            response = requests.get(next_url, headers=headers)
            json_data["results"] += response.json()["results"]

        except requests.exceptions.MissingSchema as e:
            # This error indicates the `next_url` is none
            break

    with open("ima_minerals.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))

    results = json_data["results"]
    print("Successfully retrieved " + str(len(results)) + " entries")

    return results


def infer_dtype_helper(values):
    """
    Given a list of values, infers the datatype of the values.
    Available datatypes are:
        str,
        int,
        float,
        bool,

    Note: for simplicity, list and dict will be treated as str
    """

    counts = {key: 0 for key, _, _ in DTYPES}

    for value in values:
        # if the type of value is found in DTYPES[:-1], add 1 to the count
        # else, add 1 to the count of str
        for dtype, type_, _ in DTYPES[:-1]:
            if isinstance(value, type_):
                counts[dtype] += 1
                break
        else:
            counts["str"] += 1

    dtype = max(counts, key=counts.get)
    confidence_rate = counts[dtype] / sum(counts.values())
    confidence_str = f'{counts[dtype]}/{sum(counts.values())}'

    matched = list(filter(lambda x: x[0] == dtype, DTYPES))[0] 
    return matched, confidence_rate, confidence_str


def infer_dtype(entries):
    """
    Given a list of dictionaries, infers the datatype of each key.
    Count the datatype of each key and return the most common one. 
    """
    dtypes = {}

    # collect all keys and their values
    for entry in entries:
        for key in entry.keys():
            if key not in dtypes:
                dtypes[key] = []
            dtypes[key].append(entry[key])

    # infer the datatype of each key
    for key in dtypes.keys():
        dtype, confidence_rate, confidence_str = infer_dtype_helper(dtypes[key])
        # print(f'{key}: {dtype[2]} ({confidence_rate:.2f}, {confidence_str})')
        dtypes[key] = dtype

    return dtypes


def convert_dtype(entries, dtypes):
    for entry in entries:
        for key in entry.keys():
            dtype = dtypes[key][1]
            try:
                entry[key] = dtype(entry[key])

            except ValueError:
                entry[key] = ""
            
            if dtypes[key][2] == 'xsd:string':
                entry[key] = entry[key].replace('\\', '\\\\')


def render_rdf(minerals, dtypes, output_file="mineral_rdf.ttl"):
    """
    Renders the RDF file using the Jinja2 template
    """
    template = """@prefix mindat: <http://www.mindat.org#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
# ontology design of mineral

<http://www.mindat.org> a owl:Ontology ;
    rdfs:label "Mindat" ;
    rdfs:comment "Programmatically generated ontology for minerals from mindat.org" . 

################################################################################
# data properties for minerals

{% for key, (_, _, xsd_type) in dtypes.items() %}
mindat:{{key}} rdf:type owl:DatatypeProperty ;
    rdfs:range {{xsd_type}} .
{% endfor %}

################################################################################
# Classes
mindat:mineral rdf:type owl:Class ;
    rdfs:label "Mineral" .

################################################################################
# Individuals
# Use Jinja2 to render individuals from dicts

# render minerals
{% for mineral in minerals %}
mindat:min{{mineral['id']}} rdf:type owl:NamedIndividual, mindat:mineral ;
    rdfs:label "{{mineral['name']}}" ;
{%- for key, value in mineral.items() -%}
{%- if key != 'name' and value != ''  -%}
{%- if dtypes[key][2] == 'xsd:string' %}
    mindat:{{key}} {% if '\n' in value or '"' in value %}\"\"\" {{value}} \"\"\"{% else %}"{{value}}"{% endif %} ;
{%- else %}
    mindat:{{key}} {{value}} ;
{%- endif %}
{%- endif -%}
{%- endfor -%}
    .
{% endfor %}

"""
    rdf = jinja2.Template(template).render(minerals=minerals, dtypes=dtypes)
    with open(output_file, "w", encoding='utf-8') as f:  # Specify the encoding here
        f.write(rdf)


if __name__ == "__main__":
    minerals = get_ima_minerals()
    dtypes = infer_dtype(minerals)
    convert_dtype(minerals, dtypes)
    render_rdf(minerals, dtypes)
