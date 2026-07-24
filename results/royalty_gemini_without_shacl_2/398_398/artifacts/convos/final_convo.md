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
  AssignClass (519fa326-f317-4921-801e-3325ae9dc5ee)
 Call ID: 519fa326-f317-4921-801e-3325ae9dc5ee
  Args:
    type: :Man
    source: Prince_William_of_Gloucester
  AssignClass (42b5a846-4d7f-4dd9-b674-1290d9e7027f)
 Call ID: 42b5a846-4d7f-4dd9-b674-1290d9e7027f
  Args:
    type: :Man
    source: Prince_Henry_Duke_of_Gloucester
  AssignClass (f4c3cf44-f99f-4741-9d2e-dc80c1f414b2)
 Call ID: f4c3cf44-f99f-4741-9d2e-dc80c1f414b2
  Args:
    type: :Woman
    source: Princess_Alice_Duchess_of_Gloucester
  AssignClass (ad64bff3-cd31-4675-a0b9-a32e8dc310cb)
 Call ID: ad64bff3-cd31-4675-a0b9-a32e8dc310cb
  Args:
    type: :Man
    source: George_V
  AssignClass (6f9c0d4f-f75f-41b2-8e75-4480d7371d87)
 Call ID: 6f9c0d4f-f75f-41b2-8e75-4480d7371d87
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (7e88233b-1b3c-495d-ad5c-ac2821f9f830)
 Call ID: 7e88233b-1b3c-495d-ad5c-ac2821f9f830
  Args:
    type: :Man
    source: Prince_Richard
  AddLiteral (5bff78f0-fc03-468d-af49-b36438f54493)
 Call ID: 5bff78f0-fc03-468d-af49-b36438f54493
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_William_of_Gloucester
    literal_value: 1941
  AddLiteral (8fbdf5f4-27bc-4ff6-8cbd-88fef4cf8194)
 Call ID: 8fbdf5f4-27bc-4ff6-8cbd-88fef4cf8194
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1972
    source: Prince_William_of_Gloucester
  AddTriple (6c390cbd-92d8-421e-b911-de0fd534bf0b)
 Call ID: 6c390cbd-92d8-421e-b911-de0fd534bf0b
  Args:
    source: Prince_William_of_Gloucester
    relation: :hasFather
    target: Prince_Henry_Duke_of_Gloucester
  AddTriple (568d4478-8234-419a-99b2-bf529b29babd)
 Call ID: 568d4478-8234-419a-99b2-bf529b29babd
  Args:
    target: Princess_Alice_Duchess_of_Gloucester
    relation: :hasMother
    source: Prince_William_of_Gloucester
  AddTriple (238f8f82-4a7e-491c-9b96-71e3f2ea9590)
 Call ID: 238f8f82-4a7e-491c-9b96-71e3f2ea9590
  Args:
    relation: :hasFather
    target: George_V
    source: Prince_Henry_Duke_of_Gloucester
  AddTriple (05741ac9-e23b-4e86-82a0-10e867834c9c)
 Call ID: 05741ac9-e23b-4e86-82a0-10e867834c9c
  Args:
    source: Prince_Henry_Duke_of_Gloucester
    target: Queen_Mary
    relation: :hasMother
  AddTriple (26c0a270-e41e-4adf-bd34-765d334832d7)
 Call ID: 26c0a270-e41e-4adf-bd34-765d334832d7
  Args:
    target: Prince_Richard
    relation: :hasBrother
    source: Prince_William_of_Gloucester
  AddTriple (8c2ff00e-3f40-4d3e-a6c5-4683985c6a70)
 Call ID: 8c2ff00e-3f40-4d3e-a6c5-4683985c6a70
  Args:
    source: Prince_Richard
    relation: :hasFather
    target: Prince_Henry_Duke_of_Gloucester
  AddTriple (add9ac58-5bab-4306-9a89-5db152c5dde4)
 Call ID: add9ac58-5bab-4306-9a89-5db152c5dde4
  Args:
    target: Princess_Alice_Duchess_of_Gloucester
    relation: :hasMother
    source: Prince_Richard
  Finish (643ace7e-587e-47a1-b181-fc5146d0e137)
 Call ID: 643ace7e-587e-47a1-b181-fc5146d0e137
  Args: