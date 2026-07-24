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
Prince Richard of Hesse (Richard Wilhelm Leopold; 14
May 1901 – 11 February 1969) was a German prince and politician.
Early life

Prince Richard and his twin brother Christoph were born on 14 May 1901 in Frankfurt am Main, in Prussian Hesse as the fifth son Prince Frederick Charles of Hesse and his wife Princess Margaret of Prussia.
His great-grandmother was Queen Victoria, his mother was the youngest sister of Emperor Wilhelm II.
Richard, affectionately nicknamed "Ri" by his family, grew up in a loving and close-knit family.
Career and later life

The First World War and the fall of the imperial regime

Too young to be mobilized when the First World War broke out, Richard and Prince Christoph of Hesse-Kassel spent most of the conflict in Kronberg, where they were educated at the Reform Realgymnasium.
Unlike his twin brother, who did not take the exam, Richard obtained the abitur in 1920.
Closely linked to the former Kaiser Wilhelm II, whose sister was Princess Margaret, the Hesse-Kassel were then attacked by the revolutionaries.
In this unstable context, Richard and Christoph engage as auxiliaries (hilfsdient) to protect the transports passing through Kronberg while awaiting the arrival of the French occupation troops.
Training and love life

After World War I, Richard studied civil engineering and mechanical engineering at the Darmstadt University of Technology.
From a sentimental point of view, Richard fell in love with Princess Sophie of Greece and Denmark, met around 1927.
However, she fell in love with Richard's twin brother Prince Christoph of Hesse-Kassel, and it is the latter that she married, in 1930.
Adherence to Nazism

Like his three brothers, Richard was enthusiastic about Nazism.
In 1932, the prince thus joined simultaneously the SA and the NSDAP.
Subsequently, Richard became a general (Obergruppenführer) in the Nationalsozialistisches Kraftfahrkorps (NSKK), a special unit of the SA corps, and obtained leadership of the Motorgruppe Hessen in 1935.
From a more political point of view, the prince ran, without success, in the German parliamentary elections of March 1936 and April 1938.
The Second World War and its consequences

Prince Richard enlisted in the German Army shortly after the outbreak of the Second World War.
HAS following the strengthening of the "decree of the princes", Richard was however informed of his dismissal from the army by the Reichsleiter Martin Bormann in October 1943.
At the same time, his older brother Philippe and his sister-in-law Mafalda of Italy were arrested by the Hitler regime while his twin brother, Prince Christoph of Hesse-Kassel, died in a plane crash.
Post-war and its consequences

The defeat of Germany and its occupation by the Allies brought new difficulties to Richard's life.
Arrested by the Americans shortly after the capitulation of his country, the prince was interned for sixteen months in the camp of Moosburg, in Bavaria.
Several months later, the prince underwent a denazification trial.
Meanwhile, the jewels of the House of Hesse-Kassel were stolen by American officers in 1946 and only 10% of the stolen objects were finally returned to their rightful owners, in 1951.
Later years

After the Second World War, Richard assisted his brother Prince Wolfgang of Hesse for a while in the management of the Hessische Hausstiftung.
Subsequently, he was appointed to the traffic surveillance of the state of Hesse.
In the same years, Richard of Hesse-Kassel joined the spiritual movement of “Moral Rearmament”, founded by the Lutheran pastor Frank Buchman.
Prince Richard died in 1969.



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
  AssignClass (b3091105-9265-4c48-ba41-c930086f5527)
 Call ID: b3091105-9265-4c48-ba41-c930086f5527
  Args:
    type: :Man
    source: :Prince_Richard_of_Hesse
  AssignClass (385150f3-1844-4d30-accf-a32637ed756e)
 Call ID: 385150f3-1844-4d30-accf-a32637ed756e
  Args:
    type: :Person
    source: :Prince_Richard_of_Hesse
  AddLiteral (9975abce-7088-4352-bcbc-182960f0b715)
 Call ID: 9975abce-7088-4352-bcbc-182960f0b715
  Args:
    literal_type: xsd:integer
    source: :Prince_Richard_of_Hesse
    relation: :hasBirthYear
    literal_value: 1901
  AddLiteral (abf27051-940e-45ed-85a7-c5bb0271950b)
 Call ID: abf27051-940e-45ed-85a7-c5bb0271950b
  Args:
    literal_type: xsd:integer
    literal_value: 1969
    relation: :hasDeathYear
    source: :Prince_Richard_of_Hesse
  AssignClass (bd40d8ff-b7d1-4de9-a22f-36c70979f789)
 Call ID: bd40d8ff-b7d1-4de9-a22f-36c70979f789
  Args:
    type: :Man
    source: :Prince_Christoph_of_Hesse-Kassel
  AssignClass (56d5c49a-cb4d-4fe4-8049-6a300fd91e25)
 Call ID: 56d5c49a-cb4d-4fe4-8049-6a300fd91e25
  Args:
    type: :Person
    source: :Prince_Christoph_of_Hesse-Kassel
  AddTriple (bef2ee33-6359-482b-b5cc-8a38e178b4af)
 Call ID: bef2ee33-6359-482b-b5cc-8a38e178b4af
  Args:
    relation: :isSiblingOf
    target: :Prince_Christoph_of_Hesse-Kassel
    source: :Prince_Richard_of_Hesse
  AssignClass (20ea2db6-897a-4d82-ac31-521dde51564b)
 Call ID: 20ea2db6-897a-4d82-ac31-521dde51564b
  Args:
    type: :Man
    source: :Prince_Frederick_Charles_of_Hesse
  AssignClass (80801701-e87d-4c13-91d6-4b69783f5cc0)
 Call ID: 80801701-e87d-4c13-91d6-4b69783f5cc0
  Args:
    type: :Person
    source: :Prince_Frederick_Charles_of_Hesse
  AssignClass (04d11f57-8f6f-44ca-ad25-e666adb0aac6)
 Call ID: 04d11f57-8f6f-44ca-ad25-e666adb0aac6
  Args:
    type: :Woman
    source: :Princess_Margaret_of_Prussia
  AssignClass (ba40215b-0fbd-4ce4-8677-cbb4923f25ea)
 Call ID: ba40215b-0fbd-4ce4-8677-cbb4923f25ea
  Args:
    type: :Person
    source: :Princess_Margaret_of_Prussia
  AddTriple (a19a8bef-2cb0-4e10-ac95-f7df01236c85)
 Call ID: a19a8bef-2cb0-4e10-ac95-f7df01236c85
  Args:
    source: :Prince_Richard_of_Hesse
    target: :Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
  AddTriple (c015f253-2ba6-4534-b92b-b43217bba886)
 Call ID: c015f253-2ba6-4534-b92b-b43217bba886
  Args:
    target: :Princess_Margaret_of_Prussia
    relation: :hasMother
    source: :Prince_Richard_of_Hesse
  AssignClass (99e36215-dcd7-43a0-bfa2-6ad19e5439b4)
 Call ID: 99e36215-dcd7-43a0-bfa2-6ad19e5439b4
  Args:
    type: :Woman
    source: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (86d96543-3b47-4d22-ab85-004f548cee4d)
 Call ID: 86d96543-3b47-4d22-ab85-004f548cee4d
  Args:
    type: :Person
    source: :Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (fe17ccdb-a2e8-4f4e-9fee-81fc72c0cb90)
 Call ID: fe17ccdb-a2e8-4f4e-9fee-81fc72c0cb90
  Args:
    literal_value: 1930
    relation: :hasMarriageYear
    source: :Prince_Christoph_of_Hesse-Kassel
    literal_type: xsd:integer
  AddTriple (a1ef638c-cd1d-46f5-8b59-a0e159c83e59)
 Call ID: a1ef638c-cd1d-46f5-8b59-a0e159c83e59
  Args:
    source: :Prince_Christoph_of_Hesse-Kassel
    relation: :hasRelation
    target: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (a9110ab1-0c2f-471e-afb0-33d94109eb5c)
 Call ID: a9110ab1-0c2f-471e-afb0-33d94109eb5c
  Args:
    type: :Man
    source: :Prince_Philippe_of_Hesse
  AssignClass (fdab6444-5ebe-40fa-892d-82edc59bd1ba)
 Call ID: fdab6444-5ebe-40fa-892d-82edc59bd1ba
  Args:
    type: :Person
    source: :Prince_Philippe_of_Hesse
  AddTriple (9cad77a1-057d-491b-b335-bee93cc66f27)
 Call ID: 9cad77a1-057d-491b-b335-bee93cc66f27
  Args:
    relation: :isSiblingOf
    target: :Prince_Philippe_of_Hesse
    source: :Prince_Richard_of_Hesse
  AssignClass (71e27ad7-f626-435a-a2a6-ebea9850cb0a)
 Call ID: 71e27ad7-f626-435a-a2a6-ebea9850cb0a
  Args:
    type: :Woman
    source: :Mafalda_of_Italy
  AssignClass (5f4e5c0f-fc7e-4ea2-a424-f5d718c3c122)
 Call ID: 5f4e5c0f-fc7e-4ea2-a424-f5d718c3c122
  Args:
    type: :Person
    source: :Mafalda_of_Italy
  AddTriple (66ce0dd6-d211-4470-90e8-54d6a3cca2d6)
 Call ID: 66ce0dd6-d211-4470-90e8-54d6a3cca2d6
  Args:
    source: :Prince_Philippe_of_Hesse
    target: :Mafalda_of_Italy
    relation: :hasRelation
  AssignClass (4043d567-3a5e-4c76-8c94-8f19bf9e1a6d)
 Call ID: 4043d567-3a5e-4c76-8c94-8f19bf9e1a6d
  Args:
    type: :Man
    source: :Prince_Wolfgang_of_Hesse
  AssignClass (f140fd44-3b8b-43cc-8f31-4ae0cb5ed875)
 Call ID: f140fd44-3b8b-43cc-8f31-4ae0cb5ed875
  Args:
    type: :Person
    source: :Prince_Wolfgang_of_Hesse
  AddTriple (d5543755-4e4d-4e83-945b-8e56a374ff0d)
 Call ID: d5543755-4e4d-4e83-945b-8e56a374ff0d
  Args:
    source: :Prince_Richard_of_Hesse
    relation: :isSiblingOf
    target: :Prince_Wolfgang_of_Hesse
  Finish (6f51f15f-9e56-4267-a20e-4fce149db894)
 Call ID: 6f51f15f-9e56-4267-a20e-4fce149db894
  Args: