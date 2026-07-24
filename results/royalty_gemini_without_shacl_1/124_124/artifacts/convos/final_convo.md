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
  AssignClass (b4493bfb-b789-44d6-9544-93aab2b5ed7d)
 Call ID: b4493bfb-b789-44d6-9544-93aab2b5ed7d
  Args:
    type: :Woman
    source: :PrincessAstrid
  AssignClass (f5fe1cd3-1a00-4131-8628-4e73666f7a85)
 Call ID: f5fe1cd3-1a00-4131-8628-4e73666f7a85
  Args:
    source: :PrincessAstrid
    type: :Person
  AssignClass (6e898e38-7e55-4233-adf3-34c342caea6a)
 Call ID: 6e898e38-7e55-4233-adf3-34c342caea6a
  Args:
    type: :Man
    source: :KingAlbertII
  AssignClass (4ac7e28f-b276-463d-9258-1c05c16ce4aa)
 Call ID: 4ac7e28f-b276-463d-9258-1c05c16ce4aa
  Args:
    type: :Person
    source: :KingAlbertII
  AssignClass (e8b8f867-c325-4946-9f79-1780b5335b43)
 Call ID: e8b8f867-c325-4946-9f79-1780b5335b43
  Args:
    type: :Woman
    source: :QueenPaola
  AssignClass (32cea140-e133-4e78-8d13-345574bc04dd)
 Call ID: 32cea140-e133-4e78-8d13-345574bc04dd
  Args:
    source: :QueenPaola
    type: :Person
  AssignClass (600d41d0-1bcc-42e7-97ad-0f1c1d0bdcbc)
 Call ID: 600d41d0-1bcc-42e7-97ad-0f1c1d0bdcbc
  Args:
    type: :Man
    source: :KingPhilippe
  AssignClass (5951cdfb-9e15-40a6-a14d-fbb212d40ede)
 Call ID: 5951cdfb-9e15-40a6-a14d-fbb212d40ede
  Args:
    source: :KingPhilippe
    type: :Person
  AssignClass (f9a199e9-01b2-4a5d-8e28-56a1e1b4d260)
 Call ID: f9a199e9-01b2-4a5d-8e28-56a1e1b4d260
  Args:
    source: :PrinceLorenz
    type: :Man
  AssignClass (c5326a6a-2968-445f-9332-7647b241cfaf)
 Call ID: c5326a6a-2968-445f-9332-7647b241cfaf
  Args:
    type: :Person
    source: :PrinceLorenz
  AssignClass (876210a7-eb45-4dbc-a7d7-ca1573a9b8ce)
 Call ID: 876210a7-eb45-4dbc-a7d7-ca1573a9b8ce
  Args:
    source: :AstridOfSweden
    type: :Woman
  AssignClass (de6f7b8a-dc03-44d3-bde6-5e3a3b7bc9dd)
 Call ID: de6f7b8a-dc03-44d3-bde6-5e3a3b7bc9dd
  Args:
    source: :AstridOfSweden
    type: :Person
  AssignClass (0250cae6-432a-474b-a540-aa17ac8cc00d)
 Call ID: 0250cae6-432a-474b-a540-aa17ac8cc00d
  Args:
    source: :KingLeopoldIII
    type: :Man
  AssignClass (30130c5d-04ac-4d3c-8db4-9721a1ef8350)
 Call ID: 30130c5d-04ac-4d3c-8db4-9721a1ef8350
  Args:
    source: :KingLeopoldIII
    type: :Person
  AssignClass (c1111c26-8fd5-4261-8da6-a870bf9b6bf9)
 Call ID: c1111c26-8fd5-4261-8da6-a870bf9b6bf9
  Args:
    type: :Man
    source: :FabrizioPrinceRuffoDiCalabriaSantapau
  AssignClass (dc3fce41-8ca3-46e2-9aac-995bc81235ff)
 Call ID: dc3fce41-8ca3-46e2-9aac-995bc81235ff
  Args:
    type: :Person
    source: :FabrizioPrinceRuffoDiCalabriaSantapau
  AssignClass (6db96b61-4737-49f9-bca2-6be134b8d1c6)
 Call ID: 6db96b61-4737-49f9-bca2-6be134b8d1c6
  Args:
    source: :HereditaryGrandDuchessJosephineCharlotteOfLuxembourg
    type: :Woman
  AssignClass (35244347-616c-488b-a5f0-5cd534baea3b)
 Call ID: 35244347-616c-488b-a5f0-5cd534baea3b
  Args:
    source: :HereditaryGrandDuchessJosephineCharlotteOfLuxembourg
    type: :Person
  AssignClass (1df37dcc-c330-4562-9627-6c7850764394)
 Call ID: 1df37dcc-c330-4562-9627-6c7850764394
  Args:
    source: :ArchdukeRobertOfAustriaEste
    type: :Man
  AssignClass (c4f815bd-b406-4c34-b002-ec59bd035795)
 Call ID: c4f815bd-b406-4c34-b002-ec59bd035795
  Args:
    source: :ArchdukeRobertOfAustriaEste
    type: :Person
  AssignClass (595012a6-dfb4-4ab9-a00c-a9a3e27522b9)
 Call ID: 595012a6-dfb4-4ab9-a00c-a9a3e27522b9
  Args:
    type: :Woman
    source: :PrincessMargheritaOfSavoyAosta
  AssignClass (2a43f318-8a6e-408f-8490-d0228385f6f1)
 Call ID: 2a43f318-8a6e-408f-8490-d0228385f6f1
  Args:
    type: :Person
    source: :PrincessMargheritaOfSavoyAosta
  AddLiteral (58626f5d-206f-4c58-879d-a2329db3b944)
 Call ID: 58626f5d-206f-4c58-879d-a2329db3b944
  Args:
    source: :PrincessAstrid
    literal_type: xsd:integer
    literal_value: 1962
    relation: :hasBirthYear
  AddLiteral (1e46056c-e45a-4ab5-bea0-2866be44163b)
 Call ID: 1e46056c-e45a-4ab5-bea0-2866be44163b
  Args:
    relation: :hasDeathYear
    literal_value: 1935
    literal_type: xsd:integer
    source: :AstridOfSweden
  AddLiteral (26afaeff-0e0e-4a3f-9bb0-7209c2d9710b)
 Call ID: 26afaeff-0e0e-4a3f-9bb0-7209c2d9710b
  Args:
    relation: :hasMarriageYear
    literal_value: 1984
    literal_type: xsd:integer
    source: :PrincessAstrid
  AddLiteral (451e20a4-d0b3-4e85-94da-2a0bc1735029)
 Call ID: 451e20a4-d0b3-4e85-94da-2a0bc1735029
  Args:
    source: :ArchdukeRobertOfAustriaEste
    literal_type: xsd:integer
    literal_value: 1915
    relation: :hasBirthYear
  AddLiteral (569a1c8c-5d31-4691-9cb0-a01e196cfabf)
 Call ID: 569a1c8c-5d31-4691-9cb0-a01e196cfabf
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
    source: :ArchdukeRobertOfAustriaEste
  AddLiteral (250b9a4a-eaf3-4a97-8e8e-ed033a91ed65)
 Call ID: 250b9a4a-eaf3-4a97-8e8e-ed033a91ed65
  Args:
    source: :PrincessMargheritaOfSavoyAosta
    relation: :hasBirthYear
    literal_value: 1930
    literal_type: xsd:integer
  AddLiteral (7b642517-f532-4951-91a8-e390d5b72b4e)
 Call ID: 7b642517-f532-4951-91a8-e390d5b72b4e
  Args:
    source: :PrincessMargheritaOfSavoyAosta
    literal_type: xsd:integer
    literal_value: 2022
    relation: :hasDeathYear
  AddTriple (dda02a61-eec8-4518-9810-01c176d8e5ab)
 Call ID: dda02a61-eec8-4518-9810-01c176d8e5ab
  Args:
    relation: :hasFather
    target: :KingAlbertII
    source: :PrincessAstrid
  AddTriple (011cfc6e-bad9-4c3f-a3f3-f2a31f9a7328)
 Call ID: 011cfc6e-bad9-4c3f-a3f3-f2a31f9a7328
  Args:
    target: :QueenPaola
    source: :PrincessAstrid
    relation: :hasMother
  AddTriple (d343cbab-2cd6-4c35-b9ed-1abd665df9f6)
 Call ID: d343cbab-2cd6-4c35-b9ed-1abd665df9f6
  Args:
    relation: :isSisterOf
    target: :KingPhilippe
    source: :PrincessAstrid
  AddTriple (8ea2cef2-235f-4a7f-85a8-53a10da5641e)
 Call ID: 8ea2cef2-235f-4a7f-85a8-53a10da5641e
  Args:
    relation: :hasFather
    source: :KingPhilippe
    target: :KingAlbertII
  AddTriple (63a14ca1-9d74-43ab-9f75-4af45a6832d3)
 Call ID: 63a14ca1-9d74-43ab-9f75-4af45a6832d3
  Args:
    target: :QueenPaola
    source: :KingPhilippe
    relation: :hasMother
  AddTriple (e4f0cbe1-6722-4245-b0f4-d599328cf54f)
 Call ID: e4f0cbe1-6722-4245-b0f4-d599328cf54f
  Args:
    target: :KingAlbertII
    source: :KingLeopoldIII
    relation: :isFatherOf
  AddTriple (de6ef0bc-16b1-4592-9dfd-f35aac652900)
 Call ID: de6ef0bc-16b1-4592-9dfd-f35aac652900
  Args:
    target: :KingAlbertII
    source: :AstridOfSweden
    relation: :isMotherOf
  AddTriple (c163dd12-90fc-467e-89f6-368404c9105c)
 Call ID: c163dd12-90fc-467e-89f6-368404c9105c
  Args:
    target: :ArchdukeRobertOfAustriaEste
    source: :PrinceLorenz
    relation: :hasFather
  AddTriple (1fea4521-89bb-4360-8171-13b9a37b45d4)
 Call ID: 1fea4521-89bb-4360-8171-13b9a37b45d4
  Args:
    relation: :hasMother
    target: :PrincessMargheritaOfSavoyAosta
    source: :PrinceLorenz
  Finish (c4bebbd2-2206-4ae5-b887-3389fb215591)
 Call ID: c4bebbd2-2206-4ae5-b887-3389fb215591
  Args: