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
  AssignClass (ffc2283f-3ee1-4e7f-8f18-52ec12a455a2)
 Call ID: ffc2283f-3ee1-4e7f-8f18-52ec12a455a2
  Args:
    type: :Man
    source: Ashley_Louis_David_Hicks
  AssignClass (78b54741-a4ea-4ee1-8ba1-9c34d753e8a6)
 Call ID: 78b54741-a4ea-4ee1-8ba1-9c34d753e8a6
  Args:
    type: :Person
    source: Ashley_Louis_David_Hicks
  AddLiteral (8db85148-cf29-44a2-8e35-a51ff727e3e5)
 Call ID: 8db85148-cf29-44a2-8e35-a51ff727e3e5
  Args:
    source: Ashley_Louis_David_Hicks
    literal_value: 1963
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
  AssignClass (69702399-df96-4d8d-b419-e490583eeab9)
 Call ID: 69702399-df96-4d8d-b419-e490583eeab9
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AssignClass (f1825e97-e456-4d71-903c-f75774b3b509)
 Call ID: f1825e97-e456-4d71-903c-f75774b3b509
  Args:
    type: :Person
    source: Lady_Pamela_Hicks
  AssignClass (83c796fc-a526-4998-9bc5-15453c5db56e)
 Call ID: 83c796fc-a526-4998-9bc5-15453c5db56e
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (56bbaef3-95a7-4854-9b91-6f2b88e3e449)
 Call ID: 56bbaef3-95a7-4854-9b91-6f2b88e3e449
  Args:
    type: :Person
    source: David_Nightingale_Hicks
  AddTriple (79e6cfc3-4e45-484b-83b8-116f6e507ca3)
 Call ID: 79e6cfc3-4e45-484b-83b8-116f6e507ca3
  Args:
    relation: :hasMother
    source: Ashley_Louis_David_Hicks
    target: Lady_Pamela_Hicks
  AddTriple (c488a263-5d86-4483-998d-9c61f40d7e1f)
 Call ID: c488a263-5d86-4483-998d-9c61f40d7e1f
  Args:
    relation: :hasFather
    source: Ashley_Louis_David_Hicks
    target: David_Nightingale_Hicks
  AssignClass (5272d42c-d2e1-4103-8063-c072f2931f3f)
 Call ID: 5272d42c-d2e1-4103-8063-c072f2931f3f
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (48dbcd24-3c10-4f66-8b6a-c04119317a0e)
 Call ID: 48dbcd24-3c10-4f66-8b6a-c04119317a0e
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (5a4b0888-fb6a-4f2b-bc64-823d5ae214ae)
 Call ID: 5a4b0888-fb6a-4f2b-bc64-823d5ae214ae
  Args:
    relation: :hasAncestor
    source: Ashley_Louis_David_Hicks
    target: Louis_Mountbatten
  AssignClass (75942401-0b21-45fb-a20e-37a458954c52)
 Call ID: 75942401-0b21-45fb-a20e-37a458954c52
  Args:
    type: :Woman
    source: Edwina_Brudenell
  AssignClass (15fdd10e-4420-4911-be53-84377ed0ea2e)
 Call ID: 15fdd10e-4420-4911-be53-84377ed0ea2e
  Args:
    type: :Person
    source: Edwina_Brudenell
  AddTriple (638c2187-3f6d-4ad2-ad61-7b87a9c07333)
 Call ID: 638c2187-3f6d-4ad2-ad61-7b87a9c07333
  Args:
    source: Ashley_Louis_David_Hicks
    target: Edwina_Brudenell
    relation: :hasSister
  AssignClass (474bbb14-1f37-45bd-a8aa-af221c6f9f70)
 Call ID: 474bbb14-1f37-45bd-a8aa-af221c6f9f70
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (a63b074c-19d2-4157-96b4-5dcffc1481b2)
 Call ID: a63b074c-19d2-4157-96b4-5dcffc1481b2
  Args:
    type: :Person
    source: India_Hicks
  AddTriple (cd042354-2b04-4ea1-8807-b75f90a4efc5)
 Call ID: cd042354-2b04-4ea1-8807-b75f90a4efc5
  Args:
    relation: :hasSister
    source: Ashley_Louis_David_Hicks
    target: India_Hicks
  AssignClass (de4ee991-958e-40b1-8fd1-8d57baebd3db)
 Call ID: de4ee991-958e-40b1-8fd1-8d57baebd3db
  Args:
    type: :Woman
    source: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (daa7d629-4d81-475a-8abd-276da10834df)
 Call ID: daa7d629-4d81-475a-8abd-276da10834df
  Args:
    type: :Person
    source: Marina_Allegra_Federica_Silvia_Tondato
  AddLiteral (6149e1a6-85c2-4289-9d05-08f1256a14bf)
 Call ID: 6149e1a6-85c2-4289-9d05-08f1256a14bf
  Args:
    literal_value: 1990
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: Ashley_Louis_David_Hicks
  AssignClass (631bd801-049b-4c40-bf08-12d1fe38882d)
 Call ID: 631bd801-049b-4c40-bf08-12d1fe38882d
  Args:
    type: :Man
    source: Dr_Carlo_Tondato
  AssignClass (91ec379e-567d-49e9-a93e-8cb5e32614ef)
 Call ID: 91ec379e-567d-49e9-a93e-8cb5e32614ef
  Args:
    type: :Person
    source: Dr_Carlo_Tondato
  AssignClass (77654a89-59d1-4283-85c3-3bb818d42f1b)
 Call ID: 77654a89-59d1-4283-85c3-3bb818d42f1b
  Args:
    type: :Woman
    source: Rosy_Maza
  AssignClass (783a664c-09da-42d3-8498-a461b06d2e3c)
 Call ID: 783a664c-09da-42d3-8498-a461b06d2e3c
  Args:
    type: :Person
    source: Rosy_Maza
  AddTriple (abc405a8-9f81-4f8e-9754-d4bfc19b4fd6)
 Call ID: abc405a8-9f81-4f8e-9754-d4bfc19b4fd6
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Dr_Carlo_Tondato
    relation: :hasFather
  AddTriple (b27264d5-65e8-4617-aae2-e830a6b60b7c)
 Call ID: b27264d5-65e8-4617-aae2-e830a6b60b7c
  Args:
    relation: :hasMother
    source: Marina_Allegra_Federica_Silvia_Tondato
    target: Rosy_Maza
  AssignClass (059c6384-c23e-4020-8898-8d9c2eeecd90)
 Call ID: 059c6384-c23e-4020-8898-8d9c2eeecd90
  Args:
    type: :Woman
    source: Kathryn_Sharkey
  AssignClass (e0be4f3d-15c3-4fcc-8563-836edb3660b7)
 Call ID: e0be4f3d-15c3-4fcc-8563-836edb3660b7
  Args:
    type: :Person
    source: Kathryn_Sharkey
  AddLiteral (dbcc0dac-46c0-4bb4-bd6b-34cfce165dad)
 Call ID: dbcc0dac-46c0-4bb4-bd6b-34cfce165dad
  Args:
    source: Ashley_Louis_David_Hicks
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 2015
  AssignClass (9b06097d-a33f-4d4c-84d2-3cb5aca90adc)
 Call ID: 9b06097d-a33f-4d4c-84d2-3cb5aca90adc
  Args:
    type: :Man
    source: William_T_Sharkey
  AssignClass (691e0614-3c84-467e-8047-0ba311afeb92)
 Call ID: 691e0614-3c84-467e-8047-0ba311afeb92
  Args:
    type: :Person
    source: William_T_Sharkey
  AssignClass (c4c7e8c0-1e6b-41f4-94c6-ad50827572c0)
 Call ID: c4c7e8c0-1e6b-41f4-94c6-ad50827572c0
  Args:
    type: :Woman
    source: Rosalie_Solis
  AssignClass (77e164d8-8613-4aa1-9bc4-04465fa7c6f7)
 Call ID: 77e164d8-8613-4aa1-9bc4-04465fa7c6f7
  Args:
    type: :Person
    source: Rosalie_Solis
  AddTriple (13e67fde-7fa4-4578-98e7-75f99bfda581)
 Call ID: 13e67fde-7fa4-4578-98e7-75f99bfda581
  Args:
    source: Kathryn_Sharkey
    target: William_T_Sharkey
    relation: :hasFather
  AddTriple (5c606af3-74b7-4c89-b293-b8aa38b05e5b)
 Call ID: 5c606af3-74b7-4c89-b293-b8aa38b05e5b
  Args:
    relation: :hasMother
    source: Kathryn_Sharkey
    target: Rosalie_Solis
  AssignClass (1e40bdd2-557b-403d-a79b-430bb3c8314a)
 Call ID: 1e40bdd2-557b-403d-a79b-430bb3c8314a
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (961a6b1a-bdb5-4f42-97da-d4481e092c06)
 Call ID: 961a6b1a-bdb5-4f42-97da-d4481e092c06
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  Finish (71cd7914-9afe-47ee-996e-8b3bec4fe3fb)
 Call ID: 71cd7914-9afe-47ee-996e-8b3bec4fe3fb
  Args: