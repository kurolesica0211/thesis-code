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
  AssignClass (66284aa6-99d2-4e4f-b98e-845de6cce7c4)
 Call ID: 66284aa6-99d2-4e4f-b98e-845de6cce7c4
  Args:
    type: :Man
    source: Ashley_Hicks
  AssignClass (17bcddb0-975e-4a1f-b8df-575914765672)
 Call ID: 17bcddb0-975e-4a1f-b8df-575914765672
  Args:
    source: Ashley_Hicks
    type: :Person
  AddLiteral (bf6152f3-2380-43fd-b960-ce58e8fb0ee5)
 Call ID: bf6152f3-2380-43fd-b960-ce58e8fb0ee5
  Args:
    source: Ashley_Hicks
    literal_value: 1963
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (71f10e3b-aba1-436e-a549-a98f52c9092c)
 Call ID: 71f10e3b-aba1-436e-a549-a98f52c9092c
  Args:
    source: Lady_Pamela_Hicks
    type: :Woman
  AssignClass (072d6e09-2657-40d6-afd0-a70b51600787)
 Call ID: 072d6e09-2657-40d6-afd0-a70b51600787
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AssignClass (3fb6ff7f-f990-4e5e-b2e7-0fe2410f50cd)
 Call ID: 3fb6ff7f-f990-4e5e-b2e7-0fe2410f50cd
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (f05b120f-67cc-406e-b5be-009ff1e8f7cf)
 Call ID: f05b120f-67cc-406e-b5be-009ff1e8f7cf
  Args:
    source: David_Nightingale_Hicks
    type: :Person
  AddTriple (2a1b95a0-7ac9-4b97-ab84-22c9c2a931ec)
 Call ID: 2a1b95a0-7ac9-4b97-ab84-22c9c2a931ec
  Args:
    relation: :hasFather
    target: David_Nightingale_Hicks
    source: Ashley_Hicks
  AddTriple (0ec8428b-50be-48c7-ac8e-326f49a02d1d)
 Call ID: 0ec8428b-50be-48c7-ac8e-326f49a02d1d
  Args:
    relation: :hasMother
    target: Lady_Pamela_Hicks
    source: Ashley_Hicks
  AssignClass (a2943df0-c6b8-4f6e-a585-2a2c2c1eff93)
 Call ID: a2943df0-c6b8-4f6e-a585-2a2c2c1eff93
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (68124b2c-49a5-499e-8c79-c91e5cb2b4fd)
 Call ID: 68124b2c-49a5-499e-8c79-c91e5cb2b4fd
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (918bfcbc-575f-4880-8d69-c8db0b283b1d)
 Call ID: 918bfcbc-575f-4880-8d69-c8db0b283b1d
  Args:
    relation: :hasAncestor
    source: Ashley_Hicks
    target: Louis_Mountbatten
  AssignClass (e8ec7e28-169a-4248-ab41-528eff0ac4da)
 Call ID: e8ec7e28-169a-4248-ab41-528eff0ac4da
  Args:
    source: Edwina_Brudenell
    type: :Woman
  AssignClass (a05a149a-9702-4d63-afe0-640a19c5e1cc)
 Call ID: a05a149a-9702-4d63-afe0-640a19c5e1cc
  Args:
    source: Edwina_Brudenell
    type: :Person
  AddTriple (d662288e-1a2f-4e4e-b87d-043e2a402b39)
 Call ID: d662288e-1a2f-4e4e-b87d-043e2a402b39
  Args:
    relation: :isSiblingOf
    target: Edwina_Brudenell
    source: Ashley_Hicks
  AssignClass (3fed8ee4-37aa-43dd-add2-059e0b503b93)
 Call ID: 3fed8ee4-37aa-43dd-add2-059e0b503b93
  Args:
    source: India_Hicks
    type: :Woman
  AssignClass (3c0b3ce7-2875-4346-8fd5-88328bb1f283)
 Call ID: 3c0b3ce7-2875-4346-8fd5-88328bb1f283
  Args:
    source: India_Hicks
    type: :Person
  AddTriple (be0fdb8e-d79c-4280-8bd4-0d56d0eaf7e1)
 Call ID: be0fdb8e-d79c-4280-8bd4-0d56d0eaf7e1
  Args:
    target: India_Hicks
    source: Ashley_Hicks
    relation: :isSiblingOf
  AssignClass (5e8d2dcc-a0a1-4abe-8905-2532b2b4ec2c)
 Call ID: 5e8d2dcc-a0a1-4abe-8905-2532b2b4ec2c
  Args:
    type: :Woman
    source: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (59b21642-0537-43f8-a4ae-282952d8dbb7)
 Call ID: 59b21642-0537-43f8-a4ae-282952d8dbb7
  Args:
    type: :Person
    source: Marina_Allegra_Federica_Silvia_Tondato
  AddLiteral (1335686a-e89b-4575-a634-97775c86a257)
 Call ID: 1335686a-e89b-4575-a634-97775c86a257
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Ashley_Hicks
    literal_value: 1990
  AddTriple (2a05a271-27da-4693-9221-903dfbb18b34)
 Call ID: 2a05a271-27da-4693-9221-903dfbb18b34
  Args:
    relation: :hasRelation
    source: Ashley_Hicks
    target: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (03407b0d-1d68-4e35-8e25-0c4a0f414735)
 Call ID: 03407b0d-1d68-4e35-8e25-0c4a0f414735
  Args:
    source: Carlo_Tondato
    type: :Man
  AssignClass (e5f1673e-9028-4040-8be1-dde0b91de0ae)
 Call ID: e5f1673e-9028-4040-8be1-dde0b91de0ae
  Args:
    type: :Person
    source: Carlo_Tondato
  AssignClass (d0a9da87-9105-44f7-808e-c7bc7e8520a3)
 Call ID: d0a9da87-9105-44f7-808e-c7bc7e8520a3
  Args:
    type: :Woman
    source: Rosy_Maza
  AssignClass (81710b4e-f7cf-4e12-8cea-b1e7c74acd4a)
 Call ID: 81710b4e-f7cf-4e12-8cea-b1e7c74acd4a
  Args:
    type: :Person
    source: Rosy_Maza
  AddTriple (8c281548-8166-4e0f-a8bb-f43c9e5322cf)
 Call ID: 8c281548-8166-4e0f-a8bb-f43c9e5322cf
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Carlo_Tondato
    relation: :hasFather
  AddTriple (5c024088-9f14-4293-8775-caa9c1ff7b42)
 Call ID: 5c024088-9f14-4293-8775-caa9c1ff7b42
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Rosy_Maza
    relation: :hasMother
  AssignClass (017e5211-c383-4019-8cd5-5aa48fb5047c)
 Call ID: 017e5211-c383-4019-8cd5-5aa48fb5047c
  Args:
    source: Kathryn_Sharkey
    type: :Woman
  AssignClass (8c00fd2b-ca28-412f-8ea4-d8e037e2b82a)
 Call ID: 8c00fd2b-ca28-412f-8ea4-d8e037e2b82a
  Args:
    source: Kathryn_Sharkey
    type: :Person
  AddLiteral (22e4b25d-f143-4ceb-8276-a1ed1f95e1cf)
 Call ID: 22e4b25d-f143-4ceb-8276-a1ed1f95e1cf
  Args:
    source: Ashley_Hicks
    literal_value: 2015
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (a8c5e182-9799-4962-beec-f18f65f7f153)
 Call ID: a8c5e182-9799-4962-beec-f18f65f7f153
  Args:
    relation: :hasRelation
    source: Ashley_Hicks
    target: Kathryn_Sharkey
  AssignClass (d8e84af5-86a8-4711-8c00-5fafe7d630bb)
 Call ID: d8e84af5-86a8-4711-8c00-5fafe7d630bb
  Args:
    type: :Man
    source: William_T_Sharkey
  AssignClass (cbbced37-0c0a-4a41-b6f6-544bd107c023)
 Call ID: cbbced37-0c0a-4a41-b6f6-544bd107c023
  Args:
    source: William_T_Sharkey
    type: :Person
  AssignClass (1e4b2062-daab-42a6-822c-d08b07b3f9e0)
 Call ID: 1e4b2062-daab-42a6-822c-d08b07b3f9e0
  Args:
    type: :Woman
    source: Rosalie_Solis
  AssignClass (6449bddd-384c-4ab9-a898-9463296d6d5d)
 Call ID: 6449bddd-384c-4ab9-a898-9463296d6d5d
  Args:
    type: :Person
    source: Rosalie_Solis
  AddTriple (42a47c77-241a-47c5-bdbe-c0ceb612ac25)
 Call ID: 42a47c77-241a-47c5-bdbe-c0ceb612ac25
  Args:
    relation: :hasFather
    target: William_T_Sharkey
    source: Kathryn_Sharkey
  AddTriple (87730cc2-079f-4f0d-ba4d-cde747e1c761)
 Call ID: 87730cc2-079f-4f0d-ba4d-cde747e1c761
  Args:
    relation: :hasMother
    source: Kathryn_Sharkey
    target: Rosalie_Solis
  Finish (5944df40-4781-42b3-a064-63439ef2fb13)
 Call ID: 5944df40-4781-42b3-a064-63439ef2fb13
  Args: