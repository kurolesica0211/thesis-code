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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Alexandra Elli Francisca Maria of Greece (born 15 October 1968), known professionally as Alexandra Mirzayantz, is a Greek artist, art collector, arts patron, and child life specialist.
As the daughter of Prince Michael of Greece and Denmark, she is a member of the Greek royal family and a relative of the Danish royal family.
A morganatic descendant of the House of Glücksburg, she is not a Danish princess nor is she entitled to the style Royal Highness as other members of the Greek royal family are.
She was born a princess of Greece entitled to the style Your Highness, and was excluded from the line of succession to the Greek throne.
She is a second cousin of Constantine II of Greece, who reigned as King of the Hellenes until the monarchy was abolished in 1973.
Early life and family

Princess Alexandra was born in Athens on 15 October 1968.
She is the daughter of the historian Prince Michael of Greece and Denmark and the artist Marina Karella.
She is the older sister of Princess Olga.
She is a great-granddaughter of George I of Greece and Olga Constantinovna of Russia.
She is also a great-granddaughter of Prince Jean, Duke of Guise and a great-great-granddaughter of Christian IX of Denmark.
As Princess Alexandra's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, uses the style Your Highness instead of Her Royal Highness, and is excluded from the line of succession to the former Greek throne.
On 29 July 1973, Princess Alexandra's second cousin, Constantine II of Greece, was deposed and the Greek monarchy was abolished.
Career

Princess Alexandra is a certified child life specialist.
Princess Alexandra and her husband are patrons of the New York art scene.
She owns a portrait of her grandfather, Prince Christopher of Greece and Denmark, painted by Philip de László in 1919, as part of her collection.
Personal life

Princess Alexandra married the perfumer Nicolas Mirzayantz on 27 June 1998 in Torcello.
She attended the funeral of her father, Prince Michael on 1 August 2024, and was seen with other Greek royal family members, including Princess Olga, Queen Anne-Marie of Greece, Queen Sofía of Spain, and Crown Prince Pavlos.



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
  AssignClass (dbccebaa-6fa3-438a-b308-9b1fa1967dbd)
 Call ID: dbccebaa-6fa3-438a-b308-9b1fa1967dbd
  Args:
    type: :Person
    source: Alexandra_Mirzayantz
  AssignClass (efbf6f76-04d6-4876-a42e-41cfcae1cc6e)
 Call ID: efbf6f76-04d6-4876-a42e-41cfcae1cc6e
  Args:
    type: :Woman
    source: Alexandra_Mirzayantz
  AddLiteral (dd748633-62b4-4206-bb04-5c259e2bc433)
 Call ID: dd748633-62b4-4206-bb04-5c259e2bc433
  Args:
    source: Alexandra_Mirzayantz
    literal_value: Alexandra Mirzayantz
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (3f3163f0-3906-486a-93f6-f7eac0354914)
 Call ID: 3f3163f0-3906-486a-93f6-f7eac0354914
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Princess Alexandra Elli Francisca Maria of Greece
    source: Alexandra_Mirzayantz
  AssignClass (0020e0d9-d620-452c-ba76-2ba5fd5ea9ed)
 Call ID: 0020e0d9-d620-452c-ba76-2ba5fd5ea9ed
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (35651d8d-fbda-439f-aa1b-3f3d4e79418f)
 Call ID: 35651d8d-fbda-439f-aa1b-3f3d4e79418f
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (43a5054d-ca01-4774-864c-0109e561fc54)
 Call ID: 43a5054d-ca01-4774-864c-0109e561fc54
  Args:
    type: :Person
    source: Marina_Karella
  AssignClass (bf2955b8-af76-4a50-81f2-624cbaa197cf)
 Call ID: bf2955b8-af76-4a50-81f2-624cbaa197cf
  Args:
    type: :Woman
    source: Marina_Karella
  AddTriple (3a7c4969-e71a-41cb-940d-b01bc80960c9)
 Call ID: 3a7c4969-e71a-41cb-940d-b01bc80960c9
  Args:
    relation: :hasFather
    source: Alexandra_Mirzayantz
    target: Prince_Michael_of_Greece_and_Denmark
  AddTriple (049b2fe8-04ff-4710-aab9-586f3ffe8a11)
 Call ID: 049b2fe8-04ff-4710-aab9-586f3ffe8a11
  Args:
    target: Marina_Karella
    source: Alexandra_Mirzayantz
    relation: :hasMother
  AssignClass (e187abf3-2557-4577-99cd-2bbf68ce09e7)
 Call ID: e187abf3-2557-4577-99cd-2bbf68ce09e7
  Args:
    type: :Person
    source: Princess_Olga
  AssignClass (cfae2c61-bc3a-4b18-b8d1-1c8fa4599781)
 Call ID: cfae2c61-bc3a-4b18-b8d1-1c8fa4599781
  Args:
    type: :Woman
    source: Princess_Olga
  AddTriple (8ad32cbc-9cb2-49d6-ad98-86b59440268a)
 Call ID: 8ad32cbc-9cb2-49d6-ad98-86b59440268a
  Args:
    relation: :hasSister
    source: Alexandra_Mirzayantz
    target: Princess_Olga
  AssignClass (04b039d8-6107-46e8-b7d1-da4d8629cf7c)
 Call ID: 04b039d8-6107-46e8-b7d1-da4d8629cf7c
  Args:
    type: :Person
    source: Nicolas_Mirzayantz
  AssignClass (87487c8d-1212-4c01-9fc4-b632640af281)
 Call ID: 87487c8d-1212-4c01-9fc4-b632640af281
  Args:
    type: :Man
    source: Nicolas_Mirzayantz
  AddTriple (fc560dc8-33c0-4d6f-b08e-680e52175461)
 Call ID: fc560dc8-33c0-4d6f-b08e-680e52175461
  Args:
    relation: :hasRelation
    target: Nicolas_Mirzayantz
    source: Alexandra_Mirzayantz
  AddLiteral (8292bca6-7d73-4508-ab7d-3119a9c55d64)
 Call ID: 8292bca6-7d73-4508-ab7d-3119a9c55d64
  Args:
    literal_value: 1998
    source: Alexandra_Mirzayantz
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (4badaa7f-a280-4cc8-9f04-13f081a6587b)
 Call ID: 4badaa7f-a280-4cc8-9f04-13f081a6587b
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (6a61223e-4650-4728-9330-20a6b7585645)
 Call ID: 6a61223e-4650-4728-9330-20a6b7585645
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (6845b8d1-cf9e-4efc-b7b2-83b0d6ad7002)
 Call ID: 6845b8d1-cf9e-4efc-b7b2-83b0d6ad7002
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AssignClass (f39a946b-b8c4-48d9-8c12-fc2f8647dd63)
 Call ID: f39a946b-b8c4-48d9-8c12-fc2f8647dd63
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (53626e98-e3f5-4c7e-81cf-31b13749620c)
 Call ID: 53626e98-e3f5-4c7e-81cf-31b13749620c
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Guise
  AssignClass (37fed19c-5b1d-4c22-805f-57a3fc3ae06c)
 Call ID: 37fed19c-5b1d-4c22-805f-57a3fc3ae06c
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (d8c6fc8c-40d2-4345-923e-e0112fe2e93b)
 Call ID: d8c6fc8c-40d2-4345-923e-e0112fe2e93b
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (ecf8c210-cdb2-4e00-9975-33ffdebe7cd2)
 Call ID: ecf8c210-cdb2-4e00-9975-33ffdebe7cd2
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (2f0927b4-70a2-472b-8a64-b7f60912ad83)
 Call ID: 2f0927b4-70a2-472b-8a64-b7f60912ad83
  Args:
    type: :Person
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (dc8b5345-1708-4bae-a5a1-d1396a28bbb3)
 Call ID: dc8b5345-1708-4bae-a5a1-d1396a28bbb3
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (c5d1b3f2-98c8-400b-b513-d0667e062915)
 Call ID: c5d1b3f2-98c8-400b-b513-d0667e062915
  Args:
    target: George_I_of_Greece
    source: Alexandra_Mirzayantz
    relation: :hasAncestor
  AddTriple (e24dabea-6089-4dfe-9788-f0a774642699)
 Call ID: e24dabea-6089-4dfe-9788-f0a774642699
  Args:
    target: Olga_Constantinovna_of_Russia
    source: Alexandra_Mirzayantz
    relation: :hasAncestor
  AddTriple (173c6d3e-0323-4c8f-9dad-aec774c31b6b)
 Call ID: 173c6d3e-0323-4c8f-9dad-aec774c31b6b
  Args:
    relation: :hasAncestor
    source: Alexandra_Mirzayantz
    target: Prince_Jean_Duke_of_Guise
  AddTriple (31961781-a205-4a0b-acac-829a4343c461)
 Call ID: 31961781-a205-4a0b-acac-829a4343c461
  Args:
    relation: :hasAncestor
    target: Christian_IX_of_Denmark
    source: Alexandra_Mirzayantz
  AddTriple (3fd76ce1-148f-49b4-9fda-d7c247942cfe)
 Call ID: 3fd76ce1-148f-49b4-9fda-d7c247942cfe
  Args:
    relation: :hasAncestor
    target: Prince_Christopher_of_Greece_and_Denmark
    source: Alexandra_Mirzayantz
  AssignClass (1e121b7b-86f9-4e9b-b38a-2926651e2eeb)
 Call ID: 1e121b7b-86f9-4e9b-b38a-2926651e2eeb
  Args:
    type: :Person
    source: Queen_Anne-Marie_of_Greece
  AssignClass (a9bdd8b0-0138-4473-8910-6248cf6d09f4)
 Call ID: a9bdd8b0-0138-4473-8910-6248cf6d09f4
  Args:
    type: :Woman
    source: Queen_Anne-Marie_of_Greece
  AssignClass (8ad2562a-7dff-4d3f-adee-f597f6f97f00)
 Call ID: 8ad2562a-7dff-4d3f-adee-f597f6f97f00
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  AssignClass (fbe0db39-c0f0-48a5-98b1-219b67eef4ef)
 Call ID: fbe0db39-c0f0-48a5-98b1-219b67eef4ef
  Args:
    type: :Woman
    source: Queen_Sofia_of_Spain
  AssignClass (5e714814-8a21-4395-a42d-e6c33ddbe5ea)
 Call ID: 5e714814-8a21-4395-a42d-e6c33ddbe5ea
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (9be31caa-6110-4b23-bf6c-678166eaa058)
 Call ID: 9be31caa-6110-4b23-bf6c-678166eaa058
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (b6957c2f-d80b-41d3-960e-c26bc8a5aafe)
 Call ID: b6957c2f-d80b-41d3-960e-c26bc8a5aafe
  Args:
    type: :Person
    source: Crown_Prince_Pavlos
  AssignClass (e44dbd19-000f-4466-9c57-089cea2a9d6a)
 Call ID: e44dbd19-000f-4466-9c57-089cea2a9d6a
  Args:
    type: :Man
    source: Crown_Prince_Pavlos
  Finish (2b6321c1-7ca7-494c-a3f1-03b79eb4e357)
 Call ID: 2b6321c1-7ca7-494c-a3f1-03b79eb4e357
  Args: