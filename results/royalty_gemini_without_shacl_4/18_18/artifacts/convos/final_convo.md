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
Maria de la Esperanza of Bourbon-Two Sicilies (María de la Esperanza Amalia Raniera María Rosario Luisa Gonzaga de Borbón-Dos Sicilias y Orleáns; 14 June 1914 – 8 August 2005) was a member of the House of Bourbon-Two Sicilies.
By marriage, she became the Princess of Orléans-Braganza and the consort of Prince Pedro Gastão of Orléans-Braganza, the head of the Petrópolis branch of the Brazilian Imperial Family.
She was also the maternal aunt of King Juan Carlos I of Spain.
Early life

Princess Maria de la Esperanza was born in Madrid during the period when her family was settled in Spain.
Her father, Prince Carlos of Bourbon-Two Sicilies, had renounced his rights to the throne of the Two Sicilies to become an Infante of Spain upon his marriage to the Princess of Asturias.
Her mother, Princess Louise of Orléans, was the daughter of Philippe, Count of Paris, the Orléanist pretender to the French throne.
Her sister, Princess María de las Mercedes, married Infante Juan, Count of Barcelona, and became the mother of King Juan Carlos I. Following the proclamation of the Second Spanish Republic in 1931, the family went into exile, primarily residing in France and Italy.
Marriage and issue

On 18 December 1944, Maria de la Esperanza married her third cousin, Prince Pedro Gastão of Orléans-Braganza, in Seville, Spain.
Pedro Gastão was the son of Prince Pedro de Alcântara of Orléans-Braganza and a claimant to the defunct Brazilian throne as head of the Petrópolis branch.
The couple had six children:


Later life

The Princess spent the majority of her life at the family estate in Villamanrique de la Condesa, near Seville.
She remained a respected figure within European royalty, often attending major dynastic events in Spain alongside her nephew, King Juan Carlos I.


She died on 8 August 2005, aged 91.
Her funeral was attended by the Spanish Royal Family, including King Juan Carlos and Queen Sofía, reflecting her status as a beloved member of the extended dynasty.



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
  AssignClass (af1f843b-1196-4a45-a919-f548d64aa2d3)
 Call ID: af1f843b-1196-4a45-a919-f548d64aa2d3
  Args:
    type: :Woman
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (464f9854-2bdb-48ee-b4d5-aaa157acc086)
 Call ID: 464f9854-2bdb-48ee-b4d5-aaa157acc086
  Args:
    literal_value: 1914
    relation: :hasBirthYear
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (87094a7a-e4cc-463e-b65f-48729f560fb8)
 Call ID: 87094a7a-e4cc-463e-b65f-48729f560fb8
  Args:
    literal_type: xsd:integer
    literal_value: 2005
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
  AssignClass (8c3d604c-8450-407c-8c09-8cae590a0dbe)
 Call ID: 8c3d604c-8450-407c-8c09-8cae590a0dbe
  Args:
    type: :Man
    source: :Prince_Carlos_of_Bourbon-Two_Sicilies
  AddTriple (818821e6-73e6-4fb2-8408-1ba3b71836b5)
 Call ID: 818821e6-73e6-4fb2-8408-1ba3b71836b5
  Args:
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: :Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (cee86a6e-c0e5-460c-8cd2-540491bb4b14)
 Call ID: cee86a6e-c0e5-460c-8cd2-540491bb4b14
  Args:
    source: :Princess_Louise_of_Orleans
    type: :Woman
  AddTriple (37fc5462-dfa6-48b4-9bd7-103a8b073116)
 Call ID: 37fc5462-dfa6-48b4-9bd7-103a8b073116
  Args:
    relation: :hasMother
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: :Princess_Louise_of_Orleans
  AssignClass (ae27dd28-b014-4321-88dc-3a96778812d2)
 Call ID: ae27dd28-b014-4321-88dc-3a96778812d2
  Args:
    source: :Philippe_Count_of_Paris
    type: :Man
  AddTriple (a7f39c80-79dd-4622-b095-43cc214bbb59)
 Call ID: a7f39c80-79dd-4622-b095-43cc214bbb59
  Args:
    target: :Princess_Louise_of_Orleans
    source: :Philippe_Count_of_Paris
    relation: :isFatherOf
  AssignClass (020bafd9-dfb0-45e4-a376-2af7cb0c6426)
 Call ID: 020bafd9-dfb0-45e4-a376-2af7cb0c6426
  Args:
    source: :Princess_Maria_de_las_Mercedes
    type: :Woman
  AddTriple (a3fd674e-8936-4fae-b329-0b6c8212ca4f)
 Call ID: a3fd674e-8936-4fae-b329-0b6c8212ca4f
  Args:
    relation: :hasSister
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: :Princess_Maria_de_las_Mercedes
  AssignClass (29d780f2-44dc-48dc-942f-faab695b99d6)
 Call ID: 29d780f2-44dc-48dc-942f-faab695b99d6
  Args:
    type: :Man
    source: :Infante_Juan_Count_of_Barcelona
  AddTriple (4f9c21a3-b68d-41aa-818b-87a091f83bc1)
 Call ID: 4f9c21a3-b68d-41aa-818b-87a091f83bc1
  Args:
    source: :Princess_Maria_de_las_Mercedes
    relation: :isMotherOf
    target: :King_Juan_Carlos_I
  AddTriple (60598a15-6af7-47e4-91f8-aae2ec60ee7c)
 Call ID: 60598a15-6af7-47e4-91f8-aae2ec60ee7c
  Args:
    target: :King_Juan_Carlos_I
    relation: :isFatherOf
    source: :Infante_Juan_Count_of_Barcelona
  AssignClass (c8070b72-c72a-4da2-baa8-7317a006696e)
 Call ID: c8070b72-c72a-4da2-baa8-7317a006696e
  Args:
    source: :King_Juan_Carlos_I
    type: :Man
  AddTriple (253bfeb4-8e06-4f2a-af10-54b8c9e869e2)
 Call ID: 253bfeb4-8e06-4f2a-af10-54b8c9e869e2
  Args:
    target: :King_Juan_Carlos_I
    relation: :isAuntOf
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (cac271e2-c547-4769-89cc-2af534f86211)
 Call ID: cac271e2-c547-4769-89cc-2af534f86211
  Args:
    type: :Man
    source: :Prince_Pedro_Gastao_of_Orleans-Braganza
  AddTriple (5aedd0cc-de6b-42c5-b410-034a63e39440)
 Call ID: 5aedd0cc-de6b-42c5-b410-034a63e39440
  Args:
    target: :Prince_Pedro_Gastao_of_Orleans-Braganza
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (66ae4d9c-e736-4b6d-b037-6c011edece34)
 Call ID: 66ae4d9c-e736-4b6d-b037-6c011edece34
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_value: 1944
  AssignClass (6f1d68af-fd38-42ef-ab34-cce32375920c)
 Call ID: 6f1d68af-fd38-42ef-ab34-cce32375920c
  Args:
    source: :Prince_Pedro_de_Alcantara_of_Orleans-Braganza
    type: :Man
  AddTriple (2c131923-a352-4857-b6a9-f09451d77f1e)
 Call ID: 2c131923-a352-4857-b6a9-f09451d77f1e
  Args:
    source: :Prince_Pedro_Gastao_of_Orleans-Braganza
    relation: :hasFather
    target: :Prince_Pedro_de_Alcantara_of_Orleans-Braganza
  Finish (281f15d0-bda2-4b77-b913-393e973b41df)
 Call ID: 281f15d0-bda2-4b77-b913-393e973b41df
  Args: