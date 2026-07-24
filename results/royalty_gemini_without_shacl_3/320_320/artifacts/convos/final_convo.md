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
  AssignClass (ddf023e6-4833-4345-a1bd-70e98485ea1d)
 Call ID: ddf023e6-4833-4345-a1bd-70e98485ea1d
  Args:
    type: :Man
    source: :David_Bowes-Lyon
  AssignClass (d7fe81ac-1f78-45b3-bb3b-588eaaa66153)
 Call ID: d7fe81ac-1f78-45b3-bb3b-588eaaa66153
  Args:
    source: :David_Bowes-Lyon
    type: :Person
  AddLiteral (f206d3d9-b074-498b-9ef3-8fd9f0d4d0c5)
 Call ID: f206d3d9-b074-498b-9ef3-8fd9f0d4d0c5
  Args:
    literal_value: 1902
    relation: :hasBirthYear
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (cfb2bd2d-af08-4ccb-84c7-1b9a4f6cace1)
 Call ID: cfb2bd2d-af08-4ccb-84c7-1b9a4f6cace1
  Args:
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1961
    relation: :hasDeathYear
  AssignClass (0c66272a-19e0-4f8a-b7ed-c30c2546d4d5)
 Call ID: 0c66272a-19e0-4f8a-b7ed-c30c2546d4d5
  Args:
    type: :Woman
    source: :Elizabeth_Bowes-Lyon
  AssignClass (d67a96d5-7870-44b6-8a3c-7252ea6b7d8b)
 Call ID: d67a96d5-7870-44b6-8a3c-7252ea6b7d8b
  Args:
    type: :Person
    source: :Elizabeth_Bowes-Lyon
  AddTriple (cca2e956-efbc-4df6-a00b-5c7c1382a756)
 Call ID: cca2e956-efbc-4df6-a00b-5c7c1382a756
  Args:
    relation: :hasSister
    source: :David_Bowes-Lyon
    target: :Elizabeth_Bowes-Lyon
  AssignClass (fc916d76-5d02-42ce-88e2-389afae39ef9)
 Call ID: fc916d76-5d02-42ce-88e2-389afae39ef9
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (f226c749-8a9a-4ce4-bc07-232ba113be22)
 Call ID: f226c749-8a9a-4ce4-bc07-232ba113be22
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AddTriple (e473fc1b-70ef-4c38-83c0-294d7728d968)
 Call ID: e473fc1b-70ef-4c38-83c0-294d7728d968
  Args:
    relation: :isUncleOf
    source: :David_Bowes-Lyon
    target: :Queen_Elizabeth_II
  AssignClass (b0dc8ffe-71cb-4987-9d86-48738994780c)
 Call ID: b0dc8ffe-71cb-4987-9d86-48738994780c
  Args:
    source: :Claude_Bowes-Lyon_14th
    type: :Man
  AssignClass (cf50089d-c94b-4f3e-bdc1-ded396f043a2)
 Call ID: cf50089d-c94b-4f3e-bdc1-ded396f043a2
  Args:
    type: :Ancestor
    source: :Claude_Bowes-Lyon_14th
  AddTriple (cd7773a7-ffc5-4892-a032-be838de4113b)
 Call ID: cd7773a7-ffc5-4892-a032-be838de4113b
  Args:
    relation: :hasFather
    source: :David_Bowes-Lyon
    target: :Claude_Bowes-Lyon_14th
  AssignClass (6217ae10-a655-4768-b0ec-8a7c13348708)
 Call ID: 6217ae10-a655-4768-b0ec-8a7c13348708
  Args:
    source: :Claude_Bowes-Lyon_13th
    type: :Man
  AssignClass (392b4c9d-ad73-4fb6-adb7-5f281faa6df8)
 Call ID: 392b4c9d-ad73-4fb6-adb7-5f281faa6df8
  Args:
    type: :Ancestor
    source: :Claude_Bowes-Lyon_13th
  AddTriple (8ac5e9b8-1231-4bfe-aa74-5711e174cc97)
 Call ID: 8ac5e9b8-1231-4bfe-aa74-5711e174cc97
  Args:
    relation: :hasFather
    target: :Claude_Bowes-Lyon_13th
    source: :Claude_Bowes-Lyon_14th
  AssignClass (fd97c1a6-6ae1-4bce-9006-2fc03c8840c7)
 Call ID: fd97c1a6-6ae1-4bce-9006-2fc03c8840c7
  Args:
    type: :Woman
    source: :Rachel_Pauline_Spender-Clay
  AssignClass (c865d981-cb3e-4582-a06e-72e2273f098f)
 Call ID: c865d981-cb3e-4582-a06e-72e2273f098f
  Args:
    source: :Rachel_Pauline_Spender-Clay
    type: :Person
  AddLiteral (6a3648e2-baff-4755-b993-e1fc7379228a)
 Call ID: 6a3648e2-baff-4755-b993-e1fc7379228a
  Args:
    literal_value: 1929
    relation: :hasMarriageYear
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (6dd8c2aa-a4bc-4e45-bccf-81e45d0e14a4)
 Call ID: 6dd8c2aa-a4bc-4e45-bccf-81e45d0e14a4
  Args:
    relation: :hasRelation
    target: :Rachel_Pauline_Spender-Clay
    source: :David_Bowes-Lyon
  AssignClass (02c688a3-9382-4758-9cf1-f6dfe5eb4792)
 Call ID: 02c688a3-9382-4758-9cf1-f6dfe5eb4792
  Args:
    source: :Herbert_Henry_Spender-Clay
    type: :Man
  AssignClass (5c59369b-4690-4b18-a092-3d59460ddf19)
 Call ID: 5c59369b-4690-4b18-a092-3d59460ddf19
  Args:
    source: :Herbert_Henry_Spender-Clay
    type: :Ancestor
  AssignClass (a4272758-2c77-4a14-8a28-474352dda509)
 Call ID: a4272758-2c77-4a14-8a28-474352dda509
  Args:
    source: :Pauline_Spender-Clay
    type: :Woman
  AssignClass (a66961cb-b0fe-4092-bdc9-adfa6f248163)
 Call ID: a66961cb-b0fe-4092-bdc9-adfa6f248163
  Args:
    source: :Pauline_Spender-Clay
    type: :Ancestor
  AddTriple (dec8b493-7bf8-4066-96d9-0255b223b27f)
 Call ID: dec8b493-7bf8-4066-96d9-0255b223b27f
  Args:
    target: :Herbert_Henry_Spender-Clay
    source: :Rachel_Pauline_Spender-Clay
    relation: :hasFather
  AddTriple (4c29dc25-7914-4c4f-8e6b-7a9718aed4cf)
 Call ID: 4c29dc25-7914-4c4f-8e6b-7a9718aed4cf
  Args:
    relation: :hasMother
    source: :Rachel_Pauline_Spender-Clay
    target: :Pauline_Spender-Clay
  Finish (2106b446-fb2d-47f4-8a9e-676e778abfc0)
 Call ID: 2106b446-fb2d-47f4-8a9e-676e778abfc0
  Args: