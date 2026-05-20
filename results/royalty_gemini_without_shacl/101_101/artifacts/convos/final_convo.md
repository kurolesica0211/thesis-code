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
Gustav, 7th Prince of Sayn-Wittgenstein-Berleburg (Gustav Frederik Philip Richard; born 12 January 1969), is the eldest child and only son of Princess Benedikte of Denmark and Richard, 6th Prince of Sayn-Wittgenstein-Berleburg.
His first cousin is King Frederik X of Denmark.
Biography

Prince Gustav is the head of the House of Sayn-Wittgenstein-Berleburg, the senior branch of the formerly princely house of Sayn-Wittgenstein.
He resides at Schloss Berleburg-Wittgenstein in the town of Bad Berleburg, in North Rhine-Westphalia, Germany.
He is the son of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark and has two sisters, Princess Alexandra of Sayn-Wittgenstein-Berleburg and Princess Nathalie of Sayn-Wittgenstein-Berleburg.
The principality and princely title of Sayn-Wittgenstein-Berleburg descended, historically, according to semi-Salic primogeniture.
If Gustav were to die without legitimate issue, the family heritage would devolve upon his father's younger brother, Prince Robin zu Sayn-Wittgenstein-Berleburg.
Gustav was formerly engaged to be married to Elvire Pasté de Rochefort (granddaughter of French Ambassador André Rodocanachi and wife Nada Diplarakou, herself sister of Aliki Diplarakou and grand-aunt of Princess Sibilla of Luxembourg); the engagement was announced on 16 August 2000 and the wedding planned for 12 May 2001 in Paris.
For many years, he resided with his partner, Carina Axelsson, although they were unable to marry due to a clause in Gustav's grandfather's will preventing him from inheriting family property if he marries someone not of Protestant, noble and Aryan descent.
However, on 27 April 2022, the Danish court confirmed that Gustav could marry Axelsson on 3 June 2022, civilly and on 4 June 2022, religiously in Bad Berleburg.
The couple's son, Prince Gustav Albrecht, was born on 26 May 2023 in the United States via surrogacy.
On 26 April 2024, the couple welcomed their second child, a girl, Princess Mafalda, also via surrogacy.
He is the godfather of Count Richard von Pfeil und Klein-Ellguth, son of his sister Alexandra; Konstantin Johannsmann, son of his second sister Nathalie; and Prince Vincent of Denmark, son of his first cousin, Frederik X.


Ancestry




References

External links



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
  AssignClass (b57a5899-5d79-441c-b6fc-fe89f7d09d75)
 Call ID: b57a5899-5d79-441c-b6fc-fe89f7d09d75
  Args:
    type: :Man
    source: Gustav
  AssignClass (8f349153-5dac-4de9-ad0b-bf0dbbffa72a)
 Call ID: 8f349153-5dac-4de9-ad0b-bf0dbbffa72a
  Args:
    type: :Woman
    source: Princess Benedikte of Denmark
  AssignClass (8beb8033-a95c-4047-bdff-ef2ff01a7c47)
 Call ID: 8beb8033-a95c-4047-bdff-ef2ff01a7c47
  Args:
    type: :Man
    source: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
  AssignClass (996516f8-f4fa-46c1-a78d-ed8d7620a368)
 Call ID: 996516f8-f4fa-46c1-a78d-ed8d7620a368
  Args:
    type: :Man
    source: Prince Robin zu Sayn-Wittgenstein-Berleburg
  AssignClass (4ea27c28-8bca-4acc-8bd4-40cbb8447a23)
 Call ID: 4ea27c28-8bca-4acc-8bd4-40cbb8447a23
  Args:
    type: :Woman
    source: Princess Alexandra of Sayn-Wittgenstein-Berleburg
  AssignClass (7abdd2f2-e19f-4e99-b55b-b85f5f4d6da4)
 Call ID: 7abdd2f2-e19f-4e99-b55b-b85f5f4d6da4
  Args:
    type: :Woman
    source: Princess Nathalie of Sayn-Wittgenstein-Berleburg
  AssignClass (4458e6c4-0273-436a-abeb-1c89453fd438)
 Call ID: 4458e6c4-0273-436a-abeb-1c89453fd438
  Args:
    type: :Woman
    source: Carina Axelsson
  AssignClass (466214c8-a471-4c45-b033-639a604247c8)
 Call ID: 466214c8-a471-4c45-b033-639a604247c8
  Args:
    type: :Man
    source: Prince Gustav Albrecht
  AssignClass (a1385b56-3a19-42aa-a0f0-7fb074219640)
 Call ID: a1385b56-3a19-42aa-a0f0-7fb074219640
  Args:
    type: :Woman
    source: Princess Mafalda
  AddLiteral (f5fc4df0-24b4-4dbd-9255-585f071ea931)
 Call ID: f5fc4df0-24b4-4dbd-9255-585f071ea931
  Args:
    literal_value: 1969
    source: Gustav
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (11dea722-c460-48a6-af72-7c580332c6ea)
 Call ID: 11dea722-c460-48a6-af72-7c580332c6ea
  Args:
    target: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
    source: Gustav
    relation: :hasFather
  AddTriple (5f5cf74e-11e5-4332-99ab-9a80899b92ec)
 Call ID: 5f5cf74e-11e5-4332-99ab-9a80899b92ec
  Args:
    target: Princess Benedikte of Denmark
    source: Gustav
    relation: :hasMother
  AddTriple (643ef671-8215-49f2-af2a-b0e9f73945fc)
 Call ID: 643ef671-8215-49f2-af2a-b0e9f73945fc
  Args:
    target: Princess Alexandra of Sayn-Wittgenstein-Berleburg
    source: Gustav
    relation: :hasSister
  AddTriple (d7c35ba5-045b-48d5-93ee-1c74a8634269)
 Call ID: d7c35ba5-045b-48d5-93ee-1c74a8634269
  Args:
    target: Princess Nathalie of Sayn-Wittgenstein-Berleburg
    source: Gustav
    relation: :hasSister
  AddTriple (bf326ca9-65d9-417e-afc1-accf213bfc16)
 Call ID: bf326ca9-65d9-417e-afc1-accf213bfc16
  Args:
    source: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
    relation: :hasBrother
    target: Prince Robin zu Sayn-Wittgenstein-Berleburg
  AddTriple (a7042537-8694-4b2d-bc7f-0548244e7b9f)
 Call ID: a7042537-8694-4b2d-bc7f-0548244e7b9f
  Args:
    source: Gustav
    relation: :hasChild
    target: Prince Gustav Albrecht
  AddTriple (d5583d50-a29a-436d-8ecb-77cc644741cf)
 Call ID: d5583d50-a29a-436d-8ecb-77cc644741cf
  Args:
    target: Princess Mafalda
    source: Gustav
    relation: :hasChild
  AddTriple (c21b6dd7-23df-42d7-a604-aa9f673c37af)
 Call ID: c21b6dd7-23df-42d7-a604-aa9f673c37af
  Args:
    source: Carina Axelsson
    relation: :hasChild
    target: Prince Gustav Albrecht
  AddTriple (f9264e6b-5cea-4e2f-90a0-74a3973270e1)
 Call ID: f9264e6b-5cea-4e2f-90a0-74a3973270e1
  Args:
    source: Carina Axelsson
    relation: :hasChild
    target: Princess Mafalda
  Finish (d53570d9-434e-4727-8da4-1e7fe36dbc7d)
 Call ID: d53570d9-434e-4727-8da4-1e7fe36dbc7d
  Args: