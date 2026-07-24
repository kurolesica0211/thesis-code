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
Lady Louise Alice Elizabeth Mary Mountbatten-Windsor (born 8 November 2003) is a member of the British royal family.
She is the elder child and only daughter of Prince Edward, Duke of Edinburgh, and Sophie, Duchess of Edinburgh.
Louise is the youngest niece of King Charles III.
She was born during the reign of her paternal grandmother, Queen Elizabeth II, and at the time of her birth was eighth in the line of succession to the British throne; as of 2026, she is 17th.
Early life and education

Lady Louise Alice Elizabeth Mary Mountbatten-Windsor was born prematurely at 11:32 pm on 8 November 2003 at Frimley Park Hospital, Surrey.
Her mother, Sophie, then Countess of Wessex, had been taken there by ambulance from the family home at Bagshot Park.
Her father, Prince Edward, then Earl of Wessex, and the youngest child of Queen Elizabeth II and Prince Philip, was not present for the birth, which occurred suddenly while he was on an official visit to Mauritius.
Louise was delivered by emergency Caesarean section due to a placental abruption that caused significant blood loss to both mother and child.
She was transferred to the neo-natal unit at St George's Hospital, Tooting, London, while her mother remained at Frimley Park.
Louise returned to Frimley Park on 13 November and was discharged on 23 November, four days after her mother.
Her name, Louise Alice Elizabeth Mary, was announced on 26 November.
She was baptised in the Private Chapel at Windsor Castle on 24 April 2004 by David Conner, the Dean of Windsor.
Her godparents are Lady Sarah Chatto, Lord Ivar Mountbatten, Lady Alexandra Etherington, Francesca Schwarzenbach, and Rupert Elliott.
Louise was the last child to wear the original royal christening gown.
Born with esotropia, Louise underwent an operation in 2006 in an unsuccessful attempt to correct the condition.
Louise attended St George's School, Windsor Castle, before moving to St Mary's School Ascot in 2017 from Year 9.
While at school, she took part in The Duke of Edinburgh's Award.
Louise began studying English at the University of St Andrews in September 2022.
Military training

In 2024, Louise joined the British Army's University Officers' Training Corps (UOTC) unit, Tayforth UOTC, an Army Reserve formation made up of students from the University of St Andrews and other institutions in the surrounding region.
Official appearances

In 2011, aged 7, Louise was a bridesmaid at the wedding of Prince William and Catherine Middleton.
In August 2018, she accompanied her mother, patron of UK Sail Training, to Haslar Marina in Portsmouth Harbour to meet a group of young girls working towards earning their qualification on an entry-level course of the Royal Yachting Association.
Later that month, mother and daughter attended the final of the Hockey Women's World Cup in London; the Duchess is the patron of England Hockey.
To celebrate Louise's 15th birthday in November 2018, they made a cameo appearance on Strictly Come Dancing, watching the BBC programme from the audience.
In December, Louise joined her mother at the International Horse Show at Olympia, London.
In September 2020, Louise participated in the Great British Beach Clean with her family at Southsea Beach, in support of the Marine Conservation Society.
Following the death of her grandfather, Prince Philip, Louise accompanied her parents to a church service at the Royal Chapel of All Saints on 11 April 2021.
She attended Trooping the Colour in June, where she joined her family on the balcony; the Platinum Jubilee National Service of Thanksgiving; and the Platinum Party at the Palace.
Following the death of her grandmother, Queen Elizabeth II, on 8 September 2022, Louise stood vigil for 15 minutes at the Queen's coffin at Westminster Hall with her brother James and six cousins on 17 September.
On 6 May 2023, Louise attended the coronation of King Charles III and Queen Camilla.
On 7 May, she attended the Coronation Concert at Windsor Castle.
Personal interests

Louise is a member of Girlguiding, of which her grandmother was patron and her mother is president.
Her mother was a Brownie and a Guide when she was a child.
Louise was taught to ride at an early age, and joined her father on horseback during the Queen's 90th birthday celebrations in Windsor in 2016.
She has taken up carriage driving, a sport popularised in Britain by her grandfather, Prince Philip.
In May 2017, she was responsible for leading the carriages of the Champagne Laurent-Perrier Meet of the British Driving Society at the Royal Windsor Horse Show.
In May 2019, Louise took part in the Private Driving Singles carriage drive at the Royal Windsor Horse Show and achieved third place.
In 2022, she drove one of his carriages in front of the Queen at the Royal Windsor Horse Show.
Titles, styles, and honours

Titles and styles

Louise is styled as "Lady Louise Mountbatten-Windsor", although at the time of her birth the palace also used the style "Lady Louise Windsor" in some of its announcements.
At birth, she automatically became a princess of the United Kingdom under the terms of the 1917 letters patent, which assigned princely status and the style of Royal Highness to all children of a monarch's sons.
However, when her parents married, Elizabeth II announced via a Buckingham Palace press release that their children would be styled as the children of an earl rather than as prince or princess.
In 2020, her mother stated that Louise retained her royal title and style and could choose whether to use it from the age of 18.
Honours

In June 2008, to recognise a visit by Louise's father to the Canadian province of Manitoba, a lake in the north of the province was named Lake Louise.



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
  AssignClass (c5c6a496-f148-41a4-be96-92125e1f6775)
 Call ID: c5c6a496-f148-41a4-be96-92125e1f6775
  Args:
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
    type: :Woman
  AssignClass (3d4d159e-4974-4bab-ad79-6ba2dff87938)
 Call ID: 3d4d159e-4974-4bab-ad79-6ba2dff87938
  Args:
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
    type: :Person
  AssignClass (beefb055-0503-4ad7-b511-d698a34bc193)
 Call ID: beefb055-0503-4ad7-b511-d698a34bc193
  Args:
    type: :Man
    source: Prince Edward, Duke of Edinburgh
  AssignClass (8e2dffae-0aef-4d63-8b73-fa1db60923e2)
 Call ID: 8e2dffae-0aef-4d63-8b73-fa1db60923e2
  Args:
    source: Prince Edward, Duke of Edinburgh
    type: :Person
  AssignClass (8ec5d10a-2f71-4912-af9d-363118104b9b)
 Call ID: 8ec5d10a-2f71-4912-af9d-363118104b9b
  Args:
    type: :Woman
    source: Sophie, Duchess of Edinburgh
  AssignClass (9bf1bd65-a9ba-4fcf-8434-29099be1ad9e)
 Call ID: 9bf1bd65-a9ba-4fcf-8434-29099be1ad9e
  Args:
    source: Sophie, Duchess of Edinburgh
    type: :Person
  AssignClass (e2e92804-8564-449e-b320-09184c77fba3)
 Call ID: e2e92804-8564-449e-b320-09184c77fba3
  Args:
    type: :Man
    source: King Charles III
  AssignClass (83287e81-b6c7-4fda-9847-4f24c3526ec0)
 Call ID: 83287e81-b6c7-4fda-9847-4f24c3526ec0
  Args:
    type: :Person
    source: King Charles III
  AssignClass (7f907b08-2d74-4200-9945-1ae335676c48)
 Call ID: 7f907b08-2d74-4200-9945-1ae335676c48
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AssignClass (3a649e88-3582-4bbc-ae21-37ed026d2f1a)
 Call ID: 3a649e88-3582-4bbc-ae21-37ed026d2f1a
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (c847ad3d-26b8-4ff4-af7a-c42d20ceac71)
 Call ID: c847ad3d-26b8-4ff4-af7a-c42d20ceac71
  Args:
    type: :Man
    source: Prince Philip
  AssignClass (fe0e781f-dc62-44f6-b808-74ea0c64b1c2)
 Call ID: fe0e781f-dc62-44f6-b808-74ea0c64b1c2
  Args:
    type: :Person
    source: Prince Philip
  AssignClass (39b6db05-4a65-409e-aea6-a36a43b9081a)
 Call ID: 39b6db05-4a65-409e-aea6-a36a43b9081a
  Args:
    source: James
    type: :Man
  AssignClass (61a01d34-3a3e-4511-964f-7dfc614ecbca)
 Call ID: 61a01d34-3a3e-4511-964f-7dfc614ecbca
  Args:
    source: James
    type: :Person
  AddLiteral (65524e95-eb9a-4174-97f8-918332aa0f9f)
 Call ID: 65524e95-eb9a-4174-97f8-918332aa0f9f
  Args:
    literal_type: xsd:integer
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
    literal_value: 2003
    relation: :hasBirthYear
  AddTriple (348219ac-e5eb-4a45-893f-3953096f7aea)
 Call ID: 348219ac-e5eb-4a45-893f-3953096f7aea
  Args:
    target: Prince Edward, Duke of Edinburgh
    relation: :hasFather
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
  AddTriple (fe2772b3-9f07-497b-bd2e-6518bc464f45)
 Call ID: fe2772b3-9f07-497b-bd2e-6518bc464f45
  Args:
    target: Sophie, Duchess of Edinburgh
    relation: :hasMother
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
  AddTriple (e34b3b8f-499d-4ab5-b048-864567c4bb1e)
 Call ID: e34b3b8f-499d-4ab5-b048-864567c4bb1e
  Args:
    relation: :hasFather
    target: Prince Philip
    source: Prince Edward, Duke of Edinburgh
  AddTriple (962e8f65-7237-4575-9715-ec23cf731d39)
 Call ID: 962e8f65-7237-4575-9715-ec23cf731d39
  Args:
    source: Prince Edward, Duke of Edinburgh
    target: Queen Elizabeth II
    relation: :hasMother
  AddTriple (7122de82-468c-4a2a-80af-c49c4299b08a)
 Call ID: 7122de82-468c-4a2a-80af-c49c4299b08a
  Args:
    source: Lady Louise Alice Elizabeth Mary Mountbatten-Windsor
    target: James
    relation: :hasBrother
  AddTriple (ab806488-da5a-445c-9329-fdb55a3595e3)
 Call ID: ab806488-da5a-445c-9329-fdb55a3595e3
  Args:
    relation: :hasParent
    target: Prince Edward, Duke of Edinburgh
    source: James
  AddTriple (bf8d9df0-f10b-4590-b912-bb2c12c9866d)
 Call ID: bf8d9df0-f10b-4590-b912-bb2c12c9866d
  Args:
    target: Sophie, Duchess of Edinburgh
    relation: :hasParent
    source: James
  Finish (375556c4-ad67-4f92-b6e0-15b6264f05cc)
 Call ID: 375556c4-ad67-4f92-b6e0-15b6264f05cc
  Args: