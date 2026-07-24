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
  AssignClass (651e3c26-1f6b-4b5e-be59-92a9ad1197f2)
 Call ID: 651e3c26-1f6b-4b5e-be59-92a9ad1197f2
  Args:
    type: :Woman
    source: :Princess_Astrid_of_Belgium
  AssignClass (20286c41-79a0-4ec5-b1bc-ebfde09e8806)
 Call ID: 20286c41-79a0-4ec5-b1bc-ebfde09e8806
  Args:
    source: :Princess_Astrid_of_Belgium
    type: :Person
  AssignClass (5d533b05-b532-4af0-94db-a4eb1c6422a1)
 Call ID: 5d533b05-b532-4af0-94db-a4eb1c6422a1
  Args:
    type: :Man
    source: :King_Albert_II
  AssignClass (3bc8b44e-cf40-4d74-82bd-f7ce19bcd7eb)
 Call ID: 3bc8b44e-cf40-4d74-82bd-f7ce19bcd7eb
  Args:
    type: :Person
    source: :King_Albert_II
  AssignClass (ef694689-fd8f-4cee-829e-0cde12878364)
 Call ID: ef694689-fd8f-4cee-829e-0cde12878364
  Args:
    type: :Ancestor
    source: :King_Albert_II
  AssignClass (29cb71c3-d16f-4411-8eb9-a479d3917182)
 Call ID: 29cb71c3-d16f-4411-8eb9-a479d3917182
  Args:
    type: :Woman
    source: :Queen_Paola
  AssignClass (3a650061-7174-49be-bab4-f56a6b33b8f0)
 Call ID: 3a650061-7174-49be-bab4-f56a6b33b8f0
  Args:
    source: :Queen_Paola
    type: :Person
  AssignClass (ea6e1360-9581-4cd2-9fd3-6b7b6f711aa5)
 Call ID: ea6e1360-9581-4cd2-9fd3-6b7b6f711aa5
  Args:
    source: :Queen_Paola
    type: :Ancestor
  AssignClass (d4467fe4-0455-4c89-880a-4dfa73557d46)
 Call ID: d4467fe4-0455-4c89-880a-4dfa73557d46
  Args:
    source: :King_Philippe
    type: :Man
  AssignClass (db26cc6e-e5b5-4cdd-9d8c-1dffe4fefa6f)
 Call ID: db26cc6e-e5b5-4cdd-9d8c-1dffe4fefa6f
  Args:
    type: :Person
    source: :King_Philippe
  AssignClass (fbd32d2b-901f-4357-945e-3ca90be8d60f)
 Call ID: fbd32d2b-901f-4357-945e-3ca90be8d60f
  Args:
    type: :Man
    source: :Prince_Lorenz_of_Belgium
  AssignClass (1f34b81e-1d85-4733-9c8d-1a0644ccc70a)
 Call ID: 1f34b81e-1d85-4733-9c8d-1a0644ccc70a
  Args:
    source: :Prince_Lorenz_of_Belgium
    type: :Person
  AssignClass (1ae71470-c847-4471-be77-9ef91c225a57)
 Call ID: 1ae71470-c847-4471-be77-9ef91c225a57
  Args:
    source: :Astrid_of_Sweden
    type: :Woman
  AssignClass (bfb16cc5-4528-4c85-92fb-7e8adce260fc)
 Call ID: bfb16cc5-4528-4c85-92fb-7e8adce260fc
  Args:
    source: :Astrid_of_Sweden
    type: :Person
  AssignClass (2dea5472-ffa9-407a-8a20-a4ed0f4e0070)
 Call ID: 2dea5472-ffa9-407a-8a20-a4ed0f4e0070
  Args:
    type: :Ancestor
    source: :Astrid_of_Sweden
  AssignClass (81c888f2-ef19-4276-a6f9-13c10141e380)
 Call ID: 81c888f2-ef19-4276-a6f9-13c10141e380
  Args:
    type: :Man
    source: :King_Leopold_III
  AssignClass (95a3ec84-5c75-4ff9-b3ca-86bd9a5610f5)
 Call ID: 95a3ec84-5c75-4ff9-b3ca-86bd9a5610f5
  Args:
    source: :King_Leopold_III
    type: :Person
  AssignClass (27472fb4-e350-4228-9d0a-9e7990ebc24f)
 Call ID: 27472fb4-e350-4228-9d0a-9e7990ebc24f
  Args:
    type: :Ancestor
    source: :King_Leopold_III
  AssignClass (9b9b7263-3c10-4fbe-b005-77f1876f7498)
 Call ID: 9b9b7263-3c10-4fbe-b005-77f1876f7498
  Args:
    type: :Man
    source: :Fabrizio_Prince_Ruffo_di_Calabria_Santapau
  AssignClass (f1489546-078c-463a-8902-67dbcf9b1549)
 Call ID: f1489546-078c-463a-8902-67dbcf9b1549
  Args:
    type: :Person
    source: :Fabrizio_Prince_Ruffo_di_Calabria_Santapau
  AssignClass (e450241d-b77f-4fe2-9deb-fd096beccb8e)
 Call ID: e450241d-b77f-4fe2-9deb-fd096beccb8e
  Args:
    type: :Woman
    source: :Hereditary_Grand_Duchess_Josephine_Charlotte_of_Luxembourg
  AssignClass (5165aea0-fdaf-4066-a8de-9289d0adb808)
 Call ID: 5165aea0-fdaf-4066-a8de-9289d0adb808
  Args:
    type: :Person
    source: :Hereditary_Grand_Duchess_Josephine_Charlotte_of_Luxembourg
  AssignClass (a251e2c0-a23b-4c98-bdeb-ab014caa3e49)
 Call ID: a251e2c0-a23b-4c98-bdeb-ab014caa3e49
  Args:
    source: :Robert_Archduke_of_Austria_Este
    type: :Man
  AssignClass (d808ba4f-592c-4cd9-baf7-beafd1e01a55)
 Call ID: d808ba4f-592c-4cd9-baf7-beafd1e01a55
  Args:
    source: :Robert_Archduke_of_Austria_Este
    type: :Person
  AssignClass (8816ca80-be2f-45d5-b64d-36e45c2da551)
 Call ID: 8816ca80-be2f-45d5-b64d-36e45c2da551
  Args:
    type: :Ancestor
    source: :Robert_Archduke_of_Austria_Este
  AssignClass (840e9c74-2da5-48f2-a742-fbacc4c5e907)
 Call ID: 840e9c74-2da5-48f2-a742-fbacc4c5e907
  Args:
    type: :Woman
    source: :Princess_Margherita_of_Savoy_Aosta
  AssignClass (51abce32-a8d1-48b2-81a0-7f79516c22aa)
 Call ID: 51abce32-a8d1-48b2-81a0-7f79516c22aa
  Args:
    source: :Princess_Margherita_of_Savoy_Aosta
    type: :Person
  AssignClass (85a2bed8-6e98-4e76-b9b5-fc915aaf68d6)
 Call ID: 85a2bed8-6e98-4e76-b9b5-fc915aaf68d6
  Args:
    source: :Princess_Margherita_of_Savoy_Aosta
    type: :Ancestor
  AddLiteral (caad0a5a-142e-4b12-a672-00a39500e2cd)
 Call ID: caad0a5a-142e-4b12-a672-00a39500e2cd
  Args:
    literal_type: xsd:integer
    literal_value: 1962
    relation: :hasBirthYear
    source: :Princess_Astrid_of_Belgium
  AddTriple (6167f5f5-5881-4c19-bacf-f9c7d14d9c14)
 Call ID: 6167f5f5-5881-4c19-bacf-f9c7d14d9c14
  Args:
    target: :King_Albert_II
    relation: :hasFather
    source: :Princess_Astrid_of_Belgium
  AddTriple (7553e9ee-f4e6-4457-8eb7-1b2b0fbfa164)
 Call ID: 7553e9ee-f4e6-4457-8eb7-1b2b0fbfa164
  Args:
    target: :Queen_Paola
    relation: :hasMother
    source: :Princess_Astrid_of_Belgium
  AddTriple (998c13c5-fa62-45f9-ba05-d88aba7cf19e)
 Call ID: 998c13c5-fa62-45f9-ba05-d88aba7cf19e
  Args:
    target: :King_Philippe
    relation: :isSisterOf
    source: :Princess_Astrid_of_Belgium
  AddTriple (2d569423-2b61-4fb3-a804-16bf77226007)
 Call ID: 2d569423-2b61-4fb3-a804-16bf77226007
  Args:
    source: :King_Albert_II
    relation: :isFatherOf
    target: :King_Philippe
  AddTriple (539c0a7e-4849-4b00-a577-1d2af2f7e39f)
 Call ID: 539c0a7e-4849-4b00-a577-1d2af2f7e39f
  Args:
    relation: :isMotherOf
    source: :Queen_Paola
    target: :King_Philippe
  AddLiteral (400c592d-9f3c-4a20-b7c8-2f398c1de621)
 Call ID: 400c592d-9f3c-4a20-b7c8-2f398c1de621
  Args:
    source: :Princess_Astrid_of_Belgium
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1984
  AddTriple (c05fd827-a398-4dc4-990e-e69ce564cf25)
 Call ID: c05fd827-a398-4dc4-990e-e69ce564cf25
  Args:
    target: :Prince_Lorenz_of_Belgium
    source: :Princess_Astrid_of_Belgium
    relation: :hasRelation
  AddTriple (44a8b07c-5b88-4967-9f95-0266fbcc4b6d)
 Call ID: 44a8b07c-5b88-4967-9f95-0266fbcc4b6d
  Args:
    target: :Robert_Archduke_of_Austria_Este
    relation: :hasFather
    source: :Prince_Lorenz_of_Belgium
  AddTriple (098b25f5-fdf8-4278-9f24-e22a1166a871)
 Call ID: 098b25f5-fdf8-4278-9f24-e22a1166a871
  Args:
    relation: :hasMother
    source: :Prince_Lorenz_of_Belgium
    target: :Princess_Margherita_of_Savoy_Aosta
  AddLiteral (b21a8f4c-45b2-48f9-a614-a1ba83e6140f)
 Call ID: b21a8f4c-45b2-48f9-a614-a1ba83e6140f
  Args:
    source: :Robert_Archduke_of_Austria_Este
    relation: :hasDeathYear
    literal_value: 1996
    literal_type: xsd:integer
  AddLiteral (91f5451d-3dc1-4f8d-b576-b67002b106d7)
 Call ID: 91f5451d-3dc1-4f8d-b576-b67002b106d7
  Args:
    source: :Princess_Margherita_of_Savoy_Aosta
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2022
  AddLiteral (935add48-f5be-4b2d-904f-656c22c71268)
 Call ID: 935add48-f5be-4b2d-904f-656c22c71268
  Args:
    source: :Astrid_of_Sweden
    literal_type: xsd:integer
    literal_value: 1935
    relation: :hasDeathYear
  AddTriple (f9c05404-68d9-44ca-b758-2d3c0faacd02)
 Call ID: f9c05404-68d9-44ca-b758-2d3c0faacd02
  Args:
    target: :King_Albert_II
    relation: :isMotherOf
    source: :Astrid_of_Sweden
  AddTriple (beb42fb5-d0cb-405d-86f8-95f2e27dfb8f)
 Call ID: beb42fb5-d0cb-405d-86f8-95f2e27dfb8f
  Args:
    target: :King_Leopold_III
    relation: :hasFather
    source: :King_Albert_II
  AddTriple (65628a6d-cc3f-4a4c-b87e-8faa2450d639)
 Call ID: 65628a6d-cc3f-4a4c-b87e-8faa2450d639
  Args:
    target: :Astrid_of_Sweden
    relation: :hasMother
    source: :King_Albert_II
  Finish (4af45426-1285-4a8d-97e3-f4500c7a945d)
 Call ID: 4af45426-1285-4a8d-97e3-f4500c7a945d
  Args: