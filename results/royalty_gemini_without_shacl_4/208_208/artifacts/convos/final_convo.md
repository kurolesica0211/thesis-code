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
Princess Isabelle Françoise Hélène Marie d'Orléans (27 November 1900, Le Nouvion-en-Thiérache, France – 12 February 1983, Neuilly-sur-Seine, France) was a member of the House of Orléans and, by marriage, a member of the ducal Harcourt family and of the princely House of Murat.
She was one of the four children of Prince Jean, Duke of Guise (1874–1940), who would become the Orleanist pretender to the French throne in 1926, and Princess Isabelle of Orléans.
Marriages

In 1923 the tradition of Orléans princesses marrying only other royalty (since the alleged 1681 wedding of La Grande Mademoiselle) was dispensed with, as nearly all of her relatives attended Isabelle's wedding at Amélie of Orléans château in Le Chesnay on 12 September to Count Bruno d'Harcourt (1899–1930), son of Count Eugène d'Harcourt and Armande de Pierre de Bernis.
An automobile racer, Harcourt was killed during practice for the Moroccan Grand Prix, leaving his wife with four children:


As a widow, Isabelle remarried the Bonapartist Prince Pierre Murat (1900–1948) in 1934, at Jouy-en-Josas, "upon renunciation of the rank and prerogatives appertaining to princesses of the House of France".
Prince Murat was a  great-grandson of Prince Lucien Murat.
In 1940, as World War II began and when her father died, Isabelle again took refuge at the family estate, Larache, in Morocco, where she shared quarters with her mother, and her elder sister the widowed Princess Françoise of Greece, along with her brother Henri, Count of Paris and the latter's son, Prince Michel d'Orléans.Isabella often visited her parents in Morocco, Belgium and France, especially during World 
War II.
In 1953, her younger sister,Princess Françoise, widow of Prince Christopher of Greece, died in her Paris home after a long period of depression.
Princess Isabella herself died in 1983 and is buried in the Montparnasse Cemetery in Paris.



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
  AssignClass (c2bbb261-f021-4f00-8343-cf4a6778021d)
 Call ID: c2bbb261-f021-4f00-8343-cf4a6778021d
  Args:
    type: :Woman
    source: Princess_Isabelle_dOrleans
  AssignClass (dba92191-e9bf-4326-bc59-ef098f561037)
 Call ID: dba92191-e9bf-4326-bc59-ef098f561037
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (99f9068c-f53a-4bb0-8885-07fcd10e4c2c)
 Call ID: 99f9068c-f53a-4bb0-8885-07fcd10e4c2c
  Args:
    source: Princess_Isabelle_of_Orleans_Mother
    type: :Woman
  AssignClass (6d199754-fcbb-4ecb-bfad-ac7c3743a775)
 Call ID: 6d199754-fcbb-4ecb-bfad-ac7c3743a775
  Args:
    type: :Man
    source: Count_Bruno_dHarcourt
  AssignClass (ab046527-cdf9-47a4-8a57-0cb98ac96c68)
 Call ID: ab046527-cdf9-47a4-8a57-0cb98ac96c68
  Args:
    source: Count_Eugene_dHarcourt
    type: :Man
  AssignClass (6cc3a302-6424-47a2-8098-bcacc37b0879)
 Call ID: 6cc3a302-6424-47a2-8098-bcacc37b0879
  Args:
    type: :Woman
    source: Armande_de_Pierre_de_Bernis
  AssignClass (7ce23a25-8b4c-445b-aba7-24606b68f22b)
 Call ID: 7ce23a25-8b4c-445b-aba7-24606b68f22b
  Args:
    type: :Man
    source: Prince_Pierre_Murat
  AssignClass (bfbde2b4-79d4-4a8e-9f7b-5025cd320deb)
 Call ID: bfbde2b4-79d4-4a8e-9f7b-5025cd320deb
  Args:
    source: Prince_Lucien_Murat
    type: :Man
  AssignClass (e0c50e2d-1e0a-42b6-a554-6a6a35a843ac)
 Call ID: e0c50e2d-1e0a-42b6-a554-6a6a35a843ac
  Args:
    source: Princess_Francoise_of_Greece
    type: :Woman
  AssignClass (3830487e-dc1d-4a16-9a27-dda53bb986c8)
 Call ID: 3830487e-dc1d-4a16-9a27-dda53bb986c8
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (53d0081d-cf37-4043-83a4-a6d2f1b74587)
 Call ID: 53d0081d-cf37-4043-83a4-a6d2f1b74587
  Args:
    source: Prince_Michel_dOrleans
    type: :Man
  AssignClass (596c3a43-59ab-4261-9fa9-73ed877ab532)
 Call ID: 596c3a43-59ab-4261-9fa9-73ed877ab532
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece
  AddLiteral (8310135f-c67d-4ea4-a5c7-ea969fe4eeea)
 Call ID: 8310135f-c67d-4ea4-a5c7-ea969fe4eeea
  Args:
    relation: :hasBirthYear
    literal_value: 1900
    source: Princess_Isabelle_dOrleans
    literal_type: xsd:integer
  AddLiteral (5a7d3ab3-cf3d-4fa3-aa05-02263f9734c3)
 Call ID: 5a7d3ab3-cf3d-4fa3-aa05-02263f9734c3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Isabelle_dOrleans
    literal_value: 1983
  AddLiteral (91236696-7e4a-4985-bcdc-87db5ba64a91)
 Call ID: 91236696-7e4a-4985-bcdc-87db5ba64a91
  Args:
    source: Prince_Jean_Duke_of_Guise
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7f73353b-9103-489d-9670-f0b89c3a8cce)
 Call ID: 7f73353b-9103-489d-9670-f0b89c3a8cce
  Args:
    source: Prince_Jean_Duke_of_Guise
    literal_value: 1940
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (202da322-ec89-48cf-ad3e-a8d006859e6c)
 Call ID: 202da322-ec89-48cf-ad3e-a8d006859e6c
  Args:
    literal_type: xsd:integer
    literal_value: 1899
    source: Count_Bruno_dHarcourt
    relation: :hasBirthYear
  AddLiteral (4272e579-0a3c-4d53-8db8-4ee603e7ede2)
 Call ID: 4272e579-0a3c-4d53-8db8-4ee603e7ede2
  Args:
    source: Count_Bruno_dHarcourt
    literal_value: 1930
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (659e213d-b38d-4f81-a55e-8b54f95aa68d)
 Call ID: 659e213d-b38d-4f81-a55e-8b54f95aa68d
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess_Isabelle_dOrleans
    literal_value: 1923
  AddLiteral (bba6e378-6f47-4fa3-9fe7-e6c3b9bb5026)
 Call ID: bba6e378-6f47-4fa3-9fe7-e6c3b9bb5026
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Pierre_Murat
    literal_value: 1900
  AddLiteral (3f401a7d-5bbf-4dd4-9272-40e14cf73bab)
 Call ID: 3f401a7d-5bbf-4dd4-9272-40e14cf73bab
  Args:
    literal_type: xsd:integer
    source: Prince_Pierre_Murat
    literal_value: 1948
    relation: :hasDeathYear
  AddLiteral (25ee61b8-2aa5-4c07-962b-3b5a8267929c)
 Call ID: 25ee61b8-2aa5-4c07-962b-3b5a8267929c
  Args:
    literal_value: 1934
    source: Princess_Isabelle_dOrleans
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (fa726aab-7bdb-421a-af00-984010de10ef)
 Call ID: fa726aab-7bdb-421a-af00-984010de10ef
  Args:
    source: Princess_Isabelle_dOrleans
    relation: :hasFather
    target: Prince_Jean_Duke_of_Guise
  AddTriple (c0a5e43c-6651-45f6-9873-c910d52382e2)
 Call ID: c0a5e43c-6651-45f6-9873-c910d52382e2
  Args:
    source: Princess_Isabelle_dOrleans
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans_Mother
  AddTriple (71053f3e-28cf-47c2-957c-ff2023b2c2db)
 Call ID: 71053f3e-28cf-47c2-957c-ff2023b2c2db
  Args:
    relation: :hasFather
    source: Count_Bruno_dHarcourt
    target: Count_Eugene_dHarcourt
  AddTriple (285b8229-cea9-44d3-9590-d9a81a561e47)
 Call ID: 285b8229-cea9-44d3-9590-d9a81a561e47
  Args:
    relation: :hasMother
    source: Count_Bruno_dHarcourt
    target: Armande_de_Pierre_de_Bernis
  AddTriple (f1f4dbe1-f0b7-43ef-8934-6f866f69f189)
 Call ID: f1f4dbe1-f0b7-43ef-8934-6f866f69f189
  Args:
    source: Prince_Pierre_Murat
    relation: :hasFather
    target: Prince_Lucien_Murat
  AddTriple (d42a7ca6-7f46-4b35-83c9-03288f3eda63)
 Call ID: d42a7ca6-7f46-4b35-83c9-03288f3eda63
  Args:
    relation: :hasSister
    source: Princess_Isabelle_dOrleans
    target: Princess_Francoise_of_Greece
  AddTriple (543cdd0c-b7b4-443e-9e28-2beb4725094a)
 Call ID: 543cdd0c-b7b4-443e-9e28-2beb4725094a
  Args:
    source: Princess_Isabelle_dOrleans
    relation: :hasBrother
    target: Henri_Count_of_Paris
  AddTriple (ffbcc1cc-7edb-4a55-9c9a-9eba1b82d661)
 Call ID: ffbcc1cc-7edb-4a55-9c9a-9eba1b82d661
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Prince_Michel_dOrleans
  AddTriple (c6eeae51-bc04-4568-87a3-5c6be2add3cd)
 Call ID: c6eeae51-bc04-4568-87a3-5c6be2add3cd
  Args:
    source: Princess_Francoise_of_Greece
    relation: :hasFather
    target: Prince_Christopher_of_Greece
  Finish (7ccd2020-2ee4-4159-b83f-dd67f237d75a)
 Call ID: 7ccd2020-2ee4-4159-b83f-dd67f237d75a
  Args: