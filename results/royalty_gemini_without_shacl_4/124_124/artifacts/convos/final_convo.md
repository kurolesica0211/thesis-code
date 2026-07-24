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
King Albert IIQueen Paola


Princess Astrid of Belgium, Archduchess of Austria-Este (born 5 June 1962), is the second child and first daughter of King Albert II and Queen Paola, and the younger sister to the current Belgian monarch, King Philippe.
She is married to Prince Lorenz of Belgium, head of the Austria-Este branch of the House of Habsburg-Lorraine, and is fifth in line of succession to the Belgian throne.
Biography

Princess Astrid was born one day before her father's 28th birthday at the Belvédère Château in Laeken, northern Brussels, and was named after her late paternal grandmother, Astrid of Sweden, King Leopold III's popular first wife, who had died in 1935 in a car accident aged 29.
Princess Astrid's godparents were her uncle Fabrizio, Prince Ruffo di Calabria-Santapau, 7th Duke di Guardia Lombarda, and her aunt Hereditary Grand Duchess Joséphine-Charlotte of Luxembourg.
Marriage and issue

Princess Astrid married Archduke Lorenz of Austria-Este, subsequently head of the House of Austria-Este, on 22 September 1984 at the Church of Our Lady of Victories at the Sablon in Brussels.
Lorenz is the eldest son of Robert, Archduke of Austria-Este (1915–1996) and Princess Margherita of Savoy-Aosta (1930–2022).
Princess Astrid and Prince Lorenz have five children:


Royal role

Astrid was formerly President of the Belgian Red Cross, a position which ended on 31 December 2007.
The princess is also a colonel in the Belgian Medical Service of the Belgian Armed Forces.
In April 2015, the Princess took over the Prince Albert Fund from her father King Albert.
Special Envoy

Princess Astrid has been for many years an advocate for landmine survivors rights, participating actively in the work of the Anti-Personnel Mine Ban Convention, also known as the Ottawa Treaty, since Belgium joined in 1998.
In 2013, the Princess was named Special Envoy of the convention, and has promoted the acceptance of a global ban on landmines and promoted the rights of survivors in various UN meetings.



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
  AssignClass (51957715-f7f5-421c-beaa-6ff78b97cd6c)
 Call ID: 51957715-f7f5-421c-beaa-6ff78b97cd6c
  Args:
    type: :Man
    source: Albert_II
  AssignClass (202a478a-4185-4114-b22c-82e6e0fda586)
 Call ID: 202a478a-4185-4114-b22c-82e6e0fda586
  Args:
    type: :Woman
    source: Paola
  AssignClass (87d1fcf9-71ef-4c86-b575-45201be1cac8)
 Call ID: 87d1fcf9-71ef-4c86-b575-45201be1cac8
  Args:
    source: Astrid_of_Belgium
    type: :Woman
  AssignClass (041f9fa9-76b6-4534-9197-a0acd2e87a13)
 Call ID: 041f9fa9-76b6-4534-9197-a0acd2e87a13
  Args:
    source: Philippe
    type: :Man
  AssignClass (9b05e6e6-07de-4f2b-bf61-ca991f4e0ab7)
 Call ID: 9b05e6e6-07de-4f2b-bf61-ca991f4e0ab7
  Args:
    type: :Man
    source: Lorenz_of_Belgium
  AssignClass (4a5fee3c-ac8a-47a8-9cfb-a3fb47ca2b4f)
 Call ID: 4a5fee3c-ac8a-47a8-9cfb-a3fb47ca2b4f
  Args:
    type: :Woman
    source: Astrid_of_Sweden
  AssignClass (5f64146b-cc0d-4a9e-a2df-fa4a581010af)
 Call ID: 5f64146b-cc0d-4a9e-a2df-fa4a581010af
  Args:
    type: :Man
    source: Leopold_III
  AssignClass (db48700f-4669-4825-a4f6-ae8d2a2a7392)
 Call ID: db48700f-4669-4825-a4f6-ae8d2a2a7392
  Args:
    source: Fabrizio_Ruffo_di_Calabria
    type: :Man
  AssignClass (9318c040-f883-4a09-ae6e-a7dd012429d1)
 Call ID: 9318c040-f883-4a09-ae6e-a7dd012429d1
  Args:
    source: Josephine_Charlotte_of_Luxembourg
    type: :Woman
  AssignClass (8bba1f88-343a-4007-94f8-dff068da4192)
 Call ID: 8bba1f88-343a-4007-94f8-dff068da4192
  Args:
    source: Robert_Archduke_of_Austria_Este
    type: :Man
  AssignClass (9955177c-fd4d-43df-b689-5902a608a852)
 Call ID: 9955177c-fd4d-43df-b689-5902a608a852
  Args:
    type: :Woman
    source: Margherita_of_Savoy_Aosta
  AddLiteral (ff5912d7-cbfd-433b-989e-4371e09f5424)
 Call ID: ff5912d7-cbfd-433b-989e-4371e09f5424
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1962
    source: Astrid_of_Belgium
  AddTriple (549e7670-99a2-49b5-9e2f-25440fa75d9c)
 Call ID: 549e7670-99a2-49b5-9e2f-25440fa75d9c
  Args:
    source: Astrid_of_Belgium
    target: Albert_II
    relation: :isDaughterOf
  AddTriple (ad874033-4441-4a3d-a5f2-d03f41609a8b)
 Call ID: ad874033-4441-4a3d-a5f2-d03f41609a8b
  Args:
    source: Astrid_of_Belgium
    relation: :isDaughterOf
    target: Paola
  AddTriple (fed4d02c-03ec-4c24-9ab8-b8213174e0a7)
 Call ID: fed4d02c-03ec-4c24-9ab8-b8213174e0a7
  Args:
    source: Astrid_of_Belgium
    relation: :isSisterOf
    target: Philippe
  AddTriple (18104649-3136-4792-9c34-b7d22a2d3165)
 Call ID: 18104649-3136-4792-9c34-b7d22a2d3165
  Args:
    source: Astrid_of_Belgium
    target: Albert_II
    relation: :hasFather
  AddTriple (7faeb7b0-6a4d-4a83-9564-352d69ce29ae)
 Call ID: 7faeb7b0-6a4d-4a83-9564-352d69ce29ae
  Args:
    relation: :hasMother
    target: Paola
    source: Astrid_of_Belgium
  AddTriple (4ff6b33c-e2f1-4a5e-81b4-31782c884746)
 Call ID: 4ff6b33c-e2f1-4a5e-81b4-31782c884746
  Args:
    source: Albert_II
    relation: :isFatherOf
    target: Astrid_of_Belgium
  AddTriple (b9e8b225-9ce3-4227-a766-952646b637a6)
 Call ID: b9e8b225-9ce3-4227-a766-952646b637a6
  Args:
    source: Paola
    target: Astrid_of_Belgium
    relation: :isMotherOf
  AddTriple (3f2a558f-92ad-4edb-a7ca-d152f3052086)
 Call ID: 3f2a558f-92ad-4edb-a7ca-d152f3052086
  Args:
    target: Philippe
    relation: :isFatherOf
    source: Albert_II
  AddTriple (3d1bad04-d98e-46af-a4a3-adf3cd8fe86b)
 Call ID: 3d1bad04-d98e-46af-a4a3-adf3cd8fe86b
  Args:
    relation: :isMotherOf
    target: Philippe
    source: Paola
  AddLiteral (39ee7fe5-305b-4a04-a84b-1dbf8a49aab2)
 Call ID: 39ee7fe5-305b-4a04-a84b-1dbf8a49aab2
  Args:
    source: Astrid_of_Belgium
    literal_value: 1984
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (5971441d-5347-4bfd-90ac-ffd785e6732a)
 Call ID: 5971441d-5347-4bfd-90ac-ffd785e6732a
  Args:
    source: Astrid_of_Belgium
    relation: :hasRelation
    target: Lorenz_of_Belgium
  AddTriple (8a18ce6a-85aa-481f-93a3-29ef14431419)
 Call ID: 8a18ce6a-85aa-481f-93a3-29ef14431419
  Args:
    target: Robert_Archduke_of_Austria_Este
    relation: :hasFather
    source: Lorenz_of_Belgium
  AddTriple (991fbead-33de-40bd-acb8-baac85722456)
 Call ID: 991fbead-33de-40bd-acb8-baac85722456
  Args:
    relation: :hasMother
    target: Margherita_of_Savoy_Aosta
    source: Lorenz_of_Belgium
  AddLiteral (5d0b50f7-4684-4d05-8b33-900739a7d0a4)
 Call ID: 5d0b50f7-4684-4d05-8b33-900739a7d0a4
  Args:
    source: Robert_Archduke_of_Austria_Este
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1915
  AddLiteral (5b37c6a3-b832-49af-afda-943562b70d0f)
 Call ID: 5b37c6a3-b832-49af-afda-943562b70d0f
  Args:
    source: Robert_Archduke_of_Austria_Este
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AddLiteral (6a62e100-d28a-4e85-9686-a522832e3ef4)
 Call ID: 6a62e100-d28a-4e85-9686-a522832e3ef4
  Args:
    source: Margherita_of_Savoy_Aosta
    literal_value: 1930
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ece746e2-acd5-43a6-a36a-22cc0fcf59c6)
 Call ID: ece746e2-acd5-43a6-a36a-22cc0fcf59c6
  Args:
    source: Margherita_of_Savoy_Aosta
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2022
  AddLiteral (60d186a0-9c9b-412f-9b1d-b2896bbee29d)
 Call ID: 60d186a0-9c9b-412f-9b1d-b2896bbee29d
  Args:
    literal_value: 1935
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Astrid_of_Sweden
  AddTriple (2453ca81-fb63-44f8-871a-9827d72b482f)
 Call ID: 2453ca81-fb63-44f8-871a-9827d72b482f
  Args:
    source: Leopold_III
    target: Albert_II
    relation: :isFatherOf
  Finish (1026cc37-0b7b-4864-b9a3-50f12bff1f3c)
 Call ID: 1026cc37-0b7b-4864-b9a3-50f12bff1f3c
  Args: