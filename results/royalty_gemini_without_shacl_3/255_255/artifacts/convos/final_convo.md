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
Patricia Edwina Victoria Knatchbull, 2nd
Countess Mountbatten of Burma, Baroness Brabourne, CBE, MSC, CD (née Mountbatten; 14 February 1924 – 13 June 2017), was a British peeress and third cousin of Queen Elizabeth II.
Earl Mountbatten of Burma (formerly Prince Louis of Battenberg) and of heiress Edwina Ashley.
She was the elder sister of Lady Pamela Hicks, the first cousin of Prince Philip, Duke of Edinburgh, and the last surviving baptismal sponsor to her first cousin once removed King Charles III.
Lady Mountbatten succeeded her father as Countess Mountbatten of Burma when he was assassinated in 1979, as his peerages had been created with special remainder to his daughters and their heirs male.
Early life

Patricia Mountbatten was born in the St George Hanover Square parish of London in 1924, exactly two years after her father proposed to her mother in India.
Her middle names were Edwina, after her mother, and Victoria, after her grandmother the eldest daughter of princess alice of United Kingdom


Marriage and children

On 26 October 1946, she married John Knatchbull, 7th Baron Brabourne (9 November 1924 – 23 September 2005), at the time an aide to her father in the Far East.
They had met after Patricia, having served in the Women's Royal Naval Service, was commissioned in 1945 as a third officer and was serving in the Supreme Allied Headquarters, South East Asia.
The wedding took place at Romsey Abbey in the presence of members of the royal family.
Her bridesmaids were Princess Elizabeth, Princess Margaret, Lady Pamela Mountbatten (the bride's younger sister), and Princess Alexandra, daughter of the Duke and Duchess of Kent.
As Lady Brabourne during her father's lifetime, her immediate family became closely involved in the consideration of a future consort for her first cousin once removed, Charles, Prince of Wales.
In early 1974, Lord Mountbatten began corresponding with the eldest son of Queen Elizabeth II and Prince Philip about a potential marriage to Lady Brabourne's daughter, Amanda.
Charles wrote to Lady Brabourne (who was also his godmother), about his interest in her daughter, to which she replied approvingly, though suggesting that a courtship was premature.
Amanda Knatchbull declined the marriage proposal of Charles in 1980, following the assassination of her maternal grandfather.
Activities

Patricia was educated in Malta, England, and at the Hewitt School in New York City.
In 1973 she was appointed Deputy Lieutenant for the County of Kent; she was also a serving magistrate and was involved with numerous service organisations including SOS Children's Villages UK, of which she was a Patron; the Order of St John, of which she was a Dame; and the Countess Mountbatten's Own Legion of Frontiersmen of the Commonwealth, of which she was a Patron.
On 15 June 1974, she succeeded her distant cousin (first cousin twice removed)
Lady Patricia Ramsay, formerly HRH Princess Patricia of Connaught, as Colonel-in-Chief of Princess Patricia's Canadian Light Infantry, for whom the regiment was named when Princess Patricia's father, the Duke of Connaught, was Governor General of Canada during the First World War.
Despite her succeeding to an earldom in her own right as Countess Mountbatten of Burma on the death of her father in 1979, she preferred that the officers and men of her regiment address her as Lady Patricia.
On 28 August 2007, the Governor General of Canada presented her with the Canadian Meritorious Service Cross for her services as Colonel-in-Chief of Princess Patricia's Light Infantry.
Patricia was in the boat which was blown up by the IRA off the shores of Mullaghmore, County Sligo, in August 1979, killing her 14-year-old son Nicholas; her father; her mother-in-law, the Dowager Baroness Brabourne; and 15-year-old Paul Maxwell, a boat-boy from County Fermanagh.
Following the incident the Countess became Patron and, later, President of The Compassionate Friends, a self-help charitable organisation of bereaved parents in the UK.
In June 2012, at the time of Queen Elizabeth II's first visit to the Republic of Ireland, Countess Mountbatten said the Queen had her full support for meeting Martin McGuinness, who had been a high-ranking member of the IRA.
Death and funeral

Countess Mountbatten died at her home in Mersham, Kent, on 13 June 2017, aged 93.
Her funeral service took place on 27 June at St Paul's Church, Knightsbridge, and was attended by the Queen Elizabeth II, Prince Philip, Duke of Edinburgh, and other senior members of the royal family.
Her casket was borne by a party of pall bearers from Princess Patricia's Canadian Light Infantry, who were in London on public duties.
She was buried in the Knatchbull family plot in Mersham churchyard.



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
  AssignClass (c5705e33-f6a0-4cd3-891f-09fe7ca4a449)
 Call ID: c5705e33-f6a0-4cd3-891f-09fe7ca4a449
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (2d632b1c-c729-4711-91b1-eea343c6669d)
 Call ID: 2d632b1c-c729-4711-91b1-eea343c6669d
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AddLiteral (61f42af2-3d08-46ab-8be1-6d8d7d7aae82)
 Call ID: 61f42af2-3d08-46ab-8be1-6d8d7d7aae82
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasBirthYear
    source: Patricia_Mountbatten
  AddLiteral (5ace2391-b90f-4665-b613-11ea8027809a)
 Call ID: 5ace2391-b90f-4665-b613-11ea8027809a
  Args:
    relation: :hasDeathYear
    source: Patricia_Mountbatten
    literal_type: xsd:integer
    literal_value: 2017
  AssignClass (bf682b3a-c496-45e9-9d5a-38a935b5a796)
 Call ID: bf682b3a-c496-45e9-9d5a-38a935b5a796
  Args:
    source: Earl_Mountbatten_of_Burma
    type: :Man
  AssignClass (2202c8f6-59ea-4a40-8c54-23a25ac72c10)
 Call ID: 2202c8f6-59ea-4a40-8c54-23a25ac72c10
  Args:
    source: Earl_Mountbatten_of_Burma
    type: :Person
  AssignClass (4ba4cb16-1a85-4be6-b577-d0a84f27de78)
 Call ID: 4ba4cb16-1a85-4be6-b577-d0a84f27de78
  Args:
    source: Earl_Mountbatten_of_Burma
    type: :Ancestor
  AddTriple (b8d51930-674f-461b-af26-640ea556fa90)
 Call ID: b8d51930-674f-461b-af26-640ea556fa90
  Args:
    source: Earl_Mountbatten_of_Burma
    relation: :isFatherOf
    target: Patricia_Mountbatten
  AssignClass (7a3ba511-9de4-48fc-997f-69ec6fc847ed)
 Call ID: 7a3ba511-9de4-48fc-997f-69ec6fc847ed
  Args:
    type: :Woman
    source: Edwina_Ashley
  AssignClass (1b404840-fab4-48d8-a160-87417cc217b6)
 Call ID: 1b404840-fab4-48d8-a160-87417cc217b6
  Args:
    source: Edwina_Ashley
    type: :Person
  AssignClass (ee8bb680-de50-4d76-b598-3ac4e28d6818)
 Call ID: ee8bb680-de50-4d76-b598-3ac4e28d6818
  Args:
    type: :Ancestor
    source: Edwina_Ashley
  AddTriple (fe876ea2-1b92-49a0-9155-8e4b2310e770)
 Call ID: fe876ea2-1b92-49a0-9155-8e4b2310e770
  Args:
    target: Patricia_Mountbatten
    source: Edwina_Ashley
    relation: :isMotherOf
  AssignClass (198d96ed-cfa8-4270-bb5a-0e56b907d168)
 Call ID: 198d96ed-cfa8-4270-bb5a-0e56b907d168
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AssignClass (ca783080-9d25-4aa3-a399-d9216f8c17e6)
 Call ID: ca783080-9d25-4aa3-a399-d9216f8c17e6
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AddTriple (e882ea3c-e79e-4cd6-8843-f349105396e2)
 Call ID: e882ea3c-e79e-4cd6-8843-f349105396e2
  Args:
    relation: :isSisterOf
    source: Patricia_Mountbatten
    target: Lady_Pamela_Hicks
  AssignClass (f7fa5236-67ee-4433-a848-7692f02b5d2d)
 Call ID: f7fa5236-67ee-4433-a848-7692f02b5d2d
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (8b4c951d-f781-4148-a12b-8d016c21e22f)
 Call ID: 8b4c951d-f781-4148-a12b-8d016c21e22f
  Args:
    source: John_Knatchbull
    type: :Person
  AddLiteral (249615db-f1a8-4224-90c0-5b006a206f8a)
 Call ID: 249615db-f1a8-4224-90c0-5b006a206f8a
  Args:
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasMarriageYear
    source: Patricia_Mountbatten
  AddTriple (4bdee52c-2a5e-44d5-b208-36b4cf891c8f)
 Call ID: 4bdee52c-2a5e-44d5-b208-36b4cf891c8f
  Args:
    target: John_Knatchbull
    source: Patricia_Mountbatten
    relation: :hasRelation
  AssignClass (ba960c45-fda5-4adb-9de7-53714c8238ce)
 Call ID: ba960c45-fda5-4adb-9de7-53714c8238ce
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (f6545542-9e68-4738-b168-b2399e77b7fe)
 Call ID: f6545542-9e68-4738-b168-b2399e77b7fe
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (7631b54f-34f6-4b03-a1a4-0cabcf924da7)
 Call ID: 7631b54f-34f6-4b03-a1a4-0cabcf924da7
  Args:
    target: Patricia_Mountbatten
    source: Nicholas_Knatchbull
    relation: :isSonOf
  AddTriple (ec64ec64-fefd-4f91-bac8-cee4092f5a24)
 Call ID: ec64ec64-fefd-4f91-bac8-cee4092f5a24
  Args:
    target: John_Knatchbull
    relation: :isSonOf
    source: Nicholas_Knatchbull
  AssignClass (48d52bf0-09b8-44f6-b6e4-e8eaf3021beb)
 Call ID: 48d52bf0-09b8-44f6-b6e4-e8eaf3021beb
  Args:
    source: Amanda_Knatchbull
    type: :Woman
  AssignClass (237a1026-5d5f-443a-be49-c8bfb66ba105)
 Call ID: 237a1026-5d5f-443a-be49-c8bfb66ba105
  Args:
    type: :Person
    source: Amanda_Knatchbull
  AddTriple (cad185cb-852a-46f1-b4d7-e2c2331e3c0a)
 Call ID: cad185cb-852a-46f1-b4d7-e2c2331e3c0a
  Args:
    source: Amanda_Knatchbull
    relation: :isDaughterOf
    target: Patricia_Mountbatten
  AddTriple (c3d92fc6-a039-44cc-ad9c-415dc5543bd7)
 Call ID: c3d92fc6-a039-44cc-ad9c-415dc5543bd7
  Args:
    relation: :isDaughterOf
    source: Amanda_Knatchbull
    target: John_Knatchbull
  Finish (448a7018-8699-4a9c-b87c-fc43c392ebbe)
 Call ID: 448a7018-8699-4a9c-b87c-fc43c392ebbe
  Args: