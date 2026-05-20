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
  AssignClass (f4ab8b78-2d5d-4c02-9405-93ba09d18581)
 Call ID: f4ab8b78-2d5d-4c02-9405-93ba09d18581
  Args:
    type: :Man
    source: Pedro_Luiz_of_Orléans-Braganza
  AssignClass (548e2b80-f2f6-4a4c-a9a4-a135a6769932)
 Call ID: 548e2b80-f2f6-4a4c-a9a4-a135a6769932
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    type: :Person
  AddLiteral (1a8e3639-c714-414d-9cba-c3104e69fc2e)
 Call ID: 1a8e3639-c714-414d-9cba-c3104e69fc2e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1983
    source: Pedro_Luiz_of_Orléans-Braganza
  AddLiteral (c8c975d9-c19b-43e2-9d09-95ed1b9ef148)
 Call ID: c8c975d9-c19b-43e2-9d09-95ed1b9ef148
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    literal_value: 2009
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (bfc96b7c-f4ee-4d8b-bbfe-6ee864d97286)
 Call ID: bfc96b7c-f4ee-4d8b-bbfe-6ee864d97286
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    type: :Man
  AssignClass (e9d8a5e8-b5ed-41a7-ae46-4a15d19f6aa1)
 Call ID: e9d8a5e8-b5ed-41a7-ae46-4a15d19f6aa1
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    type: :Ancestor
  AssignClass (0bb40917-fbb9-4750-b0cc-3c15252c64e2)
 Call ID: 0bb40917-fbb9-4750-b0cc-3c15252c64e2
  Args:
    source: Maria_Elisabeth_of_Bavaria
    type: :Woman
  AssignClass (af143247-ec9b-4344-b1a0-8e80480e5889)
 Call ID: af143247-ec9b-4344-b1a0-8e80480e5889
  Args:
    source: Maria_Elisabeth_of_Bavaria
    type: :Ancestor
  AssignClass (d36a5d10-1ef4-4f85-9aee-d973906dceaa)
 Call ID: d36a5d10-1ef4-4f85-9aee-d973906dceaa
  Args:
    source: António_of_Orléans-Braganza
    type: :Man
  AssignClass (e949cfce-2f1f-4de0-b061-6d1a3bd024d2)
 Call ID: e949cfce-2f1f-4de0-b061-6d1a3bd024d2
  Args:
    source: António_of_Orléans-Braganza
    type: :Ancestor
  AssignClass (316b7eb1-8ce9-4fab-9aa9-3e69a2f7d004)
 Call ID: 316b7eb1-8ce9-4fab-9aa9-3e69a2f7d004
  Args:
    source: Christine_of_Ligne
    type: :Woman
  AssignClass (d5f596a2-3384-4f08-a1d6-59982acffb56)
 Call ID: d5f596a2-3384-4f08-a1d6-59982acffb56
  Args:
    type: :Ancestor
    source: Christine_of_Ligne
  AddTriple (6af6168c-5d68-43a0-a518-48642ad26fa9)
 Call ID: 6af6168c-5d68-43a0-a518-48642ad26fa9
  Args:
    target: António_of_Orléans-Braganza
    source: Pedro_Luiz_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (2069dbc9-adc0-41d1-a15a-e87b36587e69)
 Call ID: 2069dbc9-adc0-41d1-a15a-e87b36587e69
  Args:
    target: Christine_of_Ligne
    source: Pedro_Luiz_of_Orléans-Braganza
    relation: :hasMother
  AddTriple (fbb30a8a-478f-4068-a0ee-60af5f69c6bb)
 Call ID: fbb30a8a-478f-4068-a0ee-60af5f69c6bb
  Args:
    relation: :hasFather
    target: Pedro_Henrique_of_Orléans-Braganza
    source: António_of_Orléans-Braganza
  AddTriple (ff72e102-974a-4dbb-9eef-0d4a8f8f16b6)
 Call ID: ff72e102-974a-4dbb-9eef-0d4a8f8f16b6
  Args:
    relation: :hasMother
    target: Maria_Elisabeth_of_Bavaria
    source: António_of_Orléans-Braganza
  AssignClass (976db780-64bc-4fbd-8779-b1c15c24dd5c)
 Call ID: 976db780-64bc-4fbd-8779-b1c15c24dd5c
  Args:
    source: Bertrand_of_Orléans-Braganza
    type: :Man
  AssignClass (8e5eb1ef-15e7-4869-8793-f5f361822f5d)
 Call ID: 8e5eb1ef-15e7-4869-8793-f5f361822f5d
  Args:
    source: Bertrand_of_Orléans-Braganza
    type: :Person
  AddTriple (9baaa50e-8b00-4b2c-9cc6-7b842e0d3106)
 Call ID: 9baaa50e-8b00-4b2c-9cc6-7b842e0d3106
  Args:
    relation: :isBrotherOf
    target: António_of_Orléans-Braganza
    source: Bertrand_of_Orléans-Braganza
  AssignClass (4bed116c-db51-4938-a0a8-330122e88619)
 Call ID: 4bed116c-db51-4938-a0a8-330122e88619
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Man
  AssignClass (8d3ea39d-6223-4243-8aaf-e585e0c8457e)
 Call ID: 8d3ea39d-6223-4243-8aaf-e585e0c8457e
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Person
  AddTriple (89ca7e10-ab21-462c-bbf4-18911d7d2c90)
 Call ID: 89ca7e10-ab21-462c-bbf4-18911d7d2c90
  Args:
    target: António_of_Orléans-Braganza
    source: Luiz_of_Orléans-Braganza
    relation: :isBrotherOf
  AssignClass (f15ae73b-6bc6-43b6-963f-475468a0089f)
 Call ID: f15ae73b-6bc6-43b6-963f-475468a0089f
  Args:
    source: Antoine_Prince_of_Ligne
    type: :Man
  AssignClass (9400bd1a-86e8-4c86-8051-524884ce2c45)
 Call ID: 9400bd1a-86e8-4c86-8051-524884ce2c45
  Args:
    source: Antoine_Prince_of_Ligne
    type: :Ancestor
  AssignClass (c147cdfa-a9fc-41d8-a042-f2efe4c9c9d8)
 Call ID: c147cdfa-a9fc-41d8-a042-f2efe4c9c9d8
  Args:
    type: :Woman
    source: Alix_of_Luxembourg
  AssignClass (1d71b310-c1f5-48ad-b733-4113fda3cb05)
 Call ID: 1d71b310-c1f5-48ad-b733-4113fda3cb05
  Args:
    type: :Ancestor
    source: Alix_of_Luxembourg
  AddTriple (d44c968c-06f5-463e-a1cd-c4881ecaad09)
 Call ID: d44c968c-06f5-463e-a1cd-c4881ecaad09
  Args:
    relation: :hasFather
    source: Christine_of_Ligne
    target: Antoine_Prince_of_Ligne
  AddTriple (e0e64e20-7549-4b19-89b7-e6007764b13a)
 Call ID: e0e64e20-7549-4b19-89b7-e6007764b13a
  Args:
    relation: :hasMother
    source: Christine_of_Ligne
    target: Alix_of_Luxembourg
  AssignClass (06f6a298-0d5d-4915-acbf-3b747634cd81)
 Call ID: 06f6a298-0d5d-4915-acbf-3b747634cd81
  Args:
    type: :Woman
    source: Isabel_of_Brazil
  AssignClass (4ea52e37-a6fb-45cb-85d1-baaba938d3e4)
 Call ID: 4ea52e37-a6fb-45cb-85d1-baaba938d3e4
  Args:
    source: Isabel_of_Brazil
    type: :Ancestor
  AssignClass (d843ce0a-05e0-48f5-b626-7123a25334bc)
 Call ID: d843ce0a-05e0-48f5-b626-7123a25334bc
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Man
  AssignClass (a20a976a-3996-4d68-90d1-28919a2fc18c)
 Call ID: a20a976a-3996-4d68-90d1-28919a2fc18c
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Ancestor
  AssignClass (addcad53-6d14-42ff-b526-e5c9ed10c87b)
 Call ID: addcad53-6d14-42ff-b526-e5c9ed10c87b
  Args:
    source: Pedro_II_of_Brazil
    type: :Man
  AssignClass (864a90e4-4363-486c-8f78-42c02d28a79d)
 Call ID: 864a90e4-4363-486c-8f78-42c02d28a79d
  Args:
    type: :Ancestor
    source: Pedro_II_of_Brazil
  AssignClass (43a2c64c-4cb0-4e35-99a3-59cfb4aedbd9)
 Call ID: 43a2c64c-4cb0-4e35-99a3-59cfb4aedbd9
  Args:
    type: :Woman
    source: Teresa_Cristina_of_Brazil
  AssignClass (cf173ebe-38f5-4ad5-aee7-c2e0e259917e)
 Call ID: cf173ebe-38f5-4ad5-aee7-c2e0e259917e
  Args:
    type: :Ancestor
    source: Teresa_Cristina_of_Brazil
  AddTriple (ea17dda4-d719-4d82-8978-1d86cb3794fc)
 Call ID: ea17dda4-d719-4d82-8978-1d86cb3794fc
  Args:
    relation: :hasAncestor
    source: Pedro_Luiz_of_Orléans-Braganza
    target: Isabel_of_Brazil
  AddTriple (d7932874-3e91-4d9f-9d21-a0244415f387)
 Call ID: d7932874-3e91-4d9f-9d21-a0244415f387
  Args:
    target: Gaston_of_Orléans_Count_of_Eu
    source: Pedro_Luiz_of_Orléans-Braganza
    relation: :hasAncestor
  AddTriple (2d7e0b03-0dc1-40d7-9fb4-041e64238cce)
 Call ID: 2d7e0b03-0dc1-40d7-9fb4-041e64238cce
  Args:
    relation: :hasAncestor
    target: Pedro_II_of_Brazil
    source: Pedro_Luiz_of_Orléans-Braganza
  AddTriple (bc9b022b-9da4-4b35-99ea-c14ee68b9fbd)
 Call ID: bc9b022b-9da4-4b35-99ea-c14ee68b9fbd
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    target: Teresa_Cristina_of_Brazil
    relation: :hasAncestor
  Finish (c23c92d8-5be8-4b96-9d41-a9d698482fd7)
 Call ID: c23c92d8-5be8-4b96-9d41-a9d698482fd7
  Args: