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
Princess Margarita of Baden (Margarete Alice Thyra Viktoria Marie Louise Scholastica; 14 July 1932 – 15 January 2013) was the only daughter of Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark.
She was the eldest surviving cousin of King Charles III and eldest surviving niece of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
Early life

Margarita was born on 14 July 1932 at Schloss Salem, Germany, and grew up there.
She was the eldest child and only daughter of Berthold, Margrave of Baden, who ran a school jointly with Kurt Hahn, and Princess Theodora of Greece and Denmark, older sister of Prince Philip, Duke of Edinburgh.
Margarita was the first great-great-great-granddaughter of Queen Victoria.
She came to live in London in 1948, and trained as a nurse at St Thomas' Hospital.
During this time, she was often seen with her cousins Princess Christina of Hesse and Princess Beatrix of Hohenlohe-Langenburg.
Beatrix was briefly engaged to Margarita's brother Prince Maximilian, and Christina became Margarita's future sister-in-law by marrying Prince Andrew of Yugoslavia.
Also during this time, Margarita attended the 1953 coronation of her aunt, Queen Elizabeth II.
While in London, she met Prince Tomislav, a member of the exiled Yugoslav royal family as a younger brother of the former King Peter II of Yugoslavia.
Tomislav was a third cousin of Margarita's mother; both were great-great-grandchildren of Queen Victoria and Prince Albert.
Margarita and Tomislav became engaged on 2 January 1956.
She took part in the ship tour organized by King Paul of Greece and Queen Frederica in 1954, which became known as the "Cruise of the Kings" and was attended by over 100 royals from all over Europe.
Marriage

On 5 June 1957 Margarita married Prince Tomislav of Yugoslavia, younger brother of the former King Peter II of Yugoslavia, in a civil ceremony in Salem followed by Lutheran and Serbian Orthodox church services on 6 June.
Prince Philip, Duke of Edinburgh (her maternal uncle), and King Simeon of Bulgaria were among the guests.
Later years

Margarita was a champion of Serbian charities and was also president of the Convent of Martha and Mary in Moscow.
Margarita died on 15 January 2013 in Farnham, Surrey, after a long illness.
Her uncle the Duke of Edinburgh, Queen Anne-Marie of Greece, and her nephew Alexander, Crown Prince of Yugoslavia, were among the mourners.
Margarita was buried in the family cemetery at Stefansfeld near Baden, Germany, on 28 January 2013.



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
  AssignClass (260967fd-9235-4f67-b78a-53fa1cd6fd75)
 Call ID: 260967fd-9235-4f67-b78a-53fa1cd6fd75
  Args:
    type: :Woman
    source: :Margarita_of_Baden
  AssignClass (37a1ace5-1041-47c0-83be-b31e84ea0857)
 Call ID: 37a1ace5-1041-47c0-83be-b31e84ea0857
  Args:
    type: :Person
    source: :Margarita_of_Baden
  AddLiteral (de3d38a0-24a1-4fce-af9c-d8e00d93d083)
 Call ID: de3d38a0-24a1-4fce-af9c-d8e00d93d083
  Args:
    relation: :hasBirthYear
    literal_value: 1932
    source: :Margarita_of_Baden
    literal_type: xsd:integer
  AddLiteral (270096eb-56b6-4ae5-9fd8-d2acbf9b23c3)
 Call ID: 270096eb-56b6-4ae5-9fd8-d2acbf9b23c3
  Args:
    source: :Margarita_of_Baden
    literal_type: xsd:integer
    literal_value: 2013
    relation: :hasDeathYear
  AssignClass (250593c0-93ad-4503-9f20-649a957dfdc1)
 Call ID: 250593c0-93ad-4503-9f20-649a957dfdc1
  Args:
    source: :Berthold_Margrave_of_Baden
    type: :Man
  AssignClass (c37f8ded-8c83-4c22-b9be-02800a85ff70)
 Call ID: c37f8ded-8c83-4c22-b9be-02800a85ff70
  Args:
    source: :Berthold_Margrave_of_Baden
    type: :Person
  AssignClass (8212bd4e-adbe-4118-be4d-87e40be01396)
 Call ID: 8212bd4e-adbe-4118-be4d-87e40be01396
  Args:
    source: :Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (f4c864c9-5d7f-47b9-b2e8-48452b4b030e)
 Call ID: f4c864c9-5d7f-47b9-b2e8-48452b4b030e
  Args:
    type: :Person
    source: :Princess_Theodora_of_Greece_and_Denmark
  AddTriple (6cb7bc28-b37c-4bd5-8e52-fa9ad2ebc06a)
 Call ID: 6cb7bc28-b37c-4bd5-8e52-fa9ad2ebc06a
  Args:
    relation: :hasFather
    target: :Berthold_Margrave_of_Baden
    source: :Margarita_of_Baden
  AddTriple (a7548331-56dd-4b04-87aa-68fbd4e3bf4c)
 Call ID: a7548331-56dd-4b04-87aa-68fbd4e3bf4c
  Args:
    target: :Princess_Theodora_of_Greece_and_Denmark
    source: :Margarita_of_Baden
    relation: :hasMother
  AssignClass (b15ab197-9693-4e9f-916a-48a4d058a6fd)
 Call ID: b15ab197-9693-4e9f-916a-48a4d058a6fd
  Args:
    source: :Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (e5550b4b-bb08-4d29-b479-2a94607ed04b)
 Call ID: e5550b4b-bb08-4d29-b479-2a94607ed04b
  Args:
    type: :Person
    source: :Prince_Philip_Duke_of_Edinburgh
  AddTriple (372794b5-2e0a-462e-adfc-5ff4c6bc2a7f)
 Call ID: 372794b5-2e0a-462e-adfc-5ff4c6bc2a7f
  Args:
    relation: :isBrotherOf
    target: :Princess_Theodora_of_Greece_and_Denmark
    source: :Prince_Philip_Duke_of_Edinburgh
  AssignClass (7c0925b9-530c-460d-85b5-cc8311001be1)
 Call ID: 7c0925b9-530c-460d-85b5-cc8311001be1
  Args:
    source: :Prince_Maximilian
    type: :Man
  AssignClass (ab297d2e-8545-460c-8a3c-3e517f156cb2)
 Call ID: ab297d2e-8545-460c-8a3c-3e517f156cb2
  Args:
    type: :Person
    source: :Prince_Maximilian
  AddTriple (1b0aa943-fa53-4b56-8cbf-4473752a82f1)
 Call ID: 1b0aa943-fa53-4b56-8cbf-4473752a82f1
  Args:
    source: :Margarita_of_Baden
    target: :Prince_Maximilian
    relation: :hasBrother
  AssignClass (61ddb608-a5c6-4e56-8440-db6903b67b3c)
 Call ID: 61ddb608-a5c6-4e56-8440-db6903b67b3c
  Args:
    source: :Prince_Tomislav_of_Yugoslavia
    type: :Man
  AssignClass (dbcfb85a-6c3a-4af0-a38f-b69b65377250)
 Call ID: dbcfb85a-6c3a-4af0-a38f-b69b65377250
  Args:
    source: :Prince_Tomislav_of_Yugoslavia
    type: :Person
  AddLiteral (ce5a379c-e2e7-43e4-9d19-b2923b8fe637)
 Call ID: ce5a379c-e2e7-43e4-9d19-b2923b8fe637
  Args:
    relation: :hasMarriageYear
    literal_value: 1957
    source: :Margarita_of_Baden
    literal_type: xsd:integer
  AddTriple (7da72d36-c873-4e09-aebc-11caa5895486)
 Call ID: 7da72d36-c873-4e09-aebc-11caa5895486
  Args:
    relation: :hasRelation
    target: :Prince_Tomislav_of_Yugoslavia
    source: :Margarita_of_Baden
  AssignClass (daba239d-2134-4c99-9ff6-64307b63c6cd)
 Call ID: daba239d-2134-4c99-9ff6-64307b63c6cd
  Args:
    type: :Man
    source: :King_Peter_II_of_Yugoslavia
  AssignClass (606de7bc-590e-4e9a-8146-47adb2deeefd)
 Call ID: 606de7bc-590e-4e9a-8146-47adb2deeefd
  Args:
    type: :Person
    source: :King_Peter_II_of_Yugoslavia
  AddTriple (a09d4f96-2fa7-45dd-97cc-369d750005d2)
 Call ID: a09d4f96-2fa7-45dd-97cc-369d750005d2
  Args:
    relation: :isBrotherOf
    target: :King_Peter_II_of_Yugoslavia
    source: :Prince_Tomislav_of_Yugoslavia
  Finish (132f6e78-bdba-4e33-b9de-dac9957eb992)
 Call ID: 132f6e78-bdba-4e33-b9de-dac9957eb992
  Args: