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
Princess Margarita of Baden (Margarete Alice Thyra Viktoria Marie Louise Scholastica; 14 July 1932 – 15 January 2013) was the only daughter of Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark.
She was the eldest surviving cousin of King Charles III and eldest surviving niece of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
Early life

Margarita was born on 14 July 1932 at Schloss Salem, Germany, and grew up there.
She was the eldest child and only daughter of Berthold, Margrave of Baden, who ran a school jointly with Kurt Hahn, and Princess Theodora of Greece and Denmark, older sister of Prince Philip, Duke of Edinburgh.
Margarita was the first great-great-great-granddaughter of Queen Victoria.
She came to live in London in 1948, and trained as a nurse at St Thomas' Hospital.
During this time, she was often seen with her cousins Princess Christina of Hesse and Princess Beatrix of Hohenlohe-Langenburg.
Beatrix was briefly engaged to Margarita's brother Prince Maximilian, and Christina became Margarita's future sister-in-law by marrying Prince Andrew of Yugoslavia.
Also during this time, Margarita attended the 1953 coronation of her aunt, Queen Elizabeth II.
While in London, she met Prince Tomislav, a member of the exiled Yugoslav royal family as a younger brother of the former King Peter II of Yugoslavia.
Tomislav was a third cousin of Margarita's mother; both were great-great-grandchildren of Queen Victoria and Prince Albert.
Margarita and Tomislav became engaged on 2 January 1956.
She took part in the ship tour organized by King Paul of Greece and Queen Frederica in 1954, which became known as the "Cruise of the Kings" and was attended by over 100 royals from all over Europe.
Marriage

On 5 June 1957 Margarita married Prince Tomislav of Yugoslavia, younger brother of the former King Peter II of Yugoslavia, in a civil ceremony in Salem followed by Lutheran and Serbian Orthodox church services on 6 June.
She wore a "plain white corded silk dress with a V-neckline, long sleeves, and a full skirt, and an old family train" with an orange blossom garland.
Prince Philip, Duke of Edinburgh (her maternal uncle), and King Simeon of Bulgaria were among the guests.
Later years

Margarita was a champion of Serbian charities and was also president of the Convent of Martha and Mary in Moscow.
Margarita died on 15 January 2013 in Farnham, Surrey, after a long illness.
Her uncle the Duke of Edinburgh, Queen Anne-Marie of Greece, and her nephew Alexander, Crown Prince of Yugoslavia, were among the mourners.
Margarita was buried in the family cemetery at Stefansfeld near Baden, Germany, on 28 January 2013.



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
  AssignClass (d8da799b-c708-4a6f-8fa7-5311c46f1cb8)
 Call ID: d8da799b-c708-4a6f-8fa7-5311c46f1cb8
  Args:
    type: :Person
    source: Margarita_of_Baden
  AssignClass (7ab3645d-905e-4277-9c77-c7be9695c8f6)
 Call ID: 7ab3645d-905e-4277-9c77-c7be9695c8f6
  Args:
    type: :Woman
    source: Margarita_of_Baden
  AddLiteral (e70c4951-549b-4c70-a099-3b1908c22531)
 Call ID: e70c4951-549b-4c70-a099-3b1908c22531
  Args:
    literal_value: Female
    literal_type: xsd:string
    relation: :hasSex
    source: Margarita_of_Baden
  AddLiteral (c92a1d35-7779-4ea9-8626-10f2049b19d2)
 Call ID: c92a1d35-7779-4ea9-8626-10f2049b19d2
  Args:
    source: Margarita_of_Baden
    relation: :hasBirthYear
    literal_value: 1932
    literal_type: xsd:integer
  AddLiteral (bcf86125-ba85-4d54-a821-61433902df99)
 Call ID: bcf86125-ba85-4d54-a821-61433902df99
  Args:
    literal_value: 2013
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Margarita_of_Baden
  AssignClass (d413d281-c1de-485d-905c-4c9fa05def99)
 Call ID: d413d281-c1de-485d-905c-4c9fa05def99
  Args:
    type: :Person
    source: Berthold_Margrave_of_Baden
  AssignClass (e0273737-de52-45e8-9d8f-cdf4579ec1e7)
 Call ID: e0273737-de52-45e8-9d8f-cdf4579ec1e7
  Args:
    type: :Man
    source: Berthold_Margrave_of_Baden
  AddLiteral (d906308a-d71e-43ec-ba0a-37ad0a8ae95c)
 Call ID: d906308a-d71e-43ec-ba0a-37ad0a8ae95c
  Args:
    literal_type: xsd:string
    literal_value: Male
    source: Berthold_Margrave_of_Baden
    relation: :hasSex
  AssignClass (6e3a6411-0fb3-4b3d-a59f-c6e924502a2a)
 Call ID: 6e3a6411-0fb3-4b3d-a59f-c6e924502a2a
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AssignClass (a19daa11-a74e-4085-b12c-5591a53ca349)
 Call ID: a19daa11-a74e-4085-b12c-5591a53ca349
  Args:
    type: :Woman
    source: Theodora_of_Greece_and_Denmark
  AddLiteral (49eaeee7-333a-41b0-8d0f-22bd7b6267a5)
 Call ID: 49eaeee7-333a-41b0-8d0f-22bd7b6267a5
  Args:
    relation: :hasSex
    source: Theodora_of_Greece_and_Denmark
    literal_type: xsd:string
    literal_value: Female
  AddTriple (a51cd0c7-134c-4bfe-af0d-2dc29b45d051)
 Call ID: a51cd0c7-134c-4bfe-af0d-2dc29b45d051
  Args:
    source: Margarita_of_Baden
    relation: :hasFather
    target: Berthold_Margrave_of_Baden
  AddTriple (9c7e6be1-140e-486e-b927-5e62eefcf37b)
 Call ID: 9c7e6be1-140e-486e-b927-5e62eefcf37b
  Args:
    source: Margarita_of_Baden
    relation: :hasMother
    target: Theodora_of_Greece_and_Denmark
  AssignClass (c60bf44d-68ac-471c-959e-9805af14db8a)
 Call ID: c60bf44d-68ac-471c-959e-9805af14db8a
  Args:
    source: Prince_Maximilian
    type: :Person
  AssignClass (b8e1dfd7-b164-4509-9efa-44736d64299b)
 Call ID: b8e1dfd7-b164-4509-9efa-44736d64299b
  Args:
    source: Prince_Maximilian
    type: :Man
  AddTriple (7d2502ad-bf1a-4f07-b339-14e7987ffef6)
 Call ID: 7d2502ad-bf1a-4f07-b339-14e7987ffef6
  Args:
    source: Margarita_of_Baden
    target: Prince_Maximilian
    relation: :hasBrother
  AssignClass (2876c7b3-8d77-41a6-8bf1-c9a60f2770ad)
 Call ID: 2876c7b3-8d77-41a6-8bf1-c9a60f2770ad
  Args:
    type: :Person
    source: Prince_Tomislav_of_Yugoslavia
  AssignClass (259ec6e7-88da-47f2-9573-2b86581bc82b)
 Call ID: 259ec6e7-88da-47f2-9573-2b86581bc82b
  Args:
    type: :Man
    source: Prince_Tomislav_of_Yugoslavia
  AddLiteral (c6c818ab-b0a9-43eb-b19f-0fddfd6610af)
 Call ID: c6c818ab-b0a9-43eb-b19f-0fddfd6610af
  Args:
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasMarriageYear
    source: Margarita_of_Baden
  AddTriple (d2e126c7-87f2-4e79-9ce7-5c9c6e03034c)
 Call ID: d2e126c7-87f2-4e79-9ce7-5c9c6e03034c
  Args:
    source: Margarita_of_Baden
    relation: :hasRelation
    target: Prince_Tomislav_of_Yugoslavia
  Finish (71dcd1a3-f86b-40cd-89d5-273ffd5de2bf)
 Call ID: 71dcd1a3-f86b-40cd-89d5-273ffd5de2bf
  Args: