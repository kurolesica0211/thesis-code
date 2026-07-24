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
Bertrand of Orléans-Braganza (born 2 February 1941) is the current head of the Vassouras branch of the House of Orléans-Braganza and one of the two principal claimants to the defunct Brazilian throne.
He assumed the position on 15 July 2022, following the death of his elder brother, Luiz of Orléans-Braganza.
The Vassouras branch asserts its claim in opposition to the Petrópolis branch of the Orléans-Braganzas, headed by Pedro Carlos.
Both Bertrand and Pedro Carlos are great-grandsons of Isabel, Princess Imperial of Brazil, daughter and heir of Emperor Pedro II, of the House of Braganza.
Born in Mandelieu-la-Napoule, France, the third child of Pedro Henrique of Orléans-Braganza, and Princess Maria Elisabeth of Bavaria.
Prince Bertrand is an avid traditionalist conservative, anticommunist, and outspoken advocate of right-wing Christian policies.
Although Prince Bertrand and Prince Pedro Carlos are great-grandsons of Emperor Pedro II of Brazil, of the House of Braganza, they disputed the leadership of the Brazilian Imperial Family due to a dynastic dispute regarding their parents, who were cousins.
A member of the Brazilian Imperial House, Prince Bertrand is closely related to the House of Braganza and the House of Orléans (Orleanist claimants), both through his paternal lineage, and with the House of Wittelsbach, through his maternal lineage.
He is the great-grandson of Isabel, Princess Imperial of Brazil and King Ludwig III of Bavaria.
Biography

Early life

The third son of Pedro Henrique of Orléans-Braganza and Princess Maria Elisabeth of Bavaria, his elder brothers are, in order, Luiz of Orléans-Braganza who claimed to be Head of the Brazilian Imperial Family until 2022 and Eudes of Orléans-Braganza, who renounced his dynastic rights to the Brazilian throne in order to marry a commoner.
As with his two elder brothers, Bertrand was born in southern France, 1941, even though the exile imposed on the family had already been revoked, in 1920, due to the Second World War.
Later his family moved to Paraná, where his father bought a farm and Bertrand spent his childhood.
Bertrand is a Traditionalist Catholic and a member of Tradition, Family and Property, of traditionalist Catholic inspiration, founded and directed by the intellectual leader Plinio Corrêa de Oliveira until his death.
Besides Portuguese, his native language, Bertrand is fluent in French and Spanish.
Roles

In recent years, Bertrand is coordinator and spokesman of the movement Paz no Campo (Peace in the fields), and has traveled all over Brazil lecturing for farmers and entrepreneurs in defense of private property and free enterprise.
As the activist and spokesman of the Brazilian Imperial House for the restoration of the monarchy, Bertrand has gained prominence in the national media and, on some occasions, international media, with the rise and spread of monarchist movements throughout the country.
On 22 September 2017 Bertrand participated in the program The Noite com Danilo Gentili, currently the largest talk show in the country, breaking the program's record of audience.
Political opinions

Bertrand supports typically Traditionalist Catholic ideas: he opposes same-sex marriage, favours the illegality of abortion and is against the demarcation of indigenous territory in Brazil.
Honours

As Head of the Brazilian Imperial Family, Bertrand claims the following positions:


Bertrand has also received other honours:


Ancestry

References

External links



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
  AssignClass (a020ed1d-9fd0-4f0d-94db-632fa788e766)
 Call ID: a020ed1d-9fd0-4f0d-94db-632fa788e766
  Args:
    type: :Man
    source: Bertrand_of_Orleans-Braganza
  AssignClass (638388e5-a450-441d-8498-ebcf40fc671b)
 Call ID: 638388e5-a450-441d-8498-ebcf40fc671b
  Args:
    type: :Person
    source: Bertrand_of_Orleans-Braganza
  AddLiteral (98d3a2e2-e645-40ef-94a0-a27d1d065bb1)
 Call ID: 98d3a2e2-e645-40ef-94a0-a27d1d065bb1
  Args:
    source: Bertrand_of_Orleans-Braganza
    relation: :hasBirthYear
    literal_value: 1941
    literal_type: xsd:integer
  AssignClass (66c16633-039d-462c-81cd-8c072b1827ae)
 Call ID: 66c16633-039d-462c-81cd-8c072b1827ae
  Args:
    type: :Man
    source: Luiz_of_Orleans-Braganza
  AssignClass (0f6f6a7f-d117-4cc2-9809-329b8afc348e)
 Call ID: 0f6f6a7f-d117-4cc2-9809-329b8afc348e
  Args:
    type: :Person
    source: Luiz_of_Orleans-Braganza
  AddTriple (6656b224-5875-4638-8bc8-bc334fd7363c)
 Call ID: 6656b224-5875-4638-8bc8-bc334fd7363c
  Args:
    relation: :isBrotherOf
    target: Luiz_of_Orleans-Braganza
    source: Bertrand_of_Orleans-Braganza
  AssignClass (486b7834-0abe-4305-b835-4228d8431409)
 Call ID: 486b7834-0abe-4305-b835-4228d8431409
  Args:
    type: :Man
    source: Pedro_Carlos
  AssignClass (9a47c61e-e03b-411e-a843-b52dc0e499bb)
 Call ID: 9a47c61e-e03b-411e-a843-b52dc0e499bb
  Args:
    type: :Person
    source: Pedro_Carlos
  AssignClass (8c1cee33-4d81-4fbd-9c53-9f597b37c389)
 Call ID: 8c1cee33-4d81-4fbd-9c53-9f597b37c389
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (c88a0200-3a37-4e51-9070-16d6246ea68a)
 Call ID: c88a0200-3a37-4e51-9070-16d6246ea68a
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (7f9d3deb-18a6-46b1-b6a2-52eeace619e6)
 Call ID: 7f9d3deb-18a6-46b1-b6a2-52eeace619e6
  Args:
    type: :Man
    source: Pedro_II_of_Brazil
  AssignClass (456ab890-cbc6-409b-b6d1-22fd440c4599)
 Call ID: 456ab890-cbc6-409b-b6d1-22fd440c4599
  Args:
    type: :Person
    source: Pedro_II_of_Brazil
  AddTriple (dc9bbe29-4b6d-455d-ae1e-014d71736d0e)
 Call ID: dc9bbe29-4b6d-455d-ae1e-014d71736d0e
  Args:
    source: Isabel_Princess_Imperial_of_Brazil
    relation: :isDaughterOf
    target: Pedro_II_of_Brazil
  AssignClass (1f3230f1-c4da-4a77-8ba2-432cd617e44d)
 Call ID: 1f3230f1-c4da-4a77-8ba2-432cd617e44d
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (910ef38f-886f-4448-8e11-4ce052de9de0)
 Call ID: 910ef38f-886f-4448-8e11-4ce052de9de0
  Args:
    type: :Person
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (0e60c1a7-3b93-44a5-9f92-2fd04b2046fd)
 Call ID: 0e60c1a7-3b93-44a5-9f92-2fd04b2046fd
  Args:
    type: :Woman
    source: Maria_Elisabeth_of_Bavaria
  AssignClass (513652bb-3d44-4340-b570-3be1e679ab5c)
 Call ID: 513652bb-3d44-4340-b570-3be1e679ab5c
  Args:
    type: :Person
    source: Maria_Elisabeth_of_Bavaria
  AddTriple (46e4a1e7-c4fe-440f-b645-f402cc9a4a5f)
 Call ID: 46e4a1e7-c4fe-440f-b645-f402cc9a4a5f
  Args:
    relation: :hasFather
    target: Pedro_Henrique_of_Orleans-Braganza
    source: Bertrand_of_Orleans-Braganza
  AddTriple (684ca0f7-4739-49f1-8835-ad3ec09924b7)
 Call ID: 684ca0f7-4739-49f1-8835-ad3ec09924b7
  Args:
    source: Bertrand_of_Orleans-Braganza
    relation: :hasMother
    target: Maria_Elisabeth_of_Bavaria
  AssignClass (49329c29-62c0-44bc-b7ff-f505bd994e0a)
 Call ID: 49329c29-62c0-44bc-b7ff-f505bd994e0a
  Args:
    type: :Man
    source: Eudes_of_Orleans-Braganza
  AssignClass (101f1c68-e19a-469a-b3d4-1303696af5c2)
 Call ID: 101f1c68-e19a-469a-b3d4-1303696af5c2
  Args:
    type: :Person
    source: Eudes_of_Orleans-Braganza
  AddTriple (86fe9ae6-b133-438b-a7c3-746f64ea7932)
 Call ID: 86fe9ae6-b133-438b-a7c3-746f64ea7932
  Args:
    source: Bertrand_of_Orleans-Braganza
    target: Eudes_of_Orleans-Braganza
    relation: :isBrotherOf
  AssignClass (961b1b38-8871-4c54-bc2b-2c21926da44c)
 Call ID: 961b1b38-8871-4c54-bc2b-2c21926da44c
  Args:
    type: :Man
    source: Ludwig_III_of_Bavaria
  AssignClass (5b94c968-08ae-4969-b105-465486289b4a)
 Call ID: 5b94c968-08ae-4969-b105-465486289b4a
  Args:
    type: :Person
    source: Ludwig_III_of_Bavaria
  Finish (d908ca38-be1b-4d70-8bf5-4d9b3cfaa4a0)
 Call ID: d908ca38-be1b-4d70-8bf5-4d9b3cfaa4a0
  Args: