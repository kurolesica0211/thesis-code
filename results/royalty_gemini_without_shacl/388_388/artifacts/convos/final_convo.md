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
Duke Paul Frederick of Mecklenburg (German: Herzog Paul Friedrich zu Mecklenburg; 19 September 1852 – 17 May 1923) was a member of the House of Mecklenburg-Schwerin and general of the Mecklenburg cavalry.
Life

Duke Paul Frederick was born in Ludwigslust Castle as the second eldest son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and his first wife Princess Augusta Reuss of Köstritz, the daughter of Prince Henry LXIII Reuss of Köstritz.
Duke Paul Frederick married in Schwerin on 5 May 1881 his cousin, the Austrian born Princess Marie of Windisch-Graetz, the daughter of Prince Hugo of Windisch-Graetz and his wife Duchess Louise of Mecklenburg-Schwerin.
The couple who had five children who were all raised Roman Catholic, the religion of Princess Marie, lived a quiet life in Venice.
On 21 April 1884 Duke Paul Frederick renounced his and his sons rights of succession to Mecklenburg-Schwerin in favour of his younger brothers and their sons, so they would take precedence over him and his.
In 1887, Duke Paul Fredrick raised a Lutheran decided to convert to Roman Catholicism the religion of his wife and children.
In 1906 after upsetting his nephew Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, over the amount of money that he was spending Duke Paul Frederick and his wife were ordered to submit to the controller of the royal household.
Duke Paul Frederick died in Ludwigslust, where he and his wife are both buried in the Louisenkapelle.



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
  AssignClass (f254fa93-7f6f-4cb9-aff7-b420be820853)
 Call ID: f254fa93-7f6f-4cb9-aff7-b420be820853
  Args:
    source: :PaulFrederickOfMecklenburg
    type: :Man
  AssignClass (377713a5-d056-4328-b674-38469dd612ae)
 Call ID: 377713a5-d056-4328-b674-38469dd612ae
  Args:
    source: :PaulFrederickOfMecklenburg
    type: :Person
  AddLiteral (f189144b-e4a9-4382-b5e0-86d94c6aca79)
 Call ID: f189144b-e4a9-4382-b5e0-86d94c6aca79
  Args:
    literal_value: 1852
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :PaulFrederickOfMecklenburg
  AddLiteral (309a22c9-a7ed-44ce-8db1-9fcba40c40a8)
 Call ID: 309a22c9-a7ed-44ce-8db1-9fcba40c40a8
  Args:
    relation: :hasDeathYear
    source: :PaulFrederickOfMecklenburg
    literal_value: 1923
    literal_type: xsd:integer
  AssignClass (f23ffa0f-cdf8-499e-b06b-26b8b999d052)
 Call ID: f23ffa0f-cdf8-499e-b06b-26b8b999d052
  Args:
    type: :Man
    source: :FrederickFrancisII
  AssignClass (d5cb109d-9836-4c3b-8e2f-2de303b826c9)
 Call ID: d5cb109d-9836-4c3b-8e2f-2de303b826c9
  Args:
    source: :FrederickFrancisII
    type: :Person
  AssignClass (79e20d6b-e743-4110-8715-01c4d0a99b63)
 Call ID: 79e20d6b-e743-4110-8715-01c4d0a99b63
  Args:
    type: :Woman
    source: :AugustaReussOfKostritz
  AssignClass (1e956111-f6bf-417f-a907-726bb27dd4a7)
 Call ID: 1e956111-f6bf-417f-a907-726bb27dd4a7
  Args:
    source: :AugustaReussOfKostritz
    type: :Person
  AddTriple (d7486034-60e4-4d15-bdbf-a0ec37ed939e)
 Call ID: d7486034-60e4-4d15-bdbf-a0ec37ed939e
  Args:
    target: :FrederickFrancisII
    relation: :hasFather
    source: :PaulFrederickOfMecklenburg
  AddTriple (48c14f20-3cdc-45f6-be21-92b7aae23ec6)
 Call ID: 48c14f20-3cdc-45f6-be21-92b7aae23ec6
  Args:
    target: :AugustaReussOfKostritz
    relation: :hasMother
    source: :PaulFrederickOfMecklenburg
  AssignClass (19a6b516-33fd-4512-b83f-bab44194b4d6)
 Call ID: 19a6b516-33fd-4512-b83f-bab44194b4d6
  Args:
    type: :Man
    source: :HenryLXIIIReussOfKostritz
  AssignClass (f75be3e9-8562-41d5-a3fd-1e8576533ea2)
 Call ID: f75be3e9-8562-41d5-a3fd-1e8576533ea2
  Args:
    type: :Person
    source: :HenryLXIIIReussOfKostritz
  AddTriple (84e6769a-50dc-404d-a535-9a9872808efd)
 Call ID: 84e6769a-50dc-404d-a535-9a9872808efd
  Args:
    relation: :hasFather
    source: :AugustaReussOfKostritz
    target: :HenryLXIIIReussOfKostritz
  AssignClass (8ac3f6bd-3ed7-4c82-b02d-9b757e9e43b9)
 Call ID: 8ac3f6bd-3ed7-4c82-b02d-9b757e9e43b9
  Args:
    source: :MarieOfWindischGraetz
    type: :Woman
  AssignClass (6d3fa8b2-2311-48ba-9b7b-dcd0a1a87f50)
 Call ID: 6d3fa8b2-2311-48ba-9b7b-dcd0a1a87f50
  Args:
    type: :Person
    source: :MarieOfWindischGraetz
  AddLiteral (497c5d83-7c9f-4598-b0b5-5f1af746b09c)
 Call ID: 497c5d83-7c9f-4598-b0b5-5f1af746b09c
  Args:
    relation: :hasMarriageYear
    source: :PaulFrederickOfMecklenburg
    literal_value: 1881
    literal_type: xsd:integer
  AddTriple (33c75ebe-18e8-45b6-b2a5-399624962291)
 Call ID: 33c75ebe-18e8-45b6-b2a5-399624962291
  Args:
    target: :MarieOfWindischGraetz
    source: :PaulFrederickOfMecklenburg
    relation: :hasRelation
  AssignClass (40cfa76a-ab42-4cae-90b2-346e3e7e7a17)
 Call ID: 40cfa76a-ab42-4cae-90b2-346e3e7e7a17
  Args:
    source: :HugoOfWindischGraetz
    type: :Man
  AssignClass (7960b58f-e546-4e23-bfb6-3e510f9ff290)
 Call ID: 7960b58f-e546-4e23-bfb6-3e510f9ff290
  Args:
    source: :HugoOfWindischGraetz
    type: :Person
  AssignClass (40a7a1bf-c7a3-4e3b-a3e4-ca6b039f4061)
 Call ID: 40a7a1bf-c7a3-4e3b-a3e4-ca6b039f4061
  Args:
    type: :Woman
    source: :LouiseOfMecklenburgSchwerin
  AssignClass (68cd8e38-f988-4980-8599-431651d30c3b)
 Call ID: 68cd8e38-f988-4980-8599-431651d30c3b
  Args:
    source: :LouiseOfMecklenburgSchwerin
    type: :Person
  AddTriple (940d7ac6-c34c-4600-956a-037a2260c497)
 Call ID: 940d7ac6-c34c-4600-956a-037a2260c497
  Args:
    relation: :hasFather
    source: :MarieOfWindischGraetz
    target: :HugoOfWindischGraetz
  AddTriple (72ec58b3-9a00-48fa-b60b-4ae2bccc5493)
 Call ID: 72ec58b3-9a00-48fa-b60b-4ae2bccc5493
  Args:
    target: :LouiseOfMecklenburgSchwerin
    source: :MarieOfWindischGraetz
    relation: :hasMother
  AssignClass (b2ec1899-9836-40c3-8cd9-3d4deffd856e)
 Call ID: b2ec1899-9836-40c3-8cd9-3d4deffd856e
  Args:
    source: :FrederickFrancisIV
    type: :Man
  AssignClass (7a9c6a69-0b6b-411f-aaf1-e07254b58c9e)
 Call ID: 7a9c6a69-0b6b-411f-aaf1-e07254b58c9e
  Args:
    source: :FrederickFrancisIV
    type: :Person
  AddTriple (b499fdeb-351e-43bf-aef3-f957b34720a7)
 Call ID: b499fdeb-351e-43bf-aef3-f957b34720a7
  Args:
    target: :FrederickFrancisIV
    source: :PaulFrederickOfMecklenburg
    relation: :hasRelation
  Finish (31090f81-cd46-4090-8926-7724d70e25be)
 Call ID: 31090f81-cd46-4090-8926-7724d70e25be
  Args: