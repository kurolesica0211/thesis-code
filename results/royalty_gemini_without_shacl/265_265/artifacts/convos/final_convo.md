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
Dom Luís Filipe, Prince Royal of Portugal, Duke of Braganza (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Portuguese pronunciation: ; 21 March 1887 – 1 February 1908) was the eldest son and heir apparent of King Carlos I of Portugal until his assassination.
Born in 1887, when his father was still Prince Royal, he was styled Prince of Beira at birth.
After his paternal grandfather King Luís I of Portugal died, he became Prince Royal of Portugal and Duke of Braganza as heir apparent to the throne.
Following the Lisbon Regicide that saw him and his father killed, his younger brother Manuel II became King of Portugal.
Early life

Luís Filipe Maria Carlos Amélio Fernando Víctor Manuel António Lourenço Miguel Rafael Gabriel Gonzaga Xavier Francisco de Assis Bento was born in Lisbon, the elder son of Carlos, Prince Royal of Portugal (later King Carlos I of Portugal), and Princess Amélie d'Orléans, a member of the House of Braganza.
Two years after his birth, Dom Luís Filipe inherited all his father's royal princely titles when his father became king.
He was himself re-styled Prince Royal, and at the same time inherited the Dukedom of Braganza (as 21st Duke), which brought with it the largest private fortune in Portugal at that time, completely at the disposal of the heir to the Portuguese crown.
In 1907, the Prince Royal acted as regent of the kingdom while his father was outside the country.
The same year he made a very successful official visit to the Portuguese colonies in Africa, the first member of the royal family ever to visit them.
Dom Luís Filipe was the pupil of the African war hero Mouzinho de Albuquerque, and like all the Braganzas, showed many aptitudes in the arts, besides his pursuing a military education.
Around the time of Dom Luís Filipe's assassination, negotiations for marriage to his cousin Princess Patricia of Connaught were underway.
Princess Patricia was the granddaughter of Queen Victoria of the United Kingdom and Prince Albert of Saxe-Coburg and Gotha, the daughter of British Prince Arthur, Duke of Connaught and Strathearn, and Princess Louise Margaret of Prussia.
Lisbon Regicide

On 1 February 1908, Luís Filipe and his family were returning to Lisbon from Vila Viçosa Palace.
Alfredo Luís da Costa and Manuel Buiça, two members of a revolutionary society called the Carbonária, shot at all the royal family, hitting his father King Carlos, Luís Filipe, and his younger brother Infante Manuel, Duke of Beja.
Carlos I died immediately, while Luís Filipe lived for another twenty minutes.
Manuel survived the attack, having only been shot in the arm, while the queen was unharmed.
Manuel succeeded to the throne as Manuel II.
Luís Filipe is buried next to his father and forefathers in the Royal Pantheon of the House of Braganza in Lisbon.
His younger brother, King Manuel II of Portugal, and his mother, Queen Maria Amélia, are buried opposite.
On 5 October 1910, the monarchy under the reign of his surviving younger brother, Manuel II, was overthrown in a military coup and the First Portuguese Republic was established.
Honours

Domestic

Foreign

Arms

Luis Filipe bore as heir to the throne the arms of his father; differenced by a Label of three points Or.



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
  AssignClass (be940760-495c-414a-97cd-bba549139e4e)
 Call ID: be940760-495c-414a-97cd-bba549139e4e
  Args:
    type: :Man
    source: Dom_Luís_Filipe
  AssignClass (8e4528a0-88f0-43e3-89a2-adcbb1ff189d)
 Call ID: 8e4528a0-88f0-43e3-89a2-adcbb1ff189d
  Args:
    type: :Man
    source: Carlos_I
  AssignClass (0bc51490-d8e0-4a60-aee9-23b5082d01b9)
 Call ID: 0bc51490-d8e0-4a60-aee9-23b5082d01b9
  Args:
    type: :Woman
    source: Amélie_dOrléans
  AssignClass (e7c7637d-eee1-443c-af29-e2c391824bda)
 Call ID: e7c7637d-eee1-443c-af29-e2c391824bda
  Args:
    type: :Man
    source: Manuel_II
  AddLiteral (5b6f9d47-d45e-4f88-8efe-3dba11de2edf)
 Call ID: 5b6f9d47-d45e-4f88-8efe-3dba11de2edf
  Args:
    literal_type: xsd:integer
    source: Dom_Luís_Filipe
    literal_value: 1887
    relation: :hasBirthYear
  AddLiteral (0d2b2228-dfa5-49f1-a06b-d865905d6bc8)
 Call ID: 0d2b2228-dfa5-49f1-a06b-d865905d6bc8
  Args:
    relation: :hasDeathYear
    literal_value: 1908
    source: Dom_Luís_Filipe
    literal_type: xsd:integer
  AddTriple (18206f20-3227-4bc8-9876-4ec2cb232d65)
 Call ID: 18206f20-3227-4bc8-9876-4ec2cb232d65
  Args:
    source: Dom_Luís_Filipe
    relation: :hasFather
    target: Carlos_I
  AddTriple (dcc41200-46fc-442b-a161-f2fb0ac7109d)
 Call ID: dcc41200-46fc-442b-a161-f2fb0ac7109d
  Args:
    source: Dom_Luís_Filipe
    relation: :hasMother
    target: Amélie_dOrléans
  AddTriple (8df68822-98db-4891-a875-3e0a9673ee57)
 Call ID: 8df68822-98db-4891-a875-3e0a9673ee57
  Args:
    relation: :hasBrother
    target: Manuel_II
    source: Dom_Luís_Filipe
  AddTriple (fd0dff24-a89b-4c24-93cc-cf1aad9f10f7)
 Call ID: fd0dff24-a89b-4c24-93cc-cf1aad9f10f7
  Args:
    relation: :hasFather
    target: Carlos_I
    source: Manuel_II
  AddTriple (322bb139-00e3-4b34-8190-8e1940973e77)
 Call ID: 322bb139-00e3-4b34-8190-8e1940973e77
  Args:
    source: Manuel_II
    relation: :hasMother
    target: Amélie_dOrléans
  Finish (00134dce-49f1-479e-b279-ffb7c54e3879)
 Call ID: 00134dce-49f1-479e-b279-ffb7c54e3879
  Args: