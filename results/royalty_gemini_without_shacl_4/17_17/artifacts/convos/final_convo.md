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
David Albert Charles Armstrong-Jones, 2nd Earl of Snowdon (born 3 November 1961), styled as Viscount Linley until 2017 and known professionally as David Linley, is a member of the British royal family, an English furniture maker, and honorary chairman of the auction house Christie's.
He is the only son of Antony Armstrong-Jones, 1st Earl of Snowdon and Princess Margaret, and through his mother a grandson of King George VI and first cousin of King Charles III.
When he was born, he was 5th in the line of succession to the British throne; as of 2025, he is 26th, and the highest who is not a descendant of Queen Elizabeth II, his aunt.
Early life and education

David Albert Charles Armstrong-Jones was born at 10:45 am on 3 November 1961, at Clarence House, London, the son of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
His godparents were his aunt Queen Elizabeth II, Lady Elizabeth Cavendish, Patrick Plunket, 7th Baron Plunket, Lord Rupert Nevill, and Simon Phipps.
He has one full sister, Lady Sarah Chatto (née Armstrong-Jones), and two paternal half-sisters, Lady Frances von Hofmannsthal (née Armstrong-Jones) and Polly Fry.
Professional life

Linley opened a workshop in Dorking, where he designed and made furniture for three years before setting up his own company, David Linley Furniture Limited (now known as Linley), where he makes bespoke furniture, upholstery, and interior design products known for their neoclassical appearance and use of inlaid woods.
Accordingly, the first Earl Snowdon was also created Baron Armstrong-Jones, and retained his seat in the Lords until his death in 2017, whereupon his son inherited the earldom but not the life peerage or the seat.
Serena Alleyne Stanhope (born 1 March 1970, Limerick, Ireland), daughter of Viscount Petersham (later the 12th Earl of Harrington) at St. Margaret's Church, Westminster.
He and his wife have two children:


From 2000 until 2002, Linley, his wife and son lived at Kensington Palace with his mother, Princess Margaret, in her declining years.
On 8 April 2002, Linley, along with the Prince of Wales, the Duke of York, and the Earl of Wessex, "stood guard" at the lying-in-state of their grandmother, Queen Elizabeth the Queen Mother.
This Vigil of the Princes had taken place only once before, during the lying-in-state of George V in 1936.
The first confirmation that the royal in the extortion attempt was Viscount Linley came from the journalist Nicholas Davies.
In 2011, Linley's daughter, Lady Margarita Armstrong-Jones, was a bridesmaid at the wedding of Prince William and Catherine Middleton.
In 2012, his son, styled by courtesy as Viscount Linley since January 2017, was appointed by the Queen as a page of honour.



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
  AssignClass (1aa71b76-9890-4c7c-aa39-92fb001e3d40)
 Call ID: 1aa71b76-9890-4c7c-aa39-92fb001e3d40
  Args:
    type: :Man
    source: :David_Armstrong_Jones
  AssignClass (a70bd199-2353-4afe-87b5-7a7576fe571c)
 Call ID: a70bd199-2353-4afe-87b5-7a7576fe571c
  Args:
    type: :Person
    source: :David_Armstrong_Jones
  AddLiteral (ea033d03-cfdb-4d15-a436-7d63904a3d00)
 Call ID: ea033d03-cfdb-4d15-a436-7d63904a3d00
  Args:
    literal_value: David Linley
    source: :David_Armstrong_Jones
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (43ab9604-3e27-4af2-8c3d-2a45790d65be)
 Call ID: 43ab9604-3e27-4af2-8c3d-2a45790d65be
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    source: :David_Armstrong_Jones
    literal_value: Viscount Linley
  AddLiteral (02ac987f-ce21-4485-b31f-0d91319f5d08)
 Call ID: 02ac987f-ce21-4485-b31f-0d91319f5d08
  Args:
    literal_value: 1961
    source: :David_Armstrong_Jones
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (064b1910-fbb7-4d5d-955b-7b4bb9d856d9)
 Call ID: 064b1910-fbb7-4d5d-955b-7b4bb9d856d9
  Args:
    source: :Antony_Armstrong_Jones
    type: :Man
  AssignClass (4f1e2c11-a5a6-4fe6-817a-16bb059d5dff)
 Call ID: 4f1e2c11-a5a6-4fe6-817a-16bb059d5dff
  Args:
    type: :Person
    source: :Antony_Armstrong_Jones
  AssignClass (66c77933-7a4f-403d-8ee8-2e611d4ce51b)
 Call ID: 66c77933-7a4f-403d-8ee8-2e611d4ce51b
  Args:
    type: :Woman
    source: :Princess_Margaret
  AssignClass (eda81009-6fb4-42e2-a624-9a673d6407d7)
 Call ID: eda81009-6fb4-42e2-a624-9a673d6407d7
  Args:
    source: :Princess_Margaret
    type: :Person
  AddTriple (d57c17ef-635f-4500-8ccb-f2fcfac587fd)
 Call ID: d57c17ef-635f-4500-8ccb-f2fcfac587fd
  Args:
    source: :David_Armstrong_Jones
    target: :Antony_Armstrong_Jones
    relation: :hasFather
  AddTriple (664f3fb8-6e86-495b-bbfb-70bd6837e3f1)
 Call ID: 664f3fb8-6e86-495b-bbfb-70bd6837e3f1
  Args:
    target: :Princess_Margaret
    relation: :hasMother
    source: :David_Armstrong_Jones
  AssignClass (4e4dfdd1-7b84-4678-baa3-4d9e99b826ac)
 Call ID: 4e4dfdd1-7b84-4678-baa3-4d9e99b826ac
  Args:
    type: :Man
    source: :King_George_VI
  AssignClass (d9e29bac-7acc-4d6c-8c5f-9340a235c2e7)
 Call ID: d9e29bac-7acc-4d6c-8c5f-9340a235c2e7
  Args:
    source: :King_George_VI
    type: :Person
  AddTriple (860d5589-01e2-4501-a005-f1fa0def68d3)
 Call ID: 860d5589-01e2-4501-a005-f1fa0def68d3
  Args:
    source: :Princess_Margaret
    target: :King_George_VI
    relation: :hasFather
  AssignClass (68f19a41-45f7-4559-b8d1-1fa995f5cf54)
 Call ID: 68f19a41-45f7-4559-b8d1-1fa995f5cf54
  Args:
    type: :Man
    source: :King_Charles_III
  AssignClass (6ff5e8b0-ee7e-4a99-a76b-0919de3173db)
 Call ID: 6ff5e8b0-ee7e-4a99-a76b-0919de3173db
  Args:
    type: :Person
    source: :King_Charles_III
  AssignClass (c671dd66-1c6d-408a-b718-92bc836e6b5c)
 Call ID: c671dd66-1c6d-408a-b718-92bc836e6b5c
  Args:
    source: :Queen_Elizabeth_II
    type: :Woman
  AssignClass (601fa053-12c8-476d-82fa-95d97229e08e)
 Call ID: 601fa053-12c8-476d-82fa-95d97229e08e
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AddTriple (c660f5e0-39da-49df-a0fe-44a0df731640)
 Call ID: c660f5e0-39da-49df-a0fe-44a0df731640
  Args:
    source: :David_Armstrong_Jones
    relation: :hasSister
    target: :Lady_Sarah_Chatto
  AssignClass (bc58c1a6-41d5-45e2-959f-daabe31890ba)
 Call ID: bc58c1a6-41d5-45e2-959f-daabe31890ba
  Args:
    type: :Woman
    source: :Lady_Sarah_Chatto
  AssignClass (9c2d8ee5-823d-4860-8906-5714b13ea90b)
 Call ID: 9c2d8ee5-823d-4860-8906-5714b13ea90b
  Args:
    type: :Person
    source: :Lady_Sarah_Chatto
  AddTriple (dcbd92ae-1787-4e53-8e8b-97046b4d76f9)
 Call ID: dcbd92ae-1787-4e53-8e8b-97046b4d76f9
  Args:
    source: :David_Armstrong_Jones
    target: :Lady_Frances_von_Hofmannsthal
    relation: :hasSister
  AssignClass (4d313043-be38-4532-9ee1-2fe93b7c4409)
 Call ID: 4d313043-be38-4532-9ee1-2fe93b7c4409
  Args:
    source: :Lady_Frances_von_Hofmannsthal
    type: :Woman
  AssignClass (6d055d96-d6d2-4cae-acba-e041271d7452)
 Call ID: 6d055d96-d6d2-4cae-acba-e041271d7452
  Args:
    type: :Person
    source: :Lady_Frances_von_Hofmannsthal
  AddTriple (bf531f19-2852-4d46-866e-cd3f9201edd4)
 Call ID: bf531f19-2852-4d46-866e-cd3f9201edd4
  Args:
    source: :David_Armstrong_Jones
    relation: :hasSister
    target: :Polly_Fry
  AssignClass (ea69287f-f09e-4f37-8464-7ad08877015e)
 Call ID: ea69287f-f09e-4f37-8464-7ad08877015e
  Args:
    source: :Polly_Fry
    type: :Woman
  AssignClass (511ae554-b22c-4d80-b547-09718ba24c24)
 Call ID: 511ae554-b22c-4d80-b547-09718ba24c24
  Args:
    type: :Person
    source: :Polly_Fry
  AssignClass (bb1e20b5-81a6-48ed-b7d4-85024868cdf1)
 Call ID: bb1e20b5-81a6-48ed-b7d4-85024868cdf1
  Args:
    source: :Serena_Alleyne_Stanhope
    type: :Woman
  AssignClass (dfa92a8f-d835-4433-bb1d-c1e595ed4885)
 Call ID: dfa92a8f-d835-4433-bb1d-c1e595ed4885
  Args:
    source: :Serena_Alleyne_Stanhope
    type: :Person
  AddTriple (32edd685-9fb4-48aa-8e7e-ae8ab670fef3)
 Call ID: 32edd685-9fb4-48aa-8e7e-ae8ab670fef3
  Args:
    source: :David_Armstrong_Jones
    target: :Serena_Alleyne_Stanhope
    relation: :hasRelation
  AssignClass (7b986c12-fa62-4b57-a6a9-4b26e53bdc86)
 Call ID: 7b986c12-fa62-4b57-a6a9-4b26e53bdc86
  Args:
    type: :Woman
    source: :Lady_Margarita_Armstrong_Jones
  AssignClass (360557a2-e285-4458-b899-d000faf20ffd)
 Call ID: 360557a2-e285-4458-b899-d000faf20ffd
  Args:
    source: :Lady_Margarita_Armstrong_Jones
    type: :Person
  AddTriple (2c79ee41-f3af-4232-9b56-f2f2bb834c10)
 Call ID: 2c79ee41-f3af-4232-9b56-f2f2bb834c10
  Args:
    target: :Lady_Margarita_Armstrong_Jones
    relation: :hasDaughter
    source: :David_Armstrong_Jones
  AssignClass (cf6b9ad7-535e-42dc-991e-7b052fbe9fc6)
 Call ID: cf6b9ad7-535e-42dc-991e-7b052fbe9fc6
  Args:
    source: :Viscount_Linley_son
    type: :Man
  AssignClass (7646a9db-99f0-49b4-b311-8e78f30ceb4c)
 Call ID: 7646a9db-99f0-49b4-b311-8e78f30ceb4c
  Args:
    source: :Viscount_Linley_son
    type: :Person
  AddTriple (8b63c86d-843f-4e25-abbf-9c6a83160bce)
 Call ID: 8b63c86d-843f-4e25-abbf-9c6a83160bce
  Args:
    relation: :hasSon
    target: :Viscount_Linley_son
    source: :David_Armstrong_Jones
  Finish (363f68ff-4dac-4abb-88aa-8040a765d5cc)
 Call ID: 363f68ff-4dac-4abb-88aa-8040a765d5cc
  Args: