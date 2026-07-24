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
Princess Beatrix of Hohenlohe-Langenburg (German: Beatrix Alice Marie Melita Margarete Prinzessin zu Hohenlohe-Langenburg; 10 July 1936 – 15 November 1997) was a German princess from the House of Hohenlohe-Langenburg.
She was a niece of Prince Philip, Duke of Edinburgh, and thus a first cousin of King Charles III.
Biography

Beatrix was born on 10 July 1936 in Schwäbisch Hall to Gottfried, Hereditary Prince of Hohenlohe-Langenburg, and Princess Margarita of Greece and Denmark, the eldest sister of Prince Philip, Duke of Edinburgh.
The family was not invited to Philip's wedding to Princess Elizabeth of the United Kingdom in 1947, due to her parents' membership in the Nazi Party.
Six years later, however, Beatrix and her family were seated in the royal box at  her aunt's coronation in Westminster Abbey.
In January 1956, Beatrix and her cousin, Princess Christina of Hesse, moved to London into a flat arranged by their uncle, Prince Philip, in Dolphin Square.
Beatrix took dressmaking classes at the Royal College of Art.
While Princess Christina eventually settled in the United Kingdom, marrying Prince Andrew of Yugoslavia whom the princesses were close friends with during their stay, Beatrix returned to Germany that same year.
In 1961, Beatrix became engaged to her first cousin, Maximilian, Hereditary Prince of Baden.
Maximilian later married Archduchess Valerie of Austria (b. 1941) in 1966 and Beatrix never married.
In her later years, she served as secretary to Margaret, Princess of Hesse and by Rhine, the sister-in-law of her aunt, Princess Cecilie.
She lived in Langenburg, Germany, for most of her life.
She continued to attend family events in Britain, such as the weddings of her cousins Prince Charles (later King Charles III) and Prince Andrew in 1981 and 1986, respectively.
Beatrix died on 15 November 1997, aged 61, in the town where she was born.



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
  AssignClass (d62138a1-22c5-4549-9449-631171c18809)
 Call ID: d62138a1-22c5-4549-9449-631171c18809
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (1ff344b2-e6aa-42a5-88cc-0cc7c7fd19b4)
 Call ID: 1ff344b2-e6aa-42a5-88cc-0cc7c7fd19b4
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    type: :Person
  AddLiteral (83a563fa-601d-41b6-ab30-546a072ff33b)
 Call ID: 83a563fa-601d-41b6-ab30-546a072ff33b
  Args:
    literal_value: 1936
    source: Beatrix_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (9206fffd-3a43-4be6-8144-61677d4d49a1)
 Call ID: 9206fffd-3a43-4be6-8144-61677d4d49a1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1997
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (a8432cb5-888d-4803-9e57-f20d573204b2)
 Call ID: a8432cb5-888d-4803-9e57-f20d573204b2
  Args:
    type: :Man
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
  AssignClass (47ca74bb-3367-4ccf-9f0d-b33951c75a68)
 Call ID: 47ca74bb-3367-4ccf-9f0d-b33951c75a68
  Args:
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Person
  AssignClass (9dd9fb55-3946-4f11-8956-c753c3734846)
 Call ID: 9dd9fb55-3946-4f11-8956-c753c3734846
  Args:
    source: Margarita_of_Greece_and_Denmark
    type: :Woman
  AssignClass (f6a85f49-ed76-4fc1-9c87-0052cb3af7da)
 Call ID: f6a85f49-ed76-4fc1-9c87-0052cb3af7da
  Args:
    source: Margarita_of_Greece_and_Denmark
    type: :Person
  AddTriple (09e6cdf1-1313-4352-9493-b378c72edd0d)
 Call ID: 09e6cdf1-1313-4352-9493-b378c72edd0d
  Args:
    target: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasFather
  AddTriple (2c962dfc-e2e5-440c-ab20-69064d97f40b)
 Call ID: 2c962dfc-e2e5-440c-ab20-69064d97f40b
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    target: Margarita_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (5791d70c-e7b6-4bb1-8baa-c33c6ba73ecb)
 Call ID: 5791d70c-e7b6-4bb1-8baa-c33c6ba73ecb
  Args:
    source: Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (72c5db96-43dd-490f-b415-1e65a1257ee9)
 Call ID: 72c5db96-43dd-490f-b415-1e65a1257ee9
  Args:
    source: Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (a77112be-4ee8-4eab-85a6-9445afa2736a)
 Call ID: a77112be-4ee8-4eab-85a6-9445afa2736a
  Args:
    target: Margarita_of_Greece_and_Denmark
    source: Philip_Duke_of_Edinburgh
    relation: :isBrotherOf
  AssignClass (06b5df6b-03a4-42df-bbff-bfc9e7010348)
 Call ID: 06b5df6b-03a4-42df-bbff-bfc9e7010348
  Args:
    source: Charles_III
    type: :Man
  AssignClass (584c6550-a5d5-437d-b37c-a943302c98c5)
 Call ID: 584c6550-a5d5-437d-b37c-a943302c98c5
  Args:
    source: Charles_III
    type: :Person
  AssignClass (030e7a90-f6ee-4148-a908-7159e351f676)
 Call ID: 030e7a90-f6ee-4148-a908-7159e351f676
  Args:
    type: :Woman
    source: Christina_of_Hesse
  AssignClass (e13c7118-9ce9-4971-8adb-3b718d5e050f)
 Call ID: e13c7118-9ce9-4971-8adb-3b718d5e050f
  Args:
    type: :Person
    source: Christina_of_Hesse
  AssignClass (ba70d33c-bf66-417c-9bce-796346d511c3)
 Call ID: ba70d33c-bf66-417c-9bce-796346d511c3
  Args:
    type: :Man
    source: Andrew_of_Yugoslavia
  AssignClass (3bba1102-bc6b-4fc4-9c4a-71801e2d8bd2)
 Call ID: 3bba1102-bc6b-4fc4-9c4a-71801e2d8bd2
  Args:
    type: :Person
    source: Andrew_of_Yugoslavia
  AssignClass (412d4d6d-10fd-4bda-98e1-5b34b25e6216)
 Call ID: 412d4d6d-10fd-4bda-98e1-5b34b25e6216
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    type: :Man
  AssignClass (81585e74-dc84-4fca-b426-a6571a8dd341)
 Call ID: 81585e74-dc84-4fca-b426-a6571a8dd341
  Args:
    type: :Person
    source: Maximilian_Hereditary_Prince_of_Baden
  AssignClass (e238c2eb-0c57-4390-a14b-b68f32c0c392)
 Call ID: e238c2eb-0c57-4390-a14b-b68f32c0c392
  Args:
    type: :Woman
    source: Valerie_of_Austria
  AssignClass (dca5c4a0-54f2-45dc-8e23-f8c4ae39b1ad)
 Call ID: dca5c4a0-54f2-45dc-8e23-f8c4ae39b1ad
  Args:
    source: Valerie_of_Austria
    type: :Person
  AddLiteral (d833d443-98ba-4a7a-b512-1400824d1c6d)
 Call ID: d833d443-98ba-4a7a-b512-1400824d1c6d
  Args:
    literal_value: 1966
    source: Maximilian_Hereditary_Prince_of_Baden
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (412e38b7-8a5a-4102-a627-9555fa1d053d)
 Call ID: 412e38b7-8a5a-4102-a627-9555fa1d053d
  Args:
    relation: :hasRelation
    target: Valerie_of_Austria
    source: Maximilian_Hereditary_Prince_of_Baden
  AssignClass (93594f38-486e-4fbe-ac66-06d521df1741)
 Call ID: 93594f38-486e-4fbe-ac66-06d521df1741
  Args:
    source: Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (0e24ac2b-c3cd-4fbf-9a48-60a624ed7cbd)
 Call ID: 0e24ac2b-c3cd-4fbf-9a48-60a624ed7cbd
  Args:
    source: Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (b0d87250-51f0-4a7a-8df3-9dd838b20123)
 Call ID: b0d87250-51f0-4a7a-8df3-9dd838b20123
  Args:
    type: :Woman
    source: Cecilie_of_Greece_and_Denmark
  AssignClass (d086e8dc-c218-4527-8457-41456ec8d768)
 Call ID: d086e8dc-c218-4527-8457-41456ec8d768
  Args:
    source: Cecilie_of_Greece_and_Denmark
    type: :Person
  Finish (14bdff6f-0997-4bfd-805a-33f5fdac659e)
 Call ID: 14bdff6f-0997-4bfd-805a-33f5fdac659e
  Args: