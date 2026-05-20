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
Princess Nathalie of Sayn-Wittgenstein-Berleburg (Nathalie Xenia Margrethe Benedikte; born 2 May 1975) is a Danish equestrian, an Olympian, and the daughter of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She is the niece of Queen Margrethe II of Denmark and King Constantine II of Greece.
Her first cousin is King Frederik X of Denmark.
Early life

Princess Nathalie was born on 2 May 1975 in Copenhagen, Denmark, the youngest of three children of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She grew up at Schloss Berleburg in Bad Berleburg, Germany.
Nathalie and her sister Alexandra became Danish citizens on 19 May 1998.
Neither she nor her siblings are in line of succession to the Danish throne, as that would have required taking up permanent residence in Denmark when reaching the age of mandatory education.
Equestrian career

In 1994, Princess Nathalie began training at the Swedish stud Flyinge with Kyra Kyrklund, a former world champion in dressage.
Nathalie was selected as a reserve rider for the 2000 Olympic team.
She finished 12th in the individual event and helped Denmark to a 4th-place team finish.
In January 2017, Nathalie was named head coach of the Danish national dressage team.
In autumn 2005, she opened her own stud farm, which is based in Bad Berleburg.
Marriage and children

On 4 January 2010, Princess Nathalie's engagement to German horse breeder Alexander Johannsmann (born 6 December 1977), son of showjumper Heinrich-Wilhelm Johannsmann, was announced.
The couple married civilly 27 May 2010 and religiously the following year, on 18 June 2011 at the Protestant Stadtkirche in Berleburg, Germany.
Princess Nathalie gave birth to a son, Konstantin Gustav Heinrich Richard, on 24 July 2010.
Konstantin's godparents were Crown Princess Mary of Denmark, his aunt Ann-Kathrin Johannsmann, and his uncle Prince Gustav.
On 28 January 2015, she gave birth to her second child, a daughter named Louisa Margareta Benedikte Hanna, in Bad Berleburg, Germany.
On 15 August 2022, the Danish court confirmed that Nathalie and Johannsmann had divorced.



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
  AssignClass (7df28c7e-c4cd-4342-8637-7a5b7d0d69a7)
 Call ID: 7df28c7e-c4cd-4342-8637-7a5b7d0d69a7
  Args:
    type: :Woman
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (798d94ec-f490-4afc-96d5-991c90cbd4e0)
 Call ID: 798d94ec-f490-4afc-96d5-991c90cbd4e0
  Args:
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (52213f82-2230-4c2b-b72e-809d633bc7b9)
 Call ID: 52213f82-2230-4c2b-b72e-809d633bc7b9
  Args:
    type: :Woman
    source: Benedikte_of_Denmark
  AssignClass (d83a3bf7-f86a-4f75-b33a-4fd2f25b8193)
 Call ID: d83a3bf7-f86a-4f75-b33a-4fd2f25b8193
  Args:
    type: :Person
    source: Benedikte_of_Denmark
  AssignClass (bfe50b6b-26d4-4ebc-b444-86286ed411ea)
 Call ID: bfe50b6b-26d4-4ebc-b444-86286ed411ea
  Args:
    type: :Man
    source: Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (34939292-0e4f-4850-b34d-ffa785a50dce)
 Call ID: 34939292-0e4f-4850-b34d-ffa785a50dce
  Args:
    source: Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (e56b1084-2405-4bcc-9ff2-99e1fcd583f4)
 Call ID: e56b1084-2405-4bcc-9ff2-99e1fcd583f4
  Args:
    type: :Man
    source: Alexander_Johannsmann
  AssignClass (887d7f81-6eed-4e6d-a450-2f463b6ce00d)
 Call ID: 887d7f81-6eed-4e6d-a450-2f463b6ce00d
  Args:
    source: Alexander_Johannsmann
    type: :Person
  AssignClass (2135eeb5-60c7-436f-b60c-b80f69599788)
 Call ID: 2135eeb5-60c7-436f-b60c-b80f69599788
  Args:
    source: Konstantin_Gustav_Heinrich_Richard
    type: :Man
  AssignClass (7299c838-5b7a-4b0a-8c46-6dd46b7ce0bf)
 Call ID: 7299c838-5b7a-4b0a-8c46-6dd46b7ce0bf
  Args:
    type: :Person
    source: Konstantin_Gustav_Heinrich_Richard
  AssignClass (cb280c76-ff31-4740-9e1f-754c237c7019)
 Call ID: cb280c76-ff31-4740-9e1f-754c237c7019
  Args:
    type: :Woman
    source: Louisa_Margareta_Benedikte_Hanna
  AssignClass (4cc3f001-5267-4e59-a8dd-c0afcf759b87)
 Call ID: 4cc3f001-5267-4e59-a8dd-c0afcf759b87
  Args:
    source: Louisa_Margareta_Benedikte_Hanna
    type: :Person
  AssignClass (40e3d80c-aee0-4a67-bbd2-e6a5e26b00b6)
 Call ID: 40e3d80c-aee0-4a67-bbd2-e6a5e26b00b6
  Args:
    type: :Man
    source: Heinrich-Wilhelm_Johannsmann
  AssignClass (0b2a68ca-240f-4bc1-b86d-95ec07ff78d8)
 Call ID: 0b2a68ca-240f-4bc1-b86d-95ec07ff78d8
  Args:
    source: Heinrich-Wilhelm_Johannsmann
    type: :Person
  AddTriple (d83d91e0-af8e-4937-b585-e159925b7679)
 Call ID: d83d91e0-af8e-4937-b585-e159925b7679
  Args:
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    target: Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
  AddTriple (15898556-98a5-462d-956f-5de2ed8917f5)
 Call ID: 15898556-98a5-462d-956f-5de2ed8917f5
  Args:
    relation: :hasMother
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    target: Benedikte_of_Denmark
  AddTriple (3e9804a2-35dc-4bea-9f15-df15dd4d3c11)
 Call ID: 3e9804a2-35dc-4bea-9f15-df15dd4d3c11
  Args:
    source: Alexander_Johannsmann
    target: Heinrich-Wilhelm_Johannsmann
    relation: :hasFather
  AddTriple (b29945ef-8ae4-47ec-9847-469b29475fb7)
 Call ID: b29945ef-8ae4-47ec-9847-469b29475fb7
  Args:
    target: Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: Konstantin_Gustav_Heinrich_Richard
    relation: :hasMother
  AddTriple (8219f232-c287-4351-b481-9714e266e164)
 Call ID: 8219f232-c287-4351-b481-9714e266e164
  Args:
    target: Alexander_Johannsmann
    source: Konstantin_Gustav_Heinrich_Richard
    relation: :hasFather
  AddTriple (bf0b8d43-e75f-45c7-b47c-cae6074ce36c)
 Call ID: bf0b8d43-e75f-45c7-b47c-cae6074ce36c
  Args:
    target: Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: Louisa_Margareta_Benedikte_Hanna
    relation: :hasMother
  AddTriple (189183cc-b220-4670-9352-8d7aa19cef01)
 Call ID: 189183cc-b220-4670-9352-8d7aa19cef01
  Args:
    source: Louisa_Margareta_Benedikte_Hanna
    target: Alexander_Johannsmann
    relation: :hasFather
  AddLiteral (14a9e0b0-ecb3-4165-aea6-3dda54bcafb6)
 Call ID: 14a9e0b0-ecb3-4165-aea6-3dda54bcafb6
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1975
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (93bd24f3-7d16-4a76-ae7d-8936c9b4dfbf)
 Call ID: 93bd24f3-7d16-4a76-ae7d-8936c9b4dfbf
  Args:
    source: Alexander_Johannsmann
    literal_type: xsd:integer
    literal_value: 1977
    relation: :hasBirthYear
  AddLiteral (651e4bd9-3c5b-4b42-af3e-88af26e1efc1)
 Call ID: 651e4bd9-3c5b-4b42-af3e-88af26e1efc1
  Args:
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    literal_value: 2010
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (4119fae4-2bbb-4866-8d66-93bf0303fda5)
 Call ID: 4119fae4-2bbb-4866-8d66-93bf0303fda5
  Args: