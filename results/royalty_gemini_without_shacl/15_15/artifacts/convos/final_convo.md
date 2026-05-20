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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Ariane of the Netherlands, Princess of Orange-Nassau (Ariane Wilhelmina Máxima Inés, .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}pronounced ; born 10 April 2007) is the third and youngest daughter of King Willem-Alexander and Queen Máxima.
Princess Ariane is a member of the Dutch royal house and currently third in the line of succession to the Dutch throne.
Life

Princess Ariane was born in the HMC Bronovo  in The Hague at 21:56 local time on 10 April 2007 as the third child and youngest daughter of King Willem-Alexander and Queen Máxima of the Netherlands.
Princess Ariane was baptised in the Kloosterkerk, The Hague on 29 October 2007.
Vicar Deodaat van der Boon used water from the Jordan River to baptize the princess, who was wearing the christening gown that Princess Wilhelmina first wore in 1880.
Over 850 guests were invited to attend, including Princess Máxima's parents and Dutch prime minister Jan Peter Balkenende.
Princess Ariane attended the Christelijk Gymnasium Sorghvliet in The Hague.
In May 2023, the Dutch Royal Court announced that the Princess will continue her secondary school studies at the UWC Adriatic in Italy.
Hospitalisation

On 2 May 2007, Princess Ariane was admitted to the Leiden University Medical Center with a suspected lung infection.
On 13 June 2007, Prince Willem-Alexander and Princess Máxima released a thank you note "not only for the congratulations upon Ariane's birth but also for the best wishes they received upon her hospitalisation" and released a third official picture with their newborn daughter.
On 8 October 2009, Princess Ariane was again admitted to a hospital, in which she had to stay for one night, due to a respiratory infection.
Titles, styles and arms

Titles and styles

Ariane's full title and style is "Her Royal Highness Princess Ariane of the Netherlands, Princess of Orange-Nassau.
(Dutch: Hare Koninklijke Hoogheid Ariane Wilhelmina Máxima Inés, Prinses der Nederlanden, Prinses van Oranje-Nassau).
Honours

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (a17d32e8-e976-40a1-9021-9371796e5520)
 Call ID: a17d32e8-e976-40a1-9021-9371796e5520
  Args:
    source: :Ariane
    type: :Person
  AssignClass (43953114-25ab-4fd7-a145-a913e1b6cc32)
 Call ID: 43953114-25ab-4fd7-a145-a913e1b6cc32
  Args:
    type: :Woman
    source: :Ariane
  AssignClass (fa9222fd-d4bf-47d8-8e49-4c960da7aae0)
 Call ID: fa9222fd-d4bf-47d8-8e49-4c960da7aae0
  Args:
    source: :Willem-Alexander
    type: :Person
  AssignClass (3d8e18c4-f097-4217-b5f4-87b71cb1a140)
 Call ID: 3d8e18c4-f097-4217-b5f4-87b71cb1a140
  Args:
    type: :Man
    source: :Willem-Alexander
  AssignClass (42314ecd-187b-46c5-9afc-4ddbcab0d558)
 Call ID: 42314ecd-187b-46c5-9afc-4ddbcab0d558
  Args:
    source: :Willem-Alexander
    type: :Ancestor
  AssignClass (3e5e6d7e-c262-4cb2-8cb9-0843817c4750)
 Call ID: 3e5e6d7e-c262-4cb2-8cb9-0843817c4750
  Args:
    source: :Maxima
    type: :Person
  AssignClass (4ce89316-f1ab-459a-bd8a-cddb05ce3424)
 Call ID: 4ce89316-f1ab-459a-bd8a-cddb05ce3424
  Args:
    type: :Woman
    source: :Maxima
  AssignClass (361ae4db-c5c6-4a50-a724-ca0ef2010171)
 Call ID: 361ae4db-c5c6-4a50-a724-ca0ef2010171
  Args:
    type: :Ancestor
    source: :Maxima
  AssignClass (e054ca84-414e-4dd5-8899-f788a6502522)
 Call ID: e054ca84-414e-4dd5-8899-f788a6502522
  Args:
    source: :Beatrix
    type: :Person
  AssignClass (c1f165b9-942b-4602-8c90-9dbd491f37aa)
 Call ID: c1f165b9-942b-4602-8c90-9dbd491f37aa
  Args:
    source: :Beatrix
    type: :Woman
  AssignClass (55ef7593-76ab-4f6d-81a1-3e7e17ae7d4c)
 Call ID: 55ef7593-76ab-4f6d-81a1-3e7e17ae7d4c
  Args:
    type: :Person
    source: :Margriet
  AssignClass (9e6ddfa6-5ed3-489d-82b4-f6da03e20e68)
 Call ID: 9e6ddfa6-5ed3-489d-82b4-f6da03e20e68
  Args:
    type: :Woman
    source: :Margriet
  AssignClass (193a88e6-d000-4c6c-b9b7-197f4881aa6d)
 Call ID: 193a88e6-d000-4c6c-b9b7-197f4881aa6d
  Args:
    type: :Person
    source: :PieterVanVollenhoven
  AssignClass (1253c6fd-015b-4257-a8cd-87d613ffafa4)
 Call ID: 1253c6fd-015b-4257-a8cd-87d613ffafa4
  Args:
    type: :Man
    source: :PieterVanVollenhoven
  AddLiteral (7974f893-f8ff-445e-ba29-8b1e0084a943)
 Call ID: 7974f893-f8ff-445e-ba29-8b1e0084a943
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Ariane
    literal_value: 2007
  AddTriple (ed977ba5-eaf0-4b70-a002-de7615e48558)
 Call ID: ed977ba5-eaf0-4b70-a002-de7615e48558
  Args:
    target: :Willem-Alexander
    relation: :hasFather
    source: :Ariane
  AddTriple (90621057-b44b-4cd6-9b9d-7b2838b40861)
 Call ID: 90621057-b44b-4cd6-9b9d-7b2838b40861
  Args:
    target: :Maxima
    relation: :hasMother
    source: :Ariane
  Finish (82d66d9f-cfc0-47ad-8c71-16621bfe0c80)
 Call ID: 82d66d9f-cfc0-47ad-8c71-16621bfe0c80
  Args: