================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Ashley Louis David Hicks (born 18 July 1963) is a British interior designer, author, photographer and artist.
He is the only son of Lady Pamela Hicks (née Mountbatten) and David Nightingale Hicks.
Hicks has designed interiors in Europe, the United States, and the United Kingdom.
Hicks is the grandson of Louis Mountbatten, 1st
Earl Mountbatten of Burma.
Early life and family

Ashley Louis David Hicks was born on 18 July 1963, at King's College Hospital in Denmark Hill, London.
He is the son and second child of David and Lady Pamela Hicks.
He is the younger brother of Edwina Brudenell and the older brother of India Hicks, author, television host, fashion model, and founder of her eponymous lifestyle brand.
Hicks was raised at Britwell House, an 18th-century house in Britwell Salome in Oxfordshire, that served as the family's home, as well as his father's showplace.
Hicks was a boarding student at Stowe School.
In 1978, the family decided to sell the house, and Hicks attended the three-day Sotheby's sale, 20–22 March 1979.
After the auction, the Hicks family moved to The Grove, a nearby estate, and also resided at Albany, an historic and exclusive apartment house in Piccadilly.
Through his mother, Hicks is a grandson of the first Earl and Countess Mountbatten of Burma.
Through his maternal grandfather, Lord Louis Mountbatten, Hicks is a second cousin of King Charles III.
Lady Edwina Mountbatten was one of Britain's richest women, having inherited most of the £7.5 million fortune of her grandfather, Sir Ernest Cassel.
Family tragedy

As a child, Hicks spent family holidays at Sligo Castle in Ireland and the Mountbatten family ancestral home at Broadlands in Hampshire, where the royal family were frequent guests.
In August 1979, when Hicks was 16 years old, his grandfather and his cousin Nicholas Knatchbull were assassinated by the Provisional Irish Republican Army when his grandfather's wooden boat, the Shadow V, was blown up by a remote-controlled bomb on Donegal Bay.
and I was with India, watching television.
"


Career

Hicks says his first decorating experience took place when he was 15 or 16 years old, when he decorated his room in a checkered black-and-white motif.
Influenced by his father, Hicks studied painting and fine art, graduating from the Bath School of Art and Design and trained with the Architectural Association School of Architecture, in London.
In 1997, Hicks began designing furniture at the Gem Palace in Jaipur, India.
When Hicks initially designed in India, he designed under the moniker of "Jantar Mantar".
Hicks explains, "It means abracadabra, also hocus pocus, and is local slang for the Jaipur Observatory.
"


In addition to interior and furniture design, Hicks produces various lines of fabric, wallpaper, and carpeting—some under the "David Hicks by Ashley Hicks" brand and others under his own name.
Hicks also produced a series of Allegra Hicks shops as well as a collection of home accessories that were sold in these shops.
In 2017, Hicks published his first book on his own work, Details, which also serves as a source book for his inspiration; published by IDEA Publishing, it sold out within a month.
Hicks began photographing historic interiors for Cabana Magazine in 2016, ranging from a derelict glass factory in Murano, Venice, to grand English country houses like Houghton and Althorp.
Hicks is currently a contributing editor for Cabana Magazine.
Hicks exhibited furniture and sculptural objects made by his own hands at New York's R and Company gallery in 2019,


Hicks has also regularly worked with various brands on product collaborations, including a bed linen collection with Frette, a candle range collaboration with Jo Malone and swimsuit collaborations with Orlebar Brown and Coverswim, as well as furniture projects with Kartell and Promemoria.
Personal life

On 18 October 1990, Hicks married Italian designer, Marina Allegra Federica Silvia Tondato (born Turin, Italy, 20 May 1960), a daughter of physicist and musician Dr. Carlo Tondato and his wife, the former Rosy Maza, in Wheatley, Oxfordshire.
From his first marriage, Hicks has two daughters:


After their wedding, Hicks and his wife lived in a renovated building in New York City that belonged to Marc Chagall's grandson.
Allegra said of their home, "Although it was a glamorous address it was, for us, more about the people who lived there."
Allegra remarried in June 2014 Marchese Roberto Mottola di Amato, a Neapolitan landowner and entrepreneur.
On 5 September 2015, Hicks married Kathryn 'Katalina' Sharkey also known as Kata Sharkey de Solis (born Houston, Texas, U.S., 31 December 1981, daughter of William T. Sharkey, CPA, and Rosalie Solis).
Hicks and Sharkey separated in August 2018 and then divorced.
From his second marriage, Hicks has two sons:


Hicks decorated his partner Martina Mondadori's home in Milan, Italy, in 2020.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b437359b-f16c-4739-a02b-c9d7b35d62bf)
 Call ID: b437359b-f16c-4739-a02b-c9d7b35d62bf
  Args:
    source: Ashley_Hicks
    type: :Man
  AssignClass (e70af653-c411-4cdb-9234-2d72409b379d)
 Call ID: e70af653-c411-4cdb-9234-2d72409b379d
  Args:
    type: :Person
    source: Ashley_Hicks
  AddLiteral (3ec1a9b0-1ca6-4299-b566-5f98a1470d96)
 Call ID: 3ec1a9b0-1ca6-4299-b566-5f98a1470d96
  Args:
    literal_type: xsd:integer
    source: Ashley_Hicks
    relation: :hasBirthYear
    literal_value: 1963
  AssignClass (368e4554-d139-48fb-894e-1eb829fa27b6)
 Call ID: 368e4554-d139-48fb-894e-1eb829fa27b6
  Args:
    source: Lady_Pamela_Hicks
    type: :Woman
  AssignClass (af4d336d-8e91-48bd-8968-d8234f7bba31)
 Call ID: af4d336d-8e91-48bd-8968-d8234f7bba31
  Args:
    type: :Person
    source: Lady_Pamela_Hicks
  AssignClass (346d471e-5d16-4a7d-80ee-adf5822a5bf8)
 Call ID: 346d471e-5d16-4a7d-80ee-adf5822a5bf8
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (5c82307d-3a98-4757-b96b-e8dbb9035129)
 Call ID: 5c82307d-3a98-4757-b96b-e8dbb9035129
  Args:
    source: David_Nightingale_Hicks
    type: :Person
  AddTriple (25cc323f-d6a3-4bde-a5c7-e408cfdceb45)
 Call ID: 25cc323f-d6a3-4bde-a5c7-e408cfdceb45
  Args:
    target: Lady_Pamela_Hicks
    source: Ashley_Hicks
    relation: :hasMother
  AddTriple (4fb570d9-84c9-4c4e-86ca-3db10e0a23d4)
 Call ID: 4fb570d9-84c9-4c4e-86ca-3db10e0a23d4
  Args:
    target: David_Nightingale_Hicks
    source: Ashley_Hicks
    relation: :hasFather
  AssignClass (5c652a91-1b9f-43d8-8d17-88b44ae60f76)
 Call ID: 5c652a91-1b9f-43d8-8d17-88b44ae60f76
  Args:
    type: :Woman
    source: Edwina_Brudenell
  AssignClass (8d64e0c6-c579-44b0-b4e6-54e1afee6993)
 Call ID: 8d64e0c6-c579-44b0-b4e6-54e1afee6993
  Args:
    source: Edwina_Brudenell
    type: :Person
  AssignClass (be16bfcd-4716-4b7f-a084-9c0240a038df)
 Call ID: be16bfcd-4716-4b7f-a084-9c0240a038df
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (59e7abfe-ec53-4ba4-a26b-3b9016e56dba)
 Call ID: 59e7abfe-ec53-4ba4-a26b-3b9016e56dba
  Args:
    source: India_Hicks
    type: :Person
  AddTriple (9a9cd3ba-c966-4a52-a11a-20fe6fd9a2c7)
 Call ID: 9a9cd3ba-c966-4a52-a11a-20fe6fd9a2c7
  Args:
    relation: :isSiblingOf
    source: Ashley_Hicks
    target: Edwina_Brudenell
  AddTriple (79442fce-6345-4501-981c-22302bd304c4)
 Call ID: 79442fce-6345-4501-981c-22302bd304c4
  Args:
    relation: :isSiblingOf
    source: Ashley_Hicks
    target: India_Hicks
  AssignClass (f2e9785f-452a-4835-bd21-715eea7978af)
 Call ID: f2e9785f-452a-4835-bd21-715eea7978af
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (eaac828a-f6b0-439a-87e5-185e120ae4f7)
 Call ID: eaac828a-f6b0-439a-87e5-185e120ae4f7
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (91bfd23a-eea3-4715-ae81-f69a09b3b041)
 Call ID: 91bfd23a-eea3-4715-ae81-f69a09b3b041
  Args:
    relation: :hasAncestor
    target: Louis_Mountbatten
    source: Ashley_Hicks
  AssignClass (3ffb332c-f264-4b9f-a39b-7c6e0bad0af5)
 Call ID: 3ffb332c-f264-4b9f-a39b-7c6e0bad0af5
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    type: :Woman
  AssignClass (2b377369-6d43-466f-babd-023e3ca8b9be)
 Call ID: 2b377369-6d43-466f-babd-023e3ca8b9be
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    type: :Person
  AddLiteral (2b6a5c0b-7de2-4df9-a3b1-d52fc0cad3c2)
 Call ID: 2b6a5c0b-7de2-4df9-a3b1-d52fc0cad3c2
  Args:
    literal_type: xsd:integer
    source: Ashley_Hicks
    literal_value: 1990
    relation: :hasMarriageYear
  AddTriple (f24a74a3-6889-45ee-b9c9-94d4bf7ef6fd)
 Call ID: f24a74a3-6889-45ee-b9c9-94d4bf7ef6fd
  Args:
    target: Marina_Allegra_Federica_Silvia_Tondato
    source: Ashley_Hicks
    relation: :hasRelation
  AssignClass (ea897301-a7bb-49e2-afda-2e982d3ea46d)
 Call ID: ea897301-a7bb-49e2-afda-2e982d3ea46d
  Args:
    type: :Man
    source: Carlo_Tondato
  AssignClass (6a03256d-4710-4ecf-ad2c-c8f9fa5796bf)
 Call ID: 6a03256d-4710-4ecf-ad2c-c8f9fa5796bf
  Args:
    type: :Person
    source: Carlo_Tondato
  AssignClass (aa34964c-4b9d-4faa-af7c-d465ae85aa61)
 Call ID: aa34964c-4b9d-4faa-af7c-d465ae85aa61
  Args:
    source: Rosy_Maza
    type: :Woman
  AssignClass (6f28cb8e-bc45-4dc1-abbd-a3187816c89a)
 Call ID: 6f28cb8e-bc45-4dc1-abbd-a3187816c89a
  Args:
    source: Rosy_Maza
    type: :Person
  AddTriple (f85b4eff-3400-43a4-8082-5644f7419555)
 Call ID: f85b4eff-3400-43a4-8082-5644f7419555
  Args:
    relation: :hasFather
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Carlo_Tondato
  AddTriple (dc0f3e56-8583-4338-a481-8c6359164f0a)
 Call ID: dc0f3e56-8583-4338-a481-8c6359164f0a
  Args:
    relation: :hasMother
    target: Rosy_Maza
    source: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (05cc7a05-46e6-4119-856e-2a37a9bda50c)
 Call ID: 05cc7a05-46e6-4119-856e-2a37a9bda50c
  Args:
    type: :Woman
    source: Kathryn_Sharkey
  AssignClass (5d3e9187-4771-4586-9039-31cb97b50cb9)
 Call ID: 5d3e9187-4771-4586-9039-31cb97b50cb9
  Args:
    type: :Person
    source: Kathryn_Sharkey
  AddLiteral (2698104c-6a04-4440-876f-f100c697e2fd)
 Call ID: 2698104c-6a04-4440-876f-f100c697e2fd
  Args:
    literal_type: xsd:integer
    source: Ashley_Hicks
    literal_value: 2015
    relation: :hasMarriageYear
  AddTriple (2e59cb01-ca64-41f4-96d4-acaa7254cc89)
 Call ID: 2e59cb01-ca64-41f4-96d4-acaa7254cc89
  Args:
    relation: :hasRelation
    target: Kathryn_Sharkey
    source: Ashley_Hicks
  AssignClass (4f1af88d-1071-4764-9310-1e6d5438b01a)
 Call ID: 4f1af88d-1071-4764-9310-1e6d5438b01a
  Args:
    source: William_T_Sharkey
    type: :Man
  AssignClass (992f8143-fb66-40ae-8580-e660c1d3bb50)
 Call ID: 992f8143-fb66-40ae-8580-e660c1d3bb50
  Args:
    source: William_T_Sharkey
    type: :Person
  AssignClass (dafca0bb-1a70-414e-9e51-abda3cfa1041)
 Call ID: dafca0bb-1a70-414e-9e51-abda3cfa1041
  Args:
    type: :Woman
    source: Rosalie_Solis
  AssignClass (1b61f534-1725-4233-b312-2f3787dda973)
 Call ID: 1b61f534-1725-4233-b312-2f3787dda973
  Args:
    type: :Person
    source: Rosalie_Solis
  AddTriple (f78d1486-16d1-4350-99b0-c03456d757b9)
 Call ID: f78d1486-16d1-4350-99b0-c03456d757b9
  Args:
    relation: :hasFather
    target: William_T_Sharkey
    source: Kathryn_Sharkey
  AddTriple (340f4d01-a5b2-45b3-bc8e-2af348458548)
 Call ID: 340f4d01-a5b2-45b3-bc8e-2af348458548
  Args:
    target: Rosalie_Solis
    source: Kathryn_Sharkey
    relation: :hasMother
  Finish (319dccdf-bcb5-41f6-8e59-ed269915b859)
 Call ID: 319dccdf-bcb5-41f6-8e59-ed269915b859
  Args: