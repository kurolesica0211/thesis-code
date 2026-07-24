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
Thomas Patrick John Anson, 5th Earl of Lichfield (25 April 1939 – 11 November 2005), was an English photographer from the Anson family.
He inherited the Earldom of Lichfield in 1960 from his paternal grandfather.
In his professional practice he was known as Patrick Lichfield.
Biography

Thomas Patrick John Anson was born on 25 April 1939.
He was the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), the eldest son and heir apparent of Thomas Edward Anson, 4th Earl of Lichfield (1883–1960).
His mother was born Anne Bowes-Lyon (1917–1980), a niece of Queen Elizabeth the Queen Mother.
His parents divorced in 1948, and his mother subsequently became Princess Anne of Denmark after her remarriage to Prince Georg of Denmark in 1950.
He had one sister, Lady Elizabeth Georgiana Anson (1941–2020), who married Sir Geoffrey Adam Shakerley, 6th Baronet.
Lichfield was educated at two boarding independent schools: Wellesley House School in the coastal town of Broadstairs in Kent, and Harrow School in Harrow on the Hill in north-west London, followed by the Royal Military Academy Sandhurst.
His father died in 1958, leaving Patrick to succeed as 5th Earl of Lichfield when his grandfather died in 1960.
Lichfield joined the Grenadier Guards in 1959.
He was selected to take the official photographs of the wedding of the Prince and Princess of Wales in 1981, and subsequently became one of the UK's best-known photographers.
He was chosen by Queen Elizabeth II and the Duke of Edinburgh to take official pictures of her Golden Jubilee in 2002.
He also cameoed in the British sitcom Keeping Up Appearances, appearing in the episode "Sea Fever" as a passenger on the Queen Elizabeth 2.
Lichfield resided in an apartment at the former family seat of Shugborough Hall, near Cannock Chase in Staffordshire.
Marriage and children

On 8 March 1975 Lichfield married Lady Leonora Grosvenor, elder daughter of Robert Grosvenor, 5th Duke of Westminster and Hon.
The Countess of Lichfield has not remarried and has retained her title.
She and the Earl had one son and two daughters together:


Lichfield's most recent partner was the biographer Lady Annunziata Asquith, daughter of Julian Asquith, 2nd Earl of Oxford and Asquith.
Death

On 10 November 2005, Lichfield suffered a major stroke and died the following day at the John Radcliffe Hospital in Oxford.
Lichfield's apartment at Shugborough now houses an exhibition of his work, together with a recreation of his studio.



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
  AssignClass (21e1b12e-625c-4eb0-846a-c295ec8cc55c)
 Call ID: 21e1b12e-625c-4eb0-846a-c295ec8cc55c
  Args:
    source: Thomas_Patrick_John_Anson
    type: :Man
  AssignClass (0458b2eb-72ad-462c-9475-e746fd4d965e)
 Call ID: 0458b2eb-72ad-462c-9475-e746fd4d965e
  Args:
    source: Thomas_Patrick_John_Anson
    type: :Person
  AddLiteral (6c8ba239-2fdb-4d67-be89-2b2cbb275735)
 Call ID: 6c8ba239-2fdb-4d67-be89-2b2cbb275735
  Args:
    literal_value: 1939
    source: Thomas_Patrick_John_Anson
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b5c09f16-a8b0-42ff-920f-37a96769c770)
 Call ID: b5c09f16-a8b0-42ff-920f-37a96769c770
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Thomas_Patrick_John_Anson
    literal_value: 2005
  AddLiteral (3679774f-4b42-44db-92e4-c3e702ce47ed)
 Call ID: 3679774f-4b42-44db-92e4-c3e702ce47ed
  Args:
    literal_value: Patrick Lichfield
    source: Thomas_Patrick_John_Anson
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (c84d8a00-8d55-4249-bc69-31b9a76255b0)
 Call ID: c84d8a00-8d55-4249-bc69-31b9a76255b0
  Args:
    type: :Man
    source: Thomas_William_Arnold_Anson
  AssignClass (2b5fcd05-0436-4964-9328-d583716eb0df)
 Call ID: 2b5fcd05-0436-4964-9328-d583716eb0df
  Args:
    type: :Person
    source: Thomas_William_Arnold_Anson
  AddLiteral (bd852f8b-dc62-4bfa-a5f0-faf886c2c916)
 Call ID: bd852f8b-dc62-4bfa-a5f0-faf886c2c916
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1913
    source: Thomas_William_Arnold_Anson
  AddLiteral (a44f60bf-10db-4c8e-bc53-afdf282a133e)
 Call ID: a44f60bf-10db-4c8e-bc53-afdf282a133e
  Args:
    source: Thomas_William_Arnold_Anson
    literal_value: 1958
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (2f4f455a-79da-4f9c-84b5-76e22d2e73d5)
 Call ID: 2f4f455a-79da-4f9c-84b5-76e22d2e73d5
  Args:
    relation: :hasFather
    target: Thomas_William_Arnold_Anson
    source: Thomas_Patrick_John_Anson
  AssignClass (2280e767-22b0-4f73-8865-9c2d5a1073f8)
 Call ID: 2280e767-22b0-4f73-8865-9c2d5a1073f8
  Args:
    type: :Man
    source: Thomas_Edward_Anson
  AssignClass (a4126237-c935-46ad-803b-ddc76b1fe6be)
 Call ID: a4126237-c935-46ad-803b-ddc76b1fe6be
  Args:
    source: Thomas_Edward_Anson
    type: :Person
  AddLiteral (9b0aba8c-6979-45d7-8bbe-86388d305935)
 Call ID: 9b0aba8c-6979-45d7-8bbe-86388d305935
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Thomas_Edward_Anson
    literal_value: 1883
  AddLiteral (274316e8-0fdd-44f0-aeda-24fb51939b44)
 Call ID: 274316e8-0fdd-44f0-aeda-24fb51939b44
  Args:
    literal_value: 1960
    source: Thomas_Edward_Anson
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (eddfaec8-37f0-4131-8f5e-f6d3b8406c81)
 Call ID: eddfaec8-37f0-4131-8f5e-f6d3b8406c81
  Args:
    relation: :hasFather
    target: Thomas_Edward_Anson
    source: Thomas_William_Arnold_Anson
  AssignClass (3081bdb5-55c5-4e27-a6af-1f061f7240ab)
 Call ID: 3081bdb5-55c5-4e27-a6af-1f061f7240ab
  Args:
    source: Anne_Bowes-Lyon
    type: :Woman
  AssignClass (23f40c8b-a32b-4654-a99b-da7af0a97462)
 Call ID: 23f40c8b-a32b-4654-a99b-da7af0a97462
  Args:
    source: Anne_Bowes-Lyon
    type: :Person
  AddLiteral (892aa1dc-39a8-431a-8821-a73e38c0571a)
 Call ID: 892aa1dc-39a8-431a-8821-a73e38c0571a
  Args:
    source: Anne_Bowes-Lyon
    literal_value: 1917
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d1d2e808-932d-4954-927a-d6c001f15657)
 Call ID: d1d2e808-932d-4954-927a-d6c001f15657
  Args:
    source: Anne_Bowes-Lyon
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (94b57656-cfd6-4aaa-89d0-a4cd93a4c8a7)
 Call ID: 94b57656-cfd6-4aaa-89d0-a4cd93a4c8a7
  Args:
    target: Anne_Bowes-Lyon
    relation: :hasMother
    source: Thomas_Patrick_John_Anson
  AssignClass (01573175-cc39-49d3-9894-e46bae90c7a7)
 Call ID: 01573175-cc39-49d3-9894-e46bae90c7a7
  Args:
    type: :Woman
    source: Elizabeth_Georgiana_Anson
  AssignClass (5ff30fec-e0f5-439d-a0aa-647cd3cef08c)
 Call ID: 5ff30fec-e0f5-439d-a0aa-647cd3cef08c
  Args:
    source: Elizabeth_Georgiana_Anson
    type: :Person
  AddLiteral (ebb6b8c6-81ef-47e9-9150-553b8e79b17b)
 Call ID: ebb6b8c6-81ef-47e9-9150-553b8e79b17b
  Args:
    literal_value: 1941
    source: Elizabeth_Georgiana_Anson
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b6d06db2-fc13-46cb-aaf1-b6b2e5ce3cf2)
 Call ID: b6d06db2-fc13-46cb-aaf1-b6b2e5ce3cf2
  Args:
    literal_value: 2020
    source: Elizabeth_Georgiana_Anson
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (12665f03-a689-481f-9c9c-225c72383f7c)
 Call ID: 12665f03-a689-481f-9c9c-225c72383f7c
  Args:
    relation: :hasSister
    target: Elizabeth_Georgiana_Anson
    source: Thomas_Patrick_John_Anson
  AddTriple (0e69834f-f63a-4810-a1f6-5b4b2e1b5df8)
 Call ID: 0e69834f-f63a-4810-a1f6-5b4b2e1b5df8
  Args:
    source: Elizabeth_Georgiana_Anson
    target: Thomas_William_Arnold_Anson
    relation: :hasFather
  AddTriple (2647ab21-fef6-4ab3-8e7c-3c1f51c5b5c0)
 Call ID: 2647ab21-fef6-4ab3-8e7c-3c1f51c5b5c0
  Args:
    source: Elizabeth_Georgiana_Anson
    target: Anne_Bowes-Lyon
    relation: :hasMother
  AssignClass (bb4d8748-0633-451f-8a15-69643260ee81)
 Call ID: bb4d8748-0633-451f-8a15-69643260ee81
  Args:
    source: Leonora_Grosvenor
    type: :Woman
  AssignClass (d3dc1e24-d799-4925-bc79-ef3bf6c4d1d4)
 Call ID: d3dc1e24-d799-4925-bc79-ef3bf6c4d1d4
  Args:
    source: Leonora_Grosvenor
    type: :Person
  AddLiteral (25ff37db-30cb-4284-af1a-cb32bd4bfea7)
 Call ID: 25ff37db-30cb-4284-af1a-cb32bd4bfea7
  Args:
    source: Thomas_Patrick_John_Anson
    literal_value: 1975
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (818cd47d-7ed2-4579-9599-b965c0f3d2e1)
 Call ID: 818cd47d-7ed2-4579-9599-b965c0f3d2e1
  Args:
    target: Leonora_Grosvenor
    relation: :hasRelation
    source: Thomas_Patrick_John_Anson
  Finish (fc10ebb3-bd90-43e6-8154-e10533022d71)
 Call ID: fc10ebb3-bd90-43e6-8154-e10533022d71
  Args: