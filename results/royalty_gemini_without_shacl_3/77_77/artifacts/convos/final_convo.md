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
Hilmar Freiherr von dem Bussche-Haddenhausen (31 January 1867 – 19 November 1939) was a German nobleman and a diplomat.
Early life

Hilmar was born in Hanover on 31 January 1867, and belonged to the ancient von dem Bussche noble family which originated from the County of Ravensberg.
He was a son of the deputy chief stable master Julius von dem Bussche-Haddenhausen (1827–1882) and his wife Mathilde von Salviati (1833–1892).
His younger brother, George von dem Bussche-Haddenhausen, was the mother of Baroness Gösta von dem Bussche-Haddenhausen (herself the mother of Prince Claus of the Netherlands, consort of Queen Beatrix of the Netherlands).
Career

In 1894, Bussche-Haddenhausen was appointed to the Foreign Office and began his diplomatic career.
In May 1896, Bussche-Haddenhausen was appointed legation councilor before he was recalled from Tangier in November.
Bussche-Haddenhausen's served in Washington until May 1906, when he returned to the Foreign Office in Berlin in the Politics Department working, primarily, as a department head for English affairs.
He served in that role for four years, until his mission ended shortly before the outbreak of World War I.


Bussche-Haddenhausen took over as acting head of the German embassy in Bucharest on 18 September 1914, again succeeding Julius von Waldthausen, who retired.
In December 1915, Bussche-Haddenhausen was appointed Envoy but had to return to Germany at short notice in the summer of 1916 because of the unexpected break in diplomatic relations with Romania.
In the beginning of the Weimar Republic, Bussche-Haddenhausen withdrew from public life.
Personal life

On 15 August 1899 in Buenos Aires, Bussche-Haddenhausen married María Eleonore Martínez de Hoz (1875–1957), the daughter of Argentinian landowner Narciso Martínez de Hoz, who was from one of the richest families in Argentina, and Mathilde Stegmann.
Together, they had five children, including:


Baron von dem Bussche-Haddenhausen died on 19 November 1939 in Ramos Mejía, Argentina.



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
  AssignClass (089c9334-c19c-44f6-9774-b9bd320cf4f5)
 Call ID: 089c9334-c19c-44f6-9774-b9bd320cf4f5
  Args:
    type: :Man
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddLiteral (ebf76843-d740-4995-8c05-4ec8c3cc4a5b)
 Call ID: ebf76843-d740-4995-8c05-4ec8c3cc4a5b
  Args:
    literal_type: xsd:integer
    literal_value: 1867
    relation: :hasBirthYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddLiteral (71d43a65-25b2-411e-a49a-734ca643a7f9)
 Call ID: 71d43a65-25b2-411e-a49a-734ca643a7f9
  Args:
    literal_value: 1939
    relation: :hasDeathYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AssignClass (649bfcbe-0d41-47f8-ab10-09635d08c183)
 Call ID: 649bfcbe-0d41-47f8-ab10-09635d08c183
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AddLiteral (ad7c3640-aae3-47b8-896e-f7d15fb974c0)
 Call ID: ad7c3640-aae3-47b8-896e-f7d15fb974c0
  Args:
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
    literal_value: 1827
  AddLiteral (2985c4c9-8b36-4557-a788-443a7773b30a)
 Call ID: 2985c4c9-8b36-4557-a788-443a7773b30a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1882
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (039d6ac9-3950-4db4-8506-272531acfe88)
 Call ID: 039d6ac9-3950-4db4-8506-272531acfe88
  Args:
    type: :Woman
    source: Mathilde_von_Salviati
  AddLiteral (bc98edb8-8bdf-48f5-988c-f87e2add6397)
 Call ID: bc98edb8-8bdf-48f5-988c-f87e2add6397
  Args:
    literal_value: 1833
    relation: :hasBirthYear
    source: Mathilde_von_Salviati
    literal_type: xsd:integer
  AddLiteral (fd36d68d-1fe9-4a59-8e7f-219e2724ff0b)
 Call ID: fd36d68d-1fe9-4a59-8e7f-219e2724ff0b
  Args:
    source: Mathilde_von_Salviati
    relation: :hasDeathYear
    literal_value: 1892
    literal_type: xsd:integer
  AddTriple (10e0984d-3d68-4662-abeb-290cedea4106)
 Call ID: 10e0984d-3d68-4662-abeb-290cedea4106
  Args:
    target: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddTriple (fcbac995-301e-4f87-885f-e5a5bf20136d)
 Call ID: fcbac995-301e-4f87-885f-e5a5bf20136d
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    target: Mathilde_von_Salviati
  AssignClass (0b2340e2-d690-495c-8485-c78e2201cbfa)
 Call ID: 0b2340e2-d690-495c-8485-c78e2201cbfa
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AddTriple (ab2fe397-a266-48f7-90bd-201c7a74f854)
 Call ID: ab2fe397-a266-48f7-90bd-201c7a74f854
  Args:
    target: George_von_dem_Bussche-Haddenhausen
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :isSiblingOf
  AssignClass (a406f770-2ab2-4e37-aab3-d1a52f1f6d4e)
 Call ID: a406f770-2ab2-4e37-aab3-d1a52f1f6d4e
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AddTriple (6c83eca4-ec14-42dd-b303-202f4fed0192)
 Call ID: 6c83eca4-ec14-42dd-b303-202f4fed0192
  Args:
    target: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    source: George_von_dem_Bussche-Haddenhausen
    relation: :isMotherOf
  AssignClass (bbe92b60-75c9-41ee-b72b-8195bc380a81)
 Call ID: bbe92b60-75c9-41ee-b72b-8195bc380a81
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AddTriple (b63f8e6e-c952-4d27-89b7-cfc93cae43ba)
 Call ID: b63f8e6e-c952-4d27-89b7-cfc93cae43ba
  Args:
    target: Prince_Claus_of_the_Netherlands
    relation: :isMotherOf
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (d835e8e8-159a-455b-a789-df438e62ade2)
 Call ID: d835e8e8-159a-455b-a789-df438e62ade2
  Args:
    type: :Woman
    source: María_Eleonore_Martínez_de_Hoz
  AddLiteral (4d18ea89-1a38-40b2-93bb-8bc3d8e96f9b)
 Call ID: 4d18ea89-1a38-40b2-93bb-8bc3d8e96f9b
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasBirthYear
    literal_value: 1875
    literal_type: xsd:integer
  AddLiteral (cd926580-c220-4015-83d9-63cd2936acf3)
 Call ID: cd926580-c220-4015-83d9-63cd2936acf3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1957
    source: María_Eleonore_Martínez_de_Hoz
  AddTriple (e4a2321d-b4ca-4fc9-9c66-bdcd0eed5ffa)
 Call ID: e4a2321d-b4ca-4fc9-9c66-bdcd0eed5ffa
  Args:
    target: María_Eleonore_Martínez_de_Hoz
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
  AddLiteral (7f45b5c0-3e58-4f63-8080-f51014f5bfd7)
 Call ID: 7f45b5c0-3e58-4f63-8080-f51014f5bfd7
  Args:
    literal_type: xsd:integer
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
    literal_value: 1899
  AssignClass (e56fbe93-1129-4170-ad53-efa1d5f5a6e3)
 Call ID: e56fbe93-1129-4170-ad53-efa1d5f5a6e3
  Args:
    source: Narciso_Martínez_de_Hoz
    type: :Man
  AssignClass (a57af8c4-1749-4ac5-a93f-bfc8e59feb8a)
 Call ID: a57af8c4-1749-4ac5-a93f-bfc8e59feb8a
  Args:
    type: :Woman
    source: Mathilde_Stegmann
  AddTriple (6d06576d-9012-4e26-851b-de5db3db6a4b)
 Call ID: 6d06576d-9012-4e26-851b-de5db3db6a4b
  Args:
    target: Narciso_Martínez_de_Hoz
    relation: :hasFather
    source: María_Eleonore_Martínez_de_Hoz
  AddTriple (a2631db0-c800-43ed-8620-1b8c836be84b)
 Call ID: a2631db0-c800-43ed-8620-1b8c836be84b
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasMother
    target: Mathilde_Stegmann
  Finish (b72d91ff-382a-482b-99b0-2a7676d2c346)
 Call ID: b72d91ff-382a-482b-99b0-2a7676d2c346
  Args: