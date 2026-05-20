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
Princess Antonia of Prussia, Duchess of Wellington (Antonia Elizabeth Brigid Louise Mansfeld; born 28 April 1955) is a British aristocrat and philanthropist.
Through her marriage, she is also the Princess of Waterloo, Duchess of Victoria, and Duchess of Ciudad Rodrigo.
Early life and education

Princess Antonia Elizabeth Brigid Louise Mansfeld of Prussia was born in London on 28 April 1955, the daughter of Prince Frederick of Prussia and his wife, Lady Brigid Guinness.
On her father's side, she is a great-granddaughter of the German Emperor Wilhelm II, and granddaughter of Rupert Guinness, 2nd Earl of Iveagh on her mother's side.
Career

In 2007, she was appointed as the President of The Guinness Partnership, an affordable housing charitable society in the United Kingdom, and was appointed an Officer of the Order of the British Empire in the 2008 Birthday Honours for services to social housing.
In 2008 Antonia was appointed as a fellow of Eton College, serving as a member of the college's governing body.
Personal life

On 3 February 1977, she married Charles Wellesley, Marquess of Douro at St Paul's Church, Knightsbridge in London.
Notable guests at the wedding included Queen Elizabeth The Queen Mother, the Prince of Wales, Princess Margaret, and the Duke and Duchess of Kent.
She is godmother to Lady Gabriella Kingston, daughter of Prince & Princess Michael of Kent.
When her husband succeeded his father as the 9th Duke of Wellington, she became the Princess of Waterloo in Belgium and the Netherlands, the Duchess of Victoria in Portugal, the Duchess of Wellington in the United Kingdom, and the Duchess of Ciudad Rodrigo in Spain.
They have five children, including Lady Mary Wellesley and Lady Charlotte Wellesley.


References



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
  AssignClass (93b10916-3470-4a57-bb83-02cf6b8abf6a)
 Call ID: 93b10916-3470-4a57-bb83-02cf6b8abf6a
  Args:
    type: :Person
    source: Antonia_of_Prussia
  AssignClass (4de13324-3e87-4cad-bcf3-d6d5bf5e6d70)
 Call ID: 4de13324-3e87-4cad-bcf3-d6d5bf5e6d70
  Args:
    type: :Woman
    source: Antonia_of_Prussia
  AddLiteral (bde87143-373c-4114-b995-e05eafc752e5)
 Call ID: bde87143-373c-4114-b995-e05eafc752e5
  Args:
    literal_value: 1955
    relation: :hasBirthYear
    source: Antonia_of_Prussia
    literal_type: xsd:integer
  AssignClass (ce433ccd-4f6b-4f67-9734-55d326457c35)
 Call ID: ce433ccd-4f6b-4f67-9734-55d326457c35
  Args:
    type: :Person
    source: Prince_Frederick_of_Prussia
  AssignClass (d45b4b69-fd73-4b1e-9c1b-4285779cf661)
 Call ID: d45b4b69-fd73-4b1e-9c1b-4285779cf661
  Args:
    type: :Man
    source: Prince_Frederick_of_Prussia
  AssignClass (01eeda49-7d6d-4c08-9a6d-654a58320d46)
 Call ID: 01eeda49-7d6d-4c08-9a6d-654a58320d46
  Args:
    type: :Person
    source: Lady_Brigid_Guinness
  AssignClass (6b1f3536-1825-4a77-98f3-d9277a9b0b12)
 Call ID: 6b1f3536-1825-4a77-98f3-d9277a9b0b12
  Args:
    type: :Woman
    source: Lady_Brigid_Guinness
  AddTriple (509b9b16-2ec2-4f9b-a73e-0667f1b96ab3)
 Call ID: 509b9b16-2ec2-4f9b-a73e-0667f1b96ab3
  Args:
    target: Prince_Frederick_of_Prussia
    source: Antonia_of_Prussia
    relation: :hasFather
  AddTriple (08805453-503d-4152-b622-418b10f33cec)
 Call ID: 08805453-503d-4152-b622-418b10f33cec
  Args:
    target: Lady_Brigid_Guinness
    relation: :hasMother
    source: Antonia_of_Prussia
  AssignClass (fdc41112-970c-4815-be09-c253e37345ca)
 Call ID: fdc41112-970c-4815-be09-c253e37345ca
  Args:
    type: :Person
    source: Charles_Wellesley
  AssignClass (f106822c-772d-4293-906e-f5dda39554b9)
 Call ID: f106822c-772d-4293-906e-f5dda39554b9
  Args:
    type: :Man
    source: Charles_Wellesley
  AddLiteral (cdd1af43-9310-4464-acb2-c1a38dc6577f)
 Call ID: cdd1af43-9310-4464-acb2-c1a38dc6577f
  Args:
    relation: :hasMarriageYear
    source: Antonia_of_Prussia
    literal_type: xsd:integer
    literal_value: 1977
  AddTriple (ec0a9c32-f8d0-472c-bc17-eadccfc27ef5)
 Call ID: ec0a9c32-f8d0-472c-bc17-eadccfc27ef5
  Args:
    target: Charles_Wellesley
    relation: :hasRelation
    source: Antonia_of_Prussia
  AssignClass (98292817-02ef-4c8e-a586-cbd75c8880e1)
 Call ID: 98292817-02ef-4c8e-a586-cbd75c8880e1
  Args:
    type: :Person
    source: Lady_Mary_Wellesley
  AssignClass (6ea417a3-ffc5-4dad-9b4b-d5e6373a0e61)
 Call ID: 6ea417a3-ffc5-4dad-9b4b-d5e6373a0e61
  Args:
    type: :Woman
    source: Lady_Mary_Wellesley
  AssignClass (b8dc0536-9faa-4d2a-8b72-467720c00391)
 Call ID: b8dc0536-9faa-4d2a-8b72-467720c00391
  Args:
    type: :Person
    source: Lady_Charlotte_Wellesley
  AssignClass (95fcd611-49ea-428d-b502-4fd01a65b614)
 Call ID: 95fcd611-49ea-428d-b502-4fd01a65b614
  Args:
    type: :Woman
    source: Lady_Charlotte_Wellesley
  AddTriple (48b4d138-0a00-4c08-bac6-2ba527ab76a7)
 Call ID: 48b4d138-0a00-4c08-bac6-2ba527ab76a7
  Args:
    target: Lady_Mary_Wellesley
    source: Antonia_of_Prussia
    relation: :hasChild
  AddTriple (ab172dda-d1ff-4deb-8f98-8a5ec8fe6d89)
 Call ID: ab172dda-d1ff-4deb-8f98-8a5ec8fe6d89
  Args:
    target: Lady_Charlotte_Wellesley
    source: Antonia_of_Prussia
    relation: :hasChild
  AddTriple (e8390c78-99c1-4666-91b8-7574fe0f1577)
 Call ID: e8390c78-99c1-4666-91b8-7574fe0f1577
  Args:
    target: Lady_Mary_Wellesley
    relation: :hasChild
    source: Charles_Wellesley
  AddTriple (478f94e6-faf5-4a8c-8cb3-47afbfacf439)
 Call ID: 478f94e6-faf5-4a8c-8cb3-47afbfacf439
  Args:
    source: Charles_Wellesley
    relation: :hasChild
    target: Lady_Charlotte_Wellesley
  Finish (cbc8aefc-d1ac-4f5d-83ed-ca6bf5c3f07c)
 Call ID: cbc8aefc-d1ac-4f5d-83ed-ca6bf5c3f07c
  Args: