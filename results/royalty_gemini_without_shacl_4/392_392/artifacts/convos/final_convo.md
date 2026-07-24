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
Prince William Victor Charles Augustus Henry Sigismund of Prussia (German: Wilhelm Viktor Karl August Heinrich Sigismund; 27 November 1896 at Kiel – 14 November 1978 at Puntarenas, Costa Rica), was the second son of Prince Henry of Prussia and Princess Irene of Hesse and by Rhine.
He was the nephew of Kaiser Wilhelm II and Tsarina Alexandra of Russia.
Life

Marriage and issue

On 11 July 1919 at Hemmelmark, he married Princess Charlotte of Saxe-Altenburg (4 March 1899 – 16 February 1989), the eldest daughter of Ernst II, Duke of Saxe-Altenburg.
In 1927, Sigismund and his family resettled in Costa Rica  three years after his son Alfred (1924–2013) had been born in Guatemala.
In 1957, Sigismund returned to Germany to meet with Anna Anderson whom he recognized as his cousin Grand Duchess Anastasia.
Sigismund died in Puntarenas, Costa Rica, on 14 November 1978.
Honours and awards

Prince Sigismund received the following awards:


Ancestry

See also

References



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (fe96825b-a7b7-472e-8d97-59bfdd7d0a39)
 Call ID: fe96825b-a7b7-472e-8d97-59bfdd7d0a39
  Args:
    source: :Prince_Sigismund_of_Prussia
    type: :Man
  AssignClass (5d8bc294-b526-4777-95ce-4de063240a0a)
 Call ID: 5d8bc294-b526-4777-95ce-4de063240a0a
  Args:
    type: :Person
    source: :Prince_Sigismund_of_Prussia
  AddLiteral (92feeb07-e633-442c-9c66-41f56be2e4b4)
 Call ID: 92feeb07-e633-442c-9c66-41f56be2e4b4
  Args:
    relation: :hasBirthYear
    source: :Prince_Sigismund_of_Prussia
    literal_type: xsd:integer
    literal_value: 1896
  AddLiteral (35fa867b-0229-45dd-9c3c-cd7528b02273)
 Call ID: 35fa867b-0229-45dd-9c3c-cd7528b02273
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1978
    source: :Prince_Sigismund_of_Prussia
  AddLiteral (17e50c6b-ca9b-48b2-b067-f54675da0b9e)
 Call ID: 17e50c6b-ca9b-48b2-b067-f54675da0b9e
  Args:
    literal_type: xsd:string
    literal_value: Wilhelm Viktor Karl August Heinrich Sigismund
    source: :Prince_Sigismund_of_Prussia
    relation: :alsoKnownAs
  AssignClass (deaf0f10-9457-48c9-9497-6941a04e5261)
 Call ID: deaf0f10-9457-48c9-9497-6941a04e5261
  Args:
    type: :Man
    source: :Prince_Henry_of_Prussia
  AssignClass (e1643a8f-36f2-430b-9ef5-5cc49ef468ac)
 Call ID: e1643a8f-36f2-430b-9ef5-5cc49ef468ac
  Args:
    type: :Person
    source: :Prince_Henry_of_Prussia
  AddTriple (31d0842b-e18b-45a5-9d20-3070482c863d)
 Call ID: 31d0842b-e18b-45a5-9d20-3070482c863d
  Args:
    source: :Prince_Sigismund_of_Prussia
    target: :Prince_Henry_of_Prussia
    relation: :hasFather
  AssignClass (5da1d293-bfd3-496b-a218-b24a1e231ba4)
 Call ID: 5da1d293-bfd3-496b-a218-b24a1e231ba4
  Args:
    type: :Woman
    source: :Princess_Irene_of_Hesse_and_by_Rhine
  AssignClass (5a73bb21-dbb5-4652-b7c2-ac8dcb0edd27)
 Call ID: 5a73bb21-dbb5-4652-b7c2-ac8dcb0edd27
  Args:
    type: :Person
    source: :Princess_Irene_of_Hesse_and_by_Rhine
  AddTriple (6d88cf6b-bafc-4572-968e-c8736c031c0a)
 Call ID: 6d88cf6b-bafc-4572-968e-c8736c031c0a
  Args:
    relation: :hasMother
    target: :Princess_Irene_of_Hesse_and_by_Rhine
    source: :Prince_Sigismund_of_Prussia
  AssignClass (2ec62cb8-36b2-4340-b8b3-eb8bbe1ea176)
 Call ID: 2ec62cb8-36b2-4340-b8b3-eb8bbe1ea176
  Args:
    source: :Princess_Charlotte_of_Saxe-Altenburg
    type: :Woman
  AssignClass (62ca3017-a4d6-4b01-8d2d-d4fe8fd8b83f)
 Call ID: 62ca3017-a4d6-4b01-8d2d-d4fe8fd8b83f
  Args:
    type: :Person
    source: :Princess_Charlotte_of_Saxe-Altenburg
  AddLiteral (fd83d48b-ac14-42c5-9175-ecffaf671b67)
 Call ID: fd83d48b-ac14-42c5-9175-ecffaf671b67
  Args:
    relation: :hasMarriageYear
    source: :Prince_Sigismund_of_Prussia
    literal_type: xsd:integer
    literal_value: 1919
  AddTriple (7dc603c0-5488-4dcb-b58e-be6e249457a1)
 Call ID: 7dc603c0-5488-4dcb-b58e-be6e249457a1
  Args:
    relation: :hasRelation
    target: :Princess_Charlotte_of_Saxe-Altenburg
    source: :Prince_Sigismund_of_Prussia
  AssignClass (8d28ad1d-466d-4d57-bb6a-dae83365354c)
 Call ID: 8d28ad1d-466d-4d57-bb6a-dae83365354c
  Args:
    source: :Ernst_II_Duke_of_Saxe-Altenburg
    type: :Man
  AssignClass (b6d3c438-a2c0-4124-9165-487145e10c4c)
 Call ID: b6d3c438-a2c0-4124-9165-487145e10c4c
  Args:
    source: :Ernst_II_Duke_of_Saxe-Altenburg
    type: :Person
  AddTriple (64636a19-bf26-440a-a221-928e9bfbecf8)
 Call ID: 64636a19-bf26-440a-a221-928e9bfbecf8
  Args:
    source: :Princess_Charlotte_of_Saxe-Altenburg
    target: :Ernst_II_Duke_of_Saxe-Altenburg
    relation: :hasFather
  AssignClass (a740cad1-c99d-446c-8ca2-1b17648fa80d)
 Call ID: a740cad1-c99d-446c-8ca2-1b17648fa80d
  Args:
    type: :Man
    source: :Alfred_of_Prussia
  AssignClass (a475d4c9-30e2-4b67-ac41-4f4075174ba4)
 Call ID: a475d4c9-30e2-4b67-ac41-4f4075174ba4
  Args:
    source: :Alfred_of_Prussia
    type: :Person
  AddTriple (826d0cb8-7f53-4456-8b75-6cebb829c33c)
 Call ID: 826d0cb8-7f53-4456-8b75-6cebb829c33c
  Args:
    target: :Alfred_of_Prussia
    source: :Prince_Sigismund_of_Prussia
    relation: :hasSon
  AddLiteral (7aa12b33-a057-4020-9147-0815fc3eb7e9)
 Call ID: 7aa12b33-a057-4020-9147-0815fc3eb7e9
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1924
    source: :Alfred_of_Prussia
  AddLiteral (f30cae93-ab74-44e1-890d-6b179cd7ea5e)
 Call ID: f30cae93-ab74-44e1-890d-6b179cd7ea5e
  Args:
    relation: :hasDeathYear
    source: :Alfred_of_Prussia
    literal_type: xsd:integer
    literal_value: 2013
  Finish (c01e2743-c0eb-42c6-9dfc-1cd5a3ebe363)
 Call ID: c01e2743-c0eb-42c6-9dfc-1cd5a3ebe363
  Args: