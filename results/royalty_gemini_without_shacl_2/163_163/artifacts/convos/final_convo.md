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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Infanta Margarita, Duchess of Soria, 2nd Duchess of Hernani (Margarita María de la Victoria Esperanza
Jacoba Felicidad Perpetua de Todos los Santos de Borbón y Borbón; born 6 March 1939), is the younger sister of King Juan Carlos I and aunt of the reigning King Felipe VI of Spain.
Early life

Infanta Margarita was born at Hotel Firenze Anglo American in Rome as the younger daughter of Infante Juan, Count of Barcelona, and Princess Mercedes of the Two Sicilies.
Margarita has been blind since birth.
Marriage

She married the physician and aristocrat Carlos Zurita y Delgado on 12 October 1972 in Estoril at St. Anthony's Church.
They have two children:


Activities

In 1989, alongside her husband, they created The Duke and Duchess of Soria Cultural Foundation (Spanish: Fundación Cultural Duques de Soria), a nonprofit organization dedicated to the promotion of Spanish culture, Hispanic studies, science and knowledge, as well as the preservation of cultural heritage.
Titles, styles and honours

Infanta Margarita renounced her right of succession to the Spanish throne upon marriage because it was not a dynastic wedding.
On 6 January 1979, the Infanta's distant cousin Manfredo de Borbón, 1st Duke of Hernani, died and willed his ducal title to be inherited by Margarita.
The King granted this request in 1977 and, on 27 May 1981, she became 2nd Duchess of Hernani, accompanied by the dignity of Grandee.
The peerage title refers to the town Hernani, Spain.
The month after, on 23 June 1981, King Juan Carlos created her Duchess of Soria (referring to the city Soria, Spain); this title is a title of the Royal House and cannot be inherited by her children.



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
  AssignClass (85396d3d-e252-4294-a67c-219dfdd8c384)
 Call ID: 85396d3d-e252-4294-a67c-219dfdd8c384
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (ea834500-5dc7-40a7-ad37-c88c7fb308de)
 Call ID: ea834500-5dc7-40a7-ad37-c88c7fb308de
  Args:
    type: :Woman
    source: Sofia
  AssignClass (609a7547-080b-4d1f-b742-493f314330ee)
 Call ID: 609a7547-080b-4d1f-b742-493f314330ee
  Args:
    type: :Woman
    source: Margarita_de_Borbon
  AssignClass (36f17d4c-0f6d-4a65-8f29-21e086934987)
 Call ID: 36f17d4c-0f6d-4a65-8f29-21e086934987
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (3fa1c1e6-7205-447f-8b44-967a6ddca729)
 Call ID: 3fa1c1e6-7205-447f-8b44-967a6ddca729
  Args:
    source: Mercedes_of_the_Two_Sicilies
    type: :Woman
  AssignClass (66e08a29-ab4c-4820-a791-19779e0fb950)
 Call ID: 66e08a29-ab4c-4820-a791-19779e0fb950
  Args:
    source: Carlos_Zurita_y_Delgado
    type: :Man
  AssignClass (4b89d0ef-b0c2-4ba7-825f-16b3a0e12f65)
 Call ID: 4b89d0ef-b0c2-4ba7-825f-16b3a0e12f65
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (194f1874-dd78-441e-89bc-cbec97eab4ec)
 Call ID: 194f1874-dd78-441e-89bc-cbec97eab4ec
  Args:
    source: Manfredo_de_Borbon
    type: :Man
  AddLiteral (1117baf7-4857-42db-bbc0-825d34c5e17d)
 Call ID: 1117baf7-4857-42db-bbc0-825d34c5e17d
  Args:
    source: Margarita_de_Borbon
    literal_value: 1939
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (0179af59-ac63-4ea6-9d24-015ecd5cf007)
 Call ID: 0179af59-ac63-4ea6-9d24-015ecd5cf007
  Args:
    source: Juan_Carlos_I
    relation: :hasSister
    target: Margarita_de_Borbon
  AddTriple (201d7cf4-b7c9-41ab-885b-457bbfc62c79)
 Call ID: 201d7cf4-b7c9-41ab-885b-457bbfc62c79
  Args:
    target: Juan_Carlos_I
    relation: :isSisterOf
    source: Margarita_de_Borbon
  AddTriple (6019d4c6-10df-4027-8f9b-62e2ade9ff2a)
 Call ID: 6019d4c6-10df-4027-8f9b-62e2ade9ff2a
  Args:
    relation: :hasFather
    target: Juan_Count_of_Barcelona
    source: Margarita_de_Borbon
  AddTriple (ab2f8ebd-903a-4530-8453-99a55c30496d)
 Call ID: ab2f8ebd-903a-4530-8453-99a55c30496d
  Args:
    relation: :hasMother
    target: Mercedes_of_the_Two_Sicilies
    source: Margarita_de_Borbon
  AddTriple (b706b6cb-aef5-4969-8d38-2431363b411d)
 Call ID: b706b6cb-aef5-4969-8d38-2431363b411d
  Args:
    target: Juan_Count_of_Barcelona
    relation: :hasFather
    source: Juan_Carlos_I
  AddTriple (c4f5acc2-0030-43a4-8065-dfa20225afd6)
 Call ID: c4f5acc2-0030-43a4-8065-dfa20225afd6
  Args:
    relation: :hasMother
    target: Mercedes_of_the_Two_Sicilies
    source: Juan_Carlos_I
  AddTriple (47b1807b-b8ae-48a8-8c9f-eccc0c023e1c)
 Call ID: 47b1807b-b8ae-48a8-8c9f-eccc0c023e1c
  Args:
    target: Margarita_de_Borbon
    relation: :isFatherOf
    source: Juan_Count_of_Barcelona
  AddTriple (a99cff6c-20c5-489e-8f53-03e9d55fda00)
 Call ID: a99cff6c-20c5-489e-8f53-03e9d55fda00
  Args:
    target: Juan_Carlos_I
    relation: :isFatherOf
    source: Juan_Count_of_Barcelona
  AddTriple (f995e0a0-d91c-4a4e-83f1-eae5b04edaed)
 Call ID: f995e0a0-d91c-4a4e-83f1-eae5b04edaed
  Args:
    source: Mercedes_of_the_Two_Sicilies
    target: Margarita_de_Borbon
    relation: :isMotherOf
  AddTriple (25560aa5-ac24-4912-a387-b728ec15cb02)
 Call ID: 25560aa5-ac24-4912-a387-b728ec15cb02
  Args:
    target: Juan_Carlos_I
    relation: :isMotherOf
    source: Mercedes_of_the_Two_Sicilies
  AddTriple (50f72dfa-4242-421d-b30a-0193058062c2)
 Call ID: 50f72dfa-4242-421d-b30a-0193058062c2
  Args:
    relation: :hasRelation
    target: Carlos_Zurita_y_Delgado
    source: Margarita_de_Borbon
  AddLiteral (f9cb5a39-3cf0-4ee0-92f5-ef77cc409e72)
 Call ID: f9cb5a39-3cf0-4ee0-92f5-ef77cc409e72
  Args:
    literal_value: 1972
    source: Margarita_de_Borbon
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (c3737a75-0b6b-445c-b2cb-fe365ba0ca92)
 Call ID: c3737a75-0b6b-445c-b2cb-fe365ba0ca92
  Args:
    source: Margarita_de_Borbon
    target: Felipe_VI
    relation: :isAuntOf
  Finish (1b0cb3bb-62a9-46de-8242-3b1818b2f0aa)
 Call ID: 1b0cb3bb-62a9-46de-8242-3b1818b2f0aa
  Args: