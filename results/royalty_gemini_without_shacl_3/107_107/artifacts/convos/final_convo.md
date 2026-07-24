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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Bernhard Lucas Emmanuel of Orange-Nassau, van Vollenhoven (born 25 December 1969) is a Dutch racing driver, entrepreneur and member of the Dutch royal family.
He is the second son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
With Willem-Alexander's succession however, he is no longer a member of the Dutch Royal House, and is no longer in line to direct succession to the Dutch throne, but still retains his membership of the Dutch royal family 


Early life and education

Bernhard was born on 25 December 1969 in Nijmegen in the Netherlands.
He is the second son of Princess Margriet and Pieter van Vollenhoven.
He has three brothers: Princes Maurits, Pieter-Christiaan, and Floris.
Subsequently, in 1989 he attended Groningen University in the Netherlands where he studied marketing and market research.
Business

Bernhard is a self-employed entrepreneur.
In 2002, the name Ritzen Koeriers was changed to Logistieke Meesters, at which time Bernhard was no longer involved in the business.
Marriage and family

While studying in Groningen, Bernhard met Annette Sekrève, (born 18 April 1972).
They have three children: Isabella Lily Juliana (born 2002), Samuel Bernhard Louis (born 2004), and Benjamin Pieter Floris (born 2008).
According to a royal decree of 5 July 2000, the children were granted the family name van Vollenhoven, without titles.
In January 2026, Bernhard and Annette announced that they were to divorce.
Upon the announcement of the planned abdication of Queen Beatrix, which took place on 30 April 2013, it was also restated that after the abdication, the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible for the throne.
Health

Bernhard has been receiving treatment for Crohn's disease since 2002.
Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (b2acc2d6-f679-486d-8165-d57a610fc972)
 Call ID: b2acc2d6-f679-486d-8165-d57a610fc972
  Args:
    type: :Woman
    source: Princess_Beatrix
  AssignClass (10087f7d-8fd7-43a7-a95e-5097ef20db47)
 Call ID: 10087f7d-8fd7-43a7-a95e-5097ef20db47
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (c5b827e9-18c1-47ab-967e-e75c1d96a08a)
 Call ID: c5b827e9-18c1-47ab-967e-e75c1d96a08a
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (8ba23475-5c73-4fee-b9cf-78c0a165a25b)
 Call ID: 8ba23475-5c73-4fee-b9cf-78c0a165a25b
  Args:
    type: :Man
    source: Prince_Bernhard_van_Vollenhoven
  AssignClass (2bb04584-52bc-4432-bafc-0729206ab469)
 Call ID: 2bb04584-52bc-4432-bafc-0729206ab469
  Args:
    type: :Man
    source: Prince_Maurits
  AssignClass (b7ff1e0f-7b35-44c4-aa4b-ce0fcb98c79b)
 Call ID: b7ff1e0f-7b35-44c4-aa4b-ce0fcb98c79b
  Args:
    type: :Man
    source: Prince_Pieter-Christiaan
  AssignClass (846ddd82-bcb5-4e53-af80-8f60aaf18ded)
 Call ID: 846ddd82-bcb5-4e53-af80-8f60aaf18ded
  Args:
    type: :Man
    source: Prince_Floris
  AssignClass (b2c82ad7-007b-4c60-9768-1c6b2e24de8a)
 Call ID: b2c82ad7-007b-4c60-9768-1c6b2e24de8a
  Args:
    type: :Woman
    source: Annette_Sekreve
  AssignClass (4eed480c-a4f7-41c4-af20-86326793b456)
 Call ID: 4eed480c-a4f7-41c4-af20-86326793b456
  Args:
    type: :Woman
    source: Isabella_Lily_Juliana
  AssignClass (9e96e210-b8c3-4531-ae25-90e4684dd2ce)
 Call ID: 9e96e210-b8c3-4531-ae25-90e4684dd2ce
  Args:
    type: :Man
    source: Samuel_Bernhard_Louis
  AssignClass (ee880e2d-7883-4a65-9aea-c09ce0dfeddf)
 Call ID: ee880e2d-7883-4a65-9aea-c09ce0dfeddf
  Args:
    type: :Man
    source: Benjamin_Pieter_Floris
  AddLiteral (fc905a1d-7d00-4605-a6c8-206b0bcb04ff)
 Call ID: fc905a1d-7d00-4605-a6c8-206b0bcb04ff
  Args:
    relation: :hasBirthYear
    literal_value: 1969
    literal_type: xsd:integer
    source: Prince_Bernhard_van_Vollenhoven
  AddLiteral (a5341a22-19cd-4356-9783-3e7423fbae8c)
 Call ID: a5341a22-19cd-4356-9783-3e7423fbae8c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1972
    source: Annette_Sekreve
  AddLiteral (be97ba53-3012-43bc-b2dd-77160c18a26f)
 Call ID: be97ba53-3012-43bc-b2dd-77160c18a26f
  Args:
    source: Isabella_Lily_Juliana
    literal_value: 2002
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4f44e60d-0abe-48f6-9715-211025808162)
 Call ID: 4f44e60d-0abe-48f6-9715-211025808162
  Args:
    relation: :hasBirthYear
    source: Samuel_Bernhard_Louis
    literal_type: xsd:integer
    literal_value: 2004
  AddLiteral (4d0e3281-e088-406e-aa6e-1173b69dd399)
 Call ID: 4d0e3281-e088-406e-aa6e-1173b69dd399
  Args:
    source: Benjamin_Pieter_Floris
    literal_value: 2008
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (746d0240-e48e-40da-9056-48bd934a7c26)
 Call ID: 746d0240-e48e-40da-9056-48bd934a7c26
  Args:
    relation: :isMotherOf
    target: Prince_Bernhard_van_Vollenhoven
    source: Princess_Margriet
  AddTriple (c97ce502-a9ba-45ad-bcd4-c9ac8b51f7dd)
 Call ID: c97ce502-a9ba-45ad-bcd4-c9ac8b51f7dd
  Args:
    source: Pieter_van_Vollenhoven
    target: Prince_Bernhard_van_Vollenhoven
    relation: :isFatherOf
  AddTriple (1413ea39-3ee4-4796-bf6e-f8c349d3eeab)
 Call ID: 1413ea39-3ee4-4796-bf6e-f8c349d3eeab
  Args:
    source: Princess_Margriet
    target: Prince_Maurits
    relation: :isMotherOf
  AddTriple (21359e45-adf7-4c44-ab14-825070982f72)
 Call ID: 21359e45-adf7-4c44-ab14-825070982f72
  Args:
    relation: :isFatherOf
    target: Prince_Maurits
    source: Pieter_van_Vollenhoven
  AddTriple (b11fe778-b69a-40be-a201-f2eafb146f9e)
 Call ID: b11fe778-b69a-40be-a201-f2eafb146f9e
  Args:
    relation: :isMotherOf
    target: Prince_Pieter-Christiaan
    source: Princess_Margriet
  AddTriple (f929f29a-793b-454f-98e4-eaab106619e0)
 Call ID: f929f29a-793b-454f-98e4-eaab106619e0
  Args:
    relation: :isFatherOf
    source: Pieter_van_Vollenhoven
    target: Prince_Pieter-Christiaan
  AddTriple (9940162b-8422-497b-a216-23ed08bafe66)
 Call ID: 9940162b-8422-497b-a216-23ed08bafe66
  Args:
    relation: :isMotherOf
    source: Princess_Margriet
    target: Prince_Floris
  AddTriple (063950b4-56a0-41b9-acb5-db589a6554b8)
 Call ID: 063950b4-56a0-41b9-acb5-db589a6554b8
  Args:
    target: Prince_Floris
    source: Pieter_van_Vollenhoven
    relation: :isFatherOf
  AddTriple (4e159fcf-62e9-40e0-a9b1-ae15adef44c8)
 Call ID: 4e159fcf-62e9-40e0-a9b1-ae15adef44c8
  Args:
    source: Annette_Sekreve
    target: Isabella_Lily_Juliana
    relation: :isMotherOf
  AddTriple (a2e03c06-9d44-4706-b7f4-0b808471d7f2)
 Call ID: a2e03c06-9d44-4706-b7f4-0b808471d7f2
  Args:
    relation: :isFatherOf
    source: Prince_Bernhard_van_Vollenhoven
    target: Isabella_Lily_Juliana
  AddTriple (8268ecb6-343f-441b-8093-59ba83dee773)
 Call ID: 8268ecb6-343f-441b-8093-59ba83dee773
  Args:
    target: Samuel_Bernhard_Louis
    source: Annette_Sekreve
    relation: :isMotherOf
  AddTriple (d5be284b-947e-4363-8d9b-e24cec3eb285)
 Call ID: d5be284b-947e-4363-8d9b-e24cec3eb285
  Args:
    target: Samuel_Bernhard_Louis
    source: Prince_Bernhard_van_Vollenhoven
    relation: :isFatherOf
  AddTriple (921754aa-e459-4689-9557-e13b051c723d)
 Call ID: 921754aa-e459-4689-9557-e13b051c723d
  Args:
    relation: :isMotherOf
    source: Annette_Sekreve
    target: Benjamin_Pieter_Floris
  AddTriple (2c8c4886-26cf-4c50-9f6f-634b6f84c7cc)
 Call ID: 2c8c4886-26cf-4c50-9f6f-634b6f84c7cc
  Args:
    relation: :isFatherOf
    source: Prince_Bernhard_van_Vollenhoven
    target: Benjamin_Pieter_Floris
  Finish (4ef056f1-fe47-48f9-9c3b-4a9979f299d6)
 Call ID: 4ef056f1-fe47-48f9-9c3b-4a9979f299d6
  Args: