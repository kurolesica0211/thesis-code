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
Prince William of Gloucester (William Henry Andrew Frederick; 18 December 1941 – 28 August 1972) was a member of the British royal family.
The elder son of Prince Henry, Duke of Gloucester, and Princess Alice, Duchess of Gloucester, he was a grandson of George V, nephew of Edward VIII and George VI, and first cousin of Elizabeth II.
He was the most recent descendant of George III to be diagnosed with porphyria, a condition thought to have caused George III’s mental breakdown, and in William’s case, it was most likely hereditary.
William died in 1972, aged 30, in an air crash while piloting his plane during a competition.
Early life

William was born on 18 December 1941 at the Lady Carnarvon Nursing Home in Hadley Common, Hertfordshire, the eldest son of Prince Henry, Duke of Gloucester, and Alice, Duchess of Gloucester.
His father was the third son of King George V and Queen Mary, and his mother was the third daughter of the 7th Duke of Buccleuch and Lady Margaret Bridgeman.
His godparents were King George VI (his paternal uncle), Queen Mary (his paternal grandmother), Princess Helena Victoria (his paternal first cousin twice-removed), Lady Margaret Hawkins (his maternal aunt), Major Lord William Montagu Douglas Scott (his maternal uncle) and John Vereker, 6th Viscount Gort, who was unable to attend.
At the time of William's birth, and for months afterwards, Henry was away on military duties, some involving considerable risk.
This prompted George VI to write to his sister-in-law, assuring her that, should anything happen to his brother, he would become Prince William's guardian.
In 1947, William served as a page boy at the wedding of his cousin Princess Elizabeth to Philip, Duke of Edinburgh.
The other page boy was Prince Michael of Kent.
William spent his early childhood at Barnwell Manor in Northamptonshire and later in Canberra, Australia, where his father served as Governor-General from 1945 to 1947.
Career

After returning to Britain, William took a position with Lazards, a merchant bank.
He was the second member of the British royal family to work in the civil service or diplomatic service (the first was his uncle, Prince George, Duke of Kent, in the 1920s).
By 1970, the health of his father, the Duke of Gloucester, had deteriorated following further strokes.
William had no choice but to resign from the diplomatic service and return to Britain in order to manage his father's estate and, as he put it, take on the full-time role of a royal prince.
Apart from taking over many engagements his father could no longer perform, William took particular interest in St John Ambulance, where he became increasingly active.
William occasionally served as Counsellor of State during the Queen's absence.
Personal life

William was consistently described by friends as adventurous (almost to the point of recklessness), warm, tender and extremely generous.
Regarding his family, William considered himself extremely lucky compared to other members of the royal family.
William acknowledged his father couldn't have been very happy as a young man, as a result of the strict upbringing he had received, and expressed gratitude for the freedom he had given him throughout his life.
Relationships

Former Hungarian model and stewardess Zsuzsi Starkloff (1936–2020, born Zsuzsana Maria Lehel in a Jewish-Hungarian family) had a relationship with William.
They first met in 1968 in Japan, where Starkloff worked, having previously divorced American pilot Edward Starkloff.
The relationship was further explored in the 2015 Channel 4 TV documentary, The Other Prince William.
Despite the reported reluctance of senior members of the royal family to take William's relationship with Starkloff seriously, marriage standards within the royal family were no longer as strict as they had been.
Princess Margaret, while not encouraging William, did sympathise with him in this regard and advised him to "wait a bit" and to "see how everything looks" once he returned to Britain.
William's intentions regarding his relationship with Starkloff are unclear.
In the early 1970s, William began a relationship with divorcee Nicole Sieff (née Moschietto), daughter of a Monte Carlo restaurateur, who had two sons from her marriage to Jonathan Sieff, grandson of Israel Sieff, Baron Sieff.
Health

Shortly before transferring to Tokyo in August 1968, William was examined by a Royal Air Force doctor, Headly Bellringer, at the request of his mother.
Although aware of the theory of the royal family's history of porphyria then being advanced by Ida Macalpine and Richard Hunter, Bellringer stated he "tried not to let it influence him...with all the symptoms, I was left with little option but to diagnose the Prince's condition as porphyria."
A reliable diagnosis of porphyria in a member of the British royal family lent weight to the theory – first advanced by Professor Ida Macalpine in the late 1960s – that porphyria was the underlying cause of the ill-health of both Mary, Queen of Scots (an ancestor of both of William's parents) and George III.
Death

A licensed pilot and President of the British Light Aviation Centre, William owned several aircraft and competed in amateur air show races.
William and Mitchell were killed.
William was buried in the Royal Burial Ground, Frogmore.
The comprehensive school in Oundle, which he opened in 1971, was renamed Prince William School in his memory.
William was the heir apparent of his father's peerages, Duke of Gloucester, Earl of Ulster, and Baron Culloden.
Upon his death, his younger brother Prince Richard became heir apparent, and succeeded to these peerages in 1974.
William was the first grandchild of King George V and Queen Mary to die.
Honours and arms

Honours

Arms

For his 21st birthday, in 1962, Prince William was granted the use of the Royal Arms, differenced with a label argent of five points, the outer pair and central point bearing lions gules, the inner pair crosses gules.



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
  AssignClass (173df14e-b57b-4fd9-bd70-8a05905a46e0)
 Call ID: 173df14e-b57b-4fd9-bd70-8a05905a46e0
  Args:
    source: Prince_William_of_Gloucester
    type: :Man
  AssignClass (ce81e1e2-0f82-467f-a6c3-b7770a6528f8)
 Call ID: ce81e1e2-0f82-467f-a6c3-b7770a6528f8
  Args:
    type: :Person
    source: Prince_William_of_Gloucester
  AddLiteral (39cd255a-d829-47e5-96d8-ad134b3f8562)
 Call ID: 39cd255a-d829-47e5-96d8-ad134b3f8562
  Args:
    literal_value: 1941
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_William_of_Gloucester
  AddLiteral (528450a0-bd4b-4d34-a040-ccd2b671e0fc)
 Call ID: 528450a0-bd4b-4d34-a040-ccd2b671e0fc
  Args:
    literal_value: 1972
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_William_of_Gloucester
  AssignClass (ea2ca783-befb-4a16-9496-3ba5e46df943)
 Call ID: ea2ca783-befb-4a16-9496-3ba5e46df943
  Args:
    source: Prince_Henry_Duke_of_Gloucester
    type: :Man
  AssignClass (d4a5aa66-696e-4878-9ee0-39f5b75d7f14)
 Call ID: d4a5aa66-696e-4878-9ee0-39f5b75d7f14
  Args:
    source: Prince_Henry_Duke_of_Gloucester
    type: :Person
  AssignClass (552888e2-dc1b-4178-a0ad-ec17db0c1ea4)
 Call ID: 552888e2-dc1b-4178-a0ad-ec17db0c1ea4
  Args:
    source: Princess_Alice_Duchess_of_Gloucester
    type: :Woman
  AssignClass (44ffb9ce-6789-4278-9a81-a4aafb60f9a2)
 Call ID: 44ffb9ce-6789-4278-9a81-a4aafb60f9a2
  Args:
    type: :Person
    source: Princess_Alice_Duchess_of_Gloucester
  AddTriple (f310c10d-a83f-4050-86b0-cb41efbf943f)
 Call ID: f310c10d-a83f-4050-86b0-cb41efbf943f
  Args:
    source: Prince_William_of_Gloucester
    relation: :hasFather
    target: Prince_Henry_Duke_of_Gloucester
  AddTriple (531aae86-4dbf-4ba0-9a0a-f08f13c747a1)
 Call ID: 531aae86-4dbf-4ba0-9a0a-f08f13c747a1
  Args:
    source: Prince_William_of_Gloucester
    target: Princess_Alice_Duchess_of_Gloucester
    relation: :hasMother
  AssignClass (fcb0d81a-f56c-49ba-9045-aee07d456e88)
 Call ID: fcb0d81a-f56c-49ba-9045-aee07d456e88
  Args:
    type: :Man
    source: George_V
  AssignClass (a9023347-d365-40e2-9644-5d7c32033c60)
 Call ID: a9023347-d365-40e2-9644-5d7c32033c60
  Args:
    type: :Person
    source: George_V
  AssignClass (ba497ed9-e4b1-4d3c-b53d-ad3a1354c96c)
 Call ID: ba497ed9-e4b1-4d3c-b53d-ad3a1354c96c
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (05d8d845-0921-43c1-b2d2-feeacda86596)
 Call ID: 05d8d845-0921-43c1-b2d2-feeacda86596
  Args:
    source: Queen_Mary
    type: :Person
  AddTriple (ffab8ad9-d519-4eba-ac80-8cf17b4063b8)
 Call ID: ffab8ad9-d519-4eba-ac80-8cf17b4063b8
  Args:
    relation: :hasFather
    target: George_V
    source: Prince_Henry_Duke_of_Gloucester
  AddTriple (0b937872-73f5-4141-ba55-e5648e377556)
 Call ID: 0b937872-73f5-4141-ba55-e5648e377556
  Args:
    source: Prince_Henry_Duke_of_Gloucester
    relation: :hasMother
    target: Queen_Mary
  AssignClass (454037e5-76b3-4016-972a-a5c3df2fdfd7)
 Call ID: 454037e5-76b3-4016-972a-a5c3df2fdfd7
  Args:
    type: :Man
    source: Prince_Richard
  AssignClass (04cad1c4-9fd1-4aa7-b334-9f3a56acc075)
 Call ID: 04cad1c4-9fd1-4aa7-b334-9f3a56acc075
  Args:
    type: :Person
    source: Prince_Richard
  AddTriple (1c6c288e-9c76-4cef-82c0-041856edc265)
 Call ID: 1c6c288e-9c76-4cef-82c0-041856edc265
  Args:
    target: Prince_Richard
    relation: :isBrotherOf
    source: Prince_William_of_Gloucester
  Finish (a1974d17-8c1c-4e6a-b00e-f233c010b025)
 Call ID: a1974d17-8c1c-4e6a-b00e-f233c010b025
  Args: