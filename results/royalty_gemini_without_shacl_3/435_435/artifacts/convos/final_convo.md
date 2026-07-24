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
Princess Alexandrine Irene of Prussia (7 April 1915 – 2 October 1980) was the elder daughter and fifth child of Wilhelm, German Crown Prince, and Cecilie of Mecklenburg-Schwerin.
Her grandparents were Wilhelm II, German Emperor and his wife Augusta Victoria of Schleswig-Holstein, and Frederick Francis III of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
Alexandrine was a member of the House of Hohenzollern.
She was a great-great-granddaughter of Queen Victoria.
Life

Alexandrine was born at the Kronprinzenpalais in Berlin.
She followed older brothers Wilhelm, Louis Ferdinand, Hubertus, and Frederick.
Alexandrine's only sister, Cecilie, was born in 1917.
It became clear shortly after Alexandrine's birth that she had Down syndrome.
Unlike other disabled royal children, Alexandrine was not hidden away.
As a teenager, Alexandrine attended the Trüpersche Sonderschule, a school dedicated to the education of children with special needs.
Alexandrine celebrated her confirmation along with her sister Cecilie in October 1934.
Alexandrine lived most of her later life in Bavaria, first in Pöcking and later near Lake Starnberg, where she was visited there regularly by her family, particularly her brother Louis Ferdinand.
Alexandrine died on 2 October 1980.
She was buried near her parents and brother Frederick at Hohenzollern Castle.



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
  AssignClass (2acabec4-d98c-4cf3-9d21-6ada22463f8f)
 Call ID: 2acabec4-d98c-4cf3-9d21-6ada22463f8f
  Args:
    source: Alexandrine_of_Prussia
    type: :Woman
  AssignClass (60a9600c-2caf-44f6-9435-a45df1748cb0)
 Call ID: 60a9600c-2caf-44f6-9435-a45df1748cb0
  Args:
    type: :Person
    source: Alexandrine_of_Prussia
  AddLiteral (e2ee9aa9-f42b-4d9f-8e13-6e42ad9906c5)
 Call ID: e2ee9aa9-f42b-4d9f-8e13-6e42ad9906c5
  Args:
    relation: :hasBirthYear
    source: Alexandrine_of_Prussia
    literal_type: xsd:integer
    literal_value: 1915
  AddLiteral (57eff099-7e59-4bb9-941a-5ed07c4c7045)
 Call ID: 57eff099-7e59-4bb9-941a-5ed07c4c7045
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Alexandrine_of_Prussia
    relation: :hasDeathYear
  AssignClass (aa29f93a-0587-4533-9cf6-40f26df2d726)
 Call ID: aa29f93a-0587-4533-9cf6-40f26df2d726
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (72818c73-f28f-4e4c-859b-fb7136cd6130)
 Call ID: 72818c73-f28f-4e4c-859b-fb7136cd6130
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AssignClass (bf713db7-130a-46e5-a49f-37dbf3523a80)
 Call ID: bf713db7-130a-46e5-a49f-37dbf3523a80
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (fc627101-9ae3-476c-a1a9-e66cb8fc5fe1)
 Call ID: fc627101-9ae3-476c-a1a9-e66cb8fc5fe1
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (52f7bb15-341e-46bd-b087-2515eeecaf81)
 Call ID: 52f7bb15-341e-46bd-b087-2515eeecaf81
  Args:
    source: Alexandrine_of_Prussia
    target: Wilhelm_German_Crown_Prince
    relation: :hasFather
  AddTriple (4cb7af34-6b54-4cc3-8cbc-f0984f2879ac)
 Call ID: 4cb7af34-6b54-4cc3-8cbc-f0984f2879ac
  Args:
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Alexandrine_of_Prussia
  AssignClass (0d8e8f0b-2239-41a6-90f3-dbeb42d3c391)
 Call ID: 0d8e8f0b-2239-41a6-90f3-dbeb42d3c391
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (682a6549-b771-4c0b-a93e-5647a17b08d5)
 Call ID: 682a6549-b771-4c0b-a93e-5647a17b08d5
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AssignClass (d67e3212-1c15-41b0-afc6-a0e9ac1dda7d)
 Call ID: d67e3212-1c15-41b0-afc6-a0e9ac1dda7d
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (ec1e61ab-1815-4ea3-bde1-9ba5291910fa)
 Call ID: ec1e61ab-1815-4ea3-bde1-9ba5291910fa
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Person
  AssignClass (dcc1567c-1b25-4760-83b2-aba19bf9a0fd)
 Call ID: dcc1567c-1b25-4760-83b2-aba19bf9a0fd
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (291177fe-190e-4e57-bb8e-6e7d9f5ea867)
 Call ID: 291177fe-190e-4e57-bb8e-6e7d9f5ea867
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (86e0dc5c-887e-445d-8732-8504006a4881)
 Call ID: 86e0dc5c-887e-445d-8732-8504006a4881
  Args:
    type: :Woman
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (89417b75-0b5a-4734-97f7-da30a1997699)
 Call ID: 89417b75-0b5a-4734-97f7-da30a1997699
  Args:
    type: :Person
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (86bf26a7-87c1-46ab-a745-36e6af234cb4)
 Call ID: 86bf26a7-87c1-46ab-a745-36e6af234cb4
  Args:
    type: :Man
    source: Wilhelm_brother
  AssignClass (15fdb178-0cc7-44c2-982f-786eb5e87b4f)
 Call ID: 15fdb178-0cc7-44c2-982f-786eb5e87b4f
  Args:
    type: :Person
    source: Wilhelm_brother
  AssignClass (041155b9-f7e5-48fc-9a08-4d2c02a631a5)
 Call ID: 041155b9-f7e5-48fc-9a08-4d2c02a631a5
  Args:
    type: :Man
    source: Louis_Ferdinand_brother
  AssignClass (4a565828-8ee3-4ccb-84bd-9bab9bc20c8f)
 Call ID: 4a565828-8ee3-4ccb-84bd-9bab9bc20c8f
  Args:
    type: :Person
    source: Louis_Ferdinand_brother
  AssignClass (2feb2979-be94-48c1-925b-61b937f60fe9)
 Call ID: 2feb2979-be94-48c1-925b-61b937f60fe9
  Args:
    source: Hubertus_brother
    type: :Man
  AssignClass (03bf37fd-1838-4928-817f-9ae8b474c8d3)
 Call ID: 03bf37fd-1838-4928-817f-9ae8b474c8d3
  Args:
    source: Hubertus_brother
    type: :Person
  AssignClass (3fd7840e-0030-40c9-9b5e-82f30bc95e24)
 Call ID: 3fd7840e-0030-40c9-9b5e-82f30bc95e24
  Args:
    source: Frederick_brother
    type: :Man
  AssignClass (a4d85e4e-9345-4e05-b880-fb38b17e3164)
 Call ID: a4d85e4e-9345-4e05-b880-fb38b17e3164
  Args:
    source: Frederick_brother
    type: :Person
  AssignClass (5edb7910-f3b6-412f-bcb4-d129c80ce71f)
 Call ID: 5edb7910-f3b6-412f-bcb4-d129c80ce71f
  Args:
    type: :Woman
    source: Cecilie_sister
  AssignClass (9cd84950-8521-4087-8a72-369e268bb5b1)
 Call ID: 9cd84950-8521-4087-8a72-369e268bb5b1
  Args:
    source: Cecilie_sister
    type: :Person
  AddTriple (33d8a28d-a77d-4d8c-bea1-ed267a13cff8)
 Call ID: 33d8a28d-a77d-4d8c-bea1-ed267a13cff8
  Args:
    relation: :isSiblingOf
    source: Alexandrine_of_Prussia
    target: Wilhelm_brother
  AddTriple (ca597c3d-cc90-4c66-a196-334ce86e10f4)
 Call ID: ca597c3d-cc90-4c66-a196-334ce86e10f4
  Args:
    relation: :isSiblingOf
    target: Louis_Ferdinand_brother
    source: Alexandrine_of_Prussia
  AddTriple (8eda8854-3680-40be-a37a-963f4cc7f80c)
 Call ID: 8eda8854-3680-40be-a37a-963f4cc7f80c
  Args:
    source: Alexandrine_of_Prussia
    target: Hubertus_brother
    relation: :isSiblingOf
  AddTriple (5bfd7a0a-3ecb-4f88-b5a3-c003a14ce80b)
 Call ID: 5bfd7a0a-3ecb-4f88-b5a3-c003a14ce80b
  Args:
    source: Alexandrine_of_Prussia
    target: Frederick_brother
    relation: :isSiblingOf
  AddTriple (81382a7b-23a6-40eb-9d58-5de942953643)
 Call ID: 81382a7b-23a6-40eb-9d58-5de942953643
  Args:
    target: Cecilie_sister
    source: Alexandrine_of_Prussia
    relation: :isSiblingOf
  Finish (1a4244a8-e414-4606-8053-cf69f2220ef8)
 Call ID: 1a4244a8-e414-4606-8053-cf69f2220ef8
  Args: