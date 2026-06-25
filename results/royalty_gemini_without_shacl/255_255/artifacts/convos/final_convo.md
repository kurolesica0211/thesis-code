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
  AssignClass (13796fb3-99ff-44d9-948a-6e5b9f43bb3f)
 Call ID: 13796fb3-99ff-44d9-948a-6e5b9f43bb3f
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (3e72dbb7-78eb-4025-9f8a-98713d67a58f)
 Call ID: 3e72dbb7-78eb-4025-9f8a-98713d67a58f
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddLiteral (6f1eaa84-d1ef-4139-a08e-7373248e271c)
 Call ID: 6f1eaa84-d1ef-4139-a08e-7373248e271c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1924
    source: Patricia_Mountbatten
  AddLiteral (f714d55e-829b-4a75-9589-9c83185ec285)
 Call ID: f714d55e-829b-4a75-9589-9c83185ec285
  Args:
    literal_type: xsd:integer
    literal_value: 2017
    source: Patricia_Mountbatten
    relation: :hasDeathYear
  AssignClass (70d2f5f4-fac9-42f7-bc4e-c062eeec4f85)
 Call ID: 70d2f5f4-fac9-42f7-bc4e-c062eeec4f85
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (d81b0d40-f5c4-46fc-b30b-539ed0c33e8f)
 Call ID: d81b0d40-f5c4-46fc-b30b-539ed0c33e8f
  Args:
    source: John_Knatchbull
    type: :Person
  AddLiteral (613fc9ab-a0d1-49b7-a55c-af985b597ceb)
 Call ID: 613fc9ab-a0d1-49b7-a55c-af985b597ceb
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    source: John_Knatchbull
    relation: :hasBirthYear
  AddLiteral (54aa3fb8-832d-4cca-a440-075401b3f617)
 Call ID: 54aa3fb8-832d-4cca-a440-075401b3f617
  Args:
    literal_type: xsd:integer
    source: John_Knatchbull
    literal_value: 2005
    relation: :hasDeathYear
  AddLiteral (08e32f07-5d13-4948-89c4-051f53a3a603)
 Call ID: 08e32f07-5d13-4948-89c4-051f53a3a603
  Args:
    literal_type: xsd:integer
    source: Patricia_Mountbatten
    literal_value: 1946
    relation: :hasMarriageYear
  AddTriple (7257efed-0a05-4fd5-91ce-78e930bcc261)
 Call ID: 7257efed-0a05-4fd5-91ce-78e930bcc261
  Args:
    target: John_Knatchbull
    source: Patricia_Mountbatten
    relation: :hasRelation
  AssignClass (f98a5b38-a206-446f-85a4-9549a3c323d9)
 Call ID: f98a5b38-a206-446f-85a4-9549a3c323d9
  Args:
    source: Earl_Mountbatten_of_Burma
    type: :Man
  AssignClass (488f7643-f34e-4674-9a02-fdfb741dd33f)
 Call ID: 488f7643-f34e-4674-9a02-fdfb741dd33f
  Args:
    type: :Person
    source: Earl_Mountbatten_of_Burma
  AssignClass (0c7fb9a3-dbff-4ed0-a178-b22a5ad5b7a1)
 Call ID: 0c7fb9a3-dbff-4ed0-a178-b22a5ad5b7a1
  Args:
    source: Edwina_Ashley
    type: :Woman
  AssignClass (bccbb03a-c534-42de-889e-6faf47b6272a)
 Call ID: bccbb03a-c534-42de-889e-6faf47b6272a
  Args:
    type: :Person
    source: Edwina_Ashley
  AddTriple (68b655cf-f744-43b0-bdb3-8c8d4ebe499b)
 Call ID: 68b655cf-f744-43b0-bdb3-8c8d4ebe499b
  Args:
    target: Earl_Mountbatten_of_Burma
    source: Patricia_Mountbatten
    relation: :hasFather
  AddTriple (37bdff94-6e7a-4af2-bbae-b5d7cf2808cc)
 Call ID: 37bdff94-6e7a-4af2-bbae-b5d7cf2808cc
  Args:
    relation: :hasMother
    target: Edwina_Ashley
    source: Patricia_Mountbatten
  AssignClass (9bb353b9-415b-4655-937d-d974ef25469e)
 Call ID: 9bb353b9-415b-4655-937d-d974ef25469e
  Args:
    source: Lady_Pamela_Hicks
    type: :Woman
  AssignClass (c300fb6b-0e71-49dd-af14-1e4976d3f43b)
 Call ID: c300fb6b-0e71-49dd-af14-1e4976d3f43b
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AddTriple (89b8ef8f-6277-4f3a-bc88-af7a596ee4c8)
 Call ID: 89b8ef8f-6277-4f3a-bc88-af7a596ee4c8
  Args:
    target: Lady_Pamela_Hicks
    source: Patricia_Mountbatten
    relation: :isSisterOf
  AssignClass (1cd26ecd-ea18-41f7-b9d8-dcaa617639dd)
 Call ID: 1cd26ecd-ea18-41f7-b9d8-dcaa617639dd
  Args:
    type: :Woman
    source: Amanda_Knatchbull
  AssignClass (5d164622-f1f5-459b-90cd-ecdda654900b)
 Call ID: 5d164622-f1f5-459b-90cd-ecdda654900b
  Args:
    source: Amanda_Knatchbull
    type: :Person
  AddTriple (1df3fa4a-e1a5-4c36-b281-5f4918467b00)
 Call ID: 1df3fa4a-e1a5-4c36-b281-5f4918467b00
  Args:
    relation: :isDaughterOf
    target: Patricia_Mountbatten
    source: Amanda_Knatchbull
  AddTriple (6cbf2178-1cd1-4a83-a636-d0f900f7d124)
 Call ID: 6cbf2178-1cd1-4a83-a636-d0f900f7d124
  Args:
    target: John_Knatchbull
    source: Amanda_Knatchbull
    relation: :isDaughterOf
  AssignClass (19558ed4-c1be-4dd5-ae7a-74c75872670e)
 Call ID: 19558ed4-c1be-4dd5-ae7a-74c75872670e
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (368f3bcb-5c51-4f98-bcbf-4138e35d3d04)
 Call ID: 368f3bcb-5c51-4f98-bcbf-4138e35d3d04
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (de6248d3-75f2-4cfc-b969-d09ed2bd5e2d)
 Call ID: de6248d3-75f2-4cfc-b969-d09ed2bd5e2d
  Args:
    relation: :isSonOf
    target: Patricia_Mountbatten
    source: Nicholas_Knatchbull
  AddTriple (05f27823-fb5f-4c13-bc2c-40dde33e1a12)
 Call ID: 05f27823-fb5f-4c13-bc2c-40dde33e1a12
  Args:
    target: John_Knatchbull
    source: Nicholas_Knatchbull
    relation: :isSonOf
  Finish (88983b89-445b-41dc-a98f-665327fd5403)
 Call ID: 88983b89-445b-41dc-a98f-665327fd5403
  Args: