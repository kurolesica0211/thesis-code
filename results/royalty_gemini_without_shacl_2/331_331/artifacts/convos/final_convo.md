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
James Alexander Philip Theo Mountbatten-Windsor, Earl of Wessex (born 17 December 2007), styled Viscount Severn until 2023, is a member of the British royal family.
He is the younger child and only son of Prince Edward, Duke of Edinburgh, and Sophie, Duchess of Edinburgh.
James is the youngest grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh, and a nephew of King Charles III.
He was born during the reign of his paternal grandmother and was eighth in the line of succession to the British throne at the time of his birth; as of 2026, he is 16th.
Infancy

James Alexander Philip Theo Mountbatten-Windsor was born at 4:20 pm on 17 December 2007 at Frimley Park Hospital, Surrey by caesarean section.
His father Prince Edward, Duke of Edinburgh, is the youngest child of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
His mother Sophie, Duchess of Edinburgh, worked in public relations before becoming a full-time member of the royal family after her marriage in 1999.
His full name, James Alexander Philip Theo, was announced on 21 December.
James was baptised on 19 April 2008 in the private chapel at Windsor Castle by David Conner, Dean of Windsor, witnessed by his godparents, Alastair Bruce, Duncan Bullivant, Thomas Hill, Denise Poulton, Jeanye Irwin, and his paternal grandparents, Elizabeth II and Prince Philip.
Education

James attended Eagle House School, a coeducational preparatory school near Sandhurst, Berkshire, from 2011 to 2021, before enrolling at the private Radley College in Oxfordshire.
Official appearances

James made his first official appearance in the carriage procession at Trooping the Colour in 2016, and also took part in the 2022 Trooping the Colour.
Following the thanksgiving memorial service for his grandfather Prince Philip on 29 March 2022, James attended the Platinum Jubilee National Service of Thanksgiving and the Platinum Party at the Palace in June 2022.
On 17 September 2022, during the period of official mourning for his grandmother Queen Elizabeth II, James joined his sister Louise and six cousins in mounting a 15-minute vigil around the Queen's coffin as it lay in state at Westminster Hall.
On 6 May 2023, James, who then held the courtesy title Earl of Wessex, attended his uncle Charles III's coronation at Westminster Abbey, together with the rest of the royal family.
The following day, he attended the Coronation Concert at Windsor Castle.
On 31 March 2024, James attended the Easter Matins Service at St. George's Chapel, Windsor Castle, with his mother and father.
Titles, styles, and honours

Titles and styles

The title Viscount Severn alludes to the Welsh ancestry of his mother's family.
James was accorded this courtesy title at birth as heir apparent to his father's earldom.
At birth, James automatically became a prince of the United Kingdom (Prince James of Wessex, now Prince James of Edinburgh) under the terms of the 1917 letters patent, which assigned princely status and the style of Royal Highness to all male-line grandchildren of a sovereign.
However, when his parents married, Buckingham Palace announced that their children would be styled as the children of an earl rather than as prince or princess.
In 2020, James's mother reaffirmed that James and his sister retained the right to their royal titles and styles, and could choose whether to use them from the age of 18.
When his father was created Duke of Edinburgh in March 2023, James became styled by courtesy as Earl of Wessex, the family's senior subsidiary title.
The Dukedom of Edinburgh, having been created as a life peerage, will become extinct upon his father's death, but James remains heir apparent to his father's hereditary peerages of Earl of Wessex, Earl of Forfar, and Viscount Severn.
Honours and decorations

In June 2008, to recognise Prince Edward's visit to the Canadian province of Manitoba, a lake in the north of the province was named Lake James.
James's sister was similarly honoured by Lake Louise in the same province.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (033599ef-6ae2-4be3-b9ae-5d8ac161900e)
 Call ID: 033599ef-6ae2-4be3-b9ae-5d8ac161900e
  Args:
    type: :Man
    source: :James_Mountbatten-Windsor
  AssignClass (a1774340-7b36-4f9d-9aca-581d70d7ad87)
 Call ID: a1774340-7b36-4f9d-9aca-581d70d7ad87
  Args:
    type: :Person
    source: :James_Mountbatten-Windsor
  AddLiteral (a40bc0ef-af0c-4a55-86b0-55d192aef4bd)
 Call ID: a40bc0ef-af0c-4a55-86b0-55d192aef4bd
  Args:
    source: :James_Mountbatten-Windsor
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2007
  AssignClass (d9071b94-1f32-432d-af8c-b0da083a1a52)
 Call ID: d9071b94-1f32-432d-af8c-b0da083a1a52
  Args:
    type: :Man
    source: :Prince_Edward
  AssignClass (769854b2-e187-4b90-8a54-3b7bc51fb45f)
 Call ID: 769854b2-e187-4b90-8a54-3b7bc51fb45f
  Args:
    type: :Person
    source: :Prince_Edward
  AssignClass (7ac34d59-125c-4839-a118-ef3f82e667cd)
 Call ID: 7ac34d59-125c-4839-a118-ef3f82e667cd
  Args:
    type: :Woman
    source: :Sophie_Mountbatten-Windsor
  AssignClass (9abe2f9b-dd9d-45fe-811b-205dd3e6f6c4)
 Call ID: 9abe2f9b-dd9d-45fe-811b-205dd3e6f6c4
  Args:
    type: :Person
    source: :Sophie_Mountbatten-Windsor
  AddTriple (e6c42f67-fd07-49de-b718-b7fa48a73399)
 Call ID: e6c42f67-fd07-49de-b718-b7fa48a73399
  Args:
    source: :James_Mountbatten-Windsor
    target: :Prince_Edward
    relation: :hasFather
  AddTriple (73e997b3-5655-49ee-a580-88714751da3c)
 Call ID: 73e997b3-5655-49ee-a580-88714751da3c
  Args:
    relation: :hasMother
    source: :James_Mountbatten-Windsor
    target: :Sophie_Mountbatten-Windsor
  AssignClass (9073b263-a957-4ec2-8df3-1d931860e21d)
 Call ID: 9073b263-a957-4ec2-8df3-1d931860e21d
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (6610304b-cc49-43a6-8a3e-df987db91f7d)
 Call ID: 6610304b-cc49-43a6-8a3e-df987db91f7d
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AssignClass (d4c7f881-36eb-4c38-b402-bf3361cef9c4)
 Call ID: d4c7f881-36eb-4c38-b402-bf3361cef9c4
  Args:
    type: :Man
    source: :Prince_Philip
  AssignClass (96cc04b8-0ade-475e-8378-f758932d78a0)
 Call ID: 96cc04b8-0ade-475e-8378-f758932d78a0
  Args:
    type: :Person
    source: :Prince_Philip
  AddTriple (55fd7b64-1db2-4ece-bcc7-bdb4800a135c)
 Call ID: 55fd7b64-1db2-4ece-bcc7-bdb4800a135c
  Args:
    source: :Prince_Edward
    target: :Queen_Elizabeth_II
    relation: :hasMother
  AddTriple (716a08c5-8a0a-4b9d-a7c9-fef90673e507)
 Call ID: 716a08c5-8a0a-4b9d-a7c9-fef90673e507
  Args:
    source: :Prince_Edward
    target: :Prince_Philip
    relation: :hasFather
  AssignClass (049b649e-35b0-497f-b4bc-c62473a3ea5a)
 Call ID: 049b649e-35b0-497f-b4bc-c62473a3ea5a
  Args:
    type: :Man
    source: :King_Charles_III
  AssignClass (044287b1-c3b4-4daa-b994-2f077a924aa4)
 Call ID: 044287b1-c3b4-4daa-b994-2f077a924aa4
  Args:
    type: :Person
    source: :King_Charles_III
  AddTriple (37c04429-7cad-4c6b-8677-10239c93979a)
 Call ID: 37c04429-7cad-4c6b-8677-10239c93979a
  Args:
    source: :King_Charles_III
    target: :Prince_Edward
    relation: :isBrotherOf
  AssignClass (9cad0088-2170-4934-89eb-d43d118f2a5e)
 Call ID: 9cad0088-2170-4934-89eb-d43d118f2a5e
  Args:
    type: :Woman
    source: :Louise_Mountbatten-Windsor
  AssignClass (bf20cace-9958-4128-9ff5-2930949c09d5)
 Call ID: bf20cace-9958-4128-9ff5-2930949c09d5
  Args:
    type: :Person
    source: :Louise_Mountbatten-Windsor
  AddTriple (0dd2f03e-61c6-4c1a-84d3-da3a2063e973)
 Call ID: 0dd2f03e-61c6-4c1a-84d3-da3a2063e973
  Args:
    target: :James_Mountbatten-Windsor
    source: :Louise_Mountbatten-Windsor
    relation: :isSisterOf
  AddTriple (7c85d8d7-5ed0-47b4-8550-e7efa31dca8f)
 Call ID: 7c85d8d7-5ed0-47b4-8550-e7efa31dca8f
  Args:
    source: :Louise_Mountbatten-Windsor
    target: :Sophie_Mountbatten-Windsor
    relation: :hasMother
  AddTriple (4606aa00-bb5c-4e17-b2db-b6412a4dbb01)
 Call ID: 4606aa00-bb5c-4e17-b2db-b6412a4dbb01
  Args:
    target: :Prince_Edward
    source: :Louise_Mountbatten-Windsor
    relation: :hasFather
  Finish (58b4b6eb-9cba-43a1-8429-d4774951a40a)
 Call ID: 58b4b6eb-9cba-43a1-8429-d4774951a40a
  Args: