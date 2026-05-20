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
Countess Walburga Douglas (née von Habsburg-Lothringen; born 5 October 1958) is a German-born Swedish lawyer and politician, who served as a member of the Riksdag of Sweden for the Moderate Party from 2006 to 2014.
Early life

Born in 1958 in Berg am Starnberger See, West Germany, she is the fifth daughter of Otto von Habsburg, the last crown prince of Austria-Hungary, and his wife Princess Regina of Saxe-Meiningen.
Walburga was banished from the Republic of Austria from birth and well into adult life, along with her siblings, by the Habsburg Law that had been in effect since 1938, having been (re)imposed by the Nazis.
She is a granddaughter of the last Austrian emperor, Charles I, and a member of the House of Habsburg-Lorraine.
Her ancestral titles (abolished in Austria since 1919) are Archduchess Walburga of Austria, Archduchess of Austria, Princess of Hungary and Bohemia, with the style of Her Imperial and Royal Highness (HI&RH).
She does not currently use her ancestral titles actively in her daily life; however, by law she holds the title of Countess Douglas in the Kingdom of Sweden, her current country of residence and citizenship.
On 17 September 2023, Douglas visited Armenia to dedicate the opening of the PanEuropa Armenia branch in Yerevan.
Personal life

On 5 December 1992 in Budapest, Hungary, Walburga married a Swedish nobleman, Count Carl Axel Archibald Douglas (born 27 November 1949 in Stockholm), son of Count Archibald Douglas and Baroness Margareta Lagerfelt.
Her husband's family is a  noble family in Sweden, descended from the Scot Robert Douglas, Count of Skenninge, member of the Scottish Clan Douglas and founder of its Swedish branch.
Her husband is a first cousin of Count Gustaf Douglas and his sisters Rosita Spencer-Churchill, Duchess of Marlborough, and Princess Elisabeth, Duchess in Bavaria, the wife of Prince Max, Duke in Bavaria.
They have a son, Count Mauritz Otto Wenzel Douglas (born 30 March 1994 in Stockholm).



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
  AssignClass (adff2d5e-81c8-434b-a2a6-d0ea741967b6)
 Call ID: adff2d5e-81c8-434b-a2a6-d0ea741967b6
  Args:
    type: :Woman
    source: Walburga_Douglas
  AssignClass (fc9f253a-6aa5-4fe4-b103-c1db8ce8679b)
 Call ID: fc9f253a-6aa5-4fe4-b103-c1db8ce8679b
  Args:
    source: Walburga_Douglas
    type: :Person
  AddLiteral (004b121b-6d40-4863-810c-c3d1a065f975)
 Call ID: 004b121b-6d40-4863-810c-c3d1a065f975
  Args:
    literal_type: xsd:integer
    source: Walburga_Douglas
    literal_value: 1958
    relation: :hasBirthYear
  AssignClass (fe4cbaf2-73b2-4f26-b3a9-f2f4d18690ef)
 Call ID: fe4cbaf2-73b2-4f26-b3a9-f2f4d18690ef
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (bb90abef-0386-453f-9bf1-cfe0fc973c6f)
 Call ID: bb90abef-0386-453f-9bf1-cfe0fc973c6f
  Args:
    source: Otto_von_Habsburg
    type: :Ancestor
  AssignClass (2e1d3a00-9839-4b1f-9138-ede4cbefcb2c)
 Call ID: 2e1d3a00-9839-4b1f-9138-ede4cbefcb2c
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (38e8f2e3-a0ec-440b-9251-d93128f4e662)
 Call ID: 38e8f2e3-a0ec-440b-9251-d93128f4e662
  Args:
    type: :Woman
    source: Regina_of_Saxe-Meiningen
  AssignClass (d810b008-f1d8-4e1c-abb0-364771862ec5)
 Call ID: d810b008-f1d8-4e1c-abb0-364771862ec5
  Args:
    type: :Ancestor
    source: Regina_of_Saxe-Meiningen
  AssignClass (b80330b9-0f0e-49de-84fa-3292e0827fd1)
 Call ID: b80330b9-0f0e-49de-84fa-3292e0827fd1
  Args:
    type: :Person
    source: Regina_of_Saxe-Meiningen
  AddTriple (e9ea4c7f-3ac1-452a-8e44-e383ad05cf69)
 Call ID: e9ea4c7f-3ac1-452a-8e44-e383ad05cf69
  Args:
    source: Walburga_Douglas
    relation: :hasFather
    target: Otto_von_Habsburg
  AddTriple (653a0922-707e-4352-a22e-ac58f5ebf50c)
 Call ID: 653a0922-707e-4352-a22e-ac58f5ebf50c
  Args:
    source: Walburga_Douglas
    relation: :hasMother
    target: Regina_of_Saxe-Meiningen
  AssignClass (f9f28953-f10f-4706-acfe-4aac504ca351)
 Call ID: f9f28953-f10f-4706-acfe-4aac504ca351
  Args:
    type: :Man
    source: Charles_I
  AssignClass (6d49c9d9-6c25-4745-93ae-d437cec0f2fe)
 Call ID: 6d49c9d9-6c25-4745-93ae-d437cec0f2fe
  Args:
    source: Charles_I
    type: :Ancestor
  AssignClass (7b63f360-f1ec-4ed6-a1c1-13c050195721)
 Call ID: 7b63f360-f1ec-4ed6-a1c1-13c050195721
  Args:
    type: :Person
    source: Charles_I
  AddTriple (5cc5c7d5-6bc1-48ee-b3d9-6e9baf174b5f)
 Call ID: 5cc5c7d5-6bc1-48ee-b3d9-6e9baf174b5f
  Args:
    relation: :hasAncestor
    source: Walburga_Douglas
    target: Charles_I
  AssignClass (c2e525c4-0d2b-406a-95e1-f80fc0f9f149)
 Call ID: c2e525c4-0d2b-406a-95e1-f80fc0f9f149
  Args:
    type: :Man
    source: Carl_Axel_Archibald_Douglas
  AssignClass (17034e74-6814-4351-a5d7-34688e142815)
 Call ID: 17034e74-6814-4351-a5d7-34688e142815
  Args:
    source: Carl_Axel_Archibald_Douglas
    type: :Person
  AddLiteral (6db699fb-a282-429a-b9b8-a2cfc384c537)
 Call ID: 6db699fb-a282-429a-b9b8-a2cfc384c537
  Args:
    relation: :hasBirthYear
    source: Carl_Axel_Archibald_Douglas
    literal_value: 1949
    literal_type: xsd:integer
  AddLiteral (2629fb51-d6b1-492a-beba-b72033e12de5)
 Call ID: 2629fb51-d6b1-492a-beba-b72033e12de5
  Args:
    relation: :hasMarriageYear
    source: Walburga_Douglas
    literal_value: 1992
    literal_type: xsd:integer
  AddTriple (8cedd9b5-83dd-4d8b-9af6-a0cb0743f003)
 Call ID: 8cedd9b5-83dd-4d8b-9af6-a0cb0743f003
  Args:
    relation: :hasRelation
    source: Walburga_Douglas
    target: Carl_Axel_Archibald_Douglas
  AssignClass (26ecf477-c47a-44bd-882b-29db53988af8)
 Call ID: 26ecf477-c47a-44bd-882b-29db53988af8
  Args:
    source: Archibald_Douglas
    type: :Man
  AssignClass (092d0e21-db23-45e8-bf05-ffc724c76b0b)
 Call ID: 092d0e21-db23-45e8-bf05-ffc724c76b0b
  Args:
    source: Archibald_Douglas
    type: :Ancestor
  AssignClass (215f6979-e46f-4598-91c6-cf872367f215)
 Call ID: 215f6979-e46f-4598-91c6-cf872367f215
  Args:
    source: Archibald_Douglas
    type: :Person
  AssignClass (9934ecf4-d6d0-4a47-906e-2faf0318d685)
 Call ID: 9934ecf4-d6d0-4a47-906e-2faf0318d685
  Args:
    type: :Woman
    source: Margareta_Lagerfelt
  AssignClass (38cf57f1-d2c3-4830-8e46-5a2576853393)
 Call ID: 38cf57f1-d2c3-4830-8e46-5a2576853393
  Args:
    type: :Ancestor
    source: Margareta_Lagerfelt
  AssignClass (2758e04b-59fd-4e8c-b7c8-3af22489d725)
 Call ID: 2758e04b-59fd-4e8c-b7c8-3af22489d725
  Args:
    type: :Person
    source: Margareta_Lagerfelt
  AddTriple (90180f93-c496-44b6-aaab-669343e1b206)
 Call ID: 90180f93-c496-44b6-aaab-669343e1b206
  Args:
    target: Archibald_Douglas
    relation: :hasFather
    source: Carl_Axel_Archibald_Douglas
  AddTriple (cd463e1f-60de-4c1a-b2b4-9be0dca5bede)
 Call ID: cd463e1f-60de-4c1a-b2b4-9be0dca5bede
  Args:
    relation: :hasMother
    source: Carl_Axel_Archibald_Douglas
    target: Margareta_Lagerfelt
  AssignClass (8ef7d260-4112-45ef-b9cf-629f01524e27)
 Call ID: 8ef7d260-4112-45ef-b9cf-629f01524e27
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    type: :Man
  AssignClass (061d65c5-1faa-461c-b7f2-e9f4f31a3b84)
 Call ID: 061d65c5-1faa-461c-b7f2-e9f4f31a3b84
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    type: :Person
  AddLiteral (46faaa14-b4aa-45cd-98e2-45dcc3026638)
 Call ID: 46faaa14-b4aa-45cd-98e2-45dcc3026638
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Mauritz_Otto_Wenzel_Douglas
    literal_value: 1994
  AddTriple (eaebcee4-74f1-4941-85e5-3502795771ec)
 Call ID: eaebcee4-74f1-4941-85e5-3502795771ec
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    relation: :hasFather
    target: Carl_Axel_Archibald_Douglas
  AddTriple (81f4d6f3-4cd2-4826-ab72-98f59a5c60df)
 Call ID: 81f4d6f3-4cd2-4826-ab72-98f59a5c60df
  Args:
    target: Walburga_Douglas
    relation: :hasMother
    source: Mauritz_Otto_Wenzel_Douglas
  Finish (b794231d-12fa-4358-be20-54b0aed3db0d)
 Call ID: b794231d-12fa-4358-be20-54b0aed3db0d
  Args: