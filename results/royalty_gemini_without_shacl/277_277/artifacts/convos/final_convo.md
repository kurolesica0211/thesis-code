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
Knud, Hereditary Prince of Denmark (Knud Christian Frederik Michael; 27 July 1900 – 14 June 1976) was a member of the Danish royal family, the younger son and child of King Christian X and Queen Alexandrine.
From 1947 to 1953, he was heir presumptive to his older brother, King Frederik IX, and would have succeeded him as king following his death in January 1972 had it not been for a change in the Danish Act of Succession that replaced him with his niece, Queen Margrethe II.
Later, Knud's two sons, Ingolf and Christian, were stripped of their titles of prince and removed from the line of succession by the new law because they had married commoners without asking consent from their uncle.
Early life

Prince Knud was born on 27 July 1900 at his parents' country residence, the Sorgenfri Palace, located on the shores of the small river Mølleåen in Kongens Lyngby north of Copenhagen on the island of Zealand in Denmark, during the reign of his great-grandfather King Christian IX.
His parents were Prince Christian of Denmark, son of the heir apparent Crown Prince Frederik of Denmark, and Alexandrine of Mecklenburg-Schwerin.
Knud's only sibling, Prince Frederik, had been born one year before him.
Christian IX died on 29 January 1906, and Knud's grandfather succeeded him as Frederik VIII.
Six years later, on 14 May 1912, Frederik VIII died, and Knud's father ascended the throne as Christian X.


As was customary for princes at that time, Knud started a military education and entered the naval college.
Engagement and marriage

On 27 January 1933, at the age of 32, Prince Knud was engaged to his first cousin, the 20-year-old Princess Caroline-Mathilde of Denmark.
Princess Caroline-Mathilde was the second daughter of Prince Harald of Denmark and Princess Helena of Schleswig-Holstein-Sonderburg-Glücksburg, and their fathers were brothers.
The wedding was celebrated on 8 September 1933 at the chapel of Fredensborg Palace in North Zealand, Denmark.
Here they created a home for their three children: Princess Elisabeth (born in 1935), Prince Ingolf (born in 1940) and Prince Christian (born in 1944).
In 1944, Prince Knud inherited Egelund House near Fredensborg in North Zealand from his uncle, Prince Gustav of Denmark, which the couple then used as their summer residence until the hereditary prince sold it to the Danish Employers' Association in 1954.
In 1952, Prince Knud also inherited his parents' holiday residence Klitgaarden in Skagen in North Jutland from his mother, Queen Alexandrine, which the couple then used as their holiday home, and which remained in the family's possession until 1997.
Heir presumptive

On 20 April 1947, Christian X died, and Knud's brother Frederick succeeded to the throne as Frederik IX.
Since Frederik IX had fathered no sons and the Danish Act of Succession at the time followed the principle of agnatic primogeniture, Prince Knud became heir presumptive and first in line to succeed his brother as king.
Frederik IX had, however, fathered three daughters.
The new law made Frederik IX's thirteen-year-old daughter Margrethe the new heir presumptive, placing her and her two sisters before Knud and his family in the line of succession.
Later life and legacy

King Frederik IX died in 1972 and was succeeded by his daughter Queen Margrethe II.
The Princess Caroline-Mathilde Alps in Greenland were named by the 1938–39 Mørkefjord Expedition in his wife's honour for Prince Knud had been the patron of the expedition.
Prince Knud and Princess Caroline Mathilde had sat in the former royal loge at the far left of the hall (i.e., stage right), but one especially memorable scene had not been fully visible from where they had sat.



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
  AssignClass (883155c3-0422-4316-8453-1fba3c33d25d)
 Call ID: 883155c3-0422-4316-8453-1fba3c33d25d
  Args:
    type: :Man
    source: Knud
  AssignClass (be0ff150-5c7d-4960-9047-5d03e26495e0)
 Call ID: be0ff150-5c7d-4960-9047-5d03e26495e0
  Args:
    source: Christian_X
    type: :Man
  AssignClass (7184cb5c-688c-4a58-a62e-d8b6d6e66290)
 Call ID: 7184cb5c-688c-4a58-a62e-d8b6d6e66290
  Args:
    type: :Woman
    source: Alexandrine
  AssignClass (48ded9ab-65c6-499a-a9ba-a8736ddaf726)
 Call ID: 48ded9ab-65c6-499a-a9ba-a8736ddaf726
  Args:
    source: Frederik_IX
    type: :Man
  AssignClass (9e201889-f416-4543-9011-9096b6807a96)
 Call ID: 9e201889-f416-4543-9011-9096b6807a96
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (36cba210-55ad-48a1-84ab-b8a47fe5eb0a)
 Call ID: 36cba210-55ad-48a1-84ab-b8a47fe5eb0a
  Args:
    source: Ingolf
    type: :Man
  AssignClass (44bff7a1-5c29-4fad-bf6c-7ab850042620)
 Call ID: 44bff7a1-5c29-4fad-bf6c-7ab850042620
  Args:
    type: :Man
    source: Christian_son_of_Knud
  AssignClass (d880a785-9363-49e1-9887-92eee7d43ed9)
 Call ID: d880a785-9363-49e1-9887-92eee7d43ed9
  Args:
    source: Caroline-Mathilde
    type: :Woman
  AssignClass (7b8f5f69-4dee-402b-8d4c-fbeeb820332f)
 Call ID: 7b8f5f69-4dee-402b-8d4c-fbeeb820332f
  Args:
    source: Harald
    type: :Man
  AssignClass (5cc847d2-6f5f-4fc8-a8fe-5de7f41d1cbf)
 Call ID: 5cc847d2-6f5f-4fc8-a8fe-5de7f41d1cbf
  Args:
    type: :Woman
    source: Helena
  AssignClass (5bc5cbd5-2f7c-4f20-a274-ccbbe8db82da)
 Call ID: 5bc5cbd5-2f7c-4f20-a274-ccbbe8db82da
  Args:
    type: :Woman
    source: Elisabeth
  AssignClass (e8e3fb70-fd40-4862-98c9-e16ff5ecf206)
 Call ID: e8e3fb70-fd40-4862-98c9-e16ff5ecf206
  Args:
    source: Gustav
    type: :Man
  AssignClass (c5dbe89d-0401-4ff2-820e-5e262af57e9f)
 Call ID: c5dbe89d-0401-4ff2-820e-5e262af57e9f
  Args:
    type: :Man
    source: Christian_IX
  AssignClass (076d4981-835b-4c82-b27e-12d4e9d79efb)
 Call ID: 076d4981-835b-4c82-b27e-12d4e9d79efb
  Args:
    type: :Man
    source: Frederik_VIII
  AssignClass (d740b373-11f5-47e1-a0ff-8ebc4dbaf3d8)
 Call ID: d740b373-11f5-47e1-a0ff-8ebc4dbaf3d8
  Args:
    source: Crown_Prince_Frederik
    type: :Man
  AddLiteral (8975b3a9-b71c-48cc-acfe-3ab340305267)
 Call ID: 8975b3a9-b71c-48cc-acfe-3ab340305267
  Args:
    literal_value: 1900
    source: Knud
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (afb89d52-94a5-4181-9446-e184c6a2767f)
 Call ID: afb89d52-94a5-4181-9446-e184c6a2767f
  Args:
    literal_value: 1976
    source: Knud
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (6af98ad4-e7ef-4927-a002-dadae430015b)
 Call ID: 6af98ad4-e7ef-4927-a002-dadae430015b
  Args:
    relation: :hasFather
    target: Christian_X
    source: Knud
  AddTriple (50b81a36-ea8e-45f5-bc72-aec178752b23)
 Call ID: 50b81a36-ea8e-45f5-bc72-aec178752b23
  Args:
    source: Knud
    target: Alexandrine
    relation: :hasMother
  AddTriple (6adba322-d413-4665-83aa-91c760fbd426)
 Call ID: 6adba322-d413-4665-83aa-91c760fbd426
  Args:
    source: Knud
    relation: :hasBrother
    target: Frederik_IX
  AddTriple (d5818d98-d722-4044-8346-1ef447a6f9e4)
 Call ID: d5818d98-d722-4044-8346-1ef447a6f9e4
  Args:
    source: Knud
    relation: :hasSon
    target: Ingolf
  AddTriple (663d7bd9-5674-4190-bb3c-bd7ff7b7f4bd)
 Call ID: 663d7bd9-5674-4190-bb3c-bd7ff7b7f4bd
  Args:
    source: Knud
    target: Christian_son_of_Knud
    relation: :hasSon
  AddTriple (b72aa7a5-6547-421f-b3ff-c50d2e07740b)
 Call ID: b72aa7a5-6547-421f-b3ff-c50d2e07740b
  Args:
    relation: :hasDaughter
    target: Elisabeth
    source: Knud
  AddTriple (8aa5cc78-f38e-4a67-af3b-1cb88026c9fe)
 Call ID: 8aa5cc78-f38e-4a67-af3b-1cb88026c9fe
  Args:
    target: Harald
    relation: :hasFather
    source: Caroline-Mathilde
  AddTriple (2a4afbc2-67b8-4b0e-a714-914e0e74e3e9)
 Call ID: 2a4afbc2-67b8-4b0e-a714-914e0e74e3e9
  Args:
    source: Caroline-Mathilde
    target: Helena
    relation: :hasMother
  AddTriple (64500c48-1486-4e5e-bf46-33e46f94f060)
 Call ID: 64500c48-1486-4e5e-bf46-33e46f94f060
  Args:
    source: Christian_X
    relation: :hasFather
    target: Frederik_VIII
  AddTriple (c5f87fbf-88f9-4f4e-8d1d-79a66b06afbe)
 Call ID: c5f87fbf-88f9-4f4e-8d1d-79a66b06afbe
  Args:
    target: Frederik_VIII
    relation: :hasFather
    source: Harald
  AddTriple (2ecde492-9909-4286-bf5d-606d9d35e33f)
 Call ID: 2ecde492-9909-4286-bf5d-606d9d35e33f
  Args:
    relation: :hasFather
    target: Christian_IX
    source: Frederik_VIII
  AddTriple (55108a8e-a5ca-4453-b121-2ab47ee68bed)
 Call ID: 55108a8e-a5ca-4453-b121-2ab47ee68bed
  Args:
    source: Crown_Prince_Frederik
    relation: :hasFather
    target: Christian_IX
  AddTriple (ab5e1717-b354-4223-83cd-6a80aa6d77a4)
 Call ID: ab5e1717-b354-4223-83cd-6a80aa6d77a4
  Args:
    source: Christian_X
    target: Crown_Prince_Frederik
    relation: :hasFather
  AddTriple (3dec64f1-c6c2-45a8-8442-1830563e825d)
 Call ID: 3dec64f1-c6c2-45a8-8442-1830563e825d
  Args:
    relation: :isMotherOf
    target: Knud
    source: Alexandrine
  AddTriple (4b75b748-b248-4f3f-a83d-d54f9f9ee73d)
 Call ID: 4b75b748-b248-4f3f-a83d-d54f9f9ee73d
  Args:
    target: Frederik_IX
    relation: :isMotherOf
    source: Alexandrine
  AddLiteral (e8a12584-1173-4bf2-a115-1a9a465e91b7)
 Call ID: e8a12584-1173-4bf2-a115-1a9a465e91b7
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1933
    source: Knud
  Finish (7ef5ebbb-8090-4eff-a5ad-9d8afabb7fcc)
 Call ID: 7ef5ebbb-8090-4eff-a5ad-9d8afabb7fcc
  Args: