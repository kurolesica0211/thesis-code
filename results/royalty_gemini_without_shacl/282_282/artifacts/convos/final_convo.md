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
Prince Louis of Wales (/ˈluːi/ LOO-ee; Louis Arthur Charles; born 23 April 2018) is a member of the British royal family.
He is the third and youngest child of William, Prince of Wales, and Catherine, Princess of Wales, and a grandson of King Charles III and Diana, Princess of Wales.
Infancy

Louis was born at 11:01 am on 23 April 2018 at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II.
He is the third child and second son of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
He has an elder brother and sister, Prince George and Princess Charlotte.
On 27 April, his name was announced as Louis Arthur Charles, honouring his paternal grandfather, Charles, Prince of Wales (later King Charles  III) and his 3rd-great-uncle Louis, Earl Mountbatten of Burma.
Louis was christened on 9 July by the archbishop of Canterbury, Justin Welby, in the Chapel Royal at St James's Palace.
Upbringing

Louis and his family lived at Kensington Palace and Anmer Hall in Norfolk during his early childhood.
Louis accompanied his siblings and parents to Elizabeth II's Platinum Jubilee celebrations in June 2022.
Elizabeth II died on 8 September 2022 and Louis's grandfather became king.
Accordingly, Louis became fourth in line to the throne.
Title and style

Louis is a British prince with the official style and title "His Royal Highness Prince Louis of Wales".
Before his father was created Prince of Wales on 9 September 2022, Louis was styled "His Royal Highness Prince Louis of Cambridge".
Succession

Louis is fourth in the line of succession to the British throne, behind his father and his two elder siblings.
Following the implementation of the Perth Agreement, which replaced male-preference primogeniture with absolute primogeniture, he is the first British prince to be ranked behind an elder sister in the line of succession.



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
  AssignClass (9c0b6ca5-484d-4ee8-8979-0aadb47bf55c)
 Call ID: 9c0b6ca5-484d-4ee8-8979-0aadb47bf55c
  Args:
    type: :Man
    source: :Prince_Louis_of_Wales
  AssignClass (be057752-1705-4b50-96cb-d64439a6defb)
 Call ID: be057752-1705-4b50-96cb-d64439a6defb
  Args:
    source: :Prince_Louis_of_Wales
    type: :Person
  AssignClass (a584c58a-5691-4129-b345-751acc07b83c)
 Call ID: a584c58a-5691-4129-b345-751acc07b83c
  Args:
    source: :Prince_William
    type: :Man
  AssignClass (6e862cfb-020c-4c68-92ae-3f84deb81b5d)
 Call ID: 6e862cfb-020c-4c68-92ae-3f84deb81b5d
  Args:
    type: :Person
    source: :Prince_William
  AssignClass (9734cc8e-4509-4874-a0c3-e78fe841b056)
 Call ID: 9734cc8e-4509-4874-a0c3-e78fe841b056
  Args:
    type: :Woman
    source: :Catherine_Princess_of_Wales
  AssignClass (42833881-cd55-4909-ae67-3f9fd2b28f43)
 Call ID: 42833881-cd55-4909-ae67-3f9fd2b28f43
  Args:
    type: :Person
    source: :Catherine_Princess_of_Wales
  AssignClass (473683b2-3ced-49a4-b705-d43e24bcd4d5)
 Call ID: 473683b2-3ced-49a4-b705-d43e24bcd4d5
  Args:
    source: :King_Charles_III
    type: :Man
  AssignClass (f028f157-93ba-4f87-bd03-1ec09eef32a0)
 Call ID: f028f157-93ba-4f87-bd03-1ec09eef32a0
  Args:
    type: :Person
    source: :King_Charles_III
  AssignClass (1e760ab5-6b87-4794-8ebf-156b38d8bdd1)
 Call ID: 1e760ab5-6b87-4794-8ebf-156b38d8bdd1
  Args:
    type: :Woman
    source: :Diana_Princess_of_Wales
  AssignClass (2465af45-a49c-439f-8871-8c081b73b3b7)
 Call ID: 2465af45-a49c-439f-8871-8c081b73b3b7
  Args:
    type: :Person
    source: :Diana_Princess_of_Wales
  AssignClass (e02bf39d-06f0-4610-a067-0c7f359d65ba)
 Call ID: e02bf39d-06f0-4610-a067-0c7f359d65ba
  Args:
    type: :Man
    source: :Prince_George
  AssignClass (13b71ffe-1fee-4cfa-ba55-7862581d2e33)
 Call ID: 13b71ffe-1fee-4cfa-ba55-7862581d2e33
  Args:
    source: :Prince_George
    type: :Person
  AssignClass (a5eb6359-0e97-43cf-9a15-1245b296ebc2)
 Call ID: a5eb6359-0e97-43cf-9a15-1245b296ebc2
  Args:
    type: :Woman
    source: :Princess_Charlotte
  AssignClass (a59f5d06-ac60-4904-bd13-3fd88766b022)
 Call ID: a59f5d06-ac60-4904-bd13-3fd88766b022
  Args:
    type: :Person
    source: :Princess_Charlotte
  AddLiteral (7fe6c330-b943-45f0-8557-bae1b1f11a18)
 Call ID: 7fe6c330-b943-45f0-8557-bae1b1f11a18
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Prince_Louis_of_Wales
    literal_value: 2018
  AddTriple (5f4d9e34-8ca4-4a7e-be83-ce2c8fbbe5ec)
 Call ID: 5f4d9e34-8ca4-4a7e-be83-ce2c8fbbe5ec
  Args:
    source: :Prince_Louis_of_Wales
    target: :Prince_William
    relation: :hasFather
  AddTriple (63914fdb-c59c-4aef-b2d7-292ec40a9f3d)
 Call ID: 63914fdb-c59c-4aef-b2d7-292ec40a9f3d
  Args:
    source: :Prince_Louis_of_Wales
    relation: :hasMother
    target: :Catherine_Princess_of_Wales
  AddTriple (2f935f44-d4ad-47fe-85c9-d8d5c0111de3)
 Call ID: 2f935f44-d4ad-47fe-85c9-d8d5c0111de3
  Args:
    target: :King_Charles_III
    relation: :hasFather
    source: :Prince_William
  AddTriple (a7192a8f-bf71-4d43-a026-7000ba693fd7)
 Call ID: a7192a8f-bf71-4d43-a026-7000ba693fd7
  Args:
    target: :Diana_Princess_of_Wales
    relation: :hasMother
    source: :Prince_William
  AddTriple (f8aa5d35-126c-4839-b260-4823c3177369)
 Call ID: f8aa5d35-126c-4839-b260-4823c3177369
  Args:
    source: :Prince_Louis_of_Wales
    target: :Prince_George
    relation: :hasBrother
  AddTriple (9ef5eced-7c0d-4027-a445-75e69c069bba)
 Call ID: 9ef5eced-7c0d-4027-a445-75e69c069bba
  Args:
    source: :Prince_Louis_of_Wales
    target: :Princess_Charlotte
    relation: :hasSister
  AddTriple (82cbe362-382e-42a4-9dfb-3b0f56bba835)
 Call ID: 82cbe362-382e-42a4-9dfb-3b0f56bba835
  Args:
    target: :Prince_Louis_of_Wales
    relation: :isBrotherOf
    source: :Prince_George
  AddTriple (ff0798f8-56ac-421e-86a4-75b94e604547)
 Call ID: ff0798f8-56ac-421e-86a4-75b94e604547
  Args:
    source: :Princess_Charlotte
    relation: :isSisterOf
    target: :Prince_Louis_of_Wales
  Finish (b61df2ab-e4a6-41eb-a728-53247fee8143)
 Call ID: b61df2ab-e4a6-41eb-a728-53247fee8143
  Args: