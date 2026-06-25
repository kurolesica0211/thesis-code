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
  AssignClass (a427956a-a72e-4346-87ec-849401c3656d)
 Call ID: a427956a-a72e-4346-87ec-849401c3656d
  Args:
    type: :Man
    source: James_Mountbatten-Windsor
  AssignClass (25d2b147-13e9-44a6-ba3f-c80c912533fd)
 Call ID: 25d2b147-13e9-44a6-ba3f-c80c912533fd
  Args:
    source: Prince_Edward
    type: :Man
  AssignClass (0bf0f30a-863c-4ea2-9f53-388b68e09714)
 Call ID: 0bf0f30a-863c-4ea2-9f53-388b68e09714
  Args:
    type: :Woman
    source: Sophie_Mountbatten-Windsor
  AssignClass (a1ab7822-3820-4c08-9541-3c0c42d2482f)
 Call ID: a1ab7822-3820-4c08-9541-3c0c42d2482f
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (f4e1dcb3-0298-435d-ab34-82fe519e437c)
 Call ID: f4e1dcb3-0298-435d-ab34-82fe519e437c
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (b7856789-6e57-4f63-aa16-effeebf04b3b)
 Call ID: b7856789-6e57-4f63-aa16-effeebf04b3b
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (6c061b90-884a-47cd-b77c-0694c0fac80c)
 Call ID: 6c061b90-884a-47cd-b77c-0694c0fac80c
  Args:
    type: :Woman
    source: Louise_Mountbatten-Windsor
  AddLiteral (33831b25-8a9a-4ab6-9057-44c6b436db0f)
 Call ID: 33831b25-8a9a-4ab6-9057-44c6b436db0f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: James_Mountbatten-Windsor
    literal_value: 2007
  AddTriple (f7e1735d-a4a8-429c-8033-1bb7069db80f)
 Call ID: f7e1735d-a4a8-429c-8033-1bb7069db80f
  Args:
    source: James_Mountbatten-Windsor
    relation: :hasFather
    target: Prince_Edward
  AddTriple (ae6c6525-d8be-4f4e-b7b9-765ca3fa898b)
 Call ID: ae6c6525-d8be-4f4e-b7b9-765ca3fa898b
  Args:
    relation: :hasMother
    source: James_Mountbatten-Windsor
    target: Sophie_Mountbatten-Windsor
  AddTriple (b4b42fe8-1a43-42ff-a5e3-159aaec0edba)
 Call ID: b4b42fe8-1a43-42ff-a5e3-159aaec0edba
  Args:
    target: Prince_Philip
    relation: :hasFather
    source: Prince_Edward
  AddTriple (5504d157-52f4-41d5-af6d-574c9652c29c)
 Call ID: 5504d157-52f4-41d5-af6d-574c9652c29c
  Args:
    target: Queen_Elizabeth_II
    source: Prince_Edward
    relation: :hasMother
  AddTriple (3fa8ebdf-567c-4109-b461-c51dcdbff329)
 Call ID: 3fa8ebdf-567c-4109-b461-c51dcdbff329
  Args:
    source: James_Mountbatten-Windsor
    relation: :isSiblingOf
    target: Louise_Mountbatten-Windsor
  AddTriple (27ca5f8b-bd50-43df-932e-34adbc7edd72)
 Call ID: 27ca5f8b-bd50-43df-932e-34adbc7edd72
  Args:
    target: Prince_Edward
    source: Louise_Mountbatten-Windsor
    relation: :hasFather
  AddTriple (53229dd1-0242-46b7-ba03-d1c05de4842d)
 Call ID: 53229dd1-0242-46b7-ba03-d1c05de4842d
  Args:
    relation: :hasMother
    source: Louise_Mountbatten-Windsor
    target: Sophie_Mountbatten-Windsor
  AddTriple (ac06e4e9-684f-4345-bb41-0a32e0c40254)
 Call ID: ac06e4e9-684f-4345-bb41-0a32e0c40254
  Args:
    target: Prince_Edward
    relation: :isBrotherOf
    source: King_Charles_III
  Finish (3aa433f4-9bf5-4794-b109-03b89ff0c891)
 Call ID: 3aa433f4-9bf5-4794-b109-03b89ff0c891
  Args: