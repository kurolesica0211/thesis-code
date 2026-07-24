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
Woizlawa Feodora Princess Reuss (née Duchess of Mecklenburg-Schwerin, 17 December 1918 – 3 June 2019) was a member of the German nobility, by birth of the House of Mecklenburg-Schwerin.
Her father was the seventh son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin (1823–1883) by his third wife Princess Marie of Schwarzburg-Rudolstadt (1850–1922).
Her mother was Viktoria Feodora Reuss zu Schleiz (1889–1918), the eldest child of Heinrich XXVII, Prince of Reuss zu Schleiz, regent of Principality of Reuss-Greiz and Princess Elise of Hohenlohe-Langenburg, granddaughter of Princess Feodora of Leiningen, half-sister of Queen Victoria.
She was a first cousin of:


Juliana's wedding

Preparations for the wedding of Queen Wilhelmina of the Netherlands' only child Crown Princess Juliana to the German Prince Bernhard of Lippe-Biesterfeld were underway in 1937 when a diplomatic scandal occurred.
These included Woizlawa herself (being first cousins), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Princess Sophie of Saxe-Weimar-Eisenach (her second cousin), and two of Bernhard's first cousins, Princess Sieglinde and Princess Elisabeth of Lippe.
Marriage and family

On 15 September 1939, she married in Bad Doberan to her distant relative Heinrich I Prinz Reuss (1910−1982), the eldest son of Prince Heinrich XXXIV Reuss of Schleiz (1887-1956) and his wife and cousin, Princess Sophie Renata Reuss of Köstritz (1884-1968).



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
  AssignClass (5238fee3-a6b2-4a07-afea-9dcd88ed074a)
 Call ID: 5238fee3-a6b2-4a07-afea-9dcd88ed074a
  Args:
    type: :Woman
    source: Woizlawa Feodora Princess Reuss
  AddLiteral (7664604d-5d35-46fd-b0dd-b596a13f45c3)
 Call ID: 7664604d-5d35-46fd-b0dd-b596a13f45c3
  Args:
    literal_type: xsd:integer
    source: Woizlawa Feodora Princess Reuss
    literal_value: 1918
    relation: :hasBirthYear
  AddLiteral (fee9bf26-12cd-4fb2-8629-d70f06f549ba)
 Call ID: fee9bf26-12cd-4fb2-8629-d70f06f549ba
  Args:
    literal_type: xsd:integer
    source: Woizlawa Feodora Princess Reuss
    relation: :hasDeathYear
    literal_value: 2019
  AssignClass (57260069-e77d-448f-b502-76e449005603)
 Call ID: 57260069-e77d-448f-b502-76e449005603
  Args:
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
    type: :Man
  AddLiteral (67cd8134-4866-4867-a146-e4015242a801)
 Call ID: 67cd8134-4866-4867-a146-e4015242a801
  Args:
    literal_value: 1823
    relation: :hasBirthYear
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddLiteral (1d600ebd-472f-4a5f-b6db-48b4f8147692)
 Call ID: 1d600ebd-472f-4a5f-b6db-48b4f8147692
  Args:
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasDeathYear
  AssignClass (fcfbbaaf-5cdc-4bd9-8291-05500b319e96)
 Call ID: fcfbbaaf-5cdc-4bd9-8291-05500b319e96
  Args:
    source: Princess Marie of Schwarzburg-Rudolstadt
    type: :Woman
  AddLiteral (af93660a-4c6a-422e-973c-3658d66a5245)
 Call ID: af93660a-4c6a-422e-973c-3658d66a5245
  Args:
    source: Princess Marie of Schwarzburg-Rudolstadt
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1850
  AddLiteral (7aeea609-bd77-4205-b43a-166b3993896b)
 Call ID: 7aeea609-bd77-4205-b43a-166b3993896b
  Args:
    source: Princess Marie of Schwarzburg-Rudolstadt
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1922
  AssignClass (0dc975f0-9a7b-44ee-8e31-5ff6c6f11f7c)
 Call ID: 0dc975f0-9a7b-44ee-8e31-5ff6c6f11f7c
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    type: :Woman
  AddLiteral (09ed9dac-53ff-4126-97b2-829e94d15775)
 Call ID: 09ed9dac-53ff-4126-97b2-829e94d15775
  Args:
    relation: :hasBirthYear
    literal_value: 1889
    literal_type: xsd:integer
    source: Viktoria Feodora Reuss zu Schleiz
  AddLiteral (ff5a685b-986a-4392-8745-cbb185b82342)
 Call ID: ff5a685b-986a-4392-8745-cbb185b82342
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    literal_type: xsd:integer
    literal_value: 1918
    relation: :hasDeathYear
  AssignClass (5a1b5dbe-35e4-442b-a6ec-e57d9d826e3c)
 Call ID: 5a1b5dbe-35e4-442b-a6ec-e57d9d826e3c
  Args:
    source: Heinrich XXVII, Prince of Reuss zu Schleiz
    type: :Man
  AssignClass (11f79d9f-e91f-462a-92cd-a23b45127870)
 Call ID: 11f79d9f-e91f-462a-92cd-a23b45127870
  Args:
    source: Princess Elise of Hohenlohe-Langenburg
    type: :Woman
  AssignClass (094eb140-a0be-47d7-a72e-61650d97c6ae)
 Call ID: 094eb140-a0be-47d7-a72e-61650d97c6ae
  Args:
    type: :Woman
    source: Princess Feodora of Leiningen
  AssignClass (4487a152-9302-4dc0-be19-e6ff3cda39b1)
 Call ID: 4487a152-9302-4dc0-be19-e6ff3cda39b1
  Args:
    source: Queen Victoria
    type: :Woman
  AssignClass (edf8850a-fd6b-468f-b325-bc3919609266)
 Call ID: edf8850a-fd6b-468f-b325-bc3919609266
  Args:
    source: Queen Wilhelmina of the Netherlands
    type: :Woman
  AssignClass (4ab9f6e1-d6d3-4670-9a42-6adc4bd12d8f)
 Call ID: 4ab9f6e1-d6d3-4670-9a42-6adc4bd12d8f
  Args:
    source: Crown Princess Juliana
    type: :Woman
  AssignClass (9ee0028b-651b-44cb-90ec-16c244c3ee15)
 Call ID: 9ee0028b-651b-44cb-90ec-16c244c3ee15
  Args:
    type: :Man
    source: Prince Bernhard of Lippe-Biesterfeld
  AssignClass (a5923e7e-8c33-4a2a-8392-cad29d884a5a)
 Call ID: a5923e7e-8c33-4a2a-8392-cad29d884a5a
  Args:
    type: :Woman
    source: Duchess Thyra of Mecklenburg-Schwerin
  AssignClass (e338a23f-7a99-4de5-8612-b1fbe2615072)
 Call ID: e338a23f-7a99-4de5-8612-b1fbe2615072
  Args:
    source: Grand Duchess Kira Kirillovna of Russia
    type: :Woman
  AssignClass (f0326909-62af-43c3-bc1d-1fec07771e16)
 Call ID: f0326909-62af-43c3-bc1d-1fec07771e16
  Args:
    type: :Woman
    source: Princess Sophie of Saxe-Weimar-Eisenach
  AssignClass (2388e177-efbb-4603-9db0-f4bd139487a9)
 Call ID: 2388e177-efbb-4603-9db0-f4bd139487a9
  Args:
    type: :Woman
    source: Princess Sieglinde of Lippe
  AssignClass (b3b31a4a-8eae-43ea-8964-6358dc5cc884)
 Call ID: b3b31a4a-8eae-43ea-8964-6358dc5cc884
  Args:
    type: :Woman
    source: Princess Elisabeth of Lippe
  AssignClass (41bfa490-0d66-46ea-9907-19fa165633b7)
 Call ID: 41bfa490-0d66-46ea-9907-19fa165633b7
  Args:
    type: :Man
    source: Heinrich I Prinz Reuss
  AddLiteral (a670f4a6-4f81-41a7-ac19-c22f44bce88f)
 Call ID: a670f4a6-4f81-41a7-ac19-c22f44bce88f
  Args:
    relation: :hasBirthYear
    literal_value: 1910
    source: Heinrich I Prinz Reuss
    literal_type: xsd:integer
  AddLiteral (c89a1053-5df4-4362-8c59-ffaf1bee7405)
 Call ID: c89a1053-5df4-4362-8c59-ffaf1bee7405
  Args:
    literal_type: xsd:integer
    source: Heinrich I Prinz Reuss
    relation: :hasDeathYear
    literal_value: 1982
  AddLiteral (8252d057-e64b-4651-8d7e-7ec4341c72cf)
 Call ID: 8252d057-e64b-4651-8d7e-7ec4341c72cf
  Args:
    literal_type: xsd:integer
    source: Heinrich I Prinz Reuss
    literal_value: 1939
    relation: :hasMarriageYear
  AssignClass (c590a72c-d38f-4828-b793-13eee7c582f3)
 Call ID: c590a72c-d38f-4828-b793-13eee7c582f3
  Args:
    type: :Man
    source: Prince Heinrich XXXIV Reuss of Schleiz
  AddLiteral (265c3600-fb5e-4c91-8b39-3a9c539d5e2c)
 Call ID: 265c3600-fb5e-4c91-8b39-3a9c539d5e2c
  Args:
    relation: :hasBirthYear
    literal_value: 1887
    literal_type: xsd:integer
    source: Prince Heinrich XXXIV Reuss of Schleiz
  AddLiteral (633599c0-ffc7-4ba3-850b-19241ae1cbd9)
 Call ID: 633599c0-ffc7-4ba3-850b-19241ae1cbd9
  Args:
    relation: :hasDeathYear
    literal_value: 1956
    source: Prince Heinrich XXXIV Reuss of Schleiz
    literal_type: xsd:integer
  AssignClass (5aea9f69-01dd-4ab1-b9ce-1bb196db1438)
 Call ID: 5aea9f69-01dd-4ab1-b9ce-1bb196db1438
  Args:
    source: Princess Sophie Renata Reuss of Köstritz
    type: :Woman
  AddLiteral (11404d5c-8a88-4ae8-bb95-ec6a3f39b179)
 Call ID: 11404d5c-8a88-4ae8-bb95-ec6a3f39b179
  Args:
    literal_type: xsd:integer
    source: Princess Sophie Renata Reuss of Köstritz
    relation: :hasBirthYear
    literal_value: 1884
  AddLiteral (8f21998d-1419-4398-9a99-231865c4c0ed)
 Call ID: 8f21998d-1419-4398-9a99-231865c4c0ed
  Args:
    literal_type: xsd:integer
    source: Princess Sophie Renata Reuss of Köstritz
    literal_value: 1968
    relation: :hasDeathYear
  AddTriple (61ee353a-b510-4824-b23e-4ef537de9b55)
 Call ID: 61ee353a-b510-4824-b23e-4ef537de9b55
  Args:
    relation: :hasMother
    target: Viktoria Feodora Reuss zu Schleiz
    source: Woizlawa Feodora Princess Reuss
  AddTriple (ebc060ec-2fa0-46aa-b965-3be3a0c3b31c)
 Call ID: ebc060ec-2fa0-46aa-b965-3be3a0c3b31c
  Args:
    relation: :hasMother
    target: Princess Elise of Hohenlohe-Langenburg
    source: Viktoria Feodora Reuss zu Schleiz
  AddTriple (ce9fb08a-aeb3-4ed9-9bfe-90576ad99ecd)
 Call ID: ce9fb08a-aeb3-4ed9-9bfe-90576ad99ecd
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    relation: :hasFather
    target: Heinrich XXVII, Prince of Reuss zu Schleiz
  AddTriple (248f826e-1f3f-4ed9-a5fd-3ae56246342e)
 Call ID: 248f826e-1f3f-4ed9-a5fd-3ae56246342e
  Args:
    source: Crown Princess Juliana
    relation: :hasMother
    target: Queen Wilhelmina of the Netherlands
  AddTriple (a6123bea-31a9-434b-b32e-4bb9b7abb8c5)
 Call ID: a6123bea-31a9-434b-b32e-4bb9b7abb8c5
  Args:
    relation: :hasFather
    target: Prince Heinrich XXXIV Reuss of Schleiz
    source: Heinrich I Prinz Reuss
  AddTriple (a25c047b-926a-4cb9-82b0-0e55ab82a582)
 Call ID: a25c047b-926a-4cb9-82b0-0e55ab82a582
  Args:
    source: Heinrich I Prinz Reuss
    relation: :hasMother
    target: Princess Sophie Renata Reuss of Köstritz
  Finish (07cd0163-38d6-4505-8230-6c890991a658)
 Call ID: 07cd0163-38d6-4505-8230-6c890991a658
  Args: