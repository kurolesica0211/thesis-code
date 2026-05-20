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
Lord Nicholas Charles Edward Jonathan Windsor (born 25 July 1970) is a relative of the British royal family, the youngest child of Prince Edward, Duke of Kent.
Lord Nicholas has voiced strong anti-abortion views.
Early years

Nicholas Charles Edward Jonathan Windsor was born on 25 July 1970 at King's College Hospital in Denmark Hill, London, to Prince Edward, Duke of Kent and Katharine, Duchess of Kent.
He has an older brother, Earl of St Andrews, and a sister, Lady Helen Taylor.
He was baptised later that year at Windsor Castle.
His godparents included his paternal second cousin Charles, Prince of Wales (later King Charles III), and Donald Coggan, at the time Archbishop of York and later Archbishop of Canterbury.
Religion

Nicholas's mother, the Duchess of Kent, had been received into the Catholic Church in 1994.
On 14 July 2011, Nicholas became an Honorary Vice-president of the Friends of the Personal Ordinariate of Our Lady of Walsingham, an Anglican Ordinariate within the Catholic Church.
Nicholas is also a patron of the Society of King Charles the Martyr and, though it is a largely Anglican society, he identifies it with his Catholic faith.
In a passage written by Windsor for the Society's website, he extols Charles's virtues: "In the King's personal piety, devotion and support of the Church, his ecumenical understanding (far advanced for his day), his patronage of the Arts in the service of God, his inspiration of the Christian classic, Eikon Basilike and of course his martyrdom, we have much to REMEMBER and be thankful for.
"


Nicholas has voiced strong views on the issue of abortion, which he has stated is, as a societal threat, "worse than al-Qaeda".
Marriage and family

Nicholas met his future wife, Paola Doimi de Lupis Frankopan Šubić Zrinski, at a party in New York City in 1999 to mark the Millennium.
By the marriage, the bride became Lady Nicholas Windsor.



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
  AssignClass (b410372b-509b-44d8-a9fd-782d774e7a90)
 Call ID: b410372b-509b-44d8-a9fd-782d774e7a90
  Args:
    source: Nicholas_Windsor
    type: :Man
  AssignClass (83d32468-9a58-4d9a-acf8-de900caebb04)
 Call ID: 83d32468-9a58-4d9a-acf8-de900caebb04
  Args:
    source: Nicholas_Windsor
    type: :Person
  AddLiteral (267409e5-7ec4-4050-a0f0-b7a74c06dfb3)
 Call ID: 267409e5-7ec4-4050-a0f0-b7a74c06dfb3
  Args:
    source: Nicholas_Windsor
    literal_value: 1970
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (7f9938c0-5028-4223-81a4-5880a2023937)
 Call ID: 7f9938c0-5028-4223-81a4-5880a2023937
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (4b088d1d-ba16-4e9e-b385-8a1fc136abb8)
 Call ID: 4b088d1d-ba16-4e9e-b385-8a1fc136abb8
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (0c5b0384-5313-4076-80d5-fe416dccf1e3)
 Call ID: 0c5b0384-5313-4076-80d5-fe416dccf1e3
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (7930f65a-be4c-4cb2-a030-dd1719557dd1)
 Call ID: 7930f65a-be4c-4cb2-a030-dd1719557dd1
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (08f2a815-4f12-4de6-8a96-ba065ea79f26)
 Call ID: 08f2a815-4f12-4de6-8a96-ba065ea79f26
  Args:
    source: Nicholas_Windsor
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
  AddTriple (c4f4fd7c-1cb2-46a7-a341-2c4c7f755f80)
 Call ID: c4f4fd7c-1cb2-46a7-a341-2c4c7f755f80
  Args:
    source: Nicholas_Windsor
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
  AssignClass (4255330f-e4b9-4a90-959b-9e707c212031)
 Call ID: 4255330f-e4b9-4a90-959b-9e707c212031
  Args:
    type: :Man
    source: Earl_of_St_Andrews
  AssignClass (7ba2663f-caab-42a0-8f16-8f815c077135)
 Call ID: 7ba2663f-caab-42a0-8f16-8f815c077135
  Args:
    source: Earl_of_St_Andrews
    type: :Person
  AddTriple (86a4368d-2498-4a9d-8a04-ef5d6fb731c6)
 Call ID: 86a4368d-2498-4a9d-8a04-ef5d6fb731c6
  Args:
    target: Earl_of_St_Andrews
    relation: :hasBrother
    source: Nicholas_Windsor
  AssignClass (3463c209-97d0-4f76-9cb4-34f90a3a3b1b)
 Call ID: 3463c209-97d0-4f76-9cb4-34f90a3a3b1b
  Args:
    type: :Woman
    source: Lady_Helen_Taylor
  AssignClass (64a91a5b-f7d7-476a-b36b-a95c505425e5)
 Call ID: 64a91a5b-f7d7-476a-b36b-a95c505425e5
  Args:
    type: :Person
    source: Lady_Helen_Taylor
  AddTriple (0da0cc76-f466-42c2-8e50-6ab024686f74)
 Call ID: 0da0cc76-f466-42c2-8e50-6ab024686f74
  Args:
    target: Lady_Helen_Taylor
    relation: :hasSister
    source: Nicholas_Windsor
  AssignClass (00128f7d-a85f-4f6a-b7d1-3f96190921e0)
 Call ID: 00128f7d-a85f-4f6a-b7d1-3f96190921e0
  Args:
    source: Paola_Doimi_de_Lupis_Frankopan_Subic_Zrinski
    type: :Woman
  AssignClass (08672195-0c2c-4a37-973e-104887e57993)
 Call ID: 08672195-0c2c-4a37-973e-104887e57993
  Args:
    source: Paola_Doimi_de_Lupis_Frankopan_Subic_Zrinski
    type: :Person
  AddTriple (55950658-0be9-4e89-bbe5-2acc39df11fd)
 Call ID: 55950658-0be9-4e89-bbe5-2acc39df11fd
  Args:
    target: Paola_Doimi_de_Lupis_Frankopan_Subic_Zrinski
    relation: :hasRelation
    source: Nicholas_Windsor
  Finish (39255079-9d24-4309-b880-4a3d628fdb9e)
 Call ID: 39255079-9d24-4309-b880-4a3d628fdb9e
  Args: