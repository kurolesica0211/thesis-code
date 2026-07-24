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
Peter Mark Andrew Phillips (born 15 November 1977) is a British businessman and member of the British royal family.
He is the son of Anne, Princess Royal, and Mark Phillips, and a nephew of King Charles III.
Born during the reign of his maternal grandmother Queen Elizabeth II, Phillips was fifth in the line of succession to the British throne; as of 2026, he is 19th.
Phillips attended the University of Exeter and later worked for Jaguar Racing.
In 2008, he married Canadian management consultant Autumn Kelly at St George's Chapel, Windsor Castle; they have two children.
Early life and education

Peter Mark Andrew Phillips was born at 10:46 am on 15 November 1977 at St Mary's Hospital, London.
He was the first child of Princess Anne and Mark Phillips, who had married in 1973, and the first grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
He was baptised on 22 December by the Archbishop of Canterbury Donald Coggan in the Music Room of Buckingham Palace.
His godparents were his maternal uncle, Prince Charles; Geoffrey Tiarks; Captain Hamish Lochore; Lady Cecil Cameron of Lochiel and Jane Holderness-Roddam.
Phillips was fifth in line to the throne at birth and remained so until the birth of his cousin William, Prince of Wales in 1982.
His parents were said to have refused offers from his grandmother Queen Elizabeth II that would have led to his being born in the peerage.
Phillips was the first legitimate grandchild of a monarch in more than 500 years to be born without a title or courtesy title.
Phillips has a younger sister, Zara Tindall (née Phillips; born 1981), and two younger half-sisters, Felicity Wade (née Tonkin; born 1985), the daughter of Mark Phillips and his former mistress Heather Tonkin; and Stephanie Phillips (born 1997), the daughter from his father's second marriage to Sandy Pflueger.
Phillips went to Port Regis Prep School in Shaftesbury, Dorset before following some of his family by attending Gordonstoun School in Moray, Scotland.
Phillips represented Scotland at rugby union at youth and junior level in the mid-1990s.
Career

After his graduation in 2000, Phillips worked for Jaguar as corporate hospitality manager and then for Williams racing team, where he was sponsorship accounts manager.
He left Williams in September 2005, for a job as a manager at the Royal Bank of Scotland in Edinburgh.
In the year leading up to June 2016, Phillips was responsible for organising the "Patron's Lunch", in celebration of the Queen's 90th birthday.
In January 2020, Phillips appeared in an advertisement for Chinese company Bright Food.
In the video, he uses his status as a "British royal family member" to promote the company's milk, while surrounded by luxury.
Royal funeral participation

On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Phillips joined his sister and six cousins to mount a 15-minute vigil around the coffin of their grandmother as it lay in state at Westminster Hall.
On 19 September 2022, he joined the Queen's children and other senior members of the royal family in walking behind the cortege in the state funeral procession.
Personal life

Relationships

Elizabeth Iorio and Tara Swain

Phillips dated Elizabeth Iorio, a cod liver oil heiress from the United States, for two years.
Autumn Kelly

In 2003, Phillips met Autumn Kelly, a Canadian management consultant, at the Formula 1 Canadian Grand Prix in Montreal.
If she had been Roman Catholic at the time of the marriage, Phillips would have lost his place in the line of the succession to the throne because of since-repealed terms of the Act of Settlement 1701.
Shortly before their wedding, the couple were interviewed and photographed by Hello! magazine, and were reported to have been paid £500,000, resulting in some concern in royal circles.
The couple lived in Hong Kong after Phillips changed positions within the Royal Bank of Scotland and became head of their sponsorships activities in the region.
Their first child, and the Queen's first great-grandchild, a daughter named Savannah Anne Kathleen, was born on 29 December 2010 at Gloucestershire Royal Hospital.
The Queen was present for the baby's baptism, which took place on 23 April 2011 at Church of the Holy Cross in Avening, Gloucestershire, near Gatcombe Park, the home of Phillips' mother.
Savannah was born 12th in the line to the throne and is now 20th.
On 29 March 2012, the couple's second daughter, Isla Elizabeth, was born at Gloucestershire Royal Hospital.
She was born 13th in the line to the throne and is now 21st.
On 11 February 2020, Phillips and his wife confirmed that they had separated in 2019 and announced they were planning to divorce.
Lindsay Wallace

After his divorce, Phillips began a relationship with Lindsay Wallace in 2021, with whom he made his official debut as a couple at the Epsom Derby in June 2022.
Harriet Sperling

By June 2024, Phillips had introduced his partner, NHS paediatric nurse and freelance writer Harriet Sperling (née Sanders; born 1980), to King Charles III and Queen Camilla.
According to the BBC, Sperling is a distant relation of Prince Richard, Duke of Gloucester through her father Rupert Sanders (1946–2023).



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
  AssignClass (f8cecbfa-49df-4e48-bc9e-c3db355db69b)
 Call ID: f8cecbfa-49df-4e48-bc9e-c3db355db69b
  Args:
    type: :Man
    source: :Peter_Phillips
  AssignClass (400039da-7fca-4a71-abbb-640610fedb6a)
 Call ID: 400039da-7fca-4a71-abbb-640610fedb6a
  Args:
    type: :Person
    source: :Peter_Phillips
  AddLiteral (e740f56c-a367-4bfe-a6c1-b83828cb244c)
 Call ID: e740f56c-a367-4bfe-a6c1-b83828cb244c
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    source: :Peter_Phillips
    relation: :hasBirthYear
  AssignClass (aea7d68c-726c-42f1-9ea7-afa6c3c8851b)
 Call ID: aea7d68c-726c-42f1-9ea7-afa6c3c8851b
  Args:
    type: :Woman
    source: :Anne_Princess_Royal
  AssignClass (41107178-6cf6-4878-b7ec-7ea9f5dfe194)
 Call ID: 41107178-6cf6-4878-b7ec-7ea9f5dfe194
  Args:
    type: :Person
    source: :Anne_Princess_Royal
  AssignClass (6e9f1b1a-ac9b-44a9-9c08-595d03780ff6)
 Call ID: 6e9f1b1a-ac9b-44a9-9c08-595d03780ff6
  Args:
    type: :Man
    source: :Mark_Phillips
  AssignClass (13245482-65e0-458b-923c-fea328553f0d)
 Call ID: 13245482-65e0-458b-923c-fea328553f0d
  Args:
    type: :Person
    source: :Mark_Phillips
  AddTriple (10f85e7d-73a7-4cbe-b83c-77802bcc6a41)
 Call ID: 10f85e7d-73a7-4cbe-b83c-77802bcc6a41
  Args:
    source: :Peter_Phillips
    relation: :hasFather
    target: :Mark_Phillips
  AddTriple (10a5e8be-7022-4449-9d38-c433dea37516)
 Call ID: 10a5e8be-7022-4449-9d38-c433dea37516
  Args:
    source: :Peter_Phillips
    relation: :hasMother
    target: :Anne_Princess_Royal
  AssignClass (5e29e1ab-7b8a-4cc3-bbb5-3dd236621aa7)
 Call ID: 5e29e1ab-7b8a-4cc3-bbb5-3dd236621aa7
  Args:
    type: :Woman
    source: :Zara_Tindall
  AssignClass (6424f35c-1eff-47d7-a113-6e9272a5c1f5)
 Call ID: 6424f35c-1eff-47d7-a113-6e9272a5c1f5
  Args:
    type: :Person
    source: :Zara_Tindall
  AddTriple (c483bb23-9de9-4ea5-9386-daec228f5a72)
 Call ID: c483bb23-9de9-4ea5-9386-daec228f5a72
  Args:
    target: :Zara_Tindall
    source: :Peter_Phillips
    relation: :isSiblingOf
  AssignClass (f94bd5ca-67ca-4798-ba7d-02098abbc9c8)
 Call ID: f94bd5ca-67ca-4798-ba7d-02098abbc9c8
  Args:
    type: :Woman
    source: :Felicity_Wade
  AssignClass (573f4ad7-ad2e-47cc-8f96-7a4107388c88)
 Call ID: 573f4ad7-ad2e-47cc-8f96-7a4107388c88
  Args:
    type: :Person
    source: :Felicity_Wade
  AddTriple (1b8d7d5d-0593-41f9-b6e4-264d3c4ab626)
 Call ID: 1b8d7d5d-0593-41f9-b6e4-264d3c4ab626
  Args:
    relation: :hasFather
    source: :Felicity_Wade
    target: :Mark_Phillips
  AssignClass (31b82a36-2fe8-4a6f-878d-ad1af278ce01)
 Call ID: 31b82a36-2fe8-4a6f-878d-ad1af278ce01
  Args:
    type: :Woman
    source: :Stephanie_Phillips
  AssignClass (70be7c5b-04c2-40f1-babf-8321209b35ad)
 Call ID: 70be7c5b-04c2-40f1-babf-8321209b35ad
  Args:
    type: :Person
    source: :Stephanie_Phillips
  AddTriple (641dc299-6f76-4763-8a29-bdbee1ef0d4f)
 Call ID: 641dc299-6f76-4763-8a29-bdbee1ef0d4f
  Args:
    relation: :hasFather
    source: :Stephanie_Phillips
    target: :Mark_Phillips
  AssignClass (af7200d7-9e84-4359-a014-1be04aff4972)
 Call ID: af7200d7-9e84-4359-a014-1be04aff4972
  Args:
    type: :Woman
    source: :Autumn_Kelly
  AssignClass (02764a4e-d262-4c06-bef2-09f9e2a71d82)
 Call ID: 02764a4e-d262-4c06-bef2-09f9e2a71d82
  Args:
    type: :Person
    source: :Autumn_Kelly
  AddLiteral (51849802-dd9e-4769-b2f7-6231108b7276)
 Call ID: 51849802-dd9e-4769-b2f7-6231108b7276
  Args:
    literal_value: 2008
    literal_type: xsd:integer
    source: :Peter_Phillips
    relation: :hasMarriageYear
  AddTriple (ac25e5fb-c830-45df-a441-918c1ab8f356)
 Call ID: ac25e5fb-c830-45df-a441-918c1ab8f356
  Args:
    source: :Peter_Phillips
    relation: :hasRelation
    target: :Autumn_Kelly
  AssignClass (f7b8118f-e350-4ffd-95be-9265fc7b98b8)
 Call ID: f7b8118f-e350-4ffd-95be-9265fc7b98b8
  Args:
    type: :Woman
    source: :Savannah_Phillips
  AssignClass (181a2a9c-0cc0-4868-8af0-a495441f0bdf)
 Call ID: 181a2a9c-0cc0-4868-8af0-a495441f0bdf
  Args:
    type: :Person
    source: :Savannah_Phillips
  AddTriple (48b7f1b1-c8bc-440d-a0fc-09594230ba6c)
 Call ID: 48b7f1b1-c8bc-440d-a0fc-09594230ba6c
  Args:
    relation: :hasFather
    source: :Savannah_Phillips
    target: :Peter_Phillips
  AddTriple (2ea4db1c-56f8-4214-b81b-d62df301a0ed)
 Call ID: 2ea4db1c-56f8-4214-b81b-d62df301a0ed
  Args:
    source: :Savannah_Phillips
    relation: :hasMother
    target: :Autumn_Kelly
  AssignClass (fb64b405-c901-4987-a7b6-45e18dcaeaa8)
 Call ID: fb64b405-c901-4987-a7b6-45e18dcaeaa8
  Args:
    type: :Woman
    source: :Isla_Phillips
  AssignClass (7cc02557-f138-46ab-a4b0-d494e510d552)
 Call ID: 7cc02557-f138-46ab-a4b0-d494e510d552
  Args:
    type: :Person
    source: :Isla_Phillips
  AddTriple (14a70065-594c-4e8a-9c78-6ecac585f801)
 Call ID: 14a70065-594c-4e8a-9c78-6ecac585f801
  Args:
    relation: :hasFather
    source: :Isla_Phillips
    target: :Peter_Phillips
  AddTriple (c8aafa26-6e26-4d46-b203-a1c97cb5d04c)
 Call ID: c8aafa26-6e26-4d46-b203-a1c97cb5d04c
  Args:
    target: :Autumn_Kelly
    relation: :hasMother
    source: :Isla_Phillips
  AssignClass (2698bc23-3d6f-4c94-b69f-6be70379bfe4)
 Call ID: 2698bc23-3d6f-4c94-b69f-6be70379bfe4
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (09ecf4f8-51c2-41fa-bb21-b390e9c8f89d)
 Call ID: 09ecf4f8-51c2-41fa-bb21-b390e9c8f89d
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (a49047e1-e804-4877-bb05-e98cba7c862a)
 Call ID: a49047e1-e804-4877-bb05-e98cba7c862a
  Args:
    source: :Queen_Elizabeth_II
    relation: :isMotherOf
    target: :Anne_Princess_Royal
  AssignClass (92f6c5d6-a040-4800-bbd4-3a0eeb4ada74)
 Call ID: 92f6c5d6-a040-4800-bbd4-3a0eeb4ada74
  Args:
    type: :Man
    source: :King_Charles_III
  AssignClass (957d7e28-5730-47c9-91d0-235c485c21d7)
 Call ID: 957d7e28-5730-47c9-91d0-235c485c21d7
  Args:
    type: :Person
    source: :King_Charles_III
  AddTriple (6b9916e5-1ae1-41d2-9f99-9215e79f8c2c)
 Call ID: 6b9916e5-1ae1-41d2-9f99-9215e79f8c2c
  Args:
    relation: :hasSister
    source: :King_Charles_III
    target: :Anne_Princess_Royal
  AssignClass (5ab9baa3-eed5-42bb-aac5-8860d79589fa)
 Call ID: 5ab9baa3-eed5-42bb-aac5-8860d79589fa
  Args:
    type: :Man
    source: :Prince_Philip
  AssignClass (2def79c0-6522-4101-af87-49827255e789)
 Call ID: 2def79c0-6522-4101-af87-49827255e789
  Args:
    type: :Person
    source: :Prince_Philip
  AddTriple (24a3f79d-9cab-467f-a1df-b872248eec20)
 Call ID: 24a3f79d-9cab-467f-a1df-b872248eec20
  Args:
    source: :Anne_Princess_Royal
    relation: :hasFather
    target: :Prince_Philip
  AddTriple (bd2a857d-dcdc-4259-b16d-727a37965535)
 Call ID: bd2a857d-dcdc-4259-b16d-727a37965535
  Args:
    target: :Queen_Elizabeth_II
    source: :Anne_Princess_Royal
    relation: :hasMother
  Finish (2babafc9-9b76-4ce9-ba9d-80e0c47e98a7)
 Call ID: 2babafc9-9b76-4ce9-ba9d-80e0c47e98a7
  Args: