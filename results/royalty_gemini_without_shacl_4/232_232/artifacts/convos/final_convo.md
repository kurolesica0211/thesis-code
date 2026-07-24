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
  AssignClass (138672a9-fe94-4368-ae13-e26a42cc2c7a)
 Call ID: 138672a9-fe94-4368-ae13-e26a42cc2c7a
  Args:
    type: :Man
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (bf0b7a4e-207d-4225-97d2-3dd5958cb053)
 Call ID: bf0b7a4e-207d-4225-97d2-3dd5958cb053
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AddLiteral (a53ebfd6-362e-4d27-867a-baa8aa21effb)
 Call ID: a53ebfd6-362e-4d27-867a-baa8aa21effb
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_value: 1907
  AddLiteral (0f8c6d6a-ce48-449c-81f0-191c1773bd82)
 Call ID: 0f8c6d6a-ce48-449c-81f0-191c1773bd82
  Args:
    relation: :hasDeathYear
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
    literal_value: 1994
  AssignClass (75fec5d7-a47e-47b9-92d3-de43cd5dbeb9)
 Call ID: 75fec5d7-a47e-47b9-92d3-de43cd5dbeb9
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (63b1c83c-c4fe-40fd-9565-1561d3eee21c)
 Call ID: 63b1c83c-c4fe-40fd-9565-1561d3eee21c
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (bf9bdf3a-1c38-4fe7-b35e-69af7950b3c6)
 Call ID: bf9bdf3a-1c38-4fe7-b35e-69af7950b3c6
  Args:
    target: Louis_Ferdinand_Prince_of_Prussia
    relation: :isAncestorOf
    source: Wilhelm_II
  AssignClass (51fe6467-2167-4a6d-adfa-84d86d9771ed)
 Call ID: 51fe6467-2167-4a6d-adfa-84d86d9771ed
  Args:
    type: :Man
    source: William_German_Crown_Prince
  AssignClass (c18dfd57-76b2-405b-9d8f-1332d8197ac9)
 Call ID: c18dfd57-76b2-405b-9d8f-1332d8197ac9
  Args:
    type: :Person
    source: William_German_Crown_Prince
  AddTriple (936777de-3bd5-47e6-a62f-2e7c830080a5)
 Call ID: 936777de-3bd5-47e6-a62f-2e7c830080a5
  Args:
    target: Louis_Ferdinand_Prince_of_Prussia
    relation: :isFatherOf
    source: William_German_Crown_Prince
  AssignClass (df419220-80ee-4ba8-a6db-146c37489c67)
 Call ID: df419220-80ee-4ba8-a6db-146c37489c67
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Prussia
  AssignClass (f6eb5c92-d839-40eb-8142-14db9d9f5512)
 Call ID: f6eb5c92-d839-40eb-8142-14db9d9f5512
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Prussia
  AddTriple (81cd4c6d-e62c-48c5-a294-d12f93b82aa4)
 Call ID: 81cd4c6d-e62c-48c5-a294-d12f93b82aa4
  Args:
    relation: :isBrotherOf
    target: Louis_Ferdinand_Prince_of_Prussia
    source: Prince_Wilhelm_of_Prussia
  AssignClass (80ef2f69-d4bc-430f-a6b9-7902d1fd3087)
 Call ID: 80ef2f69-d4bc-430f-a6b9-7902d1fd3087
  Args:
    source: Kira_Kirillovna
    type: :Woman
  AssignClass (0be956fe-c204-4858-a0f8-249c601667e4)
 Call ID: 0be956fe-c204-4858-a0f8-249c601667e4
  Args:
    source: Kira_Kirillovna
    type: :Person
  AddTriple (57545b94-ec42-4deb-bbad-dacaaab79d41)
 Call ID: 57545b94-ec42-4deb-bbad-dacaaab79d41
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    target: Kira_Kirillovna
    relation: :hasRelation
  AddLiteral (c12e323d-7570-4e0c-9049-fafaf92fcea1)
 Call ID: c12e323d-7570-4e0c-9049-fafaf92fcea1
  Args:
    literal_type: xsd:integer
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_value: 1938
    relation: :hasMarriageYear
  AssignClass (59f3085b-f397-41c7-ab5e-84be16a51450)
 Call ID: 59f3085b-f397-41c7-ab5e-84be16a51450
  Args:
    source: Grand_Duke_Kyril_Vladimirovich
    type: :Man
  AssignClass (a428ae48-af49-420b-84e1-267709dfcddf)
 Call ID: a428ae48-af49-420b-84e1-267709dfcddf
  Args:
    type: :Person
    source: Grand_Duke_Kyril_Vladimirovich
  AssignClass (d943bcb3-7134-428f-9384-d1b6e18768e9)
 Call ID: d943bcb3-7134-428f-9384-d1b6e18768e9
  Args:
    source: Princess_Victoria_Melita
    type: :Woman
  AssignClass (34e820c5-8b76-4406-ae98-cf3953543f2f)
 Call ID: 34e820c5-8b76-4406-ae98-cf3953543f2f
  Args:
    type: :Person
    source: Princess_Victoria_Melita
  AddTriple (d0bcacdd-af8e-4840-8d06-de66fd313904)
 Call ID: d0bcacdd-af8e-4840-8d06-de66fd313904
  Args:
    source: Grand_Duke_Kyril_Vladimirovich
    relation: :isFatherOf
    target: Kira_Kirillovna
  AddTriple (2dd57d2c-d1e2-439c-8223-c1a5145b5105)
 Call ID: 2dd57d2c-d1e2-439c-8223-c1a5145b5105
  Args:
    source: Princess_Victoria_Melita
    relation: :isMotherOf
    target: Kira_Kirillovna
  AssignClass (f51d9303-cd41-43ca-94e5-3ae7e8fa6b2e)
 Call ID: f51d9303-cd41-43ca-94e5-3ae7e8fa6b2e
  Args:
    type: :Man
    source: Prince_Louis_Ferdinand_Jr
  AssignClass (fcb553d1-823a-4e33-a152-c93dcc95f6c6)
 Call ID: fcb553d1-823a-4e33-a152-c93dcc95f6c6
  Args:
    type: :Person
    source: Prince_Louis_Ferdinand_Jr
  AddTriple (e891d675-5fb4-4a3f-b2e9-ce4903f7438f)
 Call ID: e891d675-5fb4-4a3f-b2e9-ce4903f7438f
  Args:
    source: Prince_Louis_Ferdinand_Jr
    target: Louis_Ferdinand_Prince_of_Prussia
    relation: :isSonOf
  AssignClass (85b7aec7-6876-4b56-8b46-954520bd0a5a)
 Call ID: 85b7aec7-6876-4b56-8b46-954520bd0a5a
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    type: :Man
  AssignClass (765f200d-952e-4e11-9e34-f8f21170d684)
 Call ID: 765f200d-952e-4e11-9e34-f8f21170d684
  Args:
    type: :Person
    source: Georg_Friedrich_Prince_of_Prussia
  AddTriple (8e13b936-77d2-46f4-9689-8782136e700f)
 Call ID: 8e13b936-77d2-46f4-9689-8782136e700f
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    relation: :isSonOf
    target: Prince_Louis_Ferdinand_Jr
  AssignClass (ab5bfee0-215f-4c56-a49b-3e06e655d49a)
 Call ID: ab5bfee0-215f-4c56-a49b-3e06e655d49a
  Args:
    type: :Man
    source: Frederick_William_I_of_Prussia
  AssignClass (727dc506-ff81-40ba-a054-777190f270ff)
 Call ID: 727dc506-ff81-40ba-a054-777190f270ff
  Args:
    type: :Person
    source: Frederick_William_I_of_Prussia
  AssignClass (109d2efb-bbb6-4fd5-84bd-02bed4f63985)
 Call ID: 109d2efb-bbb6-4fd5-84bd-02bed4f63985
  Args:
    source: Prince_Ferdinand_of_Hohenzollern
    type: :Man
  AssignClass (993dae79-016e-4d3e-b975-d10ad1b3523d)
 Call ID: 993dae79-016e-4d3e-b975-d10ad1b3523d
  Args:
    type: :Person
    source: Prince_Ferdinand_of_Hohenzollern
  Finish (dd383072-6710-41c3-8f73-bab775e69a5a)
 Call ID: dd383072-6710-41c3-8f73-bab775e69a5a
  Args: