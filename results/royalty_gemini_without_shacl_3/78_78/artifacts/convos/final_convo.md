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
  AssignClass (88817ec9-bf8c-48c9-9d3c-029673dc2fdb)
 Call ID: 88817ec9-bf8c-48c9-9d3c-029673dc2fdb
  Args:
    source: Ashley_Louis_David_Hicks
    type: :Person
  AssignClass (93635bd1-d5f7-4129-b482-7c8987246c59)
 Call ID: 93635bd1-d5f7-4129-b482-7c8987246c59
  Args:
    type: :Man
    source: Ashley_Louis_David_Hicks
  AddLiteral (d12207f5-a13f-4fe1-88c8-f0af18a4e90d)
 Call ID: d12207f5-a13f-4fe1-88c8-f0af18a4e90d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Ashley_Louis_David_Hicks
    literal_value: 1963
  AssignClass (d8f7d119-87d2-4f99-915b-7996355d8c37)
 Call ID: d8f7d119-87d2-4f99-915b-7996355d8c37
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AssignClass (319dcf5b-c24c-4b3f-b33c-e0092a30dd7e)
 Call ID: 319dcf5b-c24c-4b3f-b33c-e0092a30dd7e
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AssignClass (4e0bcb11-0934-4caf-a713-0abe2582c38c)
 Call ID: 4e0bcb11-0934-4caf-a713-0abe2582c38c
  Args:
    type: :Person
    source: David_Nightingale_Hicks
  AssignClass (5b75dd93-aaac-4c55-933d-cac72c42f4d5)
 Call ID: 5b75dd93-aaac-4c55-933d-cac72c42f4d5
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AddTriple (84ab9c9a-cbf5-464f-9a08-6e82b5b5b6f1)
 Call ID: 84ab9c9a-cbf5-464f-9a08-6e82b5b5b6f1
  Args:
    target: David_Nightingale_Hicks
    source: Ashley_Louis_David_Hicks
    relation: :hasFather
  AddTriple (a415f80f-b7d4-4e1b-bd05-cae31bd3dd4c)
 Call ID: a415f80f-b7d4-4e1b-bd05-cae31bd3dd4c
  Args:
    target: Lady_Pamela_Hicks
    source: Ashley_Louis_David_Hicks
    relation: :hasMother
  AssignClass (418fb51c-1cbf-45b5-b1eb-f736cbe8072a)
 Call ID: 418fb51c-1cbf-45b5-b1eb-f736cbe8072a
  Args:
    source: Louis_Mountbatten
    type: :Person
  AssignClass (7b912f35-aebd-4fd5-8f87-a53b82032dd5)
 Call ID: 7b912f35-aebd-4fd5-8f87-a53b82032dd5
  Args:
    source: Louis_Mountbatten
    type: :Man
  AddTriple (8d83ddf0-1c99-4168-be26-a0c2d2c72914)
 Call ID: 8d83ddf0-1c99-4168-be26-a0c2d2c72914
  Args:
    source: Ashley_Louis_David_Hicks
    target: Louis_Mountbatten
    relation: :hasAncestor
  AssignClass (79461150-ffa7-4e2e-8b99-5810014918ff)
 Call ID: 79461150-ffa7-4e2e-8b99-5810014918ff
  Args:
    source: Edwina_Brudenell
    type: :Person
  AssignClass (19e25e33-5f46-460b-9c38-28843db080f2)
 Call ID: 19e25e33-5f46-460b-9c38-28843db080f2
  Args:
    source: Edwina_Brudenell
    type: :Woman
  AddTriple (9467a3f0-5ead-4651-b933-44ae12abbfbf)
 Call ID: 9467a3f0-5ead-4651-b933-44ae12abbfbf
  Args:
    relation: :hasSister
    target: Edwina_Brudenell
    source: Ashley_Louis_David_Hicks
  AssignClass (4244472d-a0b3-4073-a04d-03514fb52a21)
 Call ID: 4244472d-a0b3-4073-a04d-03514fb52a21
  Args:
    type: :Person
    source: India_Hicks
  AssignClass (b0ab70f7-cf7c-4307-ae40-b84085e94bfc)
 Call ID: b0ab70f7-cf7c-4307-ae40-b84085e94bfc
  Args:
    source: India_Hicks
    type: :Woman
  AddTriple (b57c9540-83bb-4d70-9eb8-25fbf2748f03)
 Call ID: b57c9540-83bb-4d70-9eb8-25fbf2748f03
  Args:
    source: Ashley_Louis_David_Hicks
    target: India_Hicks
    relation: :hasSister
  AssignClass (ac72a023-5a7d-4987-bd25-b15ef83509f2)
 Call ID: ac72a023-5a7d-4987-bd25-b15ef83509f2
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    type: :Person
  AssignClass (1d59f14b-8008-468c-a303-e15f9aae439f)
 Call ID: 1d59f14b-8008-468c-a303-e15f9aae439f
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    type: :Woman
  AddLiteral (a17c66c9-bbad-44c4-8f5e-7103fdfaef93)
 Call ID: a17c66c9-bbad-44c4-8f5e-7103fdfaef93
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    literal_type: xsd:integer
    literal_value: 1960
    relation: :hasBirthYear
  AddLiteral (7b0bf990-e601-4205-ac31-14770f28b051)
 Call ID: 7b0bf990-e601-4205-ac31-14770f28b051
  Args:
    literal_value: 1990
    source: Ashley_Louis_David_Hicks
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (0973be4c-0e26-43c2-a1b9-5dfa81b9bd20)
 Call ID: 0973be4c-0e26-43c2-a1b9-5dfa81b9bd20
  Args:
    target: Marina_Allegra_Federica_Silvia_Tondato
    source: Ashley_Louis_David_Hicks
    relation: :hasRelation
  AssignClass (7d4ee76a-12e4-42a0-940d-a9c0f87efa4a)
 Call ID: 7d4ee76a-12e4-42a0-940d-a9c0f87efa4a
  Args:
    type: :Person
    source: Dr_Carlo_Tondato
  AssignClass (67af41b6-d7f5-44d7-872f-70bde0001fc4)
 Call ID: 67af41b6-d7f5-44d7-872f-70bde0001fc4
  Args:
    type: :Man
    source: Dr_Carlo_Tondato
  AssignClass (03a7d43c-73ae-4924-8203-273d1d4fedca)
 Call ID: 03a7d43c-73ae-4924-8203-273d1d4fedca
  Args:
    source: Rosy_Maza
    type: :Person
  AssignClass (beda83ab-da62-42b8-b3bb-5b217ab474d0)
 Call ID: beda83ab-da62-42b8-b3bb-5b217ab474d0
  Args:
    source: Rosy_Maza
    type: :Woman
  AddTriple (17ce8ecb-b4a4-46ee-89b8-f7fbb8ff0523)
 Call ID: 17ce8ecb-b4a4-46ee-89b8-f7fbb8ff0523
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Dr_Carlo_Tondato
    relation: :hasFather
  AddTriple (ed604645-56f7-4052-9298-9ab7a1bcbea1)
 Call ID: ed604645-56f7-4052-9298-9ab7a1bcbea1
  Args:
    relation: :hasMother
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Rosy_Maza
  AssignClass (26c83fb1-b420-445e-8988-b947202c7066)
 Call ID: 26c83fb1-b420-445e-8988-b947202c7066
  Args:
    source: Kathryn_Sharkey
    type: :Person
  AssignClass (67abd841-8c56-4624-8908-787936356523)
 Call ID: 67abd841-8c56-4624-8908-787936356523
  Args:
    source: Kathryn_Sharkey
    type: :Woman
  AddLiteral (639627fe-3413-42cd-8aa4-10bdb95d2810)
 Call ID: 639627fe-3413-42cd-8aa4-10bdb95d2810
  Args:
    relation: :hasBirthYear
    literal_value: 1981
    source: Kathryn_Sharkey
    literal_type: xsd:integer
  AddLiteral (fa152bd8-804f-4894-9471-2c33d7b917d7)
 Call ID: fa152bd8-804f-4894-9471-2c33d7b917d7
  Args:
    literal_value: 2015
    literal_type: xsd:integer
    source: Ashley_Louis_David_Hicks
    relation: :hasMarriageYear
  AddTriple (b08685b2-6b5d-4d09-aa0a-d311ef4a968e)
 Call ID: b08685b2-6b5d-4d09-aa0a-d311ef4a968e
  Args:
    relation: :hasRelation
    source: Ashley_Louis_David_Hicks
    target: Kathryn_Sharkey
  AssignClass (e20796f1-cd07-4506-94bd-87fe133387b4)
 Call ID: e20796f1-cd07-4506-94bd-87fe133387b4
  Args:
    source: William_T_Sharkey
    type: :Person
  AssignClass (4b741120-c385-4e98-94f1-abdfedac1aff)
 Call ID: 4b741120-c385-4e98-94f1-abdfedac1aff
  Args:
    source: William_T_Sharkey
    type: :Man
  AssignClass (0a6aa254-1f83-4ef1-bca1-93b7d8ebc4cc)
 Call ID: 0a6aa254-1f83-4ef1-bca1-93b7d8ebc4cc
  Args:
    type: :Person
    source: Rosalie_Solis
  AssignClass (6306b7ad-bd27-451f-b2dd-541b955413de)
 Call ID: 6306b7ad-bd27-451f-b2dd-541b955413de
  Args:
    type: :Woman
    source: Rosalie_Solis
  AddTriple (6769167c-d4be-415b-a59b-2cd61337cd97)
 Call ID: 6769167c-d4be-415b-a59b-2cd61337cd97
  Args:
    relation: :hasFather
    source: Kathryn_Sharkey
    target: William_T_Sharkey
  AddTriple (97dafa5b-b9b9-4861-8d34-22486caf933a)
 Call ID: 97dafa5b-b9b9-4861-8d34-22486caf933a
  Args:
    relation: :hasMother
    source: Kathryn_Sharkey
    target: Rosalie_Solis
  AssignClass (3bde43cc-0454-4fac-b2c5-3175652a17e4)
 Call ID: 3bde43cc-0454-4fac-b2c5-3175652a17e4
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AssignClass (7880b40a-c0fe-437b-9bd0-42906e859e24)
 Call ID: 7880b40a-c0fe-437b-9bd0-42906e859e24
  Args:
    source: Nicholas_Knatchbull
    type: :Man
  AddTriple (3a80aa82-703f-4585-8588-87b82d4f8b1a)
 Call ID: 3a80aa82-703f-4585-8588-87b82d4f8b1a
  Args:
    relation: :hasRelation
    source: Ashley_Louis_David_Hicks
    target: Nicholas_Knatchbull
  Finish (5b57f360-1477-4fa0-8e47-427ec54f287a)
 Call ID: 5b57f360-1477-4fa0-8e47-427ec54f287a
  Args: