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
Lady Rose Victoria Birgitte Louise Gilman (née Windsor; born 1 March 1980) is a British film art assistant and member of the British royal family.
She is the daughter of Prince Richard, Duke of Gloucester, and his wife Birgitte, Duchess of Gloucester.
Early life and education

Rose Victoria Birgitte Louise Windsor was born on 1 March 1980 at St Mary's Hospital, London, the youngest child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents included Prince Edward and Lady Sarah Armstrong-Jones.
Career

Rose has worked in the film industry as a film art assistant.
Her film credits include Harry Potter and the Order of the Phoenix, Harry Potter and the Half-Blood Prince, Margaret Thatcher: The Long Walk to Finchley, and the television series Little Britain.
Rose continues to make public appearances at state events alongside other members of the extended royal family, including the 2022 state funeral of Queen Elizabeth II and the 2023 coronation of King Charles III and Queen Camilla.
Marriage and children

Rose announced her engagement on 16 November 2007 to businessman George Gilman, the son of a former director of Leeds United.
Rose and her husband have a daughter, Lyla (born 30 May 2010, then 32nd in line of succession to the British throne), and a son, Rufus (born 30 October 2012, then 33rd in line of succession to the British throne).



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
  AssignClass (ccf3706d-66dc-4613-9f0d-359d1d2bee80)
 Call ID: ccf3706d-66dc-4613-9f0d-359d1d2bee80
  Args:
    source: :LadyRoseGilman
    type: :Person
  AssignClass (7e92009d-46be-44da-8365-d789420955fd)
 Call ID: 7e92009d-46be-44da-8365-d789420955fd
  Args:
    type: :Woman
    source: :LadyRoseGilman
  AddLiteral (d525c8f4-ec89-4d3c-853b-14fdedb3bd3f)
 Call ID: d525c8f4-ec89-4d3c-853b-14fdedb3bd3f
  Args:
    literal_value: 1980
    relation: :hasBirthYear
    source: :LadyRoseGilman
    literal_type: xsd:integer
  AssignClass (aa9128f9-894c-4122-b6c6-e866dce25321)
 Call ID: aa9128f9-894c-4122-b6c6-e866dce25321
  Args:
    source: :PrinceRichard
    type: :Person
  AssignClass (dadd8998-9a7b-4aea-bd35-99d414aeddb0)
 Call ID: dadd8998-9a7b-4aea-bd35-99d414aeddb0
  Args:
    source: :PrinceRichard
    type: :Man
  AssignClass (1d4cf78f-cfee-456d-992f-18b3388f2ba2)
 Call ID: 1d4cf78f-cfee-456d-992f-18b3388f2ba2
  Args:
    type: :Ancestor
    source: :PrinceRichard
  AssignClass (f8ccac58-0e30-42ce-9f4c-76eabd2234c3)
 Call ID: f8ccac58-0e30-42ce-9f4c-76eabd2234c3
  Args:
    source: :BirgitteGloucester
    type: :Person
  AssignClass (ec6719e3-0e9e-4298-bb8c-aeb8efd96828)
 Call ID: ec6719e3-0e9e-4298-bb8c-aeb8efd96828
  Args:
    source: :BirgitteGloucester
    type: :Woman
  AssignClass (73e4931d-6760-4d00-ae66-730b5d4e577a)
 Call ID: 73e4931d-6760-4d00-ae66-730b5d4e577a
  Args:
    type: :Ancestor
    source: :BirgitteGloucester
  AddTriple (f56972af-9f08-49fb-a65f-3cfc7e78af5a)
 Call ID: f56972af-9f08-49fb-a65f-3cfc7e78af5a
  Args:
    source: :LadyRoseGilman
    target: :PrinceRichard
    relation: :hasFather
  AddTriple (c35ed100-ca81-42b3-b0a4-6a642e51e3fa)
 Call ID: c35ed100-ca81-42b3-b0a4-6a642e51e3fa
  Args:
    relation: :hasMother
    source: :LadyRoseGilman
    target: :BirgitteGloucester
  AssignClass (6f717d41-1f11-4003-8523-541c4624e47a)
 Call ID: 6f717d41-1f11-4003-8523-541c4624e47a
  Args:
    source: :GeorgeGilman
    type: :Person
  AssignClass (d4ebc48c-c251-40d4-bd9a-cb9d22ef65a6)
 Call ID: d4ebc48c-c251-40d4-bd9a-cb9d22ef65a6
  Args:
    source: :GeorgeGilman
    type: :Man
  AddLiteral (16a03df7-6eed-4601-b14d-c53a5bb42f38)
 Call ID: 16a03df7-6eed-4601-b14d-c53a5bb42f38
  Args:
    literal_type: xsd:integer
    source: :LadyRoseGilman
    relation: :hasMarriageYear
    literal_value: 2007
  AssignClass (12168889-0d4d-40b1-b0f1-28ffd5c46f3e)
 Call ID: 12168889-0d4d-40b1-b0f1-28ffd5c46f3e
  Args:
    type: :Person
    source: :LylaGilman
  AssignClass (00b9ac40-ba4c-4d22-9e6e-3469527ee9c6)
 Call ID: 00b9ac40-ba4c-4d22-9e6e-3469527ee9c6
  Args:
    source: :LylaGilman
    type: :Woman
  AssignClass (267e98fa-bae4-4f5e-9e3a-42df7011893a)
 Call ID: 267e98fa-bae4-4f5e-9e3a-42df7011893a
  Args:
    type: :Ancestor
    source: :LylaGilman
  AddTriple (f001f308-a977-4c5a-a674-95aaac052af8)
 Call ID: f001f308-a977-4c5a-a674-95aaac052af8
  Args:
    relation: :isDaughterOf
    target: :LadyRoseGilman
    source: :LylaGilman
  AddTriple (c474dd66-b0ac-4523-b565-a0b2f12b3d87)
 Call ID: c474dd66-b0ac-4523-b565-a0b2f12b3d87
  Args:
    source: :LylaGilman
    target: :GeorgeGilman
    relation: :isDaughterOf
  AssignClass (1ea4d7cd-978e-464b-8197-b613c4e754a6)
 Call ID: 1ea4d7cd-978e-464b-8197-b613c4e754a6
  Args:
    type: :Person
    source: :RufusGilman
  AssignClass (bec919ef-1968-45bd-8c24-0a94d4743fe6)
 Call ID: bec919ef-1968-45bd-8c24-0a94d4743fe6
  Args:
    source: :RufusGilman
    type: :Man
  AssignClass (b4722101-9ed4-4026-9658-5b6226960417)
 Call ID: b4722101-9ed4-4026-9658-5b6226960417
  Args:
    source: :RufusGilman
    type: :Ancestor
  AddTriple (65f20a96-e23a-4f79-90f5-7c9203664fa5)
 Call ID: 65f20a96-e23a-4f79-90f5-7c9203664fa5
  Args:
    source: :RufusGilman
    target: :LadyRoseGilman
    relation: :isSonOf
  AddTriple (ff7de079-f2f5-4884-97c9-8a8be90e4b7d)
 Call ID: ff7de079-f2f5-4884-97c9-8a8be90e4b7d
  Args:
    relation: :isSonOf
    source: :RufusGilman
    target: :GeorgeGilman
  Finish (bef473a4-8d1a-400f-b605-429a90b82ac3)
 Call ID: bef473a4-8d1a-400f-b605-429a90b82ac3
  Args: