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
John Alexander Elphinstone, 17th Lord Elphinstone and 3rd Baron Elphinstone (22 March 1914 – 15 November 1975) was a British nobleman and serviceman during World War II.
He was a first cousin of Queen Elizabeth II.
He was a son of Sidney Elphinstone, 16th Lord Elphinstone, and Lady Mary Bowes-Lyon.
Andrew Charles Victor Elphinstone (the aide-de-camp to the Viceroy of India from 1941 to 1943) and the Hon.
Margaret Elphinstone, wife of writer Denys Rhodes.
His paternal grandparents were William Elphinstone, 15th Lord Elphinstone (the 1st Baron Elphinstone) and the former Lady Constance Euphemia Woronzow Murray (second daughter of Alexander Murray, 6th Earl of Dunmore).
He was a nephew of Queen Elizabeth
The Queen Mother and a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Lord Elphinstone served as president of the Scottish Association of Boys' Clubs, chairman of council of the Scottish branch of British Red Cross Society, and president of the Royal Zoological Society of Scotland.
Personal life

In 1970, during Manitoba's centennial, he was invited by the community of Elphinstone and gave a silver map case, which is today located at the Elphinstone post office, all named in his family's honor.



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
  AssignClass (21974036-9951-4f03-81ba-1056645610c4)
 Call ID: 21974036-9951-4f03-81ba-1056645610c4
  Args:
    type: :Man
    source: John_Alexander_Elphinstone
  AssignClass (abb1e9ae-98ea-4282-8052-be2160e66d54)
 Call ID: abb1e9ae-98ea-4282-8052-be2160e66d54
  Args:
    type: :Person
    source: John_Alexander_Elphinstone
  AddLiteral (86fbd555-8c38-4549-82ba-201f535529f7)
 Call ID: 86fbd555-8c38-4549-82ba-201f535529f7
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1914
    source: John_Alexander_Elphinstone
  AddLiteral (c34721eb-97c7-4a89-b315-c42d10665bba)
 Call ID: c34721eb-97c7-4a89-b315-c42d10665bba
  Args:
    source: John_Alexander_Elphinstone
    literal_value: 1975
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f3a199f3-c8fc-4104-88fd-e7af35759045)
 Call ID: f3a199f3-c8fc-4104-88fd-e7af35759045
  Args:
    type: :Man
    source: Sidney_Elphinstone
  AssignClass (840ca798-344b-43f2-a912-917993d714e7)
 Call ID: 840ca798-344b-43f2-a912-917993d714e7
  Args:
    type: :Person
    source: Sidney_Elphinstone
  AssignClass (42cf9838-f041-4776-9e09-8d060e81ec10)
 Call ID: 42cf9838-f041-4776-9e09-8d060e81ec10
  Args:
    type: :Woman
    source: Lady_Mary_Bowes-Lyon
  AssignClass (218569e3-0f19-4f08-bb9b-a12cb5393d1d)
 Call ID: 218569e3-0f19-4f08-bb9b-a12cb5393d1d
  Args:
    type: :Person
    source: Lady_Mary_Bowes-Lyon
  AddTriple (2a88cd69-c9ee-4296-8f47-35fe1fb75a61)
 Call ID: 2a88cd69-c9ee-4296-8f47-35fe1fb75a61
  Args:
    source: John_Alexander_Elphinstone
    target: Sidney_Elphinstone
    relation: :hasFather
  AddTriple (ae1cf141-b881-4c05-ad4d-a027f0e664ba)
 Call ID: ae1cf141-b881-4c05-ad4d-a027f0e664ba
  Args:
    source: John_Alexander_Elphinstone
    target: Lady_Mary_Bowes-Lyon
    relation: :hasMother
  AssignClass (da7a82f5-fa90-4de1-9920-9d51eaa0e7ba)
 Call ID: da7a82f5-fa90-4de1-9920-9d51eaa0e7ba
  Args:
    type: :Man
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (7d1ba27e-fe03-4a98-9236-3598ec903a9a)
 Call ID: 7d1ba27e-fe03-4a98-9236-3598ec903a9a
  Args:
    type: :Person
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (e177ba5a-e864-45f1-80b4-3f6a56d4fd57)
 Call ID: e177ba5a-e864-45f1-80b4-3f6a56d4fd57
  Args:
    type: :Woman
    source: Margaret_Elphinstone
  AssignClass (3705a551-2fdc-4ce5-bf24-d1a297078fb6)
 Call ID: 3705a551-2fdc-4ce5-bf24-d1a297078fb6
  Args:
    type: :Person
    source: Margaret_Elphinstone
  AddTriple (19209b11-9ead-40b1-ac0c-b7efc78b625f)
 Call ID: 19209b11-9ead-40b1-ac0c-b7efc78b625f
  Args:
    source: John_Alexander_Elphinstone
    relation: :isSiblingOf
    target: Andrew_Charles_Victor_Elphinstone
  AddTriple (4e787fa7-fc64-4937-8628-5c13faae65a7)
 Call ID: 4e787fa7-fc64-4937-8628-5c13faae65a7
  Args:
    relation: :isSiblingOf
    target: Margaret_Elphinstone
    source: John_Alexander_Elphinstone
  AssignClass (78b8a030-10ee-4675-a3ee-12335ffca167)
 Call ID: 78b8a030-10ee-4675-a3ee-12335ffca167
  Args:
    type: :Man
    source: William_Elphinstone
  AssignClass (68b9510e-a4fe-447f-b0bc-4398fa8c9155)
 Call ID: 68b9510e-a4fe-447f-b0bc-4398fa8c9155
  Args:
    type: :Person
    source: William_Elphinstone
  AssignClass (6f634e8e-9e28-47fd-9f4a-8fbad03b0658)
 Call ID: 6f634e8e-9e28-47fd-9f4a-8fbad03b0658
  Args:
    type: :Woman
    source: Lady_Constance_Euphemia_Woronzow_Murray
  AssignClass (e32bb8ad-ee9d-462d-90c9-df071d207d1d)
 Call ID: e32bb8ad-ee9d-462d-90c9-df071d207d1d
  Args:
    type: :Person
    source: Lady_Constance_Euphemia_Woronzow_Murray
  AddTriple (b31cb5b3-a83c-40af-9ada-7fd5d1e9b52f)
 Call ID: b31cb5b3-a83c-40af-9ada-7fd5d1e9b52f
  Args:
    target: William_Elphinstone
    relation: :hasFather
    source: Sidney_Elphinstone
  AddTriple (9d86634a-6a05-4917-a057-9a0e7943cb78)
 Call ID: 9d86634a-6a05-4917-a057-9a0e7943cb78
  Args:
    relation: :hasMother
    target: Lady_Constance_Euphemia_Woronzow_Murray
    source: Sidney_Elphinstone
  AssignClass (171274fd-5fbd-4bed-b2ca-dd57891ffe47)
 Call ID: 171274fd-5fbd-4bed-b2ca-dd57891ffe47
  Args:
    type: :Man
    source: Alexander_Murray
  AssignClass (8af08544-9d32-41b3-ad82-23f2a0d926fa)
 Call ID: 8af08544-9d32-41b3-ad82-23f2a0d926fa
  Args:
    type: :Person
    source: Alexander_Murray
  AddTriple (6cb67275-e5f6-43a4-b23a-b4fcbadf3058)
 Call ID: 6cb67275-e5f6-43a4-b23a-b4fcbadf3058
  Args:
    target: Alexander_Murray
    relation: :hasFather
    source: Lady_Constance_Euphemia_Woronzow_Murray
  Finish (91e887ae-b600-452e-ad8b-01971bd7ca3b)
 Call ID: 91e887ae-b600-452e-ad8b-01971bd7ca3b
  Args: