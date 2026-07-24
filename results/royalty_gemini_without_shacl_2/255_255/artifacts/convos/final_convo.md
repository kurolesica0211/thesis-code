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
  AssignClass (420880c5-c676-4c15-9b91-0cc1bd275c6b)
 Call ID: 420880c5-c676-4c15-9b91-0cc1bd275c6b
  Args:
    source: Patricia_Mountbatten
    type: :Woman
  AssignClass (d61883be-bc16-4b34-acbf-09659c9bf715)
 Call ID: d61883be-bc16-4b34-acbf-09659c9bf715
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AddLiteral (5f196336-b639-49ee-a5fc-d3919791b910)
 Call ID: 5f196336-b639-49ee-a5fc-d3919791b910
  Args:
    relation: :hasBirthYear
    literal_value: 1924
    source: Patricia_Mountbatten
    literal_type: xsd:integer
  AddLiteral (feeff5f2-e3a3-4c6d-8810-28adfe0a4fa5)
 Call ID: feeff5f2-e3a3-4c6d-8810-28adfe0a4fa5
  Args:
    literal_type: xsd:integer
    source: Patricia_Mountbatten
    relation: :hasDeathYear
    literal_value: 2017
  AssignClass (a5443ad0-9647-4048-8b46-5ffa3af9d44d)
 Call ID: a5443ad0-9647-4048-8b46-5ffa3af9d44d
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (20a618d4-5eff-4e6b-a32c-4bdedb25519d)
 Call ID: 20a618d4-5eff-4e6b-a32c-4bdedb25519d
  Args:
    type: :Person
    source: John_Knatchbull
  AddLiteral (d772d5a1-de8d-4e62-aa83-145be75a5923)
 Call ID: d772d5a1-de8d-4e62-aa83-145be75a5923
  Args:
    literal_type: xsd:integer
    source: John_Knatchbull
    literal_value: 1924
    relation: :hasBirthYear
  AddLiteral (c17b0f47-fdb7-4602-8fa6-5e822ba38f85)
 Call ID: c17b0f47-fdb7-4602-8fa6-5e822ba38f85
  Args:
    literal_value: 2005
    relation: :hasDeathYear
    source: John_Knatchbull
    literal_type: xsd:integer
  AddLiteral (cf47cd8a-0a76-4208-9e8e-6b1e30683193)
 Call ID: cf47cd8a-0a76-4208-9e8e-6b1e30683193
  Args:
    source: Patricia_Mountbatten
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasMarriageYear
  AddTriple (562b55c7-321b-4ab8-b2d5-de807ec8c115)
 Call ID: 562b55c7-321b-4ab8-b2d5-de807ec8c115
  Args:
    target: John_Knatchbull
    relation: :hasRelation
    source: Patricia_Mountbatten
  AssignClass (b190d3ad-6c88-411f-8a87-b7e22b5daa5f)
 Call ID: b190d3ad-6c88-411f-8a87-b7e22b5daa5f
  Args:
    type: :Man
    source: Earl_Mountbatten_of_Burma
  AssignClass (7ae904d1-b57e-4e0b-8c7d-3d4888a87d93)
 Call ID: 7ae904d1-b57e-4e0b-8c7d-3d4888a87d93
  Args:
    type: :Person
    source: Earl_Mountbatten_of_Burma
  AssignClass (407f2fce-89fb-4db6-bd9a-3c36141e0c89)
 Call ID: 407f2fce-89fb-4db6-bd9a-3c36141e0c89
  Args:
    source: Edwina_Ashley
    type: :Woman
  AssignClass (a2f8c8ae-e4bc-4332-bcd6-8b2c51713159)
 Call ID: a2f8c8ae-e4bc-4332-bcd6-8b2c51713159
  Args:
    type: :Person
    source: Edwina_Ashley
  AddTriple (1003235f-c40f-4c1e-b291-28b744373f1d)
 Call ID: 1003235f-c40f-4c1e-b291-28b744373f1d
  Args:
    source: Earl_Mountbatten_of_Burma
    target: Patricia_Mountbatten
    relation: :isFatherOf
  AddTriple (05ba2367-d9a4-42bb-ae42-9e248c61c079)
 Call ID: 05ba2367-d9a4-42bb-ae42-9e248c61c079
  Args:
    source: Edwina_Ashley
    relation: :isMotherOf
    target: Patricia_Mountbatten
  AssignClass (0b658337-f340-4aad-af52-713877ac3467)
 Call ID: 0b658337-f340-4aad-af52-713877ac3467
  Args:
    source: Lady_Pamela_Hicks
    type: :Woman
  AssignClass (786884fc-b16a-4314-9925-db40815191e5)
 Call ID: 786884fc-b16a-4314-9925-db40815191e5
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AddTriple (f875f10d-0e80-4a27-bb07-d7f5cd4ad5e4)
 Call ID: f875f10d-0e80-4a27-bb07-d7f5cd4ad5e4
  Args:
    source: Lady_Pamela_Hicks
    relation: :isSisterOf
    target: Patricia_Mountbatten
  AddTriple (be4e1ad5-a916-49a5-8dab-9e14fd4e01ef)
 Call ID: be4e1ad5-a916-49a5-8dab-9e14fd4e01ef
  Args:
    source: Earl_Mountbatten_of_Burma
    relation: :isFatherOf
    target: Lady_Pamela_Hicks
  AddTriple (eb329612-1977-4f6e-a580-221136246201)
 Call ID: eb329612-1977-4f6e-a580-221136246201
  Args:
    source: Edwina_Ashley
    target: Lady_Pamela_Hicks
    relation: :isMotherOf
  AssignClass (3177f86e-2303-4903-8674-06fac5d10a07)
 Call ID: 3177f86e-2303-4903-8674-06fac5d10a07
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (dd629e4e-6e3b-4571-8af1-ca18e9cfef95)
 Call ID: dd629e4e-6e3b-4571-8af1-ca18e9cfef95
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (8a710da4-41db-400d-83c9-eccc9b6399f5)
 Call ID: 8a710da4-41db-400d-83c9-eccc9b6399f5
  Args:
    source: Nicholas_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AddTriple (bbd86d0e-7265-439d-95ae-b087fac82ae1)
 Call ID: bbd86d0e-7265-439d-95ae-b087fac82ae1
  Args:
    source: Nicholas_Knatchbull
    target: John_Knatchbull
    relation: :isSonOf
  AssignClass (4c475111-608f-4c6e-ad57-38dd8161587c)
 Call ID: 4c475111-608f-4c6e-ad57-38dd8161587c
  Args:
    source: Amanda_Knatchbull
    type: :Woman
  AssignClass (87b70bf1-20d1-4b67-8cf8-137979365d8c)
 Call ID: 87b70bf1-20d1-4b67-8cf8-137979365d8c
  Args:
    type: :Person
    source: Amanda_Knatchbull
  AddTriple (378705a4-ad87-4331-baff-64b43d99057c)
 Call ID: 378705a4-ad87-4331-baff-64b43d99057c
  Args:
    relation: :isDaughterOf
    target: Patricia_Mountbatten
    source: Amanda_Knatchbull
  AddTriple (be891f3e-8fd6-46ed-804e-95e84cef56c3)
 Call ID: be891f3e-8fd6-46ed-804e-95e84cef56c3
  Args:
    relation: :isDaughterOf
    target: John_Knatchbull
    source: Amanda_Knatchbull
  Finish (c967b11d-3a89-45ee-baf0-89c8a39aeb68)
 Call ID: c967b11d-3a89-45ee-baf0-89c8a39aeb68
  Args: