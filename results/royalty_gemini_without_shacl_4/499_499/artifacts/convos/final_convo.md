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
Pedro Luiz of Orléans-Braganza (Pedro Luiz Maria José Miguel Gabriel Rafael Gonzaga; 12 January 1983 – 1 June 2009) was a Brazilian prince of the House of Orléans-Braganza.
He was the eldest grandson of Prince Pedro Henrique of Orléans-Braganza and Princess Maria Elisabeth of Bavaria.
A great-great-grandson of Princess Isabel and her consort Gaston of Orléans, Count of Eu, as well as of Emperor Pedro II and Empress Teresa Cristina, Pedro Luiz occupied a prominent place in the line of succession claimed by Brazilian monarchists.
His childless uncle, Bertrand of Orléans-Braganza, is one of the two current claimants to the defunct Brazilian throne, with Pedro Luiz’s father regarded as Bertrand’s immediate successor.
Because of this position, some supporters of Brazilian monarchism expected Pedro Luiz to eventually become the imperial claimant.
Family

Prince Pedro Luiz was born on 12 January 1983 in Rio de Janeiro, the elder of the two sons of Prince António of Orléans-Braganza and his Belgian wife, Princess Christine of Ligne.
His name in full was Pedro Luiz Maria José Miguel Gabriel Rafael Gonzaga de Orleans e Bragança.
His paternal grandparents were Prince Pedro Henrique of Orléans-Braganza, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
By 2009, his father's two elder brothers, Prince Luiz and Prince Bertrand, were unmarried and had no offspring.
His father António was therefore heir to the claim after his older siblings, and Pedro would, in due course, have been a claimant to the traditional headship of the Imperial House of Brazil, and the nominal Brazilian crown.
Pedro descended from all monarchs of the Kingdom of Portugal, including Dom João VI of Portugal, Brazil and the Algarves, and the later monarchs of independent Brazil, emperors Dom Pedro
I and Dom Pedro II.
Career

Pedro Luiz held dual Brazilian-Belgian citizenship and was fluent in Portuguese, English and French.
Luiz and Bertrand, known for their political beliefs, were denounced not only by some monarchists, but also by four of their own younger brothers, who tried unsuccessfully to convince them to renounce their traditional claims to the throne in favour of their brother António, and the young Pedro Luiz.
Then only ten years old, Pedro Luiz was seen beside his father during the monarchist restoration campaign.
Luiz and Bertrand believed that Pedro Luiz would be a better choice if the monarchy were to be reinstated by the Brazilian people.
In 1999 he became honorary president of Brazil's Monarchist Youth, and also held the Grand Crosses of the Order of Pedro I and of the Order of the Rose.


Pedro Luiz had expressed some opinions about Brazilian politics aside from the monarchy.
Regarding the government of President Luiz Inácio Lula da Silva he stated, "I am very pleased with the economic performance of Brazil, all derived from the policy of Lula da Silva.
Pedro Luiz was considered by many Brazilian monarchists as the prince that gathered "all the hopes and aspirations " due to the "vigor of youth and the seriousness of his character".
Duarte Pio, Duke of Bragança and heir of the abolished Portuguese crown, affirmed: " is a very intelligent person.
"


Death

Luiz was killed in the crash of Air France Flight 447 on 1 June 2009.
His double-cousin Princess Alix of Ligne had planned to travel with him, but took an earlier flight instead.
Pedro Luiz's body was among those retrieved from the ocean and was buried in Vassouras in the family's mausoleum on 5 July 2009.
Genealogy

Ancestry

Patrilineal descent

Pedro Luiz was a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Pedro Luiz' patriline is the line from which he is descended father to son.



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
  AssignClass (c428c117-0d0a-4bb7-bd40-87a23a56c028)
 Call ID: c428c117-0d0a-4bb7-bd40-87a23a56c028
  Args:
    source: Pedro_Luiz_of_Orleans-Braganza
    type: :Man
  AssignClass (2e336585-666b-4fc0-a800-edb15216b7c3)
 Call ID: 2e336585-666b-4fc0-a800-edb15216b7c3
  Args:
    type: :Person
    source: Pedro_Luiz_of_Orleans-Braganza
  AddLiteral (f6471f4d-fe7c-4418-a836-0a465fcc279a)
 Call ID: f6471f4d-fe7c-4418-a836-0a465fcc279a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Pedro_Luiz_of_Orleans-Braganza
    literal_value: 1983
  AddLiteral (f4f2cb16-716d-4ee0-a452-8f8c31a35365)
 Call ID: f4f2cb16-716d-4ee0-a452-8f8c31a35365
  Args:
    literal_value: 2009
    literal_type: xsd:integer
    source: Pedro_Luiz_of_Orleans-Braganza
    relation: :hasDeathYear
  AddTriple (8763776b-3032-413f-a092-cfddf9540aad)
 Call ID: 8763776b-3032-413f-a092-cfddf9540aad
  Args:
    relation: :hasFather
    target: Antonio_of_Orleans-Braganza
    source: Pedro_Luiz_of_Orleans-Braganza
  AddTriple (b6b8be38-681d-476f-af97-527ebcd2d646)
 Call ID: b6b8be38-681d-476f-af97-527ebcd2d646
  Args:
    source: Pedro_Luiz_of_Orleans-Braganza
    relation: :hasMother
    target: Christine_of_Ligne
  AssignClass (558ef1dd-2bcb-48e5-aea8-a959b2b81213)
 Call ID: 558ef1dd-2bcb-48e5-aea8-a959b2b81213
  Args:
    type: :Man
    source: Antonio_of_Orleans-Braganza
  AssignClass (397893d2-60db-43d9-8b64-af2fba150894)
 Call ID: 397893d2-60db-43d9-8b64-af2fba150894
  Args:
    type: :Person
    source: Antonio_of_Orleans-Braganza
  AssignClass (b6ff8c95-ae9e-4300-a899-be188e5f2acb)
 Call ID: b6ff8c95-ae9e-4300-a899-be188e5f2acb
  Args:
    type: :Woman
    source: Christine_of_Ligne
  AssignClass (c0c661a0-2f57-4dc1-b80c-4defa9883269)
 Call ID: c0c661a0-2f57-4dc1-b80c-4defa9883269
  Args:
    type: :Person
    source: Christine_of_Ligne
  AddTriple (5e1fe777-b024-40a2-8af4-cfed509de2a8)
 Call ID: 5e1fe777-b024-40a2-8af4-cfed509de2a8
  Args:
    target: Pedro_Henrique_of_Orleans-Braganza
    relation: :hasFather
    source: Pedro_Luiz_of_Orleans-Braganza
  AddTriple (011db8bd-804d-471e-9f11-3bb6958a1128)
 Call ID: 011db8bd-804d-471e-9f11-3bb6958a1128
  Args:
    source: Pedro_Luiz_of_Orleans-Braganza
    target: Maria_Elisabeth_of_Bavaria
    relation: :hasMother
  AssignClass (7ed52988-7b81-4a40-81a9-c48e95aa6d2c)
 Call ID: 7ed52988-7b81-4a40-81a9-c48e95aa6d2c
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (d3aeae63-5816-4dc6-af7a-d03616fea9c3)
 Call ID: d3aeae63-5816-4dc6-af7a-d03616fea9c3
  Args:
    type: :Person
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (383d3d4b-27b4-498f-93e6-c96ac5d80aee)
 Call ID: 383d3d4b-27b4-498f-93e6-c96ac5d80aee
  Args:
    type: :Woman
    source: Maria_Elisabeth_of_Bavaria
  AssignClass (1288a56e-e5b9-478d-a1e6-1fae98edeec1)
 Call ID: 1288a56e-e5b9-478d-a1e6-1fae98edeec1
  Args:
    type: :Person
    source: Maria_Elisabeth_of_Bavaria
  AddTriple (7cbfff4f-14ba-4beb-b8d8-eca496910bd1)
 Call ID: 7cbfff4f-14ba-4beb-b8d8-eca496910bd1
  Args:
    source: Antonio_of_Orleans-Braganza
    target: Pedro_Henrique_of_Orleans-Braganza
    relation: :hasFather
  AddTriple (e0ab67e5-cda2-4469-a7a6-cc66440fda36)
 Call ID: e0ab67e5-cda2-4469-a7a6-cc66440fda36
  Args:
    source: Antonio_of_Orleans-Braganza
    target: Maria_Elisabeth_of_Bavaria
    relation: :hasMother
  AddTriple (0f62d3fc-f894-44cb-b2f9-2f210316a676)
 Call ID: 0f62d3fc-f894-44cb-b2f9-2f210316a676
  Args:
    relation: :hasFather
    target: Antoine_Prince_of_Ligne
    source: Christine_of_Ligne
  AddTriple (9928dff7-daed-49e4-a79a-c82ad8855971)
 Call ID: 9928dff7-daed-49e4-a79a-c82ad8855971
  Args:
    source: Christine_of_Ligne
    relation: :hasMother
    target: Alix_of_Luxembourg
  AssignClass (1998bd2b-522a-472f-8b55-ac84c4d53d17)
 Call ID: 1998bd2b-522a-472f-8b55-ac84c4d53d17
  Args:
    source: Antoine_Prince_of_Ligne
    type: :Man
  AssignClass (661f905b-ad2d-4d22-9dbc-b570ad8475d9)
 Call ID: 661f905b-ad2d-4d22-9dbc-b570ad8475d9
  Args:
    source: Antoine_Prince_of_Ligne
    type: :Person
  AssignClass (67b2aa97-085b-4b0d-87de-38668fd244dd)
 Call ID: 67b2aa97-085b-4b0d-87de-38668fd244dd
  Args:
    type: :Woman
    source: Alix_of_Luxembourg
  AssignClass (19633085-7dbc-4295-95ef-46c2ffe86c97)
 Call ID: 19633085-7dbc-4295-95ef-46c2ffe86c97
  Args:
    source: Alix_of_Luxembourg
    type: :Person
  AddTriple (fa9c8bcc-67d5-4f38-b0be-dfb10dfae882)
 Call ID: fa9c8bcc-67d5-4f38-b0be-dfb10dfae882
  Args:
    relation: :isBrotherOf
    target: Antonio_of_Orleans-Braganza
    source: Luiz_of_Orleans-Braganza
  AddTriple (fa29a0b4-c889-4828-b58f-31be75699843)
 Call ID: fa29a0b4-c889-4828-b58f-31be75699843
  Args:
    source: Bertrand_of_Orleans-Braganza
    relation: :isBrotherOf
    target: Antonio_of_Orleans-Braganza
  AssignClass (1bedb0f9-19f8-4cbd-b1ce-fafc94e5d7cf)
 Call ID: 1bedb0f9-19f8-4cbd-b1ce-fafc94e5d7cf
  Args:
    source: Luiz_of_Orleans-Braganza
    type: :Man
  AssignClass (d513f9a9-1fc3-4e50-9891-e87c272332b3)
 Call ID: d513f9a9-1fc3-4e50-9891-e87c272332b3
  Args:
    source: Luiz_of_Orleans-Braganza
    type: :Person
  AssignClass (c92b9a85-fe9c-4711-b9f0-f2cf2e9579a2)
 Call ID: c92b9a85-fe9c-4711-b9f0-f2cf2e9579a2
  Args:
    type: :Man
    source: Bertrand_of_Orleans-Braganza
  AssignClass (84bf05d7-82e7-4605-a2cc-70bddf928412)
 Call ID: 84bf05d7-82e7-4605-a2cc-70bddf928412
  Args:
    type: :Person
    source: Bertrand_of_Orleans-Braganza
  Finish (b96bd193-5bc3-48a8-991c-a1298e30de94)
 Call ID: b96bd193-5bc3-48a8-991c-a1298e30de94
  Args: