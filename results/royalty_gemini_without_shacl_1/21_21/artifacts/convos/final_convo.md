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
Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), known until 2005 as Lord Romsey and until 2017 as the Lord Brabourne, is a British peer.
Life and education

Mountbatten was born at King's College Hospital in London as the eldest son of Patricia Knatchbull, née Mountbatten, later 2nd Countess Mountbatten of Burma, and film producer John Knatchbull, 7th Baron Brabourne.
Mountbatten was educated at the Dragon School, in Oxford, and Gordonstoun School, Elgin, Moray, Scotland.
On the death of his father on 23 September 2005, he became the 8th Baron Brabourne, of Brabourne in the County of Kent, in the peerage of the United Kingdom.
He also succeeded to the Knatchbull Baronetcy, of Mersham Hatch in the County of Kent, in the baronetage of England.
On the death of his mother on 13 June 2017, he became Earl Mountbatten of Burma, also a title in the peerage of the United Kingdom created for his grandfather, Admiral of the Fleet Lord Louis Mountbatten.
Mountbatten is the godfather of Philip's grandson, the Prince of Wales.
He is also related to author Jane Austen, as his father, John Knatchbull, 7th Baron Brabourne, was a direct descendant of her brother Edward Austen Knight.
Marriage and children

Mountbatten is married to Penelope Meredith Eastwood (born 16 April 1953), a daughter of Reginald Wray Frank Eastwood (1912–1980), a self-made millionaire former butcher who founded the Angus Steakhouse chain, and Marian Elizabeth (1926–2020), née Hood.
They were wed on 20 October 1979 at Romsey Abbey, less than two months after the IRA murdered his 79-year-old maternal grandfather, Louis Mountbatten, 1st
Earl Mountbatten of Burma; his 14-year-old younger brother, Nicholas Knatchbull; and his 83-year-old paternal grandmother, Doreen Knatchbull, Dowager Lady Brabourne.
The 3rd Earl Mountbatten of Burma and his wife have three children and three grandsons:


From 2010 to 2014, Mountbatten was in an extramarital relationship with Eugenie, Lady Nuttall, widow of Sir Nicholas Nuttall, 3rd Baronet, who was heir to the Edmund Nuttall Limited construction company.



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
  AssignClass (bca66c80-1e58-4732-95b1-e5b704edf003)
 Call ID: bca66c80-1e58-4732-95b1-e5b704edf003
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (e81e9bb7-1858-4065-b852-7f97334c3295)
 Call ID: e81e9bb7-1858-4065-b852-7f97334c3295
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (8f96fd52-fd35-4c9f-b0ed-97768d312585)
 Call ID: 8f96fd52-fd35-4c9f-b0ed-97768d312585
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1947
  AssignClass (861ad5fc-b63f-44a2-ad97-fa3b8b50b2d2)
 Call ID: 861ad5fc-b63f-44a2-ad97-fa3b8b50b2d2
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (dccf46c5-5b82-451b-a2f6-67759fc104e9)
 Call ID: dccf46c5-5b82-451b-a2f6-67759fc104e9
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (45923c67-5ec2-48f3-8098-0c28f52f808a)
 Call ID: 45923c67-5ec2-48f3-8098-0c28f52f808a
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (9883cf0b-4d15-45be-b953-88595313486a)
 Call ID: 9883cf0b-4d15-45be-b953-88595313486a
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (7654e65a-d4bd-4531-b099-4e94834c023c)
 Call ID: 7654e65a-d4bd-4531-b099-4e94834c023c
  Args:
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
  AddTriple (e8021607-b955-4534-bc79-73c84436d41a)
 Call ID: e8021607-b955-4534-bc79-73c84436d41a
  Args:
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
  AssignClass (19ad48ee-c10a-4765-87e8-b041a03d4ce5)
 Call ID: 19ad48ee-c10a-4765-87e8-b041a03d4ce5
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (3cb9a75e-1b57-414f-9b20-8e09a9952436)
 Call ID: 3cb9a75e-1b57-414f-9b20-8e09a9952436
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (1e32ae66-cc6e-4633-bd36-77b26a6fdd0f)
 Call ID: 1e32ae66-cc6e-4633-bd36-77b26a6fdd0f
  Args:
    source: Penelope_Meredith_Eastwood
    literal_value: 1953
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (d3ae0228-5258-43c1-b419-71883b70b4a1)
 Call ID: d3ae0228-5258-43c1-b419-71883b70b4a1
  Args:
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (32854cc0-97ea-42b2-a8d4-e59e2b07adf6)
 Call ID: 32854cc0-97ea-42b2-a8d4-e59e2b07adf6
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
  AssignClass (3c77539c-3e18-47ff-a8c4-181b1c00429e)
 Call ID: 3c77539c-3e18-47ff-a8c4-181b1c00429e
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (31c9ef5d-703b-4196-bd37-a1cd3e9c90da)
 Call ID: 31c9ef5d-703b-4196-bd37-a1cd3e9c90da
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (8a2b6bd6-3ac4-4c51-8859-0f8ac24cda37)
 Call ID: 8a2b6bd6-3ac4-4c51-8859-0f8ac24cda37
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1912
  AddLiteral (9220afd5-0056-44c7-921d-bf6fbce43c33)
 Call ID: 9220afd5-0056-44c7-921d-bf6fbce43c33
  Args:
    literal_value: 1980
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (a84b3849-9591-4640-8f49-e82788c70e0f)
 Call ID: a84b3849-9591-4640-8f49-e82788c70e0f
  Args:
    type: :Woman
    source: Marian_Elizabeth
  AssignClass (270577ec-d9d3-4686-9b35-99aa2a88720c)
 Call ID: 270577ec-d9d3-4686-9b35-99aa2a88720c
  Args:
    type: :Person
    source: Marian_Elizabeth
  AddLiteral (1dc51020-bf6e-4fd4-8632-2012003e7476)
 Call ID: 1dc51020-bf6e-4fd4-8632-2012003e7476
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Marian_Elizabeth
    literal_value: 1926
  AddLiteral (a97f5085-8eb4-4a25-84f7-0c0b4150e290)
 Call ID: a97f5085-8eb4-4a25-84f7-0c0b4150e290
  Args:
    source: Marian_Elizabeth
    literal_value: 2020
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (cab5a0bf-f1e2-493a-8aab-a30d9f148fd7)
 Call ID: cab5a0bf-f1e2-493a-8aab-a30d9f148fd7
  Args:
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
    relation: :hasFather
  AddTriple (0af045aa-d6b2-435c-af65-d69f71856716)
 Call ID: 0af045aa-d6b2-435c-af65-d69f71856716
  Args:
    target: Marian_Elizabeth
    source: Penelope_Meredith_Eastwood
    relation: :hasMother
  AssignClass (4ff671e8-e313-4af6-9c58-e321b5ca7c16)
 Call ID: 4ff671e8-e313-4af6-9c58-e321b5ca7c16
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Earl
  AssignClass (cdafc9d3-15bf-4d87-9474-7e390d12352e)
 Call ID: cdafc9d3-15bf-4d87-9474-7e390d12352e
  Args:
    type: :Person
    source: Louis_Mountbatten_1st_Earl
  AddTriple (8c3e25de-9c96-433b-b80c-a115138ea149)
 Call ID: 8c3e25de-9c96-433b-b80c-a115138ea149
  Args:
    target: Norton_Louis_Philip_Knatchbull
    source: Patricia_Knatchbull
    relation: :isMotherOf
  AddTriple (937e6a37-3347-4efe-ab82-73402582e227)
 Call ID: 937e6a37-3347-4efe-ab82-73402582e227
  Args:
    source: John_Knatchbull
    target: Norton_Louis_Philip_Knatchbull
    relation: :isFatherOf
  AssignClass (22e5fa05-b58d-4659-9485-a198f760e8c9)
 Call ID: 22e5fa05-b58d-4659-9485-a198f760e8c9
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (a45918a6-19d2-43a6-8d1c-7c8b9d4ef08c)
 Call ID: a45918a6-19d2-43a6-8d1c-7c8b9d4ef08c
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (380ae0b7-935f-41a8-a9aa-df978ff409ee)
 Call ID: 380ae0b7-935f-41a8-a9aa-df978ff409ee
  Args:
    relation: :hasBrother
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
  AssignClass (b8700601-446b-4cbe-80aa-3300641c9368)
 Call ID: b8700601-446b-4cbe-80aa-3300641c9368
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (59db24bb-92db-4c16-b434-cd2d2bb3d8fb)
 Call ID: 59db24bb-92db-4c16-b434-cd2d2bb3d8fb
  Args:
    type: :Person
    source: Doreen_Knatchbull
  AssignClass (8077c3ab-6ccc-4c04-9128-926191732e8c)
 Call ID: 8077c3ab-6ccc-4c04-9128-926191732e8c
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (595212ff-4a38-4fd0-a121-0983fcf2bff4)
 Call ID: 595212ff-4a38-4fd0-a121-0983fcf2bff4
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AssignClass (a206a2ec-0613-4005-a154-a847f5eca841)
 Call ID: a206a2ec-0613-4005-a154-a847f5eca841
  Args:
    type: :Man
    source: Nicholas_Nuttall
  AssignClass (afb6629f-ae07-456d-af41-6d577fec4110)
 Call ID: afb6629f-ae07-456d-af41-6d577fec4110
  Args:
    type: :Person
    source: Nicholas_Nuttall
  Finish (70b302b9-d3cb-4d0e-8d80-eab3b80dae5e)
 Call ID: 70b302b9-d3cb-4d0e-8d80-eab3b80dae5e
  Args: