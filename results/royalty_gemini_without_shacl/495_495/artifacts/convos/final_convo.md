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
  AssignClass (0472ed8f-8330-46ee-b26a-4f6ab351f2a8)
 Call ID: 0472ed8f-8330-46ee-b26a-4f6ab351f2a8
  Args:
    source: :Woizlawa_Feodora_Princess_Reuss
    type: :Woman
  AddLiteral (868caefc-8a1d-4ebb-a704-77c1dff7bef4)
 Call ID: 868caefc-8a1d-4ebb-a704-77c1dff7bef4
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Woizlawa_Feodora_Princess_Reuss
    literal_value: 1918
  AddLiteral (9904e05a-abfe-4e69-bbc4-961fbb9a6853)
 Call ID: 9904e05a-abfe-4e69-bbc4-961fbb9a6853
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Woizlawa_Feodora_Princess_Reuss
    literal_value: 2019
  AssignClass (370ba2da-3067-449d-83b9-30e7ade5cc42)
 Call ID: 370ba2da-3067-449d-83b9-30e7ade5cc42
  Args:
    type: :Man
    source: :Frederick_Francis_II
  AddLiteral (80fbdeb9-c24e-4233-aa88-2b5a9001609c)
 Call ID: 80fbdeb9-c24e-4233-aa88-2b5a9001609c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1823
    source: :Frederick_Francis_II
  AddLiteral (e00e7dcd-8e96-4dfe-8c88-9a9e37679846)
 Call ID: e00e7dcd-8e96-4dfe-8c88-9a9e37679846
  Args:
    source: :Frederick_Francis_II
    literal_value: 1883
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (33231689-0ec6-4710-8932-b3a6b582334b)
 Call ID: 33231689-0ec6-4710-8932-b3a6b582334b
  Args:
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
    type: :Woman
  AddLiteral (73e0af38-86b6-4763-8a8d-4adc3a6492f0)
 Call ID: 73e0af38-86b6-4763-8a8d-4adc3a6492f0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1850
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
  AddLiteral (d9816ff1-8dcc-46f5-ac66-d26dd0d6fe0e)
 Call ID: d9816ff1-8dcc-46f5-ac66-d26dd0d6fe0e
  Args:
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (307317ce-f8ee-4674-9802-eb0397754b65)
 Call ID: 307317ce-f8ee-4674-9802-eb0397754b65
  Args:
    target: :Woizlawa_Father
    source: :Woizlawa_Feodora_Princess_Reuss
    relation: :hasFather
  AssignClass (b69032a3-2e58-4da0-8c51-508f42a47e87)
 Call ID: b69032a3-2e58-4da0-8c51-508f42a47e87
  Args:
    type: :Man
    source: :Woizlawa_Father
  AddTriple (19b8d66c-be01-41b8-9ac8-b6d35b5af1ec)
 Call ID: 19b8d66c-be01-41b8-9ac8-b6d35b5af1ec
  Args:
    relation: :isFatherOf
    target: :Woizlawa_Father
    source: :Frederick_Francis_II
  AddTriple (016c511c-96fe-4251-b707-b0bb4a2087a2)
 Call ID: 016c511c-96fe-4251-b707-b0bb4a2087a2
  Args:
    relation: :isMotherOf
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
    target: :Woizlawa_Father
  AssignClass (8cb65948-d62c-485a-b91b-023901b92539)
 Call ID: 8cb65948-d62c-485a-b91b-023901b92539
  Args:
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
    type: :Woman
  AddLiteral (b3bef963-7cfd-404f-bc12-925f245fbefb)
 Call ID: b3bef963-7cfd-404f-bc12-925f245fbefb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
    literal_value: 1889
  AddLiteral (26e8f880-ed67-4f0c-85ea-e788296da0fa)
 Call ID: 26e8f880-ed67-4f0c-85ea-e788296da0fa
  Args:
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
    literal_value: 1918
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (ac809bda-1a7a-4b99-954b-a4ad16a5a141)
 Call ID: ac809bda-1a7a-4b99-954b-a4ad16a5a141
  Args:
    source: :Woizlawa_Feodora_Princess_Reuss
    target: :Viktoria_Feodora_Reuss_zu_Schleiz
    relation: :hasMother
  AssignClass (76e8fc95-5622-453d-8ba4-654977b6bee7)
 Call ID: 76e8fc95-5622-453d-8ba4-654977b6bee7
  Args:
    source: :Heinrich_XXVII_Prince_of_Reuss_zu_Schleiz
    type: :Man
  AssignClass (53891ece-8144-4f71-9201-96b541f25a84)
 Call ID: 53891ece-8144-4f71-9201-96b541f25a84
  Args:
    source: :Princess_Elise_of_Hohenlohe-Langenburg
    type: :Woman
  AddTriple (908815b3-8b90-4a0c-8a87-ab88a98d13c0)
 Call ID: 908815b3-8b90-4a0c-8a87-ab88a98d13c0
  Args:
    relation: :hasFather
    target: :Heinrich_XXVII_Prince_of_Reuss_zu_Schleiz
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
  AddTriple (0f93e5f4-439d-4733-b5b5-83232e9ef318)
 Call ID: 0f93e5f4-439d-4733-b5b5-83232e9ef318
  Args:
    relation: :hasMother
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
    target: :Princess_Elise_of_Hohenlohe-Langenburg
  AssignClass (62ad7717-6edf-44a1-8196-850f65dfc1d1)
 Call ID: 62ad7717-6edf-44a1-8196-850f65dfc1d1
  Args:
    type: :Woman
    source: :Princess_Feodora_of_Leiningen
  AddTriple (2f2f0071-c455-477f-8526-0f40e6c15710)
 Call ID: 2f2f0071-c455-477f-8526-0f40e6c15710
  Args:
    source: :Princess_Elise_of_Hohenlohe-Langenburg
    target: :Princess_Feodora_of_Leiningen
    relation: :hasMother
  AssignClass (3b0706df-4c7c-40a1-9c78-c6936e7a7814)
 Call ID: 3b0706df-4c7c-40a1-9c78-c6936e7a7814
  Args:
    type: :Man
    source: :Heinrich_I_Prinz_Reuss
  AddLiteral (a876b194-71fd-4651-a20e-258250a8dcae)
 Call ID: a876b194-71fd-4651-a20e-258250a8dcae
  Args:
    source: :Heinrich_I_Prinz_Reuss
    literal_value: 1910
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b4e6f06f-11f8-4dca-a953-86021c8d8150)
 Call ID: b4e6f06f-11f8-4dca-a953-86021c8d8150
  Args:
    literal_value: 1982
    source: :Heinrich_I_Prinz_Reuss
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (1837013e-95d7-4e01-8ccc-bec5c40aecfa)
 Call ID: 1837013e-95d7-4e01-8ccc-bec5c40aecfa
  Args:
    relation: :hasMarriageYear
    target: :Heinrich_I_Prinz_Reuss
    source: :Woizlawa_Feodora_Princess_Reuss
  AddLiteral (c2a421a0-3f61-4864-9912-ad2b69647b62)
 Call ID: c2a421a0-3f61-4864-9912-ad2b69647b62
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1939
    source: :Woizlawa_Feodora_Princess_Reuss
  AssignClass (21237523-ad4e-4ae4-9a12-6aec2574d1b3)
 Call ID: 21237523-ad4e-4ae4-9a12-6aec2574d1b3
  Args:
    type: :Man
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
  AddLiteral (bd78f6ce-598d-4954-8788-20607362c507)
 Call ID: bd78f6ce-598d-4954-8788-20607362c507
  Args:
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
    literal_value: 1887
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bea3b9e6-aa3b-4a49-bb1c-457250c4e888)
 Call ID: bea3b9e6-aa3b-4a49-bb1c-457250c4e888
  Args:
    literal_value: 1956
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (0d0733af-b460-4c39-9f01-53c65cf3900f)
 Call ID: 0d0733af-b460-4c39-9f01-53c65cf3900f
  Args:
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
    type: :Woman
  AddLiteral (73adc1ad-4424-4047-8576-8d80ae6c177f)
 Call ID: 73adc1ad-4424-4047-8576-8d80ae6c177f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1884
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
  AddLiteral (1c825278-1f9a-4e94-9a02-01da8332b6a0)
 Call ID: 1c825278-1f9a-4e94-9a02-01da8332b6a0
  Args:
    literal_value: 1968
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (9cfa5712-8ab3-41aa-b967-6fb7166834d2)
 Call ID: 9cfa5712-8ab3-41aa-b967-6fb7166834d2
  Args:
    target: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
    source: :Heinrich_I_Prinz_Reuss
    relation: :hasFather
  AddTriple (39b5d601-e2f9-4b49-9055-c22006d04b03)
 Call ID: 39b5d601-e2f9-4b49-9055-c22006d04b03
  Args:
    relation: :hasMother
    target: :Princess_Sophie_Renata_Reuss_of_Köstritz
    source: :Heinrich_I_Prinz_Reuss
  Finish (bdfdd478-fe64-40b9-98f7-7c6730ab0f27)
 Call ID: bdfdd478-fe64-40b9-98f7-7c6730ab0f27
  Args: