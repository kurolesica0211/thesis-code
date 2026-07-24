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
Louis Ferdinand, Prince of Prussia (German: Louis Ferdinand Victor Eduard Adalbert Michael Hubertus Prinz von Preußen; 9 November 1907 –  26 September 1994) was a grandson of Kaiser Wilhelm II and member of the  House of Hohenzollern, which occupied the Prussian and German thrones until the abolition of those monarchies in 1918.
Biography

Louis Ferdinand was born in Potsdam as the third in succession to the throne of the German Empire, after his father, German Crown Prince William and elder brother Prince Wilhelm of Prussia.
When Louis Ferdinand's older brother Prince Wilhelm renounced his succession rights to marry a member of the untitled nobility in 1933 (he was later to be killed in action in France in 1940 while fighting in the German army), Louis Ferdinand replaced him as second in the line of succession to the defunct German and Prussian thrones after the former Crown Prince.
Louis Ferdinand was educated in Berlin and deviated from his family's tradition by not pursuing a military career.
Louis Ferdinand dissociated himself from the Nazis after this.
He married his second cousin, Grand Duchess Kira Kirillovna of Russia, in 1938 in first a Russian Orthodox ceremony in Potsdam and then a Lutheran ceremony in Huis Doorn, Netherlands.
Kira was the second daughter of Grand Duke Kyril Vladimirovich and Princess Victoria Melita of Saxe-Coburg and Gotha.
His third son and heir apparent, Prince Louis Ferdinand, died in 1977 during military maneuvers, and thus his one-year-old grandson Georg Friedrich, Prince of Prussia (son of Prince Louis Ferdinand) became the new heir apparent to the defunct Prussian and German Imperial throne.
Upon Louis Ferdinand's death in 1994, Georg Friedrich became the pretender to the defunct thrones and head of the Hohenzollern family.
The prince was a popular figure.
In 1968 Der Spiegel reported that in a survey of their readers by Quick magazine about who would be the most honorable person to become President of the Federal Republic of Germany, Louis Ferdinand, the only one of twelve candidates who was not a politician, won with 39.8% before Carlo Schmid and Ludwig Erhard.
In a similar survey by the tabloid Bild, readers chose Louis Ferdinand by 55.6%.
In an interview with Quick, the prince indicated that he might accept the presidency but would not relinquish his claim to the imperial or Prussian crowns.
Instead of complying with his last wish after his death, the king had been laid to rest in the Garrison Church, Potsdam next to his unloved father Frederick William I of Prussia in 1786.
Both coffins were relocated during World War II and ended up in the prince's castle in what became West Germany.
The prince had Frederick William I's coffin taken to the crypt of the Church of Peace, Potsdam because the Garrison Church had been destroyed in 1945.
In interviews with C.L. Sulzberger for the book The Fall of Eagles, Louis Ferdinand expressed a deep sense of admiration for the informal bicycle monarchy and crowned republic style favored and used by the Dutch, Belgian, and Scandinavian royal families.
Praising how vehicles carrying the King or Queen would stop and wait at traffic lights, Louis Ferdinand stated that if the House of Hohenzollern were ever restored to the German throne during his lifetime, this same informality was a quality he fully intended to emulate.
Prince Ferdinand of Hohenzollern, a member of the senior Swabian branch of the Hohenzollern dynasty, Hohenzollern-Sigmaringen, is his godson.



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
  AssignClass (c49bcb22-359b-486c-b495-246b86ff6450)
 Call ID: c49bcb22-359b-486c-b495-246b86ff6450
  Args:
    type: :Man
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (c8c71d6a-6610-4af7-af4e-ea82e50c52e5)
 Call ID: c8c71d6a-6610-4af7-af4e-ea82e50c52e5
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AddLiteral (be507ffa-0bd3-4ba2-a7ba-905907edbcd6)
 Call ID: be507ffa-0bd3-4ba2-a7ba-905907edbcd6
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1907
  AddLiteral (b3064d16-1a82-4fe5-8b58-1ac1219752ad)
 Call ID: b3064d16-1a82-4fe5-8b58-1ac1219752ad
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1994
  AssignClass (49d7a1e4-dcc1-4b00-beda-94c40abdaad8)
 Call ID: 49d7a1e4-dcc1-4b00-beda-94c40abdaad8
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (13140df4-bb76-474d-8a27-98362278fb90)
 Call ID: 13140df4-bb76-474d-8a27-98362278fb90
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (a548f6a4-3ea6-4f38-8a01-11cdc1fbbb90)
 Call ID: a548f6a4-3ea6-4f38-8a01-11cdc1fbbb90
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    target: Wilhelm_II
    relation: :hasAncestor
  AssignClass (0cba9076-7e95-446f-bdf9-eee8140d6c38)
 Call ID: 0cba9076-7e95-446f-bdf9-eee8140d6c38
  Args:
    type: :Man
    source: William_German_Crown_Prince
  AssignClass (a23f01a6-4445-4411-9d0f-0b2fdc72d0b3)
 Call ID: a23f01a6-4445-4411-9d0f-0b2fdc72d0b3
  Args:
    type: :Person
    source: William_German_Crown_Prince
  AddTriple (3c8e1890-e015-46e6-bf17-5151008b501e)
 Call ID: 3c8e1890-e015-46e6-bf17-5151008b501e
  Args:
    target: William_German_Crown_Prince
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasFather
  AssignClass (792844f4-6a6a-4562-84b4-1becfcfde42d)
 Call ID: 792844f4-6a6a-4562-84b4-1becfcfde42d
  Args:
    type: :Man
    source: Wilhelm_Prince_of_Prussia
  AssignClass (e3a9d15a-7f08-4c1a-8771-d56f97696669)
 Call ID: e3a9d15a-7f08-4c1a-8771-d56f97696669
  Args:
    type: :Person
    source: Wilhelm_Prince_of_Prussia
  AddTriple (97fabb09-1fdd-4154-97a8-1b76d32400f5)
 Call ID: 97fabb09-1fdd-4154-97a8-1b76d32400f5
  Args:
    target: Wilhelm_Prince_of_Prussia
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :isSiblingOf
  AssignClass (5f1c8014-2ee2-4c02-be0d-17839e42357a)
 Call ID: 5f1c8014-2ee2-4c02-be0d-17839e42357a
  Args:
    type: :Woman
    source: Kira_Kirillovna_of_Russia
  AssignClass (50dfc9b6-a675-4c23-88dc-f7767abfafb3)
 Call ID: 50dfc9b6-a675-4c23-88dc-f7767abfafb3
  Args:
    type: :Person
    source: Kira_Kirillovna_of_Russia
  AddTriple (89dfd781-9a51-43e5-bcf8-ceb754e6e439)
 Call ID: 89dfd781-9a51-43e5-bcf8-ceb754e6e439
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    target: Kira_Kirillovna_of_Russia
    relation: :hasRelation
  AddLiteral (5d3bbe9d-d492-40f6-b650-209d842b65aa)
 Call ID: 5d3bbe9d-d492-40f6-b650-209d842b65aa
  Args:
    literal_type: xsd:integer
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasMarriageYear
    literal_value: 1938
  AssignClass (576ef1a3-4fb9-40a6-9f8a-c012dcc85f7e)
 Call ID: 576ef1a3-4fb9-40a6-9f8a-c012dcc85f7e
  Args:
    source: Kyril_Vladimirovich
    type: :Man
  AssignClass (c4b34542-82c9-4c6c-a2dc-2d4a3ab8b4c5)
 Call ID: c4b34542-82c9-4c6c-a2dc-2d4a3ab8b4c5
  Args:
    source: Kyril_Vladimirovich
    type: :Person
  AssignClass (b5bad0e2-179c-4b35-8a3d-f416337ab25f)
 Call ID: b5bad0e2-179c-4b35-8a3d-f416337ab25f
  Args:
    type: :Woman
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (5be95a68-490f-4056-83f6-240f7a16a41a)
 Call ID: 5be95a68-490f-4056-83f6-240f7a16a41a
  Args:
    type: :Person
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddTriple (f6462561-45f8-478d-866c-20a211f7361d)
 Call ID: f6462561-45f8-478d-866c-20a211f7361d
  Args:
    relation: :hasFather
    source: Kira_Kirillovna_of_Russia
    target: Kyril_Vladimirovich
  AddTriple (7746a7a0-bb5e-4de9-ba94-18ec78625f5c)
 Call ID: 7746a7a0-bb5e-4de9-ba94-18ec78625f5c
  Args:
    relation: :hasMother
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    source: Kira_Kirillovna_of_Russia
  AssignClass (4616675c-a315-4830-9a15-6836dd51f8f5)
 Call ID: 4616675c-a315-4830-9a15-6836dd51f8f5
  Args:
    type: :Man
    source: Prince_Louis_Ferdinand_son
  AssignClass (c2f8ff81-e107-421b-a184-74912823037a)
 Call ID: c2f8ff81-e107-421b-a184-74912823037a
  Args:
    source: Prince_Louis_Ferdinand_son
    type: :Person
  AddTriple (25405b77-661d-4739-8473-3f71fc0a2d51)
 Call ID: 25405b77-661d-4739-8473-3f71fc0a2d51
  Args:
    source: Prince_Louis_Ferdinand_son
    target: Louis_Ferdinand_Prince_of_Prussia
    relation: :isSonOf
  AssignClass (c5bcaff1-1d1c-4b0c-8f54-90824fcb11b2)
 Call ID: c5bcaff1-1d1c-4b0c-8f54-90824fcb11b2
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    type: :Man
  AssignClass (5df886e1-c227-4fbc-9dfb-fb06a91a687e)
 Call ID: 5df886e1-c227-4fbc-9dfb-fb06a91a687e
  Args:
    type: :Person
    source: Georg_Friedrich_Prince_of_Prussia
  AddTriple (1c4054b2-0bd3-462b-b11c-27a34869d651)
 Call ID: 1c4054b2-0bd3-462b-b11c-27a34869d651
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    target: Prince_Louis_Ferdinand_son
    relation: :isSonOf
  AssignClass (7b372b27-5f08-46d5-b1a7-77a12035e6cb)
 Call ID: 7b372b27-5f08-46d5-b1a7-77a12035e6cb
  Args:
    source: Frederick_William_I_of_Prussia
    type: :Man
  AssignClass (ccf3456c-d466-49c1-a660-d4dca7c25be4)
 Call ID: ccf3456c-d466-49c1-a660-d4dca7c25be4
  Args:
    type: :Person
    source: Frederick_William_I_of_Prussia
  AssignClass (95e4d51f-209b-4935-b7ca-a5fde1b96ee2)
 Call ID: 95e4d51f-209b-4935-b7ca-a5fde1b96ee2
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Hohenzollern
  AssignClass (a9aba599-a246-4ad9-b3b9-02e7e4f8806d)
 Call ID: a9aba599-a246-4ad9-b3b9-02e7e4f8806d
  Args:
    source: Prince_Ferdinand_of_Hohenzollern
    type: :Person
  Finish (ab4938a4-27e3-4674-91a0-f2c10bbbe0eb)
 Call ID: ab4938a4-27e3-4674-91a0-f2c10bbbe0eb
  Args: