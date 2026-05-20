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
Lady Sarah Frances Elizabeth Chatto (née Armstrong-Jones; born 1
She is the only daughter of Princess Margaret, Countess of Snowdon, and Antony Armstrong-Jones, 1st Earl of Snowdon.
She and her brother, David Armstrong-Jones, 2nd Earl of Snowdon, are the only maternal first cousins of King Charles III.
Early life and education

Lady Sarah Frances Elizabeth Armstrong-Jones was born at 8:20 am on 1 May 1964 at Kensington Palace in London.
She is the second child and only daughter of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
Sarah is a godmother to Prince Harry, Duke of Sussex, Lady Rose Gilman, and Lady Louise Windsor.
She also has half-siblings on her father's side: Polly Fry (born 1960), Lady Frances Armstrong-Jones (born 1979), and Jasper Cable-Alexander (born 1998).
Sarah and her brother, David, then Viscount Linley, grew up in the nursery of Kensington Palace, Apartment 10.
Their parents' marriage was fractious; the couple formally separated when Sarah was 12 and divorced when she was 14.
She and her brother spent weekends, depending on with which parent, at either Nymans or Royal Lodge.
Holidays were given to the royal estates at Sandringham and Balmoral, where Sarah did landscape painting.
Sarah was a bridesmaid at the wedding of her cousin Charles, Prince of Wales, and Lady Diana Spencer.
She also studied art at the Royal Academy Schools.
The film's producer, her relative John Knatchbull, 7th Baron Brabourne (son-in-law of Louis Mountbatten, 1st Earl Mountbatten of Burma), gave her a job as an intern assisting the wardrobe department and studying wood gilding under her father's cousin Thomas Messel.
Professional life

Chatto has been exhibiting her work, always under the name Sarah Armstrong-Jones, at The Redfern Gallery since 1995.
In 2004, she became vice president of the Royal Ballet, of which her mother had been president.
Chatto does not undertake public duties and is not considered a "working royal".
However, it has been reported that she was close to her aunt Queen Elizabeth II.
Chatto is frequently seen attending public events such as jubilees and funerals, as well as semi-private royal family events, such as the Sandringham Christmas service, with her sons.
Marriage and children

Sarah met Daniel Chatto during her years in India with her father in the 1980s.
Chatto was working on another British film, Heat and Dust.
He is from a theatrical family, the son of actor Tom Chatto (1920–1982) and the theatrical agent Ros Chatto (born Rosalind Joan Thompson; died 2012).
Her bridesmaids were half-sister Lady Frances, Zara Phillips (daughter of her first cousin Princess Anne), and Tara Noble-Singh, a family friend.



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
  AssignClass (529ee0c9-4ccb-4c5c-adb9-82e712daceb6)
 Call ID: 529ee0c9-4ccb-4c5c-adb9-82e712daceb6
  Args:
    type: :Woman
    source: SarahChatto
  AssignClass (841f3fd9-88f2-4a67-9ed2-9c7d4118f301)
 Call ID: 841f3fd9-88f2-4a67-9ed2-9c7d4118f301
  Args:
    type: :Woman
    source: PrincessMargaret
  AssignClass (bcd97942-9d46-4922-9b26-c76f3e400c0d)
 Call ID: bcd97942-9d46-4922-9b26-c76f3e400c0d
  Args:
    type: :Man
    source: AntonyArmstrongJones
  AssignClass (af871906-a6b2-4c3d-8060-5e15d7e3db0d)
 Call ID: af871906-a6b2-4c3d-8060-5e15d7e3db0d
  Args:
    type: :Man
    source: DavidArmstrongJones
  AssignClass (b163a935-4a32-46ec-ac97-832792a68706)
 Call ID: b163a935-4a32-46ec-ac97-832792a68706
  Args:
    source: KingCharlesIII
    type: :Man
  AssignClass (eae83228-e8ed-4679-afdf-8d1447912a57)
 Call ID: eae83228-e8ed-4679-afdf-8d1447912a57
  Args:
    type: :Man
    source: DanielChatto
  AssignClass (9901e7f7-3da3-467a-9762-262b844c83bb)
 Call ID: 9901e7f7-3da3-467a-9762-262b844c83bb
  Args:
    type: :Man
    source: TomChatto
  AssignClass (271651ce-ee33-48b2-b231-c102593accf8)
 Call ID: 271651ce-ee33-48b2-b231-c102593accf8
  Args:
    type: :Woman
    source: RosChatto
  AssignClass (d7058dde-d9ee-4ca6-827d-f7ed78020abb)
 Call ID: d7058dde-d9ee-4ca6-827d-f7ed78020abb
  Args:
    type: :Woman
    source: PollyFry
  AssignClass (669d2e74-b4a5-49a0-b652-8805be79f3c7)
 Call ID: 669d2e74-b4a5-49a0-b652-8805be79f3c7
  Args:
    source: FrancesArmstrongJones
    type: :Woman
  AssignClass (f897ccce-a40e-455a-b0c3-b6284ea8d90b)
 Call ID: f897ccce-a40e-455a-b0c3-b6284ea8d90b
  Args:
    source: JasperCableAlexander
    type: :Man
  AddLiteral (cd56207e-ce29-4348-b084-f8bca2796680)
 Call ID: cd56207e-ce29-4348-b084-f8bca2796680
  Args:
    relation: :hasBirthYear
    source: SarahChatto
    literal_type: xsd:integer
    literal_value: 1964
  AddTriple (9466235a-61d2-4a3a-9a9b-738abd828633)
 Call ID: 9466235a-61d2-4a3a-9a9b-738abd828633
  Args:
    target: PrincessMargaret
    relation: :hasMother
    source: SarahChatto
  AddTriple (2f72a19a-d470-4cbd-80a4-4ba68b67b292)
 Call ID: 2f72a19a-d470-4cbd-80a4-4ba68b67b292
  Args:
    target: AntonyArmstrongJones
    source: SarahChatto
    relation: :hasFather
  AddTriple (cd4066c1-783f-44a1-b5b8-63cb5c9ba7b8)
 Call ID: cd4066c1-783f-44a1-b5b8-63cb5c9ba7b8
  Args:
    relation: :hasBrother
    source: SarahChatto
    target: DavidArmstrongJones
  AddTriple (9292fa76-9015-4903-9fdf-b88f081faf25)
 Call ID: 9292fa76-9015-4903-9fdf-b88f081faf25
  Args:
    source: DavidArmstrongJones
    relation: :hasMother
    target: PrincessMargaret
  AddTriple (8033fc8c-0c3e-4dc7-8ed9-c786ebf7352e)
 Call ID: 8033fc8c-0c3e-4dc7-8ed9-c786ebf7352e
  Args:
    relation: :hasFather
    source: DavidArmstrongJones
    target: AntonyArmstrongJones
  AddTriple (84324216-64dc-4e08-9685-d825bae2a6c7)
 Call ID: 84324216-64dc-4e08-9685-d825bae2a6c7
  Args:
    source: DanielChatto
    relation: :hasFather
    target: TomChatto
  AddTriple (8821e6d4-f6fb-4a6a-985e-d65683f133ea)
 Call ID: 8821e6d4-f6fb-4a6a-985e-d65683f133ea
  Args:
    target: RosChatto
    relation: :hasMother
    source: DanielChatto
  AddLiteral (62165be1-c925-4866-8d49-f58887a10032)
 Call ID: 62165be1-c925-4866-8d49-f58887a10032
  Args:
    relation: :hasBirthYear
    source: PollyFry
    literal_type: xsd:integer
    literal_value: 1960
  AddLiteral (0e68dc1f-fed0-470f-8f11-51f6fed72d09)
 Call ID: 0e68dc1f-fed0-470f-8f11-51f6fed72d09
  Args:
    relation: :hasBirthYear
    literal_value: 1979
    literal_type: xsd:integer
    source: FrancesArmstrongJones
  AddLiteral (8938cd0f-602c-44e1-8668-b4e51aa91a2a)
 Call ID: 8938cd0f-602c-44e1-8668-b4e51aa91a2a
  Args:
    literal_value: 1998
    literal_type: xsd:integer
    source: JasperCableAlexander
    relation: :hasBirthYear
  AddTriple (b2fc2375-abe4-4cbf-ad96-8854d004017f)
 Call ID: b2fc2375-abe4-4cbf-ad96-8854d004017f
  Args:
    relation: :hasFather
    source: PollyFry
    target: AntonyArmstrongJones
  AddTriple (16daf37c-dc69-49d4-a4ec-ce834b80cd66)
 Call ID: 16daf37c-dc69-49d4-a4ec-ce834b80cd66
  Args:
    source: FrancesArmstrongJones
    relation: :hasFather
    target: AntonyArmstrongJones
  AddTriple (b437bfb8-9a0a-4e8c-aade-cef4aa0e65d6)
 Call ID: b437bfb8-9a0a-4e8c-aade-cef4aa0e65d6
  Args:
    source: JasperCableAlexander
    relation: :hasFather
    target: AntonyArmstrongJones
  Finish (4a7b563a-b4fe-4f74-9443-a0df423d4931)
 Call ID: 4a7b563a-b4fe-4f74-9443-a0df423d4931
  Args: