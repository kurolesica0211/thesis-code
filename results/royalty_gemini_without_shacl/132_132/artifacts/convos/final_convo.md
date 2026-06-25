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
  AssignClass (032dbacb-2bef-4cd4-8f98-9cb76825acbd)
 Call ID: 032dbacb-2bef-4cd4-8f98-9cb76825acbd
  Args:
    source: Prince_Richard_of_Hesse
    type: :Man
  AssignClass (26248b0a-0720-48fb-a8f2-967826f8da7b)
 Call ID: 26248b0a-0720-48fb-a8f2-967826f8da7b
  Args:
    source: Prince_Richard_of_Hesse
    type: :Person
  AssignClass (bd4a14bb-dcdc-4a8d-a980-38714ddcaf60)
 Call ID: bd4a14bb-dcdc-4a8d-a980-38714ddcaf60
  Args:
    source: Prince_Christoph_of_Hesse-Kassel
    type: :Man
  AssignClass (c95e812a-d5e8-44bb-bf08-c0f961115e72)
 Call ID: c95e812a-d5e8-44bb-bf08-c0f961115e72
  Args:
    source: Prince_Christoph_of_Hesse-Kassel
    type: :Person
  AssignClass (55b92a90-8470-4695-bb78-ad70e0850c37)
 Call ID: 55b92a90-8470-4695-bb78-ad70e0850c37
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (a72184ca-4a3a-4bbf-a0d9-e92574c43a35)
 Call ID: a72184ca-4a3a-4bbf-a0d9-e92574c43a35
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Person
  AssignClass (124966f3-9356-4a63-b8d2-3a60ddb27821)
 Call ID: 124966f3-9356-4a63-b8d2-3a60ddb27821
  Args:
    source: Princess_Margaret_of_Prussia
    type: :Woman
  AssignClass (0b1ce53d-2b63-43a0-b6cb-a3681aa783a4)
 Call ID: 0b1ce53d-2b63-43a0-b6cb-a3681aa783a4
  Args:
    source: Princess_Margaret_of_Prussia
    type: :Person
  AssignClass (8475b06b-a4ce-4620-b229-8eaec8ecd880)
 Call ID: 8475b06b-a4ce-4620-b229-8eaec8ecd880
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (b024b255-def6-4e7a-b766-2ab2d0bcd738)
 Call ID: b024b255-def6-4e7a-b766-2ab2d0bcd738
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (d1854974-35c7-4c1b-88b5-62aff2d31589)
 Call ID: d1854974-35c7-4c1b-88b5-62aff2d31589
  Args:
    source: Emperor_Wilhelm_II
    type: :Man
  AssignClass (dee21186-e96f-4753-a0b2-323911ff46ff)
 Call ID: dee21186-e96f-4753-a0b2-323911ff46ff
  Args:
    source: Emperor_Wilhelm_II
    type: :Person
  AssignClass (d92940d6-b382-42db-a9cf-3ec1a8846ead)
 Call ID: d92940d6-b382-42db-a9cf-3ec1a8846ead
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (89266e14-a0e2-415f-827a-82aace9d5738)
 Call ID: 89266e14-a0e2-415f-827a-82aace9d5738
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Person
  AssignClass (4430c368-b022-4b9c-b2ac-2ad692283d04)
 Call ID: 4430c368-b022-4b9c-b2ac-2ad692283d04
  Args:
    source: Prince_Philippe_of_Hesse
    type: :Man
  AssignClass (ff72a277-37b9-4433-88f2-bd5d654d9fd3)
 Call ID: ff72a277-37b9-4433-88f2-bd5d654d9fd3
  Args:
    source: Prince_Philippe_of_Hesse
    type: :Person
  AssignClass (b038fced-835b-45f9-9026-2f4a132b29f4)
 Call ID: b038fced-835b-45f9-9026-2f4a132b29f4
  Args:
    source: Mafalda_of_Italy
    type: :Woman
  AssignClass (6f2116d7-6517-40f5-9788-4fde34f3fffc)
 Call ID: 6f2116d7-6517-40f5-9788-4fde34f3fffc
  Args:
    source: Mafalda_of_Italy
    type: :Person
  AssignClass (5df92d86-a385-44b1-8aa7-4f05e529c2b4)
 Call ID: 5df92d86-a385-44b1-8aa7-4f05e529c2b4
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (cb7d1323-0881-4161-bb4b-fd374f014e86)
 Call ID: cb7d1323-0881-4161-bb4b-fd374f014e86
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Person
  AddLiteral (1d2c9e3c-72d9-4915-818e-16731f2ca8c0)
 Call ID: 1d2c9e3c-72d9-4915-818e-16731f2ca8c0
  Args:
    source: Prince_Richard_of_Hesse
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1901
  AddLiteral (ca20e29d-141c-4b1b-9351-0c82511e3a17)
 Call ID: ca20e29d-141c-4b1b-9351-0c82511e3a17
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Richard_of_Hesse
    literal_value: 1969
  AddTriple (53d20bac-3a10-46ac-9913-15de594395c6)
 Call ID: 53d20bac-3a10-46ac-9913-15de594395c6
  Args:
    relation: :hasFather
    target: Prince_Frederick_Charles_of_Hesse
    source: Prince_Richard_of_Hesse
  AddTriple (9efbbb0f-a463-47f9-a946-b79a9b6ec1b5)
 Call ID: 9efbbb0f-a463-47f9-a946-b79a9b6ec1b5
  Args:
    source: Prince_Richard_of_Hesse
    relation: :hasMother
    target: Princess_Margaret_of_Prussia
  AddTriple (646e395b-3962-44e0-aa6f-91328dcbe164)
 Call ID: 646e395b-3962-44e0-aa6f-91328dcbe164
  Args:
    relation: :isBrotherOf
    target: Prince_Christoph_of_Hesse-Kassel
    source: Prince_Richard_of_Hesse
  AddTriple (d162db0f-4b96-4169-b563-59a93c1431b6)
 Call ID: d162db0f-4b96-4169-b563-59a93c1431b6
  Args:
    target: Prince_Richard_of_Hesse
    relation: :isBrotherOf
    source: Prince_Christoph_of_Hesse-Kassel
  AddTriple (ea829a75-2f77-484b-9da3-ae8036a61752)
 Call ID: ea829a75-2f77-484b-9da3-ae8036a61752
  Args:
    target: Prince_Philippe_of_Hesse
    relation: :isBrotherOf
    source: Prince_Richard_of_Hesse
  AddTriple (dcd06eb5-bb2b-4432-aa8a-1fbcb9c62049)
 Call ID: dcd06eb5-bb2b-4432-aa8a-1fbcb9c62049
  Args:
    source: Prince_Richard_of_Hesse
    target: Prince_Wolfgang_of_Hesse
    relation: :isBrotherOf
  AddTriple (3abaff8f-8e43-4776-8775-8e75c44560b7)
 Call ID: 3abaff8f-8e43-4776-8775-8e75c44560b7
  Args:
    relation: :isSisterOf
    target: Emperor_Wilhelm_II
    source: Princess_Margaret_of_Prussia
  AddTriple (5539ce93-bc79-4892-9bb1-a2437cdb294a)
 Call ID: 5539ce93-bc79-4892-9bb1-a2437cdb294a
  Args:
    relation: :isBrotherOf
    target: Princess_Margaret_of_Prussia
    source: Emperor_Wilhelm_II
  AddTriple (334eae25-1d98-4e83-a340-8e4eade96de7)
 Call ID: 334eae25-1d98-4e83-a340-8e4eade96de7
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    target: Prince_Richard_of_Hesse
    relation: :isFatherOf
  AddTriple (26b8bdff-1413-41b6-87ff-19c3bb245f7b)
 Call ID: 26b8bdff-1413-41b6-87ff-19c3bb245f7b
  Args:
    source: Princess_Margaret_of_Prussia
    relation: :isMotherOf
    target: Prince_Richard_of_Hesse
  AddTriple (ec1abb4f-6df5-4ffb-94bd-803a9c8f401f)
 Call ID: ec1abb4f-6df5-4ffb-94bd-803a9c8f401f
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    target: Prince_Christoph_of_Hesse-Kassel
    relation: :isFatherOf
  AddTriple (efc3c397-8de1-48c4-a473-b839c224b3a9)
 Call ID: efc3c397-8de1-48c4-a473-b839c224b3a9
  Args:
    relation: :isMotherOf
    target: Prince_Christoph_of_Hesse-Kassel
    source: Princess_Margaret_of_Prussia
  AddTriple (ed4972d5-aebc-4881-8779-d90722b9e166)
 Call ID: ed4972d5-aebc-4881-8779-d90722b9e166
  Args:
    source: Prince_Christoph_of_Hesse-Kassel
    relation: :hasMarriageYear
    target: Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (88771274-460f-4781-8a61-d7ba32aafb3e)
 Call ID: 88771274-460f-4781-8a61-d7ba32aafb3e
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Christoph_of_Hesse-Kassel
    literal_value: 1930
  Finish (37bab933-1f4a-403d-83ff-749fa4772c89)
 Call ID: 37bab933-1f4a-403d-83ff-749fa4772c89
  Args: