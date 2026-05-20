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
Archduchess Helena of Austria (full German name: Helena Marie Alice Christine Josefa Anna Margareta Madeleine Walburga Blandina Cäcilie Philomena Carmela Ignatia Rita de Cascia, Erzherzogin von Österreich, Prinzessin von Toskana; 30 October 1903 – 8 September 1924) was a member of the Tuscan branch of the House of Habsburg-Lorraine and an Archduchess of Austria and Princess of Bohemia, Hungary, and Tuscany by birth.
Through her marriage to Philipp Albrecht, Hereditary Duke of Württemberg, Helena became a member of the House of Württemberg and Hereditary Duchess consort of Württemberg.
Early life

Helena was born in Linz, Austria-Hungary, the second-eldest child and eldest daughter of Archduke Peter Ferdinand, Prince of Tuscany and his wife Princess Maria Cristina of Bourbon-Two Sicilies.
Helena was raised with her three siblings in Salzburg and Vienna until the end of World War I in 1918 when her family was exiled and moved to Lucerne, Switzerland.
Marriage and issue

Helena married Philipp Albrecht, Hereditary Duke of Württemberg, eldest child and son of Albrecht, Duke of Württemberg and his wife, Archduchess Margarete Sophie of Austria, on 24 October 1923 in Altshausen.
Helena and Philipp Albrecht had one daughter:


Death

Helena died just a week after giving birth to her daughter Maria Christina, aged only 20.
Her husband later married her sister Archduchess Rosa of Austria, Princess of Tuscany in 1928.



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
  AssignClass (e33b7c0b-4040-47fd-9f27-d4db587c267c)
 Call ID: e33b7c0b-4040-47fd-9f27-d4db587c267c
  Args:
    type: :Woman
    source: Helena_of_Austria
  AssignClass (b1bb4909-784c-4adf-b87c-30e0acc54a93)
 Call ID: b1bb4909-784c-4adf-b87c-30e0acc54a93
  Args:
    source: Helena_of_Austria
    type: :Person
  AddLiteral (ee962647-6e33-4a81-aa50-a90fa851db6f)
 Call ID: ee962647-6e33-4a81-aa50-a90fa851db6f
  Args:
    source: Helena_of_Austria
    relation: :hasBirthYear
    literal_value: 1903
    literal_type: xsd:integer
  AddLiteral (15326758-6039-49ae-abc2-0e95a63f909a)
 Call ID: 15326758-6039-49ae-abc2-0e95a63f909a
  Args:
    literal_type: xsd:integer
    source: Helena_of_Austria
    relation: :hasDeathYear
    literal_value: 1924
  AssignClass (c23b97f3-9c86-47b5-8150-9265449b99e5)
 Call ID: c23b97f3-9c86-47b5-8150-9265449b99e5
  Args:
    type: :Man
    source: Peter_Ferdinand
  AssignClass (18ab8ec9-958f-441d-8074-15b106210619)
 Call ID: 18ab8ec9-958f-441d-8074-15b106210619
  Args:
    source: Peter_Ferdinand
    type: :Person
  AssignClass (612ec553-f744-4b25-b0ab-670b14ee6469)
 Call ID: 612ec553-f744-4b25-b0ab-670b14ee6469
  Args:
    type: :Woman
    source: Maria_Cristina_of_Bourbon_Two_Sicilies
  AssignClass (6ce6aaab-a612-48d4-9d65-35cd38f1a78b)
 Call ID: 6ce6aaab-a612-48d4-9d65-35cd38f1a78b
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon_Two_Sicilies
  AddTriple (1d1aec93-3cd5-4383-a4a2-b541c8fb0308)
 Call ID: 1d1aec93-3cd5-4383-a4a2-b541c8fb0308
  Args:
    source: Helena_of_Austria
    relation: :hasFather
    target: Peter_Ferdinand
  AddTriple (2e609674-550f-4113-822c-605d10e92486)
 Call ID: 2e609674-550f-4113-822c-605d10e92486
  Args:
    relation: :hasMother
    source: Helena_of_Austria
    target: Maria_Cristina_of_Bourbon_Two_Sicilies
  AssignClass (ef5e3bbf-f9d8-423f-9e72-4bc117b1e0cd)
 Call ID: ef5e3bbf-f9d8-423f-9e72-4bc117b1e0cd
  Args:
    type: :Man
    source: Philipp_Albrecht_of_Wurttemberg
  AssignClass (c44458a1-7de1-4898-88df-3db6aaf006de)
 Call ID: c44458a1-7de1-4898-88df-3db6aaf006de
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    type: :Person
  AddLiteral (3081879e-05da-4439-8c90-0d79848594a6)
 Call ID: 3081879e-05da-4439-8c90-0d79848594a6
  Args:
    literal_type: xsd:integer
    source: Helena_of_Austria
    relation: :hasMarriageYear
    literal_value: 1923
  AddTriple (2bdebacb-145d-4f43-9aab-6656d49bcf2a)
 Call ID: 2bdebacb-145d-4f43-9aab-6656d49bcf2a
  Args:
    source: Helena_of_Austria
    relation: :hasRelation
    target: Philipp_Albrecht_of_Wurttemberg
  AssignClass (7ceb7d85-6937-4430-bada-2cc82fba1e21)
 Call ID: 7ceb7d85-6937-4430-bada-2cc82fba1e21
  Args:
    type: :Man
    source: Albrecht_of_Wurttemberg
  AssignClass (eb3a5a81-cbf3-4502-bdbf-f342f4a88f29)
 Call ID: eb3a5a81-cbf3-4502-bdbf-f342f4a88f29
  Args:
    source: Albrecht_of_Wurttemberg
    type: :Person
  AssignClass (fe5a5f88-adcd-4004-9e7a-91469d173743)
 Call ID: fe5a5f88-adcd-4004-9e7a-91469d173743
  Args:
    type: :Woman
    source: Margarete_Sophie_of_Austria
  AssignClass (ba435fd4-7488-4176-83fd-6bf3639d8874)
 Call ID: ba435fd4-7488-4176-83fd-6bf3639d8874
  Args:
    type: :Person
    source: Margarete_Sophie_of_Austria
  AddTriple (ab8510c0-b71c-4978-b2c1-8718ad78eeaa)
 Call ID: ab8510c0-b71c-4978-b2c1-8718ad78eeaa
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    relation: :hasFather
    target: Albrecht_of_Wurttemberg
  AddTriple (d10d5280-627f-43bc-b471-5551f6f29874)
 Call ID: d10d5280-627f-43bc-b471-5551f6f29874
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    relation: :hasMother
    target: Margarete_Sophie_of_Austria
  AssignClass (df64b178-571e-4bec-b854-32d98579ca4a)
 Call ID: df64b178-571e-4bec-b854-32d98579ca4a
  Args:
    type: :Woman
    source: Maria_Christina_of_Wurttemberg
  AssignClass (b3102e6e-d5a9-46de-8cb0-8489b41445e9)
 Call ID: b3102e6e-d5a9-46de-8cb0-8489b41445e9
  Args:
    source: Maria_Christina_of_Wurttemberg
    type: :Person
  AddTriple (822d9ab7-1ef3-4c9f-9c0d-b49d577a70ea)
 Call ID: 822d9ab7-1ef3-4c9f-9c0d-b49d577a70ea
  Args:
    target: Helena_of_Austria
    source: Maria_Christina_of_Wurttemberg
    relation: :isDaughterOf
  AddTriple (160df08f-e482-4531-b7d6-b473f6a344f7)
 Call ID: 160df08f-e482-4531-b7d6-b473f6a344f7
  Args:
    relation: :isDaughterOf
    source: Maria_Christina_of_Wurttemberg
    target: Philipp_Albrecht_of_Wurttemberg
  AssignClass (971d60ef-16e6-4d68-80d1-2e8bda886add)
 Call ID: 971d60ef-16e6-4d68-80d1-2e8bda886add
  Args:
    source: Rosa_of_Austria
    type: :Woman
  AssignClass (b9fa6f38-74a9-42d5-93b4-3c5a447a5a48)
 Call ID: b9fa6f38-74a9-42d5-93b4-3c5a447a5a48
  Args:
    type: :Person
    source: Rosa_of_Austria
  AddTriple (5981f471-d86d-4367-a686-25334592a5bf)
 Call ID: 5981f471-d86d-4367-a686-25334592a5bf
  Args:
    relation: :isSisterOf
    source: Rosa_of_Austria
    target: Helena_of_Austria
  AddTriple (6f08ac22-149f-4400-8f99-86e78306bcfa)
 Call ID: 6f08ac22-149f-4400-8f99-86e78306bcfa
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    relation: :hasRelation
    target: Rosa_of_Austria
  AddLiteral (a866fc70-6ced-437c-9fe7-60e13ad29818)
 Call ID: a866fc70-6ced-437c-9fe7-60e13ad29818
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1928
    source: Rosa_of_Austria
  Finish (49eb83f3-ca0f-46f7-a337-9420ae9b6c5d)
 Call ID: 49eb83f3-ca0f-46f7-a337-9420ae9b6c5d
  Args: