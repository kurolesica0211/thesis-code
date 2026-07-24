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
Princess Alexandrine Irene of Prussia (7 April 1915 – 2 October 1980) was the elder daughter and fifth child of Wilhelm, German Crown Prince, and Cecilie of Mecklenburg-Schwerin.
Her grandparents were Wilhelm II, German Emperor and his wife Augusta Victoria of Schleswig-Holstein, and Frederick Francis III of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
Alexandrine was a member of the House of Hohenzollern.
She was a great-great-granddaughter of Queen Victoria.
Life

Alexandrine was born at the Kronprinzenpalais in Berlin.
She followed older brothers Wilhelm, Louis Ferdinand, Hubertus, and Frederick.
Alexandrine's only sister, Cecilie, was born in 1917.
It became clear shortly after Alexandrine's birth that she had Down syndrome.
Unlike other disabled royal children, Alexandrine was not hidden away.
As a teenager, Alexandrine attended the Trüpersche Sonderschule, a school dedicated to the education of children with special needs.
Alexandrine celebrated her confirmation along with her sister Cecilie in October 1934.
Alexandrine lived most of her later life in Bavaria, first in Pöcking and later near Lake Starnberg, where she was visited there regularly by her family, particularly her brother Louis Ferdinand.
Alexandrine died on 2 October 1980.
She was buried near her parents and brother Frederick at Hohenzollern Castle.



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
  AssignClass (fd281d44-7b32-463c-9095-56d8aed8d992)
 Call ID: fd281d44-7b32-463c-9095-56d8aed8d992
  Args:
    type: :Woman
    source: Alexandrine_Irene_of_Prussia
  AssignClass (9fefed1d-e8c3-4bd4-94b7-45a57d3d5e71)
 Call ID: 9fefed1d-e8c3-4bd4-94b7-45a57d3d5e71
  Args:
    type: :Person
    source: Alexandrine_Irene_of_Prussia
  AddLiteral (f7d7d964-10b5-4778-b259-1dbcdf43c97c)
 Call ID: f7d7d964-10b5-4778-b259-1dbcdf43c97c
  Args:
    relation: :hasBirthYear
    literal_value: 1915
    literal_type: xsd:integer
    source: Alexandrine_Irene_of_Prussia
  AddLiteral (a1f64057-94c5-400e-8120-516ee655d88c)
 Call ID: a1f64057-94c5-400e-8120-516ee655d88c
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Alexandrine_Irene_of_Prussia
  AssignClass (cb13b5c0-c731-4d8d-9151-cc0a5cb4d75b)
 Call ID: cb13b5c0-c731-4d8d-9151-cc0a5cb4d75b
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (69341de4-f24f-4e9b-8215-ef17f37ad4fe)
 Call ID: 69341de4-f24f-4e9b-8215-ef17f37ad4fe
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AssignClass (41251944-ce30-43b2-b04a-18b75fc84a80)
 Call ID: 41251944-ce30-43b2-b04a-18b75fc84a80
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (00dac7f6-4df8-4070-b1b7-5e95226525af)
 Call ID: 00dac7f6-4df8-4070-b1b7-5e95226525af
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (b685b3ed-d70b-4d6a-a279-bec33b43bec1)
 Call ID: b685b3ed-d70b-4d6a-a279-bec33b43bec1
  Args:
    source: Alexandrine_Irene_of_Prussia
    relation: :hasFather
    target: Wilhelm_German_Crown_Prince
  AddTriple (a4d4938b-e673-401f-89f0-8df83734755e)
 Call ID: a4d4938b-e673-401f-89f0-8df83734755e
  Args:
    source: Alexandrine_Irene_of_Prussia
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (e4d30d2f-45ea-4b93-b3eb-ce069365f180)
 Call ID: e4d30d2f-45ea-4b93-b3eb-ce069365f180
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (0bd17133-584b-4916-b751-bf84651200d2)
 Call ID: 0bd17133-584b-4916-b751-bf84651200d2
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (bcfcd95d-4b89-4dba-a26a-2af805284f8f)
 Call ID: bcfcd95d-4b89-4dba-a26a-2af805284f8f
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (bc6cc4de-51b8-4abc-9750-6d15c6baf578)
 Call ID: bc6cc4de-51b8-4abc-9750-6d15c6baf578
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (ab20aae8-2be9-4909-af3c-c615b3e43a28)
 Call ID: ab20aae8-2be9-4909-af3c-c615b3e43a28
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (9513d102-90b2-47f3-8744-1a65125799e7)
 Call ID: 9513d102-90b2-47f3-8744-1a65125799e7
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (179e794a-c0bf-4aa6-a6b7-8ce6e0957f4e)
 Call ID: 179e794a-c0bf-4aa6-a6b7-8ce6e0957f4e
  Args:
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (cdc70868-9d86-47fc-8644-ce8be85f6f2c)
 Call ID: cdc70868-9d86-47fc-8644-ce8be85f6f2c
  Args:
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    type: :Person
  AddTriple (e1acafed-6d84-46c1-ad28-a266915e5bcb)
 Call ID: e1acafed-6d84-46c1-ad28-a266915e5bcb
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasFather
    target: Wilhelm_II_German_Emperor
  AddTriple (8d578438-db50-4015-a9eb-81cf328d2130)
 Call ID: 8d578438-db50-4015-a9eb-81cf328d2130
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (1d78cf95-ce49-4367-b1eb-78666fb50946)
 Call ID: 1d78cf95-ce49-4367-b1eb-78666fb50946
  Args:
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    relation: :hasFather
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (d4da3df5-e77d-4b0e-9343-2f5916f4f32d)
 Call ID: d4da3df5-e77d-4b0e-9343-2f5916f4f32d
  Args:
    target: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    relation: :hasMother
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (3d13f40f-3a2e-418c-8c69-4e2358b51f89)
 Call ID: 3d13f40f-3a2e-418c-8c69-4e2358b51f89
  Args:
    type: :Man
    source: Wilhelm_brother
  AssignClass (ec8b6370-1fa3-4058-88c3-d92537dac6fa)
 Call ID: ec8b6370-1fa3-4058-88c3-d92537dac6fa
  Args:
    type: :Person
    source: Wilhelm_brother
  AssignClass (f98796bb-48d1-4139-b6ad-6f846856e04e)
 Call ID: f98796bb-48d1-4139-b6ad-6f846856e04e
  Args:
    source: Louis_Ferdinand
    type: :Man
  AssignClass (7b081083-b517-4c3c-a16a-cb89e1ad59b9)
 Call ID: 7b081083-b517-4c3c-a16a-cb89e1ad59b9
  Args:
    source: Louis_Ferdinand
    type: :Person
  AssignClass (8f2bb394-c873-467f-84d9-aa18078d42a7)
 Call ID: 8f2bb394-c873-467f-84d9-aa18078d42a7
  Args:
    type: :Man
    source: Hubertus
  AssignClass (be2fb63e-e246-400d-8699-73a06cda7939)
 Call ID: be2fb63e-e246-400d-8699-73a06cda7939
  Args:
    source: Hubertus
    type: :Person
  AssignClass (81f7cbf4-0b38-48ee-9208-efb62d60ff14)
 Call ID: 81f7cbf4-0b38-48ee-9208-efb62d60ff14
  Args:
    type: :Man
    source: Frederick
  AssignClass (7d7cb59c-de0d-48e8-b0d0-5190910efb82)
 Call ID: 7d7cb59c-de0d-48e8-b0d0-5190910efb82
  Args:
    source: Frederick
    type: :Person
  AssignClass (4da05c86-bd14-46cc-8543-3bb2bf007741)
 Call ID: 4da05c86-bd14-46cc-8543-3bb2bf007741
  Args:
    type: :Woman
    source: Cecilie_sister
  AssignClass (85b283fa-3374-4952-802c-388603d488c7)
 Call ID: 85b283fa-3374-4952-802c-388603d488c7
  Args:
    source: Cecilie_sister
    type: :Person
  AddTriple (dcd6ed94-51f0-4e3f-8982-db81bf1c2d76)
 Call ID: dcd6ed94-51f0-4e3f-8982-db81bf1c2d76
  Args:
    target: Wilhelm_brother
    relation: :hasBrother
    source: Alexandrine_Irene_of_Prussia
  AddTriple (fed7161f-f68a-4acc-95b8-79d62fbc1d4e)
 Call ID: fed7161f-f68a-4acc-95b8-79d62fbc1d4e
  Args:
    source: Alexandrine_Irene_of_Prussia
    target: Louis_Ferdinand
    relation: :hasBrother
  AddTriple (53871aa5-cef0-4911-b46a-6d02d6139a50)
 Call ID: 53871aa5-cef0-4911-b46a-6d02d6139a50
  Args:
    source: Alexandrine_Irene_of_Prussia
    target: Hubertus
    relation: :hasBrother
  AddTriple (47b0a4a3-3f57-410a-80a6-e09b7b0d530f)
 Call ID: 47b0a4a3-3f57-410a-80a6-e09b7b0d530f
  Args:
    source: Alexandrine_Irene_of_Prussia
    relation: :hasBrother
    target: Frederick
  AddTriple (e2007be2-aea8-48c0-bba2-4fba230753a0)
 Call ID: e2007be2-aea8-48c0-bba2-4fba230753a0
  Args:
    source: Alexandrine_Irene_of_Prussia
    target: Cecilie_sister
    relation: :hasSister
  Finish (48a149fb-3c8c-4234-a234-cd2c5f660ae7)
 Call ID: 48a149fb-3c8c-4234-a234-cd2c5f660ae7
  Args: