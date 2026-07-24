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
Sir David Bowes-Lyon (2 May 1902 – 13 September 1961) was a British aristocrat who was the younger brother of Queen Elizabeth the Queen Mother and uncle to Queen Elizabeth II.
Early life

David Bowes-Lyon was born on 2 May 1902.
He was the tenth and youngest child, and the sixth son, of Claude Bowes-Lyon, 14th
His paternal grandparents were Claude Bowes-Lyon, 13th
Career

During World War II, Bowes-Lyon was a member of the secret propaganda department Political Warfare Executive.
On 15 December 1948, Bowes-Lyon attended the christening of his great-nephew Prince Charles.
He was one of eight sponsors of the prince, along with King George VI, King Haakon VII of Norway, Queen Mary, Princess Margaret, the Dowager Marchioness of Milford Haven, Patricia, Lady Brabourne, and Prince George of Greece and Denmark.
As a keen gardener, Bowes-Lyon was awarded the Victoria Medal of Honour in 1953 and served as president of the Royal Horticultural Society from 1953 to 1961.
Bowes-Lyon was made a Knight Commander of the Royal Victorian Order in the 1959 Birthday Honours.
Personal life

On 6 February 1929, David Bowes-Lyon married Rachel Pauline Spender-Clay (1907–1996), younger daughter of Herbert Henry Spender-Clay and Pauline Spender-Clay.
Together, they had two children:


Bowes-Lyon died at his sister Elizabeth's home, Birkhall, on the Balmoral estate, of a heart attack after suffering from hemiplegia on 13 September 1961, aged 59.
The Queen Mother discovered him dead in bed.



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
  AssignClass (342f9b17-104a-4588-a4ca-2745358e9629)
 Call ID: 342f9b17-104a-4588-a4ca-2745358e9629
  Args:
    type: :Man
    source: :David_Bowes-Lyon
  AssignClass (510d7c7c-4d86-49d3-9a33-41e4e92d3a4b)
 Call ID: 510d7c7c-4d86-49d3-9a33-41e4e92d3a4b
  Args:
    type: :Person
    source: :David_Bowes-Lyon
  AddLiteral (60b607ea-7f6b-4e82-a151-14b5e4f42296)
 Call ID: 60b607ea-7f6b-4e82-a151-14b5e4f42296
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (13ee5641-e970-407c-affb-76293c43f721)
 Call ID: 13ee5641-e970-407c-affb-76293c43f721
  Args:
    literal_value: 1961
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (ee040e54-f9f2-4029-b68b-2c4fb055b7cb)
 Call ID: ee040e54-f9f2-4029-b68b-2c4fb055b7cb
  Args:
    type: :Woman
    source: :Queen_Elizabeth_The_Queen_Mother
  AssignClass (15f49af6-fc07-4f60-8251-0e956bd67249)
 Call ID: 15f49af6-fc07-4f60-8251-0e956bd67249
  Args:
    type: :Person
    source: :Queen_Elizabeth_The_Queen_Mother
  AddTriple (7ccd3c9e-0832-47f6-b76c-3eaf85fc6329)
 Call ID: 7ccd3c9e-0832-47f6-b76c-3eaf85fc6329
  Args:
    source: :David_Bowes-Lyon
    relation: :isSiblingOf
    target: :Queen_Elizabeth_The_Queen_Mother
  AssignClass (8fa46c92-a9a2-4112-903f-187cefed62bd)
 Call ID: 8fa46c92-a9a2-4112-903f-187cefed62bd
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (22004958-9525-42d7-a191-19255ffeec6a)
 Call ID: 22004958-9525-42d7-a191-19255ffeec6a
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (48433df6-b818-4abf-bb52-8c7c5b6415bf)
 Call ID: 48433df6-b818-4abf-bb52-8c7c5b6415bf
  Args:
    source: :David_Bowes-Lyon
    target: :Queen_Elizabeth_II
    relation: :isUncleOf
  AssignClass (83e28c76-ee2a-4f11-b18f-eef0bca8e859)
 Call ID: 83e28c76-ee2a-4f11-b18f-eef0bca8e859
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon_14th
  AssignClass (3ab957be-0a79-48dc-b0a9-1f1a35138c5c)
 Call ID: 3ab957be-0a79-48dc-b0a9-1f1a35138c5c
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon_14th
  AddTriple (b95f7ad6-2b39-45cf-b381-66e08fb56e96)
 Call ID: b95f7ad6-2b39-45cf-b381-66e08fb56e96
  Args:
    target: :Claude_Bowes-Lyon_14th
    relation: :hasFather
    source: :David_Bowes-Lyon
  AssignClass (0def26fe-8f97-426d-8750-144fdbb4a57e)
 Call ID: 0def26fe-8f97-426d-8750-144fdbb4a57e
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon_13th
  AssignClass (b550c66d-3fdc-4718-a361-14eb84176cc5)
 Call ID: b550c66d-3fdc-4718-a361-14eb84176cc5
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon_13th
  AddTriple (a68c0a9f-8245-49d4-94b8-a0802ebe519d)
 Call ID: a68c0a9f-8245-49d4-94b8-a0802ebe519d
  Args:
    source: :Claude_Bowes-Lyon_14th
    relation: :hasFather
    target: :Claude_Bowes-Lyon_13th
  AssignClass (09524a6e-e03a-4caa-918f-ec8200a0c9f8)
 Call ID: 09524a6e-e03a-4caa-918f-ec8200a0c9f8
  Args:
    type: :Woman
    source: :Rachel_Pauline_Spender-Clay
  AssignClass (c82be5da-43f5-4eb2-a791-101f91d92ade)
 Call ID: c82be5da-43f5-4eb2-a791-101f91d92ade
  Args:
    type: :Person
    source: :Rachel_Pauline_Spender-Clay
  AddLiteral (a0f92c93-0d7a-4d9e-9957-2135f18cc915)
 Call ID: a0f92c93-0d7a-4d9e-9957-2135f18cc915
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1929
    source: :David_Bowes-Lyon
  AddTriple (34e675ea-e557-43ae-8e77-a172bcd79a68)
 Call ID: 34e675ea-e557-43ae-8e77-a172bcd79a68
  Args:
    target: :Rachel_Pauline_Spender-Clay
    relation: :hasRelation
    source: :David_Bowes-Lyon
  AssignClass (bc3d2c5d-0b00-41c9-a502-a0550e3fe798)
 Call ID: bc3d2c5d-0b00-41c9-a502-a0550e3fe798
  Args:
    type: :Man
    source: :Herbert_Henry_Spender-Clay
  AssignClass (d3ccf6bd-894b-41c0-9d9f-740d1a6781e4)
 Call ID: d3ccf6bd-894b-41c0-9d9f-740d1a6781e4
  Args:
    type: :Person
    source: :Herbert_Henry_Spender-Clay
  AssignClass (20f21630-d0f1-421a-a9a8-eea963ebf92a)
 Call ID: 20f21630-d0f1-421a-a9a8-eea963ebf92a
  Args:
    type: :Woman
    source: :Pauline_Spender-Clay
  AssignClass (9a40937d-072d-4e5e-be83-5aa0e7d18ab7)
 Call ID: 9a40937d-072d-4e5e-be83-5aa0e7d18ab7
  Args:
    type: :Person
    source: :Pauline_Spender-Clay
  AddTriple (9efdf7d9-1039-4ca4-b617-5512a0ee5e60)
 Call ID: 9efdf7d9-1039-4ca4-b617-5512a0ee5e60
  Args:
    source: :Rachel_Pauline_Spender-Clay
    relation: :hasFather
    target: :Herbert_Henry_Spender-Clay
  AddTriple (52d205a1-4b1a-4040-844c-2b5ff1bac2ca)
 Call ID: 52d205a1-4b1a-4040-844c-2b5ff1bac2ca
  Args:
    target: :Pauline_Spender-Clay
    relation: :hasMother
    source: :Rachel_Pauline_Spender-Clay
  AddTriple (0df080bd-4742-4cac-90b9-fbdc4187b7bc)
 Call ID: 0df080bd-4742-4cac-90b9-fbdc4187b7bc
  Args:
    source: :Queen_Elizabeth_The_Queen_Mother
    relation: :isSisterOf
    target: :David_Bowes-Lyon
  Finish (0eacae06-3d6d-475d-9002-a21066e1abcc)
 Call ID: 0eacae06-3d6d-475d-9002-a21066e1abcc
  Args: