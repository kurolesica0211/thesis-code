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
Lady Sarah Frances Elizabeth Chatto (née Armstrong-Jones; born 1
She is the only daughter of Princess Margaret, Countess of Snowdon, and Antony Armstrong-Jones, 1st Earl of Snowdon.
She and her brother, David Armstrong-Jones, 2nd Earl of Snowdon, are the only maternal first cousins of King Charles III.
Early life and education

Lady Sarah Frances Elizabeth Armstrong-Jones was born at 8:20 am on 1 May 1964 at Kensington Palace in London.
She is the second child and only daughter of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
Sarah is a godmother to Prince Harry, Duke of Sussex, Lady Rose Gilman, and Lady Louise Windsor.
She also has half-siblings on her father's side: Polly Fry (born 1960), Lady Frances Armstrong-Jones (born 1979), and Jasper Cable-Alexander (born 1998).
Sarah and her brother, David, then Viscount Linley, grew up in the nursery of Kensington Palace, Apartment 10.
Their parents' marriage was fractious; the couple formally separated when Sarah was 12 and divorced when she was 14.
Holidays were given to the royal estates at Sandringham and Balmoral, where Sarah did landscape painting.
Sarah was a bridesmaid at the wedding of her cousin Charles, Prince of Wales, and Lady Diana Spencer.
The film's producer, her relative John Knatchbull, 7th Baron Brabourne (son-in-law of Louis Mountbatten, 1st Earl Mountbatten of Burma), gave her a job as an intern assisting the wardrobe department and studying wood gilding under her father's cousin Thomas Messel.
Professional life

Chatto has been exhibiting her work, always under the name Sarah Armstrong-Jones, at The Redfern Gallery since 1995.
Chatto does not undertake public duties and is not considered a "working royal".
However, it has been reported that she was close to her aunt Queen Elizabeth II.
Chatto is frequently seen attending public events such as jubilees and funerals, as well as semi-private royal family events, such as the Sandringham Christmas service, with her sons.
Marriage and children

Sarah met Daniel Chatto during her years in India with her father in the 1980s.
Chatto was working on another British film, Heat and Dust.
He is from a theatrical family, the son of actor Tom Chatto (1920–1982) and the theatrical agent Ros Chatto (born Rosalind Joan Thompson; died 2012).
Her bridesmaids were half-sister Lady Frances, Zara Phillips (daughter of her first cousin Princess Anne), and Tara Noble-Singh, a family friend.



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
  AssignClass (0b0c77f0-2047-4e3d-85de-a679969a60f6)
 Call ID: 0b0c77f0-2047-4e3d-85de-a679969a60f6
  Args:
    type: :Woman
    source: :Lady_Sarah_Chatto
  AssignClass (3a8cda23-680c-4dbe-b759-3c2029e49983)
 Call ID: 3a8cda23-680c-4dbe-b759-3c2029e49983
  Args:
    source: :Lady_Sarah_Chatto
    type: :Person
  AssignClass (835dd03f-b18c-4bcd-916d-b8de0cd460ba)
 Call ID: 835dd03f-b18c-4bcd-916d-b8de0cd460ba
  Args:
    source: :Princess_Margaret
    type: :Woman
  AssignClass (ad4ab2e4-32d3-4cb4-a920-0ad52cd0f222)
 Call ID: ad4ab2e4-32d3-4cb4-a920-0ad52cd0f222
  Args:
    source: :Princess_Margaret
    type: :Person
  AssignClass (9f394f9a-a661-44ea-8697-a9a1c76d01b4)
 Call ID: 9f394f9a-a661-44ea-8697-a9a1c76d01b4
  Args:
    source: :Antony_Armstrong-Jones
    type: :Man
  AssignClass (832c5df8-5208-47fc-b74d-70854505cfc8)
 Call ID: 832c5df8-5208-47fc-b74d-70854505cfc8
  Args:
    type: :Person
    source: :Antony_Armstrong-Jones
  AssignClass (d77953ca-ea88-4050-9cd0-6b248588e12b)
 Call ID: d77953ca-ea88-4050-9cd0-6b248588e12b
  Args:
    source: :David_Armstrong-Jones
    type: :Man
  AssignClass (42cd4101-6930-4f27-bd9d-cc99e2f27ade)
 Call ID: 42cd4101-6930-4f27-bd9d-cc99e2f27ade
  Args:
    source: :David_Armstrong-Jones
    type: :Person
  AddTriple (2397d980-62a6-4f15-94bc-099eb3bb1a7b)
 Call ID: 2397d980-62a6-4f15-94bc-099eb3bb1a7b
  Args:
    target: :Princess_Margaret
    source: :Lady_Sarah_Chatto
    relation: :hasMother
  AddTriple (db1cae87-ecb9-4cac-96c8-6b0980690303)
 Call ID: db1cae87-ecb9-4cac-96c8-6b0980690303
  Args:
    source: :Lady_Sarah_Chatto
    target: :Antony_Armstrong-Jones
    relation: :hasFather
  AddTriple (237e3595-44b6-4d5b-863f-1c68e5f2deaf)
 Call ID: 237e3595-44b6-4d5b-863f-1c68e5f2deaf
  Args:
    target: :Princess_Margaret
    source: :David_Armstrong-Jones
    relation: :hasMother
  AddTriple (1e3e5773-c278-44c2-9bf4-6da770f2dd18)
 Call ID: 1e3e5773-c278-44c2-9bf4-6da770f2dd18
  Args:
    target: :Antony_Armstrong-Jones
    source: :David_Armstrong-Jones
    relation: :hasFather
  AddTriple (6102ec13-18ca-4ca6-b63a-940286868793)
 Call ID: 6102ec13-18ca-4ca6-b63a-940286868793
  Args:
    target: :David_Armstrong-Jones
    source: :Lady_Sarah_Chatto
    relation: :hasBrother
  AddLiteral (be2cb41f-a57d-4038-aea9-58099a5c20bc)
 Call ID: be2cb41f-a57d-4038-aea9-58099a5c20bc
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Lady_Sarah_Chatto
    literal_value: 1964
  AssignClass (c6097496-63a4-4503-a683-ea3f360731f6)
 Call ID: c6097496-63a4-4503-a683-ea3f360731f6
  Args:
    source: :Daniel_Chatto
    type: :Man
  AssignClass (27cccf14-6dfb-425e-b7b8-18b7f5a224c2)
 Call ID: 27cccf14-6dfb-425e-b7b8-18b7f5a224c2
  Args:
    source: :Daniel_Chatto
    type: :Person
  AddTriple (fc0c7aee-62ab-484c-916d-fb4822fe95d5)
 Call ID: fc0c7aee-62ab-484c-916d-fb4822fe95d5
  Args:
    relation: :hasRelation
    source: :Lady_Sarah_Chatto
    target: :Daniel_Chatto
  AssignClass (dd4d1c56-56fa-403b-a65d-d0845ba38be5)
 Call ID: dd4d1c56-56fa-403b-a65d-d0845ba38be5
  Args:
    type: :Man
    source: :Tom_Chatto
  AssignClass (71134fc7-d9ca-4a51-bd26-479af7f7ddda)
 Call ID: 71134fc7-d9ca-4a51-bd26-479af7f7ddda
  Args:
    source: :Tom_Chatto
    type: :Person
  AssignClass (31475143-f6c3-4cd7-b280-c6562a41276b)
 Call ID: 31475143-f6c3-4cd7-b280-c6562a41276b
  Args:
    type: :Woman
    source: :Ros_Chatto
  AssignClass (a9ccfdbc-ac40-4c4c-b6c9-0470e7e62448)
 Call ID: a9ccfdbc-ac40-4c4c-b6c9-0470e7e62448
  Args:
    type: :Person
    source: :Ros_Chatto
  AddTriple (7305ce19-92ea-4813-b9ee-c1167486145d)
 Call ID: 7305ce19-92ea-4813-b9ee-c1167486145d
  Args:
    relation: :hasFather
    target: :Tom_Chatto
    source: :Daniel_Chatto
  AddTriple (d46aa968-4494-4d6c-b57e-e6b9113458f7)
 Call ID: d46aa968-4494-4d6c-b57e-e6b9113458f7
  Args:
    source: :Daniel_Chatto
    target: :Ros_Chatto
    relation: :hasMother
  AddLiteral (3b073b45-5b67-4f51-81bd-cef2ea63c18b)
 Call ID: 3b073b45-5b67-4f51-81bd-cef2ea63c18b
  Args:
    literal_value: 1920
    source: :Tom_Chatto
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bc9d2062-fdcf-4b0c-ab2e-914f98f61802)
 Call ID: bc9d2062-fdcf-4b0c-ab2e-914f98f61802
  Args:
    literal_value: 1982
    source: :Tom_Chatto
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (c0f29de3-156c-4d33-b7ac-3ee87ed008a4)
 Call ID: c0f29de3-156c-4d33-b7ac-3ee87ed008a4
  Args:
    literal_value: 2012
    source: :Ros_Chatto
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (54c9b5ad-e27d-4312-99b7-1eb418cc4da0)
 Call ID: 54c9b5ad-e27d-4312-99b7-1eb418cc4da0
  Args:
    type: :Woman
    source: :Polly_Fry
  AssignClass (fad08f21-0a9e-45fb-8ec6-be01803b7c3a)
 Call ID: fad08f21-0a9e-45fb-8ec6-be01803b7c3a
  Args:
    type: :Person
    source: :Polly_Fry
  AssignClass (4f9ec0cc-2512-4ff6-bee9-d1a4fd0c7a68)
 Call ID: 4f9ec0cc-2512-4ff6-bee9-d1a4fd0c7a68
  Args:
    source: :Lady_Frances_Armstrong-Jones
    type: :Woman
  AssignClass (489590a8-5b60-45ea-96d1-d0c7d267dc1b)
 Call ID: 489590a8-5b60-45ea-96d1-d0c7d267dc1b
  Args:
    source: :Lady_Frances_Armstrong-Jones
    type: :Person
  AssignClass (fc9dd751-623b-4887-b3e8-369de0062360)
 Call ID: fc9dd751-623b-4887-b3e8-369de0062360
  Args:
    source: :Jasper_Cable-Alexander
    type: :Man
  AssignClass (1f488726-8874-4baf-b5f9-7948389712c0)
 Call ID: 1f488726-8874-4baf-b5f9-7948389712c0
  Args:
    type: :Person
    source: :Jasper_Cable-Alexander
  AddTriple (ac393131-b1d5-45f4-8e42-ae04f5e112b6)
 Call ID: ac393131-b1d5-45f4-8e42-ae04f5e112b6
  Args:
    relation: :hasFather
    target: :Antony_Armstrong-Jones
    source: :Polly_Fry
  AddTriple (59eff34b-62e9-4dfb-a425-05a7b8d5039b)
 Call ID: 59eff34b-62e9-4dfb-a425-05a7b8d5039b
  Args:
    target: :Antony_Armstrong-Jones
    source: :Lady_Frances_Armstrong-Jones
    relation: :hasFather
  AddTriple (94903a2b-a94e-41b4-acb4-a09e3604b225)
 Call ID: 94903a2b-a94e-41b4-acb4-a09e3604b225
  Args:
    target: :Antony_Armstrong-Jones
    source: :Jasper_Cable-Alexander
    relation: :hasFather
  Finish (72a8ee4a-23a4-4b3f-8795-7a918b0a55b2)
 Call ID: 72a8ee4a-23a4-4b3f-8795-7a918b0a55b2
  Args: