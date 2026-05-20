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
Zara Anne Elizabeth Tindall (née Phillips; born 15 May 1981) is a British equestrian, Olympian, and member of the British royal family.
She is the daughter of Anne, Princess Royal, and Captain Mark Phillips, and the eldest niece of King Charles III.
At birth she was sixth in the line of succession to the British throne during the reign of her maternal grandmother, Queen Elizabeth II, and as of 2026 is 22nd.
Tindall won the individual eventing world title at Aachen in 2006 and was later named BBC Sports Personality of the Year.
She married former rugby union player Mike Tindall in 2011, and the couple have three children.
Early life and education

Zara Anne Elizabeth Phillips was born at 8:15 pm on 15 May 1981 at St Mary's Hospital, London.
Her first name was suggested by her uncle, Charles, the then Prince of Wales.
Her godparents are her maternal uncle, Andrew Mountbatten-Windsor; the Countess of Lichfield; Helen, Lady Stewart, the wife of Sir Jackie Stewart; Andrew Parker Bowles; and Hugh Thomas.
She has an elder brother, Peter, and two younger half-sisters, Felicity Wade (née Tonkin), from her father's affair with Heather Tonkin; and Stephanie Phillips, from his second marriage to Sandy Pflueger.
Phillips attended Beaudesert Park School in Stroud, Gloucestershire, and Port Regis School in Shaftesbury, Dorset, before following other members of the royal family in attending Gordonstoun School in Moray, Scotland.
Equestrianism

After leaving university, Phillips began to pursue an equestrian career, following in the footsteps of her parents.
Phillips missed the 2004 Summer Olympics in Athens after her horse was injured during training.
Riding Toytown, Phillips won individual and team gold medals at the 2005 European Eventing Championship at Blenheim.
The British Olympic Association selected Phillips and Toytown for the 2008 Olympic Games in Hong Kong; however, Toytown sustained an injury during training and she withdrew from the team.
On 25 October 2008, Phillips fell from her horse, Tsunami II, at the 15th fence of a cross‐country event in Pau, France, breaking her right collarbone.
In July 2010, Musto launched a range of equestrian clothing designed by Phillips, named ZP176 after her team number when she first represented Great Britain.
Phillips competed at the 2012 London Olympic Games on High Kingdom, winning a silver medal in the team event.
She stopped using her maiden name in March 2016 and competed as Zara Tindall for the first time during her unsuccessful attempt to qualify for the 2016 Rio Olympic Games.
In 2017, Tindall finished third at the Kentucky Three-Day Event on High Kingdom, who retired from competition in 2018.
Charity work

Tindall frequently supports and attends events for a range of charitable causes, particularly those connected with spinal injuries, equestrianism, and children's welfare.
Tindall has appeared at events for The Caudwell Charitable Trust, which supports children with special needs, disabilities, and serious illnesses.
The following year, she became patron of the Mark Davies Injured Riders Fund.
In 2013, she visited Stroud Maternity Ward to mark its 60th anniversary, and in 2014 she lent her support to the #bringbackourgirls campaign.
In April 2020, Tindall participated in the Equestrian Relief initiative to help provide additional personal protective equipment for National Health Service workers.
Other activities

In June 2015, Tindall launched an equestrian-themed jewellery collection, named "Zara Phillips Collection", in collaboration with Australian designer John Calleija.
On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Tindall joined her brother and six cousins to mount a 15-minute vigil around the coffin of the Queen, as it lay in state at Westminster Hall.
On 19 September, with her husband Mike and daughter Mia, she joined other family members at the state funeral.
Personal life

Phillips met rugby union player Mike Tindall, who was then playing for the England national team, during the squad's Rugby World Cup-winning campaign in Australia in 2003.
As required at the time by the Royal Marriages Act 1772, the Queen gave her consent to the marriage at a meeting of the Privy Council on 10 May 2011.
A celebration was held on the royal yacht Britannia prior to the wedding.
The Tindalls lived in Cheltenham, Gloucestershire, before moving to Aston Farm, a seven-bedroom property adjoining the Princess Royal's Gatcombe Park estate.
Their first child, Mia Grace, was born on 17 January 2014 at Gloucestershire Royal Hospital and was 16th, later 23rd in the line of succession.
A second daughter, Lena Elizabeth, was born on 18 June 2018 at Stroud Maternity Hospital and was 19th, later 24th, in the line of succession.
Tindall is a godmother to Prince George of Wales, the son of her cousin William, Prince of Wales.
In December 2000, before her marriage, Phillips was involved in a serious car crash near Bourton-on-the-Water, escaping injury after overturning her Land Rover.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (62232b6e-2e2c-44f8-9856-8069d4b13ffd)
 Call ID: 62232b6e-2e2c-44f8-9856-8069d4b13ffd
  Args:
    type: :Woman
    source: :ZaraTindall
  AssignClass (f232df3d-923e-4f8b-9374-4f7e40867b3f)
 Call ID: f232df3d-923e-4f8b-9374-4f7e40867b3f
  Args:
    type: :Person
    source: :ZaraTindall
  AssignClass (65022786-0c2a-4503-9823-5dc319b7af5a)
 Call ID: 65022786-0c2a-4503-9823-5dc319b7af5a
  Args:
    source: :AnnePrincessRoyal
    type: :Woman
  AssignClass (a5f1dc1d-2861-4344-a7e7-bddd79ac14f3)
 Call ID: a5f1dc1d-2861-4344-a7e7-bddd79ac14f3
  Args:
    source: :AnnePrincessRoyal
    type: :Person
  AssignClass (6bc4eb54-8f5d-4108-a5e9-61df27a9be87)
 Call ID: 6bc4eb54-8f5d-4108-a5e9-61df27a9be87
  Args:
    type: :Man
    source: :MarkPhillips
  AssignClass (5cb9e161-4256-44f8-badc-bffdf62bf054)
 Call ID: 5cb9e161-4256-44f8-badc-bffdf62bf054
  Args:
    source: :MarkPhillips
    type: :Person
  AssignClass (af9941df-33fb-44bf-93be-b626fef42210)
 Call ID: af9941df-33fb-44bf-93be-b626fef42210
  Args:
    type: :Man
    source: :MikeTindall
  AssignClass (1aab437a-78c9-429f-a2d1-bf518ae00618)
 Call ID: 1aab437a-78c9-429f-a2d1-bf518ae00618
  Args:
    type: :Person
    source: :MikeTindall
  AssignClass (7e2cf8e2-69fe-4fab-8ee7-2689d4b09c6b)
 Call ID: 7e2cf8e2-69fe-4fab-8ee7-2689d4b09c6b
  Args:
    source: :PeterPhillips
    type: :Man
  AssignClass (13cf28dc-7f41-4d5f-8a0c-628051866ce5)
 Call ID: 13cf28dc-7f41-4d5f-8a0c-628051866ce5
  Args:
    type: :Person
    source: :PeterPhillips
  AssignClass (6c0171d9-b504-41a6-89de-509c5fdb4695)
 Call ID: 6c0171d9-b504-41a6-89de-509c5fdb4695
  Args:
    source: :MiaGraceTindall
    type: :Woman
  AssignClass (5f53fcd1-7c7c-4f0a-ad57-eaa26ba18fcc)
 Call ID: 5f53fcd1-7c7c-4f0a-ad57-eaa26ba18fcc
  Args:
    source: :MiaGraceTindall
    type: :Person
  AssignClass (92db6fba-b343-4978-a41c-9e54fb87db0e)
 Call ID: 92db6fba-b343-4978-a41c-9e54fb87db0e
  Args:
    type: :Woman
    source: :LenaElizabethTindall
  AssignClass (3ec9141a-325f-4710-b45a-6f9ca926d576)
 Call ID: 3ec9141a-325f-4710-b45a-6f9ca926d576
  Args:
    type: :Person
    source: :LenaElizabethTindall
  AddLiteral (9e54724d-9dfa-42d9-aaf5-3a094d334c85)
 Call ID: 9e54724d-9dfa-42d9-aaf5-3a094d334c85
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :ZaraTindall
    literal_value: 1981
  AddTriple (50d159db-6b10-407c-a1cf-53dfde3836e1)
 Call ID: 50d159db-6b10-407c-a1cf-53dfde3836e1
  Args:
    relation: :hasMother
    source: :ZaraTindall
    target: :AnnePrincessRoyal
  AddTriple (df373f73-6fab-4f8e-aa3d-28c8e532a4ad)
 Call ID: df373f73-6fab-4f8e-aa3d-28c8e532a4ad
  Args:
    relation: :hasFather
    source: :ZaraTindall
    target: :MarkPhillips
  AddLiteral (80fb71f3-cedc-482d-91b0-4027ff32f0af)
 Call ID: 80fb71f3-cedc-482d-91b0-4027ff32f0af
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :ZaraTindall
    literal_value: 2011
  AddTriple (eee5ce5a-17f2-4760-a740-907ff0c52cbc)
 Call ID: eee5ce5a-17f2-4760-a740-907ff0c52cbc
  Args:
    relation: :hasRelation
    source: :ZaraTindall
    target: :MikeTindall
  AddTriple (881150e6-001d-4486-9fd0-a5af953d1c59)
 Call ID: 881150e6-001d-4486-9fd0-a5af953d1c59
  Args:
    relation: :hasBrother
    source: :ZaraTindall
    target: :PeterPhillips
  AddTriple (e716c89d-04f6-4f81-823c-b34c94d098a8)
 Call ID: e716c89d-04f6-4f81-823c-b34c94d098a8
  Args:
    relation: :hasChild
    source: :ZaraTindall
    target: :MiaGraceTindall
  AddTriple (db5f755c-7602-44dd-82ff-2c694bf84a24)
 Call ID: db5f755c-7602-44dd-82ff-2c694bf84a24
  Args:
    relation: :hasChild
    source: :ZaraTindall
    target: :LenaElizabethTindall
  AddTriple (a7f37763-91e7-440e-ba31-a6074f9a9403)
 Call ID: a7f37763-91e7-440e-ba31-a6074f9a9403
  Args:
    target: :MikeTindall
    relation: :hasFather
    source: :MiaGraceTindall
  AddTriple (6a03fba0-391d-4308-ae60-c8cf37727567)
 Call ID: 6a03fba0-391d-4308-ae60-c8cf37727567
  Args:
    source: :LenaElizabethTindall
    relation: :hasFather
    target: :MikeTindall
  AddLiteral (a3b2960b-d77a-4a52-be7f-e49c7070b624)
 Call ID: a3b2960b-d77a-4a52-be7f-e49c7070b624
  Args:
    literal_value: Zara Phillips
    source: :ZaraTindall
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (b9e84813-62ce-457a-8124-bf3bdc12c407)
 Call ID: b9e84813-62ce-457a-8124-bf3bdc12c407
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: :ZaraTindall
    literal_value: Zara Tindall
  Finish (ac8d2954-d14d-4e57-9566-00d5b6d14aca)
 Call ID: ac8d2954-d14d-4e57-9566-00d5b6d14aca
  Args: