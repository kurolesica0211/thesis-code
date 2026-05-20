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
Duke Christian Louis of Mecklenburg (German: Christian-Ludwig Herzog zu Mecklenburg; 29 September 1912 – 18 July 1996) was the second son of the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
Early life

Born in Schloss Ludwigslust, as a member of an elder, Mecklenburg-Schwerin line of an ancient House of Mecklenburg, he was the second child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife, Princess Alexandra of Hanover, third child and second daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark.
After the abolition of the monarchy, in 1919 the family went at the invitation of Queen Alexandrine, consort of Christian X of Denmark and sister of the Grand Duke, into exile in Denmark, where they lived for a year in Sorgenfri Palace.
Later, the family returned to Mecklenburg and lived in Gelbensande, and from 1921 the family settled at Ludwigslust Castle.
After the war

When the war ended, Ludwigslust was first occupied by the British, but soon was transferred to the Soviet occupation, so that Christian Louis initially went with his family to Glücksburg Castle in Schleswig-Holstein.
Together with his sister Thyra, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Marriage and family

On 5 July 1954 in Glücksburg, Christian Louis married in a civil wedding Princess Barbara of Prussia (1920–1994), the daughter of Prince Sigismund of Prussia and his wife, Princess Charlotte of Saxe-Altenburg.



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
  AssignClass (836d9a43-18bd-4d97-b13c-8e41a0914b62)
 Call ID: 836d9a43-18bd-4d97-b13c-8e41a0914b62
  Args:
    source: :ChristianLouisOfMecklenburg
    type: :Man
  AssignClass (e4644896-2a6a-4f99-9287-001510b50169)
 Call ID: e4644896-2a6a-4f99-9287-001510b50169
  Args:
    type: :Man
    source: :FrederickFrancisIV
  AssignClass (ae24b9c4-4d5a-4ba9-95d8-e02a8dfb8d46)
 Call ID: ae24b9c4-4d5a-4ba9-95d8-e02a8dfb8d46
  Args:
    source: :AlexandraOfHanover
    type: :Woman
  AssignClass (6df0a238-d4cd-4066-826b-73ee0583bf02)
 Call ID: 6df0a238-d4cd-4066-826b-73ee0583bf02
  Args:
    type: :Man
    source: :ErnestAugustusCrownPrinceOfHanover
  AssignClass (f2e0c8db-149f-48ad-b721-1ef3797de5a0)
 Call ID: f2e0c8db-149f-48ad-b721-1ef3797de5a0
  Args:
    type: :Woman
    source: :ThyraOfDenmark
  AssignClass (198e1c3a-0fcc-49ca-ad32-48830dc2af3d)
 Call ID: 198e1c3a-0fcc-49ca-ad32-48830dc2af3d
  Args:
    source: :ThyraOfMecklenburg
    type: :Woman
  AssignClass (53b3c50c-9431-41d2-b1c4-cb44e120227f)
 Call ID: 53b3c50c-9431-41d2-b1c4-cb44e120227f
  Args:
    type: :Woman
    source: :BarbaraOfPrussia
  AssignClass (9e3c9507-8d0a-4c7b-ae74-5c58adfd5381)
 Call ID: 9e3c9507-8d0a-4c7b-ae74-5c58adfd5381
  Args:
    source: :SigismundOfPrussia
    type: :Man
  AssignClass (c892fabc-7bf7-4299-b21d-53876ac69b7f)
 Call ID: c892fabc-7bf7-4299-b21d-53876ac69b7f
  Args:
    type: :Woman
    source: :CharlotteOfSaxeAltenburg
  AddLiteral (745dd70f-0495-49b0-922e-852751bc567c)
 Call ID: 745dd70f-0495-49b0-922e-852751bc567c
  Args:
    relation: :hasBirthYear
    literal_value: 1912
    source: :ChristianLouisOfMecklenburg
    literal_type: xsd:integer
  AddLiteral (aa944752-f0ee-49ab-b8f3-dc474185acbf)
 Call ID: aa944752-f0ee-49ab-b8f3-dc474185acbf
  Args:
    literal_type: xsd:integer
    source: :ChristianLouisOfMecklenburg
    literal_value: 1996
    relation: :hasDeathYear
  AddTriple (98cb8877-18e6-4f61-a2d2-7d09449cb07e)
 Call ID: 98cb8877-18e6-4f61-a2d2-7d09449cb07e
  Args:
    source: :ChristianLouisOfMecklenburg
    target: :FrederickFrancisIV
    relation: :hasFather
  AddTriple (a0d5f11a-5075-495d-86d3-ac616b4b6296)
 Call ID: a0d5f11a-5075-495d-86d3-ac616b4b6296
  Args:
    source: :ChristianLouisOfMecklenburg
    relation: :hasMother
    target: :AlexandraOfHanover
  AddTriple (3239c238-7144-4934-876a-83c00fb597dc)
 Call ID: 3239c238-7144-4934-876a-83c00fb597dc
  Args:
    target: :ErnestAugustusCrownPrinceOfHanover
    relation: :hasFather
    source: :AlexandraOfHanover
  AddTriple (84698a59-9721-49ce-8849-21ebb19e6940)
 Call ID: 84698a59-9721-49ce-8849-21ebb19e6940
  Args:
    source: :AlexandraOfHanover
    relation: :hasMother
    target: :ThyraOfDenmark
  AddTriple (ce30aa7b-7631-49e3-8c94-5864abb2db76)
 Call ID: ce30aa7b-7631-49e3-8c94-5864abb2db76
  Args:
    source: :ChristianLouisOfMecklenburg
    relation: :hasSister
    target: :ThyraOfMecklenburg
  AddTriple (bb42d420-a24c-42c3-b0e0-f703e35f5dbd)
 Call ID: bb42d420-a24c-42c3-b0e0-f703e35f5dbd
  Args:
    source: :BarbaraOfPrussia
    target: :SigismundOfPrussia
    relation: :hasFather
  AddTriple (66bf79e5-bd16-41e5-89f8-e9a5f74dc85f)
 Call ID: 66bf79e5-bd16-41e5-89f8-e9a5f74dc85f
  Args:
    source: :BarbaraOfPrussia
    target: :CharlotteOfSaxeAltenburg
    relation: :hasMother
  AddLiteral (6eb23ace-cc59-4ad9-8871-baa5df55b2ad)
 Call ID: 6eb23ace-cc59-4ad9-8871-baa5df55b2ad
  Args:
    literal_value: 1954
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :ChristianLouisOfMecklenburg
  AddTriple (908f5996-63d4-4a0c-8ef7-f22c001bdd5e)
 Call ID: 908f5996-63d4-4a0c-8ef7-f22c001bdd5e
  Args:
    relation: :hasRelation
    target: :BarbaraOfPrussia
    source: :ChristianLouisOfMecklenburg
  Finish (52b4ab02-3302-4e59-9c63-e83d69853081)
 Call ID: 52b4ab02-3302-4e59-9c63-e83d69853081
  Args: