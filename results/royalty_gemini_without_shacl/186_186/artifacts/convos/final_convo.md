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
Duchess Elisabeth of Mecklenburg-Schwerin (10 August 1869 – 3 September 1955) was a daughter of Frederick Francis II, Grand Duke of Mecklenburg by his third wife Princess Marie of Schwarzburg-Rudolstadt.
By her marriage to Frederick Augustus II, she became the consort of the last reigning Grand Duke of Oldenburg.
Family

Elisabeth was related to many of Europe's royal families.
She was the eldest child of Frederick Francis II, Grand Duke of Mecklenburg by his third wife, Princess Marie of Schwarzburg-Rudolstadt.
She was an older sister of Hendrik, Prince consort of the Netherlands, husband of Queen Wilhelmina of the Netherlands, making her an aunt of Queen Juliana of the Netherlands.
She was also a younger half-sister of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin.
Through Frederick Francis, she was an aunt of Alexandrine, Queen of Denmark and Cecilie, German Crown Princess.
Elisabeth was also a half sister of Marie, Grand Duchess of Russia, who was the mother of Grand Duke Cyril Vladimirovich of Russia, the pretender to the Russian throne.
Her paternal grandparents were Paul Frederick, Grand Duke of Mecklenburg and Princess Alexandrine of Prussia.
Her maternal grandparents were Prince Adolph of Schwarzburg-Rudolstadt and Princess Mathilde of Schönburg-Waldenburg.
Marriage

On 24 October 1896, Elisabeth married Frederick Augustus, Hereditary Grand Duke of Oldenburg.
His first wife Elisabeth Anna had died the previous year, leaving only one surviving daughter: Duchess Sophia Charlotte of Oldenburg.
Frederick Augustus was thus in need of a male heir.
He succeeded as Grand Duke of Oldenburg in 1900, making Elisabeth Grand Duchess consort of Oldenburg.
They had five children:


Frederick was forced to abdicate his throne at the end of World War I, when the former Grand Duchy of the German Empire joined the post-war German Republic.
A year after his abdication, he asked the Oldenburg Diet for a yearly allowance of 150,000 marks, stating that his financial condition was "extremely precarious".
In 1931, Frederick died in Rastede.
Elisabeth died on 3 September 1955, having been widowed for 24 years.



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
  AssignClass (e64d41ae-80c4-42a1-b8d3-98cc64f2debf)
 Call ID: e64d41ae-80c4-42a1-b8d3-98cc64f2debf
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (f878b8a7-b7e0-4cbd-9350-ad8b72e6d5c6)
 Call ID: f878b8a7-b7e0-4cbd-9350-ad8b72e6d5c6
  Args:
    type: :Person
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (e38b0329-57ce-4ae0-bbb3-46920c56ad81)
 Call ID: e38b0329-57ce-4ae0-bbb3-46920c56ad81
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    literal_type: xsd:integer
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (512ce820-fbb2-493b-b921-ef5e7ac18112)
 Call ID: 512ce820-fbb2-493b-b921-ef5e7ac18112
  Args:
    literal_value: 1955
    relation: :hasDeathYear
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AssignClass (ace663c6-7113-469c-9d8d-31cdf2bfb54d)
 Call ID: ace663c6-7113-469c-9d8d-31cdf2bfb54d
  Args:
    source: Frederick_Francis_II
    type: :Man
  AssignClass (af6e9858-ca79-4da2-a120-dbc1f295271b)
 Call ID: af6e9858-ca79-4da2-a120-dbc1f295271b
  Args:
    source: Frederick_Francis_II
    type: :Ancestor
  AssignClass (e6d803b2-f036-4332-81b5-9d6dd1704a13)
 Call ID: e6d803b2-f036-4332-81b5-9d6dd1704a13
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    type: :Woman
  AssignClass (3c854832-ae64-4f86-9546-044ca528e207)
 Call ID: 3c854832-ae64-4f86-9546-044ca528e207
  Args:
    type: :Ancestor
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (7c1372c9-fd5b-4a53-b737-7a8d9a14bf77)
 Call ID: 7c1372c9-fd5b-4a53-b737-7a8d9a14bf77
  Args:
    target: Frederick_Francis_II
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (3653e41a-026c-4779-b920-8872c501b4b2)
 Call ID: 3653e41a-026c-4779-b920-8872c501b4b2
  Args:
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (f720287d-2eb5-4966-b45b-ee90cb471c3a)
 Call ID: f720287d-2eb5-4966-b45b-ee90cb471c3a
  Args:
    type: :Man
    source: Frederick_Augustus_II
  AssignClass (97dfb9c2-9591-4ed6-a352-64bb4de93ee1)
 Call ID: 97dfb9c2-9591-4ed6-a352-64bb4de93ee1
  Args:
    type: :Person
    source: Frederick_Augustus_II
  AddLiteral (d013e457-1203-45f3-b877-a9293b220732)
 Call ID: d013e457-1203-45f3-b877-a9293b220732
  Args:
    literal_type: xsd:integer
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasMarriageYear
    literal_value: 1896
  AddTriple (fe2f365f-7225-4700-beeb-fb59080cc178)
 Call ID: fe2f365f-7225-4700-beeb-fb59080cc178
  Args:
    relation: :hasRelation
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Frederick_Augustus_II
  AssignClass (15526755-85e8-4130-aa0d-ff7d5f7a4c0f)
 Call ID: 15526755-85e8-4130-aa0d-ff7d5f7a4c0f
  Args:
    type: :Man
    source: Hendrik_Prince_Consort_of_the_Netherlands
  AssignClass (97a55cfd-d3d0-4478-8156-c12f75e9b766)
 Call ID: 97a55cfd-d3d0-4478-8156-c12f75e9b766
  Args:
    type: :Person
    source: Hendrik_Prince_Consort_of_the_Netherlands
  AddTriple (a6114eb8-6705-47fe-a5a1-a17b84626ba8)
 Call ID: a6114eb8-6705-47fe-a5a1-a17b84626ba8
  Args:
    relation: :isSisterOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Hendrik_Prince_Consort_of_the_Netherlands
  AssignClass (29867c0a-a52c-4d0d-90f2-e83748d70d41)
 Call ID: 29867c0a-a52c-4d0d-90f2-e83748d70d41
  Args:
    source: Queen_Wilhelmina_of_the_Netherlands
    type: :Woman
  AssignClass (13b6d28f-c1e9-4edd-a401-c96406592217)
 Call ID: 13b6d28f-c1e9-4edd-a401-c96406592217
  Args:
    type: :Person
    source: Queen_Wilhelmina_of_the_Netherlands
  AddTriple (6e8288fc-7ca9-4630-92b1-2f52ddb531c8)
 Call ID: 6e8288fc-7ca9-4630-92b1-2f52ddb531c8
  Args:
    relation: :hasRelation
    target: Queen_Wilhelmina_of_the_Netherlands
    source: Hendrik_Prince_Consort_of_the_Netherlands
  AssignClass (e2801af1-4c49-48e0-b20d-c2fac366d008)
 Call ID: e2801af1-4c49-48e0-b20d-c2fac366d008
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (87ac3938-37ad-4045-a8e8-17c54e4d2e00)
 Call ID: 87ac3938-37ad-4045-a8e8-17c54e4d2e00
  Args:
    type: :Person
    source: Queen_Juliana_of_the_Netherlands
  AddTriple (d5fd21be-67eb-4cac-95e1-45e3f17024b1)
 Call ID: d5fd21be-67eb-4cac-95e1-45e3f17024b1
  Args:
    target: Queen_Juliana_of_the_Netherlands
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isAuntOf
  AssignClass (331a194e-f5cc-4e82-be84-05b2cb3622f4)
 Call ID: 331a194e-f5cc-4e82-be84-05b2cb3622f4
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (dbed8925-4304-4293-9a73-08258e49aa88)
 Call ID: dbed8925-4304-4293-9a73-08258e49aa88
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (49e4939d-4a31-47cc-af8e-c4b92457801d)
 Call ID: 49e4939d-4a31-47cc-af8e-c4b92457801d
  Args:
    relation: :isSiblingOf
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (0d8c509b-b2cc-446b-8d5e-9e9710250622)
 Call ID: 0d8c509b-b2cc-446b-8d5e-9e9710250622
  Args:
    type: :Woman
    source: Alexandrine_Queen_of_Denmark
  AssignClass (accefa21-3b52-457c-b376-d88b4a2aaa77)
 Call ID: accefa21-3b52-457c-b376-d88b4a2aaa77
  Args:
    type: :Person
    source: Alexandrine_Queen_of_Denmark
  AddTriple (4b7f089e-7a32-44e9-8dbb-0c3d090b55ce)
 Call ID: 4b7f089e-7a32-44e9-8dbb-0c3d090b55ce
  Args:
    relation: :isAuntOf
    target: Alexandrine_Queen_of_Denmark
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (07db8b56-c82d-4fa9-bb80-fe2371ffe518)
 Call ID: 07db8b56-c82d-4fa9-bb80-fe2371ffe518
  Args:
    source: Cecilie_German_Crown_Princess
    type: :Woman
  AssignClass (62e91fed-e4a8-46e8-a929-f4c3cc76dbde)
 Call ID: 62e91fed-e4a8-46e8-a929-f4c3cc76dbde
  Args:
    type: :Person
    source: Cecilie_German_Crown_Princess
  AddTriple (1f12169e-4969-4cf8-ab20-b7c7905545c2)
 Call ID: 1f12169e-4969-4cf8-ab20-b7c7905545c2
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Cecilie_German_Crown_Princess
  AssignClass (c66d52de-7d87-47f2-8201-82a0e9973024)
 Call ID: c66d52de-7d87-47f2-8201-82a0e9973024
  Args:
    source: Marie_Grand_Duchess_of_Russia
    type: :Woman
  AssignClass (6db001d7-6e25-461d-ad32-e3eeb37a2b37)
 Call ID: 6db001d7-6e25-461d-ad32-e3eeb37a2b37
  Args:
    type: :Person
    source: Marie_Grand_Duchess_of_Russia
  AddTriple (50c82d60-98df-45c4-885f-b4aec7da6f3c)
 Call ID: 50c82d60-98df-45c4-885f-b4aec7da6f3c
  Args:
    relation: :isSiblingOf
    target: Marie_Grand_Duchess_of_Russia
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (ba24008d-eb8b-45aa-91a1-ea3b4fcff959)
 Call ID: ba24008d-eb8b-45aa-91a1-ea3b4fcff959
  Args:
    type: :Man
    source: Grand_Duke_Cyril_Vladimirovich_of_Russia
  AssignClass (6f6a1f91-9d51-4471-b7fd-76db73f33655)
 Call ID: 6f6a1f91-9d51-4471-b7fd-76db73f33655
  Args:
    source: Grand_Duke_Cyril_Vladimirovich_of_Russia
    type: :Person
  AddTriple (4a423bea-ce72-44f0-8955-db9367d22674)
 Call ID: 4a423bea-ce72-44f0-8955-db9367d22674
  Args:
    relation: :hasMother
    target: Marie_Grand_Duchess_of_Russia
    source: Grand_Duke_Cyril_Vladimirovich_of_Russia
  AssignClass (cc7cdfe0-c77b-4604-9468-602d02f59152)
 Call ID: cc7cdfe0-c77b-4604-9468-602d02f59152
  Args:
    source: Paul_Frederick_Grand_Duke_of_Mecklenburg
    type: :Man
  AssignClass (b6a8a0b7-7f02-4abe-8391-d2520dc5d5e3)
 Call ID: b6a8a0b7-7f02-4abe-8391-d2520dc5d5e3
  Args:
    type: :Ancestor
    source: Paul_Frederick_Grand_Duke_of_Mecklenburg
  AssignClass (8b68078b-cf3d-41e0-a252-52e48487b909)
 Call ID: 8b68078b-cf3d-41e0-a252-52e48487b909
  Args:
    type: :Woman
    source: Princess_Alexandrine_of_Prussia
  AssignClass (5170b088-0aac-42f9-aa66-addcfa350e29)
 Call ID: 5170b088-0aac-42f9-aa66-addcfa350e29
  Args:
    type: :Ancestor
    source: Princess_Alexandrine_of_Prussia
  AddTriple (6b38c677-4706-463c-8283-26243810774a)
 Call ID: 6b38c677-4706-463c-8283-26243810774a
  Args:
    source: Frederick_Francis_II
    target: Paul_Frederick_Grand_Duke_of_Mecklenburg
    relation: :hasFather
  AddTriple (08e0d54d-b8d0-4a26-b424-a0793bdae17d)
 Call ID: 08e0d54d-b8d0-4a26-b424-a0793bdae17d
  Args:
    source: Frederick_Francis_II
    target: Princess_Alexandrine_of_Prussia
    relation: :hasMother
  AssignClass (db9addbf-fb17-4e15-8330-df47f9c76ceb)
 Call ID: db9addbf-fb17-4e15-8330-df47f9c76ceb
  Args:
    type: :Man
    source: Prince_Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (fde07818-af64-4350-a98d-00aae291ae48)
 Call ID: fde07818-af64-4350-a98d-00aae291ae48
  Args:
    type: :Ancestor
    source: Prince_Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (da33a5bc-6f72-4465-b918-e89e3c4d5f36)
 Call ID: da33a5bc-6f72-4465-b918-e89e3c4d5f36
  Args:
    type: :Woman
    source: Princess_Mathilde_of_Schönburg-Waldenburg
  AssignClass (63b3068b-26ca-49fe-aad3-483ad615fe56)
 Call ID: 63b3068b-26ca-49fe-aad3-483ad615fe56
  Args:
    type: :Ancestor
    source: Princess_Mathilde_of_Schönburg-Waldenburg
  AddTriple (d3f44d6e-e37b-4c7c-a96c-5d699f898f08)
 Call ID: d3f44d6e-e37b-4c7c-a96c-5d699f898f08
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    target: Prince_Adolph_of_Schwarzburg-Rudolstadt
    relation: :hasFather
  AddTriple (fc16434c-a9cf-42d2-aabd-3b22280ca1ab)
 Call ID: fc16434c-a9cf-42d2-aabd-3b22280ca1ab
  Args:
    relation: :hasMother
    source: Marie_of_Schwarzburg-Rudolstadt
    target: Princess_Mathilde_of_Schönburg-Waldenburg
  AssignClass (a1bd1ee1-d5f3-4a7e-8b1b-2a4bf910f207)
 Call ID: a1bd1ee1-d5f3-4a7e-8b1b-2a4bf910f207
  Args:
    source: Elisabeth_Anna
    type: :Woman
  AssignClass (7ab7a24a-f965-471c-bb1d-d0c2803a5314)
 Call ID: 7ab7a24a-f965-471c-bb1d-d0c2803a5314
  Args:
    source: Elisabeth_Anna
    type: :Ancestor
  AddTriple (a553d728-1593-423f-ac22-a299307fdd0c)
 Call ID: a553d728-1593-423f-ac22-a299307fdd0c
  Args:
    relation: :hasRelation
    source: Frederick_Augustus_II
    target: Elisabeth_Anna
  AssignClass (85c89322-8ddc-4a33-b52a-5e575a4261d8)
 Call ID: 85c89322-8ddc-4a33-b52a-5e575a4261d8
  Args:
    source: Duchess_Sophia_Charlotte_of_Oldenburg
    type: :Woman
  AssignClass (ddff7c25-528d-46f5-b03e-856e16cdb0b9)
 Call ID: ddff7c25-528d-46f5-b03e-856e16cdb0b9
  Args:
    type: :Person
    source: Duchess_Sophia_Charlotte_of_Oldenburg
  AddTriple (388ec372-5003-406d-8930-51fcc54a38db)
 Call ID: 388ec372-5003-406d-8930-51fcc54a38db
  Args:
    relation: :hasMother
    target: Elisabeth_Anna
    source: Duchess_Sophia_Charlotte_of_Oldenburg
  AddTriple (0aa260ee-be75-426d-80f0-104ce50b36d3)
 Call ID: 0aa260ee-be75-426d-80f0-104ce50b36d3
  Args:
    relation: :hasFather
    target: Frederick_Augustus_II
    source: Duchess_Sophia_Charlotte_of_Oldenburg
  AddLiteral (3c9d9d37-0572-4c23-b190-519678d054c5)
 Call ID: 3c9d9d37-0572-4c23-b190-519678d054c5
  Args:
    literal_type: xsd:integer
    source: Frederick_Augustus_II
    relation: :hasDeathYear
    literal_value: 1931
  Finish (1ac3fca9-af9c-4730-b047-13390ae23adb)
 Call ID: 1ac3fca9-af9c-4730-b047-13390ae23adb
  Args: