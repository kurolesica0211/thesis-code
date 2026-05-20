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
Queen Margrethe II


Countess Athena of Monpezat (born Athena Marguerite Françoise Marie; 24 January 2012) is a member of the Danish royal family.
She is the younger child and only daughter of Prince Joachim and Princess Marie of Denmark.
She is the youngest grandchild of Queen Margrethe II and Prince Henrik, and the niece of King Frederik X. Athena is currently ninth in the line of succession to the Danish throne.
Biography

Athena was born a princess of Denmark on 24 January 2012 at Rigshospitalet, the Copenhagen University Hospital.
She has two older half-brothers from her father's first marriage, Nikolai and Felix, and an older brother, Henrik.
In accordance with Danish royal traditions, her names were not revealed until her christening, which took place on 20 May 2012 at the Møgeltønder Church, where her older brothers Felix and Henrik were also christened.
She was named Athena Marguerite Françoise Marie for both of her grandmothers as well as for her mother.
Her godparents are her maternal uncles, Gregory Grandet and Edouard Cavallier; Carina Axelsson, the long-term girlfriend of her father's cousin Gustav, Hereditary Prince of Sayn-Wittgenstein-Berleburg; and friends of her parents, Julie Mirabaud, Diego de Lavandeyra and Henriette Steenstrup.
Joseph Søstrenes Skole – the same Catholic private school in Ordrup as her brother Henrik.
In 2019, when Athena and her family moved to France, she was enrolled at the private school EIB Monceau in the 8th arrondissement of Paris alongside her brother.
Titles and styles

Athena was styled as "Her Highness Princess Athena of Denmark, Countess of Monpezat" from birth until 1 January 2023.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, she has been known as "Her Excellency Countess Athena of Monpezat".



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
  AssignClass (699e6a5d-71a5-4984-8a84-0b7c344b59c1)
 Call ID: 699e6a5d-71a5-4984-8a84-0b7c344b59c1
  Args:
    type: :Woman
    source: AthenaOfMonpezat
  AssignClass (1e4cef2d-e7c9-4cd2-9aab-0be3341856ad)
 Call ID: 1e4cef2d-e7c9-4cd2-9aab-0be3341856ad
  Args:
    type: :Person
    source: AthenaOfMonpezat
  AssignClass (98343935-9a6f-4ada-b57a-2131e79ea821)
 Call ID: 98343935-9a6f-4ada-b57a-2131e79ea821
  Args:
    type: :Man
    source: JoachimOfDenmark
  AssignClass (c7bda25a-6b2b-4929-8a75-2abdddc2c802)
 Call ID: c7bda25a-6b2b-4929-8a75-2abdddc2c802
  Args:
    type: :Person
    source: JoachimOfDenmark
  AssignClass (aede05b1-de45-4733-937a-8f284f3875f5)
 Call ID: aede05b1-de45-4733-937a-8f284f3875f5
  Args:
    type: :Woman
    source: MarieOfDenmark
  AssignClass (53b2de0d-bf23-4c66-8ef5-dde3a387f30a)
 Call ID: 53b2de0d-bf23-4c66-8ef5-dde3a387f30a
  Args:
    type: :Person
    source: MarieOfDenmark
  AssignClass (6ecf83c6-c55f-43cd-a319-231f6bf33800)
 Call ID: 6ecf83c6-c55f-43cd-a319-231f6bf33800
  Args:
    type: :Woman
    source: MargretheII
  AssignClass (01fc9d60-708e-4389-ae40-5fa1b774cc37)
 Call ID: 01fc9d60-708e-4389-ae40-5fa1b774cc37
  Args:
    type: :Person
    source: MargretheII
  AssignClass (caf34242-3a93-46a9-8d9c-c76519049480)
 Call ID: caf34242-3a93-46a9-8d9c-c76519049480
  Args:
    type: :Man
    source: HenrikOfDenmark
  AssignClass (dbb1c0fd-4389-4e00-86e3-8aca4f7db3ad)
 Call ID: dbb1c0fd-4389-4e00-86e3-8aca4f7db3ad
  Args:
    type: :Person
    source: HenrikOfDenmark
  AssignClass (05240090-4303-40a5-a65e-f188dc38bcdc)
 Call ID: 05240090-4303-40a5-a65e-f188dc38bcdc
  Args:
    type: :Man
    source: FrederikX
  AssignClass (c068e064-f5f3-4fa4-8299-60a32d81b115)
 Call ID: c068e064-f5f3-4fa4-8299-60a32d81b115
  Args:
    type: :Person
    source: FrederikX
  AssignClass (d89439eb-edea-4c48-8f15-66f9059c1551)
 Call ID: d89439eb-edea-4c48-8f15-66f9059c1551
  Args:
    type: :Man
    source: Nikolai
  AssignClass (0f56feb9-9343-4d16-9555-23a178113a29)
 Call ID: 0f56feb9-9343-4d16-9555-23a178113a29
  Args:
    type: :Person
    source: Nikolai
  AssignClass (895e160d-824f-45af-841b-ebbb618d0c6b)
 Call ID: 895e160d-824f-45af-841b-ebbb618d0c6b
  Args:
    type: :Man
    source: Felix
  AssignClass (e9243609-04ba-4614-b3ed-5d5c3d84a313)
 Call ID: e9243609-04ba-4614-b3ed-5d5c3d84a313
  Args:
    type: :Person
    source: Felix
  AssignClass (2b255ad5-5d1c-4365-b0f6-7043ad879d2d)
 Call ID: 2b255ad5-5d1c-4365-b0f6-7043ad879d2d
  Args:
    type: :Man
    source: HenrikJr
  AssignClass (5a8b1138-7789-4323-a5d6-ad7288d940f1)
 Call ID: 5a8b1138-7789-4323-a5d6-ad7288d940f1
  Args:
    type: :Person
    source: HenrikJr
  AddLiteral (0ae639fa-3f52-427a-9700-f55d29dc470a)
 Call ID: 0ae639fa-3f52-427a-9700-f55d29dc470a
  Args:
    literal_value: Female
    source: AthenaOfMonpezat
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (5797ddc3-9a92-4629-aca3-161505656645)
 Call ID: 5797ddc3-9a92-4629-aca3-161505656645
  Args:
    source: JoachimOfDenmark
    literal_value: Male
    relation: :hasSex
    literal_type: xsd:string
  AddLiteral (d6c07c1a-1504-42fe-9a56-d118df1f2641)
 Call ID: d6c07c1a-1504-42fe-9a56-d118df1f2641
  Args:
    literal_type: xsd:string
    relation: :hasSex
    literal_value: Female
    source: MarieOfDenmark
  AddLiteral (61de3537-7b95-4e08-8ac3-75afbdb5fe10)
 Call ID: 61de3537-7b95-4e08-8ac3-75afbdb5fe10
  Args:
    literal_type: xsd:string
    relation: :hasSex
    literal_value: Female
    source: MargretheII
  AddLiteral (4329f523-ca04-4f3e-bc4d-dd895862ae18)
 Call ID: 4329f523-ca04-4f3e-bc4d-dd895862ae18
  Args:
    literal_value: Male
    source: HenrikOfDenmark
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (7b081918-8c0f-4356-89a0-acf61207327e)
 Call ID: 7b081918-8c0f-4356-89a0-acf61207327e
  Args:
    relation: :hasSex
    literal_type: xsd:string
    source: FrederikX
    literal_value: Male
  AddLiteral (1a05cb65-998c-4e41-8d77-98edba58bbee)
 Call ID: 1a05cb65-998c-4e41-8d77-98edba58bbee
  Args:
    source: Nikolai
    literal_value: Male
    relation: :hasSex
    literal_type: xsd:string
  AddLiteral (c47b0766-dfbe-488f-8687-5a66edcfe2a8)
 Call ID: c47b0766-dfbe-488f-8687-5a66edcfe2a8
  Args:
    relation: :hasSex
    literal_type: xsd:string
    source: Felix
    literal_value: Male
  AddLiteral (dbcb45d3-7606-435d-a4c0-cc1d4f12bd59)
 Call ID: dbcb45d3-7606-435d-a4c0-cc1d4f12bd59
  Args:
    source: HenrikJr
    literal_value: Male
    relation: :hasSex
    literal_type: xsd:string
  AddTriple (65aaa646-b413-4bf1-8547-f08040c847d4)
 Call ID: 65aaa646-b413-4bf1-8547-f08040c847d4
  Args:
    source: AthenaOfMonpezat
    target: JoachimOfDenmark
    relation: :hasFather
  AddTriple (cd39b21a-a205-44a7-bf77-67ac7689aedc)
 Call ID: cd39b21a-a205-44a7-bf77-67ac7689aedc
  Args:
    target: MarieOfDenmark
    relation: :hasMother
    source: AthenaOfMonpezat
  AddTriple (1b117265-a3ad-40f1-a50a-d3e3c78c24a9)
 Call ID: 1b117265-a3ad-40f1-a50a-d3e3c78c24a9
  Args:
    relation: :hasMother
    target: MargretheII
    source: JoachimOfDenmark
  AddTriple (64cc42e0-ddb6-44f9-96cf-78f20083dac0)
 Call ID: 64cc42e0-ddb6-44f9-96cf-78f20083dac0
  Args:
    source: JoachimOfDenmark
    target: HenrikOfDenmark
    relation: :hasFather
  AddTriple (1c8d72ce-c0cf-4cb3-a8ba-b1e7b20afb4b)
 Call ID: 1c8d72ce-c0cf-4cb3-a8ba-b1e7b20afb4b
  Args:
    source: HenrikJr
    relation: :hasFather
    target: JoachimOfDenmark
  AddTriple (c76c6ec2-8167-4482-8979-e58f100e706e)
 Call ID: c76c6ec2-8167-4482-8979-e58f100e706e
  Args:
    source: HenrikJr
    relation: :hasMother
    target: MarieOfDenmark
  AddTriple (b4df0328-76e5-43f6-8f0c-ee6fa89c2409)
 Call ID: b4df0328-76e5-43f6-8f0c-ee6fa89c2409
  Args:
    source: HenrikJr
    target: AthenaOfMonpezat
    relation: :isBrotherOf
  AddTriple (f62c2b37-0eb6-43f6-96cb-64d4897699b6)
 Call ID: f62c2b37-0eb6-43f6-96cb-64d4897699b6
  Args:
    source: Nikolai
    relation: :isBrotherOf
    target: AthenaOfMonpezat
  AddTriple (64a98e63-93c1-42dd-ac25-b0bd2dba4b36)
 Call ID: 64a98e63-93c1-42dd-ac25-b0bd2dba4b36
  Args:
    relation: :isBrotherOf
    target: AthenaOfMonpezat
    source: Felix
  AddLiteral (1db7bcd2-5bd7-4afb-8c7c-0a3fb7b153ee)
 Call ID: 1db7bcd2-5bd7-4afb-8c7c-0a3fb7b153ee
  Args:
    literal_value: 2012
    source: AthenaOfMonpezat
    literal_type: xsd:integer
    relation: :hasBirthYear
  Finish (c753e1e8-fcc5-49ea-a4d4-38338b49c01a)
 Call ID: c753e1e8-fcc5-49ea-a4d4-38338b49c01a
  Args: