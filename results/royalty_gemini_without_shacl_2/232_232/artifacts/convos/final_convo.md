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
  AssignClass (c18764f8-a14e-4319-b6bd-2be0f431bf0f)
 Call ID: c18764f8-a14e-4319-b6bd-2be0f431bf0f
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  AssignClass (69388202-8e3e-46de-98da-79d70ce0b635)
 Call ID: 69388202-8e3e-46de-98da-79d70ce0b635
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AddLiteral (761740c5-39dd-4c2a-9ed9-a570397bc92d)
 Call ID: 761740c5-39dd-4c2a-9ed9-a570397bc92d
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1907
    source: Louis_Ferdinand_Prince_of_Prussia
  AddLiteral (5f919cd9-f087-48e6-9762-0eabbf2e41b3)
 Call ID: 5f919cd9-f087-48e6-9762-0eabbf2e41b3
  Args:
    relation: :hasDeathYear
    literal_value: 1994
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
  AssignClass (c49a1a67-9e4a-4ab0-934b-49a0c7e26677)
 Call ID: c49a1a67-9e4a-4ab0-934b-49a0c7e26677
  Args:
    type: :Man
    source: Kaiser_Wilhelm_II
  AssignClass (f2c4e0af-ca66-4477-803d-f9005859ffd7)
 Call ID: f2c4e0af-ca66-4477-803d-f9005859ffd7
  Args:
    source: Kaiser_Wilhelm_II
    type: :Person
  AddTriple (567002c6-bb0e-4785-8f1c-7fc32ad8f0a7)
 Call ID: 567002c6-bb0e-4785-8f1c-7fc32ad8f0a7
  Args:
    relation: :hasAncestor
    target: Kaiser_Wilhelm_II
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (041a6b31-a9ca-44d0-b90b-ca183e4875a9)
 Call ID: 041a6b31-a9ca-44d0-b90b-ca183e4875a9
  Args:
    type: :Man
    source: William_German_Crown_Prince
  AssignClass (0f7f8c1d-0825-4bbd-9ec8-052801e69fad)
 Call ID: 0f7f8c1d-0825-4bbd-9ec8-052801e69fad
  Args:
    source: William_German_Crown_Prince
    type: :Person
  AddTriple (f80fdb0e-9d47-4115-8fdf-e4f6f349b823)
 Call ID: f80fdb0e-9d47-4115-8fdf-e4f6f349b823
  Args:
    relation: :hasFather
    target: William_German_Crown_Prince
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (6cd4c2e7-2d6d-4eff-84c2-2b90fcefe689)
 Call ID: 6cd4c2e7-2d6d-4eff-84c2-2b90fcefe689
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Prussia
  AssignClass (e02874e0-9e46-4882-918e-1e48bc953c77)
 Call ID: e02874e0-9e46-4882-918e-1e48bc953c77
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Prussia
  AddTriple (ac23b369-8855-43a3-96f4-305ea7fac7cd)
 Call ID: ac23b369-8855-43a3-96f4-305ea7fac7cd
  Args:
    relation: :isSiblingOf
    target: Prince_Wilhelm_of_Prussia
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (08fdd69d-430e-4d9f-a78c-cbc1b69cd9b8)
 Call ID: 08fdd69d-430e-4d9f-a78c-cbc1b69cd9b8
  Args:
    type: :Woman
    source: Kira_Kirillovna_of_Russia
  AssignClass (b9710900-2cb1-43a4-9978-9af468724657)
 Call ID: b9710900-2cb1-43a4-9978-9af468724657
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Person
  AddTriple (090b1a41-dc13-4da5-a33b-a03725185f0f)
 Call ID: 090b1a41-dc13-4da5-a33b-a03725185f0f
  Args:
    relation: :hasRelation
    source: Louis_Ferdinand_Prince_of_Prussia
    target: Kira_Kirillovna_of_Russia
  AddLiteral (7b9dc98b-999b-4b77-b8e7-75dea5f7f4b9)
 Call ID: 7b9dc98b-999b-4b77-b8e7-75dea5f7f4b9
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasMarriageYear
  AssignClass (efa0bbef-f78c-4d4e-865d-5fe67c7bee19)
 Call ID: efa0bbef-f78c-4d4e-865d-5fe67c7bee19
  Args:
    type: :Man
    source: Grand_Duke_Kyril_Vladimirovich
  AssignClass (400fa733-c08e-4fdb-9d9d-0293019bf0ea)
 Call ID: 400fa733-c08e-4fdb-9d9d-0293019bf0ea
  Args:
    type: :Person
    source: Grand_Duke_Kyril_Vladimirovich
  AssignClass (d53ff693-9af5-4056-9c49-689729d1e4d6)
 Call ID: d53ff693-9af5-4056-9c49-689729d1e4d6
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (cd3ed0e7-63a0-488f-bdb2-ba0446e3243e)
 Call ID: cd3ed0e7-63a0-488f-bdb2-ba0446e3243e
  Args:
    type: :Person
    source: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddTriple (151e494f-c122-40a7-ae0f-ed2f8841c917)
 Call ID: 151e494f-c122-40a7-ae0f-ed2f8841c917
  Args:
    relation: :hasFather
    target: Grand_Duke_Kyril_Vladimirovich
    source: Kira_Kirillovna_of_Russia
  AddTriple (8f1df55a-ff16-4141-a221-08c2ac7b8fa8)
 Call ID: 8f1df55a-ff16-4141-a221-08c2ac7b8fa8
  Args:
    target: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
    source: Kira_Kirillovna_of_Russia
    relation: :hasMother
  AssignClass (8dcb42b8-55a7-441c-94d7-21012e0bfa6b)
 Call ID: 8dcb42b8-55a7-441c-94d7-21012e0bfa6b
  Args:
    source: Prince_Louis_Ferdinand_Jr
    type: :Man
  AssignClass (01b4db30-3181-437b-b0ec-57c9c957f176)
 Call ID: 01b4db30-3181-437b-b0ec-57c9c957f176
  Args:
    source: Prince_Louis_Ferdinand_Jr
    type: :Person
  AddTriple (92711382-0ce7-4060-af57-3cdde4942c92)
 Call ID: 92711382-0ce7-4060-af57-3cdde4942c92
  Args:
    relation: :hasFather
    source: Prince_Louis_Ferdinand_Jr
    target: Louis_Ferdinand_Prince_of_Prussia
  AddLiteral (cc20b7dd-705a-4599-ab9a-5edea46d0dd4)
 Call ID: cc20b7dd-705a-4599-ab9a-5edea46d0dd4
  Args:
    relation: :hasDeathYear
    literal_value: 1977
    source: Prince_Louis_Ferdinand_Jr
    literal_type: xsd:integer
  AssignClass (16b0e22c-0dcf-41e8-b25f-40f6134a86b8)
 Call ID: 16b0e22c-0dcf-41e8-b25f-40f6134a86b8
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    type: :Man
  AssignClass (97931f7e-e43c-43f9-ba36-ebc25141974d)
 Call ID: 97931f7e-e43c-43f9-ba36-ebc25141974d
  Args:
    type: :Person
    source: Georg_Friedrich_Prince_of_Prussia
  AddTriple (430876b6-0982-486c-964f-2d8ce37902c2)
 Call ID: 430876b6-0982-486c-964f-2d8ce37902c2
  Args:
    target: Prince_Louis_Ferdinand_Jr
    source: Georg_Friedrich_Prince_of_Prussia
    relation: :hasFather
  AddTriple (ffdcaae2-d6d4-4280-ae13-e9a0c9b8fb8a)
 Call ID: ffdcaae2-d6d4-4280-ae13-e9a0c9b8fb8a
  Args:
    source: Frederick_William_I_of_Prussia
    target: Frederick_William_I_of_Prussia
    relation: :hasFather
  AssignClass (204633fd-5d1e-4489-b11f-7e4c06ea2896)
 Call ID: 204633fd-5d1e-4489-b11f-7e4c06ea2896
  Args:
    type: :Man
    source: Frederick_William_I_of_Prussia
  AssignClass (1061497a-ef3d-4a72-a9f8-14e9e63c1ef3)
 Call ID: 1061497a-ef3d-4a72-a9f8-14e9e63c1ef3
  Args:
    source: Frederick_William_I_of_Prussia
    type: :Person
  AssignClass (7ae2ab9f-31dc-48f4-98fd-ca30d8c00af3)
 Call ID: 7ae2ab9f-31dc-48f4-98fd-ca30d8c00af3
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Hohenzollern
  AssignClass (d6bee23d-c84f-467e-9726-2bce24a33723)
 Call ID: d6bee23d-c84f-467e-9726-2bce24a33723
  Args:
    source: Prince_Ferdinand_of_Hohenzollern
    type: :Person
  AddTriple (6a3b67d9-f8ed-4558-b7a3-78e646eec7ae)
 Call ID: 6a3b67d9-f8ed-4558-b7a3-78e646eec7ae
  Args:
    relation: :hasRelation
    target: Prince_Ferdinand_of_Hohenzollern
    source: Louis_Ferdinand_Prince_of_Prussia
  Finish (413b4b8f-852a-43d5-a53d-584b3aa5c1f8)
 Call ID: 413b4b8f-852a-43d5-a53d-584b3aa5c1f8
  Args: