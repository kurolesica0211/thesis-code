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
Leopold IV, Prince of Lippe (Leopold Julius Bernhard Adalbert Otto Karl Gustav; 30 May 1871 – 30 December 1949) was the final sovereign of the Principality of Lippe in northwestern Germany from 1905 until his abdication in 1918.
He was the first and only ruler of Lippe of the Lippe-Biesterfeld branch.
Early life

He was born as Count Leopold of Lippe-Biesterfeld in Oberkassel, the son of Ernest, Count of Lippe-Biesterfeld and Countess Karoline of Wartensleben.
Leopold belonged to the Lippe-Biesterfeld line of the House of Lippe which was the most senior line of the princely house after the reigning Lippe-Detmold line.
Ruler of Lippe

Since 1895, the Principality of Lippe had been ruled by a regent due to the incapacity of Prince Alexander.
Leopold's father had acted as regent since 1897, and following his death on 26 September 1904, Leopold assumed the regency.
This was not recognized by the German Emperor Wilhelm II, who initially refused to legally recognize Leopold as regent as there was an issue over whether Leopold and his siblings were of legitimate rank, and as such eligible for the succession.
As a result, the Diet of Lippe appointed a high commission to consider the matter.
The regency issue was still ongoing when Prince Alexander died on 13 January 1905.
Leopold was confirmed as Prince of Lippe and Alexander's successor on 25 October 1905, following a court ruling.
On 3 June 1911, while out motoring, Leopold and his brother Prince Julius were attacked by a gang of Italian laborers who hurled a shower of missiles at the princes.
Though Leopold escaped unhurt, his brother received a head wound.
During World War I, Leopold upgraded the titles of the various lines of the House of Lippe.
One of the members to benefit from the granting of titles was Leopold's nephew Count Bernhard of Biesterfeld (son of Leopold's brother Bernhard), who would go on to become the Prince Consort of Queen Juliana of the Netherlands.
On 24 February 1916, Bernhard and his brother were upgraded to the title Prince of Lippe-Biesterfeld with the style Serene Highness.
The Counts of Lippe-Weissenfeld also benefited with creations of the title Prince of Lippe-Weissenfeld, with the style Serene Highness, taking place on 24 February 1916 for Count Clemens and his descendants, and again on 9 November 1918 for the other members of this line.
Just three days after upgrading the titles of members of the Lippe-Weissenfeld line, and following the German Empire's defeat in World War I and the subsequent revolution, Leopold was forced to renounce the throne on 12 November 1918.
Following the end of his rule, the Principality of Lippe was transformed into a Free state in the new Weimar Republic.
His eldest son the Hereditary Prince Ernst is reported to have been the first German prince to join the party when he signed up in May 1928.
In addition to being pro Nazi, both Hereditary Prince Ernst and Prince Chlodwig had contracted unequal marriages.
So in 1947 when Leopold wrote his will, Armin, his youngest son and only child with his second wife, would succeed him as head of the House of Lippe and also become administrator of the princely family's properties such as Schloss Detmold.
Thus when Leopold died in Detmold his three eldest sons were all disinherited and his youngest son Armin became head of the princely house.
Marriages and children

Leopold was married to Princess Bertha of Hesse-Philippsthal-Barchfeld (1874–1919) on 16 August 1901 in Rotenburg.



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
  AssignClass (b156beff-e8b1-4630-9256-843d8ffeddf7)
 Call ID: b156beff-e8b1-4630-9256-843d8ffeddf7
  Args:
    source: LeopoldIV
    type: :Man
  AssignClass (198e9b35-c4a3-4abd-81b1-de4757bb8cdf)
 Call ID: 198e9b35-c4a3-4abd-81b1-de4757bb8cdf
  Args:
    source: LeopoldIV
    type: :Person
  AssignClass (d43ad592-aef4-44f8-a28a-c669b77f07e1)
 Call ID: d43ad592-aef4-44f8-a28a-c669b77f07e1
  Args:
    type: :Man
    source: Ernest
  AssignClass (e54b7b20-6708-4ca8-b2ce-a8f4f30547f7)
 Call ID: e54b7b20-6708-4ca8-b2ce-a8f4f30547f7
  Args:
    type: :Person
    source: Ernest
  AssignClass (5ab34092-6aff-40ab-90d8-eeb9ff49ad32)
 Call ID: 5ab34092-6aff-40ab-90d8-eeb9ff49ad32
  Args:
    source: Karoline
    type: :Woman
  AssignClass (5f1cbba7-1025-435b-a7bc-e340938d7dcc)
 Call ID: 5f1cbba7-1025-435b-a7bc-e340938d7dcc
  Args:
    type: :Person
    source: Karoline
  AssignClass (a74fb793-8fab-4d9b-a195-9db6aa3e0de2)
 Call ID: a74fb793-8fab-4d9b-a195-9db6aa3e0de2
  Args:
    source: Alexander
    type: :Man
  AssignClass (e306bcc9-0265-4f1a-9f68-b187b7c4f124)
 Call ID: e306bcc9-0265-4f1a-9f68-b187b7c4f124
  Args:
    source: Alexander
    type: :Person
  AssignClass (71e34385-6e1e-4315-98d2-2458f8fb02f0)
 Call ID: 71e34385-6e1e-4315-98d2-2458f8fb02f0
  Args:
    type: :Man
    source: Julius
  AssignClass (5d53d44b-0340-4ef0-9377-9394a1dd4fcc)
 Call ID: 5d53d44b-0340-4ef0-9377-9394a1dd4fcc
  Args:
    source: Julius
    type: :Person
  AssignClass (989d9552-9979-4b87-9bf0-1aecd7da122d)
 Call ID: 989d9552-9979-4b87-9bf0-1aecd7da122d
  Args:
    type: :Man
    source: BernhardOfBiesterfeld
  AssignClass (60fd3501-118b-4ca8-ae84-af3cb270b0e5)
 Call ID: 60fd3501-118b-4ca8-ae84-af3cb270b0e5
  Args:
    type: :Person
    source: BernhardOfBiesterfeld
  AssignClass (7e1a690b-91d3-47ea-a1cc-28e3137d6785)
 Call ID: 7e1a690b-91d3-47ea-a1cc-28e3137d6785
  Args:
    type: :Man
    source: BernhardBrotherOfLeopold
  AssignClass (6cc16fc4-ae94-4fb6-8891-6ff69de68914)
 Call ID: 6cc16fc4-ae94-4fb6-8891-6ff69de68914
  Args:
    source: BernhardBrotherOfLeopold
    type: :Person
  AssignClass (3586588e-3cff-4c0b-a27f-e6159c8f119c)
 Call ID: 3586588e-3cff-4c0b-a27f-e6159c8f119c
  Args:
    type: :Man
    source: Ernst
  AssignClass (35ec4588-b290-428e-8762-fa6636583a76)
 Call ID: 35ec4588-b290-428e-8762-fa6636583a76
  Args:
    type: :Person
    source: Ernst
  AssignClass (56a10230-d3fd-4cad-bb45-ec7c1a60f1ac)
 Call ID: 56a10230-d3fd-4cad-bb45-ec7c1a60f1ac
  Args:
    source: Chlodwig
    type: :Man
  AssignClass (34340693-0424-4877-981e-1089a26ab8f4)
 Call ID: 34340693-0424-4877-981e-1089a26ab8f4
  Args:
    source: Chlodwig
    type: :Person
  AssignClass (27a1ab9f-316f-4226-beee-8192ccbb912e)
 Call ID: 27a1ab9f-316f-4226-beee-8192ccbb912e
  Args:
    source: Armin
    type: :Man
  AssignClass (e1e0d2bb-b578-4f9a-8780-608e35ae59cc)
 Call ID: e1e0d2bb-b578-4f9a-8780-608e35ae59cc
  Args:
    type: :Person
    source: Armin
  AssignClass (2d354dfb-bc62-4592-893a-84c104d15e15)
 Call ID: 2d354dfb-bc62-4592-893a-84c104d15e15
  Args:
    source: Bertha
    type: :Woman
  AssignClass (e9a06db1-34d8-4e58-b9a1-581d22b44073)
 Call ID: e9a06db1-34d8-4e58-b9a1-581d22b44073
  Args:
    type: :Person
    source: Bertha
  AddLiteral (73da4ec5-aa07-4442-9840-d3cfaaae8f7f)
 Call ID: 73da4ec5-aa07-4442-9840-d3cfaaae8f7f
  Args:
    literal_type: xsd:integer
    source: LeopoldIV
    literal_value: 1871
    relation: :hasBirthYear
  AddLiteral (a92a9f49-6f69-4651-9689-fa10eacfb822)
 Call ID: a92a9f49-6f69-4651-9689-fa10eacfb822
  Args:
    source: LeopoldIV
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1949
  AddTriple (7a6e3802-19f0-4e3e-8886-fbf76b89206f)
 Call ID: 7a6e3802-19f0-4e3e-8886-fbf76b89206f
  Args:
    source: LeopoldIV
    relation: :hasFather
    target: Ernest
  AddTriple (97cbcc17-3f4e-4e07-a96d-769693a72f61)
 Call ID: 97cbcc17-3f4e-4e07-a96d-769693a72f61
  Args:
    source: LeopoldIV
    relation: :hasMother
    target: Karoline
  AddTriple (4c161bee-18a0-403e-ad53-994b9b74ac58)
 Call ID: 4c161bee-18a0-403e-ad53-994b9b74ac58
  Args:
    source: LeopoldIV
    relation: :hasBrother
    target: Julius
  AddTriple (f89570b6-834e-4215-9ca0-a4d6dc4f595b)
 Call ID: f89570b6-834e-4215-9ca0-a4d6dc4f595b
  Args:
    relation: :hasBrother
    target: BernhardBrotherOfLeopold
    source: LeopoldIV
  AddTriple (9231ce3b-be6a-43c6-9a63-ffab914a232e)
 Call ID: 9231ce3b-be6a-43c6-9a63-ffab914a232e
  Args:
    source: BernhardOfBiesterfeld
    relation: :hasFather
    target: BernhardBrotherOfLeopold
  AddTriple (d6882e57-cda2-42e5-86f6-4d791c0cabca)
 Call ID: d6882e57-cda2-42e5-86f6-4d791c0cabca
  Args:
    relation: :hasFather
    target: LeopoldIV
    source: Ernst
  AddTriple (71e049b0-da8a-43e9-8474-763f20833b73)
 Call ID: 71e049b0-da8a-43e9-8474-763f20833b73
  Args:
    relation: :hasFather
    target: LeopoldIV
    source: Chlodwig
  AddTriple (eed58fd7-6c7e-468c-a71e-0889aec5c1a7)
 Call ID: eed58fd7-6c7e-468c-a71e-0889aec5c1a7
  Args:
    source: Armin
    relation: :hasFather
    target: LeopoldIV
  AddLiteral (c0184d98-44af-4f7e-80ba-44003d553e07)
 Call ID: c0184d98-44af-4f7e-80ba-44003d553e07
  Args:
    literal_type: xsd:integer
    source: LeopoldIV
    literal_value: 1901
    relation: :hasMarriageYear
  AddTriple (3c7c99fa-d011-4d02-8c9e-0b548d5bf6c5)
 Call ID: 3c7c99fa-d011-4d02-8c9e-0b548d5bf6c5
  Args:
    source: LeopoldIV
    relation: :hasRelation
    target: Bertha
  AddLiteral (b352dfce-240c-4f12-ae0e-d1297153acae)
 Call ID: b352dfce-240c-4f12-ae0e-d1297153acae
  Args:
    relation: :hasBirthYear
    literal_value: 1874
    source: Bertha
    literal_type: xsd:integer
  AddLiteral (b1c6621a-5505-4502-be29-17139d48ac96)
 Call ID: b1c6621a-5505-4502-be29-17139d48ac96
  Args:
    literal_type: xsd:integer
    source: Bertha
    literal_value: 1919
    relation: :hasDeathYear
  Finish (cb2d9853-0da6-402b-b37e-4bfaf02eefaa)
 Call ID: cb2d9853-0da6-402b-b37e-4bfaf02eefaa
  Args: