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
  AssignClass (9bf346be-2add-4b2d-a221-5a7a67ec0f3c)
 Call ID: 9bf346be-2add-4b2d-a221-5a7a67ec0f3c
  Args:
    type: :Woman
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (7d048314-aaf5-4b6b-a293-f5439b2925b9)
 Call ID: 7d048314-aaf5-4b6b-a293-f5439b2925b9
  Args:
    type: :Person
    source: Beatrix_of_Hohenlohe-Langenburg
  AddLiteral (0d988868-3c3f-4003-b5e3-605de855efee)
 Call ID: 0d988868-3c3f-4003-b5e3-605de855efee
  Args:
    literal_value: 1936
    literal_type: xsd:integer
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasBirthYear
  AddLiteral (d4afe175-5e65-4b64-8fa2-4072a9465725)
 Call ID: d4afe175-5e65-4b64-8fa2-4072a9465725
  Args:
    literal_value: 1997
    literal_type: xsd:integer
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasDeathYear
  AssignClass (14f033d7-71ce-4f51-87fa-31d3158b1bf4)
 Call ID: 14f033d7-71ce-4f51-87fa-31d3158b1bf4
  Args:
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (1ace6fdd-5e93-472e-8253-73bdbc4b2e73)
 Call ID: 1ace6fdd-5e93-472e-8253-73bdbc4b2e73
  Args:
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Person
  AssignClass (3990932c-5260-4f80-bca1-16e99843556f)
 Call ID: 3990932c-5260-4f80-bca1-16e99843556f
  Args:
    source: Margarita_of_Greece_and_Denmark
    type: :Woman
  AssignClass (af79c9b6-1b4e-4cc8-9d1c-ed347cedae0e)
 Call ID: af79c9b6-1b4e-4cc8-9d1c-ed347cedae0e
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AddTriple (7bd87903-1f35-4f99-b329-00c158c72e40)
 Call ID: 7bd87903-1f35-4f99-b329-00c158c72e40
  Args:
    target: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    relation: :hasFather
    source: Beatrix_of_Hohenlohe-Langenburg
  AddTriple (6e21d1d6-e11a-41ee-8cfb-29fb44830222)
 Call ID: 6e21d1d6-e11a-41ee-8cfb-29fb44830222
  Args:
    target: Margarita_of_Greece_and_Denmark
    relation: :hasMother
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (e3f8853a-e81a-4175-8577-1e5df10e5f99)
 Call ID: e3f8853a-e81a-4175-8577-1e5df10e5f99
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (52abb1da-5e0f-4253-9ecf-11026e174351)
 Call ID: 52abb1da-5e0f-4253-9ecf-11026e174351
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (7431239e-3c17-4581-b939-ce9c769378ed)
 Call ID: 7431239e-3c17-4581-b939-ce9c769378ed
  Args:
    relation: :isBrotherOf
    target: Margarita_of_Greece_and_Denmark
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (7f812655-3fe0-49cf-b68e-9d7925f9333b)
 Call ID: 7f812655-3fe0-49cf-b68e-9d7925f9333b
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (19e0f5cc-dc03-45bc-bbe4-96e50986c2b8)
 Call ID: 19e0f5cc-dc03-45bc-bbe4-96e50986c2b8
  Args:
    source: King_Charles_III
    type: :Person
  AssignClass (9be0cc6f-3052-409f-b608-fa2155a54388)
 Call ID: 9be0cc6f-3052-409f-b608-fa2155a54388
  Args:
    type: :Woman
    source: Princess_Christina_of_Hesse
  AssignClass (aa1651c0-0956-4044-af55-38a3fa1b4d09)
 Call ID: aa1651c0-0956-4044-af55-38a3fa1b4d09
  Args:
    type: :Person
    source: Princess_Christina_of_Hesse
  AssignClass (47046115-bde7-4821-8f05-27d37faafda6)
 Call ID: 47046115-bde7-4821-8f05-27d37faafda6
  Args:
    source: Prince_Andrew_of_Yugoslavia
    type: :Man
  AssignClass (d028c62b-eead-4256-b226-8331f856771f)
 Call ID: d028c62b-eead-4256-b226-8331f856771f
  Args:
    source: Prince_Andrew_of_Yugoslavia
    type: :Person
  AssignClass (48a9c110-5b47-44f6-a11c-3cf62c1b6bfe)
 Call ID: 48a9c110-5b47-44f6-a11c-3cf62c1b6bfe
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    type: :Man
  AssignClass (492e0531-d35e-4790-8f94-b470b0b420c0)
 Call ID: 492e0531-d35e-4790-8f94-b470b0b420c0
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    type: :Person
  AssignClass (29a33112-cbb6-4475-aa83-2ee22726ebb1)
 Call ID: 29a33112-cbb6-4475-aa83-2ee22726ebb1
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (c589f512-066a-4a4e-82d6-dfa642b9455b)
 Call ID: c589f512-066a-4a4e-82d6-dfa642b9455b
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Person
  AddLiteral (5bd00b42-c4e2-4947-9c16-ac35f6278c0a)
 Call ID: 5bd00b42-c4e2-4947-9c16-ac35f6278c0a
  Args:
    relation: :hasMarriageYear
    source: Maximilian_Hereditary_Prince_of_Baden
    literal_type: xsd:integer
    literal_value: 1966
  AssignClass (e211a20b-4be5-4366-9e65-635a2578936e)
 Call ID: e211a20b-4be5-4366-9e65-635a2578936e
  Args:
    source: Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (76f6bc1e-fca2-4609-9a3a-116dcb548e05)
 Call ID: 76f6bc1e-fca2-4609-9a3a-116dcb548e05
  Args:
    source: Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (02ee7026-0b45-4b36-abfd-50fa7ed5c24b)
 Call ID: 02ee7026-0b45-4b36-abfd-50fa7ed5c24b
  Args:
    type: :Woman
    source: Princess_Cecilie
  AssignClass (534e5211-9466-42ab-b872-73c0e3b1a4ca)
 Call ID: 534e5211-9466-42ab-b872-73c0e3b1a4ca
  Args:
    type: :Person
    source: Princess_Cecilie
  Finish (a5fe7af7-270e-4cc0-a7b4-f1f2276fe221)
 Call ID: a5fe7af7-270e-4cc0-a7b4-f1f2276fe221
  Args: