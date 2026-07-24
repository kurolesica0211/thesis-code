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
Lord Frederick Michael George David Louis Windsor (born 6 April 1979) is a member of the British royal family.
He is the only son of Prince and Princess Michael of Kent, and is 54th in the line of succession to the British throne.
He is married to British actress Sophie Winkleman and is a financial analyst by profession.
As a great-grandchild of King George V and Queen Mary, he is a second cousin of King Charles III.
Early life and education

Frederick Michael George David Louis Windsor was born on 6 April 1979 at St Mary's Hospital, London, and was christened on 11 July at the Chapel Royal, St James's Palace, Westminster.
A first cousin once removed of Queen Elizabeth II and a first cousin twice removed of Prince Philip, Duke of Edinburgh, he is therefore both a second cousin and a second cousin once removed of King Charles III and his siblings.
Frederick and his sister, Lady Gabriella, were brought up in the Church of England.
Career

After graduating, Frederick worked as a fashion model, appearing in a campaign for Burberry and for the designer Tomasz Starzewski, and also as a music journalist, notably for Tatler magazine.
Personal life

On St Valentine's Day, 14 February 2009, Frederick became engaged to the actress Sophie Winkleman.
She was baptised at St James's Palace in December 2013 and has Princess Eugenie among her godparents.
Maud served as a bridesmaid at the wedding of Princess Eugenie and Jack Brooksbank in 2018.
On 20 January 2016, it was announced Frederick and Sophie had become parents to a second daughter, Isabella Alexandra May, who was born on 16 January 2016 at Chelsea and Westminster Hospital in London.
From September 2016 until its closure in 2023, Frederick was president of the charity Soldier On!, which supported vulnerable, disadvantaged, or socially isolated people through archaeology and heritage projects as well as personal development workshops.
On 21 February 2017, Frederick was inducted into the Grand Order of Water Rats charitable fraternity.
Titles and styles

Under letters patent issued in 1917 and still in force today, Frederick's father is entitled to the dignity of prince and the style His Royal Highness as the son of a son of George V. Although these letters do not bestow these royal dignities beyond grandchildren of monarchs (except in the case of the children of the Prince of Wales, as modified by Elizabeth II), they allow the children of sons of sons of a British monarch to be styled as the children of a duke, with the honorific courtesy style of Lord or Lady before their given names.
Since Lord Frederick is not a peer in his own right, his style is not hereditary and his children are not entitled to any distinctions, including the prefix The Honourable.



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
  AssignClass (bce57ac0-695c-43c8-a2f5-45abaf292443)
 Call ID: bce57ac0-695c-43c8-a2f5-45abaf292443
  Args:
    type: :Man
    source: FrederickWindsor
  AssignClass (8a203c0a-9bb2-4cc1-aa72-349ba6a8a3bd)
 Call ID: 8a203c0a-9bb2-4cc1-aa72-349ba6a8a3bd
  Args:
    type: :Person
    source: FrederickWindsor
  AddLiteral (263da317-2bd7-4554-b978-62322691179a)
 Call ID: 263da317-2bd7-4554-b978-62322691179a
  Args:
    source: FrederickWindsor
    relation: :hasBirthYear
    literal_value: 1979
    literal_type: xsd:integer
  AssignClass (3a1008c9-1d8d-4bb3-8f23-4164691d60f8)
 Call ID: 3a1008c9-1d8d-4bb3-8f23-4164691d60f8
  Args:
    source: PrinceMichaelOfKent
    type: :Man
  AssignClass (0e0d9a90-053e-452a-8289-8a715d0bd15c)
 Call ID: 0e0d9a90-053e-452a-8289-8a715d0bd15c
  Args:
    source: PrinceMichaelOfKent
    type: :Person
  AssignClass (771f18a0-f8ea-49ad-951c-52329ac42ac4)
 Call ID: 771f18a0-f8ea-49ad-951c-52329ac42ac4
  Args:
    type: :Woman
    source: PrincessMichaelOfKent
  AssignClass (d5e51cfa-e18a-4f69-9125-a8c298d7f37b)
 Call ID: d5e51cfa-e18a-4f69-9125-a8c298d7f37b
  Args:
    type: :Person
    source: PrincessMichaelOfKent
  AddTriple (3c3de4fd-a407-4c0f-9d02-b58d815edeec)
 Call ID: 3c3de4fd-a407-4c0f-9d02-b58d815edeec
  Args:
    source: FrederickWindsor
    relation: :hasFather
    target: PrinceMichaelOfKent
  AddTriple (ec4660f3-7a91-4494-ab3a-c823175fd930)
 Call ID: ec4660f3-7a91-4494-ab3a-c823175fd930
  Args:
    relation: :hasMother
    target: PrincessMichaelOfKent
    source: FrederickWindsor
  AssignClass (b8769ccb-5771-43c3-afb8-2ddcdee07d84)
 Call ID: b8769ccb-5771-43c3-afb8-2ddcdee07d84
  Args:
    type: :Woman
    source: SophieWinkleman
  AssignClass (0bf160d7-d68a-4256-b2f3-461c16d28c41)
 Call ID: 0bf160d7-d68a-4256-b2f3-461c16d28c41
  Args:
    source: SophieWinkleman
    type: :Person
  AddTriple (12f7d704-d011-4f33-81d1-066fc5636e7a)
 Call ID: 12f7d704-d011-4f33-81d1-066fc5636e7a
  Args:
    source: FrederickWindsor
    relation: :hasRelation
    target: SophieWinkleman
  AddLiteral (457741dc-06c3-4bea-a4ea-36eb1c2e794a)
 Call ID: 457741dc-06c3-4bea-a4ea-36eb1c2e794a
  Args:
    source: FrederickWindsor
    literal_type: xsd:integer
    literal_value: 2009
    relation: :hasMarriageYear
  AssignClass (49fee6f2-0ad1-4ef0-81a0-162a5a3f3f9e)
 Call ID: 49fee6f2-0ad1-4ef0-81a0-162a5a3f3f9e
  Args:
    type: :Woman
    source: GabriellaWindsor
  AssignClass (ef5a3073-ac04-4710-a730-1144eb2bcaad)
 Call ID: ef5a3073-ac04-4710-a730-1144eb2bcaad
  Args:
    type: :Person
    source: GabriellaWindsor
  AddTriple (5b354e94-5774-4aba-b7c7-2973971ddae4)
 Call ID: 5b354e94-5774-4aba-b7c7-2973971ddae4
  Args:
    target: GabriellaWindsor
    relation: :hasSister
    source: FrederickWindsor
  AssignClass (4e4f440f-87b6-4b9e-b843-3231847dade8)
 Call ID: 4e4f440f-87b6-4b9e-b843-3231847dade8
  Args:
    source: IsabellaAlexandraMayWindsor
    type: :Woman
  AssignClass (88d4844e-a70f-4c90-84b4-8cca4207cf03)
 Call ID: 88d4844e-a70f-4c90-84b4-8cca4207cf03
  Args:
    type: :Person
    source: IsabellaAlexandraMayWindsor
  AddTriple (c929a7aa-2846-4d89-9a08-85b8c2945ed5)
 Call ID: c929a7aa-2846-4d89-9a08-85b8c2945ed5
  Args:
    relation: :hasDaughter
    target: IsabellaAlexandraMayWindsor
    source: FrederickWindsor
  AddTriple (d5f7a8c9-c1b6-4ad7-91fe-636f904ad0d8)
 Call ID: d5f7a8c9-c1b6-4ad7-91fe-636f904ad0d8
  Args:
    source: SophieWinkleman
    relation: :hasDaughter
    target: IsabellaAlexandraMayWindsor
  AssignClass (32d49b8c-3b16-4fe8-b688-5d4966cece6a)
 Call ID: 32d49b8c-3b16-4fe8-b688-5d4966cece6a
  Args:
    source: KingGeorgeV
    type: :Man
  AssignClass (9d669c24-46d6-4787-a4b1-6c5305d7bedf)
 Call ID: 9d669c24-46d6-4787-a4b1-6c5305d7bedf
  Args:
    type: :Person
    source: KingGeorgeV
  AssignClass (9e2b3dd6-e42d-454f-9d27-47e5e1be5466)
 Call ID: 9e2b3dd6-e42d-454f-9d27-47e5e1be5466
  Args:
    type: :Woman
    source: QueenMary
  AssignClass (543a39a0-a438-4347-82da-abca35c0806a)
 Call ID: 543a39a0-a438-4347-82da-abca35c0806a
  Args:
    source: QueenMary
    type: :Person
  AddTriple (fef13db8-4064-495f-a369-b58c5cde580b)
 Call ID: fef13db8-4064-495f-a369-b58c5cde580b
  Args:
    source: FrederickWindsor
    relation: :hasAncestor
    target: KingGeorgeV
  AddTriple (54ee5dd6-db25-4fd4-830a-9573b500e559)
 Call ID: 54ee5dd6-db25-4fd4-830a-9573b500e559
  Args:
    source: FrederickWindsor
    target: QueenMary
    relation: :hasAncestor
  Finish (1f5bac7e-780f-4562-8a9a-1b3e7efe9e59)
 Call ID: 1f5bac7e-780f-4562-8a9a-1b3e7efe9e59
  Args: