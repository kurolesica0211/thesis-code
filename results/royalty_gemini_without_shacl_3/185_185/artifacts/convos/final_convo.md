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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


The Duke of AostaThe Duchess of Aosta


The Dowager Duchess of Aosta


Princess Olga Isabelle of Savoy-Aosta, Duchess of Aosta (née Princess Olga of Greece;
Greek: Πριγκίπισσα Όλγα της Ελλάδας; born 11 November 1971), is the younger daughter of author Prince Michael of Greece and Denmark and Marina Karella, an artist and daughter of the Greek business magnate Theódoros Karéllas.
Olga is married to her second cousin Prince Aimone, Duke of Aosta.
Early life

Princess Olga was born on 11 November 1971 in Athens, Greece.
She is the younger sister of Princess Alexandra and grew up in Paris and New York, spending summers at the family's island retreat at Patmos, Greece.
Although Olga worked for a while in interior decoration, she went to Panama to photograph and study phalaena.
As Princess Olga's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, used the style Her Highness instead of Her Royal Highness (until her marriage), and is excluded from the line of succession to the former Greek throne.
Engagement, marriage and children

Olga's engagement to Prince Aimone of Savoy, son of Amedeo, 5th Duke of Aosta, was announced in May 2005.
Aimone and Olga are second cousins; both being great-grandchildren of the French pretender Jean d'Orléans, duc de Guise.
They are also second cousins once removed as George I of Greece is Aimone's great-great-grandfather and Olga's great-grandfather.
Olga's father, Prince Michael of Greece and Denmark, Aimone's paternal grandmother, Princess Irene, Duchess of Aosta (née Princess Irene of Greece and Denmark), and Prince Philip, Duke of Edinburgh (born Prince Philip of Greece and Denmark), were all first cousins.
A canonical dispensation was obtained from the Catholic Archbishop of Moscow, Monsignor Paolo Pezzi, who was the local Ordinary of prince Aimone.
On 7 March 2009, Princess Olga gave birth to a son named Umberto in Paris, France.
On 24 May 2011 in Paris, Olga gave birth to another son, named Amedeo Michele.
On 14 December 2012, Olga gave birth to a baby daughter, Isabella Vita Marina, in Paris, France.



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
  AssignClass (294a3bc9-1de2-456b-a1f0-c4b319dde333)
 Call ID: 294a3bc9-1de2-456b-a1f0-c4b319dde333
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AssignClass (c5813894-a302-4ac9-8e06-10847687656e)
 Call ID: c5813894-a302-4ac9-8e06-10847687656e
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece
  AssignClass (12371261-4188-43a6-abbf-e5aab1d0cc18)
 Call ID: 12371261-4188-43a6-abbf-e5aab1d0cc18
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (aae6efbe-4e1b-482b-9ff0-dffe7b916ff8)
 Call ID: aae6efbe-4e1b-482b-9ff0-dffe7b916ff8
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (70c00c16-58aa-4298-afbb-aa39621862d8)
 Call ID: 70c00c16-58aa-4298-afbb-aa39621862d8
  Args:
    type: :Person
    source: Marina_Karella
  AssignClass (541295d5-11ae-4149-8ed0-19b92b4197f8)
 Call ID: 541295d5-11ae-4149-8ed0-19b92b4197f8
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (fb58a12f-abe4-4d73-8175-b7ab7d69afcd)
 Call ID: fb58a12f-abe4-4d73-8175-b7ab7d69afcd
  Args:
    type: :Person
    source: Theódoros_Karéllas
  AssignClass (90dfa3d2-e4dd-47a9-987c-d34757547ecf)
 Call ID: 90dfa3d2-e4dd-47a9-987c-d34757547ecf
  Args:
    type: :Man
    source: Theódoros_Karéllas
  AssignClass (525e1b85-1599-4453-be25-22997397eec0)
 Call ID: 525e1b85-1599-4453-be25-22997397eec0
  Args:
    type: :Person
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (b05ab600-a594-4d96-bd51-8c45233b30ea)
 Call ID: b05ab600-a594-4d96-bd51-8c45233b30ea
  Args:
    type: :Man
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (15fa4ebf-b73a-49a2-8370-e73609f817fe)
 Call ID: 15fa4ebf-b73a-49a2-8370-e73609f817fe
  Args:
    type: :Person
    source: Amedeo_5th_Duke_of_Aosta
  AssignClass (f15bc227-bf3a-4bfe-8938-0373b82484d0)
 Call ID: f15bc227-bf3a-4bfe-8938-0373b82484d0
  Args:
    type: :Man
    source: Amedeo_5th_Duke_of_Aosta
  AssignClass (e972456f-a145-4ac8-9b92-f2b9d58cd30a)
 Call ID: e972456f-a145-4ac8-9b92-f2b9d58cd30a
  Args:
    type: :Person
    source: Princess_Alexandra
  AssignClass (043a47ee-6af0-4cfc-89c4-0d370b4bb862)
 Call ID: 043a47ee-6af0-4cfc-89c4-0d370b4bb862
  Args:
    type: :Woman
    source: Princess_Alexandra
  AssignClass (b3e59580-7d5e-46b0-abdd-77e22c45168e)
 Call ID: b3e59580-7d5e-46b0-abdd-77e22c45168e
  Args:
    type: :Person
    source: Umberto_of_Savoy-Aosta
  AssignClass (e268fbfd-5458-4164-9be0-09b00de59e58)
 Call ID: e268fbfd-5458-4164-9be0-09b00de59e58
  Args:
    type: :Man
    source: Umberto_of_Savoy-Aosta
  AssignClass (fb3ed9d6-6ba6-43ab-8713-07a98bea081d)
 Call ID: fb3ed9d6-6ba6-43ab-8713-07a98bea081d
  Args:
    type: :Person
    source: Amedeo_Michele_of_Savoy-Aosta
  AssignClass (1d53cc4b-c9e9-4a63-b775-d5001d33aa08)
 Call ID: 1d53cc4b-c9e9-4a63-b775-d5001d33aa08
  Args:
    type: :Man
    source: Amedeo_Michele_of_Savoy-Aosta
  AssignClass (db319fbb-88c0-45bb-8825-3d73e771ab56)
 Call ID: db319fbb-88c0-45bb-8825-3d73e771ab56
  Args:
    type: :Person
    source: Isabella_Vita_Marina_of_Savoy-Aosta
  AssignClass (907cc21f-707a-421f-9cba-a5b2e898283a)
 Call ID: 907cc21f-707a-421f-9cba-a5b2e898283a
  Args:
    type: :Woman
    source: Isabella_Vita_Marina_of_Savoy-Aosta
  AddTriple (548123c4-d9e0-4880-afe5-9c52412b98e3)
 Call ID: 548123c4-d9e0-4880-afe5-9c52412b98e3
  Args:
    source: Princess_Olga_of_Greece
    target: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (068fb556-6377-49de-bcb3-c39375af31f9)
 Call ID: 068fb556-6377-49de-bcb3-c39375af31f9
  Args:
    relation: :hasMother
    source: Princess_Olga_of_Greece
    target: Marina_Karella
  AddTriple (cd16a86b-bba3-4779-9214-0f4d6f40fbc9)
 Call ID: cd16a86b-bba3-4779-9214-0f4d6f40fbc9
  Args:
    source: Marina_Karella
    target: Theódoros_Karéllas
    relation: :hasFather
  AddTriple (ab8e2825-3cde-4a2a-b240-77e324f4b143)
 Call ID: ab8e2825-3cde-4a2a-b240-77e324f4b143
  Args:
    relation: :hasFather
    target: Amedeo_5th_Duke_of_Aosta
    source: Prince_Aimone_Duke_of_Aosta
  AddTriple (a6ee3358-8a21-4c97-bb78-c75768ada614)
 Call ID: a6ee3358-8a21-4c97-bb78-c75768ada614
  Args:
    relation: :isSisterOf
    source: Princess_Olga_of_Greece
    target: Princess_Alexandra
  AddTriple (27692cfd-5649-404a-9ae9-90abc6c4b2e9)
 Call ID: 27692cfd-5649-404a-9ae9-90abc6c4b2e9
  Args:
    relation: :hasMother
    target: Princess_Olga_of_Greece
    source: Umberto_of_Savoy-Aosta
  AddTriple (ea133c35-c356-40b0-9132-2b153e8b91e9)
 Call ID: ea133c35-c356-40b0-9132-2b153e8b91e9
  Args:
    source: Umberto_of_Savoy-Aosta
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (a31090e6-652b-4a58-8051-e58eeb347ed3)
 Call ID: a31090e6-652b-4a58-8051-e58eeb347ed3
  Args:
    target: Princess_Olga_of_Greece
    source: Amedeo_Michele_of_Savoy-Aosta
    relation: :hasMother
  AddTriple (593c7f88-73a8-47e8-967c-67973a654059)
 Call ID: 593c7f88-73a8-47e8-967c-67973a654059
  Args:
    relation: :hasFather
    target: Prince_Aimone_Duke_of_Aosta
    source: Amedeo_Michele_of_Savoy-Aosta
  AddTriple (fc151af2-cdab-4f37-aea6-dfe9a920b26c)
 Call ID: fc151af2-cdab-4f37-aea6-dfe9a920b26c
  Args:
    relation: :hasMother
    target: Princess_Olga_of_Greece
    source: Isabella_Vita_Marina_of_Savoy-Aosta
  AddTriple (6bbd986f-a093-4d49-9d69-2d8a968cd633)
 Call ID: 6bbd986f-a093-4d49-9d69-2d8a968cd633
  Args:
    relation: :hasFather
    source: Isabella_Vita_Marina_of_Savoy-Aosta
    target: Prince_Aimone_Duke_of_Aosta
  AddLiteral (3b17091a-7dff-433d-9720-4631501cf3c1)
 Call ID: 3b17091a-7dff-433d-9720-4631501cf3c1
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Princess_Olga_of_Greece
    literal_value: 1971
  Finish (3266ecf9-7d00-4563-a2d5-f4b54c93d52a)
 Call ID: 3266ecf9-7d00-4563-a2d5-f4b54c93d52a
  Args: