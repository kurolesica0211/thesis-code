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
Prince Wilhelm Friedrich Franz Joseph Christian Olaf of Prussia (4 July 1906 – 26 May 1940) was the eldest child of Wilhelm, German Crown Prince, and Duchess Cecilie of Mecklenburg-Schwerin.
At his birth, he was second in line to the German throne and was expected to succeed to the throne after the deaths of his grandfather, Emperor Wilhelm II, and his father, Crown Prince Wilhelm, although both outlived him.
In any case, the German monarchy was abolished in 1918 when he was twelve.
He later enlisted to serve in the Wehrmacht and died in active service during the German invasion of France in 1940.
Early life and childhood

Wilhelm was born on 4 July 1906 at the Hohenzollern family's private summer residence, Marmorpalais, or Marble Palace, near Potsdam, where his parents were residing until their own home, Schloss Cecilienhof, could be completed.
His father was Crown Prince Wilhelm, the eldest son and heir to the German Emperor, Wilhelm II.
His mother was Duchess Cecilie of Mecklenburg-Schwerin.
Emperor Franz Joseph of Austria was one of the Prince's godfathers.
The selection of a nanny for Wilhelm and his younger brother, Louis Ferdinand (born in 1907) caused considerable distress within the family.
On his tenth birthday in 1916, Wilhelm was made a lieutenant in the 1st Guards Regiment, and was given the Order of the Black Eagle by his grandfather.
Two years later, when he was twelve, the German monarchy was abolished.
Wilhelm and his family remained in Germany, though his grandfather, the former Emperor, went into exile in the Netherlands.
The former Crown Prince and his family remained in Potsdam, where Wilhelm and his younger brothers attended the local gymnasium.
After graduating from secondary school, Wilhelm went on to study at the Universities of Königsberg, Munich and Bonn.
In 1926, while a student at the University of Bonn, Wilhelm joined the Borussia Corps, a student organization of which his father, grandfather, and other members of the Prussian royal family were members.
Marriage and children

While a student at Bonn, Wilhelm fell in love with a fellow student, Dorothea von Salviati (10 September 1907 – 7 May 1972).
Wilhelm's grandfather did not approve of the marriage of the heir apparent in line to the German throne to a member of the minor nobility.
Wilhelm told his grandson, "Remember, there is every possible form of horse.
However, Wilhelm was determined to marry Dorothea.
Wilhelm and Dorothea married on 3 June 1933 in Bonn.
In 1940, the ex-Emperor recognized the marriage as dynastic and the girls were accorded the style of Princesses of Prussia (although their father was not restored to his former place in the putative line of succession, his renunciation of his rights remaining valid):


Military services

During the Weimar Republic, Wilhelm inadvertently caused a public scandal by attending Army manoeuvres in the uniform of the old Imperial First Foot Guards without first seeking government approval.
The Oster conspiracy of 1938 sought to restore Wilhelm to the throne.
At the beginning of World War II, Wilhelm was among a number of princes from the former German monarchies who enlisted to serve in the Wehrmacht, the unified armed forces of Germany.
Death and reaction

In May 1940, Wilhelm took part in the invasion of France.
Shortly after Wilhelm's death, a decree known as the Prinzenerlaß, or Prince's Decree, was issued, barring all members of the former German royal houses from service in the Wehrmacht.



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
  AssignClass (a8fd56b0-b510-4dfa-9363-97e3b506dc47)
 Call ID: a8fd56b0-b510-4dfa-9363-97e3b506dc47
  Args:
    type: :Person
    source: Wilhelm_of_Prussia
  AssignClass (b4987a79-d017-4b56-aeae-ba72ce8d7af7)
 Call ID: b4987a79-d017-4b56-aeae-ba72ce8d7af7
  Args:
    source: Wilhelm_of_Prussia
    type: :Man
  AddLiteral (377f9c64-0078-4712-80de-aa24c56861fc)
 Call ID: 377f9c64-0078-4712-80de-aa24c56861fc
  Args:
    literal_value: 1906
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Wilhelm_of_Prussia
  AddLiteral (5df75eb9-41b6-4adc-b4eb-88998e6fca4c)
 Call ID: 5df75eb9-41b6-4adc-b4eb-88998e6fca4c
  Args:
    literal_value: 1940
    source: Wilhelm_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f107a83e-0638-4bf8-983a-a62d0b848843)
 Call ID: f107a83e-0638-4bf8-983a-a62d0b848843
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AssignClass (55b47016-d231-413a-b303-8e6e8e747fe5)
 Call ID: 55b47016-d231-413a-b303-8e6e8e747fe5
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Man
  AssignClass (30a6d52b-ea81-4030-b232-f4d22a557326)
 Call ID: 30a6d52b-ea81-4030-b232-f4d22a557326
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (5fe0c39d-9f4a-4172-b3d7-e675b6cd4d37)
 Call ID: 5fe0c39d-9f4a-4172-b3d7-e675b6cd4d37
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (2bee3707-20e7-4eef-94c5-d24fae67d6dd)
 Call ID: 2bee3707-20e7-4eef-94c5-d24fae67d6dd
  Args:
    target: Wilhelm_German_Crown_Prince
    source: Wilhelm_of_Prussia
    relation: :hasFather
  AddTriple (12ae7a6a-86c0-4748-853a-caa46e9c0dd7)
 Call ID: 12ae7a6a-86c0-4748-853a-caa46e9c0dd7
  Args:
    source: Wilhelm_of_Prussia
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (8b2ac263-bff4-465a-b698-a6530158cd83)
 Call ID: 8b2ac263-bff4-465a-b698-a6530158cd83
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (1985e02c-a15e-45c4-ac22-5bbbc7e29c6e)
 Call ID: 1985e02c-a15e-45c4-ac22-5bbbc7e29c6e
  Args:
    type: :Man
    source: Wilhelm_II
  AddTriple (b680101d-3cab-480e-96b5-0c716ecd6a96)
 Call ID: b680101d-3cab-480e-96b5-0c716ecd6a96
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Wilhelm_German_Crown_Prince
  AssignClass (ab548f29-4483-4ef5-96e8-4450454f2279)
 Call ID: ab548f29-4483-4ef5-96e8-4450454f2279
  Args:
    source: Louis_Ferdinand
    type: :Person
  AssignClass (747936f4-f9b4-4a8f-8f84-6681e25119e5)
 Call ID: 747936f4-f9b4-4a8f-8f84-6681e25119e5
  Args:
    source: Louis_Ferdinand
    type: :Man
  AddTriple (c4edd646-4fc8-46e8-bd9d-6e784510d31b)
 Call ID: c4edd646-4fc8-46e8-bd9d-6e784510d31b
  Args:
    source: Louis_Ferdinand
    relation: :isBrotherOf
    target: Wilhelm_of_Prussia
  AssignClass (ee05a04e-55e7-4615-9bc1-94a7c77f5d98)
 Call ID: ee05a04e-55e7-4615-9bc1-94a7c77f5d98
  Args:
    source: Dorothea_von_Salviati
    type: :Person
  AssignClass (e8195676-0a4c-4818-983e-18f5e0afef0d)
 Call ID: e8195676-0a4c-4818-983e-18f5e0afef0d
  Args:
    source: Dorothea_von_Salviati
    type: :Woman
  AddLiteral (ef8864a9-d3a0-46eb-9a19-bb0aa740f476)
 Call ID: ef8864a9-d3a0-46eb-9a19-bb0aa740f476
  Args:
    source: Wilhelm_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1933
  AddTriple (59d28b50-f9ac-40f4-8417-a1d5e886f5ab)
 Call ID: 59d28b50-f9ac-40f4-8417-a1d5e886f5ab
  Args:
    source: Wilhelm_of_Prussia
    relation: :hasRelation
    target: Dorothea_von_Salviati
  Finish (162733d0-864e-4c62-b1ce-bb4036d6cd91)
 Call ID: 162733d0-864e-4c62-b1ce-bb4036d6cd91
  Args: