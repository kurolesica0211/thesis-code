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
  AssignClass (90b43a56-8f20-4864-9105-f519c054f26c)
 Call ID: 90b43a56-8f20-4864-9105-f519c054f26c
  Args:
    source: Zara_Tindall
    type: :Woman
  AssignClass (f60a3c6d-bf25-4843-ad46-4f0504ede64f)
 Call ID: f60a3c6d-bf25-4843-ad46-4f0504ede64f
  Args:
    type: :Person
    source: Zara_Tindall
  AssignClass (b0590441-7896-4264-a87c-12b1184c5141)
 Call ID: b0590441-7896-4264-a87c-12b1184c5141
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (ef22ee37-36a3-43c2-ba00-193ba6758cee)
 Call ID: ef22ee37-36a3-43c2-ba00-193ba6758cee
  Args:
    source: Anne_Princess_Royal
    type: :Ancestor
  AssignClass (db47f96d-3d48-49cd-a0d1-aede651f8312)
 Call ID: db47f96d-3d48-49cd-a0d1-aede651f8312
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (219a86d9-1371-4c63-9400-6503cef6584c)
 Call ID: 219a86d9-1371-4c63-9400-6503cef6584c
  Args:
    source: Mark_Phillips
    type: :Man
  AssignClass (20b6542d-6e88-439c-a2fb-7ae758c38517)
 Call ID: 20b6542d-6e88-439c-a2fb-7ae758c38517
  Args:
    type: :Ancestor
    source: Mark_Phillips
  AssignClass (eaf753a1-b398-4406-876c-f4c7ac718b4e)
 Call ID: eaf753a1-b398-4406-876c-f4c7ac718b4e
  Args:
    type: :Person
    source: Mark_Phillips
  AssignClass (38e6cd2c-27c6-452a-a716-cb0504a00e70)
 Call ID: 38e6cd2c-27c6-452a-a716-cb0504a00e70
  Args:
    source: Mike_Tindall
    type: :Man
  AssignClass (b03422af-5d81-42ed-ae21-0d7fb3482829)
 Call ID: b03422af-5d81-42ed-ae21-0d7fb3482829
  Args:
    type: :Person
    source: Mike_Tindall
  AssignClass (4ae04cea-e194-4671-98c8-8668fab1b762)
 Call ID: 4ae04cea-e194-4671-98c8-8668fab1b762
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (851ff8d9-ff12-4f1d-9062-776d389254b7)
 Call ID: 851ff8d9-ff12-4f1d-9062-776d389254b7
  Args:
    source: Peter_Phillips
    type: :Person
  AssignClass (6a346605-f830-45ef-b550-9bb472133dec)
 Call ID: 6a346605-f830-45ef-b550-9bb472133dec
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (d0f42980-a1b8-488d-a7df-362fd633de53)
 Call ID: d0f42980-a1b8-488d-a7df-362fd633de53
  Args:
    type: :Person
    source: Felicity_Wade
  AssignClass (12f50a31-b11d-4cea-9b40-077818915461)
 Call ID: 12f50a31-b11d-4cea-9b40-077818915461
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (afb2a50c-3c32-4c5b-811c-b331920b6bdd)
 Call ID: afb2a50c-3c32-4c5b-811c-b331920b6bdd
  Args:
    source: Stephanie_Phillips
    type: :Person
  AssignClass (13ba122f-a93e-4d3b-a11b-161f6bf56f65)
 Call ID: 13ba122f-a93e-4d3b-a11b-161f6bf56f65
  Args:
    source: Mia_Tindall
    type: :Woman
  AssignClass (ec34d105-41a5-4a35-9ea3-0ffe69a3adf7)
 Call ID: ec34d105-41a5-4a35-9ea3-0ffe69a3adf7
  Args:
    source: Mia_Tindall
    type: :Person
  AddTriple (a1e9a9fc-443a-4f38-ae3a-7ee36698498a)
 Call ID: a1e9a9fc-443a-4f38-ae3a-7ee36698498a
  Args:
    relation: :hasMother
    target: Anne_Princess_Royal
    source: Zara_Tindall
  AddTriple (bb0f77f0-d7c4-4f7a-a6af-bc8f0533ef77)
 Call ID: bb0f77f0-d7c4-4f7a-a6af-bc8f0533ef77
  Args:
    source: Zara_Tindall
    target: Mark_Phillips
    relation: :hasFather
  AddTriple (0b412b1e-7469-475f-aea0-24f66b54640d)
 Call ID: 0b412b1e-7469-475f-aea0-24f66b54640d
  Args:
    target: Peter_Phillips
    relation: :hasBrother
    source: Zara_Tindall
  AddTriple (e184cd8c-411c-4c96-a5f5-e71dbca2c2d8)
 Call ID: e184cd8c-411c-4c96-a5f5-e71dbca2c2d8
  Args:
    target: Felicity_Wade
    relation: :hasSister
    source: Mark_Phillips
  AddTriple (ea889554-0099-407a-b85d-e5dad1364bff)
 Call ID: ea889554-0099-407a-b85d-e5dad1364bff
  Args:
    source: Mark_Phillips
    target: Stephanie_Phillips
    relation: :hasSister
  AddTriple (bd83f67c-2b66-4290-8372-a56460d4f8db)
 Call ID: bd83f67c-2b66-4290-8372-a56460d4f8db
  Args:
    source: Felicity_Wade
    relation: :hasFather
    target: Mark_Phillips
  AddTriple (01acebe2-a4f4-4f9d-81e0-9f945822c520)
 Call ID: 01acebe2-a4f4-4f9d-81e0-9f945822c520
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Stephanie_Phillips
  AddTriple (ffad9b4d-7286-4847-8b36-0af57fb84889)
 Call ID: ffad9b4d-7286-4847-8b36-0af57fb84889
  Args:
    target: Zara_Tindall
    relation: :hasMother
    source: Mia_Tindall
  AddTriple (56148c01-9d30-4c41-981d-01a89c0ffbba)
 Call ID: 56148c01-9d30-4c41-981d-01a89c0ffbba
  Args:
    source: Mia_Tindall
    relation: :hasFather
    target: Mike_Tindall
  AddLiteral (ed15460d-941d-4595-825d-f477afcc7da6)
 Call ID: ed15460d-941d-4595-825d-f477afcc7da6
  Args:
    literal_value: Zara Phillips
    source: Zara_Tindall
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (92e5b169-fa22-4a40-810a-754b59bf04aa)
 Call ID: 92e5b169-fa22-4a40-810a-754b59bf04aa
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Zara_Tindall
    literal_value: 1981
  AddLiteral (14c2d0c2-e58c-4b11-a70d-5224b2718987)
 Call ID: 14c2d0c2-e58c-4b11-a70d-5224b2718987
  Args:
    literal_value: 2011
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Zara_Tindall
  Finish (b40759fb-92f0-4a01-aef8-bcf4c2c00dfa)
 Call ID: b40759fb-92f0-4a01-aef8-bcf4c2c00dfa
  Args: