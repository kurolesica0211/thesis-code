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
Duchess Elisabeth of Mecklenburg-Schwerin (10 August 1869 – 3 September 1955) was a daughter of Frederick Francis II, Grand Duke of Mecklenburg by his third wife Princess Marie of Schwarzburg-Rudolstadt.
By her marriage to Frederick Augustus II, she became the consort of the last reigning Grand Duke of Oldenburg.
Family

Elisabeth was related to many of Europe's royal families.
She was the eldest child of Frederick Francis II, Grand Duke of Mecklenburg by his third wife, Princess Marie of Schwarzburg-Rudolstadt.
She was an older sister of Hendrik, Prince consort of the Netherlands, husband of Queen Wilhelmina of the Netherlands, making her an aunt of Queen Juliana of the Netherlands.
She was also a younger half-sister of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin.
Through Frederick Francis, she was an aunt of Alexandrine, Queen of Denmark and Cecilie, German Crown Princess.
Elisabeth was also a half sister of Marie, Grand Duchess of Russia, who was the mother of Grand Duke Cyril Vladimirovich of Russia, the pretender to the Russian throne.
Her paternal grandparents were Paul Frederick, Grand Duke of Mecklenburg and Princess Alexandrine of Prussia.
Her maternal grandparents were Prince Adolph of Schwarzburg-Rudolstadt and Princess Mathilde of Schönburg-Waldenburg.
Marriage

On 24 October 1896, Elisabeth married Frederick Augustus, Hereditary Grand Duke of Oldenburg.
His first wife Elisabeth Anna had died the previous year, leaving only one surviving daughter: Duchess Sophia Charlotte of Oldenburg.
Frederick Augustus was thus in need of a male heir.
He succeeded as Grand Duke of Oldenburg in 1900, making Elisabeth Grand Duchess consort of Oldenburg.
They had five children:


Frederick was forced to abdicate his throne at the end of World War I, when the former Grand Duchy of the German Empire joined the post-war German Republic.
A year after his abdication, he asked the Oldenburg Diet for a yearly allowance of 150,000 marks, stating that his financial condition was "extremely precarious".
In 1931, Frederick died in Rastede.
Elisabeth died on 3 September 1955, having been widowed for 24 years.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c8895f01-d094-4472-b8d8-ba8947f23083)
 Call ID: c8895f01-d094-4472-b8d8-ba8947f23083
  Args:
    source: :Elisabeth_of_Mecklenburg-Schwerin
    type: :Woman
  AddLiteral (38bb1689-2c12-4f75-8e90-e13fe92a7699)
 Call ID: 38bb1689-2c12-4f75-8e90-e13fe92a7699
  Args:
    source: :Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1869
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7b27ab75-3cbf-45b6-bd42-62fa0440f4a5)
 Call ID: 7b27ab75-3cbf-45b6-bd42-62fa0440f4a5
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1955
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (6dc15496-3dac-419d-9fd4-1f56a704ef11)
 Call ID: 6dc15496-3dac-419d-9fd4-1f56a704ef11
  Args:
    type: :Man
    source: :Frederick_Francis_II_of_Mecklenburg
  AssignClass (7ceb1275-afe6-4348-84ef-10349d7d76e0)
 Call ID: 7ceb1275-afe6-4348-84ef-10349d7d76e0
  Args:
    source: :Marie_of_Schwarzburg-Rudolstadt
    type: :Woman
  AddTriple (b4478352-0eef-4732-a3e5-71f3d912aecc)
 Call ID: b4478352-0eef-4732-a3e5-71f3d912aecc
  Args:
    relation: :hasFather
    target: :Frederick_Francis_II_of_Mecklenburg
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AddTriple (ed9c0b8b-2897-44ac-b485-51bdfb1f0ca0)
 Call ID: ed9c0b8b-2897-44ac-b485-51bdfb1f0ca0
  Args:
    target: :Marie_of_Schwarzburg-Rudolstadt
    relation: :hasMother
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (797c8acf-e3eb-46a3-920a-8e1f2f42bcff)
 Call ID: 797c8acf-e3eb-46a3-920a-8e1f2f42bcff
  Args:
    type: :Man
    source: :Frederick_Augustus_II_of_Oldenburg
  AddLiteral (42a2b58a-b25f-4f3e-ac1d-069be3c0cc64)
 Call ID: 42a2b58a-b25f-4f3e-ac1d-069be3c0cc64
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1896
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AddTriple (48ab0210-826b-482a-a6fd-1fec016b509c)
 Call ID: 48ab0210-826b-482a-a6fd-1fec016b509c
  Args:
    relation: :hasRelation
    target: :Frederick_Augustus_II_of_Oldenburg
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (fcb0c1db-cb5d-480b-8a82-dc9f71dada38)
 Call ID: fcb0c1db-cb5d-480b-8a82-dc9f71dada38
  Args:
    source: :Hendrik_Prince_Consort_of_the_Netherlands
    type: :Man
  AddTriple (ed9c00f9-f970-4dbe-b95e-7fb091888ce0)
 Call ID: ed9c00f9-f970-4dbe-b95e-7fb091888ce0
  Args:
    target: :Hendrik_Prince_Consort_of_the_Netherlands
    relation: :isSiblingOf
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (31e0abb2-c671-4059-8014-b1292bc8c641)
 Call ID: 31e0abb2-c671-4059-8014-b1292bc8c641
  Args:
    type: :Woman
    source: :Queen_Wilhelmina_of_the_Netherlands
  AddTriple (3f8e7354-4cb6-4233-9f7a-8a1dfbf692d3)
 Call ID: 3f8e7354-4cb6-4233-9f7a-8a1dfbf692d3
  Args:
    source: :Hendrik_Prince_Consort_of_the_Netherlands
    target: :Queen_Wilhelmina_of_the_Netherlands
    relation: :hasRelation
  AssignClass (0a33053b-6f38-40b3-b050-e23ca0245e96)
 Call ID: 0a33053b-6f38-40b3-b050-e23ca0245e96
  Args:
    source: :Queen_Juliana_of_the_Netherlands
    type: :Woman
  AddTriple (3858116e-77a2-40b2-816d-577310a8dc92)
 Call ID: 3858116e-77a2-40b2-816d-577310a8dc92
  Args:
    relation: :isAuntOf
    target: :Queen_Juliana_of_the_Netherlands
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (5ab34cb6-8ff5-4a4d-bd03-6a5cd2756ed6)
 Call ID: 5ab34cb6-8ff5-4a4d-bd03-6a5cd2756ed6
  Args:
    source: :Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (7b4dddec-a546-40ed-b7ba-029035ea5a3f)
 Call ID: 7b4dddec-a546-40ed-b7ba-029035ea5a3f
  Args:
    target: :Frederick_Francis_III_of_Mecklenburg-Schwerin
    relation: :isSiblingOf
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (64ca50a9-7a0e-43e2-874a-5f68def00007)
 Call ID: 64ca50a9-7a0e-43e2-874a-5f68def00007
  Args:
    type: :Woman
    source: :Alexandrine_Queen_of_Denmark
  AssignClass (744753e9-f34e-44d8-a0ca-f09bd522ab17)
 Call ID: 744753e9-f34e-44d8-a0ca-f09bd522ab17
  Args:
    source: :Cecilie_German_Crown_Princess
    type: :Woman
  AddTriple (2eaba3e0-c218-4d5b-8ffd-4b1b081236fe)
 Call ID: 2eaba3e0-c218-4d5b-8ffd-4b1b081236fe
  Args:
    source: :Elisabeth_of_Mecklenburg-Schwerin
    relation: :isAuntOf
    target: :Alexandrine_Queen_of_Denmark
  AddTriple (bc728c6e-1890-4681-96ce-ccb856083697)
 Call ID: bc728c6e-1890-4681-96ce-ccb856083697
  Args:
    relation: :isAuntOf
    target: :Cecilie_German_Crown_Princess
    source: :Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (2a0854dc-5668-413c-abc7-efb52d9f54c9)
 Call ID: 2a0854dc-5668-413c-abc7-efb52d9f54c9
  Args:
    source: :Marie_Grand_Duchess_of_Russia
    type: :Woman
  AddTriple (d89555b2-a683-4e92-83ec-7b454bfc6d6a)
 Call ID: d89555b2-a683-4e92-83ec-7b454bfc6d6a
  Args:
    source: :Elisabeth_of_Mecklenburg-Schwerin
    target: :Marie_Grand_Duchess_of_Russia
    relation: :isSiblingOf
  AssignClass (408f7573-f9f4-4728-aae1-2e0cc5b3601d)
 Call ID: 408f7573-f9f4-4728-aae1-2e0cc5b3601d
  Args:
    type: :Man
    source: :Cyril_Vladimirovich_Grand_Duke_of_Russia
  AddTriple (87abe4ed-8b89-4105-9994-cd0a3d580bac)
 Call ID: 87abe4ed-8b89-4105-9994-cd0a3d580bac
  Args:
    target: :Marie_Grand_Duchess_of_Russia
    relation: :hasMother
    source: :Cyril_Vladimirovich_Grand_Duke_of_Russia
  AssignClass (9099db9a-95ea-4930-a688-17e218ce2a88)
 Call ID: 9099db9a-95ea-4930-a688-17e218ce2a88
  Args:
    type: :Man
    source: :Paul_Frederick_Grand_Duke_of_Mecklenburg
  AssignClass (708eabc4-603a-4a6c-95dd-4e0c3821d2d6)
 Call ID: 708eabc4-603a-4a6c-95dd-4e0c3821d2d6
  Args:
    source: :Alexandrine_of_Prussia
    type: :Woman
  AddTriple (e00f4e3d-102f-4448-b553-f4699f7f9c3c)
 Call ID: e00f4e3d-102f-4448-b553-f4699f7f9c3c
  Args:
    source: :Frederick_Francis_II_of_Mecklenburg
    target: :Paul_Frederick_Grand_Duke_of_Mecklenburg
    relation: :hasFather
  AddTriple (01ac95c5-0390-4021-80cb-a26cfc19cd03)
 Call ID: 01ac95c5-0390-4021-80cb-a26cfc19cd03
  Args:
    relation: :hasMother
    target: :Alexandrine_of_Prussia
    source: :Frederick_Francis_II_of_Mecklenburg
  AssignClass (5dde9e99-1a5b-42cd-98c6-787003d2a396)
 Call ID: 5dde9e99-1a5b-42cd-98c6-787003d2a396
  Args:
    type: :Man
    source: :Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (8c035602-2077-437b-a932-ae8ba6086ae3)
 Call ID: 8c035602-2077-437b-a932-ae8ba6086ae3
  Args:
    source: :Mathilde_of_Schonburg-Waldenburg
    type: :Woman
  AddTriple (2b170c6c-92b1-464a-9216-0aeae90922b3)
 Call ID: 2b170c6c-92b1-464a-9216-0aeae90922b3
  Args:
    source: :Marie_of_Schwarzburg-Rudolstadt
    relation: :hasFather
    target: :Adolph_of_Schwarzburg-Rudolstadt
  AddTriple (2c3ee663-ba2f-41b5-b8e8-82e8cccfc135)
 Call ID: 2c3ee663-ba2f-41b5-b8e8-82e8cccfc135
  Args:
    source: :Marie_of_Schwarzburg-Rudolstadt
    target: :Mathilde_of_Schonburg-Waldenburg
    relation: :hasMother
  AssignClass (5db66dce-77c7-4c1e-8a73-8c5cefd0b134)
 Call ID: 5db66dce-77c7-4c1e-8a73-8c5cefd0b134
  Args:
    source: :Elisabeth_Anna_of_Oldenburg
    type: :Woman
  AssignClass (e7fd8fd6-d179-4be5-aa73-9197707ff16f)
 Call ID: e7fd8fd6-d179-4be5-aa73-9197707ff16f
  Args:
    type: :Woman
    source: :Sophia_Charlotte_of_Oldenburg
  AddTriple (72e187e2-f8ae-4779-bee7-69442ce81606)
 Call ID: 72e187e2-f8ae-4779-bee7-69442ce81606
  Args:
    source: :Frederick_Augustus_II_of_Oldenburg
    target: :Elisabeth_Anna_of_Oldenburg
    relation: :hasRelation
  AddTriple (203a5123-fadb-4b43-babe-7c87d58314e6)
 Call ID: 203a5123-fadb-4b43-babe-7c87d58314e6
  Args:
    relation: :hasMother
    target: :Elisabeth_Anna_of_Oldenburg
    source: :Sophia_Charlotte_of_Oldenburg
  AddTriple (f6c8cc10-f0a7-4464-98ef-413a66b8cbca)
 Call ID: f6c8cc10-f0a7-4464-98ef-413a66b8cbca
  Args:
    source: :Sophia_Charlotte_of_Oldenburg
    relation: :hasFather
    target: :Frederick_Augustus_II_of_Oldenburg
  AddLiteral (8c7c5e47-71f9-4570-955c-f869eedbd6a8)
 Call ID: 8c7c5e47-71f9-4570-955c-f869eedbd6a8
  Args:
    literal_value: 1931
    source: :Frederick_Augustus_II_of_Oldenburg
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (5eec238c-d686-4dcf-82f1-d5ed09b29917)
 Call ID: 5eec238c-d686-4dcf-82f1-d5ed09b29917
  Args: