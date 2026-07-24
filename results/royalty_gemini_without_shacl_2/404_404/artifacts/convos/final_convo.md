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
Lord Ivar Alexander Michael Mountbatten, DL (born 9 March 1963) is a British aristocrat, farmer, geologist, businessman, and reality television personality.
Early life and family

Ivar
Alexander Michael Mountbatten was born in London, to David Mountbatten, 3rd Marquess of Milford Haven, and the former Janet Mercedes Bryce.
His elder brother is George Mountbatten, 4th Marquess of Milford Haven.
His paternal grandfather was Prince George of Battenberg, through whom he is a morganatic descendant of the House of Hesse-Darmstadt.
Mountbatten grew up at Moyns Park in Essex.
In a June 2022 interview with Tatler Mountbatten commented on the 1930s Gloria Vanderbilt child custody trial, where a maid made an allegation of a lesbian affair between the child's mother Gloria Morgan Vanderbilt and the Marchioness of Milford Haven, Mountbatten's grandmother.
Mountbatten was educated at Gordonstoun School, the same school attended by Prince Philip and Charles III, and he graduated from Middlebury College in Vermont with a BA degree.
Career

Mountbatten began his career as a geologist and spent significant time working in South America during his early career.
Starting in 1995, Mountbatten began his involvement in business pursuits, including being the director of the UK subsidiary of DMX Music and being involved with Coldharbour Mill Working Wool Museum.
Mountbatten was later involved with SCL Group, the parent company of the now-defunct data analytics firm Cambridge Analytica.
Mountbatten also serves as a Deputy Lieutenant of Devon.
In 2019, Mountbatten began a career in reality television by starring in the sixth series of Treasure Island with Bear Grylls.
In October 2024, Mountbatten was announced to be part of the third season of the American reality competition series The Traitors, which premiered on 9 January 2025.
Personal life

Mountbatten married Penelope Anne Vere Thompson (born Salisbury, Wiltshire, 17 March 1966), only daughter of Colin Graham Thompson of Old Manor House, Sutton Veny, Wiltshire, and Rosemary Vere Edwardes.
In September 2016, Mountbatten revealed that he was in a relationship with James Coyle, an airline cabin services director whom he met while at a ski resort in Verbier.
Mountbatten's former wife walked him down the aisle and 'gave him away' at the suggestion of their daughters.
Mountbatten is a godparent of Lady Louise Windsor (born 2003), the daughter of Prince Edward and Sophie.
Mountbatten inherited Moyns Park in 1992 along with his brother, George Mountbatten, 4th Marquess of Milford Haven, but in 1997 moved to Bridwell Park in Uffculme, Devon.



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
  AssignClass (cb89c07b-0c4e-4bcd-a6be-7be3ba58524c)
 Call ID: cb89c07b-0c4e-4bcd-a6be-7be3ba58524c
  Args:
    source: Ivar_Mountbatten
    type: :Man
  AssignClass (fff4ea80-0e4a-4636-bbd6-92aadb0cffff)
 Call ID: fff4ea80-0e4a-4636-bbd6-92aadb0cffff
  Args:
    source: Ivar_Mountbatten
    type: :Person
  AddLiteral (33a62646-6fc0-4caa-ba55-d0dd1b2944cb)
 Call ID: 33a62646-6fc0-4caa-ba55-d0dd1b2944cb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ivar_Mountbatten
    literal_value: 1963
  AssignClass (c27af28e-e4e0-40df-919b-78bdbd08bbee)
 Call ID: c27af28e-e4e0-40df-919b-78bdbd08bbee
  Args:
    type: :Man
    source: David_Mountbatten
  AssignClass (b0c99e61-7eab-4048-a16b-04320519b1f3)
 Call ID: b0c99e61-7eab-4048-a16b-04320519b1f3
  Args:
    type: :Person
    source: David_Mountbatten
  AddTriple (99dcb586-21af-4d90-8436-55376d9ea4de)
 Call ID: 99dcb586-21af-4d90-8436-55376d9ea4de
  Args:
    target: David_Mountbatten
    relation: :hasFather
    source: Ivar_Mountbatten
  AssignClass (562c3afa-8e4b-49fa-bad0-21e7176cbce2)
 Call ID: 562c3afa-8e4b-49fa-bad0-21e7176cbce2
  Args:
    source: Janet_Mercedes_Bryce
    type: :Woman
  AssignClass (5f90ada3-47cd-4ad3-9eef-52ae93a936bd)
 Call ID: 5f90ada3-47cd-4ad3-9eef-52ae93a936bd
  Args:
    type: :Person
    source: Janet_Mercedes_Bryce
  AddTriple (57d78f06-96ff-4aac-a8a0-e84ac7dc7a81)
 Call ID: 57d78f06-96ff-4aac-a8a0-e84ac7dc7a81
  Args:
    relation: :hasMother
    source: Ivar_Mountbatten
    target: Janet_Mercedes_Bryce
  AssignClass (7095bf68-0770-4315-8cf0-d16a9153dbb1)
 Call ID: 7095bf68-0770-4315-8cf0-d16a9153dbb1
  Args:
    source: George_Mountbatten_4th_Marquess
    type: :Man
  AssignClass (b3702a3c-0db1-4c66-8644-120d27905da6)
 Call ID: b3702a3c-0db1-4c66-8644-120d27905da6
  Args:
    type: :Person
    source: George_Mountbatten_4th_Marquess
  AddTriple (42c28a0c-7d44-4afb-a4a7-98660fd7ae37)
 Call ID: 42c28a0c-7d44-4afb-a4a7-98660fd7ae37
  Args:
    relation: :hasBrother
    source: Ivar_Mountbatten
    target: George_Mountbatten_4th_Marquess
  AssignClass (d536aab6-1044-40cc-b592-2e5ef584ecdd)
 Call ID: d536aab6-1044-40cc-b592-2e5ef584ecdd
  Args:
    source: Prince_George_of_Battenberg
    type: :Man
  AssignClass (35a62963-94c6-47e1-ad11-b1ef43fd6cfe)
 Call ID: 35a62963-94c6-47e1-ad11-b1ef43fd6cfe
  Args:
    type: :Person
    source: Prince_George_of_Battenberg
  AddTriple (3c306c8f-18fb-4f52-a199-30510cb7d2ba)
 Call ID: 3c306c8f-18fb-4f52-a199-30510cb7d2ba
  Args:
    source: Ivar_Mountbatten
    relation: :hasAncestor
    target: Prince_George_of_Battenberg
  AssignClass (7561c37e-f0be-4462-b52c-4602042bf46e)
 Call ID: 7561c37e-f0be-4462-b52c-4602042bf46e
  Args:
    source: Penelope_Anne_Vere_Thompson
    type: :Woman
  AssignClass (09086a89-c341-46a5-8a88-2e98bece1464)
 Call ID: 09086a89-c341-46a5-8a88-2e98bece1464
  Args:
    type: :Person
    source: Penelope_Anne_Vere_Thompson
  AddLiteral (f7c364e5-9883-4e9b-b478-f3e6a916a1fc)
 Call ID: f7c364e5-9883-4e9b-b478-f3e6a916a1fc
  Args:
    relation: :hasBirthYear
    source: Penelope_Anne_Vere_Thompson
    literal_value: 1966
    literal_type: xsd:integer
  AssignClass (f6da6cb3-a587-48f0-b7ec-df344a3f3e83)
 Call ID: f6da6cb3-a587-48f0-b7ec-df344a3f3e83
  Args:
    type: :Man
    source: Colin_Graham_Thompson
  AssignClass (d66b0e61-585d-4003-bc56-48b8a05724cc)
 Call ID: d66b0e61-585d-4003-bc56-48b8a05724cc
  Args:
    source: Colin_Graham_Thompson
    type: :Person
  AddTriple (663e5982-0262-40f7-9702-8cb684705c75)
 Call ID: 663e5982-0262-40f7-9702-8cb684705c75
  Args:
    source: Penelope_Anne_Vere_Thompson
    relation: :hasFather
    target: Colin_Graham_Thompson
  AssignClass (0f7d0f70-dbb0-41f8-a19d-77096f92e696)
 Call ID: 0f7d0f70-dbb0-41f8-a19d-77096f92e696
  Args:
    type: :Woman
    source: Rosemary_Vere_Edwardes
  AssignClass (8618b299-0789-4a9f-8458-fea168d58dbe)
 Call ID: 8618b299-0789-4a9f-8458-fea168d58dbe
  Args:
    type: :Person
    source: Rosemary_Vere_Edwardes
  AddTriple (861ba29a-57ac-4b32-928f-e425b631b038)
 Call ID: 861ba29a-57ac-4b32-928f-e425b631b038
  Args:
    target: Rosemary_Vere_Edwardes
    source: Penelope_Anne_Vere_Thompson
    relation: :hasMother
  AssignClass (26d109f8-fd15-4dc4-bbc9-f60b57cf23c4)
 Call ID: 26d109f8-fd15-4dc4-bbc9-f60b57cf23c4
  Args:
    source: James_Coyle
    type: :Man
  AssignClass (6987b4b9-37f0-4d0b-993f-a0c5bcffe480)
 Call ID: 6987b4b9-37f0-4d0b-993f-a0c5bcffe480
  Args:
    type: :Person
    source: James_Coyle
  AssignClass (12b6b297-de88-470f-acfc-aeecb5abe471)
 Call ID: 12b6b297-de88-470f-acfc-aeecb5abe471
  Args:
    type: :Woman
    source: Lady_Louise_Windsor
  AssignClass (65bc9812-0eac-46f8-bff0-00473808fba0)
 Call ID: 65bc9812-0eac-46f8-bff0-00473808fba0
  Args:
    source: Lady_Louise_Windsor
    type: :Person
  AddLiteral (8ad0419a-36de-43e6-9e64-96125976db1b)
 Call ID: 8ad0419a-36de-43e6-9e64-96125976db1b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Lady_Louise_Windsor
    literal_value: 2003
  AssignClass (13da60c8-a618-42d4-871f-e4391a2e4bfd)
 Call ID: 13da60c8-a618-42d4-871f-e4391a2e4bfd
  Args:
    type: :Man
    source: Prince_Edward
  AssignClass (05b15299-4d9e-418b-aeef-700d8ae86d91)
 Call ID: 05b15299-4d9e-418b-aeef-700d8ae86d91
  Args:
    type: :Person
    source: Prince_Edward
  AssignClass (5a47d9ab-529e-4527-ae44-65f376bf241d)
 Call ID: 5a47d9ab-529e-4527-ae44-65f376bf241d
  Args:
    source: Sophie
    type: :Woman
  AssignClass (963474e9-695b-4e5f-9fba-9d42f7d0987f)
 Call ID: 963474e9-695b-4e5f-9fba-9d42f7d0987f
  Args:
    type: :Person
    source: Sophie
  AddTriple (42496bb5-01fd-48aa-a6df-76d91a985d1d)
 Call ID: 42496bb5-01fd-48aa-a6df-76d91a985d1d
  Args:
    source: Lady_Louise_Windsor
    relation: :hasFather
    target: Prince_Edward
  AddTriple (1935b939-6058-4a83-adab-63dc0e7ca2cd)
 Call ID: 1935b939-6058-4a83-adab-63dc0e7ca2cd
  Args:
    target: Sophie
    relation: :hasMother
    source: Lady_Louise_Windsor
  Finish (ab78fa59-946b-423e-99f8-7d6b3d9c2889)
 Call ID: ab78fa59-946b-423e-99f8-7d6b3d9c2889
  Args: