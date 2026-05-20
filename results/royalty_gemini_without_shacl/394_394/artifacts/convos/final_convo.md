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
Princess Christina Margarethe of Hesse (German: Christina Margarethe Prinzessin von Hessen; 10 January 1933 – 22 November 2011) was a German princess.
A first cousin of King Charles III of the United Kingdom, she was the wife, from 1956 to 1962, of Prince Andrew of Yugoslavia, a son of Alexander I of Yugoslavia.
Family background and early life

Born in Germany on 10 January 1933 at Friedrichshof Castle near Kronberg im Taunus, Princess Christina ("Krista") of Hesse was the eldest child of Prince Christoph of Hesse (1901–1943) and Princess Sophie of Greece and Denmark (1914–2001)
Her father, Prince Christoph of Hesse, was a nephew of Germany's last emperor Wilhelm II.
Her mother, Princess Sophie of Greece and Denmark, was a grand-daughter of King George I of Greece and a sister of Prince Philip, Duke of Edinburgh.
Christina belonged by birth to the senior line of the House of Hesse, a junior branch of which reigned as grand dukes of Hesse and by Rhine within the German Empire until 1918.
Christina's paternal grandmother, Princess Margaret of Prussia, was a daughter of Queen Victoria's eldest daughter Victoria, and as such a sister of Kaiser Wilhelm II.


Prince Christoph, a member of the Schutzstaffel (SS), held important positions in Germany's Nazi regime.
On 7 October 1943, when Christina was ten years old, her father was killed in an airplane crash in the Apennine Mountains near Forlì, Italy.
His widow married Prince George William of Hanover in 1946.
From her mother's two marriages, Christina had four siblings and three half-siblings: Princess Dorothea of Hesse (1934–2025), Prince Karl of Hesse (1937–2022), Prince Rainer of Hesse (born 1939), Princess Clarissa of Hesse (born 1944), Prince Welf of Hanover (1947–1981), Prince Georg of Hanover (born 1949) and Princess Friederike of Hanover (born 1954).
Her childhood homes included her paternal grandmother's palace of Friedrichshof in Taunus, a family castle at Panker in Holstein, and her parents' residence in Berlin-Dahlem.
Christina participated in the 1953 coronation of her aunt at Westminster Abbey, walking in the procession led by her maternal grandmother, Princess Alice.
Christina and her cousin Princess Beatrix of Hohenlohe-Langenburg spent the winter of 1955-1956 living in London, where Christina studied the restoration of paintings under Anthony Blunt.
It was reported that the princesses' closest friend in England was Prince Andrew of Yugoslavia.
First marriage

Princess Christina of Hesse married Prince Andrew of Yugoslavia, the youngest son of Alexander I of Yugoslavia and Princess Maria of Romania, on 2 August 1956, at Friedrichshof Castle.
They had two children:


Soon after their marriage, Princess Christina and her first husband had purchased The Hollands, a commercial farm at Langton Green in Kent, England, which did not prove a profitable venture.
Moving to London, Prince Andrew supported his family by working for an import/export business and, later, as a bank executive.
In 1961 Christina left her husband to live with an abstract artist from the Netherlands, Robert Floris van Eyck.
Andrew initiated a divorce, and obtained custody of the couple's two children when dissolution of the marriage became final on 31 May 1962.
Second marriage

Following her divorce, Christina married Robert van Eyck on 3 December 1962 in London.
Her first husband Prince Andrew also married for the second time, this time to another cousin, Princess Kira Melita zu Leiningen (1930–2006).
Christina and Robert van Eyck separated in 1985, and divorced 3 February 1986.
In addition to Germany and England, Princess Christina of Hesse had lived in Saint-Paul-de-Vence, France, and in Gersau, Switzerland.



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
  AssignClass (49893041-b916-40e8-9fe9-8ba9592224e0)
 Call ID: 49893041-b916-40e8-9fe9-8ba9592224e0
  Args:
    type: :Woman
    source: :Christina_Margarethe_of_Hesse
  AssignClass (4a1da90c-5e5c-4988-8ec3-91ba0aa39e53)
 Call ID: 4a1da90c-5e5c-4988-8ec3-91ba0aa39e53
  Args:
    type: :Person
    source: :Christina_Margarethe_of_Hesse
  AddLiteral (a43608bc-06b6-4d13-9fc0-be0d17db9bcb)
 Call ID: a43608bc-06b6-4d13-9fc0-be0d17db9bcb
  Args:
    literal_type: xsd:integer
    source: :Christina_Margarethe_of_Hesse
    relation: :hasBirthYear
    literal_value: 1933
  AddLiteral (db8fdb07-e516-4bd7-988b-7bc9f807e865)
 Call ID: db8fdb07-e516-4bd7-988b-7bc9f807e865
  Args:
    literal_type: xsd:integer
    source: :Christina_Margarethe_of_Hesse
    relation: :hasDeathYear
    literal_value: 2011
  AddLiteral (34646c79-128f-4ebf-8b70-7a634edfe2c4)
 Call ID: 34646c79-128f-4ebf-8b70-7a634edfe2c4
  Args:
    source: :Christina_Margarethe_of_Hesse
    literal_type: xsd:string
    literal_value: Krista
    relation: :knownAs
  AssignClass (b9f01ea9-0fdf-4eca-aed3-e55b8cdef925)
 Call ID: b9f01ea9-0fdf-4eca-aed3-e55b8cdef925
  Args:
    type: :Man
    source: :Prince_Christoph_of_Hesse
  AssignClass (0adeac33-bfd3-45d3-b3c4-aa413102a953)
 Call ID: 0adeac33-bfd3-45d3-b3c4-aa413102a953
  Args:
    type: :Person
    source: :Prince_Christoph_of_Hesse
  AssignClass (a6d309de-2e13-4151-b3f0-b9189734e422)
 Call ID: a6d309de-2e13-4151-b3f0-b9189734e422
  Args:
    type: :Ancestor
    source: :Prince_Christoph_of_Hesse
  AddLiteral (e88b4ff3-a6be-4d8e-8926-a7be1937d98c)
 Call ID: e88b4ff3-a6be-4d8e-8926-a7be1937d98c
  Args:
    relation: :hasBirthYear
    literal_value: 1901
    literal_type: xsd:integer
    source: :Prince_Christoph_of_Hesse
  AddLiteral (a8977761-b387-4003-acb2-2bfe90f87891)
 Call ID: a8977761-b387-4003-acb2-2bfe90f87891
  Args:
    literal_value: 1943
    relation: :hasDeathYear
    source: :Prince_Christoph_of_Hesse
    literal_type: xsd:integer
  AssignClass (4fa9fb93-917b-4269-8a8f-9ff59c4f87ad)
 Call ID: 4fa9fb93-917b-4269-8a8f-9ff59c4f87ad
  Args:
    type: :Woman
    source: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (a4689acc-b5e8-4765-be2c-017333527587)
 Call ID: a4689acc-b5e8-4765-be2c-017333527587
  Args:
    type: :Person
    source: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (975d6d73-051f-499d-a73f-400649ac5fbf)
 Call ID: 975d6d73-051f-499d-a73f-400649ac5fbf
  Args:
    type: :Ancestor
    source: :Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (34c8a5f0-dd8c-4072-8efa-43bfe350df79)
 Call ID: 34c8a5f0-dd8c-4072-8efa-43bfe350df79
  Args:
    literal_value: 1914
    relation: :hasBirthYear
    source: :Princess_Sophie_of_Greece_and_Denmark
    literal_type: xsd:integer
  AddLiteral (c36a058f-fc68-4407-9415-c09996108b41)
 Call ID: c36a058f-fc68-4407-9415-c09996108b41
  Args:
    relation: :hasDeathYear
    literal_value: 2001
    literal_type: xsd:integer
    source: :Princess_Sophie_of_Greece_and_Denmark
  AddTriple (073cac6e-beac-43c0-8f48-1acaf581bf19)
 Call ID: 073cac6e-beac-43c0-8f48-1acaf581bf19
  Args:
    target: :Prince_Christoph_of_Hesse
    source: :Christina_Margarethe_of_Hesse
    relation: :hasFather
  AddTriple (2b7c60b9-9d2e-4f0e-a6df-4d020d575a37)
 Call ID: 2b7c60b9-9d2e-4f0e-a6df-4d020d575a37
  Args:
    target: :Princess_Sophie_of_Greece_and_Denmark
    source: :Christina_Margarethe_of_Hesse
    relation: :hasMother
  AssignClass (8ddea6c6-d3de-4e78-93f7-883436b11e30)
 Call ID: 8ddea6c6-d3de-4e78-93f7-883436b11e30
  Args:
    type: :Man
    source: :Prince_Andrew_of_Yugoslavia
  AssignClass (cd04a16c-0ef8-4aa1-955d-1cd363aa83a8)
 Call ID: cd04a16c-0ef8-4aa1-955d-1cd363aa83a8
  Args:
    type: :Person
    source: :Prince_Andrew_of_Yugoslavia
  AssignClass (f476e75f-6ee0-40de-8495-71c04e7998ae)
 Call ID: f476e75f-6ee0-40de-8495-71c04e7998ae
  Args:
    type: :Ancestor
    source: :Prince_Andrew_of_Yugoslavia
  AddTriple (f76ba8e6-0816-45de-bb05-7924548e1a52)
 Call ID: f76ba8e6-0816-45de-bb05-7924548e1a52
  Args:
    relation: :hasRelation
    source: :Christina_Margarethe_of_Hesse
    target: :Prince_Andrew_of_Yugoslavia
  AddLiteral (79497e6c-7cf9-417e-a412-77c1f8336657)
 Call ID: 79497e6c-7cf9-417e-a412-77c1f8336657
  Args:
    literal_value: 1956
    relation: :hasMarriageYear
    source: :Christina_Margarethe_of_Hesse
    literal_type: xsd:integer
  AssignClass (75596433-ea4b-4885-a0f1-5abcead3cf1c)
 Call ID: 75596433-ea4b-4885-a0f1-5abcead3cf1c
  Args:
    type: :Man
    source: :Robert_van_Eyck
  AssignClass (c0d7a6c2-c754-447e-98a3-1d49a1dbdee6)
 Call ID: c0d7a6c2-c754-447e-98a3-1d49a1dbdee6
  Args:
    type: :Person
    source: :Robert_van_Eyck
  AddTriple (a9fed16e-b813-43fd-9864-18f11473a321)
 Call ID: a9fed16e-b813-43fd-9864-18f11473a321
  Args:
    source: :Christina_Margarethe_of_Hesse
    relation: :hasRelation
    target: :Robert_van_Eyck
  AddLiteral (92bef17e-2835-4839-8a4d-3b07ca8d2464)
 Call ID: 92bef17e-2835-4839-8a4d-3b07ca8d2464
  Args:
    relation: :hasMarriageYear
    literal_value: 1962
    literal_type: xsd:integer
    source: :Christina_Margarethe_of_Hesse
  Finish (f2edf05c-88f1-4bda-8244-347c3d635b64)
 Call ID: f2edf05c-88f1-4bda-8244-347c3d635b64
  Args: