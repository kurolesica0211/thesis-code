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
Prince Wilhelm Friedrich Franz Joseph Christian Olaf of Prussia (4 July 1906 – 26 May 1940) was the eldest child of Wilhelm, German Crown Prince, and Duchess Cecilie of Mecklenburg-Schwerin.
At his birth, he was second in line to the German throne and was expected to succeed to the throne after the deaths of his grandfather, Emperor Wilhelm II, and his father, Crown Prince Wilhelm, although both outlived him.
In any case, the German monarchy was abolished in 1918 when he was twelve.
He later enlisted to serve in the Wehrmacht and died in active service during the German invasion of France in 1940.
Early life and childhood

Wilhelm was born on 4 July 1906 at the Hohenzollern family's private summer residence, Marmorpalais, or Marble Palace, near Potsdam, where his parents were residing until their own home, Schloss Cecilienhof, could be completed.
His father was Crown Prince Wilhelm, the eldest son and heir to the German Emperor, Wilhelm II.
His mother was Duchess Cecilie of Mecklenburg-Schwerin.
Emperor Franz Joseph of Austria was one of the Prince's godfathers.
The selection of a nanny for Wilhelm and his younger brother, Louis Ferdinand (born in 1907) caused considerable distress within the family.
On his tenth birthday in 1916, Wilhelm was made a lieutenant in the 1st Guards Regiment, and was given the Order of the Black Eagle by his grandfather.
Two years later, when he was twelve, the German monarchy was abolished.
Wilhelm and his family remained in Germany, though his grandfather, the former Emperor, went into exile in the Netherlands.
The former Crown Prince and his family remained in Potsdam, where Wilhelm and his younger brothers attended the local gymnasium.
After graduating from secondary school, Wilhelm went on to study at the Universities of Königsberg, Munich and Bonn.
In 1926, while a student at the University of Bonn, Wilhelm joined the Borussia Corps, a student organization of which his father, grandfather, and other members of the Prussian royal family were members.
Marriage and children

While a student at Bonn, Wilhelm fell in love with a fellow student, Dorothea von Salviati (10 September 1907 – 7 May 1972).
Wilhelm's grandfather did not approve of the marriage of the heir apparent in line to the German throne to a member of the minor nobility.
Wilhelm told his grandson, "Remember, there is every possible form of horse.
However, Wilhelm was determined to marry Dorothea.
Wilhelm and Dorothea married on 3 June 1933 in Bonn.
In 1940, the ex-Emperor recognized the marriage as dynastic and the girls were accorded the style of Princesses of Prussia (although their father was not restored to his former place in the putative line of succession, his renunciation of his rights remaining valid):


Military services

During the Weimar Republic, Wilhelm inadvertently caused a public scandal by attending Army manoeuvres in the uniform of the old Imperial First Foot Guards without first seeking government approval.
The Oster conspiracy of 1938 sought to restore Wilhelm to the throne.
At the beginning of World War II, Wilhelm was among a number of princes from the former German monarchies who enlisted to serve in the Wehrmacht, the unified armed forces of Germany.
Death and reaction

In May 1940, Wilhelm took part in the invasion of France.
Shortly after Wilhelm's death, a decree known as the Prinzenerlaß, or Prince's Decree, was issued, barring all members of the former German royal houses from service in the Wehrmacht.



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
  AssignClass (5ea235f2-2e0b-4caf-99b6-80adb2b31f91)
 Call ID: 5ea235f2-2e0b-4caf-99b6-80adb2b31f91
  Args:
    type: :Person
    source: Wilhelm_of_Prussia
  AssignClass (7ca5b57f-7ee2-483c-864e-092b3fa7b650)
 Call ID: 7ca5b57f-7ee2-483c-864e-092b3fa7b650
  Args:
    source: Wilhelm_of_Prussia
    type: :Man
  AssignClass (d092c7ce-4a18-48f3-94bc-cf7470be8da0)
 Call ID: d092c7ce-4a18-48f3-94bc-cf7470be8da0
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AssignClass (220e1591-9684-4404-b2c1-0d21a55aa0c0)
 Call ID: 220e1591-9684-4404-b2c1-0d21a55aa0c0
  Args:
    source: Crown_Prince_Wilhelm
    type: :Man
  AssignClass (3371ce38-3d1c-42e9-b38b-23a908f6d232)
 Call ID: 3371ce38-3d1c-42e9-b38b-23a908f6d232
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (03d141e5-9ab4-4d8a-a0aa-9976a565afa8)
 Call ID: 03d141e5-9ab4-4d8a-a0aa-9976a565afa8
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (f5692374-d7c2-4ec4-aaf6-846cd7cbaa0a)
 Call ID: f5692374-d7c2-4ec4-aaf6-846cd7cbaa0a
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (fa2d0357-4640-4ce5-9cda-626552955d74)
 Call ID: fa2d0357-4640-4ce5-9cda-626552955d74
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (9fac07c6-e082-4e44-b020-d0946564ea8e)
 Call ID: 9fac07c6-e082-4e44-b020-d0946564ea8e
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Person
  AssignClass (44fba88d-be60-4993-b731-c24dc9417035)
 Call ID: 44fba88d-be60-4993-b731-c24dc9417035
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Man
  AssignClass (ba6c702b-fc8b-486a-9e7b-8b0d839ec0fe)
 Call ID: ba6c702b-fc8b-486a-9e7b-8b0d839ec0fe
  Args:
    source: Dorothea_von_Salviati
    type: :Person
  AssignClass (da9e6db5-cbea-428e-8353-99adefceb55e)
 Call ID: da9e6db5-cbea-428e-8353-99adefceb55e
  Args:
    type: :Woman
    source: Dorothea_von_Salviati
  AddLiteral (6801a50c-0765-4c3b-bba3-6dee7ead2e32)
 Call ID: 6801a50c-0765-4c3b-bba3-6dee7ead2e32
  Args:
    source: Wilhelm_of_Prussia
    literal_value: 1906
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b069154f-5d91-4636-80a3-b68922079c1f)
 Call ID: b069154f-5d91-4636-80a3-b68922079c1f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1940
    source: Wilhelm_of_Prussia
  AddTriple (f4b7edc1-c96c-4bb4-b956-2e506fe42268)
 Call ID: f4b7edc1-c96c-4bb4-b956-2e506fe42268
  Args:
    source: Wilhelm_of_Prussia
    target: Crown_Prince_Wilhelm
    relation: :hasFather
  AddTriple (3630b01b-d88f-45bd-9eb5-c37254a733f2)
 Call ID: 3630b01b-d88f-45bd-9eb5-c37254a733f2
  Args:
    source: Wilhelm_of_Prussia
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AddTriple (bb833867-1a7b-4293-b039-d108d6d93a4c)
 Call ID: bb833867-1a7b-4293-b039-d108d6d93a4c
  Args:
    source: Crown_Prince_Wilhelm
    target: Wilhelm_II
    relation: :hasFather
  AddTriple (8094cced-64a6-4b7f-8869-41e921de3ea4)
 Call ID: 8094cced-64a6-4b7f-8869-41e921de3ea4
  Args:
    source: Wilhelm_of_Prussia
    relation: :hasBrother
    target: Louis_Ferdinand_of_Prussia
  AddTriple (a5a0338c-f07a-4244-9801-bb93daeae066)
 Call ID: a5a0338c-f07a-4244-9801-bb93daeae066
  Args:
    source: Louis_Ferdinand_of_Prussia
    relation: :hasParent
    target: Crown_Prince_Wilhelm
  AddTriple (6b817351-b9a3-4776-9c03-01f4d56f4999)
 Call ID: 6b817351-b9a3-4776-9c03-01f4d56f4999
  Args:
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasParent
    source: Louis_Ferdinand_of_Prussia
  AddLiteral (d1a9caff-399e-46d5-8aa4-8ed083aedd37)
 Call ID: d1a9caff-399e-46d5-8aa4-8ed083aedd37
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Wilhelm_of_Prussia
    literal_value: 1933
  AddLiteral (cab087e5-0a9b-4710-86ab-109073d43974)
 Call ID: cab087e5-0a9b-4710-86ab-109073d43974
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Dorothea_von_Salviati
    literal_value: 1933
  AddTriple (7c5cb9ca-d098-4d01-a679-ed3f1795e446)
 Call ID: 7c5cb9ca-d098-4d01-a679-ed3f1795e446
  Args:
    relation: :hasRelation
    target: Dorothea_von_Salviati
    source: Wilhelm_of_Prussia
  Finish (4a040847-be4c-4334-89b9-61b0a4057e3a)
 Call ID: 4a040847-be4c-4334-89b9-61b0a4057e3a
  Args: