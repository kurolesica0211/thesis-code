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
  AssignClass (998c54ee-acf1-4e7b-b970-b4d771ef5a6b)
 Call ID: 998c54ee-acf1-4e7b-b970-b4d771ef5a6b
  Args:
    source: Woizlawa Feodora Princess Reuss
    type: :Woman
  AssignClass (d59c521d-9ad7-4343-9689-cf4572985ce8)
 Call ID: d59c521d-9ad7-4343-9689-cf4572985ce8
  Args:
    source: Woizlawa Feodora Princess Reuss
    type: :Person
  AddLiteral (5685a26e-098a-406a-ba8c-074a61c0d2d2)
 Call ID: 5685a26e-098a-406a-ba8c-074a61c0d2d2
  Args:
    literal_value: 1918
    source: Woizlawa Feodora Princess Reuss
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (6b1d1e68-3308-4587-9a56-3ea460b2883f)
 Call ID: 6b1d1e68-3308-4587-9a56-3ea460b2883f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Woizlawa Feodora Princess Reuss
    literal_value: 2019
  AssignClass (6ce41e3c-58b6-4162-9383-becedcc6f5a4)
 Call ID: 6ce41e3c-58b6-4162-9383-becedcc6f5a4
  Args:
    type: :Man
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
  AssignClass (68aa913c-625b-47ce-952d-514977522cf6)
 Call ID: 68aa913c-625b-47ce-952d-514977522cf6
  Args:
    type: :Person
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
  AddLiteral (e43a0b09-6a13-4a6b-868c-37ecbf6d300d)
 Call ID: e43a0b09-6a13-4a6b-868c-37ecbf6d300d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
    literal_value: 1823
  AddLiteral (5c469de1-6ebd-4fab-bd6b-d953fab6e806)
 Call ID: 5c469de1-6ebd-4fab-bd6b-d953fab6e806
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Frederick Francis II, Grand Duke of Mecklenburg-Schwerin
    literal_value: 1883
  AssignClass (80e3c18f-a4ec-4472-947a-f62646eb1871)
 Call ID: 80e3c18f-a4ec-4472-947a-f62646eb1871
  Args:
    type: :Woman
    source: Princess Marie of Schwarzburg-Rudolstadt
  AssignClass (84c45c51-e19f-4dc9-98dc-b7ed9cdb7a82)
 Call ID: 84c45c51-e19f-4dc9-98dc-b7ed9cdb7a82
  Args:
    type: :Person
    source: Princess Marie of Schwarzburg-Rudolstadt
  AddLiteral (147137f3-c3b1-43a5-af2d-109189e266fb)
 Call ID: 147137f3-c3b1-43a5-af2d-109189e266fb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Princess Marie of Schwarzburg-Rudolstadt
    literal_value: 1850
  AddLiteral (fc2d9f66-b529-4ba0-a783-731b617dae88)
 Call ID: fc2d9f66-b529-4ba0-a783-731b617dae88
  Args:
    source: Princess Marie of Schwarzburg-Rudolstadt
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1922
  AssignClass (e4b37e07-68b2-4317-904a-6d19923b5883)
 Call ID: e4b37e07-68b2-4317-904a-6d19923b5883
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    type: :Woman
  AssignClass (82b31954-c084-43dd-81e3-df94174c1068)
 Call ID: 82b31954-c084-43dd-81e3-df94174c1068
  Args:
    type: :Person
    source: Viktoria Feodora Reuss zu Schleiz
  AddLiteral (7b1050b0-78de-4b91-886f-c7f02ed9c4e3)
 Call ID: 7b1050b0-78de-4b91-886f-c7f02ed9c4e3
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1889
  AddLiteral (4330cac2-fe4a-43cf-92e9-1bdb45066530)
 Call ID: 4330cac2-fe4a-43cf-92e9-1bdb45066530
  Args:
    literal_value: 1918
    source: Viktoria Feodora Reuss zu Schleiz
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (f1958913-a6a7-41a5-aba1-01d788b3e0dc)
 Call ID: f1958913-a6a7-41a5-aba1-01d788b3e0dc
  Args:
    source: Heinrich XXVII, Prince of Reuss zu Schleiz
    type: :Man
  AssignClass (eed89194-f99e-488d-9194-b45b37a3b1ea)
 Call ID: eed89194-f99e-488d-9194-b45b37a3b1ea
  Args:
    type: :Person
    source: Heinrich XXVII, Prince of Reuss zu Schleiz
  AssignClass (8ea3f206-ad23-4744-b6d3-0955e34a0047)
 Call ID: 8ea3f206-ad23-4744-b6d3-0955e34a0047
  Args:
    source: Princess Elise of Hohenlohe-Langenburg
    type: :Woman
  AssignClass (b6716c14-f957-4a7e-ac93-731effb5d16d)
 Call ID: b6716c14-f957-4a7e-ac93-731effb5d16d
  Args:
    source: Princess Elise of Hohenlohe-Langenburg
    type: :Person
  AssignClass (db65a1fa-f8e2-42c1-bef4-72d8d2807e0d)
 Call ID: db65a1fa-f8e2-42c1-bef4-72d8d2807e0d
  Args:
    source: Princess Feodora of Leiningen
    type: :Woman
  AssignClass (d3d74e99-6f73-440b-b9de-88abfd510d08)
 Call ID: d3d74e99-6f73-440b-b9de-88abfd510d08
  Args:
    source: Princess Feodora of Leiningen
    type: :Person
  AssignClass (bab79873-7529-45d7-8c6b-a3e6a7ada551)
 Call ID: bab79873-7529-45d7-8c6b-a3e6a7ada551
  Args:
    type: :Woman
    source: Queen Victoria
  AssignClass (a62daed9-ca9e-4ebb-afb5-0650ca2d1e26)
 Call ID: a62daed9-ca9e-4ebb-afb5-0650ca2d1e26
  Args:
    type: :Person
    source: Queen Victoria
  AddTriple (d81e08fd-ae83-49a4-889c-1a7d5d7c4e4d)
 Call ID: d81e08fd-ae83-49a4-889c-1a7d5d7c4e4d
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    relation: :hasFather
    target: Heinrich XXVII, Prince of Reuss zu Schleiz
  AddTriple (471b51f5-e8eb-473a-8b44-7100506fa0cc)
 Call ID: 471b51f5-e8eb-473a-8b44-7100506fa0cc
  Args:
    target: Princess Elise of Hohenlohe-Langenburg
    relation: :hasMother
    source: Viktoria Feodora Reuss zu Schleiz
  AddTriple (1ca23a56-65e6-441b-97bf-6ed0da322825)
 Call ID: 1ca23a56-65e6-441b-97bf-6ed0da322825
  Args:
    source: Princess Elise of Hohenlohe-Langenburg
    target: Viktoria Feodora Reuss zu Schleiz
    relation: :isMotherOf
  AddTriple (86e2124a-df3b-4598-aa94-73ac628bf0c4)
 Call ID: 86e2124a-df3b-4598-aa94-73ac628bf0c4
  Args:
    relation: :isFatherOf
    target: Viktoria Feodora Reuss zu Schleiz
    source: Heinrich XXVII, Prince of Reuss zu Schleiz
  AddTriple (7390e076-32b7-4894-bb4d-3e6a00e8ef4a)
 Call ID: 7390e076-32b7-4894-bb4d-3e6a00e8ef4a
  Args:
    source: Woizlawa Feodora Princess Reuss
    target: Viktoria Feodora Reuss zu Schleiz
    relation: :hasMother
  AddTriple (86493886-8c49-40aa-a093-87f4c9608144)
 Call ID: 86493886-8c49-40aa-a093-87f4c9608144
  Args:
    source: Viktoria Feodora Reuss zu Schleiz
    target: Woizlawa Feodora Princess Reuss
    relation: :isMotherOf
  AddTriple (22cddb3c-7159-4c62-8d42-ad4bfb857e32)
 Call ID: 22cddb3c-7159-4c62-8d42-ad4bfb857e32
  Args:
    relation: :hasMother
    target: Princess Feodora of Leiningen
    source: Princess Elise of Hohenlohe-Langenburg
  AddTriple (de286885-ab79-4058-970f-5ee278fc7bdd)
 Call ID: de286885-ab79-4058-970f-5ee278fc7bdd
  Args:
    source: Princess Feodora of Leiningen
    target: Princess Elise of Hohenlohe-Langenburg
    relation: :isMotherOf
  AddTriple (cd9c24dd-e7fc-49a1-83a2-d46190a47647)
 Call ID: cd9c24dd-e7fc-49a1-83a2-d46190a47647
  Args:
    relation: :hasMother
    target: Princess Feodora of Leiningen
    source: Queen Victoria
  AddTriple (d5c313af-df6e-4963-9d07-b6c55d287a77)
 Call ID: d5c313af-df6e-4963-9d07-b6c55d287a77
  Args:
    source: Princess Feodora of Leiningen
    target: Queen Victoria
    relation: :isMotherOf
  AssignClass (169367bf-b720-489f-8830-fa015dea5a6c)
 Call ID: 169367bf-b720-489f-8830-fa015dea5a6c
  Args:
    source: Heinrich I Prinz Reuss
    type: :Man
  AssignClass (1ce8119c-7edf-4e8f-b0bc-3e8f56d6f3ef)
 Call ID: 1ce8119c-7edf-4e8f-b0bc-3e8f56d6f3ef
  Args:
    source: Heinrich I Prinz Reuss
    type: :Person
  AddLiteral (1edbd5b0-308f-444f-822e-1857c306425b)
 Call ID: 1edbd5b0-308f-444f-822e-1857c306425b
  Args:
    source: Heinrich I Prinz Reuss
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1910
  AddLiteral (493d59bc-c789-485e-8060-57c8157e27eb)
 Call ID: 493d59bc-c789-485e-8060-57c8157e27eb
  Args:
    literal_value: 1982
    source: Heinrich I Prinz Reuss
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (f3bb52d1-5094-493a-a54d-eabdaf51e7cf)
 Call ID: f3bb52d1-5094-493a-a54d-eabdaf51e7cf
  Args:
    target: Heinrich I Prinz Reuss
    relation: :hasMarriageYear
    source: Woizlawa Feodora Princess Reuss
  AddLiteral (ffa31bb2-3318-4ca7-b471-f1aee60f63cd)
 Call ID: ffa31bb2-3318-4ca7-b471-f1aee60f63cd
  Args:
    source: Woizlawa Feodora Princess Reuss
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1939
  AssignClass (988d5d99-cf7d-46fb-86e1-dd63dac06860)
 Call ID: 988d5d99-cf7d-46fb-86e1-dd63dac06860
  Args:
    source: Prince Heinrich XXXIV Reuss of Schleiz
    type: :Man
  AssignClass (318f235c-d22e-40da-a3d7-8481809963b8)
 Call ID: 318f235c-d22e-40da-a3d7-8481809963b8
  Args:
    type: :Person
    source: Prince Heinrich XXXIV Reuss of Schleiz
  AddLiteral (72d12281-ba38-4f0c-ad09-5f5db31bc7f3)
 Call ID: 72d12281-ba38-4f0c-ad09-5f5db31bc7f3
  Args:
    literal_value: 1887
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince Heinrich XXXIV Reuss of Schleiz
  AddLiteral (166db1ca-d769-40ba-8c73-5ce7b5646d9a)
 Call ID: 166db1ca-d769-40ba-8c73-5ce7b5646d9a
  Args:
    source: Prince Heinrich XXXIV Reuss of Schleiz
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1956
  AssignClass (6661dac4-508f-4df1-b9c5-3ef576114e4c)
 Call ID: 6661dac4-508f-4df1-b9c5-3ef576114e4c
  Args:
    type: :Woman
    source: Princess Sophie Renata Reuss of Köstritz
  AssignClass (b3673766-d080-4306-b9db-8ae6d91e06de)
 Call ID: b3673766-d080-4306-b9db-8ae6d91e06de
  Args:
    type: :Person
    source: Princess Sophie Renata Reuss of Köstritz
  AddLiteral (5431a0de-cef5-4eaa-8df2-6966426a57a3)
 Call ID: 5431a0de-cef5-4eaa-8df2-6966426a57a3
  Args:
    literal_value: 1884
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess Sophie Renata Reuss of Köstritz
  AddLiteral (2b0d3e3e-6c95-4b60-883b-37299375b6a1)
 Call ID: 2b0d3e3e-6c95-4b60-883b-37299375b6a1
  Args:
    source: Princess Sophie Renata Reuss of Köstritz
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1968
  AddTriple (4dd4ddc1-1bd9-4f32-916d-0cebb7250290)
 Call ID: 4dd4ddc1-1bd9-4f32-916d-0cebb7250290
  Args:
    target: Prince Heinrich XXXIV Reuss of Schleiz
    relation: :hasFather
    source: Heinrich I Prinz Reuss
  AddTriple (b31b50be-5666-4444-9882-01af6afaac6e)
 Call ID: b31b50be-5666-4444-9882-01af6afaac6e
  Args:
    target: Princess Sophie Renata Reuss of Köstritz
    relation: :hasMother
    source: Heinrich I Prinz Reuss
  AddTriple (f90ecbe7-e68b-4813-bb4b-a32ef9191df5)
 Call ID: f90ecbe7-e68b-4813-bb4b-a32ef9191df5
  Args:
    relation: :isFatherOf
    target: Heinrich I Prinz Reuss
    source: Prince Heinrich XXXIV Reuss of Schleiz
  AddTriple (42db06b1-aa24-42ff-acbc-759622acee2c)
 Call ID: 42db06b1-aa24-42ff-acbc-759622acee2c
  Args:
    target: Heinrich I Prinz Reuss
    relation: :isMotherOf
    source: Princess Sophie Renata Reuss of Köstritz
  Finish (7444f7ae-d640-4adb-88c8-93b3d550c53e)
 Call ID: 7444f7ae-d640-4adb-88c8-93b3d550c53e
  Args: