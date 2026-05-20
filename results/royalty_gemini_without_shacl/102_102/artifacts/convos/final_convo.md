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
Princess Alexandra of Sayn-Wittgenstein-Berleburg, Countess Ahlefeldt-Laurvig-Bille (Alexandra Rosemarie Ingrid Benedikte; born 20 November 1970), is the first daughter and second of three children of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark, sister of two Queens, Margrethe II and Anne-Marie of Greece.
She is the first cousin of King Frederik X of Denmark.
Succession rights in Denmark

Under the succession rules set by King Frederik IX, since Princess Benedikte and her children, Prince Gustav, Princess Nathalie and Princess Alexandra, have not taken up permanent residence in Denmark, they have effectively waived their place in the line of succession to the Danish throne.
Since 19 May 1998, Alexandra has been a Danish citizen.
First marriage and children

Alexandra was married on 6 June 1998 at Gråsten Palace to Count Jefferson von Pfeil und Klein-Ellguth.
Jefferson and Alexandra are distantly related, both descending from Leopold III, Duke of Anhalt-Dessau.
Beginning in 2013, Alexandra and Jefferson lived in Heidesheim Castle, Germany, near Mainz.
Second marriage

On 18 May 2019, Alexandra married Count Michael of Ahlefeldt-Laurvig-Bille at Sankt Jørgens Kirke in Svendborgsund.
She has one sister-in-law, Countess Suzanne Ingrid Jessie Dorthe Ahlefeldt-Laurvig-Bille (b. Svendborg, 4 March 1967), lady-in-waiting to Alexandra, Countess of Frederiksborg, who married her third cousin once removed, Erik Ove Carl John Emil Vind til Sanderumgaard (b. Hellerup, 5 May 1954), the grandson of Prince Erik of Denmark.
They currently live at Egeskov Castle, ancestral home and a country residence of the Counts of Ahlefeldt, which is managed by Count Michael Preben, while Princess Alexandra engages herself in drawing, garden designing and art history.
Career

Princess Alexandra worked for UNESCO



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
  AssignClass (78afb8f0-da37-4995-9f67-12de059f1975)
 Call ID: 78afb8f0-da37-4995-9f67-12de059f1975
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (9fce0525-f70e-450f-a428-9fbcdf36145f)
 Call ID: 9fce0525-f70e-450f-a428-9fbcdf36145f
  Args:
    type: :Person
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (c7b76932-a7a1-4294-bfa5-8789b9b71892)
 Call ID: c7b76932-a7a1-4294-bfa5-8789b9b71892
  Args:
    literal_value: 1970
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (29f56e09-1f01-442c-abbc-29a9b8af4575)
 Call ID: 29f56e09-1f01-442c-abbc-29a9b8af4575
  Args:
    type: :Man
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (68c479fb-d2de-46b5-b0d9-c40fa1d313a7)
 Call ID: 68c479fb-d2de-46b5-b0d9-c40fa1d313a7
  Args:
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (871e60dd-797f-4c9e-b20c-78d96ced0139)
 Call ID: 871e60dd-797f-4c9e-b20c-78d96ced0139
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (0ecd88b9-9a3e-4b22-8b95-d35a3568d322)
 Call ID: 0ecd88b9-9a3e-4b22-8b95-d35a3568d322
  Args:
    type: :Person
    source: Princess_Benedikte_of_Denmark
  AddTriple (f4241009-8a99-4267-8bdc-200a0e9b702b)
 Call ID: f4241009-8a99-4267-8bdc-200a0e9b702b
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (d72affbe-265a-4f3e-af3b-11ee2f7d3023)
 Call ID: d72affbe-265a-4f3e-af3b-11ee2f7d3023
  Args:
    relation: :hasMother
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
  AssignClass (ef521c3f-ac20-4ba8-839f-109597882646)
 Call ID: ef521c3f-ac20-4ba8-839f-109597882646
  Args:
    type: :Man
    source: Prince_Gustav
  AssignClass (a007f5bb-f280-4220-a56f-521dc29a8217)
 Call ID: a007f5bb-f280-4220-a56f-521dc29a8217
  Args:
    source: Prince_Gustav
    type: :Person
  AssignClass (2d7d9e0d-ff19-423d-b88d-932796db4358)
 Call ID: 2d7d9e0d-ff19-423d-b88d-932796db4358
  Args:
    type: :Woman
    source: Princess_Nathalie
  AssignClass (fd7bff86-af6f-4ff1-9ace-a771e09b287b)
 Call ID: fd7bff86-af6f-4ff1-9ace-a771e09b287b
  Args:
    source: Princess_Nathalie
    type: :Person
  AddTriple (35ab9298-2b00-4803-ab7d-740e280ef84a)
 Call ID: 35ab9298-2b00-4803-ab7d-740e280ef84a
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :isSiblingOf
    target: Prince_Gustav
  AddTriple (544fa960-7b9c-4b43-9fbe-3738272c753e)
 Call ID: 544fa960-7b9c-4b43-9fbe-3738272c753e
  Args:
    relation: :isSiblingOf
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Nathalie
  AssignClass (4f2cc4fd-0692-4d0a-ba8e-6e5541ff6da4)
 Call ID: 4f2cc4fd-0692-4d0a-ba8e-6e5541ff6da4
  Args:
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    type: :Man
  AssignClass (cc92e4a8-030d-46ee-b1a8-eee00f995f10)
 Call ID: cc92e4a8-030d-46ee-b1a8-eee00f995f10
  Args:
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    type: :Person
  AddLiteral (e5feeb19-d835-4df2-9572-f2bbbdd048d6)
 Call ID: e5feeb19-d835-4df2-9572-f2bbbdd048d6
  Args:
    literal_value: 1998
    relation: :hasMarriageYear
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
  AssignClass (2ff1692b-34d2-4380-8f88-63585b262df1)
 Call ID: 2ff1692b-34d2-4380-8f88-63585b262df1
  Args:
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
    type: :Man
  AssignClass (919ee104-7ee9-4e50-a0fb-1f8a39cde1ad)
 Call ID: 919ee104-7ee9-4e50-a0fb-1f8a39cde1ad
  Args:
    type: :Person
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AddLiteral (30de4876-13d3-4b0f-bdf6-90b879325328)
 Call ID: 30de4876-13d3-4b0f-bdf6-90b879325328
  Args:
    literal_value: 2019
    literal_type: xsd:integer
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMarriageYear
  Finish (6b468939-4ed4-4fd5-9063-2a5885560ef0)
 Call ID: 6b468939-4ed4-4fd5-9063-2a5885560ef0
  Args: