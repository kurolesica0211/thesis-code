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


Amedeo of Austria-Este (Habsburg-Lorraine)
Birth and family

Amedeo was born on 21 February 1986 at the Saint-Luc University Hospital in Woluwe-Saint-Lambert, Belgium, as the first child and elder son of Lorenz, Archduke of Austria-Este, and Princess Astrid of Belgium.
Amedeo himself is godfather to his cousin, Princess Elisabeth, Duchess of Brabant.
The couple's wedding was celebrated on 5 July 2014 in Rome's Basilica of Santa Maria in Trastevere, in the presence of the royal family (with the exception of his great-aunt Queen Fabiola), as well as members of the cadet branches of the House of Habsburg-Lorraine, including the bridegroom's grandmother, Margherita of Savoy, Dowager Archduchess of Austria-Este, and members of other dynasties, including Princess Margaretha of Luxembourg and her husband Prince Nikolaus of Liechtenstein, Princess Beatrice of York and Jean-Christophe, Prince Napoléon.
Titles and styles

All the children of Princess Astrid and Archduke Lorenz bear the title of "Prince(ss) of Belgium", with the style of "Royal Highness", by Belgian Royal Decree of 2 December 1991, which is distinct from their traditional Austro-Hungarian titles.



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
  AssignClass (e0cf809f-d8ac-4ef9-a84c-1970f59934d4)
 Call ID: e0cf809f-d8ac-4ef9-a84c-1970f59934d4
  Args:
    type: :Man
    source: Amedeo_of_Austria-Este
  AssignClass (cc829b5d-b4b2-4639-a25a-c7d0a511e3a9)
 Call ID: cc829b5d-b4b2-4639-a25a-c7d0a511e3a9
  Args:
    type: :Person
    source: Amedeo_of_Austria-Este
  AddLiteral (c5806491-18d2-4e86-b846-11d648908474)
 Call ID: c5806491-18d2-4e86-b846-11d648908474
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1986
    source: Amedeo_of_Austria-Este
  AddTriple (d9f4cb29-00c5-430d-93ae-f5fdc9ef0044)
 Call ID: d9f4cb29-00c5-430d-93ae-f5fdc9ef0044
  Args:
    target: Lorenz_Archduke_of_Austria-Este
    relation: :hasFather
    source: Amedeo_of_Austria-Este
  AddTriple (844ce3c4-cfdf-4375-a2eb-2a51fe88faa5)
 Call ID: 844ce3c4-cfdf-4375-a2eb-2a51fe88faa5
  Args:
    target: Princess_Astrid_of_Belgium
    relation: :hasMother
    source: Amedeo_of_Austria-Este
  AssignClass (8b649b6e-423e-44d9-9929-b5762af4e5c1)
 Call ID: 8b649b6e-423e-44d9-9929-b5762af4e5c1
  Args:
    type: :Man
    source: Lorenz_Archduke_of_Austria-Este
  AssignClass (08ad4939-66d6-4bdb-93f3-eb0f2ecbcded)
 Call ID: 08ad4939-66d6-4bdb-93f3-eb0f2ecbcded
  Args:
    source: Lorenz_Archduke_of_Austria-Este
    type: :Person
  AssignClass (3acf259c-7064-4613-926b-96b6e2361291)
 Call ID: 3acf259c-7064-4613-926b-96b6e2361291
  Args:
    type: :Woman
    source: Princess_Astrid_of_Belgium
  AssignClass (1ce72b79-cf40-404e-b686-f85d16ab9e98)
 Call ID: 1ce72b79-cf40-404e-b686-f85d16ab9e98
  Args:
    source: Princess_Astrid_of_Belgium
    type: :Person
  AssignClass (73c75762-1ad6-4a87-ae17-4843115afbe3)
 Call ID: 73c75762-1ad6-4a87-ae17-4843115afbe3
  Args:
    type: :Woman
    source: Princess_Elisabeth_Duchess_of_Brabant
  AssignClass (71405c14-cb24-4e02-a47e-8b7c89e91c6b)
 Call ID: 71405c14-cb24-4e02-a47e-8b7c89e91c6b
  Args:
    source: Princess_Elisabeth_Duchess_of_Brabant
    type: :Person
  AddTriple (be67c0f1-7f02-4ee5-9421-177d6c616b38)
 Call ID: be67c0f1-7f02-4ee5-9421-177d6c616b38
  Args:
    source: Amedeo_of_Austria-Este
    relation: :isBloodrelationOf
    target: Princess_Elisabeth_Duchess_of_Brabant
  AssignClass (efb61b63-333e-4b78-af10-aff34a053e20)
 Call ID: efb61b63-333e-4b78-af10-aff34a053e20
  Args:
    type: :Woman
    source: Margherita_of_Savoy_Dowager_Archduchess_of_Austria-Este
  AssignClass (78fff581-7ffe-49b5-9178-788460e2faae)
 Call ID: 78fff581-7ffe-49b5-9178-788460e2faae
  Args:
    type: :Person
    source: Margherita_of_Savoy_Dowager_Archduchess_of_Austria-Este
  AddTriple (73872050-ef60-428d-8736-d7b8e4e4f149)
 Call ID: 73872050-ef60-428d-8736-d7b8e4e4f149
  Args:
    source: Lorenz_Archduke_of_Austria-Este
    target: Margherita_of_Savoy_Dowager_Archduchess_of_Austria-Este
    relation: :hasMother
  AssignClass (c455f15d-6b97-4541-a2b7-f3b10ee1967e)
 Call ID: c455f15d-6b97-4541-a2b7-f3b10ee1967e
  Args:
    source: Princess_Margaretha_of_Luxembourg
    type: :Woman
  AssignClass (96f25457-1178-4793-8ddb-a373f2bb8b5a)
 Call ID: 96f25457-1178-4793-8ddb-a373f2bb8b5a
  Args:
    type: :Person
    source: Princess_Margaretha_of_Luxembourg
  AssignClass (aa80148f-bfeb-4e75-ad9b-0dbed824c668)
 Call ID: aa80148f-bfeb-4e75-ad9b-0dbed824c668
  Args:
    type: :Man
    source: Prince_Nikolaus_of_Liechtenstein
  AssignClass (8ce4b580-00a8-4df4-a7cb-3d21c44dcb12)
 Call ID: 8ce4b580-00a8-4df4-a7cb-3d21c44dcb12
  Args:
    type: :Person
    source: Prince_Nikolaus_of_Liechtenstein
  AssignClass (82e12cbf-bef0-4aac-b05f-37a9ac800307)
 Call ID: 82e12cbf-bef0-4aac-b05f-37a9ac800307
  Args:
    source: Princess_Beatrice_of_York
    type: :Woman
  AssignClass (9488cce2-3885-43a1-8c92-53e6dab9090f)
 Call ID: 9488cce2-3885-43a1-8c92-53e6dab9090f
  Args:
    source: Princess_Beatrice_of_York
    type: :Person
  AssignClass (005b21e4-8998-40b2-b2f5-615fa2436895)
 Call ID: 005b21e4-8998-40b2-b2f5-615fa2436895
  Args:
    type: :Man
    source: Jean-Christophe_Prince_Napoléon
  AssignClass (a3cb5e9b-1bc4-4d04-b68f-6ea07c67555f)
 Call ID: a3cb5e9b-1bc4-4d04-b68f-6ea07c67555f
  Args:
    type: :Person
    source: Jean-Christophe_Prince_Napoléon
  AssignClass (22a5b53e-28fd-4c63-8691-f1e049479659)
 Call ID: 22a5b53e-28fd-4c63-8691-f1e049479659
  Args:
    source: Queen_Fabiola
    type: :Woman
  AssignClass (0b02f71f-ce30-4343-b562-ef2e6dd8d2c7)
 Call ID: 0b02f71f-ce30-4343-b562-ef2e6dd8d2c7
  Args:
    source: Queen_Fabiola
    type: :Person
  AddTriple (6ea9b7b2-3440-495c-a644-8599828e0b84)
 Call ID: 6ea9b7b2-3440-495c-a644-8599828e0b84
  Args:
    source: Queen_Fabiola
    relation: :isAncestorOf
    target: Amedeo_of_Austria-Este
  AssignClass (ea215ead-59b6-4623-b70e-0170c4367fe8)
 Call ID: ea215ead-59b6-4623-b70e-0170c4367fe8
  Args:
    source: King_Albert_II
    type: :Man
  AssignClass (298a0b73-c2f5-47e6-92b9-b326ba5fe58f)
 Call ID: 298a0b73-c2f5-47e6-92b9-b326ba5fe58f
  Args:
    source: King_Albert_II
    type: :Person
  AssignClass (38c2bfd1-6d3c-4617-9e0a-7d6103369929)
 Call ID: 38c2bfd1-6d3c-4617-9e0a-7d6103369929
  Args:
    source: Queen_Paola
    type: :Woman
  AssignClass (139b48be-6a5a-4504-915d-96c22273b790)
 Call ID: 139b48be-6a5a-4504-915d-96c22273b790
  Args:
    source: Queen_Paola
    type: :Person
  Finish (5a618245-6d74-4a6f-a3f9-76262f20ea07)
 Call ID: 5a618245-6d74-4a6f-a3f9-76262f20ea07
  Args: