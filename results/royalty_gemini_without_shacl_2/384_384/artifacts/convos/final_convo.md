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
Moritz, Landgrave of Hesse (legally Moritz Friedrich Karl Emanuel Humbert Prinz und Landgraf von Hessen; 6 August 1926 – 23 May 2013) was the son of Prince Philip, Landgrave of Hesse, and the head of the House of Hesse, also known as the House of Brabant.
Life

Landgrave Moritz was born at Racconigi Castle, in Italy.
During the Second World War, Moritz's mother, Princess Mafalda of Savoy, was arrested by the Nazis for alleged subversive activities and died in the Buchenwald concentration camp in 1944 as a result of a U.S. bombing raid on the camp.
Moritz and his siblings (Heinrich, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their uncle Louis, Prince of Hesse and by Rhine and aunt Margaret Campbell Geddes who adopted them.
Prince Louis of Hesse and by Rhine, the last head of the Hesse-Darmstadt line, died in 1968, at which time Moritz's father succeeded him as head of the entire house.
Moritz became the head of the House of Hesse after the death of his father Philip on 25 October 1980.
Moritz was a world-famous art collector.
He presided over the Foundation of the House of Hesse which is the proprietor of the Kronberg Palace Hotel and several manor estates and palaces.
Marriage and children

Moritz married Princess Tatiana of Sayn-Wittgenstein-Berleburg, daughter of Prince Gustav Albrecht.



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
  AssignClass (75728381-0510-4e92-8fd4-4373c9dfa49c)
 Call ID: 75728381-0510-4e92-8fd4-4373c9dfa49c
  Args:
    type: :Man
    source: Moritz
  AssignClass (04834acb-df31-4086-81c6-0761913c68db)
 Call ID: 04834acb-df31-4086-81c6-0761913c68db
  Args:
    source: Moritz
    type: :Person
  AddLiteral (23026044-1f14-456d-ae24-c877548339f9)
 Call ID: 23026044-1f14-456d-ae24-c877548339f9
  Args:
    relation: :hasBirthYear
    literal_value: 1926
    literal_type: xsd:integer
    source: Moritz
  AddLiteral (69117147-fecf-4fb5-83ef-837c35d947c3)
 Call ID: 69117147-fecf-4fb5-83ef-837c35d947c3
  Args:
    relation: :hasDeathYear
    literal_value: 2013
    literal_type: xsd:integer
    source: Moritz
  AssignClass (078ee959-0cbd-4d78-ab20-3f0545d30be5)
 Call ID: 078ee959-0cbd-4d78-ab20-3f0545d30be5
  Args:
    source: Philip
    type: :Man
  AssignClass (c1085cce-d0e5-4394-9efd-1dce53065b30)
 Call ID: c1085cce-d0e5-4394-9efd-1dce53065b30
  Args:
    type: :Person
    source: Philip
  AddTriple (83ba272e-6d09-46b0-8ca6-4b6608361c31)
 Call ID: 83ba272e-6d09-46b0-8ca6-4b6608361c31
  Args:
    source: Moritz
    relation: :hasFather
    target: Philip
  AssignClass (eabdc9e2-ee92-4dac-8eed-7536c8d1a43c)
 Call ID: eabdc9e2-ee92-4dac-8eed-7536c8d1a43c
  Args:
    type: :Woman
    source: Mafalda_of_Savoy
  AssignClass (5e73e122-ff00-4c3f-8087-59bc25b0b465)
 Call ID: 5e73e122-ff00-4c3f-8087-59bc25b0b465
  Args:
    source: Mafalda_of_Savoy
    type: :Person
  AddTriple (e5f3fa9d-aaff-4ef0-adc4-9048336d0d72)
 Call ID: e5f3fa9d-aaff-4ef0-adc4-9048336d0d72
  Args:
    source: Moritz
    relation: :hasMother
    target: Mafalda_of_Savoy
  AssignClass (44d7b8ef-0862-40db-9d15-33983b44a452)
 Call ID: 44d7b8ef-0862-40db-9d15-33983b44a452
  Args:
    type: :Man
    source: Heinrich
  AssignClass (7b8a48ee-22f5-4af0-b394-dd126f27c2f7)
 Call ID: 7b8a48ee-22f5-4af0-b394-dd126f27c2f7
  Args:
    type: :Person
    source: Heinrich
  AssignClass (e1ea3da6-c80a-40fc-a131-7cf95d57e615)
 Call ID: e1ea3da6-c80a-40fc-a131-7cf95d57e615
  Args:
    type: :Man
    source: Otto
  AssignClass (392f3a9d-a9f4-4e8d-92f6-686c909fff99)
 Call ID: 392f3a9d-a9f4-4e8d-92f6-686c909fff99
  Args:
    type: :Person
    source: Otto
  AssignClass (3696920e-02fb-4ea2-b20a-54322c38920e)
 Call ID: 3696920e-02fb-4ea2-b20a-54322c38920e
  Args:
    source: Elisabeth
    type: :Woman
  AssignClass (0de5ffbb-7b71-4c73-a34e-be6966908c6b)
 Call ID: 0de5ffbb-7b71-4c73-a34e-be6966908c6b
  Args:
    source: Elisabeth
    type: :Person
  AddTriple (ebd53d7c-56d3-4f7d-bed9-68c1929b6e14)
 Call ID: ebd53d7c-56d3-4f7d-bed9-68c1929b6e14
  Args:
    relation: :isSiblingOf
    target: Heinrich
    source: Moritz
  AddTriple (93a3203a-42ad-4fbf-9e8a-0e6014843dc0)
 Call ID: 93a3203a-42ad-4fbf-9e8a-0e6014843dc0
  Args:
    target: Otto
    relation: :isSiblingOf
    source: Moritz
  AddTriple (f9ae1d79-f1b8-40b8-a58b-bd2a2099c93b)
 Call ID: f9ae1d79-f1b8-40b8-a58b-bd2a2099c93b
  Args:
    source: Moritz
    target: Elisabeth
    relation: :isSiblingOf
  AssignClass (dbd5b8c4-8d49-46f2-a867-df2bf09e7ebe)
 Call ID: dbd5b8c4-8d49-46f2-a867-df2bf09e7ebe
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (37db12e3-7eb0-490a-bf98-632fc8c96182)
 Call ID: 37db12e3-7eb0-490a-bf98-632fc8c96182
  Args:
    type: :Person
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (d0aa95ee-d760-4a78-86d4-b14a5756a6fd)
 Call ID: d0aa95ee-d760-4a78-86d4-b14a5756a6fd
  Args:
    type: :Woman
    source: Margaret_Campbell_Geddes
  AssignClass (752cfb30-97d3-4228-b109-2c658c7adf02)
 Call ID: 752cfb30-97d3-4228-b109-2c658c7adf02
  Args:
    source: Margaret_Campbell_Geddes
    type: :Person
  AssignClass (79343869-5216-45de-9af2-1f60c7de3032)
 Call ID: 79343869-5216-45de-9af2-1f60c7de3032
  Args:
    type: :Woman
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
  AssignClass (e4ff5c52-1770-43cd-95ac-724febf30ecc)
 Call ID: e4ff5c52-1770-43cd-95ac-724febf30ecc
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (2ba31637-162d-4098-be20-9e7ce8cdfd9f)
 Call ID: 2ba31637-162d-4098-be20-9e7ce8cdfd9f
  Args:
    relation: :hasRelation
    target: Tatiana_of_Sayn-Wittgenstein-Berleburg
    source: Moritz
  AssignClass (40a75378-f551-40b5-ac27-be17175fe07c)
 Call ID: 40a75378-f551-40b5-ac27-be17175fe07c
  Args:
    type: :Man
    source: Gustav_Albrecht
  AssignClass (ff2a8e22-f484-48a9-9d60-b02fed21a624)
 Call ID: ff2a8e22-f484-48a9-9d60-b02fed21a624
  Args:
    source: Gustav_Albrecht
    type: :Person
  AddTriple (78501822-5354-426b-bb60-15fc9e50dcc6)
 Call ID: 78501822-5354-426b-bb60-15fc9e50dcc6
  Args:
    target: Gustav_Albrecht
    relation: :hasFather
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
  Finish (22237f99-78b9-4b95-a41f-ffa4bf2a470b)
 Call ID: 22237f99-78b9-4b95-a41f-ffa4bf2a470b
  Args: