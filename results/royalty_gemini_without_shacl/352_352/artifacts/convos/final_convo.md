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
William, Prince of Orange (Willem Nicolaas Alexander Frederik Karel Hendrik; 4 September 1840 – 11 June 1879), was heir apparent to the Dutch throne as the eldest son of King William III from 17 March 1849 until his death.
Early life

Prince William was the eldest son of King William III of the Netherlands and his first wife, Princess Sophie of Württemberg.
He was also seventeenth in the line of succession to the British throne, his claim being through his mother Sophie's great-grandmother Princess Augusta of Great Britain.
On 7 October 1840, only a month after his birth, his great-grandfather, the reigning King William I of the Netherlands, abdicated the throne due to disappointment over the recent Treaty of London, which recognized the independence of Belgium (previously provinces of the United Kingdom of the Netherlands), and the intention of marrying a Roman Catholic and Belgian noblewoman, Henrietta d'Oultremont.
In 1849, after the death of his grandfather King William II of the Netherlands, he became Prince of Orange as heir apparent.
Failed marriage attempts

After attempts to marry Prince William off to Princess Alice of the United Kingdom, the second daughter of Queen Victoria or Grand Duchess Maria Alexandrovna of Russia failed, the prince fell in love with the 19-year-old Countess Mathilde van Limburg-Stirum in 1873.
The relationship between the prince and his parents became very problematic, as his parents (who rarely agreed on anything) refused William's wish to accept Mathilde as his bride in 1874.
Also a rumour circulated that Mathilde was an illegitimate daughter of King William III and so William would potentially be marrying his own half-sister.
The 33-year-old William wanted to marry, if necessary, without the consent of his parents (this would have cost him his position in the line of succession).
Since they denied permission, the prince's attempt to marry Mathilde failed.
Death and aftermath

Heavily disillusioned with his situation in the Netherlands, Prince William then went into exile in Paris, where he threw himself into a life of sex, drinking and gambling.
The Duke de Gramont-Caderousse, a French fellow hedonist, gave him the nickname "Prince Lemon" ; the nickname became popular among the regulars in the recently created boulevards and the Parisian newspapers when they reported about his debauched lifestyle.
Prince William died at the age of 38 in his apartment in the Rue Auber, near the Paris Opera from a combination of typhus, liver complaints and total exhaustion.
After his death, his brother Alexander became heir-apparent and Prince of Orange.
His half-sister, the future queen Wilhelmina, was born a year after his death.
Honours

Ancestry

Footnotes

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (5cbb5715-549f-47c7-b43f-03773a96aa9a)
 Call ID: 5cbb5715-549f-47c7-b43f-03773a96aa9a
  Args:
    type: :Man
    source: William_Prince_of_Orange
  AssignClass (1eeb8cdc-51f7-46c3-bf24-999f48509da7)
 Call ID: 1eeb8cdc-51f7-46c3-bf24-999f48509da7
  Args:
    type: :Person
    source: William_Prince_of_Orange
  AssignClass (cee1f88e-5fa9-4f4a-a954-6f24cdf6eadc)
 Call ID: cee1f88e-5fa9-4f4a-a954-6f24cdf6eadc
  Args:
    source: Male_Sex
    type: :Male
  AssignClass (5eece8c0-69a3-4453-9adf-2bbf0e43cbce)
 Call ID: 5eece8c0-69a3-4453-9adf-2bbf0e43cbce
  Args:
    source: Male_Sex
    type: :Sex
  AddTriple (a6e825eb-d347-46b9-9cf0-912c40fe767d)
 Call ID: a6e825eb-d347-46b9-9cf0-912c40fe767d
  Args:
    relation: :hasSex
    target: Male_Sex
    source: William_Prince_of_Orange
  AddLiteral (df9ffc03-bdd1-4d64-8bae-5955f3aceb9b)
 Call ID: df9ffc03-bdd1-4d64-8bae-5955f3aceb9b
  Args:
    literal_type: xsd:integer
    source: William_Prince_of_Orange
    literal_value: 1840
    relation: :hasBirthYear
  AddLiteral (1ec375df-f448-48ba-8151-96beaa204ca2)
 Call ID: 1ec375df-f448-48ba-8151-96beaa204ca2
  Args:
    literal_value: 1879
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: William_Prince_of_Orange
  AddLiteral (acfc7946-0b5c-47b2-b9db-ac2d7546a0cd)
 Call ID: acfc7946-0b5c-47b2-b9db-ac2d7546a0cd
  Args:
    literal_value: Prince Lemon
    relation: :knownAs
    literal_type: xsd:string
    source: William_Prince_of_Orange
  AssignClass (e35ae38b-8af3-4ea1-a23c-bbbb0a81967e)
 Call ID: e35ae38b-8af3-4ea1-a23c-bbbb0a81967e
  Args:
    source: King_William_III
    type: :Man
  AssignClass (16e9c6e1-cd5b-44c3-9264-420fe10f10d5)
 Call ID: 16e9c6e1-cd5b-44c3-9264-420fe10f10d5
  Args:
    type: :Person
    source: King_William_III
  AssignClass (9a9e3bee-2472-424c-90a5-df46e604ecd1)
 Call ID: 9a9e3bee-2472-424c-90a5-df46e604ecd1
  Args:
    type: :Woman
    source: Princess_Sophie_of_Wurttemberg
  AssignClass (28fad66e-8e9d-4192-acdd-94e19419e762)
 Call ID: 28fad66e-8e9d-4192-acdd-94e19419e762
  Args:
    type: :Person
    source: Princess_Sophie_of_Wurttemberg
  AddTriple (a7423a30-4895-46b1-9b9b-c4db55ba9d35)
 Call ID: a7423a30-4895-46b1-9b9b-c4db55ba9d35
  Args:
    source: William_Prince_of_Orange
    target: King_William_III
    relation: :hasFather
  AddTriple (bd812cb0-85d5-4eaa-aa44-34481b12878c)
 Call ID: bd812cb0-85d5-4eaa-aa44-34481b12878c
  Args:
    source: William_Prince_of_Orange
    relation: :hasMother
    target: Princess_Sophie_of_Wurttemberg
  AssignClass (3ac6da62-07ac-48f0-b6a7-cacd778f92cc)
 Call ID: 3ac6da62-07ac-48f0-b6a7-cacd778f92cc
  Args:
    type: :Man
    source: Alexander
  AssignClass (24137fa1-3799-464f-8a78-0dc3bee0f0cf)
 Call ID: 24137fa1-3799-464f-8a78-0dc3bee0f0cf
  Args:
    source: Alexander
    type: :Person
  AddTriple (0d0da0fe-6d40-451f-89ab-a385fdae1187)
 Call ID: 0d0da0fe-6d40-451f-89ab-a385fdae1187
  Args:
    source: William_Prince_of_Orange
    target: Alexander
    relation: :hasBrother
  AssignClass (5a46710b-ddf0-4a71-999f-ddb048768d38)
 Call ID: 5a46710b-ddf0-4a71-999f-ddb048768d38
  Args:
    source: Wilhelmina
    type: :Woman
  AssignClass (8a9212b1-35eb-44e6-85e7-3323ef89fba6)
 Call ID: 8a9212b1-35eb-44e6-85e7-3323ef89fba6
  Args:
    type: :Person
    source: Wilhelmina
  AddTriple (eded4ee8-6ae0-409c-ac55-b4c70a2caccc)
 Call ID: eded4ee8-6ae0-409c-ac55-b4c70a2caccc
  Args:
    source: William_Prince_of_Orange
    target: Wilhelmina
    relation: :hasSister
  Finish (67c725c2-2e90-4036-b384-6fda5059dccc)
 Call ID: 67c725c2-2e90-4036-b384-6fda5059dccc
  Args: