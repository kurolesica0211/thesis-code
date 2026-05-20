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
Duke Adolf Friedrich Albrecht Heinrich of Mecklenburg-Schwerin (German: Adolf Friedrich Albrecht Heinrich, Herzog zu Mecklenburg-Schwerin; 10 October 1873 – 5 August 1969), was a German explorer in Africa, a colonial politician,  and the first president of the National Olympic Committee of West Germany (1949–1951).
Biography

Born in Schwerin, Adolf Friedrich was the third child of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin (1823–1883), and his third wife Princess Marie of Schwarzburg-Rudolstadt.
His younger brother was Prince Hendrik of the Netherlands, prince consort to the Dutch Queen Wilhelmina.
Explorer of Africa

From 1907 to 1908, Adolf Friedrich led a scientific research expedition in the region of the Central African Graben and traversed  Africa from east to west.
Adolf Friedrich and his companions explored the then little-known primeval forest region of the Congo tributaries and the basin of Lake Chad.
From 1912 to 1914, Adolf Friedrich was the last governor of Togoland in German West Africa; he was invited for the official celebration of the independence of Togo in 1960.
Duke candidate for the planned United Baltic Duchy

At the end of the First World War, in the autumn of 1918, the Duke was offered the throne of the United Baltic Duchy, a short-lived client-state proclaimed on Baltic territories under German occupation.
By the autumn of 1918, the Duke was approached by Heinrich von Stryk, a representative of the Baltic German nobility, but final steps towards implementation of their plans were undertaken on 5 November, when representatives of Baltic Germans and some pro-German oriented leaders among Estonian and Latvian politicians from Courland, Livonia and Estonia met in Riga and proclaimed the creation of the United Baltic Duchy.
Since the Duke was in Germany, the temporary regency council (Regentschaftsrat) was established in Riga, headed by baron Adolf Pilar von Pilchau, and consisting of three Baltic Germans, three Estonians and three Latvians.
Since Germany lost the War by 11 November, the Duke never assumed the Baltic throne.
Member of the International Olympic Committee

Adolf Friedrich then served as a member of the International Olympic Committee from 1926 to 1956 and as the first president of the National Olympic Committee of Germany from 1949 to 1951.
Personal life

Adolf Friedrich was married twice.
In Gera on 24 April 1917, he married Princess Viktoria Feodora of Reuss-Schleiz (1889-1918), daughter of Heinrich XXVII, Prince Reuss Younger Line and Princess Elise of Hohenlohe-Langenburg.
He later married the widow of his half-brother Duke John Albert, Princess Elisabeth of Stolberg-Rossla, on 15 October 1924; they were among the guests at 
the 1937 wedding of Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
Princess Elisabeth survived her husband by only a few weeks after his death in Eutin in 1969.
Legacy

Adolf Friedrich is commemorated in the scientific names of a genus of lizards, Adolfus, and of a species of chameleon, Kinyongia adolfifriderici, as well as in the cichlid Haplochromis adolphifrederici, and in the large tree species Aningeria adolfi-friederici.



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
  AssignClass (1e87ac66-0b9e-4cfd-b0a2-adead614d945)
 Call ID: 1e87ac66-0b9e-4cfd-b0a2-adead614d945
  Args:
    type: :Man
    source: Adolf_Friedrich_Mecklenburg_Schwerin
  AssignClass (3b90aff4-60d1-4673-8773-a09a00350599)
 Call ID: 3b90aff4-60d1-4673-8773-a09a00350599
  Args:
    source: Adolf_Friedrich_Mecklenburg_Schwerin
    type: :Person
  AddLiteral (3f365b2b-3f30-4e26-a182-ca984a11bca5)
 Call ID: 3f365b2b-3f30-4e26-a182-ca984a11bca5
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Adolf_Friedrich_Mecklenburg_Schwerin
    literal_value: 1873
  AddLiteral (943e545f-3765-42b3-bd02-ade35a63482d)
 Call ID: 943e545f-3765-42b3-bd02-ade35a63482d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1969
    source: Adolf_Friedrich_Mecklenburg_Schwerin
  AssignClass (71cee6df-89e2-4022-a1f3-17385c8cacc3)
 Call ID: 71cee6df-89e2-4022-a1f3-17385c8cacc3
  Args:
    source: Frederick_Francis_II_Mecklenburg_Schwerin
    type: :Man
  AssignClass (cfde8eb6-7d02-4516-9ecc-48eefff4e43c)
 Call ID: cfde8eb6-7d02-4516-9ecc-48eefff4e43c
  Args:
    source: Frederick_Francis_II_Mecklenburg_Schwerin
    type: :Person
  AssignClass (d0b65df0-4264-4753-9c3f-bf44e396a69b)
 Call ID: d0b65df0-4264-4753-9c3f-bf44e396a69b
  Args:
    type: :Ancestor
    source: Frederick_Francis_II_Mecklenburg_Schwerin
  AddLiteral (37764422-53b6-4573-932f-ff74acd6e3cf)
 Call ID: 37764422-53b6-4573-932f-ff74acd6e3cf
  Args:
    literal_value: 1823
    source: Frederick_Francis_II_Mecklenburg_Schwerin
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (8eb92bbf-bc8f-4ef4-bc14-5390a5277b10)
 Call ID: 8eb92bbf-bc8f-4ef4-bc14-5390a5277b10
  Args:
    literal_value: 1883
    source: Frederick_Francis_II_Mecklenburg_Schwerin
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (2d17fd61-792a-4f4e-8cc8-ba1696aa041c)
 Call ID: 2d17fd61-792a-4f4e-8cc8-ba1696aa041c
  Args:
    type: :Woman
    source: Marie_Schwarzburg_Rudolstadt
  AssignClass (23f66e16-1091-4d44-921a-fba05ba604f3)
 Call ID: 23f66e16-1091-4d44-921a-fba05ba604f3
  Args:
    type: :Person
    source: Marie_Schwarzburg_Rudolstadt
  AssignClass (033cd48f-1f49-469d-8bae-ecd398de39e1)
 Call ID: 033cd48f-1f49-469d-8bae-ecd398de39e1
  Args:
    source: Marie_Schwarzburg_Rudolstadt
    type: :Ancestor
  AddTriple (bfcd5522-1334-486f-9446-892d8238a882)
 Call ID: bfcd5522-1334-486f-9446-892d8238a882
  Args:
    source: Adolf_Friedrich_Mecklenburg_Schwerin
    relation: :hasFather
    target: Frederick_Francis_II_Mecklenburg_Schwerin
  AddTriple (ed4fd373-aa0d-4b09-8f3e-1353e52a4750)
 Call ID: ed4fd373-aa0d-4b09-8f3e-1353e52a4750
  Args:
    target: Marie_Schwarzburg_Rudolstadt
    relation: :hasMother
    source: Adolf_Friedrich_Mecklenburg_Schwerin
  AssignClass (24e8fae6-ef3e-43cb-a289-feb3c7abddaf)
 Call ID: 24e8fae6-ef3e-43cb-a289-feb3c7abddaf
  Args:
    source: Hendrik_Netherlands
    type: :Man
  AssignClass (2446b037-7292-4bb8-a9b8-bf7691429b31)
 Call ID: 2446b037-7292-4bb8-a9b8-bf7691429b31
  Args:
    source: Hendrik_Netherlands
    type: :Person
  AddTriple (22544e5b-c6e2-469d-b036-a7d7bfce182e)
 Call ID: 22544e5b-c6e2-469d-b036-a7d7bfce182e
  Args:
    source: Adolf_Friedrich_Mecklenburg_Schwerin
    relation: :hasBrother
    target: Hendrik_Netherlands
  AssignClass (51f0ea26-b537-4ca5-94d1-0027ec586662)
 Call ID: 51f0ea26-b537-4ca5-94d1-0027ec586662
  Args:
    source: Viktoria_Feodora_Reuss_Schleiz
    type: :Woman
  AssignClass (6bb3f5ca-2948-4c34-a1c0-f0b625225615)
 Call ID: 6bb3f5ca-2948-4c34-a1c0-f0b625225615
  Args:
    source: Viktoria_Feodora_Reuss_Schleiz
    type: :Person
  AddLiteral (cfcaf85a-a1d3-405b-8eb6-292672f13a83)
 Call ID: cfcaf85a-a1d3-405b-8eb6-292672f13a83
  Args:
    literal_value: 1917
    source: Adolf_Friedrich_Mecklenburg_Schwerin
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddLiteral (40072f3e-c162-48b1-bedc-a7af5f6b25df)
 Call ID: 40072f3e-c162-48b1-bedc-a7af5f6b25df
  Args:
    literal_value: 1889
    source: Viktoria_Feodora_Reuss_Schleiz
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0ee71ec4-9f43-4778-b138-27bb71b259c8)
 Call ID: 0ee71ec4-9f43-4778-b138-27bb71b259c8
  Args:
    literal_value: 1918
    source: Viktoria_Feodora_Reuss_Schleiz
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (d8a4e260-9d37-4ef3-b403-c3646d5f8efd)
 Call ID: d8a4e260-9d37-4ef3-b403-c3646d5f8efd
  Args:
    type: :Man
    source: Heinrich_XXVII_Reuss_Younger_Line
  AssignClass (bcaa716a-0188-4bfe-929f-2ca0e735ca87)
 Call ID: bcaa716a-0188-4bfe-929f-2ca0e735ca87
  Args:
    source: Heinrich_XXVII_Reuss_Younger_Line
    type: :Person
  AssignClass (43262a73-c613-423d-ba96-3c04e719d85b)
 Call ID: 43262a73-c613-423d-ba96-3c04e719d85b
  Args:
    type: :Ancestor
    source: Heinrich_XXVII_Reuss_Younger_Line
  AddTriple (c937bdc3-736b-4144-ba69-8b7d0ad0fb40)
 Call ID: c937bdc3-736b-4144-ba69-8b7d0ad0fb40
  Args:
    relation: :hasFather
    target: Heinrich_XXVII_Reuss_Younger_Line
    source: Viktoria_Feodora_Reuss_Schleiz
  AssignClass (93b856d9-68df-4874-956e-7300c8687d5c)
 Call ID: 93b856d9-68df-4874-956e-7300c8687d5c
  Args:
    type: :Woman
    source: Elise_Hohenlohe_Langenburg
  AssignClass (627d14e3-88e3-4902-b0b4-51b1bb3f50a5)
 Call ID: 627d14e3-88e3-4902-b0b4-51b1bb3f50a5
  Args:
    source: Elise_Hohenlohe_Langenburg
    type: :Person
  AssignClass (8f4c1f8f-8cec-45f9-a8ae-1bef37aa94df)
 Call ID: 8f4c1f8f-8cec-45f9-a8ae-1bef37aa94df
  Args:
    type: :Ancestor
    source: Elise_Hohenlohe_Langenburg
  AddTriple (d30ad3cf-5a18-4511-9817-ade9c03db034)
 Call ID: d30ad3cf-5a18-4511-9817-ade9c03db034
  Args:
    target: Elise_Hohenlohe_Langenburg
    relation: :hasMother
    source: Viktoria_Feodora_Reuss_Schleiz
  AssignClass (456a6d26-50e2-4c48-a0f9-fd9b07b2d751)
 Call ID: 456a6d26-50e2-4c48-a0f9-fd9b07b2d751
  Args:
    source: Elisabeth_Stolberg_Rossla
    type: :Woman
  AssignClass (ddc61bf1-3c66-409e-81de-de3fc521259d)
 Call ID: ddc61bf1-3c66-409e-81de-de3fc521259d
  Args:
    source: Elisabeth_Stolberg_Rossla
    type: :Person
  AddLiteral (3b904efd-a061-4231-9bea-d6866a6f7e14)
 Call ID: 3b904efd-a061-4231-9bea-d6866a6f7e14
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1924
    source: Adolf_Friedrich_Mecklenburg_Schwerin
  Finish (e1853f8b-765a-4050-9362-30ef4cefda55)
 Call ID: e1853f8b-765a-4050-9362-30ef4cefda55
  Args: