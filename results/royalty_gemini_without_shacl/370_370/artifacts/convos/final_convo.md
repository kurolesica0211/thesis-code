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
Prince George William of Hanover and Cumberland (Georg Wilhelm Ernst August Friedrich Axel Prinz von Hannover; 25 March 1915 – 8 January 2006) was the second-eldest son of Ernest Augustus, Duke of Brunswick, and his wife Princess Victoria Louise of Prussia, the only daughter of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
George William's wife was a sister of Prince Philip, Duke of Edinburgh, and his children are thus first cousins of King Charles III.
His sister, Frederica, became Queen of the Hellenes as the consort of King Paul of Greece.
He held the title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
Life

George William was christened on 10 May 1915 in Brunswick.
The prince's godparents included Maria Christina of Austria, Prince Axel of Denmark, and Princess Olga of Hanover and Cumberland who held the infant prince over the baptismal font.
From 1930 through 1934, Prince George William attended the elite boarding school Schule Schloss Salem in Überlingen on Lake Constance.
Schule Schloss Salem was co-founded by the prince's uncle, the last Chancellor of the German Empire, Prince Maximilian of Baden, and educator Kurt Hahn in 1920.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
Together with his wife, as well as his three brothers, he took part in the ship tours organized by his sister Queen Frederica and her husband King Paul of Greece in 1954 and 1956, which became known as the “Cruises of the Kings” and were attended by over 100 royals from all over Europe.
For many years Prince George William was a member of the International Olympic Committee (IOC) and of the Deutscher Olympischer Sportbund (DOSB), the German NOC.
Prince George William of Hanover lived in Schliersee, near Munich, and died in Munich in 2006 aged 90.
His wife, Sophie, sister of Prince Philip of Greece and Denmark, later Duke of Edinburgh, consort of Queen Elizabeth II of the United Kingdom, died in 2001.
Marriage

On 23 April 1946 in Salem, Baden-Württemberg, Germany, Prince George William married his third cousin Princess Sophie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the widow of Prince Christoph of Hesse.
After consultations with the Foreign Office, Home Office and King George VI's private secretary, Sir Alan Lascelles, a ciphered telegram dated 18 April 1946 and crafted by Sir Albert Napier, permanent secretary to the Lord Chancellor, was transmitted from the British Foreign Office to the Foreign Adviser to the British Commander in Chief at Berlin:


"The Duke of Brunswick has formally applied to The King by letter of March 22nd for the consent of His Majesty under the Act 12 Geo.
11 to the marriage of his son Prince George William with Princess Sophia Dowager Princess of Hesse.
Please convey to the Duke an informal intimation that in view of the fact that a state of war still exists between Great Britain and Germany, His Majesty is advised that the case is not one in which it is practicable for His consent to be given in the manner contemplated by the Act.
"

They had three children: Welf (1947–1981), Georg (born 1949) and Friederike (born 1954).
Ancestry

George William was a descendant of Victoria of the United Kingdom and Albert, Prince Consort through their eldest daughter Victoria, Princess Royal, the wife of Frederick III, German Emperor.
He was born a Prince of the United Kingdom of Great Britain and Ireland.



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
  AssignClass (2aa1a3e1-195e-4859-9487-10b6d45aba1f)
 Call ID: 2aa1a3e1-195e-4859-9487-10b6d45aba1f
  Args:
    source: Prince_George_William_of_Hanover_and_Cumberland
    type: :Man
  AssignClass (677321c8-4c8b-474c-8f75-96e431b8cdb2)
 Call ID: 677321c8-4c8b-474c-8f75-96e431b8cdb2
  Args:
    type: :Person
    source: Prince_George_William_of_Hanover_and_Cumberland
  AddLiteral (227a23e5-366d-448e-8d15-197af773f8db)
 Call ID: 227a23e5-366d-448e-8d15-197af773f8db
  Args:
    literal_type: xsd:integer
    source: Prince_George_William_of_Hanover_and_Cumberland
    literal_value: 1915
    relation: :hasBirthYear
  AddLiteral (431ec4f0-7816-413b-bf5a-ea6a69122a73)
 Call ID: 431ec4f0-7816-413b-bf5a-ea6a69122a73
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2006
    source: Prince_George_William_of_Hanover_and_Cumberland
  AssignClass (afdd1f32-9011-4f4b-8e51-1e1ba0a06d7b)
 Call ID: afdd1f32-9011-4f4b-8e51-1e1ba0a06d7b
  Args:
    type: :Man
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (2137a303-08f8-44fe-82ac-cb1c9d7db21f)
 Call ID: 2137a303-08f8-44fe-82ac-cb1c9d7db21f
  Args:
    source: Ernest_Augustus_Duke_of_Brunswick
    type: :Person
  AssignClass (61b45034-4502-4e44-a2a9-4f6f9b0f3042)
 Call ID: 61b45034-4502-4e44-a2a9-4f6f9b0f3042
  Args:
    type: :Woman
    source: Princess_Victoria_Louise_of_Prussia
  AssignClass (54bcc608-8232-4b3d-8b8c-15f693ae610c)
 Call ID: 54bcc608-8232-4b3d-8b8c-15f693ae610c
  Args:
    type: :Person
    source: Princess_Victoria_Louise_of_Prussia
  AddTriple (08eda8c2-3294-4735-a433-ea8e3ce641d3)
 Call ID: 08eda8c2-3294-4735-a433-ea8e3ce641d3
  Args:
    source: Prince_George_William_of_Hanover_and_Cumberland
    relation: :hasFather
    target: Ernest_Augustus_Duke_of_Brunswick
  AddTriple (49fbbd33-a5b8-4590-8be4-636c0fe9320b)
 Call ID: 49fbbd33-a5b8-4590-8be4-636c0fe9320b
  Args:
    relation: :hasMother
    source: Prince_George_William_of_Hanover_and_Cumberland
    target: Princess_Victoria_Louise_of_Prussia
  AssignClass (e3496950-1f1d-4398-bf3b-93878c65bd9b)
 Call ID: e3496950-1f1d-4398-bf3b-93878c65bd9b
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (5c7066e6-3272-4dcf-8cf3-7f34c764c71e)
 Call ID: 5c7066e6-3272-4dcf-8cf3-7f34c764c71e
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (6238a0d6-03b2-4cdc-aada-460142196697)
 Call ID: 6238a0d6-03b2-4cdc-aada-460142196697
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (dbb8a775-7ca5-4eaa-8a5a-6cff7b3db438)
 Call ID: dbb8a775-7ca5-4eaa-8a5a-6cff7b3db438
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (c75ade5a-cf8a-45d3-93f4-3fd96c77f2bc)
 Call ID: c75ade5a-cf8a-45d3-93f4-3fd96c77f2bc
  Args:
    target: Wilhelm_II_German_Emperor
    source: Princess_Victoria_Louise_of_Prussia
    relation: :hasFather
  AddTriple (0dca3b94-3227-4c9b-b8d2-a8c8e586cd77)
 Call ID: 0dca3b94-3227-4c9b-b8d2-a8c8e586cd77
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Princess_Victoria_Louise_of_Prussia
    relation: :hasMother
  AssignClass (386f8044-d1dd-4088-9286-789e078a6275)
 Call ID: 386f8044-d1dd-4088-9286-789e078a6275
  Args:
    type: :Woman
    source: Sophie_of_Greece_and_Denmark
  AssignClass (c6ea3fbd-4e89-47b5-adf9-fc133389e079)
 Call ID: c6ea3fbd-4e89-47b5-adf9-fc133389e079
  Args:
    type: :Person
    source: Sophie_of_Greece_and_Denmark
  AddTriple (17db0fed-7c2a-4c8e-85ea-2ce9777001ce)
 Call ID: 17db0fed-7c2a-4c8e-85ea-2ce9777001ce
  Args:
    target: Sophie_of_Greece_and_Denmark
    source: Prince_George_William_of_Hanover_and_Cumberland
    relation: :hasRelation
  AddLiteral (a5a9d4fd-5067-499c-871a-efb10f8859f7)
 Call ID: a5a9d4fd-5067-499c-871a-efb10f8859f7
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_George_William_of_Hanover_and_Cumberland
    literal_value: 1946
  AddLiteral (08aa7897-bd00-4758-b815-f6bcb188d7df)
 Call ID: 08aa7897-bd00-4758-b815-f6bcb188d7df
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Sophie_of_Greece_and_Denmark
    literal_value: 2001
  AssignClass (6176c6b1-7029-4bda-aeb2-d4e71c84a001)
 Call ID: 6176c6b1-7029-4bda-aeb2-d4e71c84a001
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (05cba3bc-9f82-434b-9f44-b3b20883b452)
 Call ID: 05cba3bc-9f82-434b-9f44-b3b20883b452
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (cabb1ba3-6d5d-4e93-8df4-6d666a09de25)
 Call ID: cabb1ba3-6d5d-4e93-8df4-6d666a09de25
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    relation: :hasSister
    target: Sophie_of_Greece_and_Denmark
  AssignClass (ca5e851c-19b6-409f-8634-6ebeda295661)
 Call ID: ca5e851c-19b6-409f-8634-6ebeda295661
  Args:
    type: :Woman
    source: Frederica_Queen_of_the_Hellenes
  AssignClass (469cec2b-7512-4d9e-9abb-17eb2f9c12b1)
 Call ID: 469cec2b-7512-4d9e-9abb-17eb2f9c12b1
  Args:
    type: :Person
    source: Frederica_Queen_of_the_Hellenes
  AddTriple (b4c4f2ed-46ff-428f-844f-53964b3896fe)
 Call ID: b4c4f2ed-46ff-428f-844f-53964b3896fe
  Args:
    relation: :hasSister
    source: Prince_George_William_of_Hanover_and_Cumberland
    target: Frederica_Queen_of_the_Hellenes
  AssignClass (82010fc4-d16c-4578-b17b-c1d7aee5d7eb)
 Call ID: 82010fc4-d16c-4578-b17b-c1d7aee5d7eb
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (2c3e5574-055d-4c27-a711-8dc638a12ff0)
 Call ID: 2c3e5574-055d-4c27-a711-8dc638a12ff0
  Args:
    type: :Person
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (3aa4512f-48fe-46b0-a535-d0c19d925af2)
 Call ID: 3aa4512f-48fe-46b0-a535-d0c19d925af2
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (56892189-993c-4d2b-ac85-cb7f792597e6)
 Call ID: 56892189-993c-4d2b-ac85-cb7f792597e6
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (f03d5b55-ee42-4d97-825d-a6e36660a75d)
 Call ID: f03d5b55-ee42-4d97-825d-a6e36660a75d
  Args:
    source: Sophie_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (8edfefed-c5aa-4cfb-a3cf-966f481c781a)
 Call ID: 8edfefed-c5aa-4cfb-a3cf-966f481c781a
  Args:
    relation: :hasMother
    source: Sophie_of_Greece_and_Denmark
    target: Princess_Alice_of_Battenberg
  AssignClass (9fc0d0c0-f192-422a-a897-4a8d18aa9dd6)
 Call ID: 9fc0d0c0-f192-422a-a897-4a8d18aa9dd6
  Args:
    source: Welf
    type: :Man
  AssignClass (3225292e-eec0-4e0c-bec5-5ecb81696515)
 Call ID: 3225292e-eec0-4e0c-bec5-5ecb81696515
  Args:
    type: :Person
    source: Welf
  AssignClass (dd1b9fb4-12bb-470a-a592-36bd03bd5d0c)
 Call ID: dd1b9fb4-12bb-470a-a592-36bd03bd5d0c
  Args:
    source: Georg
    type: :Man
  AssignClass (08d3bb4a-3eee-4d94-97e2-6156a46d1fea)
 Call ID: 08d3bb4a-3eee-4d94-97e2-6156a46d1fea
  Args:
    type: :Person
    source: Georg
  AssignClass (06e768ce-6853-4f3d-9118-53cbc3f3a753)
 Call ID: 06e768ce-6853-4f3d-9118-53cbc3f3a753
  Args:
    source: Friederike
    type: :Woman
  AssignClass (53282d2a-f16f-4c54-beda-6b8544db01d0)
 Call ID: 53282d2a-f16f-4c54-beda-6b8544db01d0
  Args:
    source: Friederike
    type: :Person
  AddTriple (2af74705-a1c3-461d-8c62-4edaea27821a)
 Call ID: 2af74705-a1c3-461d-8c62-4edaea27821a
  Args:
    target: Welf
    relation: :hasSon
    source: Prince_George_William_of_Hanover_and_Cumberland
  AddTriple (2f66f265-4918-4386-a109-22f8fd584bf5)
 Call ID: 2f66f265-4918-4386-a109-22f8fd584bf5
  Args:
    target: Georg
    source: Prince_George_William_of_Hanover_and_Cumberland
    relation: :hasSon
  AddTriple (ddae0a01-3969-4a8a-b2c5-bf326e7251d6)
 Call ID: ddae0a01-3969-4a8a-b2c5-bf326e7251d6
  Args:
    relation: :hasDaughter
    source: Prince_George_William_of_Hanover_and_Cumberland
    target: Friederike
  AddTriple (75e128d8-f102-443c-9ea9-c0d99685712c)
 Call ID: 75e128d8-f102-443c-9ea9-c0d99685712c
  Args:
    target: Sophie_of_Greece_and_Denmark
    relation: :hasMother
    source: Welf
  AddTriple (fa84e392-41c8-47d6-b9e3-d76b82b268d2)
 Call ID: fa84e392-41c8-47d6-b9e3-d76b82b268d2
  Args:
    target: Sophie_of_Greece_and_Denmark
    source: Georg
    relation: :hasMother
  AddTriple (3815f8f6-9565-4f1b-a45e-8f10a7a490ae)
 Call ID: 3815f8f6-9565-4f1b-a45e-8f10a7a490ae
  Args:
    target: Sophie_of_Greece_and_Denmark
    source: Friederike
    relation: :hasMother
  Finish (be6ab6a4-b0e5-4716-9748-7bd3c21c1888)
 Call ID: be6ab6a4-b0e5-4716-9748-7bd3c21c1888
  Args: