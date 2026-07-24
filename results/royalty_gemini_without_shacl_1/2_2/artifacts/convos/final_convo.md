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
Queen Margrethe II


Count Felix of Monpezat SK (born Prince Felix of Denmark; 22 July 2002) is a member of the Danish royal family.
He is a grandson of Queen Margrethe II and Prince Henrik, and a nephew of King Frederik X. Felix is currently seventh in the line of succession to the Danish throne.
Biography

Felix was born a Prince of Denmark at Rigshospitalet, the Copenhagen University Hospital in Copenhagen, Denmark, on 22 July 2002.
His names were revealed to be Felix Henrik Valdemar Christian.
His godparents are his maternal aunt, Martina Bent; and friends of his parents, Count Christian Ahlefeldt-Laurvig, Oscar Davidsen Siesbye, Damian Sibley and Annick Boel.
At the christening, the musical work Dåbens Pagt composed by Frederik Magle, dedicated to Prince Felix, saw its inaugural performance.
After their divorce, Prince Joachim and Countess Alexandra shared joint custody of Felix and his older brother Prince Nikolai.
The prince attended pre-school at the Garnison Church in Copenhagen, and at age six, followed in the footsteps of his father, brother and uncle at Krebs School in Østerbro.
Titles and styles

Originally known as "His Highness Prince Felix of Denmark", Felix assumed the style "His Highness Prince Felix of Denmark, Count of Monpezat" on 29 April 2008.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
From 1 January 2023, Felix is known as "His Excellency Count Felix of Monpezat".



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a37c05a0-afa8-42f2-ad79-8bff1f16a74e)
 Call ID: a37c05a0-afa8-42f2-ad79-8bff1f16a74e
  Args:
    type: :Person
    source: Queen_Margrethe_II
  AssignClass (e7ea8935-176c-446f-919f-e9ea5c6b5a9d)
 Call ID: e7ea8935-176c-446f-919f-e9ea5c6b5a9d
  Args:
    type: :Woman
    source: Queen_Margrethe_II
  AssignClass (1054b82e-1ba1-4d45-afcf-7ffd767d11dd)
 Call ID: 1054b82e-1ba1-4d45-afcf-7ffd767d11dd
  Args:
    source: Count_Felix_of_Monpezat
    type: :Person
  AssignClass (d9cbf19e-2058-447d-8559-b2dd4bedd2ca)
 Call ID: d9cbf19e-2058-447d-8559-b2dd4bedd2ca
  Args:
    source: Count_Felix_of_Monpezat
    type: :Man
  AddLiteral (c9e542bf-4db4-449f-931f-12ee05b6cecb)
 Call ID: c9e542bf-4db4-449f-931f-12ee05b6cecb
  Args:
    source: Count_Felix_of_Monpezat
    literal_value: His Excellency Count Felix of Monpezat
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (65148c8f-2029-4355-8dee-b816cfe2c6ee)
 Call ID: 65148c8f-2029-4355-8dee-b816cfe2c6ee
  Args:
    relation: :formerlyKnownAs
    literal_value: His Highness Prince Felix of Denmark
    literal_type: xsd:string
    source: Count_Felix_of_Monpezat
  AddLiteral (5087ceda-dbbc-4341-8ecc-ae14ef4df9d4)
 Call ID: 5087ceda-dbbc-4341-8ecc-ae14ef4df9d4
  Args:
    source: Count_Felix_of_Monpezat
    literal_value: His Highness Prince Felix of Denmark, Count of Monpezat
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (9e6ac6fd-8ade-4908-bf5c-ea3e84cbb90a)
 Call ID: 9e6ac6fd-8ade-4908-bf5c-ea3e84cbb90a
  Args:
    literal_value: 2002
    literal_type: xsd:integer
    source: Count_Felix_of_Monpezat
    relation: :hasBirthYear
  AddTriple (e85890a5-1453-44e2-a1a6-d3b268767f74)
 Call ID: e85890a5-1453-44e2-a1a6-d3b268767f74
  Args:
    relation: :hasAncestor
    target: Queen_Margrethe_II
    source: Count_Felix_of_Monpezat
  AssignClass (75f83dc4-2b75-4758-b6a8-c614fdd536ea)
 Call ID: 75f83dc4-2b75-4758-b6a8-c614fdd536ea
  Args:
    source: Prince_Henrik
    type: :Person
  AssignClass (b24605dc-29d1-4b2c-89de-ac06b538ec7d)
 Call ID: b24605dc-29d1-4b2c-89de-ac06b538ec7d
  Args:
    source: Prince_Henrik
    type: :Man
  AddTriple (2f5d537e-49d2-4c1f-be0b-9d5e6cc4fee8)
 Call ID: 2f5d537e-49d2-4c1f-be0b-9d5e6cc4fee8
  Args:
    source: Count_Felix_of_Monpezat
    relation: :hasAncestor
    target: Prince_Henrik
  AssignClass (a64577a7-0678-4f04-abd7-cdd325f964ef)
 Call ID: a64577a7-0678-4f04-abd7-cdd325f964ef
  Args:
    type: :Person
    source: King_Frederik_X
  AssignClass (269b1ee3-3191-4d06-a7b7-ac3512f10e9a)
 Call ID: 269b1ee3-3191-4d06-a7b7-ac3512f10e9a
  Args:
    type: :Man
    source: King_Frederik_X
  AddTriple (0b871772-72eb-47c4-8981-29633d8d00a6)
 Call ID: 0b871772-72eb-47c4-8981-29633d8d00a6
  Args:
    target: King_Frederik_X
    relation: :hasRelation
    source: Count_Felix_of_Monpezat
  AssignClass (fe5e9648-7546-4308-bdad-d3e927e233b0)
 Call ID: fe5e9648-7546-4308-bdad-d3e927e233b0
  Args:
    source: Prince_Joachim
    type: :Person
  AssignClass (2c252d97-189c-420f-b76a-089a47126365)
 Call ID: 2c252d97-189c-420f-b76a-089a47126365
  Args:
    source: Prince_Joachim
    type: :Man
  AddTriple (9a3a9dbd-78d8-4048-8459-e5d2bb73b177)
 Call ID: 9a3a9dbd-78d8-4048-8459-e5d2bb73b177
  Args:
    relation: :hasFather
    target: Prince_Joachim
    source: Count_Felix_of_Monpezat
  AssignClass (0ce85636-81ad-4ace-8204-9026cd8408ce)
 Call ID: 0ce85636-81ad-4ace-8204-9026cd8408ce
  Args:
    source: Countess_Alexandra
    type: :Person
  AssignClass (304ecafb-77a2-43e9-9835-2b9320e2d64a)
 Call ID: 304ecafb-77a2-43e9-9835-2b9320e2d64a
  Args:
    source: Countess_Alexandra
    type: :Woman
  AddTriple (21d7e962-09cf-48ae-a6ba-d4ad908c9346)
 Call ID: 21d7e962-09cf-48ae-a6ba-d4ad908c9346
  Args:
    source: Count_Felix_of_Monpezat
    target: Countess_Alexandra
    relation: :hasMother
  AssignClass (2e2a4ac4-eacb-431c-8026-45724699ec02)
 Call ID: 2e2a4ac4-eacb-431c-8026-45724699ec02
  Args:
    source: Prince_Nikolai
    type: :Person
  AssignClass (5ed5a6c1-a10b-4850-a20c-cf487ca2ec12)
 Call ID: 5ed5a6c1-a10b-4850-a20c-cf487ca2ec12
  Args:
    type: :Man
    source: Prince_Nikolai
  AddTriple (5392a7bf-1994-4f50-9da1-de393c41c071)
 Call ID: 5392a7bf-1994-4f50-9da1-de393c41c071
  Args:
    source: Count_Felix_of_Monpezat
    target: Prince_Nikolai
    relation: :hasBrother
  AssignClass (aab67d42-1f3f-4ad2-8f2e-6832802968d3)
 Call ID: aab67d42-1f3f-4ad2-8f2e-6832802968d3
  Args:
    type: :Person
    source: Martina_Bent
  AssignClass (a610a646-1e1f-4d7f-99a5-e117e0e47b5b)
 Call ID: a610a646-1e1f-4d7f-99a5-e117e0e47b5b
  Args:
    type: :Woman
    source: Martina_Bent
  AddTriple (8f906a56-ed60-4b3a-85ac-60276bcd883c)
 Call ID: 8f906a56-ed60-4b3a-85ac-60276bcd883c
  Args:
    target: Countess_Alexandra
    relation: :isSisterOf
    source: Martina_Bent
  Finish (4b5f9e92-13db-4805-a68e-3e27c6f3dd96)
 Call ID: 4b5f9e92-13db-4805-a68e-3e27c6f3dd96
  Args: