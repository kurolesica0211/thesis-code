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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Jaime Bernardo of Bourbon-Parma, Count of Bardi (born 13 October 1972) is a Dutch diplomat and the second son and third child of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
He is a member of the House of Bourbon-Parma as well a member of the extended Dutch royal family.
He was the senior advisor on private sector partnerships at the United Nations High Commissioner for Refugees until 2021 and served as the climate envoy of the Netherlands.
Early life

Jaime was born in Nijmegen, Netherlands.
He has a twin sister, Princess Margarita, who was born one minute earlier.
Besides his twin sister, the prince has one elder brother, Carlos, Duke of Parma, and one younger sister, Princess Carolina.
Prince Jaime was born six weeks prematurely and stayed with his sister in an incubator at the hospital.
Jaime was baptised by Bernardus Johannes Cardinal Alfrink, with his grandfather Prince Bernhard of Lippe-Biesterfeld and his grandmother Princess Madeleine of Bourbon-Parma as his godparents.
Together with his mother and his siblings he moved to the Soestdijk Palace (Baarn), then residence of his grandparents, Queen Juliana and Prince Bernhard, where he lived for several years.
He now works for the Ministry of Foreign Affairs of the Netherlands.
His first role was as the first secretary of the Netherlands Embassy in Baghdad, before becoming a political advisor to the peace mission in Pol-e Khomri in the Baghlan Province in the northern part of Afghanistan.
Until the summer of 2007 the prince worked on secondment in the cabinet of the European Commissioner Neelie Kroes.
On 7 February 2014, the Ministry of Foreign Affairs announced that he would be appointed as ambassador of the Kingdom of the Netherlands to the Holy See.
Prince Jaime was, on 15 July 2014, sworn in as ambassador by King Willem-Alexander and he served till August 2018.
In August 2021 he started as the Climate Envoy of the Netherlands and served for over four years.
The prince performs representative tasks for the Ducal House of Bourbon-Parma.
On 9 November 2015, it was announced that the couple were expecting a second child; daughter Gloria Irene was born on (2016-05-09)9 May 2016.
In a 2015 interview, Princess Viktória stated that the gender of her future child did not matter ("fortunately, we can not influence nature in the terms of gender"), after being told that there were no grandsons for the late Duke of Parma (in April 2016, Jaime's elder brother Carlos, Duke of Parma finally had a son, named Carlos Enrique).
Titles, styles and honours

Titles

Honours

Dynastic honours

Foreign honours

Notes

Already a ducal prince from birth, his father bestowed the substantive title Conte di Bardi ('Count of Bardi') upon him on 2 September 1996.
In 1996 he was incorporated into the Dutch nobility by Queen Beatrix, with the highest noble title Prins de Bourbon de Parme (Prince of Bourbon-Parma), and styled Zijne Koninklijke Hoogheid ('His Royal Highness').
He does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a grandson of Queen Juliana and cousin of the present King Willem-Alexander, he is an official member of the more extended Dutch royal family.
References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (5b48109b-97d6-4aca-99fa-b253e9bde71d)
 Call ID: 5b48109b-97d6-4aca-99fa-b253e9bde71d
  Args:
    type: :Man
    source: Prince_Jaime_Bernardo_of_Bourbon-Parma
  AssignClass (7d45272d-5f95-4be6-b4d8-e03bbe622dab)
 Call ID: 7d45272d-5f95-4be6-b4d8-e03bbe622dab
  Args:
    source: Princess_Irene_of_the_Netherlands
    type: :Woman
  AssignClass (cb2493ed-e996-4b55-bed5-ac2d156dbd78)
 Call ID: cb2493ed-e996-4b55-bed5-ac2d156dbd78
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (c0f717ae-60f8-41b8-8af0-5e23b1bf5bbb)
 Call ID: c0f717ae-60f8-41b8-8af0-5e23b1bf5bbb
  Args:
    type: :Woman
    source: Princess_Margarita
  AssignClass (9c5e3e49-ff13-42a5-9a47-35339d300ec0)
 Call ID: 9c5e3e49-ff13-42a5-9a47-35339d300ec0
  Args:
    type: :Man
    source: Carlos_Duke_of_Parma
  AssignClass (faa24f60-a5cd-47c1-9a5a-8fa79ce3fa99)
 Call ID: faa24f60-a5cd-47c1-9a5a-8fa79ce3fa99
  Args:
    source: Princess_Carolina
    type: :Woman
  AssignClass (3905f3f4-0d9e-4289-a677-eac21bcc3054)
 Call ID: 3905f3f4-0d9e-4289-a677-eac21bcc3054
  Args:
    type: :Woman
    source: Gloria_Irene
  AssignClass (19bbb608-1849-4ec1-8f92-009ca27bf133)
 Call ID: 19bbb608-1849-4ec1-8f92-009ca27bf133
  Args:
    type: :Man
    source: Carlos_Enrique
  AddLiteral (b16ac303-2c37-4f2c-ab92-085aad07f80d)
 Call ID: b16ac303-2c37-4f2c-ab92-085aad07f80d
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon-Parma
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1972
  AddTriple (d9eec52f-93bb-4ebb-87c2-41d4edd92524)
 Call ID: d9eec52f-93bb-4ebb-87c2-41d4edd92524
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon-Parma
    target: Princess_Irene_of_the_Netherlands
    relation: :hasMother
  AddTriple (db30a556-e6f2-49f2-bcdc-751b368aa2a2)
 Call ID: db30a556-e6f2-49f2-bcdc-751b368aa2a2
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon-Parma
    relation: :hasFather
    target: Carlos_Hugo_Duke_of_Parma
  AddTriple (00435d00-57e5-4d05-867d-3f0728ac904b)
 Call ID: 00435d00-57e5-4d05-867d-3f0728ac904b
  Args:
    source: Carlos_Duke_of_Parma
    target: Prince_Jaime_Bernardo_of_Bourbon-Parma
    relation: :isBrotherOf
  AddTriple (79e5bfe2-f6ba-4c8b-bf2b-ae890a5b3b27)
 Call ID: 79e5bfe2-f6ba-4c8b-bf2b-ae890a5b3b27
  Args:
    target: Prince_Jaime_Bernardo_of_Bourbon-Parma
    relation: :isSisterOf
    source: Princess_Margarita
  AddTriple (66e83cfd-7b87-4a1a-b9c2-a6ec13de88b2)
 Call ID: 66e83cfd-7b87-4a1a-b9c2-a6ec13de88b2
  Args:
    source: Princess_Carolina
    relation: :isSisterOf
    target: Prince_Jaime_Bernardo_of_Bourbon-Parma
  AddTriple (c914c7fe-51e5-4156-ba80-d646fb9007d7)
 Call ID: c914c7fe-51e5-4156-ba80-d646fb9007d7
  Args:
    target: Gloria_Irene
    relation: :isFatherOf
    source: Prince_Jaime_Bernardo_of_Bourbon-Parma
  AddTriple (d5c7ce27-5c02-4998-a8cc-de5c8df31979)
 Call ID: d5c7ce27-5c02-4998-a8cc-de5c8df31979
  Args:
    source: Carlos_Duke_of_Parma
    target: Carlos_Enrique
    relation: :isFatherOf
  Finish (4d0912c9-2744-4b71-ad41-54e902654044)
 Call ID: 4d0912c9-2744-4b71-ad41-54e902654044
  Args: